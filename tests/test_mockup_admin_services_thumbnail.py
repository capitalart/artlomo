from __future__ import annotations

from pathlib import Path

from PIL import Image

import application.mockups.admin.services as admin_services


def test_render_thumb_uses_pillow_fallback_when_node_processor_unavailable(tmp_path, monkeypatch):
    base_png = tmp_path / "base.png"
    thumb_out = tmp_path / "thumb.jpg"

    # Non-square source to verify centered contain behavior in fallback path.
    Image.new("RGB", (900, 600), (120, 160, 190)).save(base_png, format="PNG")

    monkeypatch.setattr(admin_services, "_run_node_processor", lambda payload: None)

    admin_services._render_thumb_500_jpg(base_png=base_png, thumb_out=thumb_out)

    assert thumb_out.exists()
    with Image.open(thumb_out) as thumb:
        assert thumb.format == "JPEG"
        assert thumb.size == (500, 500)
