from __future__ import annotations

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class VisualAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject: str = Field(min_length=1)
    dot_rhythm: str = Field(min_length=1)
    palette: str = Field(min_length=1)
    mood: str = Field(min_length=1)


class OpenAIArtworkAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    etsy_title: str = Field(min_length=1)
    seo_filename_slug: str = Field(min_length=1)
    etsy_description: str = Field(min_length=1, validation_alias=AliasChoices("etsy_description", "description"))
    etsy_tags: list[str] = Field(min_length=13, max_length=13, validation_alias=AliasChoices("etsy_tags", "tags"))
    visual_analysis: VisualAnalysis
    materials: list[str] = Field(min_length=13, max_length=13)
    primary_colour: str = Field(min_length=1)
    secondary_colour: str = Field(min_length=1)

    @property
    def description(self) -> str:
        return self.etsy_description

    @property
    def tags(self) -> list[str]:
        return self.etsy_tags
