from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from db import AnalysisJob, SessionLocal  # noqa: E402


def _artifact_exists_for_slug(slug: str, artifacts_dir: Path | None, processed_dir: Path | None) -> bool:
    slug_clean = str(slug or "").strip()
    if not slug_clean:
        return False

    if artifacts_dir and artifacts_dir.exists():
        direct = artifacts_dir / f"{slug_clean}.json"
        if direct.exists():
            return True

        for cand in [
            artifacts_dir / slug_clean / "analysis.json",
            artifacts_dir / slug_clean / "result.json",
            artifacts_dir / slug_clean / "listing.json",
        ]:
            if cand.exists():
                return True

    if processed_dir and processed_dir.exists():
        for cand in [
            processed_dir / slug_clean / "listing.json",
            processed_dir / slug_clean / "metadata_gemini.json",
            processed_dir / slug_clean / "metadata_openai.json",
            processed_dir / slug_clean / "metadata_manual.json",
        ]:
            if cand.exists():
                return True

    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--artifacts-dir",
        default="/srv/artlomo/data/analysis",
        help="Folder containing analysis JSON artifacts (default: /srv/artlomo/data/analysis)",
    )
    parser.add_argument(
        "--processed-dir",
        default="/srv/artlomo/application/lab/processed",
        help="Fallback folder to check for listing/metadata JSON (default: /srv/artlomo/application/lab/processed)",
    )
    parser.add_argument("--apply", action="store_true", help="Apply updates (default is dry-run)")
    args = parser.parse_args()

    artifacts_dir = Path(args.artifacts_dir).expanduser().resolve()
    processed_dir = Path(args.processed_dir).expanduser().resolve()

    session = SessionLocal()
    try:
        failed = (
            session.query(AnalysisJob)
            .filter(AnalysisJob.status == "FAILED")
            .order_by(AnalysisJob.created_at.desc())
            .all()
        )

        to_fix: list[AnalysisJob] = []
        for job in failed:
            if _artifact_exists_for_slug(str(job.slug), artifacts_dir, processed_dir):  # type: ignore[arg-type]
                to_fix.append(job)

        print(f"FAILED jobs: {len(failed)}")
        print(f"Fixable (artifact exists): {len(to_fix)}")
        if not to_fix:
            return 0

        for job in to_fix[:50]:
            print(f"- slug={job.slug} provider={job.provider} created_at={job.created_at}")
        if len(to_fix) > 50:
            print(f"... ({len(to_fix) - 50} more)")

        if not args.apply:
            print("Dry-run only. Re-run with --apply to update DB statuses.")
            return 0

        for job in to_fix:
            job.status = "PROCESSED"  # type: ignore[misc]
            job.error_message = None  # type: ignore[assignment]

        session.commit()
        print(f"Updated {len(to_fix)} jobs: FAILED -> PROCESSED")
        return 0
    finally:
        session.close()


if __name__ == "__main__":
    raise SystemExit(main())
