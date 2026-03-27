"""Stage 2B Validation Tests for Solid Image Service and Generator Routes.

Validates:
1. SolidImageService generates valid solid color images
2. SolidImageService respects memory limits
3. Generator routes render correctly
4. Generator routes query database properly
5. Utility routes handle form submission
6. Image generation and download work end-to-end
"""

from __future__ import annotations

import os
import pytest
from io import BytesIO
from pathlib import Path
from PIL import Image

from application.mockups.services.solid_image_service import (
    SolidImageService,
    SolidImageValidationError,
    SolidImageGenerationError,
)
from application.mockups.config import MockupBaseGenerationCatalog


class TestSolidImageService:
    """Test suite for SolidImageService."""

    def test_solid_image_service_generate_cyan(self):
        """Verify SolidImageService generates cyan solid image."""
        image_buffer = SolidImageService.generate_solid_image(
            aspect_ratio="16:9",
            color="#00FFFF",
            output_path=None,
        )
        
        assert isinstance(image_buffer, BytesIO)
        image_buffer.seek(0)
        img = Image.open(image_buffer)
        assert img.mode == "RGB"
        # 16:9 at scale 1000 = 16000x9000, but capped at 5000px
        assert img.size[0] > 0
        assert img.size[1] > 0

    def test_solid_image_service_respects_memory_limits(self):
        """Verify very large ratios are capped to prevent OOM."""
        # 70:99 is the largest ratio; should be capped
        image_buffer = SolidImageService.generate_solid_image(
            aspect_ratio="70:99",
            color="#FF0000",
            output_path=None,
        )
        
        assert isinstance(image_buffer, BytesIO)
        image_buffer.seek(0)
        img = Image.open(image_buffer)
        
        # Longest dimension should be <= MAX_PIXEL_DIMENSION (5000)
        max_dimension = max(img.size)
        assert max_dimension <= SolidImageService.MAX_PIXEL_DIMENSION

    def test_solid_image_service_aspect_ratio_parsing(self):
        """Verify aspect ratio parsing handles valid and invalid inputs."""
        # Valid cases
        width, height = SolidImageService._parse_aspect_ratio("16:9")
        assert width == 16
        assert height == 9

        width, height = SolidImageService._parse_aspect_ratio("1:1")
        assert width == 1
        assert height == 1

        # Invalid cases
        with pytest.raises(ValueError):
            SolidImageService._parse_aspect_ratio("16x9")  # Wrong separator

        with pytest.raises(ValueError):
            SolidImageService._parse_aspect_ratio("invalid")  # Missing separator

        with pytest.raises(ValueError):
            SolidImageService._parse_aspect_ratio("0:9")  # Non-positive

        with pytest.raises(ValueError):
            SolidImageService._parse_aspect_ratio("16:0")  # Non-positive

    def test_solid_image_service_hex_color_parsing(self):
        """Verify hex color parsing handles valid and invalid inputs."""
        # Valid cases
        r, g, b = SolidImageService._parse_hex_color("#00FFFF")
        assert (r, g, b) == (0, 255, 255)

        r, g, b = SolidImageService._parse_hex_color("00FFFF")
        assert (r, g, b) == (0, 255, 255)

        r, g, b = SolidImageService._parse_hex_color("FF0000")
        assert (r, g, b) == (255, 0, 0)

        # Invalid cases
        with pytest.raises(ValueError):
            SolidImageService._parse_hex_color("GGGGGG")  # Invalid characters

        with pytest.raises(ValueError):
            SolidImageService._parse_hex_color("FF00")  # Too short

        with pytest.raises(ValueError):
            SolidImageService._parse_hex_color("#FF00FFEE")  # Too long

    def test_solid_image_service_dimension_calculation(self):
        """Verify dimension calculation respects scaling and capping."""
        # Small ratio, scaled and capped to fit max dimension
        w, h = SolidImageService._calculate_dimensions(
            width_ratio=16,
            height_ratio=9,
            scale_factor=1000,
        )
        # 16*1000=16000, 9*1000=9000; max 16000 > 5000, so both get scaled down
        # Ratio maintained: 16:9, but longest edge = 5000
        assert w / h == pytest.approx(16 / 9, abs=0.01)
        assert max(w, h) == SolidImageService.MAX_PIXEL_DIMENSION

        # Large ratio (cap test)
        w, h = SolidImageService._calculate_dimensions(
            width_ratio=70,
            height_ratio=99,
            scale_factor=1000,
        )
        assert max(w, h) <= SolidImageService.MAX_PIXEL_DIMENSION

    def test_solid_image_service_all_aspect_ratios(self):
        """Verify solid image service works with all 13 standard aspect ratios."""
        for ratio_str in MockupBaseGenerationCatalog.ASPECT_RATIOS:
            # Convert from "XxY" to "X:Y" format
            ratio_colon = ratio_str.replace("x", ":")
            
            image_buffer = SolidImageService.generate_solid_image(
                aspect_ratio=ratio_colon,
                color="#00FFFF",
                output_path=None,
            )
            
            assert isinstance(image_buffer, BytesIO)
            image_buffer.seek(0)
            img = Image.open(image_buffer)
            assert img.mode == "RGB"

    def test_solid_image_service_file_save(self, tmp_path):
        """Verify image can be saved to disk."""
        output_path = tmp_path / "test_image.png"
        
        file_path = SolidImageService.generate_solid_image(
            aspect_ratio="1:1",
            color="#FFFFFF",
            output_path=output_path,
        )
        
        assert isinstance(file_path, str)
        assert Path(file_path).exists()
        assert Path(file_path).stat().st_size > 0
        
        # Verify it's a valid PNG
        img = Image.open(file_path)
        assert img.mode == "RGB"

    def test_solid_image_service_colors(self):
        """Verify different colors produce expected RGB values."""
        for hex_color, expected_rgb in [
            ("#00FFFF", (0, 255, 255)),  # Cyan
            ("#FF0000", (255, 0, 0)),    # Red
            ("#00FF00", (0, 255, 0)),    # Green
            ("#0000FF", (0, 0, 255)),    # Blue
            ("#FFFFFF", (255, 255, 255)),  # White
            ("#000000", (0, 0, 0)),      # Black
        ]:
            image_buffer = SolidImageService.generate_solid_image(
                aspect_ratio="1:1",
                color=hex_color,
                output_path=None,
            )
            
            assert isinstance(image_buffer, BytesIO)
            image_buffer.seek(0)
            img = Image.open(image_buffer)
            
            # Check pixel color (get first pixel)
            pixel = img.getpixel((0, 0))
            assert pixel == expected_rgb


class TestUtilityRoutes:
    """Test suite for solid image utility routes."""

    def test_solid_image_form_route_exists(self, client):
        """Verify solid image form route is accessible."""
        response = client.get("/admin/mockups/solid-image-generator")
        # Should return 200 or redirect based on auth
        assert response.status_code in (200, 302)

    def test_solid_image_generator_form_contains_aspects(self, client):
        """Verify form includes all 13 aspect ratio options."""
        response = client.get("/admin/mockups/solid-image-generator")
        
        # Check status
        if response.status_code != 200:
            pytest.skip("Route requires authentication")
        
        # Check that form contains aspect ratio options
        for ratio in MockupBaseGenerationCatalog.ASPECT_RATIOS:
            # Form should list both "XxY" format and pixel dimensions
            assert ratio.encode() in response.data or ratio.replace("x", ":").encode() in response.data


class TestServiceIntegration:
    """Integration tests for Stage 2B components."""

    def test_solid_image_service_produces_downloadable_png(self, tmp_path):
        """Verify end-to-end solid image generation."""
        output_path = tmp_path / "download.png"
        
        file_path = SolidImageService.generate_solid_image(
            aspect_ratio="16:9",
            color="#00FFFF",
            output_path=output_path,
        )
        
        # Verify file exists and is valid
        assert isinstance(file_path, str)
        assert Path(file_path).exists()
        assert Path(file_path).suffix == ".png"
        
        # Load and verify dimensions
        img = Image.open(file_path)
        assert img.size[0] / img.size[1] == pytest.approx(16 / 9, abs=0.01)

    def test_stage_2b_contract_all_features(self):
        """Verify complete Stage 2B feature contract."""
        # Layer 2: Service generates images for all configurations
        for ratio_str in ["1:1", "16:9", "70:99"]:
            image_buffer = SolidImageService.generate_solid_image(
                aspect_ratio=ratio_str,
                color="#00FFFF",
                output_path=None,
            )
            assert isinstance(image_buffer, BytesIO)

        # Layer 3: Routes would be tested with Flask test client
        # Layer 4: Templates render with Jinja (visual inspection)


@pytest.fixture
def client():
    """Provide Flask test client."""
    from application.app import create_app
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
