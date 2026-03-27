# utils/ai_services.py
"""
Central module for handling all interactions with external AI services like
OpenAI and Google Gemini.

INDEX
-----
1.  Imports & Client Initialisation
2.  AI Service Callers
"""

# ===========================================================================
# 1. Imports & Client Initialisation
# ===========================================================================
import logging
import json
import uuid
from time import time
from openai import OpenAI
try:
    import google.generativeai as genai  # type: ignore
    from google.generativeai import client as genai_client  # type: ignore
    from google.generativeai import generative_models as genai_models  # type: ignore
    configure = getattr(genai_client, "configure", None)
    GenerativeModel = getattr(genai_models, "GenerativeModel", None)
except Exception:  # pragma: no cover - optional dependency
    genai = None  # type: ignore
    configure = None  # type: ignore
    GenerativeModel = None  # type: ignore
import application.config as config

logger = logging.getLogger(__name__)


def _contains_people_of_reeds_signature(text: str) -> bool:
    return "people of the reeds" in str(text or "").lower()


def _is_heart_section(title: str) -> bool:
    return "heart" in str(title or "").strip().lower()


def _format_aspect_ratio_label(value: str | None) -> str:
    txt = str(value or "").strip()
    if not txt:
        return "UNSET"

    ratio = txt.replace("x", ":")
    parts = ratio.split(":")
    orientation = None
    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
        w = int(parts[0])
        h = int(parts[1])
        if w == h:
            orientation = "Square"
        elif w > h:
            orientation = "Landscape"
        else:
            orientation = "Portrait"

    return f"{ratio} {orientation}" if orientation else ratio


def _sanitize_title(value: str | None) -> str:
    return str(value or "").replace("|", ",").strip()

# Initialize the OpenAI client
client = OpenAI(
    api_key=config.OPENAI_API_KEY,
    project=config.OPENAI_PROJECT_ID,
)


def _chat_create_sanitized(**kwargs):
    """Wrapper for client.chat.completions.create with model-specific guards."""
    # [CRITICAL FIX] GPT-5/o1 models DO NOT support temperature/max_tokens
    model = kwargs.get('model', '') or ''
    if model.startswith(('gpt-5', 'o1', 'o3')) or 'reasoning' in model:
        # 1. Remove temperature
        kwargs.pop('temperature', None)

        # 2. Rename max_tokens -> max_completion_tokens (if required by SDK)
        if 'max_tokens' in kwargs:
            kwargs['max_completion_tokens'] = kwargs.pop('max_tokens')

        print(f"🔹 Sanitized args for {model}: Removed temperature/adjusted tokens")

    return client.chat.completions.create(**kwargs)

# Configure and initialize the Google Gemini client
gemini_model = None
if config.GEMINI_API_KEY and configure and GenerativeModel:
    try:
        configure(api_key=config.GEMINI_API_KEY)
        gemini_model = GenerativeModel(getattr(config, "GEMINI_MODEL", "gemini-1.5-flash"))
        logger.info("Google Gemini client configured successfully.")
    except Exception as e:
        logger.exception("Failed to configure Google Gemini client: %s", e)

def get_gemini_model():
    """Returns the initialized Gemini model if available."""
    return gemini_model

# ===========================================================================
# 2. AI Service Callers
# ===========================================================================

def call_ai_to_generate_title(paragraph_content: str) -> str:
    """Uses AI to generate a short, compelling title for a block of text."""
    try:
        prompt = (
            f"Generate a short, compelling heading (5 words or less) for the following paragraph. "
            f"Respond only with the heading text, nothing else.\n\nPARAGRAPH:\n\"{paragraph_content}\""
        )
        response = _chat_create_sanitized(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
        )
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            title = _sanitize_title(response.choices[0].message.content.strip().strip('"'))
            logger.info(f"AI generated title: '{title}'")
            return title
        logger.warning("AI title generation returned no content.")
        return "AI Title Generation Failed"
    except Exception as e:
        logger.error(f"AI title generation failed: {e}")
        return "AI Title Generation Failed"


def call_ai_to_rewrite(prompt: str, provider: str = "openai") -> str:
    """Calls the specified AI provider to rewrite text based on a prompt."""
    if provider != "openai":
        return "Error: Only OpenAI is currently supported for rewriting."

    try:
        response = _chat_create_sanitized(
            model=config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert copywriter. Rewrite the following text based on the user's instruction. Respond only with the rewritten text, without any extra commentary."},
                {"role": "user", "content": prompt},
            ],
        )
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            new_text = response.choices[0].message.content.strip()
            logger.info("AI successfully rewrote text based on prompt.")
            return new_text
        logger.warning("AI rewrite returned no content.")
        return "Error: AI returned an empty response."
    except Exception as e:
        logger.error(f"AI text rewrite failed: {e}")
        return f"Error during AI regeneration: {e}"


def call_ai_to_reword_text(provider: str, artwork_description: str, generic_text: str) -> str:
    """
    Uses an AI provider to reword generic text to blend with a specific artwork description.
    """
    provider = (provider or "openai").lower()
    logger.info(f"Initiating generic text rewording with provider: {provider}")

    desired_min_tokens = getattr(config, 'OPENAI_MIN_TOKENS_REWORD', 8000)
    max_tokens_cap = getattr(config, 'OPENAI_MAX_TOKENS_REWORD', 10000)
    # We can't enforce a true *minimum* with OpenAI; we strongly instruct and, if short, retry with an explicit expansion instruction.
    base_instructions = f"""You are an expert SEO copywriter for digital art marketplaces.

TASK: Reword the 'Generic Text' so it is unique, naturally follows the 'Artwork Description', and is richly expanded while preserving every factual detail (file types, dimensions, delivery info, usage notes, licensing, FAQs etc.).

OUTPUT LENGTH TARGET:
- Produce at least ~{desired_min_tokens} tokens of high-quality, non-repetitive copy (can exceed; do NOT truncate early).
- Use varied sentence structure and logically ordered sections / paragraphs. It's acceptable (preferred) to elaborate with clarifying, buyer-helpful detail provided it does not invent new unverified claims.

STRICT REQUIREMENTS:
1. Preserve ALL concrete facts (numbers, dimensions, file formats, usage rights).
2. May reorganise for clarity, may merge / split paragraphs logically.
3. No boilerplate filler; expand with genuinely helpful, relevant detail (printing guidance, styling ideas, contextual relevance) grounded in the given content.
4. No emojis, no ALL CAPS marketing hype. Professional, warm, trustworthy tone (AU spelling if ambiguous).
5. Output ONLY the expanded reworded text (no headings like 'Reworded Version', no meta commentary).
6. If original contains bullet lists, you may format helpful lists, but retain each factual item.
7. Avoid verbatim copying more than short phrases; paraphrase thoroughly.

---
Artwork Description (context for style & thematic blending):
{artwork_description}
---
Original Generic Text (must preserve all factual content, but rewrite & expand):
{generic_text}
---
BEGIN REWRITTEN TEXT BELOW THIS LINE (no preface):
"""

    if provider == "openai":
        try:
            # First attempt (chat completions path; uses max_tokens)
            primary_model = getattr(config, "OPENAI_MODEL", "gpt-4o")
            fallback_model = getattr(config, "OPENAI_MODEL_FALLBACK", "gpt-4-turbo")
            response = _chat_create_sanitized(
                model=primary_model,
                messages=[
                    {"role": "system", "content": "You are an expert SEO copywriter specializing in digital art listings."},
                    {"role": "user", "content": base_instructions},
                ],
                max_tokens=max_tokens_cap,
            )
            if response.choices and response.choices[0].message and response.choices[0].message.content:
                reworded_text = response.choices[0].message.content.strip()
                approx_tokens = int(len(reworded_text.split()) * 1.33)
                if approx_tokens < desired_min_tokens * 0.9 and max_tokens_cap >= desired_min_tokens:  # allow a 10% grace
                    logger.info("Reworded text below desired minimum tokens (%d < %d); issuing expansion retry.", approx_tokens, desired_min_tokens)
                    expansion_prompt = ("Expand further while keeping all existing content intact. Add more practical depth: printing guidance, display ideas, gifting, styling suggestions, archival quality notes, sustainable considerations, and FAQ-style clarifications. Maintain tone constraints. Output only expanded text.")
                    retry = _chat_create_sanitized(
                        model=primary_model,
                        messages=[
                            {"role": "system", "content": "You are an expert SEO copywriter specializing in digital art listings."},
                            {"role": "user", "content": base_instructions},
                            {"role": "assistant", "content": reworded_text},
                            {"role": "user", "content": expansion_prompt},
                        ],
                        max_tokens=max_tokens_cap,
                    )
                    if retry.choices and retry.choices[0].message and retry.choices[0].message.content:
                        second = retry.choices[0].message.content.strip()
                        # Prefer longer if sensible
                        if len(second) > len(reworded_text):
                            reworded_text = second
                logger.info("Successfully reworded generic text with OpenAI (len=%d chars).", len(reworded_text))
                return reworded_text
            logger.warning("OpenAI rewording returned no content.")
            raise RuntimeError("AI returned an empty response.")
        except Exception as e_primary:
            # Fallback attempt with backup model
            logger.warning("OpenAI primary model failed: %s; retrying with fallback", e_primary)
            try:
                response = _chat_create_sanitized(
                    model=fallback_model,
                    messages=[
                        {"role": "system", "content": "You are an expert SEO copywriter specializing in digital art listings."},
                        {"role": "user", "content": base_instructions},
                    ],
                    max_tokens=max_tokens_cap,
                )
                if response.choices and response.choices[0].message and response.choices[0].message.content:
                    reworded_text = response.choices[0].message.content.strip()
                    logger.info("Successfully reworded generic text with OpenAI fallback model.")
                    return reworded_text
                raise RuntimeError("AI fallback returned an empty response.")
            except Exception as e_fallback:
                logger.error("OpenAI fallback rewording failed: %s", e_fallback)
                raise
    
    elif provider == "gemini":
        model = get_gemini_model()
        if not model:
            raise RuntimeError("Gemini client is not configured. Check API key.")
        try:
            # Gemini path uses same base instructions (no multi-turn retry logic implemented here)
            response = model.generate_content(base_instructions)
            reworded_text = response.text.strip()
            logger.info("Successfully reworded generic text with Gemini.")
            return reworded_text
        except Exception as e:
            logger.error(f"Gemini rewording service error: {e}")
            raise
    
    else:
        logger.error(f"Unsupported provider for rewording: {provider}")
        raise ValueError("Unsupported provider specified")


# ===========================================================================
# 3. Unified Listing Block Rewriter (GDWS + Generic Reword)                ==
# ===========================================================================
def rewrite_listing_block(
    *,
    slug: str,
    sku: str | None,
    title: str,
    aspect_ratio: str,
    print_sizes: list[str],
    artist_bio_snippet: str,
    medium_style: str | None,
    licensing: str | None,
    marketplace: str | None,
    block_title: str,
    current_text: str,
    instructions: str | None = None,
    provider: str = "openai",
    temperature: float = 0.70,
) -> dict:
    """Rewrite (regenerate) a single listing paragraph block using a unified
    system+user prompt with cultural guardrails.

    Returns dict: {
        ok: bool,
        new_text: str,              # rewritten (or original on failure)
        trace_id: str,              # UUID for log correlation
        model: str,
        provider: str,
        warning: str|None,
        prompt_tokens_approx: int   # rough heuristic (words*1.3)
    }
    """
    trace_id = uuid.uuid4().hex
    provider_lc = (provider or "openai").lower()
    model = getattr(config, "OPENAI_MODEL", "gpt-4o")
    fallback_model = getattr(config, "OPENAI_MODEL_FALLBACK", "gpt-4-turbo")

    # Defensive normalisation
    slug = (slug or "").strip()
    title = (title or "Untitled Artwork").strip()
    aspect_ratio = _format_aspect_ratio_label((aspect_ratio or "4x5").strip())
    block_title = (block_title or "Paragraph").strip()
    current_text = (current_text or "").strip()
    instructions = (instructions or "").strip()
    artist_bio_snippet = (artist_bio_snippet or "").strip()
    medium_style = (medium_style or "").strip()
    licensing = (licensing or "").strip()
    marketplace = (marketplace or "Generic Marketplace").strip() or "Generic Marketplace"
    print_sizes = [s.strip() for s in (print_sizes or []) if s.strip()]

    if provider_lc != "openai":
        return {
            "ok": False,
            "new_text": current_text,
            "trace_id": trace_id,
            "model": model,
            "provider": provider_lc,
            "warning": "Unsupported provider",
            "prompt_tokens_approx": 0,
        }

    system_msg = (
        "You are a professional fine-art listings copywriter. Rewrite the block provided. "
        "Tone: warm, trustworthy, concise, naturally persuasive. Preserve factual meaning, update style. "
        "CULTURAL ACKNOWLEDGEMENT: We acknowledge the Boandik people as the Traditional Owners of the land where the artist lives and works, and pay our respects to Elders past and present. "
        "Respect Aboriginal culture: never claim sacred/secret knowledge, never invent Dreaming stories. "
        "Do not add emojis, no ALL CAPS headings, no salesy hype. Keep paragraphs 1–4 sentences."
    )

    size_section = "\n".join([f"* {ps}" for ps in print_sizes]) if print_sizes else "(sizes unavailable)"

    user_template = f"""---
META:
- Slug: {slug}
- SKU: {sku or '-'}
- Title: {title}
- Aspect Ratio: {aspect_ratio}
- Medium/Style: {medium_style or '-'}
- Licensing: {licensing or '-'}
- Marketplace: {marketplace}
- Artist Bio Snippet: {artist_bio_snippet or '-'}
- Target Block Title: {block_title}
- Print Sizes (display list):\n{size_section}

CURRENT BLOCK TEXT:
{current_text}

INSTRUCTIONS (editor guidance):
{instructions or '(none)'}

REWRITE REQUIREMENTS:
1) Keep core facts; remove repetition and fluff.
2) If block lists sizes, use bullet list exactly as given (update style only if improves clarity); else don't fabricate sizes.
3) Avoid repeating the artwork title more than once.
4) Cultural: Do NOT infer or assert sacred meaning; only use explicit supplied info.
5) Maintain similar length (±15%).
6) Output ONLY rewritten paragraph text (no JSON, no heading line unless the original started with a heading). If input begins with a heading line, keep/improve it.
---"""

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_template},
    ]

    # Approx token heuristic (OpenAI not called yet)
    prompt_tokens_approx = int(sum(len(m["content"].split()) for m in messages) * 1.3)

    start_ts = time()
    warning = None
    new_text = current_text
    try:
        # Dynamic ceiling: approximate input tokens (words*1.35) * expansion factor (default 1.9) then clamp
        words_in = len(current_text.split()) or 1
        approx_input_tokens = int(words_in * 1.35)
        expansion_factor = getattr(config, 'OPENAI_BLOCK_EXPANSION_FACTOR', 1.9) or 1.9
        dyn_cap = int(approx_input_tokens * expansion_factor)
        hard_cap = getattr(config, 'OPENAI_MAX_TOKENS_REWRITE_BLOCK', 2200)
        max_tokens_use = max(600, min(dyn_cap, hard_cap))  # ensure >=600 for long blocks
        resp = client.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore[arg-type]
            max_tokens=max_tokens_use,
        )
    except Exception as e_first:  # retry once with fallback
        logger.warning("rewrite_listing_block primary model failed: %s (trace_id=%s) - retrying fallback", e_first, trace_id)
        try:
            resp = client.chat.completions.create(
                model=fallback_model,
                messages=messages,  # type: ignore[arg-type]
                max_tokens=max_tokens_use,
            )
            model = fallback_model
        except Exception as e_second:  # Hard failure -> fallback to original
            warning = f"AI failure: {e_second}"[:500]
            logger.error(
                "rewrite_listing_block failure: %s | slug=%s block=%s trace_id=%s", e_second, slug, block_title, trace_id,
                exc_info=True,
            )
            return {
                "ok": False,
                "new_text": current_text,
                "trace_id": trace_id,
                "model": model,
                "provider": provider_lc,
                "warning": warning,
                "prompt_tokens_approx": prompt_tokens_approx,
            }

    try:
        choice = resp.choices[0].message.content if resp.choices and resp.choices[0].message else ""
        if choice:
            new_text = choice.strip()
    except Exception:  # pragma: no cover - defensive
        warning = "Malformed AI response; using original text"
        new_text = current_text

    if _is_heart_section(block_title) and not _contains_people_of_reeds_signature(new_text):
        logger.warning(
            "rewrite_listing_block HEART missing People of the Reeds signature; retrying once (trace_id=%s slug=%s)",
            trace_id,
            slug,
        )
        try:
            retry_messages = [
                *messages,
                {"role": "assistant", "content": new_text},
                {
                    "role": "user",
                    "content": "Mandatory fix: this HEART section MUST explicitly include the exact phrase 'People of the Reeds'. Rewrite again and include it naturally.",
                },
            ]
            retry = client.chat.completions.create(
                model=model,
                messages=retry_messages,  # type: ignore[arg-type]
                max_tokens=max_tokens_use,
            )
            choice2 = retry.choices[0].message.content if retry.choices and retry.choices[0].message else ""
            candidate = choice2.strip() if choice2 else new_text
            if _contains_people_of_reeds_signature(candidate):
                new_text = candidate
            else:
                warning = "HEART rewrite missing People of the Reeds signature; kept original text"
                new_text = current_text
        except Exception as exc:  # pragma: no cover - best-effort
            warning = f"HEART rewrite enforcement failed: {exc}"[:500]
            new_text = current_text

    duration_ms = int((time() - start_ts) * 1000)

    log_obj = {
        "event": "ai.rewrite_block",
        "trace_id": trace_id,
        "slug": slug,
        "block_title": block_title,
        "provider": provider_lc,
        "model": model,
        "temperature": temperature,
        "prompt_tokens_approx": prompt_tokens_approx,
        "duration_ms": duration_ms,
        "len_input_chars": len(current_text),
        "len_output_chars": len(new_text),
        "had_warning": bool(warning),
    }
    try:
        logger.info("AI_REWRITE %s", json.dumps(log_obj, ensure_ascii=False))
    except Exception:
        logger.info("AI_REWRITE trace_id=%s slug=%s block=%s", trace_id, slug, block_title)

    return {
        "ok": True,
        "new_text": new_text or current_text,
        "trace_id": trace_id,
        "model": model,
        "provider": provider_lc,
        "warning": warning,
        "prompt_tokens_approx": prompt_tokens_approx,
    }


def rewrite_section_with_context(
    *,
    model: str,
    provider: str,
    api_key: str | None,
    section_title: str,
    section_text: str,
    context: dict,
    instructions: str | None = None,
    temperature: float = 0.5,
) -> str:
    """Lightweight wrapper for rewriting a generic or GDWS section.
    Returns rewritten text (plain string) or original on failure.
    """
    if (provider or 'openai').lower() != 'openai':
        return section_text
    sec_title = section_title or 'Section'
    sec_text = (section_text or '').strip()
    instructions = (instructions or '').strip()
    print_sizes = context.get('print_sizes') or []
    bio = context.get('artist_bio_snippet') or ''
    licensing = context.get('licensing') or {}
    generic_blocks = context.get('generic_blocks') or []
    # Summarise generic block titles only to reduce prompt size
    block_titles = ", ".join([b.get('title','') for b in generic_blocks][:12])
    sizes_bullets = "\n".join([f"* {s}" for s in print_sizes]) if print_sizes else ""
    system_msg = (
        "You are an art-listing copywriter. Output plain text only. "
        "Respect Aboriginal culture; do not invent sacred or secret details. AU spelling."
    )
    user_parts = [
        f"Title: {context.get('title')}",
        f"Slug: {context.get('slug')}",
        f"Aspect: {context.get('aspect')}",
        f"Print Sizes:\n{sizes_bullets}" if sizes_bullets else "",
        f"Artist Bio Snippet: {bio}" if bio else "",
        f"Licensing: digital_download={licensing.get('digital_download')} personal_use_only={licensing.get('personal_use_only')}",
        f"Generic Block Titles: {block_titles}" if block_titles else "",
        f"Current Section Title: {sec_title}",
        f"Current Section Text:\n{sec_text}",
        f"Instructions: {instructions}" if instructions else "",
        "Rewrite only the section text. Keep the heading line unchanged if present. Maintain meaning, tighten style, no emojis, no ALL CAPS, similar length (±15%).",
    ]
    user_content = "\n".join([p for p in user_parts if p])
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_content},
    ]
    try:
        words_in = len(sec_text.split()) or 1
        approx_input_tokens = int(words_in * 1.35)
        expansion_factor = getattr(config, 'OPENAI_BLOCK_EXPANSION_FACTOR', 1.9) or 1.9
        dyn_cap = int(approx_input_tokens * expansion_factor)
        hard_cap = getattr(config, 'OPENAI_MAX_TOKENS_SECTION', 2200)
        max_tokens_use = max(600, min(dyn_cap, hard_cap))
        resp = client.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore[arg-type]
            max_tokens=max_tokens_use,
        )
        choice = resp.choices[0].message.content if resp.choices and resp.choices[0].message else ''
        candidate = choice.strip() if choice else sec_text

        if _is_heart_section(sec_title) and not _contains_people_of_reeds_signature(candidate):
            retry_messages = [
                *messages,
                {"role": "assistant", "content": candidate},
                {
                    "role": "user",
                    "content": "Mandatory fix: this HEART section MUST explicitly include the exact phrase 'People of the Reeds'. Rewrite again and include it naturally.",
                },
            ]
            retry = client.chat.completions.create(
                model=model,
                messages=retry_messages,  # type: ignore[arg-type]
                max_tokens=max_tokens_use,
            )
            choice2 = retry.choices[0].message.content if retry.choices and retry.choices[0].message else ''
            candidate2 = choice2.strip() if choice2 else candidate
            return candidate2 if _contains_people_of_reeds_signature(candidate2) else sec_text

        return candidate
    except Exception as e:  # pragma: no cover - fallback path
        logger.warning("rewrite_section_with_context failure: %s", e)
        return sec_text