from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Index,
    Integer,
    String,
    Text,
    create_engine,
    text,
)
from sqlalchemy.orm import declarative_base, sessionmaker


def _resolve_db_path() -> Path:
    explicit = (os.getenv("ARTLOMO_DB_PATH") or "").strip()
    if explicit:
        return Path(explicit).expanduser().resolve()

    base_dir = Path(os.getenv("ARTLOMO_BASE_DIR", Path(__file__).resolve().parent)).resolve()
    data_db = base_dir / "data" / "artlomo.sqlite3"
    if data_db.parent.exists():
        return data_db

    return (base_dir / "var" / "db" / "artlomo.sqlite3").resolve()


DB_PATH = _resolve_db_path()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(32), default="viewer", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)

    login_enabled = Column(Boolean, default=True, nullable=False)
    login_override_until = Column(DateTime, nullable=True)

    force_no_cache = Column(Boolean, default=False, nullable=False)
    force_no_cache_until = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(64), unique=True, index=True, nullable=False)  # UUID for external reference
    slug = Column(String(128), index=True, nullable=False)
    sku = Column(String(64), index=True, nullable=True)  # Resolved SKU for the artwork
    provider = Column(String(32), index=True, nullable=False)  # openai, gemini
    status = Column(String(32), index=True, nullable=False)  # QUEUED, RUNNING, DONE, FAILED
    stage = Column(String(64), nullable=True)  # stage1_image, stage2_etsy, stage3_marketing, complete
    progress = Column(Integer, default=0, nullable=False)  # 0-100
    attempts = Column(Integer, default=0, nullable=False)  # Retry count
    reason = Column(String(128), nullable=True)  # Short error code (ERR_CONTRACT, ERR_TIMEOUT, etc)
    error_message = Column(String(1024), nullable=True)  # Human-readable error
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)  # When worker claimed job
    finished_at = Column(DateTime, nullable=True)  # When job completed/failed


class Artwork(Base):
    __tablename__ = "artworks"

    id = Column(String(32), primary_key=True, index=True)  # SKU e.g. RJC-0138
    slug = Column(String(128), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=True)
    owner_id = Column(String(64), index=True, nullable=True)  # username of owner
    status = Column(String(32), index=True, nullable=False, default="unprocessed")  # unprocessed, processed, locked, deleted
    previous_status = Column(String(32), nullable=True)  # status before deletion (for restore)
    analysis_source = Column(String(32), nullable=True)  # openai, gemini, manual
    image_path = Column(String(512), nullable=True)  # path to stored image
    thumb_path = Column(String(512), nullable=True)  # path to thumbnail
    metadata_json = Column(String(8192), nullable=True)  # cached metadata as JSON string
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)  # timestamp when moved to trash


class AnalysisPreset(Base):
    __tablename__ = "analysis_presets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=False, index=True)
    provider = Column(String(32), nullable=False, index=True)  # openai, gemini
    is_default = Column(Boolean, default=False, nullable=False, index=True)
    
    # Sections stored as JSON text
    system_prompt = Column(Text, nullable=False)
    user_full_prompt = Column(Text, nullable=False)
    user_section_prompt = Column(Text, nullable=False)
    listing_boilerplate = Column(Text, nullable=False)
    analysis_prompt = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class ForgeJob(Base):
    __tablename__ = "forge_jobs"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(128), nullable=False, index=True)
    shape_descriptor = Column(String(256), nullable=False)
    status = Column(String(32), nullable=False, index=True, default="Pending")  # Pending, Generating, Processing, Completed, Failed
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class MockupBaseGenerationJob(Base):
    __tablename__ = "mockup_base_generation_jobs"

    __table_args__ = (
        CheckConstraint(
            "variation_index >= 1 AND variation_index <= 20",
            name="ck_mockup_base_generation_variation_index",
        ),
        Index(
            "ix_mockup_base_generation_lookup",
            "aspect_ratio",
            "category",
            "variation_index",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(64), unique=True, index=True, nullable=False)

    # Queue identity tuple for a generated base.
    aspect_ratio = Column(String(16), index=True, nullable=False)
    category = Column(String(64), index=True, nullable=False)
    variation_index = Column(Integer, nullable=False)
    generation_mode = Column(String(50), default="standard", server_default="standard")

    # Stage 1 status lifecycle: Pending -> Generating -> ProcessingCoordinates -> Completed/Failed.
    status = Column(String(64), index=True, nullable=False, default="Pending")
    attempts = Column(Integer, default=0, nullable=False)
    stage = Column(String(64), nullable=True)

    # Diagnostics and output references populated by worker stages.
    reason = Column(String(128), nullable=True)
    error_message = Column(Text, nullable=True)
    prompt_text = Column(Text, nullable=True)
    generated_image_path = Column(String(1024), nullable=True)
    coordinates_path = Column(String(1024), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)


class GeminiStudioJob(Base):
    __tablename__ = "gemini_studio_jobs"

    __table_args__ = (
        CheckConstraint(
            "variation_index >= 1 AND variation_index <= 10",
            name="ck_gemini_studio_variation_index",
        ),
        Index(
            "ix_gemini_studio_batch_lookup",
            "batch_id",
            "variation_index",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(64), unique=True, index=True, nullable=False)
    batch_id = Column(String(64), index=True, nullable=False)

    prompt_text = Column(Text, nullable=False)
    source_image_path = Column(String(1024), nullable=False)
    source_filename = Column(String(255), nullable=False)
    output_image_path = Column(String(1024), nullable=True)

    aspect_ratio = Column(String(16), index=True, nullable=False)
    category = Column(String(64), index=True, nullable=False)
    variation_index = Column(Integer, nullable=False)

    status = Column(String(64), index=True, nullable=False, default="Pending")
    error_message = Column(Text, nullable=True)
    frame_coordinates_json = Column(Text, nullable=True)
    frame_coordinates_model = Column(String(128), nullable=True)
    frame_coordinates_error = Column(Text, nullable=True)
    added_to_library = Column(Boolean, default=False, nullable=False)
    library_base_slug = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)


class EzyMockupJob(Base):
    __tablename__ = "ezy_mockup_jobs"

    __table_args__ = (
        CheckConstraint(
            "variation_index >= 1 AND variation_index <= 10",
            name="ck_ezy_mockup_variation_index",
        ),
        Index(
            "ix_ezy_mockup_batch_lookup",
            "batch_id",
            "variation_index",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(64), unique=True, index=True, nullable=False)
    batch_id = Column(String(64), index=True, nullable=False)

    prompt_text = Column(Text, nullable=False)
    source_image_path = Column(String(1024), nullable=False)
    source_filename = Column(String(255), nullable=False)

    room_output_path = Column(String(1024), nullable=True)
    mask_output_path = Column(String(1024), nullable=True)
    transparent_output_path = Column(String(1024), nullable=True)

    aspect_ratio = Column(String(16), index=True, nullable=False)
    category = Column(String(64), index=True, nullable=False)
    variation_index = Column(Integer, nullable=False)

    auto_generate_alpha = Column(Boolean, default=True, nullable=False)
    edge_smoothing = Column(Boolean, default=False, nullable=False)

    status = Column(String(64), index=True, nullable=False, default="Pending")
    error_message = Column(Text, nullable=True)
    frame_coordinates_json = Column(Text, nullable=True)
    frame_coordinates_model = Column(String(128), nullable=True)
    frame_coordinates_error = Column(Text, nullable=True)
    pipeline_stage_json = Column(Text, nullable=True)
    harmonized_output_path = Column(String(1024), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)


class PrecisionMockupJob(Base):
    __tablename__ = "precision_mockup_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(64), unique=True, index=True, nullable=False)
    batch_id = Column(String(64), index=True, nullable=False)

    prompt_text = Column(Text, nullable=False)
    source_image_path = Column(String(1024), nullable=False)
    source_filename = Column(String(255), nullable=False)

    room_output_path = Column(String(1024), nullable=True)
    transparent_output_path = Column(String(1024), nullable=True)

    aspect_ratio = Column(String(16), index=True, nullable=False)
    category = Column(String(64), index=True, nullable=False)

    status = Column(String(64), index=True, nullable=False, default="Pending")
    error_message = Column(Text, nullable=True)
    frame_coordinates_json = Column(Text, nullable=True)
    frame_coordinates_model = Column(String(128), nullable=True)
    frame_coordinates_error = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)


Base.metadata.create_all(bind=engine)


def _ensure_sqlite_runtime_columns() -> None:
    if engine.dialect.name != "sqlite":
        return

    required_columns = {
        "frame_coordinates_json": "TEXT",
        "frame_coordinates_model": "VARCHAR(128)",
        "frame_coordinates_error": "TEXT",
    }

    ezy_required_columns = {
        "pipeline_stage_json": "TEXT",
        "harmonized_output_path": "VARCHAR(1024)",
    }

    with engine.begin() as connection:
        rows = connection.execute(text("PRAGMA table_info(gemini_studio_jobs)"))
        existing = {str(row[1]) for row in rows}
        for column_name, column_type in required_columns.items():
            if column_name in existing:
                continue
            connection.execute(
                text(f"ALTER TABLE gemini_studio_jobs ADD COLUMN {column_name} {column_type}")
            )

        ezy_rows = connection.execute(text("PRAGMA table_info(ezy_mockup_jobs)"))
        ezy_existing = {str(row[1]) for row in ezy_rows}
        for column_name, column_type in ezy_required_columns.items():
            if column_name in ezy_existing:
                continue
            connection.execute(
                text(f"ALTER TABLE ezy_mockup_jobs ADD COLUMN {column_name} {column_type}")
            )


_ensure_sqlite_runtime_columns()
