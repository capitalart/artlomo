"""Stage 2A Validation Tests for MockupPromptService and GeminiImageService.

Validates:
1. MockupPromptService generates valid prompts for all categories
2. Prompts never contain aspect ratio in text (only via API config)
3. Prompts always include cyan rectangle placeholder
4. GeminiImageService can be instantiated and validated
5. Error handling for invalid inputs
"""

from __future__ import annotations

import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest

import application.mockups.services.gemini_service as gemini_service_module
from application.mockups.config import MockupBaseGenerationCatalog
from application.mockups.services.mockup_prompt_service import MockupPromptService
from application.mockups.services.gemini_service import (
    GeminiImageService,
    GeminiAuthenticationError,
    GeminiGenerationError,
    GeminiRateLimitError,
)


class _FakeGenerateImagesConfig:
    """Lightweight config object used to inspect GenAI request parameters."""

    aspect_ratio: str
    image_size: str
    number_of_images: int
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)


class _FakeEditImageConfig(_FakeGenerateImagesConfig):
    """Lightweight config object used to inspect edit_image request parameters."""

    edit_mode: str
    output_mime_type: str


class _FakeImage:
    """Minimal stand-in for google.genai.types.Image."""

    def __init__(self, *, location: str | None = None, image_bytes: bytes | None = None):
        self.location = location
        self.image_bytes = image_bytes

    @classmethod
    def from_file(cls, *, location: str, mime_type: str | None = None):
        return cls(location=location)


class _FakeControlReferenceConfig:
    """Minimal stand-in for google.genai.types.ControlReferenceConfig."""

    def __init__(self, *, control_type, enable_control_image_computation):
        self.control_type = control_type
        self.enable_control_image_computation = enable_control_image_computation


class _FakeControlReferenceImage:
    """Minimal stand-in for google.genai.types.ControlReferenceImage."""

    def __init__(self, *, reference_id, reference_image, config):
        self.reference_id = reference_id
        self.reference_image = reference_image
        self.config = config


class _FakeGeneratedImage:
    """Fake generated image payload with a bytes-compatible data attribute."""

    def __init__(self, data: bytes):
        self.data = data
        self.image = SimpleNamespace(image_bytes=data)


class _FakeGenerateImagesResponse:
    """Fake Gemini response containing a single generated image."""

    def __init__(self, data: bytes):
        self.generated_images = [_FakeGeneratedImage(data)]


class _FakeModels:
    """Capture calls made to the mocked Gemini models client."""

    def __init__(self, response_bytes: bytes):
        self.response_bytes = response_bytes
        self.generate_images_calls: list[dict[str, object]] = []
        self.edit_image_calls: list[dict[str, object]] = []
        self.edit_image_error: Exception | None = None

    def generate_images(self, *, model, prompt, config):
        self.generate_images_calls.append(
            {
                "model": model,
                "prompt": prompt,
                "config": config,
            }
        )
        return _FakeGenerateImagesResponse(self.response_bytes)

    def edit_image(self, *, model, prompt, reference_images, config):
        self.edit_image_calls.append(
            {
                "model": model,
                "prompt": prompt,
                "reference_images": reference_images,
                "config": config,
            }
        )
        if self.edit_image_error is not None:
            raise self.edit_image_error
        return _FakeGenerateImagesResponse(self.response_bytes)

    def list(self):
        return []


class _FakeClient:
    """Fake google.genai.Client replacement for deterministic tests."""

    def __init__(self, response_bytes: bytes = b"fake-png-bytes", **kwargs):
        self.api_key = kwargs.get("api_key")
        self.vertexai = kwargs.get("vertexai", False)
        self.project = kwargs.get("project")
        self.location = kwargs.get("location")
        self.models = _FakeModels(response_bytes=response_bytes)


def _install_fake_genai(monkeypatch, response_bytes: bytes = b"fake-png-bytes") -> _FakeClient:
    """Patch the Gemini service module to use fake genai/types implementations."""

    fake_client = _FakeClient(response_bytes=response_bytes)

    fake_types = SimpleNamespace(
        GenerateImagesConfig=_FakeGenerateImagesConfig,
        EditImageConfig=_FakeEditImageConfig,
        Image=_FakeImage,
        ControlReferenceConfig=_FakeControlReferenceConfig,
        ControlReferenceImage=_FakeControlReferenceImage,
        EditMode=SimpleNamespace(EDIT_MODE_CONTROLLED_EDITING="EDIT_MODE_CONTROLLED_EDITING"),
        ControlReferenceType=SimpleNamespace(CONTROL_TYPE_SCRIBBLE="CONTROL_TYPE_SCRIBBLE"),
    )
    fake_genai = SimpleNamespace(Client=lambda **kwargs: _configure_fake_client(fake_client, **kwargs))

    monkeypatch.setattr(gemini_service_module, "genai", fake_genai)
    monkeypatch.setattr(gemini_service_module, "types", fake_types)

    return fake_client


def _configure_fake_client(fake_client: _FakeClient, **kwargs) -> _FakeClient:
    """Mutate the reusable fake client with the requested constructor args."""
    fake_client.api_key = kwargs.get("api_key")
    fake_client.vertexai = kwargs.get("vertexai", False)
    fake_client.project = kwargs.get("project")
    fake_client.location = kwargs.get("location")
    return fake_client


@pytest.fixture(autouse=True)
def _isolate_control_state(monkeypatch, tmp_path):
    """Prevent tests from reading the live operator control-state file."""
    control_state_path = tmp_path / "mockup_generator_control.json"
    control_state_path.write_text('{"placeholder_mode": "cyan"}', encoding="utf-8")
    monkeypatch.setattr(gemini_service_module, "CONTROL_STATE_PATH", control_state_path)


class TestMockupPromptService:
    """Test suite for MockupPromptService prompt generation."""

    def test_prompt_generated_for_all_categories(self):
        """Verify MockupPromptService generates valid prompts for all 22 categories."""
        for category in MockupBaseGenerationCatalog.CATEGORIES:
            prompt = MockupPromptService.generate_prompt(
                category=category,
                variation_index=1,
            )
            assert isinstance(prompt, str)
            assert len(prompt) > 100, f"Prompt too short for category '{category}'"
            assert "cyan" in prompt.lower(), f"Cyan placeholder missing in '{category}' prompt"

    def test_prompt_includes_cyan_placeholder_description(self):
        """Verify that all prompts include standard cyan placeholder language."""
        categories_to_test = ["living-room", "cafe", "bedroom-adults", "kitchen"]
        for category in categories_to_test:
            prompt = MockupPromptService.generate_prompt(
                category=category,
                variation_index=5,
            )
            # Check for key marker phrases
            assert "solid" in prompt.lower()
            assert "perfectly flat" in prompt.lower()
            assert "untextured matte cyan" in prompt.lower()
            assert "rectangle" in prompt.lower()

    def test_prompt_does_not_contain_aspect_ratio(self):
        """Verify aspect ratio text is NOT included in prompts.

        This is a critical constraint: aspect ratio is passed via API config,
        not in prompt text. This test ensures prompt consistency.
        """
        aspect_ratios = ["1x1", "16x9", "9x16", "3x2", "2x3"]
        for aspect_ratio in aspect_ratios:
            # Replace with colon format that might appear in text
            aspect_colon = aspect_ratio.replace("x", ":")
            for category in ["living-room", "cafe"]:
                prompt = MockupPromptService.generate_prompt(
                    category=category,
                    variation_index=1,
                )
                # Neither format should appear in the prompt
                assert aspect_ratio not in prompt, (
                    f"Aspect ratio '{aspect_ratio}' found in prompt for category '{category}'"
                )
                assert aspect_colon not in prompt, (
                    f"Aspect ratio '{aspect_colon}' found in prompt for category '{category}'"
                )

    def test_prompt_deterministic_seeding(self):
        """Verify same (category, variation) produces identical prompts.

        This ensures reproducible batch generation.
        """
        category = "living-room"
        variation_index = 7

        prompt1 = MockupPromptService.generate_prompt(
            category=category,
            variation_index=variation_index,
        )
        prompt2 = MockupPromptService.generate_prompt(
            category=category,
            variation_index=variation_index,
        )

        assert prompt1 == prompt2, (
            "Same (category, variation_index) should produce identical prompts"
        )

    def test_prompt_different_variations_produce_different_prompts(self):
        """Verify different variation indices produce different prompts."""
        category = "cafe"
        prompts = [
            MockupPromptService.generate_prompt(category=category, variation_index=i)
            for i in range(1, 6)
        ]

        # At least some should differ (due to random selection from prop/lighting/texture)
        unique_prompts = set(prompts)
        assert len(unique_prompts) > 1, (
            "Multiple variations should produce different prompts due to randomization"
        )

    def test_prompt_invalid_category_raises_error(self):
        """Verify ValueError is raised for unknown category."""
        with pytest.raises(ValueError, match="Unknown category"):
            MockupPromptService.generate_prompt(
                category="invalid-category",
                variation_index=1,
            )

    def test_prompt_invalid_variation_index_raises_error(self):
        """Verify ValueError is raised for out-of-bounds variation_index."""
        with pytest.raises(ValueError, match="variation_index must be 1-20"):
            MockupPromptService.generate_prompt(
                category="living-room",
                variation_index=0,
            )

        with pytest.raises(ValueError, match="variation_index must be 1-20"):
            MockupPromptService.generate_prompt(
                category="living-room",
                variation_index=21,
            )

    def test_prompt_all_variation_indices_accepted(self):
        """Verify all variation indices 1-20 are accepted."""
        category = "bedroom-kids"
        for variation_index in range(1, 21):
            prompt = MockupPromptService.generate_prompt(
                category=category,
                variation_index=variation_index,
            )
            assert isinstance(prompt, str)
            assert len(prompt) > 100


class TestGeminiImageServiceInitialization:
    """Test suite for GeminiImageService initialization and validation."""

    def test_gemini_service_raises_error_without_api_key(self):
        """Verify GeminiImageService raises error when API key is missing."""
        # Temporarily remove API key from environment
        original_key = os.environ.pop("GEMINI_API_KEY", None)
        original_google_key = os.environ.pop("GOOGLE_API_KEY", None)
        original_vertex_flag = os.environ.pop("GOOGLE_GENAI_USE_VERTEXAI", None)
        try:
            with pytest.raises(
                GeminiAuthenticationError, match="Gemini credentials not configured"
            ):
                GeminiImageService(api_key=None)
        finally:
            # Restore API key if it existed
            if original_key:
                os.environ["GEMINI_API_KEY"] = original_key
            if original_google_key:
                os.environ["GOOGLE_API_KEY"] = original_google_key
            if original_vertex_flag:
                os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = original_vertex_flag

    def test_gemini_service_accepts_explicit_api_key(self):
        """Verify GeminiImageService can be initialized with explicit API key."""
        # Use a dummy key for this test (we're just testing initialization, not API calls)
        service = GeminiImageService(api_key="test-key-12345")
        assert service.api_key == "test-key-12345"

    def test_gemini_service_reads_api_key_from_environment(self):
        """Verify GeminiImageService reads API key from GEMINI_API_KEY env var."""
        original_key = os.environ.get("GEMINI_API_KEY")
        test_key = "env-test-key-67890"
        os.environ["GEMINI_API_KEY"] = test_key

        try:
            service = GeminiImageService()
            assert service.api_key == test_key
        finally:
            # Restore original key
            if original_key:
                os.environ["GEMINI_API_KEY"] = original_key
            else:
                os.environ.pop("GEMINI_API_KEY", None)

    def test_gemini_service_reads_google_api_key_from_environment(self):
        """Verify GeminiImageService reads API key from GOOGLE_API_KEY env var."""
        original_gemini_key = os.environ.pop("GEMINI_API_KEY", None)
        original_google_key = os.environ.get("GOOGLE_API_KEY")
        test_key = "google-api-key-123"
        os.environ["GOOGLE_API_KEY"] = test_key

        try:
            service = GeminiImageService()
            assert service.api_key == test_key
        finally:
            if original_gemini_key:
                os.environ["GEMINI_API_KEY"] = original_gemini_key
            if original_google_key:
                os.environ["GOOGLE_API_KEY"] = original_google_key
            else:
                os.environ.pop("GOOGLE_API_KEY", None)

    def test_gemini_service_invalid_aspect_ratio_raises_error(self):
        """Verify ValueError is raised for invalid aspect ratio."""
        service = GeminiImageService(api_key="test-key")
        with pytest.raises(ValueError, match="Invalid aspect_ratio"):
            service.generate_image(
                prompt="test prompt",
                aspect_ratio="invalid-ratio",
                category="living-room",
                variation_index=1,
            )

    def test_gemini_service_invalid_category_raises_error(self):
        """Verify ValueError is raised for invalid category."""
        service = GeminiImageService(api_key="test-key")
        with pytest.raises(ValueError, match="Invalid category"):
            service.generate_image(
                prompt="test prompt",
                aspect_ratio="16x9",
                category="invalid-category",
                variation_index=1,
            )

    def test_gemini_service_invalid_variation_index_raises_error(self):
        """Verify ValueError is raised for out-of-bounds variation_index."""
        service = GeminiImageService(api_key="test-key")

        with pytest.raises(ValueError, match="variation_index must be 1-20"):
            service.generate_image(
                prompt="test prompt",
                aspect_ratio="16x9",
                category="living-room",
                variation_index=0,
            )

        with pytest.raises(ValueError, match="variation_index must be 1-20"):
            service.generate_image(
                prompt="test prompt",
                aspect_ratio="16x9",
                category="living-room",
                variation_index=21,
            )


class TestStage2AIntegrationContract:
    """Integration tests for Stage 2A components working together."""

    def test_prompt_service_output_compatible_with_gemini_service(self, monkeypatch, tmp_path):
        """Verify Gemini receives aspect ratio and native 2K size via config."""
        category = "cafe"
        variation_index = 3
        aspect_ratio = "16x9"
        fake_bytes = b"fake-png-2k-output"

        fake_client = _install_fake_genai(monkeypatch, response_bytes=fake_bytes)
        monkeypatch.setattr(GeminiImageService, "MOCKUP_BASE_STORAGE_DIR", tmp_path)
        monkeypatch.setattr(
            GeminiImageService,
            "REFERENCE_GUIDE_STORAGE_DIR",
            tmp_path / "reference-guides",
        )
        monkeypatch.setattr(
            GeminiImageService,
            "LEGACY_REFERENCE_GUIDE_STORAGE_DIR",
            tmp_path / "legacy-reference-guides",
        )
        monkeypatch.setenv("MOCKUP_REQUIRE_REFERENCE_GUIDE", "false")
        # Disable the global aspect-ratio override so the aspect ratio passed to
        # generate_image() is the one used in the Gemini API call.
        monkeypatch.setattr(GeminiImageService, "FORCE_GENERATION_ASPECT_RATIO", "")

        # Generate a prompt
        prompt = MockupPromptService.generate_prompt(
            category=category,
            variation_index=variation_index,
        )

        # Verify the prompt is a string and non-empty
        assert isinstance(prompt, str)
        assert len(prompt) > 50
        assert aspect_ratio not in prompt
        assert aspect_ratio.replace("x", ":") not in prompt

        service = GeminiImageService(api_key="test-key")
        file_path = service.generate_image(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            category=category,
            variation_index=variation_index,
        )

        assert Path(file_path).exists()
        assert Path(file_path).read_bytes() == fake_bytes
        assert len(fake_client.models.generate_images_calls) == 1

        call = fake_client.models.generate_images_calls[0]
        assert call["model"] == service.IMAGE_GENERATION_MODEL
        # Service wraps the user prompt with HARD_EDGE_PROMPT_PREFIX + system instructions;
        # verify the original prompt content is preserved in the full call prompt.
        assert prompt in str(call["prompt"])

        config = call["config"]
        # Service passes config as a plain dict (not types.GenerateImagesConfig).
        assert isinstance(config, (dict, _FakeGenerateImagesConfig))
        aspect_ratio_val = config["aspect_ratio"] if isinstance(config, dict) else config.aspect_ratio
        image_size_val = config["image_size"] if isinstance(config, dict) else config.image_size
        assert aspect_ratio_val == "16:9"
        assert image_size_val == service.NATIVE_IMAGE_SIZE

    def test_stage2a_uses_generation_aspect_override_for_canvas(self, monkeypatch, tmp_path):
        """Verify canvas aspect can be forced independently from placeholder guide aspect."""
        category = "display"
        variation_index = 1
        placeholder_aspect_ratio = "2x3"
        canvas_aspect_ratio = "1x1"
        fake_bytes = b"fake-canvas-override"

        fake_client = _install_fake_genai(monkeypatch, response_bytes=fake_bytes)
        monkeypatch.setattr(GeminiImageService, "MOCKUP_BASE_STORAGE_DIR", tmp_path)
        monkeypatch.setattr(
            GeminiImageService,
            "REFERENCE_GUIDE_STORAGE_DIR",
            tmp_path / "reference-guides",
        )
        monkeypatch.setattr(
            GeminiImageService,
            "LEGACY_REFERENCE_GUIDE_STORAGE_DIR",
            tmp_path / "legacy-reference-guides",
        )
        monkeypatch.setenv("MOCKUP_REQUIRE_REFERENCE_GUIDE", "false")

        prompt = MockupPromptService.generate_prompt(
            category=category,
            variation_index=variation_index,
        )

        service = GeminiImageService(api_key="test-key")
        file_path = service.generate_image(
            prompt=prompt,
            aspect_ratio=placeholder_aspect_ratio,
            category=category,
            variation_index=variation_index,
            generation_aspect_ratio=canvas_aspect_ratio,
        )

        assert Path(file_path).exists()
        assert Path(file_path).read_bytes() == fake_bytes
        assert len(fake_client.models.generate_images_calls) == 1

        config = fake_client.models.generate_images_calls[0]["config"]
        assert isinstance(config, (dict, _FakeGenerateImagesConfig))
        aspect_ratio_val = config["aspect_ratio"] if isinstance(config, dict) else config.aspect_ratio
        assert aspect_ratio_val == "1:1"

    def test_stage2a_maps_unsupported_aspect_ratio_to_nearest_supported(self, monkeypatch, tmp_path):
        """Verify unsupported 2x3 requests are mapped to a supported Gemini ratio (3:4)."""
        category = "cafe"
        variation_index = 3
        aspect_ratio = "2x3"
        fake_bytes = b"fake-mapped-aspect-output"

        fake_client = _install_fake_genai(monkeypatch, response_bytes=fake_bytes)
        monkeypatch.setattr(GeminiImageService, "MOCKUP_BASE_STORAGE_DIR", tmp_path)
        monkeypatch.setattr(
            GeminiImageService,
            "REFERENCE_GUIDE_STORAGE_DIR",
            tmp_path / "reference-guides",
        )
        monkeypatch.setattr(
            GeminiImageService,
            "LEGACY_REFERENCE_GUIDE_STORAGE_DIR",
            tmp_path / "legacy-reference-guides",
        )
        monkeypatch.setenv("MOCKUP_REQUIRE_REFERENCE_GUIDE", "false")
        # Disable the global aspect-ratio override so the tested ratio mapping
        # (2x3 -> 3:4) is preserved and not overridden by FORCE_GENERATION_ASPECT_RATIO.
        monkeypatch.setattr(GeminiImageService, "FORCE_GENERATION_ASPECT_RATIO", "")

        prompt = MockupPromptService.generate_prompt(
            category=category,
            variation_index=variation_index,
        )

        service = GeminiImageService(api_key="test-key")
        file_path = service.generate_image(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            category=category,
            variation_index=variation_index,
        )

        assert Path(file_path).exists()
        assert Path(file_path).read_bytes() == fake_bytes
        assert len(fake_client.models.generate_images_calls) == 1

        config = fake_client.models.generate_images_calls[0]["config"]
        assert isinstance(config, (dict, _FakeGenerateImagesConfig))
        aspect_ratio_val = config["aspect_ratio"] if isinstance(config, dict) else config.aspect_ratio
        assert aspect_ratio_val == "3:4"

    def test_stage2a_uses_cyan_reference_guide_when_available(self, monkeypatch, tmp_path):
        """Verify Gemini uses edit_image with the per-aspect cyan guide when present."""
        category = "cafe"
        variation_index = 4
        aspect_ratio = "16x9"
        fake_bytes = b"guided-fake-png"

        fake_client = _install_fake_genai(monkeypatch, response_bytes=fake_bytes)
        monkeypatch.setattr(GeminiImageService, "MOCKUP_BASE_STORAGE_DIR", tmp_path / "bases")

        reference_dir = tmp_path / "reference-guides"
        reference_dir.mkdir(parents=True, exist_ok=True)
        (reference_dir / "cyan_guide_16x9.png").write_bytes(b"guide-bytes")

        monkeypatch.setattr(GeminiImageService, "REFERENCE_GUIDE_STORAGE_DIR", reference_dir)
        monkeypatch.setattr(
            GeminiImageService,
            "LEGACY_REFERENCE_GUIDE_STORAGE_DIR",
            tmp_path / "legacy-reference-guides",
        )
        monkeypatch.setenv("GOOGLE_GENAI_USE_VERTEXAI", "true")
        monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "test-project")
        monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", "australia-southeast1")

        prompt = MockupPromptService.generate_prompt(
            category=category,
            variation_index=variation_index,
        )

        service = GeminiImageService(api_key="test-key")
        file_path = service.generate_image(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            category=category,
            variation_index=variation_index,
        )

        assert Path(file_path).exists()
        assert Path(file_path).read_bytes() == fake_bytes
        assert len(fake_client.models.edit_image_calls) == 1
        assert len(fake_client.models.generate_images_calls) == 0

        call = fake_client.models.edit_image_calls[0]
        assert call["model"] == service.IMAGE_EDIT_MODEL
        # Service wraps the user prompt with HARD_EDGE_PROMPT_PREFIX + system instructions.
        assert prompt in str(call["prompt"])

        config = call["config"]
        assert isinstance(config, _FakeEditImageConfig)
        assert config.edit_mode == "EDIT_MODE_CONTROLLED_EDITING"
        assert config.number_of_images == 1
        assert config.output_mime_type == "image/png"

        reference_images = call["reference_images"]
        assert isinstance(reference_images, list)
        assert len(reference_images) == 1

        control_reference = reference_images[0]
        assert isinstance(control_reference, _FakeControlReferenceImage)
        assert control_reference.reference_id == 1
        assert control_reference.reference_image.location.endswith("cyan_guide_16x9.png")
        assert control_reference.config.control_type == "CONTROL_TYPE_SCRIBBLE"
        assert control_reference.config.enable_control_image_computation is True

    def test_stage2a_requires_vertex_when_guide_mode_enabled(self, monkeypatch, tmp_path):
        """Verify strict guide mode rejects text-only fallback outside Vertex AI mode."""
        category = "cafe"
        variation_index = 4
        aspect_ratio = "16x9"
        fake_bytes = b"non-vertex-fake-png"

        fake_client = _install_fake_genai(monkeypatch, response_bytes=fake_bytes)
        monkeypatch.setattr(fake_client.models, "edit_image", None)
        monkeypatch.setattr(GeminiImageService, "MOCKUP_BASE_STORAGE_DIR", tmp_path / "bases")

        reference_dir = tmp_path / "reference-guides"
        reference_dir.mkdir(parents=True, exist_ok=True)
        (reference_dir / "cyan_guide_16x9.png").write_bytes(b"guide-bytes")

        monkeypatch.setattr(GeminiImageService, "REFERENCE_GUIDE_STORAGE_DIR", reference_dir)
        monkeypatch.setattr(
            GeminiImageService,
            "LEGACY_REFERENCE_GUIDE_STORAGE_DIR",
            tmp_path / "legacy-reference-guides",
        )
        monkeypatch.setenv("MOCKUP_REQUIRE_REFERENCE_GUIDE", "true")
        monkeypatch.setenv("MOCKUP_REQUIRE_REFERENCE_GUIDE_STRICT", "true")
        monkeypatch.delenv("GOOGLE_GENAI_USE_VERTEXAI", raising=False)
        monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
        monkeypatch.delenv("GOOGLE_CLOUD_LOCATION", raising=False)

        prompt = MockupPromptService.generate_prompt(
            category=category,
            variation_index=variation_index,
        )

        service = GeminiImageService(api_key="test-key")
        with pytest.raises(GeminiGenerationError, match="reference-guided edit_image is unavailable"):
            service.generate_image(
                prompt=prompt,
                aspect_ratio=aspect_ratio,
                category=category,
                variation_index=variation_index,
            )

        assert len(fake_client.models.edit_image_calls) == 0
        assert len(fake_client.models.generate_images_calls) == 0

    def test_stage2a_requires_reference_guides_by_default(self, monkeypatch, tmp_path):
        """Verify the mockup pipeline defaults to guide-backed generation."""
        _install_fake_genai(monkeypatch, response_bytes=b"unused")
        monkeypatch.setattr(GeminiImageService, "MOCKUP_BASE_STORAGE_DIR", tmp_path / "bases")
        monkeypatch.setattr(GeminiImageService, "REFERENCE_GUIDE_STORAGE_DIR", tmp_path / "reference-guides")
        monkeypatch.setattr(
            GeminiImageService,
            "LEGACY_REFERENCE_GUIDE_STORAGE_DIR",
            tmp_path / "legacy-reference-guides",
        )
        monkeypatch.setattr(
            GeminiImageService,
            "POSITIONAL_REFERENCE_GUIDE_STORAGE_DIR",
            tmp_path / "positional-reference-guides",
        )
        monkeypatch.setattr(
            GeminiImageService,
            "POSITIONAL_REFERENCE_GUIDE_SOURCE_DIR",
            tmp_path / "positional-source-guides",
        )
        monkeypatch.delenv("MOCKUP_REQUIRE_REFERENCE_GUIDE", raising=False)
        monkeypatch.delenv("MOCKUP_REQUIRE_REFERENCE_GUIDE_STRICT", raising=False)

        prompt = MockupPromptService.generate_prompt(category="cafe", variation_index=1)
        service = GeminiImageService(api_key="test-key")

        with pytest.raises(GeminiGenerationError, match="No reference guide found"):
            service.generate_image(
                prompt=prompt,
                aspect_ratio="5x4",
                category="cafe",
                variation_index=1,
            )

    def test_stage2a_uses_positional_guide_when_selected(self, monkeypatch, tmp_path):
        """Verify positional placeholder mode resolves the positional guide image."""
        fake_client = _install_fake_genai(monkeypatch, response_bytes=b"guide-image")
        monkeypatch.setattr(GeminiImageService, "MOCKUP_BASE_STORAGE_DIR", tmp_path / "bases")

        positional_dir = tmp_path / "positional-reference-guides"
        positional_dir.mkdir(parents=True, exist_ok=True)
        (positional_dir / "coordinate-tester-5x4.jpg").write_bytes(b"guide-bytes")

        control_state_path = tmp_path / "control.json"
        control_state_path.write_text('{"placeholder_mode": "positional"}', encoding="utf-8")

        monkeypatch.setattr(
            gemini_service_module,
            "CONTROL_STATE_PATH",
            control_state_path,
        )
        monkeypatch.setattr(
            GeminiImageService,
            "POSITIONAL_REFERENCE_GUIDE_STORAGE_DIR",
            positional_dir,
        )
        monkeypatch.setattr(
            GeminiImageService,
            "POSITIONAL_REFERENCE_GUIDE_SOURCE_DIR",
            tmp_path / "positional-source-guides",
        )
        monkeypatch.setattr(GeminiImageService, "REFERENCE_GUIDE_STORAGE_DIR", tmp_path / "reference-guides")
        monkeypatch.setattr(
            GeminiImageService,
            "LEGACY_REFERENCE_GUIDE_STORAGE_DIR",
            tmp_path / "legacy-reference-guides",
        )
        monkeypatch.setenv("GOOGLE_GENAI_USE_VERTEXAI", "true")
        monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "test-project")
        monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", "us-central1")

        prompt = MockupPromptService.generate_prompt(category="cafe", variation_index=1)
        service = GeminiImageService(api_key="test-key")
        service.generate_image(
            prompt=prompt,
            aspect_ratio="5x4",
            category="cafe",
            variation_index=1,
        )

        assert len(fake_client.models.edit_image_calls) == 1
        edit_call = cast(dict[str, Any], fake_client.models.edit_image_calls[0])
        reference_images = cast(list[Any], edit_call["reference_images"])
        control_reference = reference_images[0]
        assert control_reference.reference_image.location.endswith("coordinate-tester-5x4.jpg")

    def test_stage2a_disables_text_only_fallback_when_guided_edit_fails(
        self,
        monkeypatch,
        tmp_path,
    ):
        """Verify strict guide mode surfaces guided-edit failures without fallback."""
        category = "living-room"
        variation_index = 2
        aspect_ratio = "4x5"
        fake_bytes = b"fallback-png"

        fake_client = _install_fake_genai(monkeypatch, response_bytes=fake_bytes)
        fake_client.models.edit_image_error = RuntimeError("edit path unavailable")
        monkeypatch.setattr(GeminiImageService, "MOCKUP_BASE_STORAGE_DIR", tmp_path / "bases")

        reference_dir = tmp_path / "reference-guides"
        reference_dir.mkdir(parents=True, exist_ok=True)
        (reference_dir / "cyan_guide_4x5.png").write_bytes(b"guide-bytes")

        monkeypatch.setattr(GeminiImageService, "REFERENCE_GUIDE_STORAGE_DIR", reference_dir)
        monkeypatch.setattr(
            GeminiImageService,
            "LEGACY_REFERENCE_GUIDE_STORAGE_DIR",
            tmp_path / "legacy-reference-guides",
        )
        monkeypatch.setenv("MOCKUP_REQUIRE_REFERENCE_GUIDE", "true")
        monkeypatch.setenv("MOCKUP_REQUIRE_REFERENCE_GUIDE_STRICT", "true")
        monkeypatch.setenv("GOOGLE_GENAI_USE_VERTEXAI", "true")
        monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "test-project")
        monkeypatch.setenv("GOOGLE_CLOUD_LOCATION", "us-central1")

        prompt = MockupPromptService.generate_prompt(
            category=category,
            variation_index=variation_index,
        )

        service = GeminiImageService(api_key="test-key")
        with pytest.raises(
            GeminiGenerationError,
            match="Reference-guided generation failed and text-only fallback is disabled",
        ):
            service.generate_image(
                prompt=prompt,
                aspect_ratio=aspect_ratio,
                category=category,
                variation_index=variation_index,
            )

        assert len(fake_client.models.edit_image_calls) == 1
        assert len(fake_client.models.generate_images_calls) == 0

    def test_stage2a_contract_all_categories_and_aspects(self, monkeypatch, tmp_path):
        """Verify Stage 2A contract for all category and aspect combinations."""
        monkeypatch.setenv("MOCKUP_REQUIRE_REFERENCE_GUIDE", "false")
        monkeypatch.setattr(
            GeminiImageService,
            "_call_gemini_generate_images",
            lambda self, prompt, aspect_ratio, thought_signature=None, system_instruction=None, raw_prompt=False: b"contract-test-image",
        )
        monkeypatch.setattr(
            GeminiImageService,
            "_save_image_to_disk",
            lambda self, image_bytes, category, aspect_ratio, variation_index: (
                tmp_path / f"{category}_{aspect_ratio}_{variation_index}.png"
            ),
        )
        monkeypatch.setattr(
            GeminiImageService,
            "REFERENCE_GUIDE_STORAGE_DIR",
            tmp_path / "reference-guides",
        )
        monkeypatch.setattr(
            GeminiImageService,
            "LEGACY_REFERENCE_GUIDE_STORAGE_DIR",
            tmp_path / "legacy-reference-guides",
        )

        # Test a subset for performance (full test would be 13*23*20 = 5,980 combinations)
        test_categories = MockupBaseGenerationCatalog.CATEGORIES[:5]  # First 5 categories
        test_aspects = MockupBaseGenerationCatalog.ASPECT_RATIOS[:3]  # First 3 aspects
        test_variations = [1, 10, 20]  # First, middle, and last variation

        for category in test_categories:
            for variation_index in test_variations:
                # Generate prompt
                prompt = MockupPromptService.generate_prompt(
                    category=category,
                    variation_index=variation_index,
                )

                # Verify prompt contract
                assert isinstance(prompt, str)
                assert len(prompt) > 100
                assert "cyan" in prompt.lower()

                # Verify GeminiImageService accepts all parameter combinations
                service = GeminiImageService(api_key="test-key")
                for aspect_ratio in test_aspects:
                    try:
                        result = service.generate_image(
                            prompt=prompt,
                            aspect_ratio=aspect_ratio,
                            category=category,
                            variation_index=variation_index,
                        )
                        assert isinstance(result, str)
                    except ValueError as e:
                        pytest.fail(f"Unexpected ValueError: {str(e)}")
                    except Exception:
                        pytest.fail("Unexpected non-validation exception during contract test")

    def test_generate_images_surfaces_rate_limit_with_retry_delay(self, monkeypatch):
        """Verify Gemini 429 responses become retryable rate-limit errors."""
        fake_client = _install_fake_genai(monkeypatch, response_bytes=b"unused")

        def _raise_quota(*, model, prompt, config):
            raise RuntimeError(
                "429 RESOURCE_EXHAUSTED. Please retry in 21.884554567s. "
                "{'error': {'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '21s'}]}}"
            )

        fake_client.models.generate_images = _raise_quota
        monkeypatch.setenv("MOCKUP_REQUIRE_REFERENCE_GUIDE", "false")
        monkeypatch.setattr(
            GeminiImageService,
            "REFERENCE_GUIDE_STORAGE_DIR",
            Path("/tmp/nonexistent-reference-guides"),
        )
        monkeypatch.setattr(
            GeminiImageService,
            "LEGACY_REFERENCE_GUIDE_STORAGE_DIR",
            Path("/tmp/nonexistent-legacy-reference-guides"),
        )
        monkeypatch.setattr(
            GeminiImageService,
            "POSITIONAL_REFERENCE_GUIDE_STORAGE_DIR",
            Path("/tmp/nonexistent-positional-reference-guides"),
        )
        monkeypatch.setattr(
            GeminiImageService,
            "POSITIONAL_REFERENCE_GUIDE_SOURCE_DIR",
            Path("/tmp/nonexistent-positional-source-guides"),
        )

        service = GeminiImageService(api_key="test-key")

        with pytest.raises(GeminiRateLimitError) as exc_info:
            service.generate_image(
                prompt="test prompt",
                aspect_ratio="1x1",
                category="living-room",
                variation_index=1,
            )

        assert exc_info.value.retry_after_seconds == 21
        assert "Retry after approximately 21s" in str(exc_info.value)
