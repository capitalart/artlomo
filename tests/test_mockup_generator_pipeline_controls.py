from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest
from celery.exceptions import Retry
from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Base, MockupBaseGenerationJob
import application.mockups.admin.routes.generator_routes as generator_routes
import application.mockups.tasks_mockup_generator as tasks_module


def _build_test_session_factory(tmp_path: Path):
    engine = create_engine(
        f"sqlite:///{(tmp_path / 'pipeline-controls.sqlite3').as_posix()}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_start_pipeline_dispatches_pending_jobs(app_client, monkeypatch, tmp_path):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(generator_routes, "SessionLocal", session_factory)
    monkeypatch.setattr(generator_routes, "_load_control_state", lambda: {"state": "running"})

    dispatched_job_ids: list[int] = []
    monkeypatch.setattr(
        tasks_module.process_mockup_job,
        "delay",
        lambda job_id: dispatched_job_ids.append(job_id),
    )

    response = app_client.post(
        "/admin/mockups/mockup-generator/start-pipeline",
        json={
            "mode": "aspect_and_category",
            "aspect_ratio": "1x1",
            "category": "living-room",
            "quantity": 1,
        },
        headers={"X-CSRFToken": app_client.csrf_token},
    )

    assert response.status_code == 202
    payload = response.get_json()
    assert payload["created"] == 1
    assert payload["dispatched"] == 1
    assert payload["pending_jobs"] == 1
    assert len(dispatched_job_ids) == 1


def test_start_pipeline_trojan_mode_creates_mode_specific_job_identity(app_client, monkeypatch, tmp_path):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(generator_routes, "SessionLocal", session_factory)
    monkeypatch.setattr(generator_routes, "_load_control_state", lambda: {"state": "running"})

    dispatched_job_ids: list[int] = []
    monkeypatch.setattr(
        tasks_module.process_mockup_job,
        "delay",
        lambda job_id: dispatched_job_ids.append(job_id),
    )

    response = app_client.post(
        "/admin/mockups/mockup-generator/start-pipeline",
        json={
            "mode": "aspect_and_category",
            "aspect_ratio": "1x1",
            "category": "living-room",
            "quantity": 1,
            "placeholder_mode": "artwork_trojan",
        },
        headers={"X-CSRFToken": app_client.csrf_token},
    )

    assert response.status_code == 202
    payload = response.get_json()
    assert payload["generation_mode"] == "artwork_trojan"
    assert payload["placeholder_mode"] == "artwork_trojan"
    assert payload["created"] == 1
    assert payload["dispatched"] == 1

    session = session_factory()
    rows = session.query(MockupBaseGenerationJob).all()
    assert len(rows) == 1
    assert str(cast(Any, rows[0]).generation_mode) == "artwork_trojan"
    assert str(cast(Any, rows[0]).job_id).endswith("__artwork_trojan")
    session.close()


def test_start_pipeline_plain_composite_creates_mode_specific_job_identity(app_client, monkeypatch, tmp_path):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(generator_routes, "SessionLocal", session_factory)
    monkeypatch.setattr(generator_routes, "_load_control_state", lambda: {"state": "running"})

    dispatched_job_ids: list[int] = []
    monkeypatch.setattr(
        tasks_module.process_mockup_job,
        "delay",
        lambda job_id: dispatched_job_ids.append(job_id),
    )

    response = app_client.post(
        "/admin/mockups/mockup-generator/start-pipeline",
        json={
            "mode": "aspect_and_category",
            "aspect_ratio": "5x7",
            "category": "meeting-room",
            "quantity": 1,
            "placeholder_mode": "artwork_only_composite",
        },
        headers={"X-CSRFToken": app_client.csrf_token},
    )

    assert response.status_code == 202
    payload = response.get_json()
    assert payload["generation_mode"] == "artwork_only_composite"
    assert payload["placeholder_mode"] == "artwork_only_composite"
    assert payload["created"] == 1
    assert payload["dispatched"] == 1

    session = session_factory()
    rows = session.query(MockupBaseGenerationJob).all()
    assert len(rows) == 1
    assert str(cast(Any, rows[0]).generation_mode) == "artwork_only_composite"
    assert str(cast(Any, rows[0]).job_id).endswith("__artwork_only_composite")
    session.close()


def test_start_pipeline_raw_prompt_only_forces_artwork_only_composite_mode(app_client, monkeypatch, tmp_path):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(generator_routes, "SessionLocal", session_factory)
    monkeypatch.setattr(generator_routes, "_load_control_state", lambda: {"state": "running"})

    dispatched_job_ids: list[int] = []
    monkeypatch.setattr(
        tasks_module.process_mockup_job,
        "delay",
        lambda job_id: dispatched_job_ids.append(job_id),
    )

    response = app_client.post(
        "/admin/mockups/mockup-generator/start-pipeline",
        json={
            "mode": "aspect_and_category",
            "aspect_ratio": "2x3",
            "category": "cafe",
            "quantity": 1,
            "placeholder_mode": "artwork_trojan",
            "raw_prompt_only_enabled": True,
            "raw_prompt_text": "please generate a square image of a mockup of this 2:3 aspect ratio artwork in an office",
        },
        headers={"X-CSRFToken": app_client.csrf_token},
    )

    assert response.status_code == 202
    payload = response.get_json()
    assert payload["generation_mode"] == "artwork_only_composite"
    assert payload["raw_prompt_only_enabled"] is True
    assert payload["dispatched"] == 1

    session = session_factory()
    rows = session.query(MockupBaseGenerationJob).all()
    assert len(rows) == 1
    assert str(cast(Any, rows[0]).generation_mode) == "artwork_only_composite"
    session.close()


def test_control_endpoint_sets_skip_coordinate_detection(app_client, monkeypatch):
    monkeypatch.setattr(generator_routes, "_load_control_state", lambda: {"state": "running"})

    saved_args: dict[str, object] = {}

    def _fake_save_control_state(state, message, **kwargs):
        saved_args.update({"state": state, "message": message, **kwargs})
        return {
            "state": str(state),
            "message": str(message),
            "max_retries": "3",
            "placeholder_mode": "artwork_trojan",
            "skip_coordinate_detection": "true" if bool(kwargs.get("skip_coordinate_detection")) else "false",
            "updated_at": "",
        }

    monkeypatch.setattr(generator_routes, "_save_control_state", _fake_save_control_state)

    response = app_client.post(
        "/admin/mockups/mockup-generator/control",
        json={
            "action": "set_skip_coordinate_detection",
            "skip_coordinate_detection": True,
        },
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["control_state"]["skip_coordinate_detection"] == "true"
    assert bool(saved_args.get("skip_coordinate_detection")) is True


def test_process_job_cleans_generated_image_when_coordinate_extraction_fails(
    monkeypatch,
    tmp_path,
):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(tasks_module, "SessionLocal", session_factory)
    monkeypatch.setattr(tasks_module, "_load_control_state", lambda: {"state": "running"})

    session = session_factory()
    job = MockupBaseGenerationJob(
        job_id="mbg_1x1_living-room_v1",
        aspect_ratio="1x1",
        category="living-room",
        variation_index=1,
        status="Pending",
        stage="Queued",
        attempts=0,
    )
    session.add(job)
    session.commit()
    job_id = job.id
    session.close()

    output_path = tmp_path / "generated.png"

    class _FakeGeminiImageService:
        def generate_image(self, prompt, aspect_ratio, category, variation_index, generation_aspect_ratio=None, **kwargs):
            output_path.write_bytes(b"png-bytes")
            return str(output_path)

    monkeypatch.setattr(tasks_module, "GeminiImageService", _FakeGeminiImageService)
    monkeypatch.setattr(tasks_module.MockupPromptService, "generate_prompt", lambda **kwargs: "prompt")
    monkeypatch.setattr(tasks_module, "_register_generated_base", lambda **kwargs: "base-1")
    monkeypatch.setattr(
        tasks_module.MockupCoordinateService,
        "extract_coordinates",
        lambda image_path: (_ for _ in ()).throw(tasks_module.CyanQuadNotFoundError("no cyan quad")),
    )

    result = tasks_module.process_mockup_job.run(job_id)

    assert result["status"] == "failed"
    assert not output_path.exists()

    session = session_factory()
    refreshed_job = session.get(MockupBaseGenerationJob, job_id)
    assert refreshed_job is not None
    assert str(cast(Any, refreshed_job).status) == "Failed"
    assert cast(Any, refreshed_job).generated_image_path is None
    assert cast(Any, refreshed_job).coordinates_path is None
    session.close()


def test_process_job_stop_after_image_generation_cleans_outputs_and_resets_pending(
    monkeypatch,
    tmp_path,
):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(tasks_module, "SessionLocal", session_factory)

    control_states = iter([
        {"state": "running"},
        {"state": "stopped"},
    ])
    monkeypatch.setattr(tasks_module, "_load_control_state", lambda: next(control_states))

    session = session_factory()
    job = MockupBaseGenerationJob(
        job_id="mbg_4x5_cafe_v1",
        aspect_ratio="4x5",
        category="cafe",
        variation_index=1,
        status="Pending",
        stage="Queued",
        attempts=0,
    )
    session.add(job)
    session.commit()
    job_id = job.id
    session.close()

    output_path = tmp_path / "stopped-generated.png"

    class _FakeGeminiImageService:
        def generate_image(self, prompt, aspect_ratio, category, variation_index, generation_aspect_ratio=None, **kwargs):
            output_path.write_bytes(b"png-bytes")
            return str(output_path)

    monkeypatch.setattr(tasks_module, "GeminiImageService", _FakeGeminiImageService)
    monkeypatch.setattr(tasks_module.MockupPromptService, "generate_prompt", lambda **kwargs: "prompt")
    monkeypatch.setattr(tasks_module, "_register_generated_base", lambda **kwargs: "base-1")
    monkeypatch.setattr(
        tasks_module.MockupCoordinateService,
        "extract_coordinates",
        lambda image_path: [{"x": 0, "y": 0}],
    )

    result = tasks_module.process_mockup_job.run(job_id)

    assert result["status"] == "stopped"
    assert not output_path.exists()

    session = session_factory()
    refreshed_job = session.get(MockupBaseGenerationJob, job_id)
    assert refreshed_job is not None
    assert str(cast(Any, refreshed_job).status) == "Pending"
    assert str(cast(Any, refreshed_job).stage) == "StoppedAfterImageGeneration"
    assert cast(Any, refreshed_job).generated_image_path is None
    assert cast(Any, refreshed_job).coordinates_path is None
    session.close()


def test_process_job_fails_after_retry_when_border_not_detected(
    monkeypatch,
    tmp_path,
):
    """Verifies that a CompositeCyanContourNotFoundError fails the job after retry attempts."""
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(tasks_module, "SessionLocal", session_factory)
    monkeypatch.setattr(tasks_module, "_load_control_state", lambda: {"state": "running"})

    session = session_factory()
    job = MockupBaseGenerationJob(
        job_id="mbg_1x1_living-room_v1",
        aspect_ratio="1x1",
        category="living-room",
        variation_index=1,
        status="Pending",
        stage="Queued",
        attempts=0,
    )
    session.add(job)
    session.commit()
    job_id = job.id
    session.close()

    output_path = tmp_path / "generated-no-border.png"
    generate_call_count = {"count": 0}

    class _FakeGeminiImageService:
        last_placeholder_mode = tasks_module.GENERATION_MODE_ARTWORK_TROJAN
        last_reference_guide_path = "/fake/guide.png"

        def generate_image(self, prompt, aspect_ratio, category, variation_index, generation_aspect_ratio=None, **kwargs):
            generate_call_count["count"] += 1
            output_path.write_bytes(b"png-bytes")
            return str(output_path)

    monkeypatch.setattr(tasks_module, "GeminiImageService", _FakeGeminiImageService)
    monkeypatch.setattr(
        tasks_module.CompositeCoordinateService,
        "extract_coordinates_and_erase",
        lambda image_path: (_ for _ in ()).throw(
            tasks_module.CompositeCyanContourNotFoundError("No cyan fiducial ring detected.")
        ),
    )

    result = tasks_module.process_mockup_job.run(job_id)

    assert result["status"] == "failed"
    assert result["error_type"] == "CompositeCyanContourNotFoundError"
    assert "No cyan fiducial ring detected" in result["error"]
    # One generation per retry attempt.
    assert generate_call_count["count"] == tasks_module.MAX_CYAN_REGEN_ATTEMPTS
    # Generated image cleaned up on failure.
    assert not output_path.exists()

    session = session_factory()
    refreshed_job = session.get(MockupBaseGenerationJob, job_id)
    assert refreshed_job is not None
    assert str(cast(Any, refreshed_job).status) == "Failed"
    assert cast(Any, refreshed_job).generated_image_path is None
    assert cast(Any, refreshed_job).coordinates_path is None
    session.close()


def test_process_job_skips_coordinate_detection_when_control_enabled(monkeypatch, tmp_path):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(tasks_module, "SessionLocal", session_factory)
    monkeypatch.setattr(tasks_module, "_load_control_state", lambda: {"state": "running", "skip_coordinate_detection": "true"})

    session = session_factory()
    job = MockupBaseGenerationJob(
        job_id="mbg_1x1_living-room_v1__artwork_trojan",
        aspect_ratio="1x1",
        category="living-room",
        variation_index=1,
        generation_mode="artwork_trojan",
        status="Pending",
        stage="Queued",
        attempts=0,
    )
    session.add(job)
    session.commit()
    job_id = job.id
    session.close()

    output_path = tmp_path / "generated-skip-detection.png"
    guide_path = tmp_path / "1x1-outlined-artwork.png"
    Image.new("RGB", (256, 256), (0, 255, 255)).save(guide_path, format="PNG")

    class _FakeGeminiImageService:
        last_placeholder_mode = tasks_module.GENERATION_MODE_ARTWORK_TROJAN
        last_reference_guide_path = str(guide_path)

        def generate_image(self, prompt, aspect_ratio, category, variation_index, generation_aspect_ratio=None, **kwargs):
            Image.new("RGB", (512, 512), (170, 170, 170)).save(output_path, format="PNG")
            return str(output_path)

    extract_call_count = {"count": 0}

    def _fail_if_called(image_path):
        extract_call_count["count"] += 1
        raise AssertionError("extract_coordinates_and_erase should not be called when skip_coordinate_detection=true")

    monkeypatch.setattr(tasks_module, "GeminiImageService", _FakeGeminiImageService)
    monkeypatch.setattr(tasks_module, "_resolve_trojan_reference_artwork_path", lambda aspect_ratio: guide_path)
    monkeypatch.setattr(tasks_module.CompositeCoordinateService, "extract_coordinates_and_erase", _fail_if_called)
    monkeypatch.setattr(tasks_module, "_register_generated_base", lambda **kwargs: "base-skip-detection")

    result = tasks_module.process_mockup_job.run(job_id)

    assert result["status"] == "completed"
    assert result["coordinates_source"] == "fallback"
    assert len(result["coordinates"]) == 4
    assert extract_call_count["count"] == 0


def test_process_job_requeues_after_gemini_rate_limit(monkeypatch, tmp_path):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(tasks_module, "SessionLocal", session_factory)
    monkeypatch.setattr(tasks_module, "_load_control_state", lambda: {"state": "running"})

    session = session_factory()
    job = MockupBaseGenerationJob(
        job_id="mbg_5x4_music-room_v1",
        aspect_ratio="5x4",
        category="music-room",
        variation_index=1,
        status="Pending",
        stage="Queued",
        attempts=0,
    )
    session.add(job)
    session.commit()
    job_id = job.id
    session.close()

    class _FakeGeminiImageService:
        def generate_image(self, prompt, aspect_ratio, category, variation_index, generation_aspect_ratio=None, **kwargs):
            raise tasks_module.GeminiRateLimitError(
                "Gemini API quota exceeded. Retry after approximately 22s.",
                retry_after_seconds=22,
            )

    retry_calls: list[dict[str, int]] = []

    def _fake_retry(*, exc, countdown, max_retries):
        retry_calls.append({"countdown": countdown, "max_retries": max_retries})
        raise Retry()

    monkeypatch.setattr(tasks_module, "GeminiImageService", _FakeGeminiImageService)
    monkeypatch.setattr(tasks_module.MockupPromptService, "generate_prompt", lambda **kwargs: "prompt")
    monkeypatch.setattr(tasks_module, "_register_generated_base", lambda **kwargs: "base-1")
    monkeypatch.setattr(tasks_module.process_mockup_job, "retry", _fake_retry)

    with pytest.raises(Retry):
        tasks_module.process_mockup_job.run(job_id)

    assert len(retry_calls) == 1
    assert retry_calls[0]["countdown"] >= 22
    assert retry_calls[0]["max_retries"] == tasks_module.MOCKUP_GEMINI_RATE_LIMIT_MAX_RETRIES

    session = session_factory()
    refreshed_job = session.get(MockupBaseGenerationJob, job_id)
    assert refreshed_job is not None
    assert str(cast(Any, refreshed_job).status) == "Pending"
    assert str(cast(Any, refreshed_job).stage) == "RetryQueued"
    assert str(cast(Any, refreshed_job).reason) == "GeminiRateLimitError"
    assert "Scheduled retry" in str(cast(Any, refreshed_job).error_message)
    session.close()


def test_queue_mockup_jobs_creates_parallel_artwork_trojan_jobs(monkeypatch, tmp_path):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(tasks_module, "SessionLocal", session_factory)
    monkeypatch.setattr(tasks_module.MockupBaseGenerationCatalog, "ASPECT_RATIOS", ("1x1",))
    monkeypatch.setattr(tasks_module.MockupBaseGenerationCatalog, "CATEGORIES", ("cafe",))
    monkeypatch.setattr(tasks_module.MockupBaseGenerationCatalog, "VARIATION_MIN_INDEX", 1)
    monkeypatch.setattr(tasks_module.MockupBaseGenerationCatalog, "VARIATION_MAX_INDEX", 1)

    session = session_factory()
    session.add(
        MockupBaseGenerationJob(
            job_id="mbg_1x1_cafe_v1",
            aspect_ratio="1x1",
            category="cafe",
            variation_index=1,
            generation_mode="standard",
            status="Completed",
            stage="Completed",
            attempts=1,
        )
    )
    session.commit()
    session.close()

    result = tasks_module.queue_mockup_jobs.run(mode="artwork_trojan")

    assert result == {
        "expected_total": 1,
        "existing_before": 0,
        "created": 1,
        "final_total": 1,
    }

    session = session_factory()
    trojan_job = session.query(MockupBaseGenerationJob).filter_by(generation_mode="artwork_trojan").one()
    assert str(cast(Any, trojan_job).job_id) == "mbg_1x1_cafe_v1__artwork_trojan"
    assert str(cast(Any, trojan_job).status) == "Pending"
    session.close()


def test_process_job_artwork_trojan_uses_reference_override_and_composite_service(
    monkeypatch,
    tmp_path,
):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(tasks_module, "SessionLocal", session_factory)
    monkeypatch.setattr(tasks_module, "_load_control_state", lambda: {"state": "running"})

    session = session_factory()
    job = MockupBaseGenerationJob(
        job_id="mbg_1x1_cafe_v1__artwork_trojan",
        aspect_ratio="1x1",
        category="cafe",
        variation_index=1,
        generation_mode="artwork_trojan",
        status="Pending",
        stage="Queued",
        attempts=0,
    )
    session.add(job)
    session.commit()
    job_id = job.id
    session.close()

    output_path = tmp_path / "trojan-generated.png"
    trojan_reference_path = tmp_path / "1x1.jpg"
    trojan_reference_path.write_bytes(b"reference")
    generated_calls: list[dict[str, object]] = []

    class _FakeGeminiImageService:
        def __init__(self):
            self.last_placeholder_mode = "artwork_trojan"
            self.last_reference_guide_path = str(trojan_reference_path)

        def generate_image(
            self,
            prompt,
            aspect_ratio,
            category,
            variation_index,
            generation_aspect_ratio=None,
            reference_guide_override=None,
            placeholder_mode_override=None,
        ):
            generated_calls.append(
                {
                    "prompt": prompt,
                    "aspect_ratio": aspect_ratio,
                    "category": category,
                    "variation_index": variation_index,
                    "generation_aspect_ratio": generation_aspect_ratio,
                    "reference_guide_override": reference_guide_override,
                    "placeholder_mode_override": placeholder_mode_override,
                }
            )
            output_path.write_bytes(b"png-bytes")
            return str(output_path)

    registered_calls: list[dict[str, object]] = []
    monkeypatch.setattr(tasks_module, "GeminiImageService", _FakeGeminiImageService)
    monkeypatch.setattr(tasks_module, "_resolve_trojan_reference_artwork_path", lambda aspect_ratio: trojan_reference_path)
    monkeypatch.setattr(
        tasks_module.CompositeCoordinateService,
        "extract_coordinates_and_erase",
        lambda image_path: [
            {"x": 10, "y": 20},
            {"x": 30, "y": 20},
            {"x": 30, "y": 40},
            {"x": 10, "y": 40},
        ],
    )
    monkeypatch.setattr(
        tasks_module,
        "_register_generated_base",
        lambda **kwargs: registered_calls.append(kwargs) or "trojan-base-1",
    )

    result = tasks_module.process_mockup_job.run(job_id)

    assert result["status"] == "completed"
    assert result["base_id"] == "trojan-base-1"
    assert len(generated_calls) == 1
    assert generated_calls[0]["reference_guide_override"] == trojan_reference_path
    assert generated_calls[0]["placeholder_mode_override"] == "artwork_trojan"
    assert generated_calls[0]["generation_aspect_ratio"] == tasks_module.MOCKUP_CANVAS_ASPECT_RATIO
    assert "cyan-black fiducial border" in str(generated_calls[0]["prompt"])
    assert len(registered_calls) == 1
    assert registered_calls[0]["external_job_id"] == "mbg_1x1_cafe_v1__artwork_trojan"

    session = session_factory()
    refreshed_job = session.get(MockupBaseGenerationJob, job_id)
    assert refreshed_job is not None
    assert str(cast(Any, refreshed_job).status) == "Completed"
    assert cast(Any, refreshed_job).coordinates_path is not None
    assert cast(Any, refreshed_job).prompt_text is not None
    assert "artwork_trojan" in str(cast(Any, refreshed_job).prompt_text)
    session.close()


def test_process_job_plain_composite_uses_artwork_only_guide_and_skips_detection(
    monkeypatch,
    tmp_path,
):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(tasks_module, "SessionLocal", session_factory)
    monkeypatch.setattr(tasks_module, "_load_control_state", lambda: {"state": "running", "skip_coordinate_detection": "false"})

    session = session_factory()
    job = MockupBaseGenerationJob(
        job_id="mbg_5x7_meeting-room_v1__artwork_only_composite",
        aspect_ratio="5x7",
        category="meeting-room",
        variation_index=1,
        generation_mode="artwork_only_composite",
        status="Pending",
        stage="Queued",
        attempts=0,
    )
    session.add(job)
    session.commit()
    job_id = job.id
    session.close()

    output_path = tmp_path / "plain-composite.png"
    guide_path = tmp_path / "5x7-artwork-placeholder.png"
    Image.new("RGB", (256, 256), (255, 255, 255)).save(guide_path, format="PNG")

    generated_calls: list[dict[str, object]] = []

    class _FakeGeminiImageService:
        last_placeholder_mode = tasks_module.GENERATION_MODE_ARTWORK_ONLY_COMPOSITE
        last_reference_guide_path = str(guide_path)

        def generate_image(self, prompt, aspect_ratio, category, variation_index, generation_aspect_ratio=None, reference_guide_override=None, placeholder_mode_override=None, **kwargs):
            generated_calls.append(
                {
                    "prompt": prompt,
                    "aspect_ratio": aspect_ratio,
                    "reference_guide_override": reference_guide_override,
                    "placeholder_mode_override": placeholder_mode_override,
                }
            )
            Image.new("RGB", (768, 768), (200, 200, 200)).save(output_path, format="PNG")
            return str(output_path)

    extract_call_count = {"count": 0}

    def _unexpected_extract(image_path):
        extract_call_count["count"] += 1
        raise AssertionError("Composite coordinate extraction should not run for plain composite workflow")

    registered_calls: list[dict[str, object]] = []
    monkeypatch.setattr(tasks_module, "GeminiImageService", _FakeGeminiImageService)
    monkeypatch.setattr(tasks_module, "_resolve_artwork_only_reference_path", lambda aspect_ratio: guide_path)
    monkeypatch.setattr(tasks_module.CompositeCoordinateService, "extract_coordinates_and_erase", _unexpected_extract)
    monkeypatch.setattr(
        tasks_module,
        "_register_generated_base",
        lambda **kwargs: registered_calls.append(kwargs) or "plain-base-1",
    )

    result = tasks_module.process_mockup_job.run(job_id)

    assert result["status"] == "completed"
    assert result["coordinates_source"] == "fallback"
    assert len(generated_calls) == 1
    assert generated_calls[0]["reference_guide_override"] == guide_path
    assert generated_calls[0]["placeholder_mode_override"] == "artwork_only_composite"
    assert "fiducial border" not in str(generated_calls[0]["prompt"])
    assert "aspect ratio 5x7" in str(generated_calls[0]["prompt"])
    assert extract_call_count["count"] == 0
    assert len(registered_calls) == 1
    assert registered_calls[0]["external_job_id"] == "mbg_5x7_meeting-room_v1__artwork_only_composite"


def test_process_job_uses_custom_prompt_text_from_control_state(monkeypatch, tmp_path):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(tasks_module, "SessionLocal", session_factory)
    monkeypatch.setattr(
        tasks_module,
        "_load_control_state",
        lambda: {
            "state": "running",
            "skip_coordinate_detection": "true",
            "custom_prompt_text": "Square mockup for {{category}} with artwork ratio {{aspect_ratio}} variation {{variation_index}}.",
        },
    )

    session = session_factory()
    job = MockupBaseGenerationJob(
        job_id="mbg_4x5_cafe_v2__artwork_only_composite",
        aspect_ratio="4x5",
        category="cafe",
        variation_index=2,
        generation_mode="artwork_only_composite",
        status="Pending",
        stage="Queued",
        attempts=0,
    )
    session.add(job)
    session.commit()
    job_id = job.id
    session.close()

    output_path = tmp_path / "custom-prompt.png"
    guide_path = tmp_path / "4x5-artwork-placeholder.png"
    Image.new("RGB", (256, 256), (255, 255, 255)).save(guide_path, format="PNG")

    generated_calls: list[dict[str, object]] = []

    class _FakeGeminiImageService:
        last_placeholder_mode = tasks_module.GENERATION_MODE_ARTWORK_ONLY_COMPOSITE
        last_reference_guide_path = str(guide_path)

        def generate_image(self, prompt, aspect_ratio, category, variation_index, generation_aspect_ratio=None, reference_guide_override=None, placeholder_mode_override=None, **kwargs):
            generated_calls.append(
                {
                    "prompt": prompt,
                    "reference_guide_override": reference_guide_override,
                    "placeholder_mode_override": placeholder_mode_override,
                }
            )
            Image.new("RGB", (768, 768), (190, 190, 190)).save(output_path, format="PNG")
            return str(output_path)

    monkeypatch.setattr(tasks_module, "GeminiImageService", _FakeGeminiImageService)
    monkeypatch.setattr(tasks_module, "_resolve_artwork_only_reference_path", lambda aspect_ratio: guide_path)
    monkeypatch.setattr(
        tasks_module,
        "_register_generated_base",
        lambda **kwargs: "custom-prompt-base",
    )

    result = tasks_module.process_mockup_job.run(job_id)

    assert result["status"] == "completed"
    assert len(generated_calls) == 1
    assert generated_calls[0]["reference_guide_override"] == guide_path
    assert generated_calls[0]["placeholder_mode_override"] == "artwork_only_composite"
    assert generated_calls[0]["prompt"] == "Square mockup for cafe with artwork ratio 4x5 variation 2."


def test_process_job_raw_prompt_only_sends_exact_text(monkeypatch, tmp_path):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(tasks_module, "SessionLocal", session_factory)
    raw_text = "please generate a square image of a mockup of this 2:3 aspect ratio artwork in an office"
    monkeypatch.setattr(
        tasks_module,
        "_load_control_state",
        lambda: {
            "state": "running",
            "skip_coordinate_detection": "true",
            "raw_prompt_only_enabled": "true",
            "raw_prompt_text": raw_text,
            "custom_prompt_text": "Square mockup for {{category}} with artwork ratio {{aspect_ratio}} variation {{variation_index}}.",
        },
    )

    session = session_factory()
    job = MockupBaseGenerationJob(
        job_id="mbg_2x3_office_v1__artwork_only_composite",
        aspect_ratio="2x3",
        category="office",
        variation_index=1,
        generation_mode="artwork_only_composite",
        status="Pending",
        stage="Queued",
        attempts=0,
    )
    session.add(job)
    session.commit()
    job_id = job.id
    session.close()

    output_path = tmp_path / "raw-only.png"
    guide_path = tmp_path / "2x3-artwork-placeholder.png"
    Image.new("RGB", (256, 256), (255, 255, 255)).save(guide_path, format="PNG")

    generated_calls: list[dict[str, object]] = []

    class _FakeGeminiImageService:
        last_placeholder_mode = tasks_module.GENERATION_MODE_ARTWORK_ONLY_COMPOSITE
        last_reference_guide_path = str(guide_path)

        def generate_image(self, prompt, aspect_ratio, category, variation_index, generation_aspect_ratio=None, reference_guide_override=None, placeholder_mode_override=None, **kwargs):
            generated_calls.append({
                "prompt": prompt,
                "reference_guide_override": reference_guide_override,
                "placeholder_mode_override": placeholder_mode_override,
            })
            Image.new("RGB", (768, 768), (180, 180, 180)).save(output_path, format="PNG")
            return str(output_path)

    monkeypatch.setattr(tasks_module, "GeminiImageService", _FakeGeminiImageService)
    monkeypatch.setattr(tasks_module, "_resolve_artwork_only_reference_path", lambda aspect_ratio: guide_path)
    monkeypatch.setattr(tasks_module, "_register_generated_base", lambda **kwargs: "raw-prompt-base")

    result = tasks_module.process_mockup_job.run(job_id)

    assert result["status"] == "completed"
    assert len(generated_calls) == 1
    assert generated_calls[0]["reference_guide_override"] == guide_path
    assert generated_calls[0]["placeholder_mode_override"] == "artwork_only_composite"
    assert generated_calls[0]["prompt"] == raw_text


def test_process_job_custom_prompt_auto_injects_aspect_ratio_when_missing(monkeypatch, tmp_path):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(tasks_module, "SessionLocal", session_factory)
    monkeypatch.setattr(
        tasks_module,
        "_load_control_state",
        lambda: {
            "state": "running",
            "skip_coordinate_detection": "true",
            "custom_prompt_text": "Generate a premium mockup scene for {{category}}.",
        },
    )

    session = session_factory()
    job = MockupBaseGenerationJob(
        job_id="mbg_70x99_living-room_v1__artwork_only_composite",
        aspect_ratio="70x99",
        category="living-room",
        variation_index=1,
        generation_mode="artwork_only_composite",
        status="Pending",
        stage="Queued",
        attempts=0,
    )
    session.add(job)
    session.commit()
    job_id = job.id
    session.close()

    output_path = tmp_path / "custom-prompt-inject.png"
    guide_path = tmp_path / "70x99-artwork-placeholder.png"
    Image.new("RGB", (256, 256), (255, 255, 255)).save(guide_path, format="PNG")

    generated_calls: list[dict[str, object]] = []

    class _FakeGeminiImageService:
        last_placeholder_mode = tasks_module.GENERATION_MODE_ARTWORK_ONLY_COMPOSITE
        last_reference_guide_path = str(guide_path)

        def generate_image(self, prompt, aspect_ratio, category, variation_index, generation_aspect_ratio=None, reference_guide_override=None, placeholder_mode_override=None, **kwargs):
            generated_calls.append({"prompt": prompt})
            Image.new("RGB", (768, 768), (180, 180, 180)).save(output_path, format="PNG")
            return str(output_path)

    monkeypatch.setattr(tasks_module, "GeminiImageService", _FakeGeminiImageService)
    monkeypatch.setattr(tasks_module, "_resolve_artwork_only_reference_path", lambda aspect_ratio: guide_path)
    monkeypatch.setattr(tasks_module, "_register_generated_base", lambda **kwargs: "custom-prompt-inject")

    result = tasks_module.process_mockup_job.run(job_id)

    assert result["status"] == "completed"
    assert len(generated_calls) == 1
    rendered_prompt = str(generated_calls[0]["prompt"])
    assert "living-room" in rendered_prompt
    assert "70x99" in rendered_prompt
    assert "Technical constraint: preserve the supplied artwork at exact aspect ratio 70x99" in rendered_prompt


def test_prompt_preview_renders_custom_prompt_with_aspect_injection(app_client):
    response = app_client.post(
        "/admin/mockups/mockup-generator/prompt-preview",
        json={
            "placeholder_mode": "artwork_only_composite",
            "category": "living-room",
            "aspect_ratio": "70x99",
            "variation_index": 1,
            "custom_prompt_text": "Generate a premium mockup scene for {{category}}.",
        },
    )

    assert response.status_code == 200
    payload = response.get_json()
    prompt_text = str(payload["prompt_text"])
    assert "living-room" in prompt_text
    assert "70x99" in prompt_text
    assert "Technical constraint: preserve the supplied artwork at exact aspect ratio 70x99" in prompt_text


def test_clear_pending_generation_jobs_removes_only_pending(app_client, monkeypatch, tmp_path):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(generator_routes, "SessionLocal", session_factory)

    session = session_factory()
    session.add_all(
        [
            MockupBaseGenerationJob(
                job_id="mbg_1x1_cafe_v1",
                aspect_ratio="1x1",
                category="cafe",
                variation_index=1,
                status="Pending",
                stage="Queued",
                attempts=0,
            ),
            MockupBaseGenerationJob(
                job_id="mbg_1x1_cafe_v2",
                aspect_ratio="1x1",
                category="cafe",
                variation_index=2,
                status="Pending",
                stage="Queued",
                attempts=0,
            ),
            MockupBaseGenerationJob(
                job_id="mbg_1x1_cafe_v3",
                aspect_ratio="1x1",
                category="cafe",
                variation_index=3,
                status="Failed",
                stage="Failed",
                attempts=1,
                error_message="boom",
                reason="RuntimeError",
            ),
        ]
    )
    session.commit()
    session.close()

    response = app_client.post(
        "/admin/mockups/mockup-generator/clear-pending",
        headers={"X-CSRFToken": app_client.csrf_token},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["cleared"] == 2
    assert payload["status_counts"]["Pending"] == 0
    assert payload["status_counts"]["Failed"] == 1

    session = session_factory()
    remaining = session.query(MockupBaseGenerationJob).order_by(MockupBaseGenerationJob.id.asc()).all()
    assert len(remaining) == 1
    assert str(cast(Any, remaining[0]).status) == "Failed"
    session.close()


def test_clear_failed_generation_jobs_removes_only_failed(app_client, monkeypatch, tmp_path):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(generator_routes, "SessionLocal", session_factory)

    session = session_factory()
    session.add_all(
        [
            MockupBaseGenerationJob(
                job_id="mbg_1x1_cafe_v1",
                aspect_ratio="1x1",
                category="cafe",
                variation_index=1,
                status="Failed",
                stage="Failed",
                attempts=1,
                error_message="boom-1",
                reason="RuntimeError",
            ),
            MockupBaseGenerationJob(
                job_id="mbg_1x1_cafe_v2",
                aspect_ratio="1x1",
                category="cafe",
                variation_index=2,
                status="Failed",
                stage="Failed",
                attempts=2,
                error_message="boom-2",
                reason="RuntimeError",
            ),
            MockupBaseGenerationJob(
                job_id="mbg_1x1_cafe_v3",
                aspect_ratio="1x1",
                category="cafe",
                variation_index=3,
                status="Pending",
                stage="Queued",
                attempts=0,
            ),
        ]
    )
    session.commit()
    session.close()

    response = app_client.post(
        "/admin/mockups/mockup-generator/clear-failed",
        headers={"X-CSRFToken": app_client.csrf_token},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["cleared"] == 2
    assert payload["status_counts"]["Failed"] == 0
    assert payload["status_counts"]["Pending"] == 1
    assert payload["recent_failed_jobs"] == []

    session = session_factory()
    remaining = session.query(MockupBaseGenerationJob).order_by(MockupBaseGenerationJob.id.asc()).all()
    assert len(remaining) == 1
    assert str(cast(Any, remaining[0]).status) == "Pending"
    session.close()


def test_generator_status_returns_recent_failure_details(app_client, monkeypatch, tmp_path):
    session_factory = _build_test_session_factory(tmp_path)
    monkeypatch.setattr(generator_routes, "SessionLocal", session_factory)
    monkeypatch.setattr(generator_routes, "_load_control_state", lambda: {"state": "running"})

    session = session_factory()
    session.add(
        MockupBaseGenerationJob(
            job_id="mbg_4x5_bedroom_v1",
            aspect_ratio="4x5",
            category="bedroom",
            variation_index=1,
            status="Failed",
            stage="Failed",
            attempts=2,
            reason="GeminiGenerationError",
            error_message="Gemini API call failed",
        )
    )
    session.commit()
    session.close()

    response = app_client.get("/admin/mockups/mockup-generator/status")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status_counts"]["Failed"] == 1
    assert len(payload["recent_failed_jobs"]) == 1
    assert payload["recent_failed_jobs"][0]["job_id"] == "mbg_4x5_bedroom_v1"
    assert payload["recent_failed_jobs"][0]["error_message"] == "Gemini API call failed"
    assert payload["recent_failed_jobs"][0]["reason"] == "GeminiGenerationError"