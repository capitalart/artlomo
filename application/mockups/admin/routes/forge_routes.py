from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import desc

from db import ForgeJob, SessionLocal
from application.mockups.services.forge_service import add_forge_job


forge_bp = Blueprint(
    "forge_admin",
    __name__,
    template_folder="../ui/templates",
    static_folder="../ui/static",
    url_prefix="/admin/forge",
)


@forge_bp.route("/", methods=["GET"])  # type: ignore[misc]
def forge_dashboard():
    return render_template("mockups/forge.html")


@forge_bp.route("/queue", methods=["POST"])  # type: ignore[misc]
def queue_forge_jobs():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"success": False, "message": "Request body must be JSON"}), 400

        category = str(data.get("category", "")).strip()
        shape_descriptor = str(data.get("shape_descriptor", "")).strip()
        quantity_raw = data.get("quantity", 1)

        if not category:
            return jsonify({"success": False, "message": "Field 'category' is required"}), 400
        if not shape_descriptor:
            return jsonify({"success": False, "message": "Field 'shape_descriptor' is required"}), 400

        try:
            quantity = int(quantity_raw)
        except (TypeError, ValueError):
            return jsonify({"success": False, "message": "Field 'quantity' must be an integer"}), 400

        if quantity < 1 or quantity > 50:
            return jsonify({"success": False, "message": "Field 'quantity' must be between 1 and 50"}), 400

        job_ids: list[int] = []
        for _ in range(quantity):
            job_ids.append(add_forge_job(category=category, shape_descriptor=shape_descriptor))

        return jsonify(
            {
                "success": True,
                "message": f"Queued {len(job_ids)} forge job(s)",
                "job_ids": job_ids,
                "count": len(job_ids),
            }
        )
    except Exception as exc:
        return jsonify({"success": False, "message": f"Failed to queue forge jobs: {exc}"}), 500


@forge_bp.route("/status", methods=["GET"])  # type: ignore[misc]
def get_forge_status():
    try:
        with SessionLocal() as session:
            jobs = (
                session.query(ForgeJob)
                .order_by(desc(ForgeJob.created_at))
                .limit(50)
                .all()
            )

            jobs_data = [
                {
                    "id": job.id,
                    "category": job.category,
                    "shape_descriptor": job.shape_descriptor,
                    "status": job.status,
                    "error_message": job.error_message,
                }
                for job in jobs
            ]

        return jsonify(jobs_data)
    except Exception as exc:
        return jsonify({"success": False, "message": f"Failed to retrieve forge status: {exc}"}), 500