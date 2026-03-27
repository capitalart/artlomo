"""Common UI package.

This blueprint exists primarily to provide the `common.static` endpoint used
by templates to reference shared static assets (icons/js/css).
"""

from flask import Blueprint


common_bp = Blueprint(
    "common",
    __name__,
    template_folder="templates",
    static_folder="static",
    # Avoid colliding with the app-level `/static` route.
    static_url_path="/common/static",
)


__all__ = ["common_bp"]
