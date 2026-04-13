"""
Tests for the Detail Closeup feature.

Covers:
- Proxy image generation from master
- Crop rendering with normalized center coordinates
- Bounds validation
- 2048x2048px output verification
- Route handlers with CSRF and slug validation
"""

import json
import pytest
from pathlib import Path
from PIL import Image
from application.artwork.services.detail_closeup_service import DetailCloseupService


class TestDetailCloseupService:
    """Test the DetailCloseupService class."""

    @pytest.fixture
    def service(self, tmp_path):
        """Create a service instance with temporary directory."""
        return DetailCloseupService(processed_root=tmp_path)

    @pytest.fixture
    def master_image(self, tmp_path):
        """Create a test master image (14400x14400px)."""
        slug = "test-artwork"
        slug_dir = tmp_path / slug
        slug_dir.mkdir(parents=True, exist_ok=True)

        # Create a 14400x14400 test image
        test_image = Image.new("RGB", (14400, 14400), color=(200, 150, 100))

        master_path = slug_dir / f"{slug}-MASTER.jpg"
        test_image.save(str(master_path), "JPEG", quality=95)

        return slug, master_path

    def test_generate_proxy_preview(self, service, master_image):
        """Test proxy preview generation."""
        slug, master_path = master_image
        assert master_path.exists(), "Master image should exist"

        result = service.generate_proxy_preview(slug)
        assert result is True, "generate_proxy_preview should return True"

        proxy_path = master_path.parent / f"{slug}-CLOSEUP-PROXY.jpg"
        assert proxy_path.exists(), "Proxy image should be created"

        # Verify proxy dimensions
        proxy_img = Image.open(proxy_path)
        long_edge = max(proxy_img.width, proxy_img.height)
        assert long_edge == 7200, f"Proxy long edge should be 7200, got {long_edge}"

    def test_render_detail_crop_basic(self, service, master_image):
        """Test basic crop rendering at image center."""
        slug, master_path = master_image

        result = service.render_detail_crop(slug, norm_x=0.5, norm_y=0.5, scale=1.0)

        assert result is True, "Should return True on success"
        assert service.has_detail_closeup(slug), "Crop file should be saved"

        # Verify output is exactly 2048x2048
        crop_path = service._get_detail_closeup_path(slug)
        crop_img = Image.open(crop_path)
        assert crop_img.size == (2048, 2048), f"Expected 2048x2048, got {crop_img.size}"

    def test_render_detail_crop_zoomed(self, service, master_image):
        """Test crop rendering with zoom (scale > 1.0)."""
        slug, master_path = master_image

        result = service.render_detail_crop(slug, norm_x=0.5, norm_y=0.5, scale=2.0)

        assert result is True, "Should return True on success"
        crop_path = service._get_detail_closeup_path(slug)
        crop_img = Image.open(crop_path)
        assert crop_img.size == (2048, 2048), "Zoomed crop should be 2048x2048"

    def test_render_detail_crop_with_norm_offset(self, service, master_image):
        """Test crop rendering with non-centered normalized coordinates."""
        slug, master_path = master_image

        result = service.render_detail_crop(slug, norm_x=0.6, norm_y=0.55, scale=1.0)

        assert result is True, "Should return True on success"
        crop_path = service._get_detail_closeup_path(slug)
        crop_img = Image.open(crop_path)
        assert crop_img.size == (2048, 2048)

    def test_render_detail_crop_invalid_scale_low(self, service, master_image):
        """Test that crop rejects scale < 0.1."""
        slug, master_path = master_image

        with pytest.raises(ValueError, match="Invalid scale"):
            service.render_detail_crop(slug, norm_x=0.5, norm_y=0.5, scale=0.05)

    def test_render_detail_crop_invalid_scale_high(self, service, master_image):
        """Test that crop rejects scale > 10.0."""
        slug, master_path = master_image

        with pytest.raises(ValueError, match="Invalid scale"):
            service.render_detail_crop(slug, norm_x=0.5, norm_y=0.5, scale=15.0)

    def test_render_detail_crop_rejects_invalid_norm(self, service, master_image):
        """Test that crop rejects out-of-bounds normalized coordinates."""
        slug, master_path = master_image

        with pytest.raises(ValueError, match="Invalid normalized coordinates"):
            service.render_detail_crop(slug, norm_x=1.5, norm_y=0.5, scale=1.0)

    def test_has_detail_closeup(self, service, master_image):
        """Test checking if detail closeup exists."""
        slug, master_path = master_image

        # Should not exist initially
        assert service.has_detail_closeup(slug) is False

        # Create one
        service.render_detail_crop(slug, norm_x=0.5, norm_y=0.5, scale=1.0)

        # Now should exist
        assert service.has_detail_closeup(slug) is True

    def test_get_detail_closeup_url(self, service, master_image):
        """Test getting the URL for a saved closeup."""
        slug, master_path = master_image

        # Before save, URL should be None
        assert service.get_detail_closeup_url(slug) is None

        # After save, URL should point to mockup
        service.render_detail_crop(slug, norm_x=0.5, norm_y=0.5, scale=1.0)
        url = service.get_detail_closeup_url(slug)
        assert url is not None
        assert slug in url
        assert "detail-closeup" in url

    def test_missing_master_image(self, service, tmp_path):
        """Test handling of missing master image."""
        slug = "nonexistent"

        result = service.generate_proxy_preview(slug)
        assert result is False, "Should return False for missing master"

        result = service.render_detail_crop(slug, norm_x=0.5, norm_y=0.5, scale=1.0)
        assert result is False, "Should return False for missing master"


class TestDetailCloseupRoutes:
    """Test the detail closeup routes."""

    @pytest.fixture
    def client(self, app_client):
        """Use the app_client fixture from conftest."""
        return app_client

    @pytest.fixture
    def test_slug(self, tmp_path, app):
        """Create test artwork with master image."""
        slug = "test-closeup-route"
        
        # Create processed directory structure
        processed_dir = Path(app.config["LAB_PROCESSED_DIR"])
        slug_dir = processed_dir / slug
        slug_dir.mkdir(parents=True, exist_ok=True)

        # Create master image
        master_img = Image.new("RGB", (14400, 14400), color=(100, 100, 100))
        master_path = slug_dir / f"{slug}-MASTER.jpg"
        master_img.save(str(master_path), "JPEG", quality=95)

        return slug

    def test_detail_closeup_proxy_route(self, client, test_slug):
        """Test GET /detail-closeup/proxy endpoint."""
        response = client.get(f"/artwork/{test_slug}/detail-closeup/proxy")
        
        assert response.status_code == 200
        assert response.mimetype == "image/jpeg"

    def test_detail_closeup_proxy_invalid_slug(self, client):
        """Test proxy route rejects invalid slug."""
        response = client.get("/artwork/../../etc/passwd/detail-closeup/proxy")
        
        assert response.status_code == 404

    def test_detail_closeup_editor_route(self, client, test_slug):
        """Test GET /detail-closeup/editor endpoint."""
        response = client.get(f"/artwork/{test_slug}/detail-closeup/editor")
        
        assert response.status_code == 200
        assert b"Detail Closeup Editor" in response.data
        assert b"detail_closeup.js" in response.data

    def test_detail_closeup_editor_invalid_slug(self, client):
        """Test editor route rejects invalid slug."""
        response = client.get("/artwork/invalid../slug/detail-closeup/editor")
        
        assert response.status_code == 404

    def test_detail_closeup_freeze_route(self, client, test_slug):
        """Test POST /detail-closeup/freeze endpoint."""
        payload = {"scale": 1.5, "offset_x": 50, "offset_y": 50}

        response = client.post(
            f"/artwork/{test_slug}/detail-closeup/freeze",
            data=json.dumps(payload),
            content_type="application/json",
            headers={"X-CSRF-Token": client.csrf_token}
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "ok"
        assert data["preview_data"].startswith("data:image/jpeg;base64,")

    def test_detail_closeup_freeze_missing_csrf(self, client, test_slug):
        """Test freeze endpoint requires CSRF token."""
        payload = {"scale": 1.5, "offset_x": 0, "offset_y": 0}

        response = client.post(
            f"/artwork/{test_slug}/detail-closeup/freeze",
            data=json.dumps(payload),
            content_type="application/json",
            # Missing CSRF token
        )

        assert response.status_code == 400

    def test_detail_closeup_save_route(self, client, test_slug):
        """Test POST /detail-closeup/save endpoint."""
        payload = {"scale": 1.0, "norm_x": 0.5, "norm_y": 0.5}

        response = client.post(
            f"/artwork/{test_slug}/detail-closeup/save",
            data=json.dumps(payload),
            content_type="application/json",
            headers={"X-CSRF-Token": client.csrf_token}
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"

    def test_detail_closeup_save_invalid_scale(self, client, test_slug):
        """Test save endpoint rejects invalid scale."""
        payload = {"scale": 100.0, "norm_x": 0.5, "norm_y": 0.5}

        response = client.post(
            f"/artwork/{test_slug}/detail-closeup/save",
            data=json.dumps(payload),
            content_type="application/json",
            headers={"X-CSRF-Token": client.csrf_token}
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data or "scale" in data.get("message", "").lower()

    def test_detail_closeup_view_route_not_found(self, client, test_slug):
        """Test view route returns 404 when closeup doesn't exist."""
        response = client.get(f"/artwork/{test_slug}/detail-closeup")
        
        # Should 404 since we haven't saved a closeup
        assert response.status_code == 404

    def test_detail_closeup_view_route_success(self, client, test_slug):
        """Test view route returns saved closeup."""
        # First save a closeup
        save_payload = {"scale": 1.0, "norm_x": 0.5, "norm_y": 0.5}
        save_response = client.post(
            f"/artwork/{test_slug}/detail-closeup/save",
            data=json.dumps(save_payload),
            content_type="application/json",
            headers={"X-CSRF-Token": client.csrf_token}
        )
        assert save_response.status_code == 200

        # Now view should work
        response = client.get(f"/artwork/{test_slug}/detail-closeup")
        assert response.status_code == 200
        assert response.mimetype == "image/jpeg"


class TestDetailCloseupIntegration:
    """Integration tests for the complete detail closeup workflow."""

    def test_full_workflow(self, app, tmp_path):
        """Test complete workflow: proxy → freeze → save → view."""
        from application.artwork.services.detail_closeup_service import DetailCloseupService
        
        slug = "full-workflow-test"
        processed_dir = tmp_path / "processed"
        processed_dir.mkdir()
        
        slug_dir = processed_dir / slug
        slug_dir.mkdir()

        # Step 1: Create master image
        master = Image.new("RGB", (14400, 14400), color=(100, 100, 100))
        master_path = slug_dir / f"{slug}-MASTER.jpg"
        master.save(str(master_path), "JPEG", quality=95)

        svc = DetailCloseupService(processed_root=processed_dir)

        # Step 2: Generate proxy
        assert svc.generate_proxy_preview(slug) is True
        proxy_path = slug_dir / f"{slug}-CLOSEUP-PROXY.jpg"
        assert proxy_path.exists()

        # Step 3: Render crop (simulates freeze + save)
        result = svc.render_detail_crop(slug, norm_x=0.5, norm_y=0.5, scale=1.5)
        assert result is True, "Should successfully render detail crop"
        
        # Step 4: Verify output
        crop_path = svc._get_detail_closeup_path(slug)
        assert crop_path.exists(), "Crop file should exist"
        crop_img = Image.open(crop_path)
        assert crop_img.size == (2048, 2048)

        # Step 5: Check if saved
        assert svc.has_detail_closeup(slug) is True
        url = svc.get_detail_closeup_url(slug)
        assert url is not None
