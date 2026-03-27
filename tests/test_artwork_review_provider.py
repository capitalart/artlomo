import json
from pathlib import Path


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_gemini_review_prefers_gemini_metadata(app, app_client):
    slug = "rjc-1000"
    sku = "RJC-1000"
    processed_dir = Path(app.config["LAB_PROCESSED_DIR"]) / slug
    processed_dir.mkdir(parents=True, exist_ok=True)

    _write_json(processed_dir / f"{sku.lower()}-metadata.json", {"sku": sku})
    _write_json(processed_dir / f"{sku.lower()}-listing.json", {"slug": slug, "sku": sku})
    _write_json(
        processed_dir / f"{sku.lower()}-metadata_gemini.json",
        {
            "source": "gemini",
            "analysis": {
                "etsy_title": "Gemini Specific Title",
                "description": "Gemini specific description body",
                "tags": ["gemini", "specific", "tag"],
            },
        },
    )
    _write_json(
        processed_dir / f"{sku.lower()}-metadata_openai.json",
        {
            "source": "openai",
            "analysis": {
                "etsy_title": "OpenAI Title Should Not Render",
                "description": "OpenAI description",
                "tags": ["openai", "tag"],
            },
        },
    )

    resp = app_client.get(f"/artwork/{slug}/review/gemini")
    assert resp.status_code == 200

    html = resp.get_data(as_text=True)
    assert "Gemini Specific Title" in html
    assert "OpenAI Title Should Not Render" not in html
