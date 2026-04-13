"""
Etsy Description Format Validator

Validates that generated artwork descriptions comply with Etsy's strict requirements:
- Plain text only (no HTML/markdown)
- Minimum 850 characters for SEO
- Exactly 13 tags (max 20 chars each)
- Proper structure and formatting
- Heritage statement with correct em-dash formatting
"""

from __future__ import annotations

import re
import logging
from typing import Any

logger = logging.getLogger("ai_processing")


class EtsyValidationResult:
    """Result of Etsy description validation."""
    
    def __init__(self, is_valid: bool, errors: list[str] | None = None, warnings: list[str] | None = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []
    
    def add_error(self, msg: str) -> None:
        """Add validation error."""
        if msg not in self.errors:
            self.errors.append(msg)
        self.is_valid = False
    
    def add_warning(self, msg: str) -> None:
        """Add validation warning."""
        if msg not in self.warnings:
            self.warnings.append(msg)
    
    def __str__(self) -> str:
        result = []
        if self.is_valid:
            result.append("✅ VALID - Description passes all Etsy requirements")
        else:
            result.append("❌ INVALID - Description has errors:")
            for error in self.errors:
                result.append(f"  • {error}")
        
        if self.warnings:
            result.append("\n⚠️  WARNINGS (not critical but recommended to fix):")
            for warning in self.warnings:
                result.append(f"  • {warning}")
        
        return "\n".join(result)


def validate_description(description: str | Any) -> EtsyValidationResult:
    """
    Validate Etsy description for compliance.
    
    Checks:
    1. Is plain text (no HTML tags, no markdown syntax)
    2. Minimum 850 characters
    3. Starts with emoji header and location
    4. Includes heritage statement with em-dash
    5. Has proper section structure
    6. Uses Unicode em-dashes, not hyphens
    7. Contains no unsupported HTML/markdown
    
    Args:
        description: The Etsy description text to validate
    
    Returns:
        EtsyValidationResult with validity status and error/warning messages
    """
    result = EtsyValidationResult(is_valid=True)
    
    # Convert to string if needed
    if not isinstance(description, str):
        result.add_error(f"Description must be a string, got {type(description).__name__}")
        return result
    
    desc = description.strip()
    
    # Check 1: Minimum length (850 characters for Google SEO)
    if len(desc) < 850:
        result.add_error(f"Description too short: {len(desc)} chars (minimum 850 required for SEO)")
    elif len(desc) < 950:
        result.add_warning(f"Description could be longer: {len(desc)} chars (aim for 950+ for better SEO)")
    
    # Check 2: No HTML tags
    html_pattern = r'<[^>]+>'
    if re.search(html_pattern, desc):
        result.add_error("Description contains HTML tags - Etsy will strip these. Use plain text only.")
    
    # Check 3: No markdown syntax
    if re.search(r'^#+\s', desc, re.MULTILINE):
        result.add_error("Description contains markdown headers (###) - use emoji headers instead")
    if re.search(r'\*\*[^*]+\*\*', desc):
        result.add_error("Description contains markdown bold (**text**) - Etsy doesn't support this")
    if re.search(r'~~[^~]+~~', desc):
        result.add_error("Description contains markdown strikethrough (~~text~~)")
    if re.search(r'`[^`]+`', desc):
        result.add_error("Description contains code blocks or inline code (backticks)")
    
    # Check 4: Starts with emoji header
    if not re.match(r'^[🌅🌿🙌💎📐🛒❤️]', desc):
        result.add_warning("Description should start with an emoji header (🌅 recommended)")
    
    # Check 5: Heritage statement with proper em-dash
    if "Boandik" in desc or "Bunganditj" in desc:
        # Check for proper em-dash formatting
        if "Boandik (Bunganditj)—the People of the Reeds" in desc:
            # Correct format found
            pass
        elif "Boandik (Bunganditj) - the People of the Reeds" in desc:
            result.add_error(
                "Heritage statement uses hyphen (-) instead of em-dash (—). "
                "Use Unicode em-dash: 'Boandik (Bunganditj)—the People of the Reeds'"
            )
        elif "Boandik (Bunganditj)--the People of the Reeds" in desc:
            result.add_error(
                "Heritage statement uses double-hyphen (--) instead of em-dash (—). "
                "Use Unicode em-dash: 'Boandik (Bunganditj)—the People of the Reeds'"
            )
        elif "Boandik" in desc and "People of the Reeds" not in desc:
            result.add_warning(
                "Heritage statement mentions Boandik but doesn't include 'People of the Reeds' translation"
            )
    
    # Check 6: Section structure
    required_sections = {
        "🌅": "High-Vibe Hook",
        "🌿": "The Soul of the Piece",
        "🙌": "Connection to Country",
        "💎": "Technical Excellence & Value",
        "📐": "Printing & Size Guide",
    }
    
    found_sections = []
    for emoji, section_name in required_sections.items():
        if emoji in desc:
            found_sections.append(section_name)
    
    if len(found_sections) < 4:
        result.add_warning(
            f"Description has {len(found_sections)} required emoji sections (aim for 5+). "
            f"Found: {', '.join(found_sections) or 'none'}"
        )
    
    # Check 7: Technical specifications mentioned
    if "14,400px" not in desc and "14400px" not in desc and "7,200px" not in desc and "7200px" not in desc:
        result.add_warning("Description should mention print resolution (7,200px or 14,400px) for credibility")
    if "300 DPI" not in desc and "300 dpi" not in desc.lower():
        result.add_warning("Description should mention 300 DPI for clarity")
    if "48" not in desc and "24" not in desc:
        result.add_warning("Description should mention print size (24-inch or 48-inch)")
    
    # Check 8: No quotation marks (should use single quotes)
    if '"' in desc:
        # Allow quotes in contractions and possessives, but warn about straight quotes
        if re.search(r'[^\']\s"[^"]+"\s', desc):
            result.add_warning(
                "Description contains straight double quotes (\") - use single quotes (') or remove quotation marks"
            )
    
    # Check 9: Unicode em-dash usage (should have at least one for sophistication)
    if "—" not in desc:
        if "-" in desc or "--" in desc:
            result.add_warning(
                "Description could use Unicode em-dash (—) for sophisticated typography. "
                "Especially important in heritage statement."
            )
    
    # Check 10: Line breaks for mobile readability
    line_breaks = desc.count('\n')
    if line_breaks < 5:
        result.add_warning(
            f"Description has minimal line breaks ({line_breaks}). "
            "Add more blank lines between sections for mobile readability."
        )
    
    # Check 11: Emoji usage for visual hierarchy
    emoji_count = len(re.findall(r'[🌅🌿🙌💎📐🛒❤️✨🖼️🌭🇦🇺🍃]', desc))
    if emoji_count < 5:
        result.add_warning(
            f"Description has {emoji_count} emojis (aim for 5+). "
            "Emojis help with visual hierarchy on mobile and Etsy's interface."
        )
    
    # Check 12: Forbidden language patterns
    forbidden_patterns = [
        (r'I\s+painted', "Don't use 'painted' - use 'rendered' or 'generated'"),
        (r'brushstrokes?', "Don't use 'brushstrokes' - use 'digital strokes' or 'light-filled marks'"),
        (r'\bon\s+canvas\b', "Don't mention 'on canvas' - this is digital art"),
        (r'\boils?\b|\bacrylic', "Don't mention 'oils' or 'acrylics' - this is digital art"),
        (r'painterly|\bpainterly\b', "Don't use 'painterly' - describe the style specifically"),
    ]
    
    for pattern, message in forbidden_patterns:
        if re.search(pattern, desc, re.IGNORECASE):
            result.add_error(f"Forbidden language: {message}")
    
    logger.info(f"[ETSY_VALIDATOR] Description validation: {len(desc)} chars, "
                f"{'VALID' if result.is_valid else 'INVALID'}, "
                f"{len(result.errors)} errors, {len(result.warnings)} warnings")
    
    return result


def validate_tags(tags: list[str] | Any) -> EtsyValidationResult:
    """
    Validate Etsy tags.
    
    Checks:
    1. Exactly 13 tags
    2. Each tag max 20 characters
    3. Buyer-intent focused (not generic art terms)
    4. No special characters
    
    Args:
        tags: List of tag strings
    
    Returns:
        EtsyValidationResult with validity status
    """
    result = EtsyValidationResult(is_valid=True)
    
    if not isinstance(tags, list):
        result.add_error(f"Tags must be a list, got {type(tags).__name__}")
        return result
    
    # Check count
    if len(tags) != 13:
        result.add_error(f"Must have exactly 13 tags, got {len(tags)}")
    
    # Check each tag
    for i, tag in enumerate(tags, 1):
        if not isinstance(tag, str):
            result.add_error(f"Tag {i} is not a string: {type(tag).__name__}")
            continue
        
        tag = tag.strip()
        
        # Check length
        if len(tag) > 20:
            result.add_error(f"Tag {i} too long: '{tag}' ({len(tag)}/20 chars)")
        elif len(tag) < 2:
            result.add_error(f"Tag {i} too short: '{tag}'")
        
        # Check for special characters (Etsy doesn't allow most)
        if re.search(r'[^a-zA-Z0-9\s\-&]', tag):
            result.add_warning(f"Tag {i} contains special characters: '{tag}'")
        
        # Check if it's generic/weak
        weak_tags = ['art', 'artwork', 'digital', 'print', 'decor', 'design']
        if tag.lower() in weak_tags:
            result.add_warning(f"Tag {i} is too generic: '{tag}' - use more specific buyer intent terms")
    
    return result


def validate_title(title: str | Any) -> EtsyValidationResult:
    """
    Validate Etsy title.
    
    Checks:
    1. Max 140 characters
    2. Contains key elements (location, "48 Inch" or "24 Inch", artist name)
    3. Uses pipe separators
    4. Proper capitalization
    
    Args:
        title: Etsy title string
    
    Returns:
        EtsyValidationResult with validity status
    """
    result = EtsyValidationResult(is_valid=True)
    
    if not isinstance(title, str):
        result.add_error(f"Title must be a string, got {type(title).__name__}")
        return result
    
    title = title.strip()
    
    # Check length
    if len(title) > 140:
        result.add_error(f"Title too long: {len(title)}/140 characters")
    elif len(title) < 30:
        result.add_warning(f"Title very short: {len(title)} chars (aim for 50-140)")
    
    # Check for key elements
    if "48" not in title and "48-inch" not in title.lower() and "24" not in title and "24-inch" not in title.lower():
        result.add_warning("Title should mention print size ('48' or '24' for inches)")
    
    if "Digital" not in title and "Download" not in title:
        result.add_warning("Title should indicate it's a Digital Download")
    
    # Check for pipe separators
    if "|" in title:
        pass  # Good format
    else:
        result.add_warning("Title should use pipe separators (|) for better SEO formatting")
    
    return result


def validate_complete_analysis(analysis: dict[str, Any]) -> EtsyValidationResult:
    """
    Validate complete artwork analysis output.
    
    Args:
        analysis: Complete analysis dictionary with all fields
    
    Returns:
        EtsyValidationResult combining all validation checks
    """
    result = EtsyValidationResult(is_valid=True)
    
    # Validate title
    title_result = validate_title(analysis.get("etsy_title"))
    if not title_result.is_valid:
        for error in title_result.errors:
            result.add_error(f"Title: {error}")
    for warning in title_result.warnings:
        result.add_warning(f"Title: {warning}")
    
    # Validate description
    desc_result = validate_description(analysis.get("etsy_description") or analysis.get("description"))
    if not desc_result.is_valid:
        for error in desc_result.errors:
            result.add_error(f"Description: {error}")
    for warning in desc_result.warnings:
        result.add_warning(f"Description: {warning}")
    
    # Validate tags
    tags_result = validate_tags(analysis.get("etsy_tags") or analysis.get("tags"))
    if not tags_result.is_valid:
        for error in tags_result.errors:
            result.add_error(f"Tags: {error}")
    for warning in tags_result.warnings:
        result.add_warning(f"Tags: {warning}")
    
    return result
