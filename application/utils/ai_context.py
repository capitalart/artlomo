"""utils/ai_context.py
Shared AI context builder for GDWS + generic reword flows.
"""
from __future__ import annotations

from typing import Dict, List
from pathlib import Path
import application.config as config

# Import parsing helpers from embed routes (avoid HTTP self-calls)
try:  # pragma: no cover - defensive import
    from routes.gdws_embed_routes import _generic_text_dir, _load_per_artwork_override, _to_blocks  # type: ignore
except Exception:  # Fallback minimal implementations
    def _generic_text_dir():  # type: ignore
        return getattr(config, 'GENERIC_TEXTS_DIR', Path(getattr(config, 'BASE_DIR')) / 'generic_texts')
    def _load_per_artwork_override(slug: str):  # type: ignore
        return ''
    def _to_blocks(text: str):  # type: ignore
        return []

ASPECT_PRINT_SIZES = {
    '4x5': [
        '4x5, 8x10, 11x14, 12x15, 16x20, 20x25, 24x30',
        'A4, A3, A2 (close fits)'
    ],
    '2x3': [
        '4x6, 8x12, 12x18, 16x24, 20x30, 24x36'
    ],
    '3x4': [
        '6x8, 9x12, 12x16, 15x20, 18x24'
    ],
    'square': [
        '8x8, 10x10, 12x12, 16x16, 20x20'
    ]
}


ROBIN_ACKNOWLEDGEMENT_OF_COUNTRY = (
    "I acknowledge the Traditional Custodians of the lands where I live and work, "
    "the Boandik people of the Mount Gambier and Naracoorte region, and pay my respects "
    "to Elders past, present, and emerging."
)


def _normalise_title_subject(title: str) -> str:
    t = (title or "").replace("|", " ").strip()
    t = " ".join(t.split())
    if not t:
        return "Australian Native Flora"
    # Keep the subject compact; use the first clause before a dash/colon if present.
    for sep in (" - ", " — ", ": "):
        if sep in t:
            t = t.split(sep, 1)[0].strip()
            break
    return t


def _load_generic_blocks(slug: str, aspect: str) -> List[Dict[str, str]]:
    # Per-artwork override first
    override_text = _load_per_artwork_override(slug) if slug else ''
    if override_text:
        return _to_blocks(override_text)
    # Aspect file, then fallback 4x5
    gdir = _generic_text_dir()
    p = gdir / f"{aspect}.txt"
    if not p.exists():
        p = gdir / '4x5.txt'
    try:
        txt = p.read_text(encoding='utf-8')
    except Exception:
        txt = ''
    return _to_blocks(txt)


def build_ai_context(*, slug: str, aspect: str, title: str, unique_text: str | None, include_generic: bool = True) -> dict:
    """Return dictionary of AI context fields.

    Keys:
      slug, aspect, title, unique_text, print_sizes, generic_blocks,
      artist_bio_snippet, licensing
    """
    aspect_norm = (aspect or '4x5').lower()
    print_sizes = ASPECT_PRINT_SIZES.get(aspect_norm, ASPECT_PRINT_SIZES['4x5'])
    generic_blocks = _load_generic_blocks(slug, aspect_norm) if include_generic else []
    # Artist bio: pick first block with 'about the artist' in title, else empty
    artist_bio_snippet = ''
    for b in generic_blocks:
        if 'artist' in (b.get('title') or '').lower():
            artist_bio_snippet = (b.get('content') or '')[:600]
            break

    subject = _normalise_title_subject(title)
    etsy_title_suggested = f"Aboriginal Dot Painting Wall Art, {subject} Australian Native Flora, Digital Download Art"
    return {
        'slug': slug,
        'aspect': aspect_norm,
        'title': title,
        'etsy_title_suggested': etsy_title_suggested,
        'unique_text': (unique_text or '').strip(),
        'print_sizes': print_sizes,
        'generic_blocks': generic_blocks,
        'artist_bio_snippet': artist_bio_snippet,
        'etsy_rules': {
            'no_pipes_in_title': True,
            'title_template': "Aboriginal Dot Painting Wall Art, [Subject] Australian Native Flora, Digital Download Art.",
            'first_30_words_hook_required': True,
            'acknowledgement_of_country': ROBIN_ACKNOWLEDGEMENT_OF_COUNTRY,
            'cultural_storytelling_guidance': (
                "Analyse the dot work, colour palette, and overall rhythm of the artwork. "
                "Write an original, respectful Dreamtime-connection narrative that feels poetic and grounded in nature, "
                "without claiming sacred/secret knowledge or attributing specific Dreaming stories to particular Nations unless explicitly provided."
            ),
        },
        'licensing': {
            'digital_download': True,
            'personal_use_only': True,
        }
    }

# End of file