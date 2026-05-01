from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from application.config import ARTLOMO_FFMPEG_BIN, ARTLOMO_FFPROBE_BIN


def resolve_binary(name: str, override: str) -> tuple[str | None, str]:
    candidate = (override or "").strip()
    if candidate:
        path = Path(candidate).expanduser()
        if path.exists() and path.is_file():
            return str(path), "override"
        return None, f"override-missing:{path}"

    resolved = shutil.which(name)
    if resolved:
        return resolved, "path"

    for fallback in (f"/usr/bin/{name}", f"/usr/local/bin/{name}"):
        path = Path(fallback)
        if path.exists() and path.is_file():
            return str(path), "fallback"

    return None, "not-found"


def version_line(binary_path: str | None) -> str:
    if not binary_path:
        return "unavailable"
    try:
        result = subprocess.run(
            [binary_path, "-hide_banner", "-version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        output = (result.stdout or result.stderr or "").splitlines()
        return output[0].strip() if output else "unavailable"
    except Exception as exc:
        return f"unavailable ({exc})"


def major_family(version_text: str) -> str:
    lower = version_text.lower()
    if "ffmpeg version 5." in lower:
        return "5.x"
    if "ffmpeg version 7." in lower:
        return "7.x"
    return "unknown"


def main() -> int:
    ffmpeg_path, ffmpeg_source = resolve_binary("ffmpeg", ARTLOMO_FFMPEG_BIN)
    ffprobe_path, ffprobe_source = resolve_binary("ffprobe", ARTLOMO_FFPROBE_BIN)

    ffmpeg_version = version_line(ffmpeg_path)
    ffprobe_version = version_line(ffprobe_path)

    print(f"configured_ffmpeg_override={(ARTLOMO_FFMPEG_BIN or '<unset>')}")
    print(f"resolved_ffmpeg_path={(ffmpeg_path or '<missing>')}")
    print(f"resolved_ffmpeg_source={ffmpeg_source}")
    print(f"resolved_ffmpeg_version={ffmpeg_version}")
    print(f"resolved_ffmpeg_family={major_family(ffmpeg_version)}")
    print(f"configured_ffprobe_override={(ARTLOMO_FFPROBE_BIN or '<unset>')}")
    print(f"resolved_ffprobe_path={(ffprobe_path or '<missing>')}")
    print(f"resolved_ffprobe_source={ffprobe_source}")
    print(f"resolved_ffprobe_version={ffprobe_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())