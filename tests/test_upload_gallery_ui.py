from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1] / "application"


def test_unprocessed_template_actions_and_delete_only():
    tpl = (APP_ROOT / "common/ui/templates/artworks/unprocessed.html").read_text()
    assert "Generate Mockups" not in tpl
    assert "data-upload-delete-trigger" in tpl
    assert "url_for('artwork.review'" not in tpl
    assert "action-row-split" not in tpl


def test_processed_template_only_shows_review():
    tpl = (APP_ROOT / "common/ui/templates/artworks/processed.html").read_text()
    assert "Manual Analysis" not in tpl
    assert "OpenAI Analysis" not in tpl
    assert "Gemini Analysis" not in tpl
    assert "Review" in tpl or "processed-analyse" in tpl
    # Processed gallery now supports bulk delete via data-bulk-delete-trigger
    assert "data-bulk-delete-trigger" in tpl or "Delete Selected" in tpl


def test_upload_page_is_metadata_free():
    tpl = (APP_ROOT / "common/ui/templates/artworks/upload.html").read_text()
    assert "name=\"artist_name\"" not in tpl
    assert "name=\"title\"" not in tpl
    assert "data-upload-dropzone" in tpl
    assert "uploadResults" in tpl
    assert "uploadProgress" not in tpl
    assert "uploadProcessing" not in tpl
    assert "arrows-clockwise-light.svg" in tpl


def test_upload_js_polling_and_spinner_contract():
    js = (APP_ROOT / "common/ui/static/js/upload.js").read_text()
    assert "UploadController" in js
    assert "uploadDropzone" in js and "uploadFileInput" in js
    assert "XMLHttpRequest" in js
    assert "drag-over" in js
    # pollIntervalMs is a class property (this.pollIntervalMs = 1000)
    assert "pollIntervalMs = 1000" in js
    assert "activeUploads" in js
    assert "normalizeStage" in js and "isCompleteState" in js
    assert "arrows-clockwise-dark" in js and "arrows-clockwise-light" in js
    assert "All artworks processed" in js
    assert "stageValue === 'complete'" in js


def test_upload_processing_modal_structure():
    tpl = (APP_ROOT / "common/ui/templates/artworks/upload.html").read_text()
    assert "processing-modal" in tpl
    assert "processing-list" in tpl
    assert "processingBackgroundBtn" in tpl
    assert "processingCloseBtn" in tpl
    assert "Run in background" in tpl
    assert "Preparing uploads…" in tpl
    assert "Uploading &amp; Processing Artworks" in tpl


def test_modal_opens_immediately_and_auto_closes_on_done():
    js = (APP_ROOT / "common/ui/static/js/upload.js").read_text()
    assert "showProcessingOverlay();" in js
    assert "hideProcessingOverlay(true);" in js
    assert "All artworks processed" in js


def test_no_progress_bars_rendered():
    tpl = (APP_ROOT / "common/ui/templates/artworks/upload.html").read_text()
    assert "progress-bar" not in tpl
    assert "progress" not in tpl.lower()


def test_error_state_stops_polling():
    js = (APP_ROOT / "common/ui/static/js/upload.js").read_text()
    # Error handling uses state.error and hasError pattern, not a named handleError function
    assert "state.error" in js or "hasError" in js
    assert "clearInterval" in js and "error" in js


def test_delete_modal_global_disabled_for_artworks_pages():
    js = (APP_ROOT / "common/ui/static/js/delete-modal.js").read_text()
    assert "pathname.startsWith('/artworks')" in js


def test_status_endpoint_uses_unprocessed_status_file():
    py = (APP_ROOT / "upload/routes/upload_routes.py").read_text()
    assert "LAB_UNPROCESSED_DIR" in py
    assert "processing_status" in py
    assert "processing_status(slug" in py
    assert "Not found" in py


def test_review_routes_and_targets_exist():
    py = (APP_ROOT / "artwork/routes/artwork_routes.py").read_text()
    assert "review_openai" in py
    assert "review_gemini" in py
    assert "manual.workspace" in py


def test_manual_workspace_lock_and_title_save_hooks():
    tpl = (APP_ROOT / "common/ui/templates/analysis_workspace.html").read_text()
    assert "data-analysis-lock" in tpl
    py_service = (APP_ROOT / "analysis/manual/services/manual_service.py").read_text()
    assert "meta_path" in py_service and "metadata.json" in py_service
    py_routes = (APP_ROOT / "analysis/manual/routes/manual_routes.py").read_text()
    assert "locked and cannot be edited" in py_routes


def test_upload_gallery_poll_status_uses_slug_not_sku():
    js = (APP_ROOT / "common/ui/static/js/upload_gallery.js").read_text()
    assert "pollStatus = async ({ slug" in js
    assert "/api/analysis/status/${encodeURIComponent(slug)}" in js
    assert "/api/analysis/status/${encodeURIComponent(sku)}" not in js
