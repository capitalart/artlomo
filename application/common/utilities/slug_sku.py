import os
import re
from pathlib import Path
from .files import ensure_dir


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower())
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    return cleaned or "artwork"


_SAFE_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", re.IGNORECASE)


def is_safe_slug(value: str) -> bool:
    candidate = (value or "").strip()
    if not candidate:
        return False
    if len(candidate) > 96:
        return False
    if "." in candidate:
        return False
    return bool(_SAFE_SLUG_RE.fullmatch(candidate))


def short_title_slug(text: str, max_words: int = 6, max_length: int = 48) -> str:
    base = slugify(text or "") if (text or "").strip() else "untitled"
    parts = [p for p in base.split("-") if p][:max_words]
    truncated = "-".join(parts).strip("-")
    if len(truncated) > max_length:
        truncated = truncated[:max_length].strip("-")
    return truncated or "untitled"


def _read_sequence(path: Path) -> int:
    if not path.exists():
        return 1
    try:
        return int(path.read_text().strip())
    except ValueError:
        return 1


def _write_sequence(path: Path, value: int) -> None:
    ensure_dir(path.parent)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(str(value), encoding="utf-8")
    os.replace(tmp_path, path)


def next_sku(sequence_path: Path, prefix: str = "RJC") -> str:
    current = _read_sequence(sequence_path)
    sku = f"{prefix}-{current:04d}"
    _write_sequence(sequence_path, current + 1)
    return sku


def slug_for_artist(artist_name: str, sku: str) -> str:
    clean = slugify(artist_name)
    if not clean:
        clean = "artist"
    return f"{clean}-{sku.lower()}"


def slug_for_artwork(artist_name: str, title: str, sku: str) -> str:
    artist = slugify(artist_name) or "artist"
    title_part = short_title_slug(title)
    return f"{artist}-{title_part}-{sku.lower()}"
