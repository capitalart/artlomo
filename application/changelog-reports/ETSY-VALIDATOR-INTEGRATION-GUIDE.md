# ETSY VALIDATOR INTEGRATION GUIDE

**Version:** 1.0
**Date:** March 3, 2026
**Purpose:** Show how to validate AI-generated Etsy descriptions for compliance and quality

---

## OVERVIEW

The `etsy_validator.py` module provides automated validation of artwork descriptions to ensure they meet Etsy's strict requirements:

- **Plain text only** (no HTML or markdown)

- **Minimum 850 characters** for SEO

- **Exactly 13 tags** with buyer intent focus

- **Heritage statement** with proper em-dash formatting

- **All required sections** present with correct structure

---

## WHAT THE VALIDATOR CHECKS

### Description Validation

## Critical Errors (will mark invalid)

- Total length < 850 characters

- Contains HTML tags (`<h1>`, `<br>`, etc.)

- Contains markdown syntax (`###`, `~~`, etc.)

- Uses forbidden language ("painted," "brushstrokes," etc.)

## Warnings (doesn't fail, but flags for improvement)

- Doesn't start with emoji header

- Missing heritage statement

- Uses hyphens (-) instead of em-dash (—)

- Doesn't mention 14,400px resolution

- Insufficient line breaks for mobile

- Few emojis for visual hierarchy

### Tags Validation

## Critical Errors

- Not exactly 13 tags

- Any tag exceeds 20 characters

- Invalid characters in tags

## Warnings

- Generic tags ("Art," "Artwork") detected

- Technical tags ("14400px") detected

- Artist name in tags

### Title Validation

Critical Errors

- Exceeds 140 characters

- Very short (< 30 chars)

Warnings

- Missing "48" or size reference

- Missing "Digital" or "Download"

- No pipe separators

### Complete Analysis Validation

Validates the entire output object (title, description, tags, colors, filename).

---

## BASIC USAGE EXAMPLES

### 1. Validate a Single Description

```python
from application.analysis.etsy_validator import validate_description, EtsyValidationResult

# Load your description

description = """
| 🌅 Bool Lagoon Dreamtime | Limestone Wetlands | Large 48-Inch Statement Art |

Premium Digital Download...
[rest of description]
"""

# Validate it

result = validate_description(description)

# Check if valid

if result.is_valid:
    print("✅ Description passes all checks")
else:
    print("❌ Description has issues:")
    for error in result.errors:
        print(f"  ERROR: {error}")

# Print all warnings too

for warning in result.warnings:
    print(f"  WARNING: {warning}")

# Get full report

print(result)  # Pretty-printed with all details
```

### 2. Validate Tags

```python
from application.analysis.etsy_validator import validate_tags

tags = [
    "Large Office Decor",
    "Aussie Housewarming",
    "48 Inch Wall Art",
    "Living Room Art",
    "Modern Home Decor",
    "Contemporary Art Print",
    "Digital Download Art",
    "Printable Home Decor",
    "Statement Wall Piece",
    "Landscape Print Gift",
    "Professional Wall Art",
    "Gallery Quality Print",
    "Earth Tone Home Decor"
]

result = validate_tags(tags)

print(result)  # Will show 13 tags valid
```

### 3. Validate Complete Analysis Output

```python
from application.analysis.etsy_validator import validate_complete_analysis

# Your API response

analysis = {
    | "etsy_title": "Bool Lagoon Dreamtime | Limestone Wetlands | Large 48-Inch Statement Art", |
    "etsy_description": "🌅 [full description with all sections...]",
    "etsy_tags": [...],  # list of 13 tags
    "seo_filename_slug": "rjc-0042-bool-lagoon-by-robin-custance",
    "visual_analysis": {"subject": "...", "dot_rhythm": "...", "palette": "...", "mood": "..."},
    "materials": [...],  # list of 13 materials
    "primary_colour": "Blue",
    "secondary_colour": "Green"
}

result = validate_complete_analysis(analysis)

# Print comprehensive report

print(result)

# Access individual results

if not result.is_valid:
    print("\nFIX THESE ERRORS:")
    for error in result.errors:
        print(f"  ❌ {error}")

if result.warnings:
    print("\nOPTIONAL IMPROVEMENTS:")
    for warning in result.warnings:
        print(f"  ⚠️  {warning}")
```

---

## INTEGRATION WITH ANALYSIS SERVICES

### After OpenAI Analysis

```python
from application.analysis.openai.service import analyse_artwork
from application.analysis.etsy_validator import validate_complete_analysis
import logging

logger = logging.getLogger("ai_processing")

async def analyse_with_validation(image_bytes, sku, **kwargs):
    """Analyse artwork with automatic Etsy validation."""

    # Run analysis
    analysis_result = await analyse_artwork(
        image_bytes=image_bytes,
        sku=sku,
        **kwargs
    )

    # Validate result
    validation = validate_complete_analysis(analysis_result.output)

    # Log results
    if validation.is_valid:
        logger.info(f"[OPENAI] {sku} analysis PASSED validation")
    else:
        logger.warning(f"[OPENAI] {sku} analysis FAILED validation:")
        for error in validation.errors:
            logger.warning(f"  {error}")
        for warning in validation.warnings:
            logger.warning(f"  {warning}")

    # Return analysis with validation info
    analysis_result.validation = validation
    return analysis_result
```

### After Gemini Analysis

```python
from application.analysis.gemini.service import analyse_artwork
from application.analysis.etsy_validator import validate_complete_analysis

async def analyse_with_validation(image_bytes, sku, **kwargs):
    """Analyse artwork with automatic Etsy validation (Gemini)."""

    # Run analysis
    analysis_result = await analyse_artwork(
        image_bytes=image_bytes,
        sku=sku,
        **kwargs
    )

    # Validate result
    validation = validate_complete_analysis(analysis_result.output)

    # Store validation alongside result
    return {
        "analysis": analysis_result.output,
        "validation": validation,
        "model": "gemini-pro-vision",
        "is_compliant": validation.is_valid
    }
```

---

## VALIDATION WORKFLOW

### Recommended Process

```text
1. AI generates description
2. Validator checks for compliance
3. If invalid:
   a. Log specific errors
   b. Regenerate using feedback
   c. Re-validate until passing
4. If valid:
   a. Store with validation timestamp
   b. Save to Etsy-compatible format
   c. Ready for upload
```

### Error Recovery Pattern

```python
from application.analysis.etsy_validator import validate_description

MAX_RETRIES = 3
attempt = 0
description = initial_description

while attempt < MAX_RETRIES:
    result = validate_description(description)

    if result.is_valid:
        print(f"✅ Valid after {attempt + 1} attempt(s)")
        return description

    # Extract what failed
    error_summary = " | ".join(f"{e[:50]}..." for e in result.errors[:2])
    print(f"Attempt {attempt + 1} failed: {error_summary}")

    # Request regeneration with feedback
    description = regenerate_with_feedback(
        original_description=description,
        errors=result.errors,
        warnings=result.warnings
    )

    attempt += 1

# After max retries

if not result.is_valid:
    log_critical_failure(
        sku=sku,
        errors=result.errors,
        warnings=result.warnings
    )
```

---

## COMMON VALIDATION FAILURES & FIXES

### Error: "Description too short"

**What it means:** < 850 characters

## How to fix

```python

# Expand the Soul of the Piece section

# Add more color description

# Reference more visual details

# Describe emotional impact more

# Check with character count

desc_length = len(description)
print(f"Current: {desc_length} chars (need 850+)")
```

### Error: "No HTML tags"

**What it means:** HTML was detected in output

How to fix

```python

# Search for common HTML patterns

import re

if re.search(r'<[^>]+>', description):
    print("FOUND HTML TAGS!")
    # Remove or replace
    description = description.replace("<br>", "\n")
    description = description.replace("<h2>", "")
    description = description.replace("</h2>", "")
```

### Error: "Heritage statement uses hyphen"

**What it means:** Using "-" or "--" instead of "—"

How to fix

```python

# Replace regular hyphens with em-dash

description = description.replace("Boandik (Bunganditj) - the People",
                                  "Boandik (Bunganditj)— the People")

# Or ensure the correct Unicode character

description = description.replace("(Bunganditj)--", "(Bunganditj)—")
```

### Warning: "Too few emojis"

**What it means:** < 5 emojis for visual breaks

How to fix

```python

# Add strategic emojis

# Examples: • ✨ 🖼️ 🍃 🌭 🇦🇺 ❤️

# Each section should have emoji header

# Add emojis to important points

# But don't overdo it (max ~15 total)

```

### Warning: "Missing 14,400px mention"

**What it means:** Technical spec not stated

How to fix

```python

# Add to Technical Excellence section

text.append("You'll receive a museum-quality JPG at 14,400px and 300 DPI.")

# Or weave into opening

text.append("Experience this 14,400px digital artwork in museum-quality detail.")
```

---

## LOGGING & MONITORING

### Log Validation Results

```python
import logging
from application.analysis.etsy_validator import validate_complete_analysis

logger = logging.getLogger("ai_processing")

def log_validation(sku, analysis, validation):
    """Log validation results for monitoring."""

    status = "VALID ✅" if validation.is_valid else "INVALID ❌"

    logger.info(
        | f"[VALIDATION] {sku} | {status} | " |
        f"Errors: {len(validation.errors)} | "
        f"Warnings: {len(validation.warnings)}"
    )

    if validation.errors:
        logger.warning(f"[VALIDATION] {sku} Errors:")
        for error in validation.errors:
            logger.warning(f"  • {error}")

    if validation.warnings:
        logger.info(f"[VALIDATION] {sku} Warnings:")
        for warning in validation.warnings:
            logger.info(f"  • {warning}")
```

### Dashboard Metrics

```text
VALIDATION METRICS (Daily)

Total Analyses: 42
Valid (first try): 38 (90.5%)
Valid (after regen): 4 (9.5%)
Failed (after retries): 0 (0%)

Common Errors:
1. Character count too low: 3 times
2. Missing heritage statement: 0 times
3. HTML tags detected: 0 times

Average Retry Attempts: 0.1 per analysis
Success Rate: 100%
```

---

## BEST PRACTICES

### 1. Always Validate Before Saving

```python

# Good

analysis = await generate_analysis(image)
validation = validate_complete_analysis(analysis)
if validation.is_valid:
    save_to_database(analysis)

# Bad

analysis = await generate_analysis(image)
save_to_database(analysis)  # Might be invalid!
```

### 2. Use Warnings for Continuous Improvement

```python

# Warnings don't fail validation, but they're valuable

if validation.warnings:
    # Track which warnings are most common
    log_warning_trends(validation.warnings)

    # Maybe update prompts to avoid them
    # Or create a "good" vs "excellent" tier
```

### 3. Test Both Models

```python

# OpenAI tends to produce slightly different output than Gemini

# Validate both separately to understand differences

openai_result = await openai_analyze(image)
openai_validation = validate_complete_analysis(openai_result)

gemini_result = await gemini_analyze(image)
gemini_validation = validate_complete_analysis(gemini_result)

# Compare quality metrics

compare_validation_results(openai_validation, gemini_validation)
```

### 4. Create Custom Validators if Needed

```python
from application.analysis.etsy_validator import validate_description, EtsyValidationResult

def validate_brand_voice(description):
    """Custom validator for Robin's specific voice."""
    result = EtsyValidationResult(is_valid=True)

    # Check for specific phrases that signal good voice
    positive_phrases = [
        "sensory",
        "luminous",
        "ancient wetlands",
        "People of the Reeds"
    ]

    found_phrases = sum(1 for phrase in positive_phrases if phrase in description)

    if found_phrases < 2:
        result.add_warning(f"Only {found_phrases}/4 brand voice phrases found")

    return result
```

---

## RUNNING VALIDATION INDEPENDENTLY

### Command Line Testing

```bash

# Test validation logic directly

python -m application.analysis.etsy_validator

# Or create a test script

cat > test_validator.py << 'EOF'
from application.analysis.etsy_validator import validate_description, validate_tags

# Load test description

with open('sample_description.txt') as f:
    desc = f.read()

# Validate

result = validate_description(desc)
print(result)

# Also validate tags

tags = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10", "tag11", "tag12", "tag13"]
tags_result = validate_tags(tags)
print(tags_result)
EOF

python test_validator.py
```

---

## NEXT STEPS

1. **Integrate validator** into both OpenAI and Gemini analysis services

1. **Log all validation results** for monitoring and improvement

1. **Create dashboard** to track validation metrics over time

1. **Compare model performance** to see which produces better descriptions

1. **Refine prompts** based on validation feedback patterns

1. **Archive validation reports** with each analysis for audit trail

---

## SUPPORT & DEBUGGING

### Enable Debug Logging

```python
import logging

# Enable debug logging for validator

logging.getLogger("ai_processing").setLevel(logging.DEBUG)

# Now all validation calls will be logged in detail

```

### Export Validation Report

```python
def export_validation_report(analysis, validation, filepath):
    """Save validation results as JSON for analysis."""
    import json

    report = {
        "timestamp": datetime.now().isoformat(),
        "analysis_fields": {
            "title_length": len(analysis.get("etsy_title", "")),
            "description_length": len(analysis.get("etsy_description", "")),
            "tag_count": len(analysis.get("etsy_tags", [])),
        },
        "validation_status": {
            "is_valid": validation.is_valid,
            "error_count": len(validation.errors),
            "warning_count": len(validation.warnings),
        },
        "errors": validation.errors,
        "warnings": validation.warnings,
    }

    with open(filepath, "w") as f:
        json.dump(report, f, indent=2)
```

---

**Remember:** Validation is not a barrier to quality—it's a guarantee of it. Use it every time.
