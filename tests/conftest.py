import sys
import time
from pathlib import Path

import pytest

# Ensure application package is importable when running pytest from the repo root.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def app(tmp_path):
    """Create a Flask app configured for isolated test lab paths."""
    from application.app import create_app

    flask_app = create_app()
    lab_dir = tmp_path / "lab"
    unprocessed_dir = lab_dir / "unprocessed"
    processed_dir = lab_dir / "processed"
    locked_dir = lab_dir / "locked"
    index_dir = lab_dir / "index"
    for path in (unprocessed_dir, processed_dir, locked_dir, index_dir):
        path.mkdir(parents=True, exist_ok=True)

    flask_app.config.update(
        TESTING=True,
        LAB_DIR=lab_dir,
        LAB_UNPROCESSED_DIR=unprocessed_dir,
        LAB_PROCESSED_DIR=processed_dir,
        LAB_LOCKED_DIR=locked_dir,
        LAB_INDEX_DIR=index_dir,
        ARTWORKS_INDEX_PATH=index_dir / "artworks.json",
        SECRET_KEY="test-secret-key",
    )
    return flask_app


@pytest.fixture
def app_client(app):
    """Create an authenticated test client with a valid CSRF token."""
    with app.test_client() as client:
        now = float(time.time())
        with client.session_transaction() as sess:
            sess["username"] = "pytest-user"
            sess["is_admin"] = True
            sess["login_ts"] = now
            sess["last_activity_ts"] = now
            sess["_csrf_token"] = "test-csrf-token"

        client.csrf_token = "test-csrf-token"
        yield client
