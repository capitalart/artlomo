#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import datetime

# Folder structure snapshot for the new application only.

SCRIPT_DIR = Path(__file__).resolve().parent
# Script lives at application/tools/app-stacks/files; parent[2] is the application root.
APP_ROOT = Path(os.environ.get("APP_ROOT_OVERRIDE", SCRIPT_DIR.parents[2]))
WORKSPACE_ROOT = Path(os.environ.get("WORKSPACE_ROOT_OVERRIDE", APP_ROOT.parent))
STACK_DIR = APP_ROOT / "tools" / "app-stacks" / "stacks"
FILE_PREFIX = os.environ.get("FILE_PREFIX", "application")
STAMP = datetime.now().strftime("%a-%d-%B-%Y-%I-%M-%p").upper()
OUTPUT_NAME = f"{FILE_PREFIX}-folder-structure-{STAMP}.txt"
OUTPUT_PATH = STACK_DIR / OUTPUT_NAME

IGNORE_NAMES = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "backups",
    "tmp",
    "logs",
    "outputs",
    "var",
}
IGNORE_EXTS = {".pyc", ".pyo", ".log", ".tmp"}


def should_skip(entry: Path) -> bool:
    name = entry.name
    if name in IGNORE_NAMES:
        return True
    if entry.suffix in IGNORE_EXTS:
        return True
    rel_to_ws = entry.relative_to(WORKSPACE_ROOT).as_posix() if WORKSPACE_ROOT in entry.parents else name
    rel_to_app = entry.relative_to(APP_ROOT).as_posix() if APP_ROOT in entry.parents else ""
    if rel_to_ws in {
        "application/tools/app-stacks/backups",
        "application/tools/app-stacks/stacks",
        "application/lab/processed",
        "application/lab/unprocessed",
        "application/lab/locked",
    }:
        return True
    if rel_to_app in {"tools/app-stacks/backups", "tools/app-stacks/stacks"}:
        return True
    return False


def build_tree(start: Path, prefix: str = "") -> str:
    lines = []
    try:
        entries = sorted(start.iterdir(), key=lambda p: p.name.lower())
    except PermissionError:
        return ""

    entries = [e for e in entries if not should_skip(e)]
    for idx, entry in enumerate(entries):
        connector = "`-- " if idx == len(entries) - 1 else "|-- "
        lines.append(f"{prefix}{connector}{entry.name}")
        if entry.is_dir():
            extension = "    " if idx == len(entries) - 1 else "|   "
            lines.append(build_tree(entry, prefix + extension))
    return "\n".join([ln for ln in lines if ln])


def main() -> None:
    if not APP_ROOT.exists():
        raise SystemExit(f"Application root not found: {APP_ROOT}")

    STACK_DIR.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        # Application directory tree
        f.write("=== APPLICATION ===\n\n")
        f.write(f"{APP_ROOT.name}\n")
        f.write(build_tree(APP_ROOT))
        f.write("\n\n")

        # Shared common directory tree
        common_dir = WORKSPACE_ROOT / "common"
        if common_dir.exists() and common_dir.is_dir():
            f.write("=== COMMON ===\n\n")
            f.write(f"{common_dir.name}\n")
            f.write(build_tree(common_dir))
            f.write("\n\n")
        
        # Video worker directory tree
        video_worker_dir = WORKSPACE_ROOT / "video_worker"
        if video_worker_dir.exists() and video_worker_dir.is_dir():
            f.write("=== VIDEO WORKER ===\n\n")
            f.write(f"{video_worker_dir.name}\n")
            f.write(build_tree(video_worker_dir))
            f.write("\n\n")
        
        # Tests directory tree
        tests_dir = WORKSPACE_ROOT / "tests"
        if tests_dir.exists() and tests_dir.is_dir():
            f.write("=== TESTS ===\n\n")
            f.write(f"{tests_dir.name}\n")
            f.write(build_tree(tests_dir))
            f.write("\n\n")
        
        # Workspace root files (key files only)
        f.write("=== WORKSPACE ROOT FILES ===\n\n")
        root_files = [
            "db.py", "wsgi.py", "pytest.ini", "requirements.txt", "CHANGELOG.md",
            "README.md", "QUICK-START-GUIDE.md", ".env", ".gitignore",
            ".copilotrules", ".clinerules", ".cursorrules", ".windsurfrules"
        ]
        for filename in root_files:
            filepath = WORKSPACE_ROOT / filename
            if filepath.exists():
                f.write(f"  {filename}\n")

    print(f"Folder structure written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
