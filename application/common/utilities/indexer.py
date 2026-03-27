"""Lightweight index updater for the clean-room application tree."""
from pathlib import Path


def update_index(index_path: Path | None = None) -> Path:
    repo_root = Path(__file__).resolve().parents[3]
    app_root = repo_root / "application"
    index_file = index_path or (repo_root / "INDEX.md")

    lines: list[str] = []
    if index_file.exists():
        lines = [line.rstrip("\n") for line in index_file.read_text(encoding="utf-8").splitlines()]
    if not lines:
        lines = ["# Application Index", ""]

    existing = set(lines)
    new_entries: list[str] = []
    for path in sorted(app_root.rglob("*")):
        if path.is_file():
            rel = path.relative_to(repo_root)
            entry = f"- {rel.as_posix()}"
            if entry not in existing:
                new_entries.append(entry)

    if new_entries:
        lines.append("## Auto-added entries")
        lines.extend(new_entries)
        lines.append("")
        index_file.write_text("\n".join(lines), encoding="utf-8")
    return index_file


def main() -> None:
    update_index()


if __name__ == "__main__":
    main()
