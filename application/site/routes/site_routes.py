from __future__ import annotations

from pathlib import Path

from flask import Blueprint, render_template


site_bp = Blueprint(
    "site",
    __name__,
    template_folder=str(Path(__file__).resolve().parents[2] / "common" / "ui" / "templates"),
)


@site_bp.get("/about")
def about():
    return render_template("site/about.html", title="About", page_title="About")


@site_bp.get("/manifesto")
def manifesto():
    return render_template("site/manifesto.html", title="The Manifesto", page_title="The Manifesto")


@site_bp.get("/artists")
def artists():
    return render_template("site/artists.html", title="Artists", page_title="Artists")


@site_bp.get("/contact")
def contact():
    return render_template("site/contact.html", title="Contact", page_title="Contact")


@site_bp.get("/resources")
def resources():
    return render_template("site/resources.html", title="Resources", page_title="Resources")


@site_bp.get("/security")
def security():
    return render_template("site/security.html", title="Security", page_title="Security")


@site_bp.get("/privacy")
def privacy():
    return render_template("site/privacy.html", title="Privacy", page_title="Privacy")


@site_bp.get("/terms")
def terms():
    return render_template("site/terms.html", title="Terms", page_title="Terms")


@site_bp.get("/sitemap")
def sitemap():
    return render_template("site/sitemap.html", title="Site Map", page_title="Site Map")
