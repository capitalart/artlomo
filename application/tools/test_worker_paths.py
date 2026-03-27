#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from application.app import create_app
from application.video.services.video_service import VideoService


def _run_version(binary_path: str, args: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run([binary_path, *args], capture_output=True, text=True, timeout=15)
    except Exception as exc:  # pylint: disable=broad-except
        return False, f"exec_failed: {exc}"

    output = (result.stdout or "").strip() or (result.stderr or "").strip()
    if result.returncode != 0:
        return False, f"exit={result.returncode} output={output[:300]}"
    return True, output[:300]


def main() -> int:
    app = create_app()
    with app.app_context():
        cfg = app.config
        svc = VideoService(processed_root=Path(cfg["LAB_PROCESSED_DIR"]), logs_dir=Path("/srv/artlomo/logs"))

        node_bin = svc._resolve_binary_path("node") or svc._resolve_binary_path("nodejs")  # pylint: disable=protected-access
        ffmpeg_bin = svc._resolve_binary_path("ffmpeg")  # pylint: disable=protected-access
        xvfb_bin = svc._resolve_binary_path("xvfb-run")  # pylint: disable=protected-access

        print(f"node: {node_bin or 'NOT_FOUND'}")
        print(f"ffmpeg: {ffmpeg_bin or 'NOT_FOUND'}")
        print(f"xvfb-run: {xvfb_bin or 'NOT_FOUND'}")

        ok = True

        if node_bin:
            node_ok, node_msg = _run_version(node_bin, ["--version"])
            print(f"node --version: {'OK' if node_ok else 'FAIL'} :: {node_msg}")
            ok = ok and node_ok
        else:
            print("node --version: FAIL :: node binary not resolved")
            ok = False

        if ffmpeg_bin:
            ff_ok, ff_msg = _run_version(ffmpeg_bin, ["-version"])
            print(f"ffmpeg -version: {'OK' if ff_ok else 'FAIL'} :: {ff_msg}")
            ok = ok and ff_ok
        else:
            print("ffmpeg -version: FAIL :: ffmpeg binary not resolved")
            ok = False

        if xvfb_bin:
            xv_ok, xv_msg = _run_version(xvfb_bin, ["--help"])
            print(f"xvfb-run --help: {'OK' if xv_ok else 'FAIL'} :: {xv_msg}")
            ok = ok and xv_ok
        else:
            print("xvfb-run --help: SKIP :: xvfb-run not resolved")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
