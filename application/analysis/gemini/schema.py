from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing import Any, Annotated, Literal


class VisualAnalysis(BaseModel):
    """Visual characteristics extracted from artwork image."""
    model_config = ConfigDict(extra="forbid")

    subject: str = Field(min_length=1, description="Primary subject of the artwork")
    dot_rhythm: str = Field(min_length=1, description="Description of dot pattern and rhythm")
    palette: str = Field(min_length=1, description="Evocative colour palette names")
    mood: str = Field(min_length=1, description="Emotional tone of the artwork")


class GeminiArtworkAnalysis(BaseModel):
    """Heritage-First Etsy listing schema with visual analysis and manual workspace alignment."""
    model_config = ConfigDict(extra="forbid")

    etsy_title: str = Field(min_length=1, max_length=140, description="Etsy title, max 140 chars")
    etsy_description: str = Field(min_length=1, description="Full Etsy description with heritage acknowledgement")
    etsy_tags: list[Annotated[str, StringConstraints(max_length=20)]] = Field(
        min_length=13,
        max_length=13,
        description="Exactly 13 Etsy tags (each max 20 chars)",
    )
    seo_filename_slug: str = Field(min_length=1, max_length=61, description="SEO filename slug, lowercase hyphens only")
    visual_analysis: VisualAnalysis = Field(description="Visual characteristics from image analysis")
    materials: list[str] = Field(min_length=13, max_length=13, description="Exactly 13 digital craft materials")
    primary_colour: Literal[
        "Black",
        "Blue",
        "Brown",
        "Gold",
        "Green",
        "Grey",
        "Indigo",
        "Orange",
        "Pink",
        "Purple",
        "Red",
        "Silver",
        "Teal",
        "White",
        "Yellow",
    ] = Field(min_length=1, description="Primary colour name")
    secondary_colour: Literal[
        "Black",
        "Blue",
        "Brown",
        "Gold",
        "Green",
        "Grey",
        "Indigo",
        "Orange",
        "Pink",
        "Purple",
        "Red",
        "Silver",
        "Teal",
        "White",
        "Yellow",
    ] = Field(min_length=1, description="Secondary colour name")

    mockup_category: str | None = Field(default=None, description="Suggested mockup category derived from mood/subject")

    # Legacy aliases for backward compatibility
    @property
    def description(self) -> str:
        """Alias for etsy_description (backward compat)."""
        return self.etsy_description

    @property
    def tags(self) -> list[str]:
        """Alias for etsy_tags (backward compat)."""
        return self.etsy_tags
