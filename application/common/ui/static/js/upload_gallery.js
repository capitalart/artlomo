// Custom delete modal controller for artworks pages (Bootstrap-free)

document.addEventListener('DOMContentLoaded', () => {
  // -------------------------
  // Delete modal logic
  // -------------------------
  const modal = document.getElementById('uploadDeleteModal');
  const hasDeleteModal = Boolean(modal);

  const csrfToken = (() => {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? (meta.getAttribute('content') || '').trim() : '';
  })();

  const postJson = async (url, payload) => {
    const resp = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-CSRF-Token': csrfToken,
      },
      body: JSON.stringify(payload || {}),
      credentials: 'same-origin',
    });
    let data = null;
    try {
      data = await resp.json();
    } catch (e) {
      data = null;
    }
    return { resp, data };
  };

  const pollStatus = async ({ slug, onUpdate, timeoutMs = 60 * 1000 }) => {
    const start = Date.now();
    let lastData = null;
    while (Date.now() - start < timeoutMs) {
      let resp;
      let data;
      try {
        resp = await fetch(`/api/analysis/status/${encodeURIComponent(slug)}`, {
          headers: { 'Accept': 'application/json' },
          credentials: 'same-origin',
        });
        data = await resp.json();
      } catch (e) {
        await new Promise((r) => setTimeout(r, 750));
        continue;
      }

      if (resp && resp.ok && data) {
        lastData = data;
      }

      if (typeof onUpdate === 'function') onUpdate({ resp, data });

      if (resp && resp.ok && data && data.done) return data;

      await new Promise((r) => setTimeout(r, 750));
    }

    const stage = ((lastData && lastData.stage) || '').toString().toLowerCase();
    const lastMessage = (lastData && (lastData.error || lastData.message)) || '';

    if (stage === 'queued') {
      return {
        status: 'error',
        stage,
        error: 'Analysis queue is still queued. The analysis worker may be offline.',
        message: lastMessage || 'Analysis queue is still queued. The analysis worker may be offline.',
      };
    }

    return {
      status: 'error',
      stage: stage || 'timeout',
      error: lastMessage || 'Analysis timed out before completion.',
      message: lastMessage || 'Analysis timed out before completion.',
    };
  };

  const setFailedState = (el) => {
    if (!(el instanceof HTMLElement)) return;
    el.textContent = 'Analysis Failed - Try Again';
    el.classList.remove('disabled');
    el.removeAttribute('aria-disabled');
    el.classList.add('btn-stark-red');
  };

  // -------------------------
  // Bulk selection UI
  // -------------------------
  const bulkSelectAll = document.querySelector('[data-bulk-select-all]');
  const bulkDeselectAll = document.querySelector('[data-bulk-deselect-all]');
  const bulkCount = document.querySelector('[data-bulk-count]');
  const bulkDeleteTrigger = document.querySelector('[data-bulk-delete-trigger]');
  const bulkCheckboxes = () => Array.from(document.querySelectorAll('[data-bulk-select]'));
  const selectedCheckboxes = () => bulkCheckboxes().filter((cb) => cb instanceof HTMLInputElement && cb.checked);
  const bulkSize = () => bulkCheckboxes().length;

  const setAll = (checked) => {
    bulkCheckboxes().forEach((cb) => {
      if (cb instanceof HTMLInputElement) cb.checked = checked;
    });
  };

  const updateBulkUI = () => {
    const selected = selectedCheckboxes().length;
    const total = bulkSize();
    if (bulkCount) {
      bulkCount.textContent = `${selected} Selected`;
      bulkCount.hidden = selected === 0;
    }
    if (bulkSelectAll && bulkSelectAll instanceof HTMLInputElement) {
      bulkSelectAll.checked = total > 0 && selected === total;
      bulkSelectAll.indeterminate = selected > 0 && selected < total;
    }
    if (bulkDeleteTrigger) bulkDeleteTrigger.disabled = selected === 0;
  };

  const dialog = hasDeleteModal ? modal.querySelector('.upload-modal-dialog') : null;
  const backdrop = hasDeleteModal ? modal.querySelector('.upload-modal-backdrop') : null;
  const thumbEl = hasDeleteModal ? modal.querySelector('[data-delete-thumb]') : null;
  const slugEl = hasDeleteModal ? modal.querySelector('[data-delete-slug]') : null;
  const idEl = hasDeleteModal ? modal.querySelector('[data-delete-id]') : null;
  const inputEl = hasDeleteModal ? modal.querySelector('[data-delete-input]') : null;
  const errorEl = hasDeleteModal ? modal.querySelector('[data-delete-error]') : null;
  const confirmBtn = hasDeleteModal ? modal.querySelector('[data-delete-confirm]') : null;
  const dismissButtons = hasDeleteModal ? modal.querySelectorAll('[data-delete-dismiss]') : [];

  const focusableSelector = 'a[href], button:not([disabled]), input:not([disabled]), textarea:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])';

  let activeButton = null;
  let lastFocused = null;
  let bulkDeleteQueue = null;
  let mode = 'unprocessed';

  const confirmLabel = () => (mode === 'processed' ? 'Confirm' : 'Confirm Delete');

  const openaiLinks = Array.from(document.querySelectorAll('[data-openai-async]'));
  openaiLinks.forEach((el) => {
    el.addEventListener('click', async (event) => {
      if (!(el instanceof HTMLElement)) return;
      event.preventDefault();
      const slug = (el.getAttribute('data-slug') || '').trim();
      const sku = (el.getAttribute('data-sku') || '').trim();
      if (!slug || !sku) return;

      const originalText = el.textContent;
      el.setAttribute('aria-disabled', 'true');
      el.classList.add('disabled');
      el.textContent = 'Queued…';

      const { resp, data } = await postJson(`/api/analysis/openai/${encodeURIComponent(slug)}`, { csrf_token: csrfToken });
      if (!resp.ok) {
        el.textContent = 'Error';
        el.classList.remove('disabled');
        el.removeAttribute('aria-disabled');
        window.alert((data && (data.message || data.error)) || 'Failed to start OpenAI analysis');
        el.textContent = originalText;
        return;
      }

      // Show animated spinner overlay
      if (typeof AnalysisLoader !== 'undefined') {
        AnalysisLoader.show('OpenAI');
      }

      el.textContent = 'Processing…';

      const result = await pollStatus({
        slug,
        onUpdate: ({ data: status }) => {
          if (!status) return;
          const stage = (status.stage || '').toString();
          if (stage) el.textContent = `Processing… (${stage})`;
        },
      });

      if (!result) {
        if (typeof AnalysisLoader !== 'undefined') {
          AnalysisLoader.showError('Analysis timed out - no response from server');
        }
        el.textContent = originalText;
        el.classList.remove('disabled');
        el.removeAttribute('aria-disabled');
        window.alert('Timed out waiting for analysis to complete');
        return;
      }

      if (result.status === 'error' || result.error) {
        if (typeof AnalysisLoader !== 'undefined') {
          AnalysisLoader.showError(result.message || result.error || 'Analysis failed');
        }
        setFailedState(el);
        window.alert((result && (result.message || result.error)) || 'Analysis failed');
        return;
      }

      if (typeof AnalysisLoader !== 'undefined') {
        AnalysisLoader.hide();
      }
      window.location.href = `/artwork/${encodeURIComponent(slug)}/review/openai`;
    });
  });

  const geminiLinks = Array.from(document.querySelectorAll('[data-gemini-async]'));
  geminiLinks.forEach((el) => {
    el.addEventListener('click', async (event) => {
      if (!(el instanceof HTMLElement)) return;
      event.preventDefault();
      const slug = (el.getAttribute('data-slug') || '').trim();
      const sku = (el.getAttribute('data-sku') || '').trim();
      if (!slug || !sku) return;

      const originalText = el.textContent;
      el.setAttribute('aria-disabled', 'true');
      el.classList.add('disabled');
      el.textContent = 'Queued…';

      const { resp, data } = await postJson(`/api/analysis/gemini/${encodeURIComponent(slug)}`, { csrf_token: csrfToken });
      if (!resp.ok) {
        el.textContent = 'Error';
        el.classList.remove('disabled');
        el.removeAttribute('aria-disabled');
        window.alert((data && (data.message || data.error)) || 'Failed to start Gemini analysis');
        el.textContent = originalText;
        return;
      }

      // Show animated spinner overlay
      if (typeof AnalysisLoader !== 'undefined') {
        AnalysisLoader.show('Gemini');
      }

      el.textContent = 'Processing…';

      const result = await pollStatus({
        slug,
        onUpdate: ({ data: status }) => {
          if (!status) return;
          const stage = (status.stage || '').toString();
          if (stage) el.textContent = `Processing… (${stage})`;
        },
      });

      if (!result) {
        if (typeof AnalysisLoader !== 'undefined') {
          AnalysisLoader.showError('Analysis timed out - no response from server');
        }
        el.textContent = originalText;
        el.classList.remove('disabled');
        el.removeAttribute('aria-disabled');
        window.alert('Timed out waiting for analysis to complete');
        return;
      }

      if (result.status === 'error' || result.error) {
        if (typeof AnalysisLoader !== 'undefined') {
          AnalysisLoader.showError(result.message || result.error || 'Analysis failed');
        }
        setFailedState(el);
        window.alert((result && (result.message || result.error)) || 'Analysis failed');
        return;
      }

      if (typeof AnalysisLoader !== 'undefined') {
        AnalysisLoader.hide();
      }
      window.location.href = `/artwork/${encodeURIComponent(slug)}/review/gemini`;
    });
  });

  const lockBody = (locked) => {
    document.body.classList.toggle('overlay-lock', locked);
    document.body.classList.toggle('upload-modal-open', locked);
  };

  const resetForm = () => {
    if (inputEl) inputEl.value = '';
    if (errorEl) errorEl.textContent = '';
    if (confirmBtn) {
      confirmBtn.disabled = true;
      confirmBtn.dataset.loading = 'false';
      confirmBtn.textContent = confirmLabel();
    }
  };

  const getFocusable = () => Array.from(modal ? modal.querySelectorAll(focusableSelector) : [])
    .filter((el) => !el.hasAttribute('disabled') && el.getAttribute('tabindex') !== '-1' && el.offsetParent !== null);

  const focusFirstField = () => {
    if (inputEl && !inputEl.hasAttribute('disabled') && inputEl.hidden !== true) {
      inputEl.focus({ preventScroll: true });
      return;
    }
    const focusables = getFocusable();
    if (focusables.length) {
      focusables[0].focus({ preventScroll: true });
    }
  };

  const setModalVisibility = (open) => {
    if (!modal) return;
    modal.classList.toggle('hidden', !open);
    modal.setAttribute('aria-hidden', open ? 'false' : 'true');
    lockBody(open);
  };

  const closeModal = () => {
    setModalVisibility(false);
    resetForm();
    bulkDeleteQueue = null;
    const target = activeButton || lastFocused;
    if (target && typeof target.focus === 'function') {
      target.focus({ preventScroll: true });
    }
    activeButton = null;
  };

  const openModal = (btn) => {
    activeButton = btn;
    lastFocused = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    mode = (btn.dataset.deleteMode || 'unprocessed').trim() || 'unprocessed';
    const slug = btn.dataset.slug || '';
    const artworkId = btn.dataset.id || slug;
    const thumbUrl = btn.dataset.thumbUrl || '';
    if (slugEl) slugEl.textContent = slug;
    if (idEl) idEl.textContent = artworkId;
    if (thumbEl) {
      thumbEl.src = thumbUrl;
      thumbEl.alt = slug ? `${slug} thumbnail` : 'Artwork thumbnail';
    }
    resetForm();
    // Both modes require typing "DELETE" for confirmation (Clean-Room v2.0 standard)
    if (inputEl) {
      inputEl.hidden = false;
      inputEl.removeAttribute('disabled');
    }
    const label = modal.querySelector('.delete-modal__label');
    if (label) {
      label.hidden = false;
    }
    if (confirmBtn && confirmBtn.dataset.loading !== 'true') {
      confirmBtn.disabled = true;  // Always disabled until "DELETE" is typed
      confirmBtn.textContent = confirmLabel();
    }
    setModalVisibility(true);
    focusFirstField();
  };

  const openBulkModal = (queue, bulkMode) => {
    bulkDeleteQueue = Array.isArray(queue) ? queue : [];
    activeButton = null;
    lastFocused = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    mode = (bulkMode || 'unprocessed').trim() || 'unprocessed';
    if (slugEl) slugEl.textContent = `${bulkDeleteQueue.length} selected`;
    if (idEl) idEl.textContent = '';
    if (thumbEl) {
      thumbEl.src = '';
      thumbEl.alt = 'Artwork thumbnail';
    }
    resetForm();
    // Both modes require typing "DELETE" for confirmation (Clean-Room v2.0 standard)
    if (inputEl) {
      inputEl.hidden = false;
      inputEl.removeAttribute('disabled');
    }
    const label = modal.querySelector('.delete-modal__label');
    if (label) label.hidden = false;
    if (confirmBtn && confirmBtn.dataset.loading !== 'true') {
      confirmBtn.disabled = true;  // Always disabled until "DELETE" is typed
      confirmBtn.textContent = confirmLabel();
    }
    setModalVisibility(true);
    focusFirstField();
  };

  const validate = () => {
    // Both unprocessed and processed modes require typing "DELETE" (Clean-Room v2.0 standard)
    const val = (inputEl && inputEl.value) ? inputEl.value.trim() : '';
    const ok = val.toUpperCase() === 'DELETE';
    if (confirmBtn && confirmBtn.dataset.loading !== 'true') {
      confirmBtn.disabled = !ok;
    }
    if (errorEl) errorEl.textContent = '';
  };

  const performDelete = async (event) => {
    if (event) event.preventDefault();
    if (!confirmBtn) return;
    confirmBtn.disabled = true;
    confirmBtn.dataset.loading = 'true';
    confirmBtn.textContent = 'Deleting...';
    if (errorEl) errorEl.textContent = '';

    try {
      if (bulkDeleteQueue && bulkDeleteQueue.length) {
        for (let i = 0; i < bulkDeleteQueue.length; i += 1) {
          const entry = bulkDeleteQueue[i];
          if (!entry || !entry.deleteUrl) continue;
          const resp = await fetch(entry.deleteUrl, {
            method: 'POST',
            headers: Object.assign(
              { 'X-Requested-With': 'XMLHttpRequest' },
              csrfToken ? { 'X-CSRFToken': csrfToken } : {},
            ),
            body: new URLSearchParams({ slug: entry.slug || '' }),
          });
          if (!resp.ok) {
            const text = await resp.text();
            throw new Error(text || `Delete failed (${resp.status})`);
          }
          if (entry.card) entry.card.remove();
        }
        updateBulkUI();
      } else {
        if (!activeButton) return;
        const deleteUrl = activeButton.dataset.deleteUrl;
        if (!deleteUrl) return;
        const resp = await fetch(deleteUrl, {
          method: 'POST',
          headers: Object.assign(
            { 'X-Requested-With': 'XMLHttpRequest' },
            csrfToken ? { 'X-CSRFToken': csrfToken } : {},
          ),
          body: new URLSearchParams({ slug: activeButton.dataset.slug || '' }),
        });
        if (!resp.ok) {
          const text = await resp.text();
          throw new Error(text || `Delete failed (${resp.status})`);
        }
        const card = activeButton.closest('.gallery-card');
        if (card) card.remove();
        updateBulkUI();
      }
      closeModal();
    } catch (err) {
      if (errorEl) errorEl.textContent = err instanceof Error ? err.message : 'Delete failed';
      confirmBtn.disabled = false;
      confirmBtn.dataset.loading = 'false';
      confirmBtn.textContent = confirmLabel();
    }
  };

  document.querySelectorAll('[data-upload-delete-trigger]').forEach((btn) => {
    btn.addEventListener('click', (event) => {
      event.preventDefault();
      openModal(btn);
    });
  });

  if (bulkSelectAll) {
    if (bulkSelectAll instanceof HTMLInputElement) {
      bulkSelectAll.addEventListener('change', () => {
        setAll(bulkSelectAll.checked);
        updateBulkUI();
      });
    } else {
      bulkSelectAll.addEventListener('click', (event) => {
        event.preventDefault();
        setAll(true);
        updateBulkUI();
      });
    }
  }

  if (bulkDeselectAll) {
    bulkDeselectAll.addEventListener('click', (event) => {
      event.preventDefault();
      setAll(false);
      updateBulkUI();
    });
  }

  bulkCheckboxes().forEach((cb) => {
    cb.addEventListener('change', () => updateBulkUI());
  });

  if (bulkDeleteTrigger) {
    bulkDeleteTrigger.addEventListener('click', (event) => {
      event.preventDefault();
      const queue = selectedCheckboxes().map((cb) => {
        const slug = cb.dataset.slug || '';
        const card = cb.closest('.gallery-card');
        const deleteBtn = card ? card.querySelector('[data-upload-delete-trigger]') : null;
        const deleteUrl = deleteBtn && deleteBtn instanceof HTMLElement ? deleteBtn.dataset.deleteUrl : null;
        return { slug, deleteUrl, card };
      }).filter((entry) => entry && entry.deleteUrl);
      if (!queue.length) return;
      const bulkMode = (bulkDeleteTrigger.dataset.deleteMode || '').trim() || 'unprocessed';
      openBulkModal(queue, bulkMode);
    });
  }

  updateBulkUI();

  if (inputEl) inputEl.addEventListener('input', validate);
  if (confirmBtn) confirmBtn.addEventListener('click', performDelete);
  dismissButtons.forEach((btn) => btn.addEventListener('click', (event) => {
    event.preventDefault();
    closeModal();
  }));

  if (backdrop) {
    backdrop.addEventListener('click', (event) => {
      event.preventDefault();
      closeModal();
    });
  }

  if (dialog) {
    dialog.addEventListener('click', (event) => {
      event.stopPropagation();
    });
  }

  if (modal) {
    modal.addEventListener('click', (event) => {
      if (event.target === modal) {
        event.preventDefault();
        closeModal();
      }
    });

    document.addEventListener('keydown', (event) => {
      if (modal.classList.contains('hidden')) return;
      if (event.key === 'Escape') {
        event.preventDefault();
        closeModal();
        return;
      }
      if (event.key === 'Tab') {
        const focusables = getFocusable();
        if (!focusables.length) return;
        const first = focusables[0];
        const last = focusables[focusables.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus({ preventScroll: true });
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus({ preventScroll: true });
        }
      }
    });
  }
});
