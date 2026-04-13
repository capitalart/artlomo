from __future__ import annotations

from application.common.utilities.images import ImageInfo
from application.upload.services.qc_service import QCService


def _image_info(*, long_edge: int) -> ImageInfo:
    width = long_edge
    height = max(1, long_edge - 100)
    return ImageInfo(
        width=width,
        height=height,
        fmt="JPEG",
        dpi_x=300,
        dpi_y=300,
        mode="RGB",
        icc_present=False,
        icc_profile_name=None,
    )


def test_upload_qc_accepts_7200px_long_edge(monkeypatch):
    service = QCService(required_long_edge=7200, required_dpi=300, allowed_extensions={"jpg", "jpeg"})

    monkeypatch.setattr(
        "application.upload.services.qc_service.images.read_image_info",
        lambda _bytes: _image_info(long_edge=7200),
    )
    monkeypatch.setattr(
        "application.upload.services.qc_service.images.is_jpeg_format",
        lambda _fmt: True,
    )

    result = service.validate_upload(b"fake-jpeg", "sample.jpg")

    assert result.passed is True
    assert result.reasons == []


def test_upload_qc_rejects_below_7200px_long_edge(monkeypatch):
    service = QCService(required_long_edge=7200, required_dpi=300, allowed_extensions={"jpg", "jpeg"})

    monkeypatch.setattr(
        "application.upload.services.qc_service.images.read_image_info",
        lambda _bytes: _image_info(long_edge=7199),
    )
    monkeypatch.setattr(
        "application.upload.services.qc_service.images.is_jpeg_format",
        lambda _fmt: True,
    )

    result = service.validate_upload(b"fake-jpeg", "sample.jpg")

    assert result.passed is False
    assert any("Long edge must be at least 7200px" in reason for reason in result.reasons)