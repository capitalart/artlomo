from pathlib import Path

from ...common.utilities.images import generate_thumbnail


def create_thumb(image_bytes: bytes, size: tuple[int, int]) -> bytes:
    return generate_thumbnail(image_bytes, size)


def create_detail_closeup_thumb(src_path: Path, dest_path: Path, size: tuple[int, int] = (500, 500)) -> None:
    """Create a thumbnail for a detail closeup image and persist it."""
    thumb_bytes = generate_thumbnail(src_path.read_bytes(), size)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_bytes(thumb_bytes)
