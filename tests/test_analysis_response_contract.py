from application.analysis.services.response_contract import validate_analysis_response


def test_validate_analysis_response_accepts_valid_payload() -> None:
    payload = {
        "listing": {
            "title": "Calm Wetland Light",
            "description": "A warm atmospheric landscape narrative for Etsy listing.",
            "tags": ["australian wall art"],
            "materials": ["Digital Download"],
        },
        "metadata": {"source": "openai"},
    }

    result = validate_analysis_response(payload)

    assert result.ok is True
    assert result.reason is None


def test_validate_analysis_response_rejects_failure_marker() -> None:
    payload = {
        "listing": {
            "title": "STATUS: FAILED",
            "description": "ANALYSIS_FAILED\nREASON: model overloaded",
            "tags": ["australian wall art"],
            "materials": ["Digital Download"],
        }
    }

    result = validate_analysis_response(payload)

    assert result.ok is False
    assert "failure marker" in (result.reason or "").lower()


def test_validate_analysis_response_rejects_missing_required_fields() -> None:
    payload = {"listing": {"title": "Only title"}}

    result = validate_analysis_response(payload)

    assert result.ok is False
    assert "missing required listing field" in (result.reason or "").lower()
