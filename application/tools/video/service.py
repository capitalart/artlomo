from __future__ import annotations

import json
import shutil
from pathlib import Path
import subprocess
from typing import Optional

from application.mockups import config as mockups_config
from application.video.services.video_service import VideoService as CanonicalVideoService


class VideoService:
    def __init__(self, processed_root: Path):
        self.processed_root = Path(processed_root)

    def _artwork_dir(self, slug: str) -> Path:
        return self.processed_root / slug

    def _master_path(self, slug: str) -> Path:
        """Get path to master image (standardized)."""
        import json
        d = self._artwork_dir(slug)
        
        # 1. Standard: [slug]-MASTER.jpg
        p1 = d / f"{slug}-MASTER.jpg"
        if p1.exists():
            return p1
            
        # 2. SEO Filename (from listing.json)
        # Get SKU from metadata first
        sku = slug
        meta_path = d / f"{slug.lower()}-metadata.json"
        if not meta_path.exists():
            meta_path = d / "metadata.json"
        if meta_path.exists():
            try:
                meta_doc = json.loads(meta_path.read_text(encoding="utf-8"))
                if isinstance(meta_doc, dict):
                    sku = str(meta_doc.get("sku") or meta_doc.get("artwork_id") or sku).strip() or sku
            except Exception:
                pass
        
        # Try SKU-prefixed listing first
        listing_path = d / f"{sku.lower()}-listing.json"
        if not listing_path.exists():
            listing_path = d / "listing.json"
        if listing_path.exists():
            try:
                doc = json.loads(listing_path.read_text(encoding="utf-8"))
                seo_name = doc.get("seo_filename")
                if seo_name:
                    p2 = d / seo_name
                    if p2.exists():
                        return p2
            except Exception:
                pass

        # 3. Legacy: [slug].jpg
        p3 = d / f"{slug}.jpg"
        if p3.exists():
            return p3
            
        return p1

    def _output_path(self, slug: str) -> Path:
        return self._artwork_dir(slug) / f"{slug}_NODE_V1.mp4"

    def _status_path(self, slug: str) -> Path:
        return self._artwork_dir(slug) / "video_status.json"

    def _write_status(self, slug: str, *, status: str, percent: int, stage: str, message: str = "") -> None:
        payload = {
            "status": status,
            "percent": int(max(0, min(100, percent))),
            "stage": stage,
            "message": message,
        }
        path = self._status_path(slug)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")

    def _analyse_path(self, slug: str) -> Path:
        return self._artwork_dir(slug) / f"{slug}-ANALYSE.jpg"

    def _detail_path(self, slug: str) -> Path:
        return self._artwork_dir(slug) / mockups_config.MOCKUPS_SUBDIR / f"{slug}-detail-closeup.jpg"

    def _mockup_paths(self, slug: str, max_count: int = 8) -> list[Path]:
        mockups_dir = self._artwork_dir(slug) / mockups_config.MOCKUPS_SUBDIR
        found: list[Path] = []
        for slot in range(1, max_count + 1):
            path = mockups_dir / f"mu-{slug}-{slot:02d}.jpg"
            if path.exists():
                found.append(path)
        return found

    def _build_motion_expr(self, index: int, frames: int) -> tuple[str, str, str]:
        denom = max(1, frames - 1)
        progress = "on/{f}".format(f=denom)
        # Sub-pixel center zoom for smooth, consistent mockup motion.
        return ("1.00+0.025*{p}".format(p=progress), "(iw-iw/zoom)/2", "(ih-ih/zoom)/2")

    def _master_motion_expr(self, master_path: Path, frames: int) -> tuple[str, str, str]:
        denom = max(1, frames - 1)
        progress = "on/{f}".format(f=denom)
        width, height = self._image_dimensions_via_node(master_path)

        if width > height:
            # Landscape: smooth left-to-right pan.
            return ("1.04", "(iw-iw/zoom)*({p})".format(p=progress), "(ih-ih/zoom)/2")
        if height > width:
            # Portrait: smooth bottom-to-top pan.
            return ("1.04", "(iw-iw/zoom)/2", "(ih-ih/zoom)*(1-{p})".format(p=progress))

        # Square: gentle center zoom.
        return ("1.00+0.20*{p}".format(p=progress), "(iw-iw/zoom)/2", "(ih-ih/zoom)/2")

    def _image_dimensions_via_node(self, image_path: Path) -> tuple[int, int]:
        node_bin = shutil.which("node") or shutil.which("nodejs")
        if not node_bin:
            return (1, 1)
        payload = {
            "action": "read_image_meta",
            "image_path": str(image_path),
        }
        VIDEO_WORKER_DIR = Path(__file__).resolve().parents[2] / "video_worker"
        cmd = [
            node_bin,
            str(VIDEO_WORKER_DIR / "processor.js"),
            json.dumps(payload, ensure_ascii=True, separators=(",", ":")),
        ]
        xvfb_bin = shutil.which("xvfb-run")
        if xvfb_bin:
            cmd = [xvfb_bin, "-a", *cmd]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=60)
            if proc.returncode != 0:
                return (1, 1)
            parsed = json.loads((proc.stdout or "").strip() or "{}")
            width = int(parsed.get("width") or 0)
            height = int(parsed.get("height") or 0)
            if width > 0 and height > 0:
                return (width, height)
        except Exception:
            return (1, 1)
        return (1, 1)

    def _compact_ffmpeg_error(self, raw: str) -> str:
        text = (raw or "").strip()
        if not text:
            return "ffmpeg failed"

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        priority_tokens = (
            "do not match",
            "failed to configure",
            "error reinitializing",
            "invalid argument",
            "nothing was written",
            "could not open encoder",
            "conversion failed",
        )
        for token in priority_tokens:
            for line in reversed(lines):
                if token in line.lower():
                    return line[:400]

        for line in reversed(lines):
            line_lower = line.lower()
            if any(token in line_lower for token in ("error", "failed", "invalid", "nothing was written", "could not")):
                return line[:400]
        return lines[-1][:400]

    def _run_ffmpeg(self, cmd: list[str]) -> tuple[bool, str]:
        ffmpeg_bin = shutil.which("ffmpeg")
        if not ffmpeg_bin:
            try:
                import imageio_ffmpeg  # type: ignore

                ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
            except Exception:
                ffmpeg_bin = None

        if not ffmpeg_bin:
            return (
                False,
                "ffmpeg binary not found. Install ffmpeg system package or ensure imageio-ffmpeg is available.",
            )

        exec_cmd = list(cmd)
        exec_cmd[0] = ffmpeg_bin
        try:
            proc = subprocess.run(exec_cmd, capture_output=True, text=True, check=False)
            if proc.returncode != 0:
                return False, self._compact_ffmpeg_error(proc.stderr or proc.stdout or "ffmpeg failed")
            return True, ""
        except Exception as exc:
            return False, str(exc)

    def generate_promo_video(
        self,
        slug: str,
        duration_seconds: int = 15,
        resolution: tuple[int, int] = (1024, 1024),
        fps: int = 60,
    ) -> Optional[Path]:
        print("\n\n >>> EXECUTING VERIFIED V3 60FPS LOGIC <<< \n\n")
        out_path = self._output_path(slug)
        self._write_status(slug, status="processing", percent=0, stage="initializing", message="Preparing assets")

        canonical = CanonicalVideoService(processed_root=self.processed_root, logs_dir=Path("/srv/artlomo/logs"))
        ok = canonical.generate_kinematic_video(slug)
        if not ok:
            self._write_status(slug, status="error", percent=100, stage="error", message="Video generation failed")
            return None

        self._write_status(slug, status="success", percent=100, stage="complete", message="Video generation complete")
        return out_path if out_path.exists() and out_path.stat().st_size > 0 else None
