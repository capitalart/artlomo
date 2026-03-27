"""Mockup Base Generation - Prompt Construction Service.

Generates highly dynamic, category-aware text prompts for Gemini image generation.
Each prompt describes a photorealistic interior scene featuring a matte cyan placeholder
rectangle on the wall, with category-specific furniture, lighting, and atmospheric details.

Design Principles:
- Category-aware detail injection (café gets espresso machines, nursery gets cribs)
- Dynamic variation (20 unique prompts per category, never repeat)
- Aspect ratio NOT included in prompt text (handled via API config instead)
- Cyan placeholder always described as: "solid, perfectly flat, untextured matte cyan rectangle"
- Three-quarter perspective room view
- Professional commercial staging
"""

from __future__ import annotations

import random
from typing import Dict, List


class MockupPromptService:
    """Service for generating dynamic, category-aware mockup scene prompts."""

    # Category-specific domain knowledge: props, lighting styles, and atmospheric cues
    CATEGORY_DETAILS: Dict[str, Dict[str, List[str]]] = {
        "bathroom": {
            "props": [
                "marble sink",
                "chrome faucet",
                "white subway tile",
                "porcelain fixtures",
                "fluffy white towel rack",
                "potted fern",
                "mirror with LED frame",
                "marble countertop",
            ],
            "lighting": [
                "soft morning light from frosted window",
                "warm LED vanity lights above mirror",
                "diffused overhead lighting",
                "cool gallery-style spotlights",
            ],
            "textures": [
                "sleek polished ceramic",
                "soft terrycloth",
                "brushed stainless steel",
                "natural stone",
            ],
        },
        "bedroom-adults": {
            "props": [
                "upholstered bed frame",
                "bedside lamp",
                "minimalist nightstand",
                "reading chair",
                "soft area rug",
                "linen curtains",
                "wooden dresser",
                "modern pendant light",
            ],
            "lighting": [
                "warm golden hour light through gauzy curtains",
                "soft accent lighting from bedside lamp",
                "cool blue twilight mood",
                "soft ambient overhead light",
            ],
            "textures": [
                "soft linen and cotton",
                "warm wood grain",
                "plush fabric",
                "natural fibre",
            ],
        },
        "bedroom-kids": {
            "props": [
                "colorful toy storage",
                "soft stuffed animals",
                "whimsical window seat",
                "wooden building blocks",
                "night light",
                "playful bedding",
                "wall shelving",
                "cheerful pendant",
            ],
            "lighting": [
                "warm whimsical afternoon light",
                "gentle soft lighting suitable for sleep",
                "playful rainbow light through prism",
                "warm small accent lights",
            ],
            "textures": [
                "soft wool and cotton",
                "smooth painted wood",
                "plush fabrics",
                "natural and dyed textiles",
            ],
        },
        "cafe": {
            "props": [
                "espresso machine gleaming chrome",
                "wooden barista counter",
                "pendant lights over bar",
                "vintage industrial stools",
                "coffee cup and saucer",
                "fresh pastries display",
                "chalkboard menu",
                "warm wood shelving",
            ],
            "lighting": [
                "warm morning café light from large window",
                "soft golden tungsten overhead lights",
                "industrial pendant lighting",
                "natural light accented by warm bulbs",
            ],
            "textures": [
                "steamed milk foam",
                "polished chrome",
                "wood grain and veneer",
                "ceramic and porcelain",
            ],
        },
        "closeup": {
            "props": [
                "magnifying glass",
                "artist's desk lamp",
                "fine detail brush set",
                "protective glass panel",
                "studio spotlight",
                "minimal background",
                "neutral backdrop",
            ],
            "lighting": [
                "studio-grade focused spotlight",
                "precise directional light emphasizing detail",
                "soft raking light revealing texture",
                "gallery-quality accent lighting",
            ],
            "textures": [
                "micro-texture surface",
                "fine brushwork",
                "precise detail clarity",
            ],
        },
        "dining": {
            "props": [
                "elegant dining table",
                "upholstered chair set",
                "crystal chandelier",
                "fine china place setting",
                "white tablecloth",
                "fresh flowers centerpiece",
                "wine glasses",
                "silverware",
            ],
            "lighting": [
                "warm candlelit ambiance",
                "soft overhead chandelier glow",
                "dimmable accent lighting",
                "warm golden evening light through windows",
            ],
            "textures": [
                "fine linen and damask",
                "polished wood",
                "crystal and glass",
                "ceramic and porcelain",
            ],
        },
        "display": {
            "props": [
                "museum-quality pedestal",
                "track lighting system",
                "gallery white walls",
                "minimalist display shelving",
                "glass shadow box",
                "polished concrete floor",
                "accent lighting",
                "professional information placard",
            ],
            "lighting": [
                "gallery-grade directional spotlights",
                "warm museum track lighting",
                "precise accent light from above",
                "professional exhibition lighting",
            ],
            "textures": [
                "polished concrete",
                "white gallery wall",
                "gallery track",
                "museum-quality materials",
            ],
        },
        "gallery": {
            "props": [
                "white gallery walls",
                "polished hardwood floors",
                "track lighting rig",
                "minimalist sculpture",
                "modern bench seating",
                "clean sightlines",
                "neutral tones",
                "professional ambiance",
            ],
            "lighting": [
                "professional gallery track lighting",
                "warm museum-quality spotlights",
                "soft ambient gallery light",
                "directional accent lighting from above",
            ],
            "textures": [
                "white matte wall finish",
                "polished hardwood",
                "clean gallery aesthetic",
                "professional materials",
            ],
        },
        "games": {
            "props": [
                "game console",
                "gaming chair ergonomic design",
                "RGB LED gaming lights",
                "monitor stand",
                "gaming keyboard and mouse",
                "cable management",
                "LED strip lighting",
                "gaming headset stand",
            ],
            "lighting": [
                "RGB gaming ambient lighting",
                "cool blue accent lights",
                "monitor glow",
                "futuristic accent lighting",
            ],
            "textures": [
                "smooth gaming peripherals",
                "sleek plastic and metal",
                "LED and glass",
                "gaming-grade materials",
            ],
        },
        "gift": {
            "props": [
                "luxury gift wrapping",
                "silk ribbon and bow",
                "gift box with lid",
                "premium tissue paper",
                "decorative accent",
                "ribbon spool",
                "premium presentation",
                "elegant background",
            ],
            "lighting": [
                "warm flattering gift presentation light",
                "soft luxury lighting",
                "warm golden accent light",
                "flattering warm glow",
            ],
            "textures": [
                "luxurious silk ribbon",
                "premium paper",
                "gift box cardstock",
                "elegant presentation fabric",
            ],
        },
        "hallway": {
            "props": [
                "pendant hall light",
                "wooden console table",
                "decorative mirror",
                "indoor plant",
                "runner rug",
                "wall sconces",
                "minimal accessories",
                "open sightlines",
            ],
            "lighting": [
                "soft hallway sconce lighting",
                "pendant light overhead",
                "warm accent wall lighting",
                "soft diffused ambient light",
            ],
            "textures": [
                "smooth wall finish",
                "wood console",
                "soft runner fabric",
                "decorative accessories",
            ],
        },
        "kitchen": {
            "props": [
                "stainless steel appliances",
                "granite countertop",
                "pendant lights over island",
                "wooden cutting board",
                "fresh herbs in pot",
                "ceramic cookware",
                "open shelving",
                "island with seating",
            ],
            "lighting": [
                "warm under-cabinet lighting",
                "island pendant lights",
                "natural window light over sink",
                "soft overhead kitchen lighting",
            ],
            "textures": [
                "polished granite",
                "stainless steel",
                "wood grain",
                "ceramic and glass",
            ],
        },
        "living-room": {
            "props": [
                "comfortable sofa",
                "coffee table wood grain",
                "side table with lamp",
                "television console",
                "area rug",
                "throw pillow set",
                "bookshelf",
                "window with drapes",
            ],
            "lighting": [
                "warm sunset light through windows",
                "soft table lamp glow",
                "overhead dimmer lighting",
                "accent lighting from corner lamp",
            ],
            "textures": [
                "plush upholstery",
                "soft area rug",
                "polished wood furniture",
                "soft throw pillows",
            ],
        },
        "meeting-room": {
            "props": [
                "conference table wood or glass",
                "ergonomic office chairs",
                "whiteboard and markers",
                "video conferencing screen",
                "notepad and pen",
                "water pitcher and glasses",
                "minimalist décor",
                "professional lighting",
            ],
            "lighting": [
                "professional neutral overhead lighting",
                "warm professional accent lights",
                "screen display lighting",
                "soft neutral ambient light",
            ],
            "textures": [
                "polished wood or glass",
                "professional chair upholstery",
                "clean presentation surfaces",
                "neutral wall finish",
            ],
        },
        "music-room": {
            "props": [
                "musical instrument stand",
                "acoustic treatment panels",
                "microphone on stand",
                "keyboard or synthesizer",
                "music stand",
                "studio monitor speakers",
                "comfortable stool",
                "sound-dampening materials",
            ],
            "lighting": [
                "warm studio ambient lighting",
                "soft accent spotlight",
                "warm overhead lights",
                "intimate music studio lighting",
            ],
            "textures": [
                "acoustic fabric",
                "polished instrument wood",
                "sound-absorbing materials",
                "studio-grade finishes",
            ],
        },
        "nursery": {
            "props": [
                "white wooden crib",
                "soft area rug",
                "rocking chair",
                "night light soft glow",
                "hanging mobile",
                "changing table",
                "plush stuffed animals",
                "window with sheer curtains",
            ],
            "lighting": [
                "soft warm night light ambiance",
                "gentle window light",
                "warm soft overhead light",
                "gentle accent lighting",
            ],
            "textures": [
                "soft crib linens",
                "plush carpet",
                "smooth painted wood",
                "gentle fabric drapes",
            ],
        },
        "outdoors": {
            "props": [
                "wooden deck or patio",
                "comfortable outdoor chair",
                "potted plants and flowers",
                "outdoor pendant light",
                "natural stone surface",
                "garden view",
                "lounge seating",
                "natural elements",
            ],
            "lighting": [
                "warm golden hour sunlight",
                "soft evening dusk light",
                "landscape outdoor lighting",
                "natural sunset glow",
            ],
            "textures": [
                "natural wood deck",
                "stone patio",
                "living plant foliage",
                "outdoor furniture fabric",
            ],
        },
        "restaurant": {
            "props": [
                "elegant dining table",
                "plush dining chair",
                "dimmed pendant lighting",
                "white tablecloth",
                "fine glassware",
                "silverware place setting",
                "flower arrangement",
                "warm ambiance",
            ],
            "lighting": [
                "warm intimate restaurant lighting",
                "soft candle-like overhead lights",
                "warm accent table lighting",
                "intimate dimmed ambiance",
            ],
            "textures": [
                "fine white linens",
                "polished silverware",
                "fine china",
                "elegant upholstery",
            ],
        },
        "sitting-room": {
            "props": [
                "wingback chair",
                "side table small",
                "reading lamp brass",
                "bookshelf wall",
                "area rug persian",
                "fireplace mantel",
                "throw blanket",
                "cozy seating",
            ],
            "lighting": [
                "warm reading lamp glow",
                "soft fireplace light",
                "warm ambient overhead",
                "intimate cozy lighting",
            ],
            "textures": [
                "velvet upholstery",
                "polished wood",
                "soft throw fabric",
                "warm rug texture",
            ],
        },
        "stairs": {
            "props": [
                "wooden staircase",
                "stair runner carpet",
                "handrail polished wood",
                "wall sconce lighting",
                "open baluster design",
                "landing with accent table",
                "wall art along stairs",
                "natural light from above",
            ],
            "lighting": [
                "warm stair landing light",
                "sconce lights along walls",
                "natural light from upper window",
                "warm ambient stair lighting",
            ],
            "textures": [
                "smooth wooden stairs",
                "soft stair runner",
                "polished handrail",
                "textured wall finish",
            ],
        },
        "study": {
            "props": [
                "wooden desk with surface",
                "ergonomic office chair",
                "desk lamp task lighting",
                "bookshelf with volumes",
                "notepad and pen holder",
                "computer monitor stand",
                "filing cabinet",
                "library aesthetic",
            ],
            "lighting": [
                "warm task lighting desk lamp",
                "soft overhead study light",
                "warm ambient study lighting",
                "focused desk illumination",
            ],
            "textures": [
                "polished wood desk",
                "book spine leather",
                "chair upholstery",
                "paper and writing materials",
            ],
        },
        "waiting-room": {
            "props": [
                "contemporary seating",
                "glass side table",
                "magazine rack with publications",
                "wall-mounted clock",
                "plant corner accent",
                "calm neutral colors",
                "comfortable waiting chair",
                "professional ambiance",
            ],
            "lighting": [
                "soft professional ambient light",
                "warm neutral overhead lighting",
                "soft accent lighting",
                "calm neutral professional glow",
            ],
            "textures": [
                "comfortable chair upholstery",
                "glass table surface",
                "smooth wall finish",
                "neutral fabric materials",
            ],
        },
        "workplace": {
            "props": [
                "modern office desk",
                "ergonomic work chair",
                "computer setup and monitor",
                "desk organizer system",
                "potted desk plant",
                "overhead workspace lighting",
                "professional wall art",
                "productivity aesthetic",
            ],
            "lighting": [
                "bright professional task lighting",
                "neutral overhead office light",
                "bright focused desk illumination",
                "professional neutral workspace light",
            ],
            "textures": [
                "smooth desk surface",
                "chair upholstery",
                "monitor and technology",
                "professional wall finish",
            ],
        },
    }

    @classmethod
    def generate_prompt(
        cls, category: str, variation_index: int
    ) -> str:
        """Generate a dynamic, category-aware mockup scene prompt.

        Args:
            category: One of the 22 standard categories (e.g., 'living-room', 'cafe')
            variation_index: Integer from 1 to 20, used to seed randomization
                           so the same (category, variation) tuple always produces
                           the same prompt

        Returns:
            A detailed text prompt suitable for Gemini image generation

        Raises:
            ValueError: If category not found or variation_index out of bounds
        """
        if category not in cls.CATEGORY_DETAILS:
            raise ValueError(f"Unknown category: {category}")
        if variation_index < 1 or variation_index > 20:
            raise ValueError(f"variation_index must be 1-20, got {variation_index}")

        # Seed randomness with category and variation to ensure
        # the same (category, variation) always produces the same prompt
        random.seed(f"{category}_{variation_index}")

        details = cls.CATEGORY_DETAILS[category]

        # Randomly select one from each detail category
        prop = random.choice(details["props"])
        lighting = random.choice(details["lighting"])
        texture = random.choice(details["textures"])

        # Generate a dynamic prompt with category-specific flavor
        prompt = cls._build_prompt(
            category=category,
            prop=prop,
            lighting=lighting,
            texture=texture,
            variation_index=variation_index,
        )

        return prompt

    @classmethod
    def _build_prompt(
        cls,
        category: str,
        prop: str,
        lighting: str,
        texture: str,
        variation_index: int,
    ) -> str:
        """Construct the final prompt string.

        This method builds a detailed, photorealistic interior scene description
        that includes:
        - Category-specific room setting
        - Dynamic props and furnishings
        - Lighting conditions
        - A prominent matte cyan rectangle on the wall (the artwork placeholder)
        - Photography quality notes

        NOTE: Aspect ratio is NOT included here. It is passed separately
              via the Gemini API config parameter.

        Args:
            category: Room category name
            prop: A specific prop or furniture piece for this variation
            lighting: Description of the lighting condition
            texture: Description of key textures in the scene
            variation_index: The variation number for reference in verbose output

        Returns:
            A complete, detailed prompt string
        """
        # Build category-specific room description
        category_descriptor = cls._get_category_descriptor(category)

        prompt = f"""
Create a photorealistic, professional interior design photograph of a {category_descriptor}.

SCENE COMPOSITION:
- Three-quarter perspective view of the room interior
- Camera positioned to show depth and space
- Well-composed architectural framing
- Professional photography aesthetic

WALL ARTWORK PLACEHOLDER:
- Centered on a wall is a solid, perfectly flat, untextured matte cyan rectangle
- The cyan (#00FFFF) rectangle occupies a reasonable portion of the wall space
- It is completely unobstructed by furniture, plants, or other objects
- The rectangle is genuinely matte (not reflective or glossy)
- Its edges are clean, parallel, and perpendicular to the wall surface
- The rectangle sits naturally in the room's perspective
- CRITICAL: The entire surface of the cyan rectangle must be a perfectly uniform, solid #00FFFF colour with absolutely NO variation of any kind
- CRITICAL: No shadows, cast shadows, light patches, sunlight streaks, warm highlights, reflections, gradients, vignetting, light falloff, or any environmental lighting effect may appear on, across, or overlapping the cyan rectangle at all
- CRITICAL: Room lighting and any shadows from furniture, windows, or lamps must NOT touch or cross the cyan rectangle in any way — they must stop at the rectangle's edges

KEY FURNISHINGS AND DETAILS:
- Include a prominent {prop}
- The room features {texture} surfaces and materials
- Attention to realistic proportions and scale

LIGHTING AND ATMOSPHERE:
- Lighting: {lighting}
- Warm, inviting ambiance
- Natural or professional artificial lighting
- Soft shadows that reveal form without harsh contrast
- Color grading: warm, professional, commercial-quality
- All lighting, shadows, and atmospheric effects are restricted to the room and its furnishings only — the cyan placeholder rectangle must remain completely unaffected by any light or shadow

PHOTOGRAPHY NOTES:
- High-quality product photography aesthetic
- Sharp focus throughout
- Professional color grading
- Clean, polished, magazine-ready appearance
- Variation #{variation_index}: Unique perspective and styling

OUTPUT:
Generate a single, high-quality photorealistic image that matches this exact description.
Ensure the cyan rectangle is clearly visible, unobstructed, and perfectly matte.
"""
        return prompt.strip()

    @classmethod
    def _get_category_descriptor(cls, category: str) -> str:
        """Return a human-friendly room description for a category.

        Args:
            category: Category identifier

        Returns:
            A descriptive phrase for the room type
        """
        descriptors = {
            "bathroom": "modern bathroom",
            "bedroom-adults": "contemporary master bedroom",
            "bedroom-kids": "cheerful children's bedroom",
            "cafe": "upscale café interior",
            "closeup": "detailed studio workspace",
            "dining": "elegant dining room",
            "display": "contemporary gallery display space",
            "gallery": "professional art gallery",
            "games": "modern gaming entertainment room",
            "gift": "luxury gift presentation setup",
            "hallway": "contemporary residential hallway",
            "kitchen": "modern kitchen with island",
            "living-room": "contemporary living room",
            "meeting-room": "professional conference room",
            "music-room": "studio music production room",
            "nursery": "soft, welcoming nursery",
            "outdoors": "outdoor patio and garden space",
            "restaurant": "fine dining restaurant interior",
            "sitting-room": "cozy sitting room with fireplace",
            "stairs": "elegant residential staircase",
            "study": "writer's study with library",
            "waiting-room": "serene professional waiting area",
            "workplace": "modern office workspace",
        }
        return descriptors.get(category, "modern interior space")
