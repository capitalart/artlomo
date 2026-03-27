from __future__ import annotations

import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from db import MockupBaseGenerationJob, SessionLocal, engine
from application.mockups.config import (
    MOCKUP_BASE_GENERATION_CONFIG,
    MOCKUP_BASE_GENERATION_STATUSES,
    MockupBaseGenerationCatalog,
)


@pytest.fixture(autouse=True)
def reset_mockup_base_generation_table():
    """Ensure clean table state for each test."""
    MockupBaseGenerationJob.__table__.drop(bind=engine, checkfirst=True)
    MockupBaseGenerationJob.__table__.create(bind=engine, checkfirst=True)
    yield


@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_catalog_source_of_truth_contract():
    assert len(MockupBaseGenerationCatalog.ASPECT_RATIOS) == 13
    assert "4x5" in MockupBaseGenerationCatalog.ASPECT_RATIOS

    # User-provided category list currently contains 23 entries.
    assert len(MockupBaseGenerationCatalog.CATEGORIES) == 23
    assert "bathroom" in MockupBaseGenerationCatalog.CATEGORIES
    assert "workplace" in MockupBaseGenerationCatalog.CATEGORIES

    assert MockupBaseGenerationCatalog.VARIATION_MIN_INDEX == 1
    assert MockupBaseGenerationCatalog.VARIATION_MAX_INDEX == 20

    assert MOCKUP_BASE_GENERATION_CONFIG["variation_min_index"] == 1
    assert MOCKUP_BASE_GENERATION_CONFIG["variation_max_index"] == 20


def test_status_lifecycle_contract():
    assert MOCKUP_BASE_GENERATION_STATUSES == (
        "Pending",
        "Generating",
        "ProcessingCoordinates",
        "Completed",
        "Failed",
    )


def test_model_persists_identity_tuple_and_status(db_session):
    job = MockupBaseGenerationJob(
        job_id=f"mbg-{uuid.uuid4().hex[:20]}",
        aspect_ratio="3x4",
        category="living-room",
        variation_index=7,
        status="Pending",
        attempts=0,
    )

    db_session.add(job)
    db_session.commit()

    row = (
        db_session.query(MockupBaseGenerationJob)
        .filter(MockupBaseGenerationJob.job_id == job.job_id)
        .first()
    )

    assert row is not None
    assert row.aspect_ratio == "3x4"
    assert row.category == "living-room"
    assert row.variation_index == 7
    assert row.status == "Pending"


def test_model_enforces_variation_index_bounds(db_session):
    invalid_job = MockupBaseGenerationJob(
        job_id=f"mbg-{uuid.uuid4().hex[:20]}",
        aspect_ratio="3x4",
        category="living-room",
        variation_index=21,
        status="Pending",
    )

    db_session.add(invalid_job)
    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()
