"""Analysis Management Admin Routes"""

from __future__ import annotations

import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash

from application.routes.auth_routes import login_required
from application.utils.csrf import require_csrf_or_400
from application.analysis.services import AnalysisPresetService

logger = logging.getLogger(__name__)

analysis_management_bp = Blueprint(
    "analysis_management",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@analysis_management_bp.route("/analysis-management", methods=["GET"])
@login_required
def analysis_management_hub():
    """Analysis Management hub page."""
    presets_openai = AnalysisPresetService.list_presets(provider="openai")
    presets_gemini = AnalysisPresetService.list_presets(provider="gemini")
    
    return render_template(
        "analysis_management_hub.html",
        presets_openai=presets_openai,
        presets_gemini=presets_gemini,
    )


@analysis_management_bp.route("/analysis-management/jobs", methods=["GET"])
@login_required
def analysis_jobs_admin_page():
    """Admin page for listing/canceling queued and historical analysis jobs."""
    return render_template("analysis_jobs_admin.html")


@analysis_management_bp.route("/analysis-management/edit/<provider>/<int:preset_id>", methods=["GET"])
@login_required
def edit_preset(provider: str, preset_id: int):
    """Edit an analysis preset."""
    preset = AnalysisPresetService.get_default_preset(provider) if preset_id == 0 else None
    
    if not preset and preset_id > 0:
        session = __import__("db").SessionLocal()
        try:
            from db import AnalysisPreset
            preset = session.query(AnalysisPreset).filter(
                AnalysisPreset.id == preset_id,
                AnalysisPreset.provider == provider.lower(),
            ).first()
        finally:
            session.close()
    
    if not preset:
        flash("Preset not found", "error")
        return redirect(url_for("analysis_management.analysis_management_hub"))
    
    is_default = preset.is_default
    
    return render_template(
        "analysis_preset_editor.html",
        preset=AnalysisPresetService.to_dict(preset),
        is_default=is_default,
        provider=provider,
    )


@analysis_management_bp.route("/analysis-management/save", methods=["POST"])
@login_required
def save_preset():
    """Save/update an analysis preset."""
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    
    data = request.get_json() or {}
    
    preset_id = data.get("preset_id")
    name = str(data.get("name") or "").strip()
    provider = str(data.get("provider") or "").strip().lower()
    is_default = bool(data.get("is_default"))
    
    system_prompt = str(data.get("system_prompt") or "").strip()
    user_full_prompt = str(data.get("user_full_prompt") or "").strip()
    user_section_prompt = str(data.get("user_section_prompt") or "").strip()
    listing_boilerplate = str(data.get("listing_boilerplate") or "").strip()
    analysis_prompt = str(data.get("analysis_prompt") or "").strip()
    
    if not name or not provider or provider not in ["openai", "gemini"]:
        return jsonify({"status": "error", "message": "Invalid preset data"}), 400
    
    if not all([system_prompt, user_full_prompt, user_section_prompt, analysis_prompt]):
        return jsonify({"status": "error", "message": "All prompt fields are required"}), 400
    
    # Try to get existing preset if editing
    existing_preset = None
    if preset_id:
        session = __import__("db").SessionLocal()
        try:
            from db import AnalysisPreset
            existing_preset = session.query(AnalysisPreset).filter(
                AnalysisPreset.id == preset_id
            ).first()
            if existing_preset and existing_preset.is_default and not is_default:
                return jsonify({"status": "error", "message": "Cannot unset default preset"}), 400
        finally:
            session.close()
    
    saved_preset = AnalysisPresetService.save_preset(
        name=name,
        provider=provider,
        system_prompt=system_prompt,
        user_full_prompt=user_full_prompt,
        user_section_prompt=user_section_prompt,
        listing_boilerplate=listing_boilerplate,
        analysis_prompt=analysis_prompt,
        is_default=is_default,
        preset_id=preset_id,
    )
    
    if not saved_preset:
        return jsonify({"status": "error", "message": "Failed to save preset"}), 500
    
    return jsonify({
        "status": "ok",
        "message": "Preset saved successfully",
        "preset": AnalysisPresetService.to_dict(saved_preset),
    })


@analysis_management_bp.route("/analysis-management/delete/<int:preset_id>", methods=["POST"])
@login_required
def delete_preset(preset_id: int):
    """Delete an analysis preset."""
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp
    
    if not AnalysisPresetService.delete_preset(preset_id):
        return jsonify({"status": "error", "message": "Failed to delete preset"}), 500
    
    return jsonify({"status": "ok", "message": "Preset deleted successfully"})


@analysis_management_bp.route("/analysis-management/export/<int:preset_id>", methods=["GET"])
@login_required
def export_preset(preset_id: int):
    """Export a preset as JSON for download/sharing."""
    session = __import__("db").SessionLocal()
    try:
        from db import AnalysisPreset
        preset = session.query(AnalysisPreset).filter(
            AnalysisPreset.id == preset_id
        ).first()
        
        if not preset:
            return jsonify({"status": "error", "message": "Preset not found"}), 404
        
        preset_dict = AnalysisPresetService.to_dict(preset)
        
        # Remove id and timestamps for export (they'll be regenerated on import)
        export_data = {
            "provider": preset_dict["provider"],
            "name": preset_dict["name"],
            "system_prompt": preset_dict["system_prompt"],
            "user_full_prompt": preset_dict["user_full_prompt"],
            "user_section_prompt": preset_dict["user_section_prompt"],
            "listing_boilerplate": preset_dict["listing_boilerplate"],
            "analysis_prompt": preset_dict["analysis_prompt"],
            "is_default": preset_dict["is_default"],
        }
        
        return jsonify({
            "status": "ok",
            "message": "Preset exported successfully",
            "preset": export_data,
        })
    finally:
        session.close()
