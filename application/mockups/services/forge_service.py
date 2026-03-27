"""
ArtLomo Studio Forge Service

Background processing engine for generating mockup base images using AI Image API
and processing them with OpenCV to extract 4-point coordinate zones.

Architecture:
- Queue management using ForgeJob database model
- Background worker polling for Pending tasks
- OpenCV-based cyan marker detection (#00FFFF)
- 4-point quad extraction with 4px outward bleed
- V2.0 coordinate schema output
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np

from db import ForgeJob, SessionLocal
from application.mockups.config import MOCKUP_BASES_DIR, STANDARD_MOCKUP_ASPECT_RATIOS

logger = logging.getLogger(__name__)


# =============================================================================
# Queue Management
# =============================================================================


def add_forge_job(category: str, shape_descriptor: str) -> int:
    """
    Add a new ForgeJob to the database queue.

    Args:
        category: Mockup category (e.g., 'living-room', 'bedroom-adults')
        shape_descriptor: Text description of the desired mockup shape/scene

    Returns:
        The ID of the newly created ForgeJob

    Raises:
        ValueError: If category or shape_descriptor is empty
    """
    if not category or not category.strip():
        raise ValueError("Category cannot be empty")
    if not shape_descriptor or not shape_descriptor.strip():
        raise ValueError("Shape descriptor cannot be empty")

    with SessionLocal() as session:
        job = ForgeJob(
            category=category.strip(),
            shape_descriptor=shape_descriptor.strip(),
            status="Pending",
            created_at=datetime.utcnow(),
        )
        session.add(job)
        session.commit()
        session.refresh(job)
        job_id = job.id
        logger.info(f"Forge job {job_id} created: category={category}, descriptor={shape_descriptor}")
        return job_id  # type: ignore[return-value]


def get_pending_jobs(limit: int = 10) -> List[ForgeJob]:
    """
    Retrieve pending ForgeJob records from the database.

    Args:
        limit: Maximum number of jobs to retrieve

    Returns:
        List of ForgeJob instances with status='Pending'
    """
    with SessionLocal() as session:
        jobs = (
            session.query(ForgeJob)
            .filter(ForgeJob.status == "Pending")
            .order_by(ForgeJob.created_at.asc())
            .limit(limit)
            .all()
        )
        # Detach from session to avoid lazy-load errors
        session.expunge_all()
        return jobs


def update_job_status(job_id: int, status: str, error_message: str | None = None) -> None:
    """
    Update the status of a ForgeJob.

    Args:
        job_id: ForgeJob ID
        status: New status (Pending, Generating, Processing, Completed, Failed)
        error_message: Optional error message for Failed status
    """
    with SessionLocal() as session:
        job = session.query(ForgeJob).filter(ForgeJob.id == job_id).first()
        if job:
            job.status = status  # type: ignore[assignment]
            if error_message:
                job.error_message = error_message  # type: ignore[assignment]
            session.commit()
            logger.info(f"Forge job {job_id} status updated to {status}")


# =============================================================================
# OpenCV Cyan Marker Detection
# =============================================================================


def detect_cyan_marker_quad(image_path: Path) -> List[Tuple[float, float]]:
    """
    Detect the cyan (#00FFFF) colored marker region in an image and extract
    the 4-point bounding quad.

    Algorithm:
    1. Load image and convert to HSV color space
    2. Create mask for cyan color (#00FFFF)
    3. Find contours in the mask
    4. Select the largest contour by area
    5. Approximate contour to 4 points (polygon approximation)
    6. Order points as Top-Left, Top-Right, Bottom-Right, Bottom-Left
    7. Apply 4px outward bleed to all points

    Args:
        image_path: Path to the input image file

    Returns:
        List of 4 (x, y) tuples in order: TL, TR, BR, BL

    Raises:
        FileNotFoundError: If image file does not exist
        ValueError: If no cyan marker found or cannot approximate to 4 points
    """
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Load image
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")

    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define cyan color range in HSV
    # Cyan (#00FFFF) in HSV is approximately H=90, S=255, V=255
    # Allow some tolerance for lighting variations
    lower_cyan = np.array([85, 200, 200])
    upper_cyan = np.array([95, 255, 255])

    # Create mask for cyan
    mask = cv2.inRange(hsv, lower_cyan, upper_cyan)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise ValueError("No cyan marker region detected in image")

    # Find the largest contour by area
    largest_contour = max(contours, key=cv2.contourArea)

    # Approximate to 4 points using polygon approximation
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    # Try increasing epsilon if we got more than 4 points
    max_attempts = 10
    for attempt in range(max_attempts):
        if len(approx) == 4:
            break
        epsilon *= 1.2
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    if len(approx) != 4:
        raise ValueError(f"Could not approximate cyan marker to 4 points (got {len(approx)} points)")

    # Extract 4 points as (x, y) tuples
    points = [(float(p[0][0]), float(p[0][1])) for p in approx]  # type: ignore[index]

    # Order points: Top-Left, Top-Right, Bottom-Right, Bottom-Left
    ordered = _order_quad_points(points)

    # Apply 4px outward bleed
    bled = _apply_outward_bleed(ordered, bleed_px=4)

    return bled


def _order_quad_points(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Order 4 points in clockwise order starting from top-left.

    Returns: [TL, TR, BR, BL]
    """
    # Sort by y-coordinate to get top 2 and bottom 2
    sorted_by_y = sorted(points, key=lambda p: p[1])
    top_two = sorted(sorted_by_y[:2], key=lambda p: p[0])
    bottom_two = sorted(sorted_by_y[2:], key=lambda p: p[0])

    tl, tr = top_two
    bl, br = bottom_two

    return [tl, tr, br, bl]


def _apply_outward_bleed(points: List[Tuple[float, float]], bleed_px: float) -> List[Tuple[float, float]]:
    """
    Apply outward bleed to a quad by moving each point away from the centroid.

    Args:
        points: Ordered quad points [TL, TR, BR, BL]
        bleed_px: Bleed distance in pixels

    Returns:
        Bled quad points in the same order
    """
    # Calculate centroid
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)

    bled = []
    for x, y in points:
        # Vector from centroid to point
        dx = x - cx
        dy = y - cy
        # Normalize
        length = (dx * dx + dy * dy) ** 0.5
        if length < 1e-6:
            # Point is at centroid, cannot bleed
            bled.append((x, y))
            continue
        dx /= length
        dy /= length
        # Move point outward by bleed_px
        new_x = x + dx * bleed_px
        new_y = y + dy * bleed_px
        bled.append((new_x, new_y))

    return bled


def save_coordinates_v2(quad_points: List[Tuple[float, float]], output_path: Path) -> None:
    """
    Save quad coordinates to JSON file in v2.0 schema format.

    V2.0 Schema:
    {
        "format_version": "2.0",
        "zones": [
            {
                "points": [
                    {"x": ..., "y": ...},
                    {"x": ..., "y": ...},
                    {"x": ..., "y": ...},
                    {"x": ..., "y": ...}
                ]
            }
        ]
    }

    Args:
        quad_points: List of 4 (x, y) tuples in order TL, TR, BR, BL
        output_path: Path to output JSON file
    """
    if len(quad_points) != 4:
        raise ValueError(f"Expected 4 quad points, got {len(quad_points)}")

    coordinate_data = {
        "format_version": "2.0",
        "zones": [
            {
                "points": [
                    {"x": int(round(x)), "y": int(round(y))} for x, y in quad_points
                ]
            }
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(coordinate_data, f, indent=2)

    logger.info(f"Saved v2.0 coordinates to {output_path}")


# =============================================================================
# Image Processing Workflow
# =============================================================================


def process_forge_image(job_id: int, image_path: Path, aspect_ratio: str, category: str) -> None:
    """
    Process a generated forge image:
    1. Detect cyan marker quad
    2. Extract 4-point coordinates
    3. Save to JSON in v2.0 schema
    4. Move image and JSON to mockup bases directory

    Args:
        job_id: ForgeJob ID
        image_path: Path to the generated image file
        aspect_ratio: Aspect ratio (e.g., '3x4', '1x1')
        category: Category name (e.g., 'living-room')

    Raises:
        ValueError: If processing fails
    """
    try:
        logger.info(f"Processing forge image for job {job_id}: {image_path}")

        # Detect cyan quad
        quad_points = detect_cyan_marker_quad(image_path)

        # Generate output paths
        base_slug = image_path.stem
        target_dir = MOCKUP_BASES_DIR / aspect_ratio / category
        target_dir.mkdir(parents=True, exist_ok=True)

        target_image = target_dir / f"{base_slug}.png"
        target_coords = target_dir / f"{base_slug}.json"

        # Save coordinates
        save_coordinates_v2(quad_points, target_coords)

        # Move/copy image to target location
        if image_path != target_image:
            import shutil
            shutil.copy2(str(image_path), str(target_image))
            logger.info(f"Copied image to {target_image}")

        update_job_status(job_id, "Completed")
        logger.info(f"Forge job {job_id} completed successfully")

    except Exception as exc:
        error_msg = f"Failed to process forge image: {str(exc)}"
        logger.error(f"Job {job_id}: {error_msg}", exc_info=True)
        update_job_status(job_id, "Failed", error_message=error_msg)
        raise ValueError(error_msg) from exc


# =============================================================================
# Background Worker
# =============================================================================


def forge_worker_loop(poll_interval: float = 5.0, max_iterations: int | None = None) -> None:
    """
    Background worker loop that continuously polls for pending ForgeJob tasks.

    Workflow:
    1. Poll database for Pending jobs
    2. For each job:
       a. Update status to Processing
       b. Call AI Image API to generate mockup base (placeholder for now)
       c. Process generated image with OpenCV
       d. Save coordinates and update status to Completed or Failed

    Args:
        poll_interval: Seconds to wait between polling cycles
        max_iterations: Maximum number of polling cycles (None = infinite)

    Note:
        This is a blocking function intended to run as a background service.
        In production, run this via systemd, supervisor, or a container orchestrator.
    """
    logger.info("Forge worker started")
    iteration = 0

    while True:
        if max_iterations is not None and iteration >= max_iterations:
            logger.info(f"Forge worker stopping after {max_iterations} iterations")
            break

        iteration += 1

        try:
            jobs = get_pending_jobs(limit=5)
            if not jobs:
                logger.debug("No pending forge jobs")
                time.sleep(poll_interval)
                continue

            logger.info(f"Processing {len(jobs)} pending forge job(s)")

            for job in jobs:
                try:
                    logger.info(f"Starting forge job {job.id}: category={job.category}, descriptor={job.shape_descriptor}")
                    update_job_status(job.id, "Generating")  # type: ignore[arg-type]

                    # TODO: Replace with actual AI Image API call
                    # For now, this is a placeholder that simulates image generation
                    # generated_image_path = call_ai_image_api(
                    #     prompt=f"Create a mockup base image for {job.shape_descriptor} in {job.category} category "
                    #            f"with a cyan (#00FFFF) rectangular marker indicating the artwork placement zone",
                    #     style="photorealistic",
                    # )
                    #
                    # Placeholder: Assume image is already generated and placed at a known location
                    # Replace this with your actual AI API integration
                    generated_image_path = Path("/tmp/forge_placeholder.png")

                    if not generated_image_path.exists():
                        raise FileNotFoundError(
                            f"AI Image API did not generate file at {generated_image_path}. "
                            "Replace this placeholder with actual API integration."
                        )

                    update_job_status(job.id, "Processing")  # type: ignore[arg-type]

                    # Determine aspect ratio (default to 3x4 for now)
                    # In production, extract aspect from shape_descriptor or add as separate field
                    aspect_ratio = "3x4"
                    if aspect_ratio not in STANDARD_MOCKUP_ASPECT_RATIOS:
                        aspect_ratio = "3x4"

                    # Process image and save coordinates
                    process_forge_image(job.id, generated_image_path, aspect_ratio, job.category)  # type: ignore[arg-type]

                except Exception as exc:
                    error_msg = f"Forge job {job.id} failed: {str(exc)}"
                    logger.error(error_msg, exc_info=True)
                    update_job_status(job.id, "Failed", error_message=error_msg)  # type: ignore[arg-type]

        except Exception as exc:
            logger.error(f"Forge worker error: {str(exc)}", exc_info=True)

        time.sleep(poll_interval)


# =============================================================================
# CLI Entry Point
# =============================================================================


if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    if len(sys.argv) > 1 and sys.argv[1] == "worker":
        logger.info("Starting forge worker in CLI mode")
        forge_worker_loop(poll_interval=5.0)
    else:
        logger.info("ArtLomo Studio Forge Service")
        logger.info("Usage: python forge_service.py worker")
