"""Integration tests for analysis job queue (Stage 3 Stage-2 execution).

Tests the DB-backed job queue with Stage 1 + Stage 2 worker flow (providers mocked):
- Job enqueueing
- Worker claiming and processing
- Job status endpoints
- Manifest updates
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from db import AnalysisJob, Base, SessionLocal, engine
from application.analysis.worker.analysis_worker import _claim_next_job, _process_job_stage1a
from application.app import create_app
from application.common.utilities.files import write_json_atomic


@pytest.fixture(scope="function")
def db_session():
    """Create clean test database session."""
    AnalysisJob.__table__.drop(bind=engine, checkfirst=True)
    AnalysisJob.__table__.create(bind=engine, checkfirst=True)
    session = SessionLocal()
    
    # Clean up existing jobs
    session.query(AnalysisJob).delete()
    session.commit()
    
    yield session
    
    session.close()


@pytest.fixture(scope="function")
def client():
    """Create authenticated Flask test client for API endpoint tests."""
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        with test_client.session_transaction() as sess:
            current_ts = time.time()
            sess["username"] = "pytest-admin"
            sess["role"] = "admin"
            sess["login_ts"] = current_ts
            sess["last_activity_ts"] = current_ts
        yield test_client


@pytest.fixture
def mock_processed_dir(tmp_path):
    """Create mock processed artwork directory structure."""
    processed_root = tmp_path / "processed"
    processed_root.mkdir()
    
    # Create test artwork directory
    artwork_dir = processed_root / "test-slug"
    artwork_dir.mkdir()
    
    # Create minimal manifest
    manifest = {
        "version": 1,
        "slug": "test-slug",
        "sku": "TEST-0001",
        "files": {},
    }
    write_json_atomic(artwork_dir / "test-slug-assets.json", manifest)
    
    # Create minimal metadata
    metadata = {
        "slug": "test-slug",
        "sku": "TEST-0001",
        "artwork_id": "TEST-0001",
    }
    write_json_atomic(artwork_dir / "metadata.json", metadata)
    
    return processed_root


def test_enqueue_creates_job_record(db_session):
    """Test that enqueueing creates AnalysisJob record."""
    import uuid
    
    job_id = str(uuid.uuid4())
    job = AnalysisJob(
        job_id=job_id,
        slug="test-slug",
        sku="TEST-0001",
        provider="openai",
        status="QUEUED",
        stage="stage1_image",
        progress=0,
        attempts=0,
    )
    
    db_session.add(job)
    db_session.commit()
    
    # Verify job exists
    retrieved = db_session.query(AnalysisJob).filter(AnalysisJob.job_id == job_id).first()
    assert retrieved is not None
    assert retrieved.status == "QUEUED"
    assert retrieved.slug == "test-slug"
    assert retrieved.provider == "openai"


def test_worker_claims_queued_job(db_session):
    """Test worker can claim QUEUED job atomically."""
    import uuid
    
    # Create two queued jobs
    job1 = AnalysisJob(
        job_id=str(uuid.uuid4()),
        slug="slug1",
        sku="SKU1",
        provider="openai",
        status="QUEUED",
        stage="stage1_image",
        progress=0,
        attempts=0,
    )
    job2 = AnalysisJob(
        job_id=str(uuid.uuid4()),
        slug="slug2",
        sku="SKU2",
        provider="gemini",
        status="QUEUED",
        stage="stage1_image",
        progress=0,
        attempts=0,
    )
    
    db_session.add(job1)
    db_session.add(job2)
    db_session.commit()
    
    # Claim first job
    claimed = _claim_next_job(db_session)
    
    assert claimed is not None
    assert getattr(claimed, "status", None) == "RUNNING"
    assert getattr(claimed, "attempts", None) == 1
    assert getattr(claimed, "started_at", None) is not None
    
    # Should be job1 (oldest)
    assert getattr(claimed, "slug", None) == "slug1"


def test_worker_processes_job_stage1a(db_session, mock_processed_dir, tmp_path):
    """Test worker executes Stage 1+2 and writes slug-prefixed outputs."""
    import uuid
    
    job_id = str(uuid.uuid4())
    job = AnalysisJob(
        job_id=job_id,
        slug="test-slug",
        sku="TEST-0001",
        provider="openai",
        status="RUNNING",
        stage="stage1_image",
        progress=0,
        attempts=1,
    )
    
    db_session.add(job)
    db_session.commit()
    
    # Mock config + provider call to keep test deterministic
    with (
        patch("application.analysis.worker.analysis_worker.get_config") as mock_cfg,
        patch("application.analysis.worker.analysis_worker.run_openai_analysis_for_slug") as mock_openai,
    ):
        cfg_mock = MagicMock()
        cfg_mock.LAB_PROCESSED_DIR = mock_processed_dir
        cfg_mock.ARTWORKS_INDEX_PATH = tmp_path / "artworks.json"
        mock_cfg.return_value = cfg_mock

        stage_provider_result = {
            "listing": {
                "title": "Wetland Dusk Story Print",
                "description": "A warm, buyer-friendly narrative with digital download clarity and quality notes.\nDigital download only. 14400px and prints up to 48\" long edge at 300 DPI. Personal use only.",
                "tags": ["wetlands", "sunset", "landscape", "dot art"],
                "primary_colour": "Gold",
                "secondary_colour": "Indigo",
                "visual_analysis": {
                    "subject": "Wetland reeds at dusk",
                    "dot_rhythm": "Layered dot clusters with flowing movement",
                    "palette": "Gold, Indigo, Ochre",
                    "mood": "Warm sunset glow",
                },
            },
            "metadata": {
                "original_filename": "bool-lagoon-dusk.jpg",
                "analysis": {
                    "visual_analysis": {
                        "subject": "Wetland reeds at dusk",
                        "dot_rhythm": "Layered dot clusters with flowing movement",
                        "palette": "Gold, Indigo, Ochre",
                        "mood": "Warm sunset glow",
                    }
                },
            },
        }
        mock_openai.return_value = stage_provider_result
        
        # Create minimal index
        index_data = {
            "version": 2,
            "items": {},
            "updated_at": "2026-03-04T00:00:00Z",
        }
        write_json_atomic(cfg_mock.ARTWORKS_INDEX_PATH, index_data)
        
        # Process job
        _process_job_stage1a(job, db_session)
    
    # Verify job is marked DONE at stage2
    db_session.refresh(job)
    assert getattr(job, "status", None) == "DONE"
    assert getattr(job, "progress", None) == 66
    assert getattr(job, "stage", None) == "stage2_etsy"
    assert getattr(job, "finished_at", None) is not None
    
    # Verify manifest was updated
    manifest_path = mock_processed_dir / "test-slug" / "test-slug-assets.json"
    assert manifest_path.exists()
    
    manifest = json.loads(manifest_path.read_text())
    assert "analysis" in manifest
    assert manifest["analysis"]["status"] == "success"
    assert manifest["analysis"]["progress"] == 66
    assert manifest["analysis"]["job_id"] == job_id
    assert manifest["analysis"]["stage"] == "stage2_etsy"

    assert manifest["files"]["analysis_stage1"] == "test-slug-analysis-stage1.json"
    assert manifest["files"]["ai_packet"] == "test-slug-ai-packet.json"
    assert manifest["files"]["copy_etsy"] == "test-slug-copy-etsy.json"

    stage1_path = mock_processed_dir / "test-slug" / "test-slug-analysis-stage1.json"
    ai_packet_path = mock_processed_dir / "test-slug" / "test-slug-ai-packet.json"
    stage2_path = mock_processed_dir / "test-slug" / "test-slug-copy-etsy.json"
    assert stage1_path.exists()
    assert ai_packet_path.exists()
    assert stage2_path.exists()

    stage1_payload = json.loads(stage1_path.read_text(encoding="utf-8"))
    assert stage1_payload["subject"] == "Wetland reeds at dusk"
    assert isinstance(stage1_payload["palette"], list)
    assert isinstance(stage1_payload["keywords"], list)

    stage2_payload = json.loads(stage2_path.read_text(encoding="utf-8"))
    assert stage2_payload["title"]
    assert isinstance(stage2_payload["seo_keywords"], list)


def test_worker_stage2_failure_marks_failed_without_moving_folder(db_session, mock_processed_dir, tmp_path):
    """Test Stage 2 failure updates job/manifest and keeps folder in place."""
    import uuid

    job_id = str(uuid.uuid4())
    job = AnalysisJob(
        job_id=job_id,
        slug="test-slug",
        sku="TEST-0001",
        provider="openai",
        status="RUNNING",
        stage="stage1_image",
        progress=0,
        attempts=1,
    )

    db_session.add(job)
    db_session.commit()

    with (
        patch("application.analysis.worker.analysis_worker.get_config") as mock_cfg,
        patch("application.analysis.worker.analysis_worker.run_openai_analysis_for_slug") as mock_openai,
            patch("application.analysis.worker.analysis_worker._cfg_bool", return_value=False),
    ):
        cfg_mock = MagicMock()
        cfg_mock.LAB_PROCESSED_DIR = mock_processed_dir
        cfg_mock.ARTWORKS_INDEX_PATH = tmp_path / "artworks.json"
        mock_cfg.return_value = cfg_mock

        stage1_result = {
            "listing": {
                "title": "Stage1 Seed Title",
                "description": "Digital download only. 14400px and up to 48\" long edge. Personal use only.",
                "tags": ["wetlands", "sunset", "landscape", "dot art"],
                "visual_analysis": {
                    "subject": "Wetland reeds at dusk",
                    "dot_rhythm": "Layered dot clusters",
                    "palette": "Gold, Indigo",
                    "mood": "Warm sunset glow",
                },
            },
            "metadata": {
                "original_filename": "stage1.jpg",
                "analysis": {
                    "visual_analysis": {
                        "subject": "Wetland reeds at dusk",
                        "dot_rhythm": "Layered dot clusters",
                        "palette": "Gold, Indigo",
                        "mood": "Warm sunset glow",
                    }
                },
            },
        }
        # Stage2 unusable payload (missing title/description)
        stage2_result = {"listing": {}, "metadata": {}}
        mock_openai.side_effect = [stage1_result, stage2_result]

        index_data = {
            "version": 2,
            "items": {},
            "updated_at": "2026-03-04T00:00:00Z",
        }
        write_json_atomic(cfg_mock.ARTWORKS_INDEX_PATH, index_data)

        _process_job_stage1a(job, db_session)

    db_session.refresh(job)
    assert getattr(job, "status", None) == "FAILED"
    assert str(getattr(job, "reason", "")).startswith("ERR_STAGE2_VALIDATE")
    assert getattr(job, "error_message", None)

    artwork_dir = mock_processed_dir / "test-slug"
    assert artwork_dir.exists()

    manifest_path = artwork_dir / "test-slug-assets.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["analysis"]["status"] == "failed"
    assert manifest["analysis"]["stage"] == "stage2_etsy"
    assert manifest["analysis"]["reason"].startswith("ERR_STAGE2_VALIDATE")


def test_stage2_minor_validation_sets_needs_review(db_session, mock_processed_dir, tmp_path):
    """Test minor Stage 2 issues mark manifest as needs_review instead of failed."""
    import uuid

    job = AnalysisJob(
        job_id=str(uuid.uuid4()),
        slug="test-slug",
        sku="TEST-0001",
        provider="openai",
        status="RUNNING",
        stage="stage1_image",
        progress=0,
        attempts=1,
    )
    db_session.add(job)
    db_session.commit()

    with (
        patch("application.analysis.worker.analysis_worker.get_config") as mock_cfg,
        patch("application.analysis.worker.analysis_worker.run_openai_analysis_for_slug") as mock_openai,
    ):
        cfg_mock = MagicMock()
        cfg_mock.LAB_PROCESSED_DIR = mock_processed_dir
        cfg_mock.ARTWORKS_INDEX_PATH = tmp_path / "artworks.json"
        mock_cfg.return_value = cfg_mock

        long_line = "A" * 300
        provider_result = {
            "listing": {
                "title": "Stage2 Needs Review Title",
                "description": long_line,
                "tags": ["wetlands", "sunset", "landscape"],
                "visual_analysis": {
                    "subject": "Wetland reeds",
                    "dot_rhythm": "Rhythmic dot flow",
                    "palette": "Gold, Indigo",
                    "mood": "Calm twilight",
                },
            },
            "metadata": {
                "original_filename": "review.jpg",
                "analysis": {
                    "visual_analysis": {
                        "subject": "Wetland reeds",
                        "dot_rhythm": "Rhythmic dot flow",
                        "palette": "Gold, Indigo",
                        "mood": "Calm twilight",
                    }
                },
            },
        }
        mock_openai.return_value = provider_result

        index_data = {
            "version": 2,
            "items": {},
            "updated_at": "2026-03-04T00:00:00Z",
        }
        write_json_atomic(cfg_mock.ARTWORKS_INDEX_PATH, index_data)

        _process_job_stage1a(job, db_session)

    db_session.refresh(job)
    assert getattr(job, "status", None) == "DONE"
    assert getattr(job, "reason", None) == "WARN_STAGE2_REVIEW"

    manifest = json.loads((mock_processed_dir / "test-slug" / "test-slug-assets.json").read_text(encoding="utf-8"))
    assert manifest["analysis"]["status"] == "needs_review"
    assert manifest["analysis"]["reason"] == "WARN_STAGE2_REVIEW"


def test_provider_selection_persists_into_stage2_execution(db_session, mock_processed_dir, tmp_path):
    """Test provider chosen at enqueue is used for subsequent stages."""
    import uuid

    job = AnalysisJob(
        job_id=str(uuid.uuid4()),
        slug="test-slug",
        sku="TEST-0001",
        provider="gemini",
        status="RUNNING",
        stage="stage1_image",
        progress=0,
        attempts=1,
    )
    db_session.add(job)
    db_session.commit()

    with (
        patch("application.analysis.worker.analysis_worker.get_config") as mock_cfg,
        patch("application.analysis.worker.analysis_worker.run_gemini_analysis_for_slug") as mock_gemini,
        patch("application.analysis.worker.analysis_worker.run_openai_analysis_for_slug") as mock_openai,
            patch("application.analysis.worker.analysis_worker._cfg_bool", return_value=False),
    ):
        cfg_mock = MagicMock()
        cfg_mock.LAB_PROCESSED_DIR = mock_processed_dir
        cfg_mock.ARTWORKS_INDEX_PATH = tmp_path / "artworks.json"
        mock_cfg.return_value = cfg_mock

        gemini_result = {
            "listing": {
                "title": "Gemini Stage 2 Title",
                "description": "Digital download only. 14400px print file for up to 48\" long edge at 300 DPI. Personal use only and copyright remains with the artist.",
                "tags": ["wetlands", "sunset", "landscape"],
                "visual_analysis": {
                    "subject": "Wetland reeds",
                    "dot_rhythm": "Rhythmic dot flow",
                    "palette": "Gold, Indigo",
                    "mood": "Calm twilight",
                },
            },
            "metadata": {
                "original_filename": "gemini.jpg",
                "analysis": {
                    "visual_analysis": {
                        "subject": "Wetland reeds",
                        "dot_rhythm": "Rhythmic dot flow",
                        "palette": "Gold, Indigo",
                        "mood": "Calm twilight",
                    }
                },
            },
        }
        mock_gemini.return_value = gemini_result

        index_data = {
            "version": 2,
            "items": {},
            "updated_at": "2026-03-04T00:00:00Z",
        }
        write_json_atomic(cfg_mock.ARTWORKS_INDEX_PATH, index_data)

        _process_job_stage1a(job, db_session)

    db_session.refresh(job)
    assert getattr(job, "status", None) == "DONE"
    assert getattr(job, "stage", None) == "stage2_etsy"
    assert mock_gemini.call_count == 2
    assert mock_openai.call_count == 0


def test_job_summary_endpoint_counts(client, db_session):
    """Test /api/jobs/summary returns correct counts."""
    import uuid
    from datetime import datetime, timedelta
    
    # Create various jobs
    jobs = [
        AnalysisJob(
            job_id=str(uuid.uuid4()),
            slug="slug1",
            provider="openai",
            status="QUEUED",
            stage="stage1_image",
            progress=0,
            attempts=0,
        ),
        AnalysisJob(
            job_id=str(uuid.uuid4()),
            slug="slug2",
            provider="gemini",
            status="RUNNING",
            stage="stage1_image",
            progress=50,
            attempts=1,
            started_at=datetime.utcnow(),
        ),
        AnalysisJob(
            job_id=str(uuid.uuid4()),
            slug="slug3",
            provider="openai",
            status="DONE",
            stage="complete",
            progress=100,
            attempts=1,
            finished_at=datetime.utcnow(),
        ),
        AnalysisJob(
            job_id=str(uuid.uuid4()),
            slug="slug4",
            provider="gemini",
            status="FAILED",
            stage="stage1_image",
            progress=10,
            attempts=2,
            reason="ERR_TEST",
            error_message="Test failure",
            finished_at=datetime.utcnow(),
        ),
    ]
    
    for job in jobs:
        db_session.add(job)
    db_session.commit()
    
    # Query summary endpoint
    response = client.get("/api/jobs/summary")
    assert response.status_code == 200
    
    data = response.get_json()
    assert data["queued"] == 1
    assert data["running"] == 1
    assert data["done_recent"] == 1
    assert data["failed_recent"] == 1
    assert data["total_active"] == 2


def test_recent_jobs_endpoint(client, db_session):
    """Test /api/jobs/recent returns recent jobs."""
    import uuid
    from datetime import datetime
    
    # Create recent completed jobs
    jobs = [
        AnalysisJob(
            job_id=str(uuid.uuid4()),
            slug=f"slug{i}",
            sku=f"SKU{i}",
            provider="openai" if i % 2 == 0 else "gemini",
            status="DONE" if i % 2 == 0 else "FAILED",
            stage="complete" if i % 2 == 0 else "stage1_image",
            progress=100 if i % 2 == 0 else 50,
            attempts=1,
            finished_at=datetime.utcnow(),
        )
        for i in range(5)
    ]
    
    for job in jobs:
        db_session.add(job)
    db_session.commit()
    
    # Query recent endpoint
    response = client.get("/api/jobs/recent")
    assert response.status_code == 200
    
    data = response.get_json()
    assert "jobs" in data
    assert len(data["jobs"]) == 5
    
    # Should be ordered by finished_at desc
    for job_data in data["jobs"]:
        assert "job_id" in job_data
        assert "slug" in job_data
        assert "status" in job_data
        assert "provider" in job_data


def test_job_detail_endpoint(client, db_session):
    """Test /api/jobs/<job_id> returns job details."""
    import uuid
    
    job_id = str(uuid.uuid4())
    job = AnalysisJob(
        job_id=job_id,
        slug="test-slug",
        sku="TEST-0001",
        provider="openai",
        status="RUNNING",
        stage="stage1_image",
        progress=50,
        attempts=1,
    )
    
    db_session.add(job)
    db_session.commit()
    
    response = client.get(f"/api/jobs/{job_id}")
    assert response.status_code == 200
    
    data = response.get_json()
    assert data["job_id"] == job_id
    assert data["slug"] == "test-slug"
    assert data["status"] == "RUNNING"
    assert data["progress"] == 50


def test_admin_jobs_list_endpoint(client, db_session):
    """Test /api/jobs/admin/list returns newest jobs and admin fields."""
    import uuid

    job = AnalysisJob(
        job_id=str(uuid.uuid4()),
        slug="admin-list-slug",
        sku="ADMIN-0001",
        provider="openai",
        status="QUEUED",
        stage="stage1_image",
        progress=0,
        attempts=0,
    )
    db_session.add(job)
    db_session.commit()

    response = client.get("/api/jobs/admin/list?limit=10")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data.get("jobs"), list)
    assert data.get("count", 0) >= 1
    assert any(row.get("slug") == "admin-list-slug" for row in data["jobs"])


def test_cancel_job_endpoint_deletes_non_running_job(client, db_session):
    """Cancel endpoint should cleanup and remove non-running jobs from DB."""
    import uuid

    job_id = str(uuid.uuid4())
    job = AnalysisJob(
        job_id=job_id,
        slug="cancel-slug",
        sku="CANCEL-0001",
        provider="gemini",
        status="FAILED",
        stage="stage1_image",
        progress=0,
        attempts=1,
    )
    db_session.add(job)
    db_session.commit()

    csrf_token = "test-csrf-token"
    with client.session_transaction() as sess:
        sess["_csrf_token"] = csrf_token

    with patch("application.analysis.api.job_routes.cleanup_analysis_job_artifacts") as mock_cleanup:
        mock_cleanup.return_value = {
            "slug": "cancel-slug",
            "deleted_files": ["/tmp/a.json"],
            "touched_dirs": ["/tmp"],
            "manifest_updates": 1,
            "artwork_rows_deleted": 1,
        }

        response = client.post(
            f"/api/jobs/{job_id}/cancel",
            json={"cleanup": True, "remove_artwork_record": True, "csrf_token": csrf_token},
            headers={"X-CSRFToken": csrf_token},
        )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["ok"] is True
    assert payload["pending"] is False
    assert payload["cleanup"]["artwork_rows_deleted"] == 1

    db_session.expire_all()
    row = db_session.query(AnalysisJob).filter(AnalysisJob.job_id == job_id).first()
    assert row is None


def test_cancel_job_endpoint_marks_running_job_cancel_requested(client, db_session):
    """Running jobs should be marked for cancellation so the worker can exit safely."""
    import uuid

    job_id = str(uuid.uuid4())
    job = AnalysisJob(
        job_id=job_id,
        slug="running-slug",
        sku="RUN-0001",
        provider="openai",
        status="RUNNING",
        stage="stage1_image",
        progress=30,
        attempts=1,
    )
    db_session.add(job)
    db_session.commit()

    csrf_token = "test-csrf-token-2"
    with client.session_transaction() as sess:
        sess["_csrf_token"] = csrf_token

    with patch("application.analysis.api.job_routes.cleanup_analysis_job_artifacts") as mock_cleanup:
        mock_cleanup.return_value = {
            "slug": "running-slug",
            "deleted_files": [],
            "touched_dirs": [],
            "manifest_updates": 0,
            "artwork_rows_deleted": 0,
        }

        response = client.post(
            f"/api/jobs/{job_id}/cancel",
            json={"cleanup": True, "remove_artwork_record": True, "csrf_token": csrf_token},
            headers={"X-CSRFToken": csrf_token},
        )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["ok"] is True
    assert payload["pending"] is True

    db_session.expire_all()
    row = db_session.query(AnalysisJob).filter(AnalysisJob.job_id == job_id).first()
    assert row is not None
    assert row.status == "CANCEL_REQUESTED"
