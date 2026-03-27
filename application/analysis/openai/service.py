from __future__ import annotations

import base64
import json
import logging
import shutil
from io import BytesIO
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Any
from uuid import uuid4

from flask import current_app

import application.config as config
from application.common.utilities.files import write_bytes_atomic, write_json_atomic, sanitize_etsy_filename
from application.upload.services import storage_service
from application.utils.ai_services import client as openai_client

from PIL import Image
try:
    from openai import (
        APIConnectionError,
        APITimeoutError,
        AuthenticationError,
        BadRequestError,
        NotFoundError,
        PermissionDeniedError,
        RateLimitError,
    )
except Exception:  # pylint: disable=broad-except
    APIConnectionError = None  # type: ignore
    APITimeoutError = None  # type: ignore
    AuthenticationError = None  # type: ignore
    BadRequestError = None  # type: ignore
    PermissionDeniedError = None  # type: ignore
    RateLimitError = None  # type: ignore
    from openai import NotFoundError

from application.analysis import prompts

from .schema import OpenAIArtworkAnalysis


class OpenAIAnalysisError(RuntimeError):
    pass


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (bytes, bytearray)):
        return str(value)
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(v) for v in value]
    try:
        return float(value)
    except Exception:
        return str(value)


def _classify_openai_error(exc: Exception) -> str:
    msg = str(exc or "").strip().lower()

    if AuthenticationError is not None and isinstance(exc, AuthenticationError):
        return "ERR_AUTH"
    if PermissionDeniedError is not None and isinstance(exc, PermissionDeniedError):
        return "ERR_AUTH"
    if RateLimitError is not None and isinstance(exc, RateLimitError):
        return "ERR_RATE_LIMIT"
    if APITimeoutError is not None and isinstance(exc, APITimeoutError):
        return "ERR_TIMEOUT"
    if APIConnectionError is not None and isinstance(exc, APIConnectionError):
        return "ERR_TIMEOUT"
    if isinstance(exc, NotFoundError):
        return "ERR_MODEL"
    if BadRequestError is not None and isinstance(exc, BadRequestError):
        if "model" in msg and "not" in msg and "found" in msg:
            return "ERR_MODEL"
        return "ERR_BAD_REQUEST"

    if "rate limit" in msg or "too many requests" in msg:
        return "ERR_RATE_LIMIT"
    if "timeout" in msg or "timed out" in msg:
        return "ERR_TIMEOUT"
    if "invalid api key" in msg or "incorrect api key" in msg or "authentication" in msg:
        return "ERR_AUTH"
    if "insufficient_quota" in msg or "insufficient quota" in msg or "quota" in msg or "billing" in msg or "balance" in msg:
        return "ERR_BALANCE"
    if "model" in msg and "not" in msg and "found" in msg:
        return "ERR_MODEL"
    return "ERR_UNKNOWN"


def _raise_openai_error(*, message: str, error_code: str, cause: Exception) -> None:
    err = OpenAIAnalysisError(message)
    setattr(err, "error_code", error_code)
    raise err from cause


def _log_openai_exception(*, log: logging.Logger, sku: str, exc: Exception, model: str, prompt_id: str) -> None:
    extra_parts: list[str] = []
    for key in ("status_code", "code", "type"):
        val = getattr(exc, key, None)
        if val is not None:
            extra_parts.append(f"{key}={val}")
    body = getattr(exc, "body", None)
    if body is not None:
        try:
            extra_parts.append(f"body={json.dumps(body, ensure_ascii=False)[:2000]}")
        except Exception:
            extra_parts.append(f"body={str(body)[:2000]}")

    details = " ".join(extra_parts).strip()
    if details:
        log.error("[%s] OpenAI API error: model=%s prompt_id=%s %s", sku, model, prompt_id, details)
    log.exception("[%s] OpenAI API exception: model=%s prompt_id=%s message=%s", sku, model, prompt_id, str(exc))


def _should_fallback_to_gpt4o(exc: Exception) -> bool:
    """Detect OpenAI 400s caused by model/parameter incompatibility."""
    msg = str(exc or "")
    if "Unsupported parameter: 'max_tokens'" in msg:
        return True
    if "Use 'max_completion_tokens' instead" in msg:
        return True
    if "Unsupported value: 'temperature'" in msg:
        return True

    body = getattr(exc, "body", None)
    if isinstance(body, dict):
        err = body.get("error") if isinstance(body.get("error"), dict) else body
        param = (err.get("param") if isinstance(err, dict) else None)
        code = (err.get("code") if isinstance(err, dict) else None)
        if param in {"max_tokens", "temperature"}:
            return True
        if code in {"unsupported_parameter", "unsupported_value"}:
            return True

    return False


def _supports_temperature(model_name: str) -> bool:
    model_lower = (model_name or "").strip().lower()
    if model_lower.startswith(("o1", "gpt-5", "o3")) or "reasoning" in model_lower:
        return False
    return True


def _is_temperature_unsupported(exc: Exception) -> bool:
    msg = str(exc or "")
    if "Unsupported value: 'temperature'" in msg:
        return True
    body = getattr(exc, "body", None)
    if isinstance(body, dict):
        err = body.get("error") if isinstance(body.get("error"), dict) else body
        param = (err.get("param") if isinstance(err, dict) else None)
        code = (err.get("code") if isinstance(err, dict) else None)
        if param == "temperature" and code == "unsupported_value":
            return True
    return False


def _now_iso() -> str:
    """Return current timestamp in Adelaide, South Australian time (ISO 8601 format)."""
    adelaide_tz = ZoneInfo("Australia/Adelaide")
    return datetime.now(adelaide_tz).isoformat()


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _format_aspect_ratio_label(value: Any) -> str | None:
    if value is None:
        return None

    raw = value
    if isinstance(raw, dict):
        label = raw.get("label") if isinstance(raw.get("label"), str) else None
        if label and label.strip():
            raw = label.strip()
        else:
            return None

    if not isinstance(raw, str):
        return None

    txt = raw.strip()
    if not txt or txt.upper() == "UNSET":
        return None

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


def _sanitize_etsy_title(value: Any) -> str:
    import re
    title = str(value or "").strip()
    if not title:
        return ""
    # Remove forbidden Etsy characters: colons, semicolons, em-dashes, quotes, brackets, slashes, etc.
    # Keep only: letters, numbers, spaces, hyphens, ampersands, pipes
    title = re.sub(r'[:\;\u2014"\'()\[\]{}/\\]', '', title)
    # Replace em-dashes with hyphens
    title = title.replace('\u2014', '-')
    # Clean up multiple spaces
    title = " ".join(title.split()).strip()
    # Truncate to 140 chars max
    if len(title) > 140:
        title = title[:140].rstrip()
    return title


def _aspect_ratio_key(value: Any) -> str | None:
    label = _format_aspect_ratio_label(value)
    if not label:
        return None
    ratio = label.split()[0].strip()
    if ratio in {"2:3", "3:4", "4:5"}:
        return ratio
    return None


def _save_request_log(
    messages: list[dict[str, Any]],
    model: str,
    temperature: float,
    seed_info: dict[str, Any] | None,
    processed_dir: Path,
    sku: str,
) -> None:
    """
    Save OpenAI request details as Markdown for debugging.

    Captures the full payload (prompts, model, config) sent to OpenAI before the API call.
    Saves to listing-request.md in the processed artwork directory.

    Args:
        messages: The messages array (system + user prompts)
        model: Model name (e.g., "gpt-4o")
        temperature: Temperature setting
        seed_info: Seed context dict (location, sentiment, original_prompt)
        processed_dir: Path to processed artwork directory
        sku: Artwork SKU for logging
    """
    try:
        # Extract system prompt
        system_prompt = ""
        if messages and len(messages) > 0:
            system_prompt = messages[0].get("content", "")

        # Extract user prompt text and detect image
        user_text = ""
        has_image = False
        if messages and len(messages) > 1:
            user_content = messages[1].get("content", [])
            if isinstance(user_content, list):
                for item in user_content:
                    if isinstance(item, dict):
                        if item.get("type") == "text":
                            user_text = item.get("text", "")
                        elif item.get("type") == "image_url":
                            has_image = True

        # Format seed context
        location = ""
        sentiment = ""
        has_original_prompt = False
        if seed_info:
            location = seed_info.get("location", "")
            sentiment = seed_info.get("sentiment", "")
            has_original_prompt = bool(seed_info.get("original_prompt"))

        # Build Markdown (with proper formatting to pass linting)
        # Use Adelaide, South Australian time
        adelaide_tz = ZoneInfo("Australia/Adelaide")
        now_adelaide = datetime.now(adelaide_tz)
        timestamp = now_adelaide.isoformat()
        
        # Format filename timestamp (e.g., "01-mar-2026-1-57pm") in Adelaide time
        filename_timestamp = now_adelaide.strftime("%d-%b-%Y-%I-%M%p").lower()
        
        md_lines = [
            "# OpenAI Analysis Request Log",
            "",
            f"**Artwork:** {sku}  ",
            f"**Model:** {model}  ",
            f"**Temperature:** {temperature}  ",
            f"**Timestamp:** {timestamp}",
            "",
            "## Seed Context",
            "",
            f"- **Location:** {location or 'Not provided'}",
            f"- **Sentiment:** {sentiment or 'Not provided'}",
            f"- **Original Prompt:** {'Present (not shown for privacy)' if has_original_prompt else 'Not provided'}",
            "",
            "## System Prompt",
            "",
            "```markdown",
            system_prompt,
            "```",
            "",
            "## User Prompt",
            "",
            "### Text Content",
            "",
            "```",
            user_text,
            "```",
            "",
            "### Image",
            "",
            "Base64-encoded image provided (not shown for brevity)" if has_image else "No image",
            "",
        ]

        md_content = "\n".join(md_lines)
        # Include timestamp in filename to show when analysis was run
        # SKU-prefixed format: {sku}-listing-request-{timestamp}.md
        log_path = processed_dir / f"{sku.lower()}-listing-request-{filename_timestamp}.md"

        # Write to file (non-blocking on error)
        log_path.write_text(md_content, encoding="utf-8")

    except Exception as exc:  # pylint: disable=broad-except
        # Non-breaking: Log warning but don't interrupt analysis
        log = logging.getLogger("ai_processing")
        log.warning("[%s] Failed to save request log: %s", sku, exc)


def _write_conversation_log(
    slug: str,
    sku: str,
    processed_dir: Path,
    messages: list[dict[str, Any]],
    response: dict[str, Any] | None,
    rejection: str | None = None,
    append_mode: bool = False,
) -> None:
    """Write AI conversation (request + response) to SKU-prefixed Markdown file.
    
    Creates or appends to {slug}/{sku}-ai-conversation.md with full back-and-forth
    for transparency and debugging. If retry happens, the function appends to preserve
    the full interaction history.
    
    Args:
        slug: Artwork slug for directory
        sku: Artwork SKU for filename
        processed_dir: Path to processed artwork directory
        messages: The messages sent to OpenAI (system + user)
        response: The structured response from OpenAI (parsed analysis)
        rejection: If provided, prepends ⚠️ REJECTED: {rejection}
        append_mode: If True, appends to existing file (for retries)
    """
    try:
        conversation_path = processed_dir / f"{sku.lower()}-ai-conversation.md"
        
        # Extract system prompt
        system_prompt = ""
        if messages and len(messages) > 0:
            system_prompt = messages[0].get("content", "")
        
        # Extract user prompt text
        user_text = ""
        if messages and len(messages) > 1:
            user_content = messages[1].get("content", [])
            if isinstance(user_content, list):
                for item in user_content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        user_text = item.get("text", "")
                        break
        
        # Format markdown content
        lines = []
        
        if not append_mode:
            # First interaction - add header
            lines.append(f"# AI Conversation Log: {sku}")
            lines.append("")
        
        if rejection:
            # Prepend rejection notice
            lines.append(f"⚠️ REJECTED: {rejection}")
            lines.append("")
        
        # Request section
        lines.append("### 👤 REQUEST (SYSTEM & CONTEXT)")
        lines.append("")
        lines.append("**System Prompt:**")
        lines.append("")
        lines.append("```markdown")
        lines.append(system_prompt)
        lines.append("```")
        lines.append("")
        lines.append("**User Prompt:**")
        lines.append("")
        lines.append("```")
        lines.append(user_text)
        lines.append("```")
        lines.append("")
        
        # Response section
        lines.append("### 🤖 AI RESPONSE")
        lines.append("")
        if response:
            lines.append("```json")
            lines.append(json.dumps(response, indent=2))
            lines.append("```")
        else:
            lines.append("No response received")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        
        content = "\n".join(lines)
        
        if append_mode and conversation_path.exists():
            # Append to existing file
            existing = conversation_path.read_text(encoding="utf-8")
            conversation_path.write_text(existing + content, encoding="utf-8")
        else:
            # Write or overwrite
            conversation_path.write_text(content, encoding="utf-8")
    
    except Exception as exc:  # pylint: disable=broad-except
        log = logging.getLogger("ai_processing")
        log.warning("[%s] Failed to save conversation log: %s", sku, exc)


def _validate_description_start(description: str, sku: str = "") -> tuple[bool, str]:
    """Validate that description opens with sensory/atmospheric language, not technical keywords.
    
    Returns: (is_valid, reason)
    
    FORBIDDEN STARTS (Technical/Disclaimer):
    - "Premium Digital Download"
    - "Large 48 Inch"
    - "High Resolution"
    - "Digital File"
    - "This is not a physical"
    - "No physical item"
    - "Digital download"
    
    PREFERRED STARTS (Sensory/Atmospheric):
    - "Immerse" / "Bring"
    - "Under" / "Over" 
    - "The glow" / "The smell" / "The hush"
    - "Shimmering" / "Luminous" / "Ethereal"
    - "Rhythmic" / "Visual song"
    - Any vivid sensory verb or atmospheric descriptor
    """
    text = str(description or "").strip()
    if not text:
        return (True, "Description is empty")
    
    first_100 = text[:100].lower()
    
    # Check for forbidden technical starts
    forbidden_starts = [
        "premium digital download",
        "large 48 inch",
        "high resolution",
        "digital file",
        "this is not a physical",
        "no physical item",
        "digital download",
        "created as a premium",
        "this file is",
        "file type:",
    ]
    
    for forbidden in forbidden_starts:
        if first_100.startswith(forbidden):
            return (
                False,
                f"❌ Description opens with technical keyword '{forbidden}'. "
                f"Must lead with sensory/atmospheric language (e.g., 'Immerse', 'The glow', 'Bring', 'Shimmering', 'Rhythmic')."
            )
    
    # If we get here, description passes validation (doesn't start with forbidden keywords)
    return (True, "✓ Description opens with sensory/atmospheric language (Master Protocol style)")


def _prepend_functional_hook(description: str, payload: dict[str, Any]) -> str:
    """Prepend a strict 'Functional Hook' paragraph (160-250 chars) to the description.
    
    The hook must contain:
    - "Premium Digital Download | Large 48 Inch Wall Art | Australian Landscape"
    - "This is a high-resolution digital file; no physical item will be shipped."
    
    NOTE: The AI-generated description should already contain the NARRATIVE STORYTELLING MODULE
    (sensory hook + heritage connection + digital craft). This functional hook is prepended
    BEFORE the narrative for SEO optimization purposes, creating a two-layer opening:
    1. Functional Hook (SEO keywords, 160-250 chars)
    2. Narrative Storytelling (atmospheric, heritage-rich, 300+ chars)
    
    Maintains Robin's heartfelt, evocative tone while meeting Google Search Console optimization.
    """
    text = str(description or "").strip()
    if not text:
        return text
    
    # Check if functional hook already exists
    if "This is a high-resolution digital file; no physical item will be shipped" in text:
        return text
    
    # Extract subject/location for context
    visual_analysis = payload.get("visual_analysis") or {}
    subject = str(visual_analysis.get("subject") or "").strip()
    
    # Build functional hook (target 160-250 chars)
    hook = (
        "Premium Digital Download | Large 48 Inch Wall Art | Australian Landscape. "
        "This is a high-resolution digital file; no physical item will be shipped. "
    )
    
    # Add evocative context if subject is available and we have room
    if subject and len(hook) < 200:
        # Add brief subject reference to stay under 250 chars
        subject_snippet = subject[:60] if len(subject) > 60 else subject
        context = f"Experience {subject_snippet} in museum-quality detail."
        if len(hook) + len(context) <= 250:
            hook += context
    
    # Ensure we're within 160-250 character range
    hook = hook.strip()
    if len(hook) < 160:
        # Pad with evocative language to reach 160 minimum
        hook += " Transform your space with this breathtaking digital artwork."
    
    if len(hook) > 250:
        # Trim to 250 chars at last complete sentence
        hook = hook[:247] + "..."
    
    # Prepend hook to description with separator
    return f"{hook}\n\n{text}"


def _inject_gold_standard_blocks(description: str, aspect_ratio: Any) -> str:
    text = str(description or "").strip()
    if not text:
        return text
    if "📐 PRINTING & SIZE GUIDE" in text:
        return text

    ratio = _aspect_ratio_key(aspect_ratio) or "2:3"
    
    # Frame size data for cleaner table formatting
    sizes_data = {
        "2:3": {
            "inches": ["4×6", "6×9", "8×12", "12×18", "16×24", "20×30", "24×36", "32×48"],
            "cm": ["10×15", "20×30", "30×45", "40×60", "60×90"],
        },
        "3:4": {
            "inches": ["6×8", "9×12", "12×16", "18×24", "24×32", "30×40", "36×48"],
            "cm": ["15×20", "20×27", "30×40", "45×60", "60×80", "75×100", "90×120"],
        },
        "4:5": {
            "inches": ["4×5", "8×10", "11×14", "16×20", "24×30", "32×40", "38×48"],
            "cm": ["10×13", "20×25", "28×36", "40×50", "60×75", "80×100", "96×122"],
        },
    }
    
    sizes = sizes_data.get(ratio, sizes_data["2:3"])
    inches_str = " · ".join(sizes["inches"])
    cm_str = " · ".join(sizes["cm"])

    size_block = (
        f"---\n\n"
        f"### 📐 FRAME SIZES ({ratio} Aspect Ratio)\n\n"
        f"**Inches**  \n{inches_str}\n\n"
        f"**Centimeters**  \n{cm_str}"
    )

    how_to_print = (
        f"\n\n---\n\n"
        "### 🖨️ PRINTING RECOMMENDATION\n\n"
        "**Best Results With:**  \nHeavyweight matte paper · Fine art canvas · Archival ink\n\n"
        "**In Australia**  \n"
        "Officeworks · Local professional photo lab\n\n"
        "**International**  \n"
        "Printful · Gelato · Staples"
    )

    thank_you = (
        f"\n\n---\n\n"
        "### ❤️ SUPPORT INDEPENDENT ART\n\n"
        "Thank you for supporting South Australian artist **Robin Custance**.\n\n"
        "**Personal Use Only** — Resale and commercial distribution prohibited.  \n"
        "**© Robin Custance. All rights reserved.**"
    )

    return f"{text}\n\n{size_block}{how_to_print}{thank_you}".strip()


def _encode_image_base64(image_path: Path) -> str:
    try:
        data = image_path.read_bytes()
    except Exception as exc:  # pylint: disable=broad-except
        raise OpenAIAnalysisError(f"Failed to read analyse image: {image_path.name}") from exc
    return base64.b64encode(data).decode("utf-8")


def _cfg_get(key: str, default: Any) -> Any:
    try:
        return current_app.config.get(key, default)
    except Exception:
        return default


def _parse_model_stack(raw: Any) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, (list, tuple)):
        vals = [str(v).strip() for v in raw]
        return [v for v in vals if v]
    text = str(raw).strip()
    if not text:
        return []
    parts: list[str] = []
    for chunk in text.replace("\n", ",").split(","):
        val = str(chunk).strip()
        if val:
            parts.append(val)
    return parts


def _should_try_next_model(exc: Exception) -> bool:
    if RateLimitError is not None and isinstance(exc, RateLimitError):
        return True
    if APIConnectionError is not None and isinstance(exc, APIConnectionError):
        return True
    if APITimeoutError is not None and isinstance(exc, APITimeoutError):
        return True
    if isinstance(exc, NotFoundError):
        return True

    status = getattr(exc, "status_code", None)
    if status in {404, 429, 503}:
        return True
    code = getattr(exc, "code", None)
    if code in {404, 429, 503}:
        return True

    msg = str(exc or "").lower()
    if "status code" in msg and any(x in msg for x in ("404", "429", "503")):
        return True
    if "too many requests" in msg or "rate limit" in msg:
        return True
    if "service unavailable" in msg:
        return True
    if "not found" in msg and "model" in msg:
        return True

    return False


def _encode_image_base64_optimized(
    *,
    image_path: Path,
    sku: str,
    max_long_edge: int,
    max_mb: int,
) -> tuple[str, dict[str, Any], bytes]:
    log = logging.getLogger("ai_processing")
    max_bytes = int(max_mb) * 1024 * 1024

    try:
        with Image.open(image_path) as im:
            original_exif = im.getexif()
            original_dpi = im.info.get("dpi")
            original_xmp = im.info.get("xmp")
            icc_profile = im.info.get("icc_profile")

            exif_bytes = b""
            try:
                exif_bytes = original_exif.tobytes() if original_exif else b""
            except Exception:
                exif_bytes = b""

            src_w, src_h = im.size
            log.info("[%s] Thread started. Source dimensions: %sx%s", sku, src_w, src_h)
            log.info(
                "[%s] Metadata preserved: DPI=%s, EXIF=%s, XMP=%s",
                sku,
                original_dpi,
                bool(original_exif),
                bool(original_xmp),
            )
            log.debug(
                "[%s] Metadata extracted: EXIF=%s, DPI=%s, XMP=%s, ICC=%s",
                sku,
                bool(exif_bytes),
                original_dpi,
                bool(original_xmp),
                bool(icc_profile),
            )

            im = im.convert("RGB")
            if max(src_w, src_h) > int(max_long_edge):
                im.thumbnail((int(max_long_edge), int(max_long_edge)), Image.Resampling.LANCZOS)
            out_w, out_h = im.size

            buf = BytesIO()
            # Keep optimized ANALYSE JPEG quality at 80+.
            quality_steps = [95, 90, 85, 80]
            out_bytes = b""
            used_quality = 95

            base_save_kwargs: dict[str, Any] = {
                "format": "JPEG",
                "optimize": True,
            }
            if exif_bytes:
                base_save_kwargs["exif"] = exif_bytes
            if original_dpi:
                base_save_kwargs["dpi"] = original_dpi
            if original_xmp:
                base_save_kwargs["xmp"] = original_xmp
            if icc_profile:
                base_save_kwargs["icc_profile"] = icc_profile

            for q in quality_steps:
                buf.seek(0)
                buf.truncate(0)
                save_kwargs = dict(base_save_kwargs)
                save_kwargs["quality"] = int(q)
                try:
                    im.save(buf, **save_kwargs)
                except TypeError:
                    log.debug("[%s] JPEG save does not support XMP kwarg; retrying without XMP", sku)
                    save_kwargs.pop("xmp", None)
                    im.save(buf, **save_kwargs)
                out_bytes = buf.getvalue()
                used_quality = int(q)
                if len(out_bytes) <= max_bytes:
                    break

            if not out_bytes:
                raise OpenAIAnalysisError("Failed to encode optimized JPEG")
            if len(out_bytes) > max_bytes:
                raise OpenAIAnalysisError(
                    f"Optimized image still too large ({len(out_bytes)} bytes > {max_bytes} bytes)"
                )

            log.info(
                "[%s] Image optimized: %spx, %sKB, Quality=%s",
                sku,
                int(max_long_edge),
                int(len(out_bytes) / 1024),
                used_quality,
            )
            log.info(
                "[%s] OpenAI vision image optimized: src=%sx%s dst=%sx%s bytes=%s quality=%s max_mb=%s",
                sku,
                src_w,
                src_h,
                out_w,
                out_h,
                len(out_bytes),
                used_quality,
                int(max_mb),
            )

            meta = {
                "src_w": int(src_w),
                "src_h": int(src_h),
                "dst_w": int(out_w),
                "dst_h": int(out_h),
                "bytes": int(len(out_bytes)),
                "quality": int(used_quality),
                "exif": bool(exif_bytes),
                "dpi": original_dpi,
                "xmp": bool(original_xmp),
                "icc": bool(icc_profile),
            }
            return base64.b64encode(out_bytes).decode("utf-8"), meta, out_bytes
    except OpenAIAnalysisError:
        raise
    except Exception as exc:  # pylint: disable=broad-except
        raise OpenAIAnalysisError("Failed to optimize analyse image") from exc


def _seed_listing_payload(*, slug: str, sku: str, meta: dict[str, Any]) -> dict[str, Any]:
    now = _now_iso()
    master_name = str(meta.get("stored_filename") or storage_service.master_name(slug))
    thumb_name = str(meta.get("thumb_filename") or storage_service.thumb_name(slug))
    analyse_name = str(meta.get("analyse_filename") or storage_service.analyse_name(slug))
    return {
        "slug": slug,
        "sku": sku,
        "title": str(meta.get("display_title") or sku),
        "description": str(meta.get("description") or ""),
        "tags": meta.get("tags") or [],
        "materials": meta.get("materials") or [],
        "price": str(meta.get("price") or ""),
        "quantity": meta.get("quantity") or config.LISTING_DEFAULTS.get("QUANTITY", 0),
        "category": str(meta.get("category") or ""),
        "seo_filename": str(meta.get("seo_filename") or ""),
        "analysis_source": "openai",
        "images": {
            "hero": master_name,
            "small": thumb_name,
            "analyse": analyse_name,
        },
        "artist": meta.get("artist") or {},
        "created_at": str(meta.get("created_at") or now),
        "updated_at": now,
    }


def run_openai_analysis_for_slug(
    *,
    slug: str,
    processed_root: Path,
    model: str | None = None,
) -> dict[str, Any]:
    log = logging.getLogger("ai_processing")
    
    processed_dir = processed_root / slug
    if not processed_dir.exists() or not processed_dir.is_dir():
        raise OpenAIAnalysisError("Processed artwork directory not found.")

    # Load metadata with fallback logic (try SKU-prefixed, then legacy metadata.json)
    meta = storage_service.load_metadata_with_fallback(processed_dir)
    if not meta:
        raise OpenAIAnalysisError("Missing required JSON: metadata.json (with or without SKU prefix)")
    
    sku = str(meta.get("sku") or meta.get("artwork_id") or slug).strip() or slug
    original_filename = str(meta.get("original_filename") or "").strip()
    formatted_aspect = _format_aspect_ratio_label(meta.get("aspect_ratio"))
    
    # Initialize integrity report to track retry and fallback events
    integrity_report = {
        "retry_triggered": False,
        "model_fallback": False,
        "rejection_reason": None,
    }
    
    # Load artist-provided seed context if available
    seed_context = storage_service.load_seed_context(processed_dir)

    # Load assets manifest (source of truth for file references)
    assets_manifest = storage_service.load_assets_manifest(processed_dir)
    
    # Determine master and analyse filenames from assets manifest, with fallback to metadata
    if assets_manifest and assets_manifest.get("files"):
        master_name = str(assets_manifest["files"].get("master") or storage_service.master_name(slug))
        analyse_name = str(assets_manifest["files"].get("analyse") or storage_service.analyse_name(slug))
    else:
        master_name = str(meta.get("stored_filename") or storage_service.master_name(slug))
        analyse_name = str(meta.get("analyse_filename") or storage_service.analyse_name(slug))
    
    master_path = processed_dir / master_name
    analyse_path = processed_dir / analyse_name
    source_path = analyse_path if analyse_path.exists() else master_path
    if not source_path.exists():
        raise OpenAIAnalysisError("Neither master nor analyse image exists for artwork.")

    max_long_edge = int(_cfg_get("ANALYSE_LONG_EDGE", getattr(config, "ANALYSE_LONG_EDGE", 2400)) or 2400)
    max_mb = int(_cfg_get("OPENAI_IMAGE_MAX_MB", getattr(config, "OPENAI_IMAGE_MAX_MB", 20)) or 20)
    image_b64, image_meta, optimized_bytes = _encode_image_base64_optimized(
        image_path=source_path,
        sku=sku,
        max_long_edge=max_long_edge,
        max_mb=max_mb,
    )

    try:
        write_bytes_atomic(analyse_path, optimized_bytes)
    except Exception:
        logging.getLogger("ai_processing").exception("[%s] Failed to persist optimized ANALYSE image", sku)

    cfg_default_model = _cfg_get("OPENAI_DEFAULT_MODEL", getattr(config, "OPENAI_DEFAULT_MODEL", config.OPENAI_MODEL))
    cfg_stack_raw = _cfg_get("OPENAI_MODEL_STACK", getattr(config, "OPENAI_MODEL_STACK", ""))
    cfg_stack = _parse_model_stack(cfg_stack_raw)

    selected_model = (model or cfg_default_model or "gpt-4o").strip() or "gpt-4o"
    if model is None and cfg_stack:
        selected_model = cfg_stack[0]
    timeout_s = float(_cfg_get("OPENAI_API_TIMEOUT", getattr(config, "OPENAI_API_TIMEOUT", 60.0)) or 60.0)
    retries = int(_cfg_get("OPENAI_API_RETRIES", getattr(config, "OPENAI_API_RETRIES", 1)) or 1)
    max_tokens = int(_cfg_get(
        "ARTWORK_ANALYSIS_MAX_OUTPUT_TOKENS",
        getattr(config, "ARTWORK_ANALYSIS_MAX_OUTPUT_TOKENS", 2000),
    ) or 2000)
    # Master Protocol v2.5: Changed from 0.2 to 0.7 for storytelling with heart
    temperature = float(_cfg_get("TEMPERATURE", getattr(config, "TEMPERATURE", 0.7)) or 0.7)

    prompt_id = uuid4().hex

    prompt_text = (
        "Analyse the following artwork image and produce the structured listing fields.\n"
        "Return ONLY a JSON object that matches the required schema (no labelled sections, no plain text, no markdown).\n"
        f"SKU: {sku}\n"
        f"Aspect ratio: {formatted_aspect or 'UNSET'}\n"
        f"Original filename: {original_filename}"
    )

    def _call(model_name: str, temp: float):
        try:
            kwargs: dict[str, Any] = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": prompts.get_system_prompt(seed_info=seed_context)},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                        ],
                    },
                ],
                "response_format": OpenAIArtworkAnalysis,
                "max_completion_tokens": max_tokens,
                "timeout": timeout_s,
            }
            if _supports_temperature(model_name):
                kwargs["temperature"] = float(temp)

            # Save request payload as Markdown for debugging
            _save_request_log(
                messages=kwargs["messages"],
                model=model_name,
                temperature=kwargs.get("temperature", 0.0),
                seed_info=seed_context,
                processed_dir=processed_dir,
                sku=sku,
            )

            return openai_client.beta.chat.completions.parse(**kwargs)
        except TypeError as exc:
            _raise_openai_error(
                message=(
                    "OpenAI client library does not support max_completion_tokens. "
                    "Upgrade the openai Python package, or pin to a model that supports max_tokens."
                ),
                error_code="ERR_CLIENT",
                cause=exc,
            )

    log = logging.getLogger("ai_processing")

    models_to_try: list[str] = []
    for candidate in [selected_model, *cfg_stack, "gpt-4o"]:
        val = str(candidate or "").strip()
        if val and val not in models_to_try:
            models_to_try.append(val)

    used_model = models_to_try[0] if models_to_try else selected_model
    used_temperature = float(temperature)
    attempts = max(1, int(retries))

    def _call_with_retries(model_name: str, temp: float):
        last_exc: Exception | None = None
        for attempt in range(1, attempts + 1):
            try:
                log.info(
                    "OpenAI analysis call: slug=%s model=%s timeout_s=%s max_completion_tokens=%s temperature=%s attempt=%s/%s",
                    slug,
                    model_name,
                    timeout_s,
                    max_tokens,
                    temp,
                    attempt,
                    attempts,
                )
                return _call(model_name, float(temp))
            except Exception as exc:  # pylint: disable=broad-except
                last_exc = exc
                if attempt < attempts:
                    continue
                raise

        if last_exc is not None:
            raise last_exc
        raise RuntimeError("OpenAI retry loop reached invalid state")

    completion = None
    last_exc: Exception | None = None
    for idx, model_name in enumerate(models_to_try):
        used_model = model_name
        try:
            log.info("[%s] API Request: Model=%s, Prompt_ID=%s", sku, used_model, prompt_id)
            completion = _call_with_retries(used_model, used_temperature)
            break
        except Exception as exc:  # pylint: disable=broad-except
            last_exc = exc

            if _is_temperature_unsupported(exc) and used_temperature != 1.0:
                log.warning(
                    "[%s] OpenAI rejected temperature=%s for model '%s'; retrying once with temperature=1.0.",
                    sku,
                    used_temperature,
                    used_model,
                )
                try:
                    used_temperature = 1.0
                    completion = _call_with_retries(used_model, used_temperature)
                    break
                except Exception as exc2:  # pylint: disable=broad-except
                    last_exc = exc2
                    exc = exc2

            should_next = _should_try_next_model(exc) or (_should_fallback_to_gpt4o(exc) and used_model != "gpt-4o")
            has_next = idx < (len(models_to_try) - 1)
            if should_next and has_next:
                log.warning("OpenAI %s failed. Retrying with next in stack...", used_model)
                integrity_report["model_fallback"] = True
                continue

            code = _classify_openai_error(exc)
            _log_openai_exception(log=log, sku=sku, exc=exc, model=used_model, prompt_id=prompt_id)
            _raise_openai_error(message=f"OpenAI request failed: {str(exc)}", error_code=code, cause=exc)

    if completion is None:
        exc = last_exc or RuntimeError("OpenAI request failed")
        code = _classify_openai_error(exc) if isinstance(exc, Exception) else "ERR_UNKNOWN"
        if isinstance(exc, Exception):
            _log_openai_exception(log=log, sku=sku, exc=exc, model=used_model, prompt_id=prompt_id)
        _raise_openai_error(message=f"OpenAI request failed: {str(exc)}", error_code=code, cause=exc if isinstance(exc, Exception) else RuntimeError(str(exc)))

    parsed = None
    try:
        if not completion:
            raise OpenAIAnalysisError("Empty response from OpenAI")
        parsed = completion.choices[0].message.parsed
    except Exception as exc:  # pylint: disable=broad-except
        _raise_openai_error(
            message="OpenAI response missing parsed structured output.",
            error_code="ERR_PARSE",
            cause=exc,
        )

    if not isinstance(parsed, OpenAIArtworkAnalysis):
        try:
            parsed = OpenAIArtworkAnalysis.model_validate(parsed)
        except Exception as exc:  # pylint: disable=broad-except
            _raise_openai_error(
                message="OpenAI structured output failed validation.",
                error_code="ERR_PARSE",
                cause=exc,
            )

    if not parsed:
        raise OpenAIAnalysisError("Failed to parse OpenAI response")
    payload = parsed.model_dump()

    # Log the initial API conversation (success or first attempt)
    try:
        kwargs_for_log = {
            "role": "assistant",
            "content": payload if isinstance(payload, dict) else {"error": "Could not serialize response"},
        }
        messages_for_log: list[dict[str, Any]] = []
        if completion and completion.choices:
            msg = completion.choices[0].message
            messages_for_log = [{"role": msg.role, "content": msg.content}]
        _write_conversation_log(
            slug=slug,
            sku=sku,
            processed_dir=processed_dir,
            messages=messages_for_log,
            response=payload,
            rejection=None,
            append_mode=False,
        )
    except Exception as exc:  # pylint: disable=broad-except
        log.warning("[%s] Failed to log initial conversation: %s", sku, exc)

    # Master Protocol v2.5: Validate description length (850-character minimum for narrative substance)
    raw_description = str(payload.get("etsy_description") or payload.get("description") or "").strip()
    if len(raw_description) < 850:
        log.warning(
            "[%s] Description too short (%d chars). Re-prompting for expanded narrative...",
            sku,
            len(raw_description),
        )
        
        # Mark integrity report
        integrity_report["retry_triggered"] = True
        integrity_report["rejection_reason"] = f"Description under 850 chars ({len(raw_description)} provided)"
        
        # Build re-prompt with explicit expansion instruction
        expansion_prompt = (
            "Your narrative was too short. The Heartfelt Narrative section must be robust (850+ characters) "
            "with a dedicated 'Connection to Country' sub-section describing the artwork as a map of spirit "
            "or a rhythmic conversation with the land. Include the People of the Reeds heritage, sensory details "
            "of the landscape, and the labor of digital craft. Maintain the atmospheric, story-driven tone."
        )
        
        # Re-run analysis with expansion instruction
        try:
            reprompt_kwargs: dict[str, Any] = {
                "model": used_model,
                "messages": [
                    {"role": "system", "content": prompts.get_system_prompt(seed_info=seed_context)},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"{prompt_text}\n\n{expansion_prompt}"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                        ],
                    },
                ],
                "response_format": OpenAIArtworkAnalysis,
                "max_completion_tokens": max_tokens,
                "timeout": timeout_s,
            }
            if _supports_temperature(used_model):
                reprompt_kwargs["temperature"] = float(used_temperature)
            
            log.info("[%s] Re-prompting OpenAI for expanded description...", sku)
            recompletion = openai_client.beta.chat.completions.parse(**reprompt_kwargs)
            
            if recompletion and recompletion.choices:
                reparsed = recompletion.choices[0].message.parsed
                if isinstance(reparsed, OpenAIArtworkAnalysis):
                    payload = reparsed.model_dump()
                    expanded_description = str(payload.get("etsy_description") or payload.get("description") or "").strip()
                    log.info(
                        "[%s] Re-prompt successful. Description expanded to %d chars.",
                        sku,
                        len(expanded_description),
                    )
                    
                    # Log the re-prompt conversation (appended to first conversation)
                    try:
                        _write_conversation_log(
                            slug=slug,
                            sku=sku,
                            processed_dir=processed_dir,
                            messages=reprompt_kwargs["messages"],
                            response=payload,
                            rejection=integrity_report["rejection_reason"],
                            append_mode=True,
                        )
                    except Exception as exc:  # pylint: disable=broad-except
                        log.warning("[%s] Failed to log re-prompt conversation: %s", sku, exc)
        except Exception as exc:  # pylint: disable=broad-except
            log.warning("[%s] Re-prompt failed: %s. Using original response.", sku, exc)

    metadata_out = {
        "source": "openai",
        "model": used_model,
        "slug": slug,
        "sku": sku,
        "original_filename": original_filename,
        "image": image_meta,
        "analysis": payload,
        "created_at": _now_iso(),
        "prompt_id": prompt_id,
        "temperature": used_temperature,
        "integrity_report": integrity_report,
    }
    write_json_atomic(processed_dir / f"{sku.lower()}-metadata_openai.json", _json_safe(metadata_out))

    log.info("[SUCCESS] [%s] Analysis complete. Raw JSON saved to metadata_openai.json.", sku)

    listing_path = processed_dir / f"{sku.lower()}-listing.json"
    if listing_path.exists():
        listing = _load_json(listing_path)
        if not isinstance(listing.get("images"), dict):
            listing["images"] = {}
        listing.setdefault("slug", slug)
        listing.setdefault("sku", sku)
    else:
        listing = _seed_listing_payload(slug=slug, sku=sku, meta=meta)

    listing["analysis_source"] = "openai"
    listing["title"] = _sanitize_etsy_title(payload.get("etsy_title")) or listing.get("title")
    
    # Step 1: Use AI's description directly from Master Protocol (sole author)
    # The prepend hook is bypassed to honor the Master Protocol's narrative authority
    raw_description = payload.get("etsy_description") or payload.get("description") or listing.get("description") or ""
    # description_with_hook = _prepend_functional_hook(raw_description, payload)  # DISABLED: Master Protocol is sole author
    
    # VALIDATION: Check that description opens with sensory/atmospheric language (Master Protocol v2.5)
    is_valid_start, validation_msg = _validate_description_start(raw_description, sku)
    log.info("[%s] Description start validation: %s", sku, validation_msg)
    
    # Step 2: Inject gold standard blocks (size guide, printing info, etc.)
    listing["description"] = _inject_gold_standard_blocks(
        raw_description,
        (meta.get("analyse_qc") or {}).get("aspect_ratio") or meta.get("aspect_ratio"),
    )
    tags_raw = payload.get("etsy_tags") or payload.get("tags") or listing.get("tags") or []
    if isinstance(tags_raw, list):
        def _sanitize_tag(value: str) -> str:
            raw = "".join(ch for ch in str(value or "") if (ch.isalnum() or ch.isspace())).strip()
            cleaned = " ".join(raw.split()).strip()
            if len(cleaned) > 20:
                cleaned = cleaned[:20].rstrip()
            return cleaned

        tags = [_sanitize_tag(t) for t in tags_raw]
        tags = [t for t in tags if t]
        tags = tags[:13]
        filler = [
            "digital download",
            "printable art",
            "wall decor",
            "landscape art",
            "australian art",
        ]
        i = 0
        while len(tags) < 13:
            tags.append(_sanitize_tag(filler[i % len(filler)]))
            i += 1
        listing["tags"] = tags

    listing["materials"] = [
        "Digital Download",
        "High-Res JPG",
        "300 DPI",
        "14400px File",
        "Museum Quality Digital",
        "Instant Download",
        "Printable Art",
        "Large Scale Print",
        "RGB Colour Profile",
        "Wall Art File",
        "Digital Artwork",
        "Gallery Quality",
        "Professional File",
    ]

    seo_slug = str(payload.get("seo_filename_slug") or "").strip()
    if seo_slug:
        base = sanitize_etsy_filename(seo_slug, sku, max_length=66)
        listing["seo_filename"] = f"{base}.jpg"

    listing["primary_colour"] = payload.get("primary_colour")
    listing["secondary_colour"] = payload.get("secondary_colour")

    if isinstance(payload.get("visual_analysis"), dict):
        listing["visual_analysis"] = payload["visual_analysis"]
    listing["updated_at"] = _now_iso()
    
    # Add integrity report for frontend quality alerts
    listing["integrity_report"] = integrity_report

    write_json_atomic(listing_path, listing)
    
    # Rename ANALYSE file to SEO-friendly filename if available (optimal for mockups)
    seo_filename = listing.get("seo_filename")
    if seo_filename:
        try:
            analyse_name = storage_service.analyse_name(slug)
            analyse_path = processed_dir / analyse_name
            seo_path = processed_dir / seo_filename
            if analyse_path.exists() and not seo_path.exists():
                shutil.copy2(analyse_path, seo_path)
                log.info("[%s] Copied ANALYSE file to SEO filename: %s", sku, seo_filename)
                # Update assets.json to point to new SEO filename
                try:
                    assets_files = list(processed_dir.glob(f"{sku.lower()}-assets.json"))
                    if assets_files:
                        assets_path = assets_files[0]
                        assets_data = json.loads(assets_path.read_text(encoding="utf-8"))
                        if "files" in assets_data:
                            assets_data["files"]["analyse"] = seo_filename
                            write_json_atomic(assets_path, assets_data)
                except Exception:  # pylint: disable=broad-except
                    pass
        except Exception as exc:  # pylint: disable=broad-except
            log.warning("[%s] Failed to rename ANALYSE file to SEO filename: %s", sku, exc)
    
    # Sync comprehensive assets index (keep it in sync with all file changes)
    try:
        from application.mockups.assets_sync import sync_assets_index
        sync_assets_index(processed_dir, sku=sku)
    except Exception:  # pylint: disable=broad-except
        log.debug("[%s] Optional: assets index sync skipped", sku)
    
    return {"listing": listing, "metadata": metadata_out}
