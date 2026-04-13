# Artwork Placeholder Routes

This blueprint provides navigation-only placeholder pages for future workflows. No business logic is implemented.

## Routes

- `/artwork/<slug>/analysis/openai`

- `/artwork/<slug>/analysis/gemini`

- `/artwork/<slug>/analysis/manual`

- `/artwork/<slug>/review`

- `/artwork/<slug>/delete` (confirmation only, no deletion)

All pages render placeholders showing the artwork slug and a not-implemented notice.

## Files

- `routes/artwork_routes.py` — Blueprint registering placeholder routes.

- `ui/templates/artwork_placeholder.html` — Generic placeholder page for analysis/review routes.

- `ui/templates/delete_confirm.html` — Confirmation placeholder; no-op actions.

## Notes

- Styling and layout use shared base template and global containers.

- No business logic runs; these are navigation scaffolds only.
