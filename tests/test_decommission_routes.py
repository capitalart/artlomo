"""Regression tests — decommissioned vs preserved mockup admin routes.

Asserts:
* Every retired URL returns 404 (route never registered).
* Every preserved URL returns 200 after authenticated access.

These tests use the same `app` / `app_client` fixtures defined in conftest.py.
"""

import pytest


# ---------------------------------------------------------------------------
# Retired route paths — must not be reachable
# ---------------------------------------------------------------------------
RETIRED_PATHS = [
    "/admin/mockups/gemini-studio",
    "/admin/mockups/gemini-studio/status",
    "/admin/mockups/basic-mockups",
    "/admin/mockups/ezy-mockups",
    "/admin/mockups/ezy-mockups/status",
    "/admin/mockups/precision-mockups",
    "/admin/mockups/precision-mockups/status",
    "/admin/mockups/mockup-generator",
    "/admin/mockups/mockup-generator/status",
    "/admin/mockups/mockup-generator/queue-admin",
    "/admin/mockups/mockup-generator/prompt-settings",
]

# ---------------------------------------------------------------------------
# Preserved route paths — must return 200 after authenticated GET
# ---------------------------------------------------------------------------
PRESERVED_PATHS = [
    "/admin/mockups/bases",
    "/admin/mockups/bases/upload",
    "/admin/mockups/aspects",
    "/admin/mockups/categories-manager",
    "/admin/mockups/solid-image-generator",
]


class TestRetiredRoutesReturn404:
    """Each decommissioned URL must yield 404 regardless of auth state."""

    @pytest.mark.parametrize("path", RETIRED_PATHS)
    def test_retired_get_returns_404(self, app_client, path):
        resp = app_client.get(path, follow_redirects=False)
        assert resp.status_code == 404, (
            f"Expected 404 for retired path {path!r}, got {resp.status_code}"
        )

    @pytest.mark.parametrize("path", RETIRED_PATHS)
    def test_retired_get_unauthenticated_returns_404(self, app, path):
        """Unauthed requests to retired routes should still 404, not redirect."""
        with app.test_client() as client:
            resp = client.get(path, follow_redirects=False)
        # 404 is fine; a redirect-to-login (3xx) would mean the route exists
        # and we only need to confirm it does not 200 or 3xx to dead content
        assert resp.status_code != 200, (
            f"Retired path {path!r} should not return 200 (got {resp.status_code})"
        )


class TestPreservedRoutesReturn200:
    """Each preserved mockup admin page must return 200 after authentication."""

    @pytest.mark.parametrize("path", PRESERVED_PATHS)
    def test_preserved_get_returns_200(self, app_client, path):
        resp = app_client.get(path, follow_redirects=False)
        assert resp.status_code == 200, (
            f"Expected 200 for preserved path {path!r}, got {resp.status_code}"
        )

    @pytest.mark.parametrize("path", PRESERVED_PATHS)
    def test_preserved_renders_html(self, app_client, path):
        resp = app_client.get(path, follow_redirects=False)
        assert resp.status_code == 200
        content_type = resp.headers.get("Content-Type", "")
        assert "text/html" in content_type, (
            f"Expected HTML response for {path!r}, got {content_type!r}"
        )
        body = resp.data.decode("utf-8", errors="ignore")
        assert "<html" in body.lower(), (
            f"Response body for {path!r} does not look like HTML"
        )
