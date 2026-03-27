from __future__ import annotations

from flask import Blueprint, render_template

analysis_bp = Blueprint(
    "analysis",
    __name__,
    template_folder="ui/templates",
)


@analysis_bp.get("/rules-reference")
def rules_reference():
    return render_template("etsy_rules_reference.html")
