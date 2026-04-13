from pathlib import Path
from typing import Dict


def load_aspect_facts(aspect_key: str, base_dir: Path) -> Dict[str, str]:
    """
    Parse trimmed generic_texts/<aspect>.txt to extract structured facts for Description V4.
    Expected keys in that file (human-readable lines):
      - ASPECT_LABEL: e.g., "3:4 (Vertical)"
      - MASTER_PIXELS: e.g., "10,800 × 14,400 px"
      - MAX_PRINT: e.g., "36 × 48 in (≈ 91.4 × 121.9 cm)"
      - POPULAR_SIZES: single line sizes separated by " · "
      - POPULAR_SIZES_CM: single line sizes (cm) separated by " · "
      - PRINTING_TIP: one sentence
      - ARTIST_BIO_SHORT: one short paragraph
      - INTERNAL_LINK: Etsy URL
    Returns a dict with those keys; raises ValueError if any are missing.
    """
    fpath = base_dir / "generic_texts" / f"{aspect_key}.txt"
    text = Path(fpath).read_text(encoding="utf-8")

    # Simple line-based extraction
    facts: Dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip().upper()
        v = v.strip()
        if k in {
            "ASPECT_LABEL",
            "MASTER_PIXELS",
            "MAX_PRINT",
            "POPULAR_SIZES",
            "POPULAR_SIZES_CM",
            "PRINTING_TIP",
            "ARTIST_BIO_SHORT",
            "INTERNAL_LINK",
        }:
            facts[k] = v

    required = [
        "ASPECT_LABEL",
        "MASTER_PIXELS",
        "MAX_PRINT",
        "POPULAR_SIZES",
        "POPULAR_SIZES_CM",
        "PRINTING_TIP",
        "ARTIST_BIO_SHORT",
        "INTERNAL_LINK",
    ]
    missing = [k for k in required if k not in facts]
    if missing:
        raise ValueError(f"Missing aspect facts in {fpath}: {missing}")

    # Quick Etsy link sanity
    if not facts["INTERNAL_LINK"].startswith("https://www.etsy.com"):
        raise ValueError("INTERNAL_LINK must be an Etsy URL")

    return facts
