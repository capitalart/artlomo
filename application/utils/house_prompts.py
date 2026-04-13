from __future__ import annotations

SYSTEM = """You are a Senior Art Curator & Etsy Specialist for Robin Custance.
Output MUST be plain text (no HTML). Use Australian spelling.
Cultural guardrails: be respectful of Aboriginal culture; never claim sacred/secret knowledge; do not invent Dreaming details; only state heritage/Country provided by the user.
Links: only Etsy URLs are allowed. Do not include email addresses, phone numbers, QR codes, or third-party shop/print links.
Formatting: use --- as the ONLY separator between paragraphs to create a cohesive text block. Use only the allowed emoji set when indicated."""

USER_FULL = """ARTWORK
- Title: {title}
- Slug: {slug}
- Aspect: {aspect}
- Technical Authority: Artwork files range from 7,200px (up to 24-inch prints) to 14,400px (museum-grade 48-inch prints) at 300 DPI. Format: JPEG.
- Print sizes: 10×12.5\" (25×32 cm); 16×20\" (40×50 cm); 24×30\" (60×76 cm); 32×40\" (81×102 cm); 38.4×48\" (97.5×122 cm)
- Artist Bio: Robin Custance is a descendant of the Boandik (Bunganditj) people, known as the People of the Reeds, from the Naracoorte - Mt Gambier Region of South Australia. Creating digital landscapes from Kaurna Country (Adelaide), Robin's connection to water, wetlands, and limestone country flows through each work. Each artwork is envisioned and generated through carefully crafted digital prompts, then meticulously upscaled, refined, and digitally signed.
- Licensing: digital download; personal use only

STYLE
- Pioneer Engine v1.0
- Tone: warm, contemporary, trustworthy
- Emojis allowed (sparingly): 🎨 ✨ 🙌 🖼 🚀 ✅ 👉 📩 ❤️ 🛒 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣

PIONEER EXECUTION RULES
1. Paragraph Separator: Use --- as the ONLY separator between paragraphs (no blank lines).
2. Character Density: Every paragraph MUST be at least 250 characters long to maximise Etsy SEO indexing.
3. 13-Paragraph Structure: The description MUST contain exactly 13 emoji-led story blocks joined by ---.
4. Technical Authority: Block 7 MUST cite "14,400px" and "300 DPI" as the museum-quality standard.
5. Heritage Guard: The artist bio section MUST mention "People of the Reeds" (Boandik/Bindjali).
6. No Quotes: Never wrap field values in quotation marks.
7. No AI Meta: Never include phrases like "As an AI" or external artist names (e.g., Monet, Picasso).

SECTIONS (exact order, exact headings):
1) 🎨 About the Artist – Robin Custance
2) ✨ Did You Know? Aboriginal Art & the Spirit of Dot Painting
3) 🖼 4:5 (Vertical)
4) 📐 Printing Tips
5) 🏪 Top 10 Print-On-Demand Services (optional — brand names only, no links, add disclaimer)
6) ⚠️ Important Notes
7) 📏 Museum-Quality Technical Specs
8) ❓ Frequently Asked Questions
9) 🚀 Explore My Work
10) 💫 Why You'll Love This Artwork
11) 🛒 How To Buy & Print
12) 🙌 Thank You
13) ❤️ People of the Reeds Acknowledgement

TASK
Write the FULL description with exactly 13 emoji-led paragraphs in the order above. Each paragraph must be at least 250 characters. Separate paragraphs with --- only.
Include the Etsy shop link only in section "🚀 Explore My Work": {etsy_url}
P.S.
The shop link must be shown as the FULL literal URL exactly: {etsy_url}
- Do NOT shorten it.
- Do NOT omit "https://".
- Do NOT use anchor/markdown or "text link" phrasing. Print the raw URL in the sentence.
Forbidden wording (must NEVER appear in this exact order anywhere):
- 'download artwork by Robin Custance'
- 'download art by Robin Custance'
- 'download wall artwork by Robin Custance'
- 'download wall art by Robin Custance'
Return plain text only (no JSON)."""

USER_SECTION = """ARTWORK
- Title: {title}
- Slug: {slug}
- Aspect: {aspect}

STYLE
- Pioneer Engine v1.0; follow the specific section rules and emoji limits.
- Character Density: This section MUST be at least 250 characters long.

TASK
Rewrite the following section to match Pioneer Engine v1.0. Keep the heading unchanged. Respect facts and do not add external links.

SECTION TITLE: {section_title}

CURRENT TEXT:
{section_text}

P.S.
If this section includes the shop link, show the FULL literal URL exactly: {etsy_url}
(no shorteners, no markdown, no anchor text).
RETURN
Plain text for this ONE section only (at least 250 characters).
Forbidden wording (must NEVER appear in this exact order anywhere):
- 'download artwork by Robin Custance'
- 'download art by Robin Custance'
- 'download wall artwork by Robin Custance'
- 'download wall art by Robin Custance'
"""

LISTING_BOILERPLATE = """---
🏆 LIMITED EDITION
This digital release is limited to 25 copies maximum.
---
📏 TECHNICAL SPECIFICATIONS
• File type: 1 × High-Resolution JPEG
• Resolution: 7,200–14,400px (long edge) @ 300 DPI
• Max print size: Up to 48 inches (121.9 cm) at 14,400px; up to 24 inches (61 cm) at 7,200px
• Aspect ratio: Print to your preferred proportions
---
✨ THE DIGITAL CRAFT BEHIND THE FILE
While the vision for each artwork begins with AI-guided generation, what you receive is far more than an algorithm's output—it's a labor of digital craft. Every file undergoes my custom upscaling process, meticulously designed to achieve 7,200–14,400px resolution at 300 DPI, enabling flawless prints from 24 to 48 inches. I personally inspect each piece for clarity and tonal balance, making careful color corrections to ensure the file translates beautifully when printed by professional labs. This isn't a raw export—it's a refined, exhibition-ready digital artwork, digitally signed to guarantee authenticity. You're not just downloading pixels; you're receiving a piece that has been lovingly prepared to honor the landscape it represents.
---
🎨 ABOUT THE ARTIST
I am Robin Custance, a South Australian digital artist and descendant of the Boandik (Bunganditj) people, known as the People of the Reeds, from the Naracoorte - Mt Gambier Region. My connection to water, wetlands, and limestone country flows through each work. Each artwork is envisioned and generated through carefully crafted digital prompts, then meticulously upscaled, refined, and digitally signed to museum-quality standards. My practice explores contemporary landscape through algorithmic patterns and modern digital abstraction.
---
❤️ ACKNOWLEDGEMENT OF COUNTRY
As a descendant of the Boandik (Bunganditj) people, known as the People of the Reeds, I create with deep respect for the Traditional Custodians of all lands across Australia. I pay my respects to Elders past, present, and emerging.
---
📐 PRINTING & SIZE GUIDE
Optimised for over 15 standard sizes including 18×24, 24×32, 30×40, and 36×48 inches. For museum-grade results, use a professional print lab."""

TECHNICAL_EXCELLENCE_BLOCK = """✨ THE DIGITAL CRAFT BEHIND THE FILE

While the vision for each artwork begins with AI-guided generation, what you receive is far more than an algorithm's output—it's a labor of digital craft. Every file undergoes my custom upscaling process, meticulously designed to achieve up to 14,400px resolution at 300 DPI — the museum-quality standard for flawless 48-inch prints. Files start at 7,200px, enabling crisp 24-inch output at 300 DPI.

I personally inspect each piece for clarity and tonal balance, making careful color corrections to ensure the file translates beautifully when printed by professional labs. This isn't a raw export—it's a refined, exhibition-ready digital artwork, digitally signed to guarantee authenticity. You're not just downloading pixels; you're receiving a piece that has been lovingly prepared to honor the landscape it represents."""

def build_seed_context(seed_info: dict | None) -> str:
    """Build the seed context injection block dynamically based on provided fields.
    
    Empty fields are omitted entirely rather than shown as "(not provided)".
    - If location is empty: Do not mention location in the prompt.
    - If sentiment is empty: Instruct AI to use its own emotional interpretation.
    - If original_prompt is empty: Proceed with visual-only stylistic analysis.
    """
    if not seed_info:
        return ""
    
    location = str(seed_info.get("location") or "").strip()
    # Support both "sentiment" (new) and "notes" (legacy) field names
    sentiment = str(seed_info.get("sentiment") or seed_info.get("notes") or "").strip()
    original_prompt = str(seed_info.get("original_prompt") or "").strip()
    
    # If nothing provided, return empty
    if not any([location, sentiment, original_prompt]):
        return ""
    
    # Build context dynamically
    blocks = ["ARTIST-PROVIDED CONTEXT (GUIDED CREATIVE ENGINE):"]
    blocks.append("The artist has provided anchors for this piece. Use ONLY the provided fields to guide your analysis.")
    
    if location:
        blocks.append(f"""
- Location / Country: {location}
  (Use as factual setting for the NARRATIVE STORYTELLING MODULE. Create sensory-rich hooks specific to this place: the smell of rain on limestone, the light on country tracks, the feel of this landscape. Weave this location naturally into the opening narrative hook.)""")
    
    if sentiment:
        blocks.append(f"""
- General Info / Sentiment: {sentiment}
  (PRIMARY CREATIVE ANCHOR — Treat this as the tonal foundation. Extrapolate this sentiment into the vocabulary, rhythm, and emotional texture of the ENTIRE description, especially the narrative storytelling opening. Do not repeat the sentiment word; use it to choose the vocabulary and cadence of the prose. EMBODY it throughout.)

EXTRAPOLATION ENGINE: Build the entire narrative around this feeling. For example, if "Ghostly" is provided, use haunting, translucent, spectral, whispered language throughout the narrative storytelling opening and description.""")
    else:
        blocks.append("""
- Sentiment: (Not provided)
  Use your own emotional interpretation based purely on what you observe in the artwork. Let the visual elements guide the mood and tone of your description.""")
    
    if original_prompt:
        blocks.append(f"""
- Creative Foundation: {original_prompt}
  (INTERNAL STYLISTIC INTELLIGENCE — Use this to understand the digital generation process, visual elements, and artistic intent. This helps you describe texture, composition, and visual style accurately.)

CRITICAL PRIVACY RULE: The "Creative Foundation" text is strictly internal. Use it to inform your stylistic descriptions (e.g., "luminous digital texture", "meticulously generated patterns", "carefully composed elements") but NEVER output the raw prompt text in the final description.""")
    else:
        blocks.append("""
- Creative Foundation: (Not provided)
  Proceed with visual-only stylistic analysis. Describe what you observe in terms of texture, technique, and visual style based purely on the image.""")
    
    return "\n".join(blocks)


ANALYSIS_PROMPT = """You are a visual metadata extraction engine for fine-art digital files.

Return ONLY a raw JSON object. Do not include:
- Markdown code blocks or fencing
- Headers, footers, or explanatory text
- Artist biographies or personal narratives
- Printing specifications or technical notes
- Acknowledgement of Country or cultural preambles
- Any text before or after the JSON

Focus strictly on visual metadata extraction:
- Dominant colours (from allowed palette)
- Visual composition analysis
- Subject matter identification
- Mood and atmosphere
- SEO-optimized title and tags

Output format: A single valid JSON object with no surrounding text.

DESCRIPTION STRUCTURE RULE:
When generating the 'etsy_description' field, the AI MUST structure it as:
[Generated Impressionistic Description based on visual analysis]
---
[Append the standard LISTING_BOILERPLATE verbatim]"""
