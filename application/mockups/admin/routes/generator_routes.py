"""Solid colour image utility — Flask routes for the solid image generator.

The Mockup Generator Dashboard and Queue Admin routes that formerly lived in this
module were decommissioned.  Only the utility blueprint (``utility_bp``) remains.
"""

from __future__ import annotations

import logging

from flask import Blueprint, abort, flash, render_template, request, send_file

from application.mockups.config import MockupBaseGenerationCatalog
from application.mockups.services.solid_image_service import (
    SolidImageGenerationError,
    SolidImageService,
    SolidImageValidationError,
)


logger = logging.getLogger(__name__)

utility_bp = Blueprint(
    "utility",
    __name__,
    template_folder="../ui/templates",
    static_folder="../ui/static",
)


# ============================================================================
# Solid Image Utility Routes
# ============================================================================


@utility_bp.route("/solid-image-generator", methods=["GET"])
def solid_image_generator_form():
    """Display the solid image generator form.

    Provides:
    - Dropdown for 13 aspect ratios
    - HTML5 color picker (default #00FFFF)
    - Form submission to download generated image
    """
    try:
        return render_template(
            "mockups/solid_image_generator.html",
            aspect_ratios=MockupBaseGenerationCatalog.ASPECT_RATIOS,
            default_color="00FFFF",
        )
    except Exception as e:
        logger.error(f"Error rendering solid image form: {str(e)}", exc_info=True)
        flash("Error rendering form. Check server logs.", "error")
        abort(500)


@utility_bp.route("/solid-image-generator", methods=["POST"])
def solid_image_generator_download():
    """Process form submission and return solid image for download.

    Expected POST data:
    - aspect_ratio: One of the 13 standard aspect ratios (e.g., "16:9")
    - color: Hex color code (e.g., "00FFFF" or "#00FFFF")

    Returns:
        PNG image file for download
    """
    try:
        # Get form parameters
        aspect_ratio_key = request.form.get("aspect_ratio", "")
        color_input = request.form.get("color", SolidImageService.DEFAULT_COLOR)

        # Normalize color to remove # if present 
        if color_input.startswith("#"):
            color_input = color_input[1:]

        # Validate aspect ratio
        if aspect_ratio_key not in MockupBaseGenerationCatalog.ASPECT_RATIOS:
            flash(f"Invalid aspect ratio: {aspect_ratio_key}", "error")
            return render_template(
                "mockups/solid_image_generator.html",
                aspect_ratios=MockupBaseGenerationCatalog.ASPECT_RATIOS,
                default_color=color_input,
            ), 400

        # Convert aspect ratio from "XxY" format to "X:Y" format for service
        aspect_ratio_colon = aspect_ratio_key.replace("x", ":")

        logger.info(
            f"Generating solid image: aspect_ratio={aspect_ratio_colon}, "
            f"color={color_input}"
        )

        try:
            # Generate image to BytesIO (in-memory)
            image_buffer = SolidImageService.generate_solid_image(
                aspect_ratio=aspect_ratio_colon,
                color=f"#{color_input}",
                output_path=None,  # Return as BytesIO, not saved to disk
            )

            # Send to client as download
            filename = f"solid_{aspect_ratio_key}_{color_input}.png"
            return send_file(
                image_buffer,
                mimetype="image/png",
                as_attachment=True,
                download_name=filename,
            )

        except (SolidImageValidationError, SolidImageGenerationError) as e:
            logger.error(f"Image generation error: {str(e)}")
            flash(f"Image generation error: {str(e)}", "error")
            return render_template(
                "mockups/solid_image_generator.html",
                aspect_ratios=MockupBaseGenerationCatalog.ASPECT_RATIOS,
                default_color=color_input,
            ), 400

    except Exception as e:
        logger.error(f"Error processing solid image request: {str(e)}", exc_info=True)
        flash("Error processing request. Check server logs.", "error")
        abort(500)
