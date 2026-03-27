// Upload page controller: strict status-driven modal lifecycle with reliable drag-and-drop.

document.addEventListener('DOMContentLoaded', () => {
  class UploadController {
    constructor() {
      this.dropzone = document.getElementById('upload-dropzone') || document.getElementById('uploadDropzone');
      this.fileInput = document.getElementById('upload-input') || document.getElementById('uploadFileInput');
      this.statusEl = document.getElementById('uploadStatus');
      this.resultsEl = document.getElementById('uploadResults');
      this.processingOverlay = document.getElementById('processing-modal');
      this.processingOverlayList = document.getElementById('processing-list');
      this.processingMessageText = document.getElementById('processingMessageText');
      this.processingCloseBtn = document.getElementById('processingCloseBtn');
      this.processingBackgroundBtn = document.getElementById('processingBackgroundBtn');
      this.uploadEndpoint = this.dropzone ? this.dropzone.dataset.uploadEndpoint : null;
      this.MAX_BYTES = 50 * 1024 * 1024; // 50MB per-file UI guard
      this.activeUploads = new Map(); // slug -> { intervalId, state }
      this.batchExpectedTotal = 0;
      this.batchSlugs = new Set();
      this.overlaySuppressed = false;
      this.overlayCloseTimer = null;
      this.pollIntervalMs = 1000;

      this.csrf = (() => {
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? (meta.getAttribute('content') || '').trim() : '';
      })();

      if (!this.dropzone || !this.fileInput || !this.uploadEndpoint) return;

      if (this.processingCloseBtn) this.processingCloseBtn.disabled = false;
      this.applyThemeToSpinners();
      this.observeThemeChanges();
      this.bindDropzone();
      this.bindControls();
    }

    observeThemeChanges() {
      if (!document.body) return;
      const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
          if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
            this.applyThemeToSpinners();
          }
        });
      });
      observer.observe(document.body, { attributes: true, attributeFilter: ['data-theme'] });
    }

    setStatus(message, tone = 'info') {
      if (!this.statusEl) return;
      this.statusEl.textContent = message;
      this.statusEl.dataset.state = tone;
    }

    clearStatus() {
      this.setStatus('', '');
    }

    spinnerSrc() {
      const themeHost = document.body;
      const theme = (themeHost && themeHost.dataset && themeHost.dataset.theme) || 'light';
      return theme === 'dark'
        ? '/static/icons/arrows-clockwise-dark.svg'
        : '/static/icons/arrows-clockwise-light.svg';
    }

    createSpinner() {
      const spinner = document.createElement('img');
      spinner.className = 'processing-icon spinning';
      spinner.src = this.spinnerSrc();
      spinner.alt = '';
      spinner.setAttribute('aria-hidden', 'true');
      return spinner;
    }

    applyThemeToSpinners() {
      const icons = this.processingOverlay ? this.processingOverlay.querySelectorAll('.processing-icon') : [];
      icons.forEach((icon) => {
        icon.src = this.spinnerSrc();
      });
    }

    stageLabel(stage) {
      const map = {
        uploaded: 'Preparing uploads…',
        queued: 'Preparing uploads…',
        preparing: 'Preparing uploads…',
        uploading: 'Uploading files…',
        upload_complete: 'Upload complete. Processing artwork…',
        processing: 'Processing artwork…',
        qc: 'Quality checking artwork…',
        thumbnail: 'Generating thumbnails…',
        derivatives: 'Generating artwork files…',
        writing_metadata: 'Writing metadata…',
        metadata: 'Writing metadata…',
        finalizing: 'Finalizing artwork…',
        done: 'Processing complete',
        complete: 'Processing complete',
        error: 'Error',
      };
      return map[stage] || 'Preparing uploads…';
    }

    setModalMessage(text) {
      if (this.processingMessageText) this.processingMessageText.textContent = text;
    }

    bindDropzone() {
      const dz = this.dropzone;
      const fi = this.fileInput;

      dz.addEventListener('click', (event) => {
        event.preventDefault();
        event.stopPropagation();
        fi.click();
      });

      dz.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          event.stopPropagation();
          fi.click();
        }
      });

      fi.addEventListener('change', () => {
        if (fi.files && fi.files.length) this.handleFiles(fi.files);
        fi.value = '';
      });

      ['dragenter', 'dragover'].forEach((evt) => {
        dz.addEventListener(evt, (event) => {
          event.preventDefault();
          event.stopPropagation();
          dz.classList.add('drag-over');
        });
      });

      dz.addEventListener('dragleave', (event) => {
        event.preventDefault();
        event.stopPropagation();
        dz.classList.remove('drag-over');
      });

      dz.addEventListener('drop', (event) => {
        event.preventDefault();
        event.stopPropagation();
        dz.classList.remove('drag-over');
        if (event.dataTransfer && event.dataTransfer.files && event.dataTransfer.files.length) {
          this.handleFiles(event.dataTransfer.files);
        }
      });

      // Prevent browser from opening files when dropped outside the dropzone.
      ['dragover', 'drop'].forEach((evt) => {
        document.addEventListener(evt, (event) => {
          event.preventDefault();
        });
      });
    }

    bindControls() {
      if (this.processingBackgroundBtn) {
        this.processingBackgroundBtn.addEventListener('click', (event) => {
          event.preventDefault();
          this.overlaySuppressed = true;
          this.hideProcessingOverlay(true);
        });
      }

      if (this.processingCloseBtn) {
        this.processingCloseBtn.addEventListener('click', (event) => {
          event.preventDefault();
          this.overlaySuppressed = true;
          this.hideProcessingOverlay(true);
        });
      }
    }

    resetBatch() {
      if (this.resultsEl) this.resultsEl.innerHTML = '';
      if (this.processingOverlayList) this.processingOverlayList.innerHTML = '';
      this.stopAllPolling();
      this.batchExpectedTotal = 0;
      this.batchSlugs.clear();
      if (this.overlayCloseTimer) {
        clearTimeout(this.overlayCloseTimer);
        this.overlayCloseTimer = null;
      }
      this.overlaySuppressed = false;
      this.hideProcessingOverlay(true);
    }

    stopAllPolling() {
      this.activeUploads.forEach((entry) => {
        if (entry.intervalId) clearInterval(entry.intervalId);
      });
      this.activeUploads.clear();
    }

    validateFiles(fileList) {
      const accepted = [];
      const rejected = [];
      Array.from(fileList || []).forEach((file) => {
        const isJpg = file && (file.type === 'image/jpeg' || file.name.toLowerCase().endsWith('.jpg') || file.name.toLowerCase().endsWith('.jpeg'));
        if (!isJpg) {
          rejected.push(`${file.name} (not JPG)`);
          return;
        }
        if (file.size > this.MAX_BYTES) {
          rejected.push(`${file.name} (>50MB)`);
          return;
        }
        accepted.push(file);
      });
      return { accepted, rejected };
    }

    async handleFiles(fileList) {
      if (!fileList || !fileList.length) return;
      this.resetBatch();
      const { accepted, rejected } = this.validateFiles(fileList);
      if (rejected.length) this.setStatus(`Rejected: ${rejected.join('; ')}`, 'warning');
      if (!accepted.length) return;

      this.batchExpectedTotal = accepted.length;

      this.setStatus(`Uploading ${accepted.length} file(s)...`, 'info');
      this.setModalMessage('Preparing uploads…');
      this.showProcessingOverlay();

      for (let i = 0; i < accepted.length; i += 1) {
        const file = accepted[i];
        try {
          this.setModalMessage('Uploading files…');
          const payload = await this.uploadFile(file);
          this.appendResult(payload);
        } catch (err) {
          this.setStatus(err instanceof Error ? err.message : 'Upload failed', 'danger');
          if (!this.activeUploads.size) this.hideProcessingOverlay(true);
          return;
        }
      }

      this.setStatus('Uploads sent. Awaiting processing…', 'info');
      this.setModalMessage('Upload complete. Processing artwork…');
    }

    uploadFile(file) {
      return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', this.uploadEndpoint);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        if (this.csrf) xhr.setRequestHeader('X-CSRFToken', this.csrf);

        xhr.onreadystatechange = () => {
          if (xhr.readyState !== XMLHttpRequest.DONE) return;
          if (xhr.status >= 200 && xhr.status < 300) {
            try {
              const data = JSON.parse(xhr.responseText || '{}');
              if (!data || data.status !== 'ok' || !data.slug) {
                reject(new Error('Upload response malformed'));
                return;
              }
              resolve(data);
            } catch (err) {
              reject(err);
            }
          } else {
            let message = `Upload failed (${xhr.status})`;
            try {
              const data = JSON.parse(xhr.responseText || '{}');
              if (data && data.message) message = data.message;
            } catch (err) {
              if (xhr.responseText) message = xhr.responseText;
            }
            reject(new Error(message));
          }
        };

        const formData = new FormData();
        formData.append('artwork', file);
        xhr.send(formData);
      });
    }

    appendResult({ slug, thumb_url: thumbUrl, unprocessed_url: unprocessedUrl }) {
      if (this.resultsEl) {
        const row = document.createElement('a');
        row.href = unprocessedUrl;
        row.className = 'upload-result-row';
        row.setAttribute('aria-label', `Open unprocessed artwork ${slug}`);

        const img = document.createElement('img');
        img.className = 'upload-result-thumb';
        img.src = thumbUrl;
        img.alt = `${slug} thumbnail`;
        img.loading = 'lazy';

        const meta = document.createElement('div');
        meta.className = 'upload-result-meta';

        const title = document.createElement('p');
        title.className = 'upload-result-title';
        title.textContent = slug;

        const status = document.createElement('p');
        status.className = 'upload-result-status';
        status.textContent = 'Unprocessed';

        meta.appendChild(title);
        meta.appendChild(status);
        row.appendChild(img);
        row.appendChild(meta);
        this.resultsEl.appendChild(row);
      }

      this.batchSlugs.add(slug);
      this.startProcessing(slug, thumbUrl);
    }

    ensureProcessingRow(slug, thumbUrl) {
      const container = this.processingOverlayList;
      if (!container) return null;
      let row = container.querySelector(`[data-processing-slug="${slug}"]`);
      if (row) return row;

      row = document.createElement('div');
      row.className = 'processing-row';
      row.dataset.processingSlug = slug;

      const img = document.createElement('img');
      img.className = 'processing-thumb';
      img.src = thumbUrl;
      img.alt = `${slug} thumbnail`;
      img.loading = 'lazy';

      const meta = document.createElement('div');
      meta.className = 'processing-meta';
      const title = document.createElement('p');
      title.className = 'processing-title';
      title.textContent = slug;
      const status = document.createElement('p');
      status.className = 'processing-status';
      status.textContent = 'Processing…';
      meta.appendChild(title);
      meta.appendChild(status);

      const action = document.createElement('div');
      action.className = 'processing-action';
      action.appendChild(this.createSpinner());

      row.appendChild(img);
      row.appendChild(meta);
      row.appendChild(action);
      container.appendChild(row);
      return row;
    }

    normalizeStage(rawStage) {
      const stage = (rawStage || 'queued').toString().toLowerCase();
      if (stage === 'done') return 'complete';
      return stage;
    }

    isCompleteState(state) {
      if (!state) return false;
      const stage = this.normalizeStage(state.stage);
      return !state.error && (state.done === true || stage === 'complete');
    }

    renderRow(slug, stage, message, done, errorText) {
      const existing = this.activeUploads.get(slug) || {};
      const row = this.ensureProcessingRow(slug, existing.thumbUrl || '');
      if (!row) return;
      const friendly = errorText || message || this.stageLabel(stage) || 'Preparing uploads…';
      const statusElRow = row.querySelector('.processing-status');
      const actionEl = row.querySelector('.processing-action');
      if (statusElRow) statusElRow.textContent = friendly;
      if (!actionEl) return;
      actionEl.innerHTML = '';
      if (!done && !errorText) {
        actionEl.appendChild(this.createSpinner());
      }
    }

    appendContinueButton() {
      if (!this.resultsEl) return;
      const existingContinue = this.resultsEl.querySelector('[data-continue-to-unprocessed]');
      if (existingContinue) return;

      const wrap = document.createElement('div');
      wrap.className = 'upload-results-continue';

      const btn = document.createElement('a');
      btn.href = '/artworks/unprocessed';
      btn.className = 'btn btn-stark-outline upload-results-continue-btn';
      btn.dataset.continueToUnprocessed = '1';
      btn.textContent = 'Continue to Process these Artworks';
      btn.setAttribute('aria-label', 'Continue to Process these Artworks');

      wrap.appendChild(btn);
      this.resultsEl.appendChild(wrap);
    }

    evaluateCompletion() {
      if (!this.activeUploads.size) return false;

      const expectedTotal = Number(this.batchExpectedTotal) || 0;
      const knownTotal = this.batchSlugs.size;
      const slugs = knownTotal ? Array.from(this.batchSlugs) : Array.from(this.activeUploads.keys());
      const entries = slugs.map((slug) => this.activeUploads.get(slug)).filter(Boolean);

      const completeCount = entries.reduce((count, entry) => (this.isCompleteState(entry.state) ? count + 1 : count), 0);
      if (expectedTotal > 0) {
        console.log(`Batch status: ${completeCount} of ${expectedTotal} complete`);
      }

      // Never close early: wait until we've seen all slugs for this batch.
      if (expectedTotal > 0 && knownTotal < expectedTotal) return false;

      const allComplete = entries.length > 0 && entries.every((entry) => this.isCompleteState(entry.state));
      const allTerminal = entries.length > 0 && entries.every((entry) => this.isCompleteState(entry.state) || (entry.state && entry.state.error));

      if (allComplete) {
        this.setModalMessage('All artworks processed');
        this.appendContinueButton();
        this.stopAllPolling();
        this.hideProcessingOverlay(true);
      } else if (allTerminal) {
        this.stopAllPolling();
      }

      return allComplete;
    }

    async pollOnce(slug) {
      if (!this.activeUploads.has(slug)) return;
      try {
        const resp = await fetch(`/artworks/${encodeURIComponent(slug)}/status`, { headers: { Accept: 'application/json' } });
        const data = resp.ok ? await resp.json() : { error: 'Status unavailable', stage: 'queued', done: false };
        const stageValue = this.normalizeStage(data.stage);
        const isDone = Boolean(data && data.done) || stageValue === 'complete';
        const hasError = Boolean(data && data.error);
        const message = data && data.message ? data.message : this.stageLabel(stageValue);

        const existing = this.activeUploads.get(slug) || {};
        this.activeUploads.set(slug, { ...existing, state: { stage: stageValue, done: isDone, error: hasError ? data.error : null } });

        this.renderRow(slug, stageValue, message, isDone, hasError ? data.error : null);

        if (hasError || isDone) {
          if (existing.intervalId) clearInterval(existing.intervalId);
        }

        this.evaluateCompletion();
      } catch (err) {
        // Keep polling; show minimal feedback.
        this.renderRow(slug, 'queued', this.stageLabel('queued'), false, null);
      }
    }

    startProcessing(slug, thumbUrl) {
      this.ensureProcessingRow(slug, thumbUrl);

      const poll = () => this.pollOnce(slug);

      this.activeUploads.set(slug, { intervalId: null, state: { stage: 'queued', done: false, error: null }, thumbUrl });
      poll();
      const intervalId = setInterval(poll, this.pollIntervalMs);
      const entry = this.activeUploads.get(slug) || {};
      this.activeUploads.set(slug, { ...entry, intervalId });
      this.showProcessingOverlay();
    }

    showProcessingOverlay() {
      if (!this.processingOverlay || this.overlaySuppressed) return;
      this.applyThemeToSpinners();
      this.processingOverlay.classList.remove('hidden', 'closing');
      this.processingOverlay.setAttribute('aria-hidden', 'false');
      document.body.classList.add('overlay-lock');
    }

    hideProcessingOverlay(immediate = false) {
      if (!this.processingOverlay) return;
      if (this.overlayCloseTimer) {
        clearTimeout(this.overlayCloseTimer);
        this.overlayCloseTimer = null;
      }
      if (immediate) {
        this.processingOverlay.classList.add('hidden');
        this.processingOverlay.classList.remove('closing');
        this.processingOverlay.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('overlay-lock');
        return;
      }
      const delay = 300;
      this.processingOverlay.classList.add('closing');
      this.overlayCloseTimer = setTimeout(() => {
        this.processingOverlay.classList.add('hidden');
        this.processingOverlay.classList.remove('closing');
        this.processingOverlay.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('overlay-lock');
        this.overlayCloseTimer = null;
      }, delay);
    }
  }

  new UploadController();
});
