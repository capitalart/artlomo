"""Routes for the manual workflow foundation phase."""

from pathlib import Path

from flask import Blueprint, abort, flash, redirect, render_template, request, send_file, url_for, current_app

from application.utils.csrf import require_csrf_or_400

from ..errors import ManualValidationError, ManualWorkflowError
from ..services import (
    ensure_manual_storage_migrated,
    enqueue_mockups,
    get_manual_asset,
    lock_manual_workspace,
    load_manual_listing,
    promote_unanalysed_to_manual,
    save_manual_metadata,
)
from ..forms import AnalysisForm

manual_bp = Blueprint(
    "manual",
    __name__,
    template_folder="../ui/templates",
    static_folder="../ui/static",
)


@manual_bp.get("/process/<slug>")
def process_get(slug: str):
    return redirect(url_for("manual.workspace", slug=slug))


@manual_bp.post("/process/<slug>")  # type: ignore[misc]
def process(slug: str):
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    try:
        ensure_manual_storage_migrated(slug)
        result = promote_unanalysed_to_manual(slug)
        enqueue_mockups(result.get("manual_slug", slug))
        flash("Manual analysis workspace prepared.", "success")
        target_slug = result.get("manual_slug", slug)
    except ManualWorkflowError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("upload.unprocessed"))
    return redirect(url_for("manual.workspace", slug=target_slug))


@manual_bp.get("/workspace/<slug>")
def workspace(slug: str):
    cfg = current_app.config
    locked_dir = Path(cfg["LAB_LOCKED_DIR"]) / slug
    if locked_dir.exists():
        flash("Artwork is locked and cannot be edited.", "warning")
        return redirect(url_for("upload.locked"))
    try:
        ensure_manual_storage_migrated(slug)
        manual_data = load_manual_listing(slug)
        form = AnalysisForm(data=manual_data)
        # Manually populate seed context fields into form
        if manual_data.get('seed_context'):
            form.location.data = manual_data['seed_context'].get('location')  # type: ignore[attr-defined]
            form.sentiment.data = manual_data['seed_context'].get('sentiment')  # type: ignore[attr-defined]
            form.original_prompt.data = manual_data['seed_context'].get('original_prompt')  # type: ignore[attr-defined]
    except ManualWorkflowError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("upload.unprocessed"))
    from collections import Counter
    import json

    from application.mockups.catalog.loader import load_physical_bases
    from application.mockups.routes.mockup_routes import (
        build_mockup_preflight_for_slug,
        list_mockup_entries_for_slug,
        mockups_dir_has_files_for_slug,
    )
    from application.artwork.services.detail_closeup_service import DetailCloseupService

    preflight = build_mockup_preflight_for_slug(slug)
    mockup_entries = list_mockup_entries_for_slug(slug)
    mockups_have_files = mockups_dir_has_files_for_slug(slug)

    aspect = str(preflight.get("aspect") or "").strip() or None
    bases = load_physical_bases(aspect=aspect) if aspect else []
    counts = Counter([b.category for b in bases if getattr(b, "category", None)])
    categories = sorted(counts.keys())
    category_options = [
        {
            "value": str(cat),
            "label": f"{str(cat).replace('-', ' ').title()} ({int(counts.get(cat) or 0)})",
            "count": int(counts.get(cat) or 0),
        }
        for cat in categories
    ]

    # Load seed context and QC data if available
    processed_root = Path(cfg["LAB_PROCESSED_DIR"])
    processed_dir = processed_root / slug
    seed_context = {}
    qc_doc = {}
    listing_doc = {}
    if processed_dir.exists():
        # SKU extraction (needed for file lookups)
        sku = slug
        # Try SKU-prefixed metadata first, then fall back
        meta_path = processed_dir / f"{slug.lower()}-metadata.json"
        if not meta_path.exists():
            meta_path = processed_dir / "metadata.json"
        if meta_path.exists():
            try:
                meta_doc = json.loads(meta_path.read_text(encoding="utf-8"))
                if isinstance(meta_doc, dict):
                    sku = str(meta_doc.get("sku") or meta_doc.get("artwork_id") or sku).strip() or sku
            except Exception:
                sku = slug
        
        # Now try to load JSON files with SKU prefix
        seed_context_file = processed_dir / "seed_context.json"
        if seed_context_file.exists():
            try:
                with open(seed_context_file, "r") as f:
                    seed_context = json.load(f)
            except Exception:
                seed_context = {}
        
        qc_file = processed_dir / f"{sku.lower()}-qc.json"
        if not qc_file.exists():
            qc_file = processed_dir / "qc.json"
        if qc_file.exists():
            try:
                with open(qc_file, "r") as f:
                    qc_doc = json.load(f)
            except Exception:
                qc_doc = {}
        
        listing_file = processed_dir / f"{sku.lower()}-listing.json"
        if not listing_file.exists():
            listing_file = processed_dir / "listing.json"
        if listing_file.exists():
            try:
                with open(listing_file, "r") as f:
                    listing_doc = json.load(f)
            except Exception:
                listing_doc = {}

    # Asset URLs (for unified template: thumb for UI preview, full-res for modal)
    analyse_name = f"{slug}-ANALYSE.jpg"
    thumb_name = f"{slug}-THUMB.jpg"
    analyse_path = processed_dir / analyse_name
    thumb_path = processed_dir / thumb_name
    analyse_url = url_for('artwork.asset', slug=slug, filename=analyse_name) if analyse_path.exists() else None
    thumb_url = url_for('artwork.asset', slug=slug, filename=thumb_name) if thumb_path.exists() else None

    # Check for detail closeup
    detail_closeup_service = DetailCloseupService(processed_root=processed_root)
    has_detail_closeup = detail_closeup_service.has_detail_closeup(slug)
    detail_closeup_url = None
    detail_closeup_thumb_url = None
    if has_detail_closeup:
        detail_closeup_url = url_for('artwork.detail_closeup_view', slug=slug)
        detail_closeup_thumb_url = url_for('artwork.detail_closeup_thumb', slug=slug)

    # SKU is already extracted above

    # Populate SEO filename if not set
    if not manual_data.get('seo_filename'):
        manual_data['seo_filename'] = manual_data.get('stored_filename') or f"{slug}.jpg"

    return render_template(
        "analysis_workspace.html",
        analysis_source="Manual",
        slug=slug,
        sku=sku,
        listing=listing_doc,
        analysis={},
        qc=qc_doc,
        seed_context=seed_context,
        analyse_url=analyse_url,
        thumb_url=thumb_url,
        has_detail_closeup=has_detail_closeup,
        detail_closeup_url=detail_closeup_url,
        detail_closeup_thumb_url=detail_closeup_thumb_url,
        mockups_preflight=preflight,
        mockup_entries=mockup_entries,
        mockup_category_options=category_options,
    )


@manual_bp.post("/workspace/<slug>")  # type: ignore[misc]
def workspace_post(slug: str):
    form = AnalysisForm()
    action = request.form.get("action", "save")
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    try:
        cfg = current_app.config
        locked_dir = Path(cfg["LAB_LOCKED_DIR"]) / slug
        if locked_dir.exists():
            flash("Artwork is locked and cannot be edited.", "warning")
            return redirect(url_for("upload.locked"))
        ensure_manual_storage_migrated(slug)
        save_manual_metadata(slug, request.form.to_dict())
        if action == "generate_mockups":
            enqueue_mockups(slug)
        if action == "lock":
            lock_manual_workspace(slug)
            flash("Artwork locked and moved to Locked.", "success")
            return redirect(url_for("upload.locked"))
        flash("Manual metadata saved.", "success")
    except ManualValidationError as exc:
        flash(str(exc), "warning")
    except ManualWorkflowError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("manual.workspace", slug=slug))


@manual_bp.get("/asset/<slug>/<path:filename>", endpoint="asset")
def manual_asset(slug: str, filename: str):
    try:
        ensure_manual_storage_migrated(slug)
        asset_path = get_manual_asset(slug, filename)
    except ManualWorkflowError:
        abort(404)
    return send_file(asset_path, as_attachment=False)
