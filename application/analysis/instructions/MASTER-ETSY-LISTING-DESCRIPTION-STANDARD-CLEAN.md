# Master Etsy Listing Description Standard

Version: 2.0 Clean
Scope: Deterministic generation of Etsy digital artwork listing descriptions for ArtLomo / Dream Art Machine.

## Objective
Generate Etsy listing text that is Etsy-compliant, Google-aware, buyer-friendly, mobile-readable, brand-consistent with Robin Custance / BOAND Art, and safe for automated use.

## Output Contract
The generator must return exactly these fields:

```text
STATUS:
TITLE:
DESCRIPTION:
SEO_KEYWORDS:
ARTWORK_DETAILS:
```

If generation fails, return:

```text
STATUS: FAILED
REASON: <clear explanation>
```

Legacy failure marker accepted for backwards compatibility:

```text
ANALYSIS_FAILED
REASON: <clear explanation>
```

## Hard Rules
- Plain text only.
- Do not output HTML.
- Do not rely on Etsy preserving markdown.
- Never imply a physical item will be shipped.
- Always state that this is a digital download.
- Always state that no physical item is shipped.
- Do not claim the artwork is traditional hand-painted art if it is AI-assisted digital art.
- Do not invent cultural stories, Dreaming stories, permissions, sacred meanings, locations, animals, or provenance.
- Do not use misleading scarcity or investment language.
- Do not make medical, spiritual, financial, or legal claims.
- Do not use another artist’s name in a way that implies authorship or official association.

## Recommended Description Template

```text
Bring [subject/location/mood] into your home with this high-resolution digital artwork by Robin Custance.

This piece features [accurate visual description]. The composition is designed to feel [mood], with [colour/light/detail notes] that make it suitable for [rooms/interior styles].

WHAT YOU RECEIVE
- High-resolution digital artwork file
- Suitable for large-format printing
- Instant download through Etsy after purchase
- No physical item is shipped

PRINTING
For best results, print through a professional print lab or quality giclée service. Choose archival matte paper, fine art paper, or photographic paper depending on the finish you prefer.

WHERE IT WORKS
Ideal for living rooms, bedrooms, hallways, offices, studios, guest rooms, and thoughtful gifting.

ARTIST NOTE
Created by Robin Custance, a South Australian digital artist inspired by Australian landscapes, light, memory, and place.

PLEASE NOTE
Colours may vary slightly depending on your screen, printer, paper, and framing choices. This purchase is for personal use unless a commercial licence is clearly stated.
```

## Title Rules
A strong Etsy title should lead with what the buyer is searching for, include the subject or location, include style or emotional cue, include “digital download” or “printable wall art”, include size value where accurate, and include Robin Custance where space allows.

Good title format:

```text
[Subject/Location] Wall Art - [Style/Mood] Australian Digital Download - Large 48 Inch Printable Art - Robin Custance
```

## SEO Keyword Rules
Use natural buyer phrases. Prioritise subject, location, style, room/use, format, Australian relevance, and artist name.

Example:

```text
Australian landscape art, digital download wall art, printable artwork, South Australian art, large wall print, nature wall decor, Robin Custance art
```

## Artwork Details Rules
Include only facts known from metadata or analysis:
- Artist
- Artwork title
- File format
- Pixel dimensions
- Print size guidance
- Delivery method
- Physical shipping status
- Personal-use licence note

## Failure Handling
The pipeline must fail safely when image analysis is missing, metadata is missing required identifiers, output cannot be parsed into required fields, digital-download or no-physical-shipping disclosure is omitted, or unsupported claims appear.

On failure, ArtLomo should:
- Mark `analysis_status = failed`.
- Preserve source files.
- Return artwork lifecycle to a safe retryable state.
- Log the reason.
- Allow retry without duplicating assets or corrupting the index.

## Definition of Done
A generated listing is acceptable only when all required fields are present, digital-download and no-physical-shipping disclosures are explicit, the description is readable on mobile, the facts match the artwork metadata, and no unsupported cultural, legal, medical, investment, or physical-product claims are present.
