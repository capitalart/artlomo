(function () {
  const STORAGE_KEY = 'mockupAdminSelection';
  const CSRF_TOKEN = (() => {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') || '' : '';
  })();

  const restoreSelection = () => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return new Set();
      const parsed = JSON.parse(raw);
      if (!Array.isArray(parsed)) return new Set();
      return new Set(parsed.map(String));
    } catch (err) {
      console.warn('Failed to restore selection', err);
      return new Set();
    }
  };

  const persistSelection = (selection) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(selection)));
    } catch (err) {
      console.warn('Failed to persist selection', err);
    }
  };

  const parseDatasetJson = (el, key, fallback) => {
    try {
      const raw = el.dataset[key];
      return raw ? JSON.parse(raw) : fallback;
    } catch (err) {
      console.warn('Failed to parse dataset json', key, err);
      return fallback;
    }
  };

  const postJSON = async (url, payload) => {
    const headers = { 'Content-Type': 'application/json' };
    if (CSRF_TOKEN) headers['X-CSRFToken'] = CSRF_TOKEN;
    const resp = await fetch(url, {
      method: 'POST',
      headers,
      credentials: 'same-origin',
      body: JSON.stringify(payload || {}),
    });
    if (!resp.ok) {
      const body = await resp.json().catch(() => ({}));
      throw new Error(body.message || `Request failed (${resp.status})`);
    }
    const contentType = resp.headers.get('content-type') || '';
    if (!contentType.includes('application/json')) {
      return {};
    }
    return resp.json();
  };

  const getJSON = async (url) => {
    const resp = await fetch(url, {
      method: 'GET',
      credentials: 'same-origin',
    });
    if (!resp.ok) {
      const body = await resp.json().catch(() => ({}));
      throw new Error(body.message || `Request failed (${resp.status})`);
    }
    return resp.json();
  };

  const ensurePill = (card, selector, className, text) => {
    let pill = card.querySelector(selector);
    if (!pill && text) {
      const thumb = card.querySelector('.template-thumb');
      if (!thumb) return null;
      pill = document.createElement('span');
      pill.className = className;
      pill.textContent = text;
      thumb.appendChild(pill);
    }
    return pill;
  };

  const applyBaseToCard = (card, base, statusLabels) => {
    if (!card) return;
    card.dataset.mockupStatus = base.status;
    card.dataset.mockupAspect = base.aspect_ratio;
    card.dataset.mockupCategory = base.category;
    card.dataset.mockupAspectSource = base.aspect_source || '';

    const perspectivePill = card.querySelector('[data-perspective-pill]');
    if (perspectivePill) {
      perspectivePill.hidden = !(base && base.coordinate_type === 'Perspective');
    }

    const statusText = statusLabels[base.status] || base.status;
    const statePill = card.querySelector('[data-state-pill]');
    if (statePill) statePill.textContent = statusText;

    const needsPill = ensurePill(card, '[data-needs-coords-pill]', 'state-pill mandatory', 'Needs coordinates');
    if (needsPill) needsPill.hidden = !(base.status === 'missing_coordinates' || base.status === 'needs_regeneration');

    const sizePill = ensurePill(card, '[data-size-chart-pill]', 'state-pill', 'Size chart');
    if (sizePill) sizePill.hidden = !base.is_size_chart;

    const incompletePill = ensurePill(card, '[data-incomplete-pill]', 'state-pill incomplete', 'Incomplete');
    if (incompletePill) incompletePill.hidden = !base.is_incomplete;

    const metaSummary = card.querySelector('[data-meta-summary]');
    if (metaSummary) metaSummary.textContent = `Aspect ${base.aspect_ratio} · Category ${base.category} · Regions ${base.region_count || '—'}`;

    const metaStatus = card.querySelector('[data-meta-status]');
    if (metaStatus) metaStatus.textContent = `Status ${statusText}`;

    const aspectSourceLabel = card.querySelector('[data-aspect-source-label]');
    if (aspectSourceLabel) aspectSourceLabel.textContent = base.aspect_source_label || '';

    const aspectSelect = card.querySelector('[data-card-aspect]');
    if (aspectSelect) aspectSelect.value = base.aspect_ratio;

    const categorySelect = card.querySelector('[data-card-category]');
    if (categorySelect) categorySelect.value = base.category;

    const previewBtn = card.querySelector('[data-open-preview]');
    if (previewBtn) {
      previewBtn.dataset.mockupAspect = base.aspect_ratio;
      previewBtn.dataset.previewArtworks = JSON.stringify(base.preview_artwork_options || []);
      previewBtn.dataset.previewDefault = (base.preview_artwork_options && base.preview_artwork_options[0] && base.preview_artwork_options[0].filename) || '';
    }
  };

  const ready = () => {
    const toolbar = document.querySelector('[data-batch-toolbar]');
    if (!toolbar) return;

    const statusLabels = parseDatasetJson(toolbar, 'statusLabels', {});
    const bulkEndpoint = toolbar.dataset.endpointBulk;
    const generateAsyncEndpoint = toolbar.dataset.endpointGenerateAsync || '';
    const generationProgressEndpoint = toolbar.dataset.endpointGenerationProgress || '';
    const selection = restoreSelection();
    const countEl = toolbar.querySelector('[data-selected-count]');
    const limitWarning = document.querySelector('[data-batch-limit-warning]');
    const max = Number(toolbar.dataset.batchMax || '25');
    const selectVisibleBtn = toolbar.querySelector('[data-select-visible]');
    const selectAllBtn = toolbar.querySelector('[data-select-all]');
    const deselectAllBtn = toolbar.querySelector('[data-deselect-all]');
    const generateTriggerBtn = toolbar.querySelector('[data-generate-trigger]');
    const generateCloseBtn = document.querySelector('[data-generate-close]');
    const generateAckBtn = document.querySelector('[data-generate-ack]');
    let generateInProgress = false;

    const isVisible = (el) => {
      if (!el) return false;
      const style = window.getComputedStyle(el);
      return style.display !== 'none' && style.visibility !== 'hidden' && el.offsetParent !== null;
    };

    const getVisibleCheckboxes = () =>
      Array.from(document.querySelectorAll('[data-mockup-card]'))
        .filter((card) => isVisible(card))
        .map((card) => card.querySelector('[data-mockup-checkbox]'))
        .filter(Boolean);

    const getAllCheckboxes = () => Array.from(document.querySelectorAll('[data-mockup-checkbox]'));

    const getSelectedMockups = () =>
      getAllCheckboxes()
        .filter((box) => box && box.checked)
        .map((box) => String(box.value || '').trim())
        .filter((id) => id.length > 0);

    const syncSelectionFromChecked = () => {
      selection.clear();
      getSelectedMockups().forEach((id) => selection.add(id));
      persistSelection(selection);
      return Array.from(selection);
    };

    const updateToolbar = () => {
      const selectedIds = syncSelectionFromChecked();
      const count = selectedIds.length;
      if (countEl) countEl.textContent = String(count);
      toolbar.dataset.visible = '1';
      const warn = count > max;
      if (limitWarning) {
        limitWarning.hidden = !warn;
      }
      const generateBtn = toolbar.querySelector('[data-generate-trigger]');
      if (generateBtn) {
        generateBtn.disabled = warn || count === 0;
        generateBtn.classList.toggle('disabled', warn || count === 0);
      }
      if (selectVisibleBtn) {
        const visibleBoxes = getVisibleCheckboxes();
        const allSelected = visibleBoxes.length > 0 && visibleBoxes.every((box) => box.checked);
        selectVisibleBtn.textContent = allSelected ? 'Unselect filtered' : 'Select filtered';
        selectVisibleBtn.disabled = visibleBoxes.length === 0;
      }
    };

    const toggleVisibleSelection = () => {
      const visibleBoxes = getVisibleCheckboxes();
      if (!visibleBoxes.length) return;
      const allSelected = visibleBoxes.every((box) => box.checked);
      const targetState = !allSelected;
      visibleBoxes.forEach((box) => {
        box.checked = targetState;
        const id = box.value;
        if (targetState) {
          selection.add(id);
        } else {
          selection.delete(id);
        }
      });
      persistSelection(selection);
      updateToolbar();
    };

    const selectAll = () => {
      const boxes = getAllCheckboxes();
      boxes.forEach((box) => {
        box.checked = true;
        selection.add(String(box.value));
      });
      persistSelection(selection);
      updateToolbar();
    };

    const deselectAll = () => {
      const boxes = getAllCheckboxes();
      boxes.forEach((box) => {
        box.checked = false;
      });
      selection.clear();
      persistSelection(selection);
      updateToolbar();
    };

    Array.from(document.querySelectorAll('[data-mockup-checkbox]')).forEach((box) => {
      const id = box.value;
      if (selection.has(id)) {
        box.checked = true;
      }
      box.addEventListener('change', () => {
        if (box.checked) {
          selection.add(id);
        } else {
          selection.delete(id);
        }
        persistSelection(selection);
        updateToolbar();
      });
    });

    if (selectVisibleBtn) {
      selectVisibleBtn.addEventListener('click', toggleVisibleSelection);
    }

    if (selectAllBtn) {
      selectAllBtn.addEventListener('click', selectAll);
    }

    if (deselectAllBtn) {
      deselectAllBtn.addEventListener('click', deselectAll);
    }

    const sanitizeBtn = toolbar.querySelector('[data-sanitize-sync]');
    if (sanitizeBtn) {
      sanitizeBtn.addEventListener('click', async () => {
        sanitizeBtn.disabled = true;
        const modal = document.querySelector('[data-sanitize-modal]');
        const closeBtn = modal ? modal.querySelector('[data-sanitize-close]') : null;
        const actions = modal ? modal.querySelector('[data-sanitize-actions]') : null;
        const statusEl = modal ? modal.querySelector('[data-sanitize-status]') : null;

        const openModal = () => {
          if (!modal) return;
          modal.dataset.visible = '1';
          document.body.classList.add('overlay-lock');
        };

        const closeModal = () => {
          if (!modal) return;
          modal.dataset.visible = '';
          document.body.classList.remove('overlay-lock');
        };

        if (closeBtn) {
          closeBtn.disabled = true;
          closeBtn.onclick = () => closeModal();
        }

        if (actions) actions.hidden = true;

        if (statusEl) statusEl.textContent = 'Running Sanitize & Sync…';
        openModal();
        try {
          const res = await postJSON('/admin/mockups/bases/sanitize-sync', {});
          if (!res || res.status !== 'ok') {
            throw new Error((res && res.message) || 'Sanitize & Sync failed');
          }
          const summary = (res && res.summary) || {};
          const renamed = Number(summary.renamed || 0);
          const thumbs = Number(summary.thumbs || 0);
          const coords = Number(summary.coords_updated || 0);
          const removed = Number(summary.removed_empty_dirs || 0);
          if (statusEl) statusEl.textContent = `Done. Renamed ${renamed}, thumbs ${thumbs}, coords ${coords}, removed empty dirs ${removed}.`;
          setTimeout(() => {
            window.location.reload();
          }, 650);
        } catch (err) {
          if (statusEl) statusEl.textContent = `Error: ${err && err.message ? err.message : 'Sanitize & Sync failed'}`;
          if (!modal) {
            alert(err && err.message ? err.message : 'Sanitize & Sync failed');
          }
          if (actions) actions.hidden = false;
          if (closeBtn) closeBtn.disabled = false;
        } finally {
          sanitizeBtn.disabled = false;
        }
      });
    }

    const thumbsBtn = toolbar.querySelector('[data-generate-thumbs]');
    if (thumbsBtn) {
      thumbsBtn.addEventListener('click', async () => {
        thumbsBtn.disabled = true;
        const modal = document.querySelector('[data-generate-thumbs-modal]');
        const closeBtn = modal ? modal.querySelector('[data-generate-thumbs-close]') : null;
        const actions = modal ? modal.querySelector('[data-generate-thumbs-actions]') : null;
        const statusEl = modal ? modal.querySelector('[data-generate-thumbs-status]') : null;

        const openModal = () => {
          if (!modal) return;
          modal.dataset.visible = '1';
          document.body.classList.add('overlay-lock');
        };

        const closeModal = () => {
          if (!modal) return;
          modal.dataset.visible = '';
          document.body.classList.remove('overlay-lock');
        };

        if (closeBtn) {
          closeBtn.disabled = true;
          closeBtn.onclick = () => closeModal();
        }
        if (actions) actions.hidden = true;

        if (statusEl) statusEl.textContent = 'Scanning for missing thumbnails…';
        openModal();
        try {
          const res = await postJSON('/admin/mockups/bases/generate-thumbs', {});
          if (!res || res.status !== 'ok') {
            throw new Error((res && res.message) || 'Generate Thumbnails failed');
          }
          const summary = (res && res.summary) || {};
          const generated = Number(summary.generated || 0);
          const skipped = Number(summary.skipped || 0);
          const failed = Number(summary.failed || 0);
          const scanned = Number(summary.scanned || 0);
          if (statusEl) {
            statusEl.textContent = `Done. Generated ${generated}. Skipped ${skipped}. Failed ${failed}. Scanned ${scanned}.`;
          }
          setTimeout(() => {
            window.location.reload();
          }, 650);
        } catch (err) {
          if (statusEl) statusEl.textContent = `Error: ${err && err.message ? err.message : 'Generate Thumbnails failed'}`;
          if (!modal) {
            alert(err && err.message ? err.message : 'Generate Thumbnails failed');
          }
          if (actions) actions.hidden = false;
          if (closeBtn) closeBtn.disabled = false;
        } finally {
          thumbsBtn.disabled = false;
        }
      });
    }

    const openModal = (name) => {
      const modal = document.querySelector(`[data-modal="${name}"]`);
      if (modal) modal.dataset.visible = '1';
    };
    const closeModal = () => {
      document.querySelectorAll('[data-modal]').forEach((modal) => {
        modal.dataset.visible = '';
      });
    };

    document.querySelectorAll('[data-open-modal]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const target = btn.getAttribute('data-open-modal');
        if (selection.size === 0) return;
        if (target === 'generate' && selection.size > max) return;
        openModal(target);
      });
    });

    document.querySelectorAll('[data-close-modal]').forEach((btn) => {
      btn.addEventListener('click', () => {
        if (generateInProgress && btn.hasAttribute('data-generate-close')) return;
        closeModal();
      });
    });

    const runBulk = async (action, extra) => {
      const payload = Object.assign({ mockup_ids: syncSelectionFromChecked(), action }, extra || {});
      return postJSON(bulkEndpoint, payload);
    };

    const deleteBtn = document.querySelector('[data-confirm-delete]');
    if (deleteBtn) {
      deleteBtn.addEventListener('click', async () => {
        try {
          await runBulk('delete');
          persistSelection(new Set());
          window.location.reload();
        } catch (err) {
          alert(err.message || 'Delete failed');
        }
      });
    }

    const moveBtn = document.querySelector('[data-confirm-move]');
    if (moveBtn) {
      moveBtn.addEventListener('click', async () => {
        const categorySelect = document.querySelector('[data-move-category]');
        const category = categorySelect ? categorySelect.value : '';
        try {
          await runBulk('category', { category });
          window.location.reload();
        } catch (err) {
          alert(err.message || 'Move failed');
        }
      });
    }

    const aspectBtn = document.querySelector('[data-confirm-aspect]');
    if (aspectBtn) {
      aspectBtn.addEventListener('click', async () => {
        const aspectSelect = document.querySelector('[data-aspect-select]');
        const aspect_ratio = aspectSelect ? aspectSelect.value : '';
        try {
          await runBulk('aspect', { aspect_ratio });
          window.location.reload();
        } catch (err) {
          alert(err.message || 'Aspect change failed');
        }
      });
    }

    const runCoordinateGeneration = async () => {
      const selectedIds = getSelectedMockups();
      if (!selectedIds.length || selectedIds.length > max) return;
      if (!generateAsyncEndpoint || !generationProgressEndpoint) {
        alert('Async generation endpoints are not configured');
        return;
      }
      selection.clear();
      selectedIds.forEach((id) => selection.add(id));
      persistSelection(selection);
      updateToolbar();

      const progress = document.querySelector('[data-generate-progress]');
      const status = document.querySelector('[data-generate-batch-status]');
      const bar = document.querySelector('[data-generate-progress-bar]');
      if (progress) progress.textContent = `Processing 0 of ${selectedIds.length}`;
      if (status) status.textContent = '';
      if (bar) bar.style.width = '0%';
      if (generateCloseBtn) generateCloseBtn.disabled = true;
      if (generateAckBtn) {
        generateAckBtn.hidden = true;
        generateAckBtn.disabled = true;
      }

      openModal('generate');
      if (generateTriggerBtn) generateTriggerBtn.disabled = true;
      generateInProgress = true;
      let pollTimer = null;
      let pollBusy = false;
      const finishGeneration = ({ reload = false, allowClose = true } = {}) => {
        if (pollTimer) {
          window.clearInterval(pollTimer);
          pollTimer = null;
        }
        generateInProgress = false;
        if (generateTriggerBtn) generateTriggerBtn.disabled = false;
        if (generateCloseBtn) generateCloseBtn.disabled = !allowClose;
        if (generateAckBtn) {
          generateAckBtn.hidden = !allowClose;
          generateAckBtn.disabled = !allowClose;
        }
        if (reload) {
          window.location.reload();
        }
      };

      try {
        await postJSON(generateAsyncEndpoint, { mockup_ids: selectedIds, force: true });
        if (status) status.textContent = 'Background generation started…';

        const pollProgress = async () => {
          if (pollBusy) return;
          pollBusy = true;
          try {
            const res = await getJSON(generationProgressEndpoint);
            const detail = (res && res.detail) || {};
            const total = Number(detail.total || selectedIds.length || 0);
            const completed = Number(detail.current ?? detail.completed ?? 0);
            const percent = Number(detail.percent || 0);
            const phase = String(detail.status || 'processing').toLowerCase();
            const msg = detail.message || `Step ${completed} of ${total}`;

            if (progress) progress.textContent = total > 0 ? `Processing ${completed} of ${total}` : 'Processing…';
            if (bar) bar.style.width = `${Math.max(0, Math.min(100, percent))}%`;
            if (status) status.textContent = msg;

            if (phase === 'completed') {
              if (bar) bar.style.width = '100%';
              finishGeneration({ reload: true, allowClose: true });
            } else if (phase === 'failed') {
              finishGeneration({ reload: false, allowClose: true });
            }
          } catch (err) {
            if (status) status.textContent = err && err.message ? err.message : 'Progress polling failed';
            finishGeneration({ reload: false, allowClose: true });
          } finally {
            pollBusy = false;
          }
        };

        await pollProgress();
        if (generateInProgress) {
          pollTimer = window.setInterval(pollProgress, 2000);
        }
      } catch (err) {
        if (status) status.textContent = err.message || 'Coordinate generation failed';
        finishGeneration({ reload: false, allowClose: true });
      }
    };

    if (generateTriggerBtn) {
      generateTriggerBtn.addEventListener('click', async () => {
        await runCoordinateGeneration();
      });
    }

    if (generateAckBtn) {
      generateAckBtn.addEventListener('click', () => {
        window.location.reload();
      });
    }

    document.addEventListener('keydown', (evt) => {
      if (evt.key === 'Escape' && !generateInProgress) closeModal();
    });

    // Per-card controls
    document.querySelectorAll('[data-mockup-card]').forEach((card) => {
      const mockupId = card.dataset.mockupId;

      const handleCardUpdate = (base) => {
        applyBaseToCard(card, base, statusLabels);
      };

      const cardDelete = card.querySelector('[data-card-delete]');
      if (cardDelete) {
        cardDelete.addEventListener('click', async () => {
          const confirmed = window.confirm('Delete this mockup base?');
          if (!confirmed) return;
          try {
            await postJSON(card.dataset.endpointDelete, {});
            if (selection.has(mockupId)) {
              selection.delete(mockupId);
              persistSelection(selection);
            }
            card.remove();
            updateToolbar();
          } catch (err) {
            alert(err.message || 'Delete failed');
          }
        });
      }

      const cardRegen = card.querySelector('[data-card-regenerate]');
      if (cardRegen) {
        cardRegen.addEventListener('click', async () => {
          cardRegen.disabled = true;
          try {
            const res = await postJSON(card.dataset.endpointRegenerate, {});
            if (res && res.base) handleCardUpdate(res.base);
          } catch (err) {
            alert(err.message || 'Regeneration failed');
          } finally {
            cardRegen.disabled = false;
          }
        });
      }

      const categoryBtn = card.querySelector('[data-card-category-apply]');
      if (categoryBtn) {
        categoryBtn.addEventListener('click', async () => {
          const select = card.querySelector('[data-card-category]');
          const category = select ? select.value : '';
          try {
            const res = await postJSON(card.dataset.endpointCategory, { category });
            if (res && res.base) handleCardUpdate(res.base);
          } catch (err) {
            alert(err.message || 'Move failed');
          }
        });
      }

      const aspectBtn = card.querySelector('[data-card-aspect-apply]');
      if (aspectBtn) {
        aspectBtn.addEventListener('click', async () => {
          const select = card.querySelector('[data-card-aspect]');
          const aspect_ratio = select ? select.value : '';
          try {
            const res = await postJSON(card.dataset.endpointAspect, { aspect_ratio });
            if (res && res.base) handleCardUpdate(res.base);
          } catch (err) {
            alert(err.message || 'Aspect override failed');
          }
        });
      }
    });

    updateToolbar();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ready);
  } else {
    ready();
  }
})();
