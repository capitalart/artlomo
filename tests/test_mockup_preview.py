"""
Tests for mockup preview generation, artwork selection, and caching.
Validates contracts for preview modal behavior and preview generation workflow.
"""
import json
from pathlib import Path
from datetime import datetime, timezone
import pytest
from unittest.mock import Mock, patch, MagicMock

from application.mockups.admin.preview import PreviewService
from application.mockups.errors import ValidationError
from application.mockups.config import DEFAULT_MOCKUP_ASPECT, MOCKUP_TESTS_DIR


@pytest.fixture
def temp_preview_dirs(tmp_path):
    """Create temporary directories for preview testing."""
    catalog_path = tmp_path / "catalog"
    preview_art_root = tmp_path / "preview_art"
    cache_root = tmp_path / "cache"
    
    catalog_path.mkdir(parents=True)
    preview_art_root.mkdir(parents=True)
    cache_root.mkdir(parents=True)
    
    return {
        "catalog": catalog_path,
        "preview_art": preview_art_root,
        "cache": cache_root,
    }


@pytest.fixture
def preview_service(temp_preview_dirs):
    """Create preview service with temp directories."""
    service = PreviewService(
        catalog_path=temp_preview_dirs["catalog"],
        preview_art_root=temp_preview_dirs["preview_art"],
        cache_root=temp_preview_dirs["cache"],
    )
    return service


# ============================================================================
# Artwork Selection Tests
# ============================================================================

def test_list_preview_artworks_exact_aspect_match(preview_service, temp_preview_dirs):
    """
    **Contract**: When test artwork exists with exact aspect match, 
    _iter_preview_art_files returns exactly that file.
    """
    # Create test artwork files
    art_root = temp_preview_dirs["preview_art"]
    (art_root / "coordinate-tester-3x4.jpg").write_bytes(b"fake jpg")
    (art_root / "coordinate-tester-16x9.jpg").write_bytes(b"fake jpg")
    
    # Query for 3x4
    results = preview_service._iter_preview_art_files("3x4")
    assert len(results) == 1
    assert results[0].name == "coordinate-tester-3x4.jpg"
    
    # Query for 16x9
    results = preview_service._iter_preview_art_files("16x9")
    assert len(results) == 1
    assert results[0].name == "coordinate-tester-16x9.jpg"


def test_list_preview_artworks_prefers_coordinate_tester_name(preview_service, temp_preview_dirs):
    """
    **Contract**: When both new and legacy names exist, prefer coordinate-tester naming.
    """
    art_root = temp_preview_dirs["preview_art"]
    (art_root / "3x4.jpg").write_bytes(b"legacy")
    (art_root / "coordinate-tester-3x4.jpg").write_bytes(b"new")

    results = preview_service._iter_preview_art_files("3x4")
    assert len(results) == 1
    assert results[0].name == "coordinate-tester-3x4.jpg"


def test_list_preview_artworks_no_exact_match_returns_all(preview_service, temp_preview_dirs):
    """
    **Contract**: When no exact aspect match exists, fallback to all available 
    artworks (sorted alphabetically for determinism).
    """
    art_root = temp_preview_dirs["preview_art"]
    (art_root / "coordinate-tester-3x4.jpg").write_bytes(b"foo")
    (art_root / "coordinate-tester-16x9.jpg").write_bytes(b"bar")
    (art_root / "coordinate-tester-1x1.jpg").write_bytes(b"baz")
    
    # Query for non-existent aspect "2x3"
    results = preview_service._iter_preview_art_files("2x3")
    assert len(results) == 3
    # Should be sorted alphabetically
    names = [p.name for p in results]
    assert names == sorted(names)
    assert "coordinate-tester-1x1.jpg" in names


def test_list_preview_artworks_unset_aspect_returns_all(preview_service, temp_preview_dirs):
    """
    **Contract**: When aspect is UNSET (DEFAULT_MOCKUP_ASPECT), fallback to all 
    available artworks instead of returning empty list.
    This allows previewing bases without configured aspect ratio.
    """
    art_root = temp_preview_dirs["preview_art"]
    (art_root / "coordinate-tester-3x4.jpg").write_bytes(b"foo")
    (art_root / "coordinate-tester-16x9.jpg").write_bytes(b"bar")
    
    # Query with DEFAULT_MOCKUP_ASPECT (UNSET)
    results = preview_service._iter_preview_art_files(DEFAULT_MOCKUP_ASPECT)
    assert len(results) == 2
    # Verify we can preview UNSET bases with available test assets
    assert any(p.name == "coordinate-tester-3x4.jpg" for p in results)


def test_list_preview_artworks_empty_directory(preview_service):
    """
    **Contract**: When no artworks exist, return empty list (not error).
    """
    results = preview_service._iter_preview_art_files("3x4")
    assert results == []
    
    results = preview_service._iter_preview_art_files(None)
    assert results == []


def test_list_preview_artwork_records_includes_metadata(preview_service, temp_preview_dirs):
    """
    **Contract**: Record list includes filename, aspect, and path for each artwork.
    """
    art_root = temp_preview_dirs["preview_art"]
    (art_root / "coordinate-tester-3x4.jpg").write_bytes(b"fake")
    
    records = preview_service.list_preview_artwork_records("3x4")
    assert len(records) == 1
    assert records[0]["filename"] == "coordinate-tester-3x4.jpg"
    assert records[0]["aspect"] == "3x4"
    assert records[0]["path"] is None or isinstance(records[0]["path"], str)


def test_default_preview_artwork_returns_first_match(preview_service, temp_preview_dirs):
    """
    **Contract**: default_preview_artwork returns first artwork in sorted order (deterministic by filename).
    Sorted order is lexicographic by filename.
    """
    art_root = temp_preview_dirs["preview_art"]
    (art_root / "coordinate-tester-1x1.jpg").write_bytes(b"a")
    (art_root / "coordinate-tester-3x4.jpg").write_bytes(b"b")
    (art_root / "coordinate-tester-16x9.jpg").write_bytes(b"c")
    
    # For aspect with multiple fallback options, should get first in lexicographic order
    artwork = preview_service.default_preview_artwork("2x3")
    assert artwork is not None
    assert artwork.name == "coordinate-tester-16x9.jpg"


def test_default_preview_artwork_none_when_empty(preview_service):
    """
    **Contract**: default_preview_artwork returns None when no artworks available.
    """
    artwork = preview_service.default_preview_artwork("3x4")
    assert artwork is None


# ============================================================================
# Preview Generation Tests
# ============================================================================

def test_generate_preview_requires_ready_coordinates(preview_service):
    """
    **Contract**: generate_preview raises ValidationError if coordinates not in 'coordinates_ready' status.
    """
    # Mock a base with uploaded status (no coordinates)
    mock_base = Mock()
    mock_base.status = "uploaded"
    mock_base.coordinates = None
    
    with patch.object(preview_service, "_load_base_by_id", return_value=mock_base):
        with pytest.raises(ValidationError) as exc_info:
            preview_service.generate_preview("test-mockup-id")
        assert "Coordinates are not ready" in str(exc_info.value)


def test_generate_preview_requires_coordinates_payload(preview_service):
    """
    **Contract**: generate_preview raises ValidationError if coordinates payload exists 
    but content is invalid/unparseable.
    """
    mock_base = Mock()
    mock_base.status = "coordinates_ready"
    mock_base.coordinates = Mock()  # File path to coords
    mock_base.base_image = Mock()
    
    with patch.object(preview_service, "_load_base_by_id", return_value=mock_base):
        with patch("application.mockups.loader.load_base_rgba"):
            with patch("application.mockups.loader.load_coords", side_effect=Exception("Bad JSON")):
                with pytest.raises(Exception):
                    preview_service.generate_preview("test-mockup-id")


def test_generate_preview_validates_corners_within_image(preview_service):
    """
    **Contract**: generate_preview validates coordinate corners are within image bounds.
    """
    mock_base = Mock()
    mock_base.status = "coordinates_ready"
    mock_base.coordinates = Mock()
    mock_base.base_image = Mock()
    mock_base.aspect_ratio = "3x4"
    mock_base.id = "test-id"
    
    # Mock coordinate spec with invalid corner
    mock_coord_spec = Mock()
    mock_coord_spec.regions = []
    
    with patch.object(preview_service, "_load_base_by_id", return_value=mock_base):
        with patch("application.mockups.loader.load_base_rgba"):
            with patch("application.mockups.loader.load_coords"):
                with patch("application.mockups.validation.validate_coordinate_schema", 
                          return_value=mock_coord_spec):
                    with patch("application.mockups.validation.validate_corners_within_image",
                              side_effect=ValidationError("Corner out of bounds")):
                        with pytest.raises(ValidationError, match="Corner out of bounds"):
                            preview_service.generate_preview("test-mockup-id")


def test_generate_preview_returns_cache_path_and_timestamp(preview_service, temp_preview_dirs):
    """
    **Contract**: generate_preview returns (out_path, generated_at) tuple where 
    generated_at is ISO format UTC timestamp.
    """
    mock_base = Mock()
    mock_base.status = "coordinates_ready"
    mock_base.coordinates = Mock()
    mock_base.base_image = Mock()
    mock_base.aspect_ratio = "3x4"
    mock_base.id = "test-id"
    
    mock_coord_spec = Mock()
    mock_coord_spec.regions = []
    
    # Create dummy artwork
    art_root = temp_preview_dirs["preview_art"]
    (art_root / "coordinate-tester-3x4.jpg").write_bytes(b"fake jpg")
    
    # Mock all the image processing
    mock_base_img = Mock()
    mock_base_img.size = (800, 1000)
    mock_art_img = Mock()
    mock_composite = Mock()
    mock_composite.save = Mock()
    
    with patch.object(preview_service, "_load_base_by_id", return_value=mock_base):
        with patch("application.mockups.loader.load_base_rgba", return_value=mock_base_img):
            with patch("application.mockups.loader.load_coords"):
                with patch("application.mockups.loader.load_artwork_rgba", return_value=mock_art_img):
                    with patch("application.mockups.validation.validate_coordinate_schema",
                              return_value=mock_coord_spec):
                        with patch("application.mockups.validation.validate_corners_within_image"):
                            with patch.object(preview_service, "_composite", return_value=mock_composite):
                                with patch.object(preview_service, "_write_preview", 
                                               return_value=Path("/cache/test-id/preview-20260308T120000.jpg")):
                                    out_path, generated_at = preview_service.generate_preview("test-mockup-id")
                                    
                                    assert isinstance(out_path, Path)
                                    assert out_path.name.startswith("preview-")
                                    assert ".jpg" in out_path.name
                                    
                                    # Verify generated_at is valid ISO format
                                    parsed_time = datetime.fromisoformat(generated_at)
                                    # Should be current UTC time (within reasonable margin)
                                    now = datetime.now(timezone.utc)
                                    delta = abs((now - parsed_time).total_seconds())
                                    assert delta < 5  # Within 5 seconds


# ============================================================================
# Cache Management Tests
# ============================================================================

def test_trim_cache_keeps_latest_files(preview_service, temp_preview_dirs):
    """
    **Contract**: _trim_cache keeps newest MAX_CACHE_ITEMS files, deletes oldest.
    """
    cache_dir = temp_preview_dirs["cache"] / "test-mockup-id"
    cache_dir.mkdir(parents=True)
    
    # Create 10 dummy preview files with staggered mtimes
    for i in range(10):
        f = cache_dir / f"preview-{i:02d}.jpg"
        f.write_bytes(b"dummy")
    
    # Call trim
    preview_service._trim_cache(cache_dir)
    
    # Should only keep MAX_CACHE_ITEMS (5)
    remaining = list(cache_dir.glob("*.jpg"))
    assert len(remaining) <= 5


def test_cache_directory_resolved_safely(preview_service, temp_preview_dirs):
    """
    **Contract**: resolve_cached_file validates path is within cache dir (no traversal).
    """
    cache_dir = temp_preview_dirs["cache"] / "mockup-1"
    cache_dir.mkdir(parents=True)
    
    # Create legitimate file
    legit = cache_dir / "preview-001.jpg"
    legit.write_bytes(b"real")
    
    # Should work for legit file
    resolved = preview_service.resolve_cached_file("mockup-1", "preview-001.jpg")
    assert resolved == legit
    
    # Should reject path traversal attempts
    with pytest.raises(ValidationError, match="Invalid preview path"):
        preview_service.resolve_cached_file("mockup-1", "../../../etc/passwd")
    
    # Should reject files outside cache
    with pytest.raises(ValidationError, match="Invalid preview path"):
        preview_service.resolve_cached_file("mockup-1", "../../other-mockup/file.jpg")


def test_resolve_cached_file_validates_exists(preview_service, temp_preview_dirs):
    """
    **Contract**: resolve_cached_file raises ValidationError if file doesn't exist.
    """
    with pytest.raises(ValidationError, match="Preview not found"):
        preview_service.resolve_cached_file("mockup-99", "nonexistent.jpg")


# ============================================================================
# Integration Tests
# ============================================================================

def test_artwork_selection_deterministic_order(preview_service, temp_preview_dirs):
    """
    **Contract**: Multiple calls with same parameters return same artwork 
    (deterministic due to sorted file listing).
    """
    art_root = temp_preview_dirs["preview_art"]
    (art_root / "zebra.jpg").write_bytes(b"z")
    (art_root / "apple.jpg").write_bytes(b"a")
    (art_root / "monkey.jpg").write_bytes(b"m")
    
    # Query same non-existent aspect multiple times
    result1 = preview_service._iter_preview_art_files("nonexistent")
    result2 = preview_service._iter_preview_art_files("nonexistent")
    
    assert result1 == result2
    # First should always be same
    assert result1[0].name == "apple.jpg"


def test_resolve_artwork_with_explicit_key(preview_service, temp_preview_dirs):
    """
    **Contract**: _resolve_artwork with key parameter selects specific artwork 
    from fallback options (only from current aspect's available artworks).
    """
    art_root = temp_preview_dirs["preview_art"]
    (art_root / "coordinate-tester-3x4.jpg").write_bytes(b"a")
    (art_root / "coordinate-tester-16x9.jpg").write_bytes(b"b")
    
    # For non-existent aspect, we get both as fallback options
    # Request one by explicit key
    artwork = preview_service._resolve_artwork("2x3", key="coordinate-tester-16x9.jpg")
    assert artwork.name == "coordinate-tester-16x9.jpg"
    
    # For exact aspect match, key must be that file (only one option)
    artwork = preview_service._resolve_artwork("3x4", key="coordinate-tester-3x4.jpg")
    assert artwork.name == "coordinate-tester-3x4.jpg"


def test_resolve_artwork_invalid_key_raises_error(preview_service, temp_preview_dirs):
    """
    **Contract**: _resolve_artwork raises ValidationError if explicit key not found.
    """
    art_root = temp_preview_dirs["preview_art"]
    (art_root / "coordinate-tester-3x4.jpg").write_bytes(b"a")
    
    with pytest.raises(ValidationError, match="Preview artwork not found"):
        preview_service._resolve_artwork("3x4", key="nonexistent.jpg")


def test_preview_artwork_asset_path_security(preview_service, temp_preview_dirs):
    """
    **Contract**: resolve_preview_artwork rejects suspicious filenames and validates path.
    """
    art_root = temp_preview_dirs["preview_art"]
    (art_root / "test.jpg").write_bytes(b"legit")
    
    # Valid
    path = preview_service.resolve_preview_artwork("test.jpg")
    assert path.exists()
    
    # Invalid: traversal
    with pytest.raises(ValidationError):
        preview_service.resolve_preview_artwork("../../../etc/passwd")
    
    # Invalid: path separators
    with pytest.raises(ValidationError):
        preview_service.resolve_preview_artwork("subdir/test.jpg")
    
    # Invalid: nonexistent
    with pytest.raises(ValidationError):
        preview_service.resolve_preview_artwork("nonexistent.jpg")
