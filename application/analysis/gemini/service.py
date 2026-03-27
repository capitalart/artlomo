from __future__ import annotations

import json
import logging
import re
import shutil
import time
from io import BytesIO
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

import application.config as config
from application.common.utilities.files import write_bytes_atomic, write_json_atomic, sanitize_etsy_filename
from application.upload.services import storage_service

from application.analysis import prompts
from application.utils.ai_utils import safe_parse_json

from .schema import GeminiArtworkAnalysis

from PIL import Image

try:
    from google.api_core.exceptions import (
        DeadlineExceeded,
        InvalidArgument,
        NotFound,
        PermissionDenied,
        ResourceExhausted,
        ServiceUnavailable,
        Unauthorized,
        Unauthenticated,
    )
except Exception:  # pylint: disable=broad-except
    DeadlineExceeded = None  # type: ignore
    InvalidArgument = None  # type: ignore
    NotFound = None  # type: ignore
    PermissionDenied = None  # type: ignore
    ResourceExhausted = None  # type: ignore
    ServiceUnavailable = None  # type: ignore
    Unauthorized = None  # type: ignore
    Unauthenticated = None  # type: ignore


class GeminiAnalysisError(RuntimeError):
    def __init__(self, message: str, error_code: str | None = None, error_detail: str | None = None):
        super().__init__(message)
        self.error_code = error_code or "ERR_UNKNOWN"
        self.error_detail = error_detail or message


# Singleton Gemini client - initialized once per worker process
_gemini_client = None
_gemini_client_key = None
_model_probe_cache: dict[str, Any] = {
    "model": "",
    "checked_at": 0.0,
    "stack_sig": "",
}
_MODEL_PROBE_TTL_S = 300.0
_model_cooldown_until: dict[str, float] = {}


def _get_gemini_client():
    """Get or create singleton Gemini client to avoid handshake overhead."""
    global _gemini_client, _gemini_client_key
    
    api_key = (config.GEMINI_API_KEY or "").strip()
    if not api_key:
        return None
    
    # Re-initialize if key changed (unlikely but safe)
    if _gemini_client is not None and _gemini_client_key == api_key:
        return _gemini_client
    
    try:
        from google import genai
        _gemini_client = genai.Client(api_key=api_key)
        _gemini_client_key = api_key
        logging.getLogger("ai_processing").info("[GEMINI] Client initialized (singleton)")
        return _gemini_client
    except Exception as exc:
        logging.getLogger("ai_processing").error("[GEMINI] Failed to initialize client: %s", exc)
        return None


def _classify_gemini_error(exc: Exception) -> str:
    msg = str(exc or "").strip().lower()

    if Unauthenticated is not None and isinstance(exc, Unauthenticated):
        return "ERR_AUTH"
    if Unauthorized is not None and isinstance(exc, Unauthorized):
        return "ERR_AUTH"
    if PermissionDenied is not None and isinstance(exc, PermissionDenied):
        return "ERR_AUTH"
    if DeadlineExceeded is not None and isinstance(exc, DeadlineExceeded):
        return "ERR_TIMEOUT"
    if ServiceUnavailable is not None and isinstance(exc, ServiceUnavailable):
        return "ERR_TIMEOUT"
    if ResourceExhausted is not None and isinstance(exc, ResourceExhausted):
        return "ERR_RATE_LIMIT"
    if NotFound is not None and isinstance(exc, NotFound):
        return "ERR_MODEL"
    if InvalidArgument is not None and isinstance(exc, InvalidArgument):
        if "model" in msg and "not" in msg and "found" in msg:
            return "ERR_MODEL"
        return "ERR_BAD_REQUEST"

    if "rate" in msg and "limit" in msg:
        return "ERR_RATE_LIMIT"
    if "quota" in msg or "billing" in msg or "balance" in msg or "insufficient" in msg:
        return "ERR_BALANCE"
    if "timeout" in msg or "timed out" in msg or "deadline" in msg:
        return "ERR_TIMEOUT"
    if "api key" in msg or "unauth" in msg or "permission" in msg or "auth" in msg:
        return "ERR_AUTH"
    if "model" in msg and "not" in msg and "found" in msg:
        return "ERR_MODEL"
    return "ERR_UNKNOWN"


def _raise_gemini_error(*, message: str, error_code: str, cause: Exception) -> None:
    err = GeminiAnalysisError(message)
    setattr(err, "error_code", error_code)
    raise err from cause


def _log_gemini_exception(*, log: logging.Logger, sku: str, exc: Exception, model: str, prompt_id: str) -> None:
    extra_parts: list[str] = []
    for key in ("status_code", "code", "status", "reason"):
        val = getattr(exc, key, None)
        if val is not None:
            extra_parts.append(f"{key}={val}")

    details = " ".join(extra_parts).strip()
    if details:
        log.error("[%s] Gemini API error: model=%s prompt_id=%s %s", sku, model, prompt_id, details)
    log.exception("[%s] Gemini API exception: model=%s prompt_id=%s message=%s", sku, model, prompt_id, str(exc))


def _should_retry_model_fallback(exc: Exception) -> bool:
    msg = str(exc or "").lower()
    if "404" in msg and "not found" in msg:
        return True
    if "model" in msg and "not" in msg and "found" in msg:
        return True
    if getattr(exc, "status_code", None) == 404:
        return True
    if getattr(exc, "code", None) == 404:
        return True
    return False


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


def _normalize_model_name(model_name: Any) -> str:
    """Normalize configured Gemini model aliases to API-supported identifiers.

    Some stacks use short aliases (e.g. gemini-3-flash) that are not available
    on v1beta. Normalize them to known compatible names while preserving
    explicitly versioned names.
    """
    val = str(model_name or "").strip()
    if not val:
        return ""
    lowered = val.lower()
    alias_map = {
        "gemini-3-flash": "gemini-3-flash-preview",
    }
    return alias_map.get(lowered, val)


def _cfg_bool(name: str, default: bool = False) -> bool:
    raw = getattr(config, name, default)
    if isinstance(raw, bool):
        return raw
    txt = str(raw or "").strip().lower()
    if txt in {"1", "true", "yes", "on"}:
        return True
    if txt in {"0", "false", "no", "off", ""}:
        return False
    return bool(default)


def _cfg_int(name: str, default: int) -> int:
    raw = getattr(config, name, default)
    try:
        return int(raw)
    except Exception:
        return int(default)


def _is_model_temporarily_disabled(model_name: str) -> bool:
    until = float(_model_cooldown_until.get(str(model_name).strip(), 0.0) or 0.0)
    return until > time.time()


def _mark_model_temporarily_disabled(model_name: str, seconds: int) -> None:
    if seconds <= 0:
        return
    _model_cooldown_until[str(model_name).strip()] = time.time() + float(seconds)


def _choose_best_working_model(*, client: Any, candidates: list[str], sku: str, log: logging.Logger) -> str:
    """Probe candidate Gemini models with a tiny text-only request.

    Returns the strongest currently-working model from the ordered candidate list.
    Uses a short-lived in-process cache to avoid probing on every job.
    """
    normalized = [str(c).strip() for c in candidates if str(c).strip()]
    if not normalized:
        return "gemini-2.5-flash"

    stack_sig = ",".join(normalized)
    now_ts = time.time()
    cached_model = str(_model_probe_cache.get("model") or "").strip()
    cached_at = float(_model_probe_cache.get("checked_at") or 0.0)
    cached_sig = str(_model_probe_cache.get("stack_sig") or "")

    if cached_model and cached_sig == stack_sig and (now_ts - cached_at) <= _MODEL_PROBE_TTL_S:
        return cached_model

    from google.genai import types

    probe_contents = [types.Part.from_text(text="Reply with OK.")]
    probe_config = types.GenerateContentConfig(max_output_tokens=8)

    for model_name in normalized:
        try:
            t0 = time.perf_counter()
            probe_resp = client.models.generate_content(  # type: ignore[arg-type]
                model=model_name,
                contents=probe_contents,
                config=probe_config,
            )
            _ = _extract_text(probe_resp)
            elapsed_ms = int((time.perf_counter() - t0) * 1000)
            log.info("[%s] Gemini model preflight selected=%s latency=%sms", sku, model_name, elapsed_ms)
            _model_probe_cache["model"] = model_name
            _model_probe_cache["checked_at"] = now_ts
            _model_probe_cache["stack_sig"] = stack_sig
            return model_name
        except Exception as exc:  # pylint: disable=broad-except
            code = _classify_gemini_error(exc)
            log.warning("[%s] Gemini model preflight failed model=%s code=%s", sku, model_name, code)

    # If all probes failed, keep caller order and let main error handling run.
    _model_probe_cache["model"] = ""
    _model_probe_cache["checked_at"] = now_ts
    _model_probe_cache["stack_sig"] = stack_sig
    return normalized[0]


def _should_try_next_model(exc: Exception) -> bool:
    if NotFound is not None and isinstance(exc, NotFound):
        return True
    if ResourceExhausted is not None and isinstance(exc, ResourceExhausted):
        return True
    if ServiceUnavailable is not None and isinstance(exc, ServiceUnavailable):
        return True
    if DeadlineExceeded is not None and isinstance(exc, DeadlineExceeded):
        return True

    msg = str(exc or "").lower()
    if "rate" in msg and "limit" in msg:
        return True
    if "quota" in msg:
        return True
    if "timeout" in msg or "deadline" in msg:
        return True
    if "service unavailable" in msg:
        return True
    if "model" in msg and "not" in msg and "found" in msg:
        return True
    return False


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


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
    cleaned = " ".join(title.split()).strip()
    # Truncate to 140 chars max
    if len(cleaned) > 140:
        cleaned = cleaned[:140].rstrip()
    return cleaned


def _sanitize_public_text(value: Any) -> str:
    text = str(value or "")
    if not text:
        return ""
    text = text.replace("\"", "").replace("'", "")
    text = text.replace("“", "").replace("”", "").replace("‘", "").replace("’", "")
    text = re.sub(r"\[cite_start\]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\[cite:[^\]]*\]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmonet\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bas an ai\b.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bi cant see\b.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bi cannot see\b.*", "", text, flags=re.IGNORECASE)
    text = "\n".join([" ".join(line.split()).strip() for line in text.splitlines()]).strip()
    return text


def _split_story_blocks(text: str) -> list[str]:
    normalized = str(text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return []
    if "\n---\n" in normalized:
        parts = [p.strip() for p in normalized.split("\n---\n")]
        return [p for p in parts if p]
    if "\n\n" in normalized:
        parts = [p.strip() for p in normalized.split("\n\n")]
        return [p for p in parts if p]
    return [normalized]


def _is_emoji_led_paragraph(text: str) -> bool:
    stripped = str(text or "").lstrip()
    if not stripped:
        return False
    first = stripped[0]
    if first.isalnum():
        return False
    if first in {"-", "*", "•"}:
        return False
    if first in {"!", "?", ".", ",", ":", ";", "(", ")", "[", "]", "{", "}", "/", "\\"}:
        return False
    return True


def _normalize_seo_slug(value: Any) -> str:
    raw = str(value or "").strip().lower()
    raw = re.sub(r"[^a-z0-9\-]+", "-", raw)
    raw = re.sub(r"-+", "-", raw).strip("-")
    if not raw:
        return "by-robin-custance"
    if "robin-custance" not in raw:
        raw = f"{raw}-robin-custance".strip("-")
    if not raw.endswith("robin-custance"):
        raw = re.sub(r"-?robin-custance.*$", "-robin-custance", raw).strip("-")
    if len(raw) > 61:
        raw = raw[:61].rstrip("-")
    return raw


def _normalize_colour(value: Any) -> str:
    allowed = {
        "Black",
        "Blue",
        "Brown",
        "Gold",
        "Green",
        "Grey",
        "Indigo",
        "Orange",
        "Pink",
        "Purple",
        "Red",
        "Silver",
        "Teal",
        "White",
        "Yellow",
    }
    raw = str(value or "").strip()
    if not raw:
        return "Blue"
    candidate = raw[:1].upper() + raw[1:].lower()
    if candidate in allowed:
        return candidate
    upper = raw.strip().upper()
    for item in allowed:
        if item.upper() == upper:
            return item
    return "Blue"


def _normalize_gemini_payload(raw_payload: dict[str, Any]) -> dict[str, Any]:
    payload: dict[str, Any] = dict(raw_payload or {})

    # Legacy field names (older prompts / models)
    if "etsy_description" not in payload and isinstance(payload.get("description"), str):
        payload["etsy_description"] = payload.get("description")
    if "etsy_tags" not in payload and isinstance(payload.get("tags"), list):
        payload["etsy_tags"] = payload.get("tags")

    def _as_str_list(value: Any) -> list[str]:
        if not isinstance(value, list):
            return []
        out: list[str] = []
        for item in value:
            s = str(item or "").strip()
            if s:
                out.append(s)
        return out

    tags = _as_str_list(payload.get("etsy_tags"))
    if tags:
        def _sanitize_tag(value: str) -> str:
            raw = "".join(ch for ch in str(value or "") if (ch.isalnum() or ch.isspace())).strip()
            cleaned = " ".join(raw.split()).strip()
            if len(cleaned) > 20:
                cleaned = cleaned[:20].rstrip()
            return cleaned

        tags = [_sanitize_tag(t) for t in tags]
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
        payload["etsy_tags"] = tags

    title = payload.get("etsy_title")
    if title is not None:
        payload["etsy_title"] = _sanitize_etsy_title(_sanitize_public_text(title))

    desc = payload.get("etsy_description")
    if desc is not None:
        payload["etsy_description"] = _sanitize_public_text(desc)

    materials = _as_str_list(payload.get("materials"))
    if materials:
        materials = materials[:13]
        while len(materials) < 13:
            materials.append("digital file")
        payload["materials"] = materials

    payload["materials"] = [
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

    primary = str(payload.get("primary_colour") or "").strip()
    secondary = str(payload.get("secondary_colour") or "").strip()
    if primary and not secondary:
        payload["secondary_colour"] = primary

    payload["primary_colour"] = _normalize_colour(payload.get("primary_colour"))
    payload["secondary_colour"] = _normalize_colour(payload.get("secondary_colour"))

    payload["seo_filename_slug"] = _normalize_seo_slug(payload.get("seo_filename_slug"))

    return payload


def _aspect_ratio_key(value: Any) -> str | None:
    label = _format_aspect_ratio_label(value)
    if not label:
        return None
    ratio = label.split()[0].strip()
    if ratio in {"2:3", "3:4", "4:5"}:
        return ratio
    return None


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
        "analysis_source": "gemini",
        "images": {
            "hero": master_name,
            "small": thumb_name,
            "analyse": analyse_name,
        },
        "artist": meta.get("artist") or {},
        "created_at": str(meta.get("created_at") or now),
        "updated_at": now,
    }


def _build_safety_settings():
    try:
        from google.genai import types

        return [
            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_NONE),
            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
        ]
    except Exception:
        return None


def _extract_text(response: Any) -> str:
    text = getattr(response, "text", None)
    if isinstance(text, str) and text.strip():
        return text.strip()

    candidates = getattr(response, "candidates", None)
    if isinstance(candidates, list) and candidates:
        content = getattr(candidates[0], "content", None)
        parts = getattr(content, "parts", None)
        if isinstance(parts, list) and parts:
            for part in parts:
                t = getattr(part, "text", None)
                if isinstance(t, str) and t.strip():
                    return t.strip()

    raise GeminiAnalysisError("Gemini response contained no text")


def _read_image_bytes_optimized(
    *,
    image_path: Path,
    sku: str,
    max_long_edge: int,
    max_mb: int,
) -> tuple[bytes, dict[str, Any]]:
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
                raise GeminiAnalysisError("Failed to encode optimized JPEG")
            if len(out_bytes) > max_bytes:
                raise GeminiAnalysisError(
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
                "Gemini vision image optimized: src=%sx%s dst=%sx%s bytes=%s quality=%s max_mb=%s",
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
            return out_bytes, meta
    except GeminiAnalysisError:
        raise
    except Exception as exc:  # pylint: disable=broad-except
        raise GeminiAnalysisError("Failed to optimize analyse image", error_code="ERR_BAD_REQUEST", error_detail=str(exc)) from exc


def run_gemini_analysis_for_slug(
    *,
    slug: str,
    processed_root: Path,
    model: str | None = None,
) -> dict[str, Any]:
    log = logging.getLogger("ai_processing")
    
    if not (config.GEMINI_API_KEY or "").strip():
        raise GeminiAnalysisError("Gemini API key is not configured.", error_code="ERR_AUTH")

    processed_dir = processed_root / slug
    if not processed_dir.exists() or not processed_dir.is_dir():
        raise GeminiAnalysisError("Processed artwork directory not found.", error_code="ERR_BAD_REQUEST")

    # Load metadata with fallback logic (try SKU-prefixed, then legacy metadata.json)
    meta = storage_service.load_metadata_with_fallback(processed_dir)
    if not meta:
        raise GeminiAnalysisError("Missing required JSON: metadata.json (with or without SKU prefix)", error_code="ERR_BAD_REQUEST")
    
    sku = str(meta.get("sku") or meta.get("artwork_id") or slug).strip() or slug
    original_filename = str(meta.get("original_filename") or "").strip()
    formatted_aspect = _format_aspect_ratio_label(meta.get("aspect_ratio"))
    
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
        raise GeminiAnalysisError("Neither master nor analyse image exists for artwork.", error_code="ERR_BAD_REQUEST")

    max_long_edge = int(getattr(config, "ANALYSE_LONG_EDGE", 2400) or 2400)
    max_mb = int(getattr(config, "OPENAI_IMAGE_MAX_MB", 20) or 20)
    image_bytes, image_meta = _read_image_bytes_optimized(
        image_path=source_path,
        sku=sku,
        max_long_edge=max_long_edge,
        max_mb=max_mb,
    )

    try:
        write_bytes_atomic(analyse_path, image_bytes)
    except Exception:
        logging.getLogger("ai_processing").exception("Failed to persist optimized analyse image (slug=%s)", slug)

    cfg_stack = [_normalize_model_name(v) for v in _parse_model_stack(getattr(config, "GEMINI_MODEL_STACK", ""))]
    selected_model = _normalize_model_name(
        model or config.GEMINI_MODEL or (cfg_stack[0] if cfg_stack else "gemini-2.5-flash")
    ) or "gemini-2.5-flash"
    if model is None and cfg_stack:
        selected_model = cfg_stack[0]

    prompt_id = uuid4().hex

    try:
        from google.genai import types

        client = _get_gemini_client()
        if client is None:
            raise GeminiAnalysisError("Gemini client not available - check API key configuration", error_code="ERR_AUTH")

        prompt_text = (
            "Analyse the following artwork image and produce the structured listing fields.\n"
            "Return ONLY a JSON object that matches the required schema (no labelled sections, no plain text, no markdown).\n"
            "Also include 'mockup_category' as a single short category suggestion suitable for a decor mockup setting (e.g., 'Natural Timber') derived from the visual mood/subject.\n"
            f"SKU: {sku}\n"
            f"Aspect ratio: {formatted_aspect or 'UNSET'}\n"
            f"Original filename: {original_filename}"
        )

        contents = [
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            types.Part.from_text(text=prompt_text),
        ]

        request_config = types.GenerateContentConfig(
            systemInstruction=prompts.get_gemini_system_prompt(seed_info=seed_context),  # type: ignore[call-arg]
            responseMimeType="application/json",  # type: ignore[call-arg]
            safetySettings=_build_safety_settings(),  # type: ignore[call-arg]
        )

        primary_model = _normalize_model_name((cfg_stack[0] if cfg_stack else selected_model).strip() or selected_model)
        fallback_model = _normalize_model_name(cfg_stack[1] if len(cfg_stack) > 1 else "gemini-2.5-pro")
        models_to_try: list[str] = []
        for candidate in [primary_model, fallback_model]:
            val = str(candidate or "").strip()
            if val and val not in models_to_try:
                models_to_try.append(val)

        log = logging.getLogger("ai_processing")
        probe_enabled = _cfg_bool("GEMINI_MODEL_PROBE_ENABLED", False)
        if probe_enabled and len(models_to_try) > 1:
            best_model = _choose_best_working_model(client=client, candidates=models_to_try, sku=sku, log=log)
            if best_model in models_to_try:
                models_to_try = [best_model] + [m for m in models_to_try if m != best_model]

        cooldown_s = max(0, _cfg_int("GEMINI_MODEL_COOLDOWN_S", 900))
        active_models = [m for m in models_to_try if not _is_model_temporarily_disabled(m)]
        if active_models:
            if len(active_models) != len(models_to_try):
                skipped = [m for m in models_to_try if m not in active_models]
                log.warning("[%s] Skipping model(s) in cooldown: %s", sku, ",".join(skipped))
            models_to_try = active_models

        selected_model = models_to_try[0]
        log.info("[%s] API Request: Model=%s, Prompt_ID=%s", sku, selected_model, prompt_id)

        last_exc: Exception | None = None
        resp = None
        used_model = selected_model
        for m in models_to_try:
            try:
                used_model = m
                try:
                    resp = client.models.generate_content(model=m, contents=contents, config=request_config)  # type: ignore[arg-type]
                except Exception as exc:  # pylint: disable=broad-except
                    error_type = type(exc).__name__
                    details = str(exc)
                    log = logging.getLogger("ai_processing")
                    log.error("--- GEMINI DIAGNOSTIC START ---")
                    log.error("Error Type: %s", error_type)
                    log.error("Error Details: %s", details)
                    upper = details.upper()
                    if "API_KEY" in upper or "API KEY" in upper or "UNAUTH" in upper or "PERMISSION" in upper:
                        log.error("DIAGNOSIS: GEMINI_API_KEY is missing/incorrect or lacks permission.")
                    elif "429" in upper or re.search(r"\bRATE\b", upper) or "RESOURCE_EXHAUSTED" in upper:
                        log.error("DIAGNOSIS: Rate limit exceeded or quota exhausted.")
                    elif "404" in upper or "NOT_FOUND" in upper:
                        log.error("DIAGNOSIS: Model identifier not available on this API version; check configured model stack.")
                    elif "INVALID_ARGUMENT" in upper or "400" in upper:
                        log.error("DIAGNOSIS: Request payload/config invalid (schema/fields/model).")
                    elif "TIMED OUT" in upper or "TIMEOUT" in upper or "DEADLINE" in upper:
                        log.error("DIAGNOSIS: Network timeout contacting Gemini.")
                    elif "CONNECTION" in upper or "DNS" in upper or "NETWORK" in upper:
                        log.error("DIAGNOSIS: Network/DNS/connectivity issue contacting Gemini.")
                    log.error("--- GEMINI DIAGNOSTIC END ---")

                    is_busy = (
                        "503" in upper
                        or "UNAVAILABLE" in upper
                        or "OVERLOADED" in upper
                        or "429" in upper
                        or "RESOURCE_EXHAUSTED" in upper
                    )
                    if is_busy and m == primary_model and fallback_model in models_to_try:
                        log.warning("[GEMINI FALLBACK] Model %s busy/overloaded, trying fallback: %s", m, fallback_model)
                        last_exc = exc
                        continue

                    raise ValueError(f"Gemini {error_type}: {details}") from exc
                break
            except Exception as exc:  # pylint: disable=broad-except
                last_exc = exc
                err_code = _classify_gemini_error(exc)
                if err_code == "ERR_MODEL":
                    _mark_model_temporarily_disabled(m, cooldown_s)
                    logging.getLogger("ai_processing").warning(
                        "[%s] Model %s disabled for %ss due to ERR_MODEL", sku, m, cooldown_s
                    )
                should_next = _should_retry_model_fallback(exc) or _should_try_next_model(exc)
                if m == primary_model and not should_next:
                    raise
                if m != models_to_try[-1] and should_next:
                    logging.getLogger("ai_processing").warning("Gemini %s failed. Retrying with next in stack...", m)
                    continue
                raise

        if resp is None:
            error_msg = str(last_exc) if last_exc else "Unknown error"
            logging.getLogger("ai_processing").error(
                "Gemini request failed for all models. primary=%s fallback=%s error=%s",
                primary_model,
                fallback_model,
                error_msg,
            )
            # Raise with detailed error message for UI display
            err = GeminiAnalysisError(f"All Gemini models failed. Last error: {error_msg}")
            setattr(err, "error_code", _classify_gemini_error(last_exc) if last_exc else "ERR_UNKNOWN")
            setattr(err, "error_detail", error_msg)
            raise err

        raw_text = _extract_text(resp)
    except GeminiAnalysisError:
        raise
    except Exception as exc:  # pylint: disable=broad-except
        log = logging.getLogger("ai_processing")
        code = _classify_gemini_error(exc)
        error_detail = str(exc)
        log.error("[GEMINI ERROR] sku=%s model=%s code=%s detail=%s", sku, selected_model, code, error_detail)
        _log_gemini_exception(log=log, sku=sku, exc=exc, model=selected_model, prompt_id=prompt_id)
        err = GeminiAnalysisError(f"Gemini request failed: {error_detail}")
        setattr(err, "error_code", code)
        setattr(err, "error_detail", error_detail)
        raise err from exc

    raw_payload = safe_parse_json(raw_text)
    if raw_payload is None:
        _raise_gemini_error(
            message="Gemini response was not valid JSON.",
            error_code="ERR_PARSE",
            cause=ValueError("Failed to parse Gemini response as JSON"),
        )

    if isinstance(raw_payload, dict):
        raw_payload = _normalize_gemini_payload(raw_payload)

    try:
        parsed = GeminiArtworkAnalysis.model_validate(raw_payload)
    except Exception as exc:  # pylint: disable=broad-except
        _raise_gemini_error(
            message="Gemini structured output failed validation.",
            error_code="ERR_PARSE",
            cause=exc,
        )

    payload = parsed.model_dump()

    payload["etsy_title"] = _sanitize_etsy_title(_sanitize_public_text(payload.get("etsy_title")))
    payload["seo_filename_slug"] = _normalize_seo_slug(payload.get("seo_filename_slug"))

    payload["primary_colour"] = _normalize_colour(payload.get("primary_colour"))
    payload["secondary_colour"] = _normalize_colour(payload.get("secondary_colour"))

    description = _sanitize_public_text(payload.get("etsy_description"))
    blocks = _split_story_blocks(description)
    
    # Relax validation: Use helper to pad to 13 blocks and check emojis without crashing
    from application.utils.ai_utils import validate_pioneer_blocks
    blocks = validate_pioneer_blocks(blocks)

    for i, block in enumerate(blocks, start=1):
        if not block: # Skip validation for padded empty blocks
            continue
        
        # Log warnings instead of raising for Pioneer style violations
        if len(block) < 250:
            logging.getLogger("ai_processing").warning("[%s] Gemini Pioneer description block %d is short (%d chars).", sku, i, len(block))
            
    if len(blocks) >= 7:
        tech_block = blocks[6]
        tech_upper = tech_block.upper()
        if "14400" not in tech_upper or "300" not in tech_upper or "DPI" not in tech_upper:
            logging.getLogger("ai_processing").warning("[%s] Gemini Pioneer description block 7 missing hero metrics (14400px/300 DPI).", sku)
    payload["etsy_description"] = "\n---\n".join(blocks)

    metadata_out = {
        "source": "gemini",
        "model": used_model,
        "slug": slug,
        "sku": sku,
        "original_filename": original_filename,
        "image": image_meta,
        "analysis": payload,
        "created_at": _now_iso(),
        "prompt_id": prompt_id,
    }
    write_json_atomic(processed_dir / f"{sku.lower()}-metadata_gemini.json", metadata_out)
    logging.getLogger("ai_processing").info("[SUCCESS] [%s] Analysis complete. Raw JSON saved to metadata_gemini.json.", sku)

    listing_path = processed_dir / f"{sku.lower()}-listing.json"
    if listing_path.exists():
        listing = _load_json(listing_path)
        if not isinstance(listing.get("images"), dict):
            listing["images"] = {}
        listing.setdefault("slug", slug)
        listing.setdefault("sku", sku)
    else:
        listing = _seed_listing_payload(slug=slug, sku=sku, meta=meta)

    listing["analysis_source"] = "gemini"
    listing["title"] = _sanitize_etsy_title(payload.get("etsy_title")) or listing.get("title")
    listing["description"] = payload.get("etsy_description") or listing.get("description")
    listing["tags"] = payload.get("etsy_tags") or listing.get("tags") or []
    listing["materials"] = payload.get("materials") or listing.get("materials") or []

    seo_slug = str(payload.get("seo_filename_slug") or "").strip()
    if seo_slug:
        base = sanitize_etsy_filename(seo_slug, sku, max_length=66)
        listing["seo_filename"] = f"{base}.jpg"

    listing["primary_colour"] = payload.get("primary_colour")
    listing["secondary_colour"] = payload.get("secondary_colour")
    if isinstance(payload.get("visual_analysis"), dict):
        listing["visual_analysis"] = payload["visual_analysis"]

    mockup_category = payload.get("mockup_category")
    if isinstance(mockup_category, str) and mockup_category.strip():
        listing["mockup_category"] = mockup_category.strip()
    listing["updated_at"] = _now_iso()

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
