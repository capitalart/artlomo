# Copilot Chunked Undo Toolkit

This toolkit creates safe, file-scoped checkpoints so changes can be undone in
small chunks.

## Files

- `chunk_checkpoint.sh`: Create a checkpoint chunk for specific files.

- `chunk_list.sh`: List all saved chunks.

- `chunk_restore.sh`: Restore a chunk (or dry-run first).

## Why This Is Safe

- Checkpoints are explicit and file-scoped.

- Restore only touches files listed in the chunk manifest.

- Supports `--dry-run` for preview before changing anything.

- Refuses paths outside the repository root.

## Quick Start

1. Create a chunk before editing files:

```bash
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html
```

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text
./application/tools/copilot-undo/chunk_checkpoint.sh stage3-ui \
  application/mockups/admin/routes/forge_routes.py \
  application/mockups/admin/ui/templates/mockups/forge.html

```text

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash

1. Make your edits.

1. Preview restore plan:

```bash
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui
```

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh --dry-run 20260309_143000__stage3-ui

```text

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash

1. Restore the chunk:

```bash
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui
```

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text
./application/tools/copilot-undo/chunk_restore.sh 20260309_143000__stage3-ui

```text

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.

## Notes

- If a file existed at checkpoint time, restore writes the saved backup.

- If a file was missing at checkpoint time, restore deletes it if it now exists.

- Chunks are stored in `.copilot-undo/chunks/` at repository root.
