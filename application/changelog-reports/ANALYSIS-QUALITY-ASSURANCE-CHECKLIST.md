# ARTLOMO ANALYSIS QUALITY ASSURANCE CHECKLIST

**Version:** 4.0 (Ultimate Quality Implementation)
**Last Updated:** March 3, 2026
**Purpose:** Ensure every AI-generated artwork description achieves museum-grade quality

---

## PRE-ANALYSIS PREPARATION

### Image Quality Check

- [ ] Image file size is reasonable (not corrupted or truncated)

- [ ] Image dimensions support 14,400px long edge claim (original should be sizable)

- [ ] Image color profile is recognizable (not grayscale if colors present)

- [ ] No visible artifacts, blurriness, or compression issues in source

### Metadata Preparation

- [ ] SKU is valid and consistent

- [ ] Original filename is available and clean

- [ ] Aspect ratio is calculated correctly (2:3, 3:4, or 4:5)

- [ ] Seed context is provided if available (location, sentiment, original prompt)

### Configuration Review

- [ ] Temperature is set to 0.7 (for storytelling with heart)

- [ ] Max tokens is set to 2000+ (allows for comprehensive descriptions)

- [ ] Model selection matches availability (GPT-4o or latest available)

- [ ] Request timeout is adequate (60+ seconds)

---

## DURING API CALL MONITORING

### OpenAI Specific

- [ ] Request is logged to listing-request.md for debugging

- [ ] Response format constraint is used (structured output)

- [ ] max_completion_tokens prevents truncation

- [ ] Error handling captures and classifies failures

- [ ] Retry logic respects rate limits and timeouts

### Gemini Specific

- [ ] Client is initialized as singleton (cost efficiency)

- [ ] API key is valid and has adequate quota

- [ ] Response parsing handles JSON gracefully

- [ ] Error classification matches Gemini error types

- [ ] Fallback mechanism to manual analysis if needed

---

## POST-ANALYSIS VALIDATION (CRITICAL)

### Character Count

- [ ] **MINIMUM:** 850 characters total

- [ ] **TARGET:** 950-1,100 characters for optimal conversion

- [ ] Count includes all sections from headline through signature

- [ ] No unnecessary padding or repetition

### Plain Text Compliance (ESSENTIAL)

- [ ] NO HTML tags present (search: <, >)

- [ ] NO markdown syntax (search: #, ~~, `, **, __)

- [ ] NO straight double quotes (") allowed

- [ ] NO markdown bold with asterisks (**text**)

- [ ] Line breaks are newline characters (\n), not HTML `````<br>`````

- [ ] Emojis are present and render correctly

### Heritage Statement Accuracy

- [ ] Text contains: "Boandik (Bunganditj)—the People of the Reeds"

- [ ] Uses Unicode em-dash (—) NOT hyphen (-) or double-hyphen (--)

- [ ] Heritage section is respectful and accurate

- [ ] No claims of Indigenous ownership or sacred knowledge

- [ ] Translation "People of the Reeds" is included

### Technical Specifications

- [ ] Mentions "14,400px" or "14,400 pixels"

- [ ] Mentions "300 DPI"

- [ ] Mentions "48-inch" or "48 inches" (with optional metric)

- [ ] Mentions "museum-quality" or "gallery-ready" or "gallery-style"

- [ ] All specs are accurate and not inflated

### Section Structure

- [ ] 7 main sections present with correct emojis:

  - [ ] 🌅 Title/Hook

  - [ ] 🌿 Soul of the Piece

  - [ ] 🙌 Connection to Country

  - [ ] 💎 Technical Excellence

  - [ ] 📐 Printing Guide

  - [ ] 🛒 How to Buy & Print

  - [ ] ❤️ Thank You & Stay Connected

  - [ ] Sections appear in correct order

  - [ ] Proper separators (---) between major sections

### Narrative Quality

- [ ] Opening sensory hook is vivid and specific

- [ ] "Soul of the Piece" includes visual read and emotional connection

- [ ] Heritage connection is woven naturally (not bolted on)

- [ ] Digital craft transition explains AI → upscaling → refinement

- [ ] Descriptive language is evocative (not generic)

- [ ] No clichés or overused art-speak

### Voice & Tone

- [ ] Tone is "Museum-Grade Curator meets Aussie Campfire Storyteller"

- [ ] Language is warm and personal (not corporate)

- [ ] Australian English is used (Colour, Grey, Ochre, Recognise)

- [ ] First person voice (Robin's perspective)

- [ ] Conversational and approachable

### Forbidden Language Check

- [ ] NO "I painted" or "painted with"

- [ ] NO "brushstrokes" or "brush marks"

- [ ] NO "on canvas"

- [ ] NO "oils," "acrylics," or "pigments"

- [ ] NO "painterly" or "abstract expressionism"

- [ ] NO unsupported styling language

### Required Language Check

- [ ] Uses "I rendered," "I generated," "I envisioned"

- [ ] Includes "digital layers," "light-filled strokes"

- [ ] Mentions "luminous digital composition"

- [ ] References "gallery-ready digital file"

- [ ] Uses "meticulously upscaled"

- [ ] Describes "museum-quality clarity"

### Color Accuracy

- [ ] Colors mentioned are from Palette analysis only

- [ ] No invented colors like "Midnight Indigo"

- [ ] Colors are specific and evocative

- [ ] Color descriptions support visual read section

### Geographic Accuracy

- [ ] Location specificity is maintained (no over-generalization)

- [ ] Region attribution is accurate

- [ ] Place names are spelled correctly

- [ ] Geographic references support the narrative

### Mobile Readability

- [ ] Adequate line breaks for small screens

- [ ] No single paragraph exceeds 4-5 lines

- [ ] Blank lines after emoji headers

- [ ] Blank lines between all sections

- [ ] No continuous prose blocks

- [ ] Bullet points break up information

### Title Validation

- [ ] Title is <= 140 characters

- [ ] Title includes location or vibe

- [ ] Title includes "Digital Download" or "Digital Art"

- [ ] Title includes "48 Inch" or similar size indicator

- [ ] Title uses pipe separators (|)

- [ ] NO quotation marks in title

### Tags Validation

- [ ] Exactly 13 tags

- [ ] Each tag is max 20 characters

- [ ] All tags are lowercase or properly capitalized

- [ ] NO special characters (except spaces and hyphens)

- [ ] NO artist names (Robin Custance, etc.)

- [ ] NO generic terms (Art, Artwork, Digital, Abstract)

- [ ] All tags focus on BUYER INTENT:

  - [ ] Room type (Living Room, Office, Bedroom)

  - [ ] Gift occasions (Housewarming, Birthday)

  - [ ] Size descriptors (48 Inch, Large Scale)

  - [ ] Use cases (Wall Art, Home Decor, Statement Piece)

  - [ ] Style descriptors (Modern, Contemporary, Australian)

### Materials List Validation

- [ ] Exactly 13 materials

- [ ] In standard order (Digital Download, High-Res JPG, etc.)

- [ ] No features or properties (only product types)

- [ ] All materials are relevant to digital downloads

- [ ] No duplication

### Colors Validation

- [ ] Primary color is standard color name

- [ ] Secondary color is standard color name

- [ ] Both colors match the artwork palette

- [ ] Colors are from approved list (Black, Blue, Brown, Gold, Green, Grey, Orange, Pink, Purple, Red, Silver, Teal, White, Yellow)

### SEO Filename Validation

- [ ] Lowercase only

- [ ] Hyphens only (no underscores, spaces, dots)

- [ ] Max 61 characters

- [ ] Includes SKU prefix

- [ ] Includes location reference

- [ ] Human-readable and descriptive

---

## ETSY COMPATIBILITY TEST

### Preview Rendering

- [ ] View description in Etsy "preview" (if available)

- [ ] Verify emoji rendering is correct

- [ ] Verify line breaks display properly

- [ ] Verify no HTML tags are visible

- [ ] Check mobile view (Etsy is 60%+ mobile traffic)

### Strip Test

- [ ] Imagine Etsy strips all attempted formatting

- [ ] Description still reads well in plain text

- [ ] Emojis add visual interest without being critical

- [ ] Line breaks are essential for readability

- [ ] Content flows logically

### Character Encoding

- [ ] Em-dashes (—) are Unicode character U+2014

- [ ] No smart quotes or special typography

- [ ] Unicode bullets (•) render correctly

- [ ] Star emoji and other emojis are standard Unicode

---

## FINAL QUALITY GATES

### Gate 1: Content Quality

✅ OR ❌

- [ ] Description tells a compelling story

- [ ] Sensory language is vivid and specific

- [ ] Heritage connection feels authentic

- [ ] Technical value is clearly justified

- [ ] Buyer would feel confident purchasing

### Gate 2: Etsy Compliance

✅ OR ❌

- [ ] Plain text with no HTML/markdown

- [ ] All required specs mentioned

- [ ] Heritage statement formatted correctly

- [ ] 850+ characters for SEO

- [ ] 13 tags with buyer intent

- [ ] 13 materials in standard order

### Gate 3: Accuracy & Integrity

✅ OR ❌

- [ ] No false claims about print size

- [ ] No inaccurate geographic info

- [ ] No unsupported color or material claims

- [ ] Heritage references are respectful

- [ ] No clichéd or generic language

### Gate 4: Cultural Sensitivity

✅ OR ❌

- [ ] Heritage acknowledgement is respectful

- [ ] Translation of Boandik/Bunganditj is included

- [ ] No claims of Indigenous ownership

- [ ] Connection to Country is authentic

- [ ] Language honors traditions appropriately

---

## QUALITY SCORE CALCULATION

## Perfect Score: 100 points

- Content Quality (25 points):

  - [ ] Narrative excellence (sensory, emotional, specific)

  - [ ] Voice consistency (warm, authentic, Australian)

  - [ ] Word choice (vivid, appropriate, no clichés)

  - [ ] Flow and structure (logical, engaging, compelling)

  - [ ] Originality (unique perspective, not templated)

  - Etsy Compliance (25 points):

  - [ ] Plain text format (no HTML/markdown)

  - [ ] Character count (850+ minimum)

  - [ ] Section structure (7 sections, correct order)

  - [ ] Technical specs (14,400px, 300 DPI, 48-inch mentioned)

  - [ ] Heritage formatting (em-dash required)

  - Formatting & Readability (20 points):

  - [ ] Mobile-friendly (adequate line breaks, short paragraphs)

  - [ ] Visual hierarchy (emojis, bullets, separators)

  - [ ] Typography (no quotation marks, proper Unicode)

  - [ ] Layout (whitespace, breathing room between sections)

  - [ ] Accessibility (clear, easy to scan)

  - Accuracy & Integrity (15 points):

  - [ ] Geographic accuracy (correct location references)

  - [ ] Technical accuracy (realistic claims, justified value)

  - [ ] Color accuracy (palette matches artwork)

  - [ ] Heritage accuracy (respectful, informed)

  - [ ] No false or misleading claims

  - SEO & Discoverability (15 points):

  - [ ] Title optimization (140 chars, keywords, separators)

  - [ ] Tag relevance (buyer intent, not generic)

  - [ ] Filename SEO (descriptive, includes location)

  - [ ] Keyword distribution (natural, not stuffed)

  - [ ] Searchability (terms buyers actually use)

---

## CONTINUOUS IMPROVEMENT

### After Each Analysis

- [ ] Log any validation failures

- [ ] Note any common issues with the model

- [ ] Record any improvements to prompts needed

- [ ] Flag any cultural sensitivity concerns

- [ ] Update best practices if new insights emerge

### Monthly Reviews

- [ ] Analyze conversion metrics (if available)

- [ ] Review buyer feedback and questions

- [ ] Identify patterns in successful vs. unsuccessful listings

- [ ] Refine prompts based on performance data

- [ ] Update this checklist with new learnings

### Quarterly Updates

- [ ] Re-test both OpenAI and Gemini models

- [ ] Verify Etsy requirements haven't changed

- [ ] Review heritage protocol updates

- [ ] Benchmark against competing listings

- [ ] Publish updated best practices guide

---

## QUICK REFERENCE: TOP 10 QUALITY REQUIREMENTS

These are the TOP 10 things that guarantee success:

1. **PLAIN TEXT ONLY** - No HTML, no markdown. Period.

1. **850+ CHARACTERS** - Google SEO minimum. Aim for 950-1,100.

1. **EM-DASH IN HERITAGE** - "Boandik (Bunganditj)—the People of the Reeds" (exact)

1. **VIVID SENSORY OPENING** - Make the buyer FEEL the place

1. **TECHNICAL VALUE JUSTIFIED** - Explain why 14,400px = 48 inches @ 300 DPI

1. **AUTHENTIC VOICE** - Warm curator + Aussie storyteller = genuine

1. **MOBILE READABILITY** - Adequate line breaks, short paragraphs, whitespace

1. **BUYER INTENT TAGS** - What do customers SEARCH for? Use that language

1. **EXACT MATERIALS LIST** - 13 items in standard order, no substitutions

1. **ETSY COMPLIANCE** - Render correctly on mobile, no stripped HTML, plain text

If you get these 10 right, the listing will convert.

---

## TROUBLESHOOTING

### Issue: Description feels generic

- **Solution:** Add more specific sensory details. Research the location. Reference unique visual elements from the artwork.

### Issue: Character count is too low

- **Solution:** Expand the "Soul of the Piece" section. Add more detail about colors, rhythm, and emotional impact. Include more specific geographic context.

### Issue: Buyer intent tags are weak

- **Solution:** Replace generic terms with search terms. What would you type into Etsy to find this artwork? Use that language.

### Issue: Heritage statement doesn't feel authentic

- **Solution:** Ensure it's woven naturally into the narrative, not bolted on. Show HOW the artwork reflects the connection to Country.

### Issue: Content is too salesly or corporate

- **Solution:** Use first person (Robin's voice). Add warmth. Reference specific places and sensations. Use conversational language.

### Issue: Emojis don't render or look wrong

- **Solution:** Verify emoji are standard Unicode. Test on mobile. Keep emoji selection simple and relevant.

### Issue: Technical specs aren't compelling

- **Solution:** Explain the WHY. 14,400px doesn't mean much—but "14,400px = up to 48-inch prints at 300 DPI for gallery-quality clarity" DOES mean something.

---

## FINAL NOTE

This checklist represents the culmination of research into Etsy best practices, cultural sensitivity, technical excellence, and conversion optimization. Every item exists because it either improves buyer experience, ensures platform compliance, or increases conversion likelihood.

Use this checklist for EVERY analysis. Make it part of your quality culture.

Quality is not an accident. It's a choice. Choose it every time.
