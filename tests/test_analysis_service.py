"""
Tests for Heritage-First AI analysis service schema compliance and cultural integrity.
Validates that Gemini/OpenAI analysis outputs meet the heritage protocol requirements,
include mandatory cultural acknowledgements, and slot correctly into manual workspace.
"""

from pathlib import Path
import pytest
from application.analysis.gemini.schema import (
    GeminiArtworkAnalysis,
    VisualAnalysis,
)


class TestVisualAnalysisSchema:
    """Validate VisualAnalysis object structure and required fields."""

    def test_visual_analysis_has_four_required_fields(self):
        """VisualAnalysis must have subject, dot_rhythm, palette, mood."""
        visual = VisualAnalysis(
            subject="Blue Wren",
            dot_rhythm="radiating sunbursts",
            palette="Ochre, Sunrise Gold, Eucalyptus Green",
            mood="tranquil",
        )
        assert visual.subject == "Blue Wren"
        assert visual.dot_rhythm == "radiating sunbursts"
        assert visual.palette == "Ochre, Sunrise Gold, Eucalyptus Green"
        assert visual.mood == "tranquil"

    def test_visual_analysis_rejects_empty_subject(self):
        """subject field must have min_length=1."""
        with pytest.raises(ValueError):
            VisualAnalysis(
                subject="",
                dot_rhythm="sunbursts",
                palette="Gold",
                mood="tranquil",
            )

    def test_visual_analysis_rejects_empty_dot_rhythm(self):
        """dot_rhythm field must have min_length=1."""
        with pytest.raises(ValueError):
            VisualAnalysis(
                subject="Blue Wren",
                dot_rhythm="",
                palette="Gold",
                mood="tranquil",
            )

    def test_visual_analysis_rejects_empty_palette(self):
        """palette field must have min_length=1."""
        with pytest.raises(ValueError):
            VisualAnalysis(
                subject="Blue Wren",
                dot_rhythm="sunbursts",
                palette="",
                mood="tranquil",
            )

    def test_visual_analysis_rejects_empty_mood(self):
        """mood field must have min_length=1."""
        with pytest.raises(ValueError):
            VisualAnalysis(
                subject="Blue Wren",
                dot_rhythm="sunbursts",
                palette="Gold",
                mood="",
            )


class TestGeminiArtworkAnalysisSchema:
    """Validate GeminiArtworkAnalysis schema compliance with heritage protocol."""

    def test_etsy_title_max_140_characters(self):
        """etsy_title must not exceed 140 characters."""
        title = "A" * 140
        analysis = GeminiArtworkAnalysis(
            etsy_title=title,
            etsy_description="Test description with heritage acknowledgement and 14,400px.",
            etsy_tags=["people of the reeds", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10", "tag11", "tag12", "tag13"],
            visual_analysis=VisualAnalysis(
                subject="Test",
                dot_rhythm="test",
                palette="test",
                mood="test",
            ),
            seo_filename_slug="test-slug",
            materials=["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10", "m11", "m12", "m13"],
            primary_colour="Blue",
            secondary_colour="Gold",
        )
        assert len(analysis.etsy_title) == 140

    def test_etsy_title_rejects_over_140_characters(self):
        """etsy_title must reject strings over 140 characters."""
        title = "A" * 141
        with pytest.raises(ValueError):
            GeminiArtworkAnalysis(
                etsy_title=title,
                etsy_description="Test description with heritage acknowledgement and 14,400px.",
                etsy_tags=["people of the reeds", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10", "tag11", "tag12", "tag13"],
                visual_analysis=VisualAnalysis(
                    subject="Test",
                    dot_rhythm="test",
                    palette="test",
                    mood="test",
                ),
                seo_filename_slug="test-slug",
                materials=["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10", "m11", "m12", "m13"],
                primary_colour="Blue",
                secondary_colour="Gold",
            )

    def test_etsy_tags_exactly_13_tags(self):
        """etsy_tags must contain exactly 13 tags."""
        tags = [f"tag{i}" for i in range(1, 14)]
        analysis = GeminiArtworkAnalysis(
            etsy_title="Test Title",
            etsy_description="Test description with heritage acknowledgement and 14,400px.",
            etsy_tags=tags,
            visual_analysis=VisualAnalysis(
                subject="Test",
                dot_rhythm="test",
                palette="test",
                mood="test",
            ),
            seo_filename_slug="test-slug",
            materials=["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10", "m11", "m12", "m13"],
            primary_colour="Blue",
            secondary_colour="Gold",
        )
        assert len(analysis.etsy_tags) == 13

    def test_etsy_tags_rejects_fewer_than_13(self):
        """etsy_tags must have at least 13 tags."""
        tags = ["tag1", "tag2", "tag3"]  # Only 3 tags
        with pytest.raises(ValueError):
            GeminiArtworkAnalysis(
                etsy_title="Test Title",
                etsy_description="Test description with heritage acknowledgement and 14,400px.",
                etsy_tags=tags,
                visual_analysis=VisualAnalysis(
                    subject="Test",
                    dot_rhythm="test",
                    palette="test",
                    mood="test",
                ),
                seo_filename_slug="test-slug",
                materials=["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10", "m11", "m12", "m13"],
                primary_colour="Blue",
                secondary_colour="Gold",
            )

    def test_etsy_tags_rejects_more_than_13(self):
        """etsy_tags must not exceed 13 tags."""
        tags = [f"tag{i}" for i in range(1, 15)]  # 14 tags
        with pytest.raises(ValueError):
            GeminiArtworkAnalysis(
                etsy_title="Test Title",
                etsy_description="Test description with heritage acknowledgement and 14,400px.",
                etsy_tags=tags,
                visual_analysis=VisualAnalysis(
                    subject="Test",
                    dot_rhythm="test",
                    palette="test",
                    mood="test",
                ),
                seo_filename_slug="test-slug",
                materials=["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10", "m11", "m12", "m13"],
                primary_colour="Blue",
                secondary_colour="Gold",
            )

    def test_materials_exactly_13_materials(self):
        """materials must contain exactly 13 items."""
        materials = [f"material{i}" for i in range(1, 14)]
        analysis = GeminiArtworkAnalysis(
            etsy_title="Test Title",
            etsy_description="Test description with heritage acknowledgement and 14,400px.",
            etsy_tags=["tag" + str(i) for i in range(1, 14)],
            visual_analysis=VisualAnalysis(
                subject="Test",
                dot_rhythm="test",
                palette="test",
                mood="test",
            ),
            seo_filename_slug="test-slug",
            materials=materials,
            primary_colour="Blue",
            secondary_colour="Gold",
        )
        assert len(analysis.materials) == 13

    def test_visual_analysis_object_present_and_valid(self):
        """visual_analysis must be a VisualAnalysis object with 4 fields."""
        analysis = GeminiArtworkAnalysis(
            etsy_title="Test Title",
            etsy_description="Test description with heritage acknowledgement and 14,400px.",
            etsy_tags=["tag" + str(i) for i in range(1, 14)],
            visual_analysis=VisualAnalysis(
                subject="Blue Wren",
                dot_rhythm="radiating sunbursts",
                palette="Ochre, Gold",
                mood="tranquil",
            ),
            seo_filename_slug="test-slug",
            materials=["m" + str(i) for i in range(1, 14)],
            primary_colour="Blue",
            secondary_colour="Gold",
        )
        assert isinstance(analysis.visual_analysis, VisualAnalysis)
        assert analysis.visual_analysis.subject == "Blue Wren"
        assert analysis.visual_analysis.dot_rhythm == "radiating sunbursts"
        assert analysis.visual_analysis.palette == "Ochre, Gold"
        assert analysis.visual_analysis.mood == "tranquil"


class TestHeritageProtocolCompliance:
    """Validate that output descriptions meet heritage-first protocol requirements."""

    def test_heritage_system_prompt_imported_correctly(self):
        """HERITAGE_FIRST_SYSTEM_PROMPT must be importable and contain key strings."""
        from application.analysis.prompts import (
            HERITAGE_FIRST_SYSTEM_PROMPT,
            SYSTEM_PROMPT,
        )

        assert "People of the Reeds" in HERITAGE_FIRST_SYSTEM_PROMPT
        assert "Boandik" in HERITAGE_FIRST_SYSTEM_PROMPT or "bindjali" in HERITAGE_FIRST_SYSTEM_PROMPT.lower()
        assert "14,400px" in HERITAGE_FIRST_SYSTEM_PROMPT
        assert "narrative" in HERITAGE_FIRST_SYSTEM_PROMPT.lower() or "lead" in HERITAGE_FIRST_SYSTEM_PROMPT.lower()
        assert "visual_analysis" in HERITAGE_FIRST_SYSTEM_PROMPT.lower()
        # Verify aliases work
        assert SYSTEM_PROMPT == HERITAGE_FIRST_SYSTEM_PROMPT

    def test_sample_analysis_includes_people_of_reeds_tag(self):
        """etsy_tags should include 'people of the reeds' tag in typical output."""
        tags = ["people of the reeds", "blue wren", "australian art", "aboriginal inspired", "dot painting",
                "indigenous art", "watercolor", "landscape", "nature", "gallery art", "limited edition", "print", "digital download"]
        analysis = GeminiArtworkAnalysis(
            etsy_title="Blue Wren: People of the Reeds",
            etsy_description="I acknowledge the Traditional Custodians... 14,400px museum-quality digital download.",
            etsy_tags=tags,
            visual_analysis=VisualAnalysis(
                subject="Blue Wren",
                dot_rhythm="radiating sunbursts",
                palette="Ochre, Sunrise Gold",
                mood="tranquil",
            ),
            seo_filename_slug="blue-wren-people-of-reeds",
            materials=["digital art", "acrylic", "watercolor", "ink", "pigment", "canvas", "paper", "textile", "resin", "wood", "clay", "stone", "glass"],
            primary_colour="Gold",
            secondary_colour="Gold",
        )
        assert "people of the reeds" in analysis.etsy_tags

    def test_sample_analysis_includes_14400px_in_description(self):
        """etsy_description should mention 14,400px museum-quality standard."""
        description = "I acknowledge the Traditional Custodians of the land... This 14,400px museum-quality digital download supports professional gallery prints up to 48 inches wide at 300 DPI. Limited to 25 copies."
        analysis = GeminiArtworkAnalysis(
            etsy_title="Blue Wren Print",
            etsy_description=description,
            etsy_tags=["people of the reeds", "blue", "wren", "print", "digital", "art", "aboriginal", "australian", "nature", "landscape", "gallery", "limited", "edition"],
            visual_analysis=VisualAnalysis(
                subject="Blue Wren",
                dot_rhythm="sunbursts",
                palette="Blue, Gold",
                mood="vibrant",
            ),
            seo_filename_slug="blue-wren",
            materials=["digital"] + ["x"] * 12,
            primary_colour="Blue",
            secondary_colour="Gold",
        )
        assert "14,400px" in analysis.etsy_description or "14400px" in analysis.etsy_description.replace(",", "")

    def test_sample_analysis_heritage_acknowledgement_in_description(self):
        """etsy_description should include heritage acknowledgement phrase."""
        description = """I acknowledge the Traditional Custodians of the land on which I live and create, 
the Bindjali people of the Naracoorte district and the Boandik people of the wider Limestone Coast.

This Blue Wren artwork celebrates songlines and cultural connection through radiating dot patterns.
14,400px museum-quality digital download for gallery prints up to 48 inches wide @ 300 DPI."""
        analysis = GeminiArtworkAnalysis(
            etsy_title="Blue Wren Songlines",
            etsy_description=description,
            etsy_tags=["people of the reeds", "songlines", "wren", "aboriginal", "indigenous", "boandik", "limestone", "coast", "dot", "painting", "australian", "art", "print"],
            visual_analysis=VisualAnalysis(
                subject="Blue Wren",
                dot_rhythm="radiating songlines",
                palette="Sky Blue, Earth Ochre",
                mood="spiritual",
            ),
            seo_filename_slug="blue-wren-songlines-by-robin-custance",
            materials=["digital art", "vector", "color", "design", "craft", "skill", "technique", "style", "composition", "balance", "harmony", "rhythm", "pattern"],
            primary_colour="Blue",
            secondary_colour="Brown",
        )
        assert "acknowledge" in analysis.etsy_description.lower()
        assert ("boandik" in analysis.etsy_description.lower() or "bindjali" in analysis.etsy_description.lower())


class TestManualWorkspaceIntegration:
    """Validate that analysis JSON slots correctly into manual workspace listing.json."""

    def test_analysis_schema_matches_listing_json_contract(self):
        """All analysis fields must map to listing.json metadata fields."""
        # This test verifies that the schema structure matches what manual workspace expects
        analysis = GeminiArtworkAnalysis(
            etsy_title="Blue Wren",
            etsy_description="A description with heritage and 14,400px.",
            etsy_tags=["tag" + str(i) for i in range(1, 14)],
            visual_analysis=VisualAnalysis(
                subject="Blue Wren",
                dot_rhythm="sunbursts",
                palette="Ochre",
                mood="tranquil",
            ),
            seo_filename_slug="blue-wren-by-robin-custance",
            materials=["m" + str(i) for i in range(1, 14)],
            primary_colour="Gold",
            secondary_colour="Gold",
        )
        
        # Verify backward compatibility via legacy properties
        # (service.py uses etsy_description/etsy_tags, but legacy code may expect description/tags)
        assert hasattr(analysis, 'etsy_title')
        assert hasattr(analysis, 'etsy_description')
        assert hasattr(analysis, 'etsy_tags')
        assert hasattr(analysis, 'visual_analysis')
        assert hasattr(analysis, 'seo_filename_slug')
        assert hasattr(analysis, 'materials')
        assert hasattr(analysis, 'primary_colour')
        assert hasattr(analysis, 'secondary_colour')

    def test_analysis_dict_serialization_for_listing_json(self):
        """Analysis should serialize to dict for JSON storage in listing.json."""
        analysis = GeminiArtworkAnalysis(
            etsy_title="Test",
            etsy_description="Heritage and 14,400px.",
            etsy_tags=["tag" + str(i) for i in range(1, 14)],
            visual_analysis=VisualAnalysis(
                subject="Test",
                dot_rhythm="test",
                palette="test",
                mood="test",
            ),
            seo_filename_slug="test",
            materials=["m" + str(i) for i in range(1, 14)],
            primary_colour="Blue",
            secondary_colour="Gold",
        )
        
        # Convert to dict (as would be done for JSON serialization)
        data = analysis.model_dump()
        assert data['etsy_title'] == "Test"
        assert data['etsy_description'] == "Heritage and 14,400px."
        assert len(data['etsy_tags']) == 13
        assert 'visual_analysis' in data
        assert data['visual_analysis']['subject'] == "Test"
        assert data['visual_analysis']['dot_rhythm'] == "test"
        assert data['visual_analysis']['palette'] == "test"
        assert data['visual_analysis']['mood'] == "test"


class TestPromptConfiguration:
    """Validate that prompts.py is correctly configured with heritage protocol."""

    def test_heritage_first_system_prompt_is_primary(self):
        """HERITAGE_FIRST_SYSTEM_PROMPT should be the primary system prompt."""
        from application.analysis.prompts import HERITAGE_FIRST_SYSTEM_PROMPT

        # Prompt should be long enough to contain full instructions
        assert len(HERITAGE_FIRST_SYSTEM_PROMPT) > 500

        # Must contain core heritage elements
        assert "People of the Reeds" in HERITAGE_FIRST_SYSTEM_PROMPT
        assert "Robin Custance" in HERITAGE_FIRST_SYSTEM_PROMPT
        assert "etsy_title" in HERITAGE_FIRST_SYSTEM_PROMPT
        assert "etsy_description" in HERITAGE_FIRST_SYSTEM_PROMPT
        assert "etsy_tags" in HERITAGE_FIRST_SYSTEM_PROMPT
        assert "visual_analysis" in HERITAGE_FIRST_SYSTEM_PROMPT

    def test_aliases_resolve_correctly(self):
        """SYSTEM_PROMPT and MASTER_CURATOR_PROMPT should alias HERITAGE_FIRST_SYSTEM_PROMPT."""
        from application.analysis.prompts import (
            HERITAGE_FIRST_SYSTEM_PROMPT,
            SYSTEM_PROMPT,
            MASTER_CURATOR_PROMPT,
        )

        assert SYSTEM_PROMPT is HERITAGE_FIRST_SYSTEM_PROMPT
        assert MASTER_CURATOR_PROMPT is HERITAGE_FIRST_SYSTEM_PROMPT

    def test_prompt_includes_heritage_acknowledgement_instruction(self):
        """Prompt must instruct the model to include heritage acknowledgement."""
        from application.analysis.prompts import HERITAGE_FIRST_SYSTEM_PROMPT

        # Check for mandatory acknowledgement instruction
        prompt_lower = HERITAGE_FIRST_SYSTEM_PROMPT.lower()
        assert "acknowledge" in prompt_lower or "acknowledgement" in prompt_lower
        assert "boandik" in prompt_lower or "bindjali" in prompt_lower
