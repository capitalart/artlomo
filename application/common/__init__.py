"""Shared `application.common` package.

This layer owns shared UI (templates/static) and domain-friendly helpers.

We expose `common_bp` so the application factory can register it, enabling
`url_for('common.static', ...)` in templates.
"""

from application.common.ui import common_bp

__all__ = ["common_bp"]

