(function () {
  const run = () => {
    let currentGalleryIndex = 0;
    const galleryImages = Array.from(
      new Set(
        Array.from(document.querySelectorAll('[data-full-src]'))
          .map((el) => (el.getAttribute('data-full-src') || '').trim())
          .filter(Boolean),
      ),
    );

    const resolveGalleryIndex = (fullSrc) => {
      if (!fullSrc) return -1;
      const existing = galleryImages.indexOf(fullSrc);
      if (existing >= 0) return existing;
      galleryImages.push(fullSrc);
      return galleryImages.length - 1;
    };

    const modal = document.getElementById('artPreviewModal');
    const img = document.getElementById('modalImg');

    const openGallery = (index) => {
      if (!modal || !img) return;
      currentGalleryIndex = index;
      if (galleryImages[currentGalleryIndex]) {
        img.src = galleryImages[currentGalleryIndex];
        modal.classList.remove('hidden');
      }
    };

    const closeModal = () => {
      if (!modal) return;
      modal.classList.add('hidden');
    };

    const changeSlide = (n) => {
      if (!img || galleryImages.length === 0) return;
      currentGalleryIndex += n;
      if (currentGalleryIndex < 0) currentGalleryIndex = galleryImages.length - 1;
      if (currentGalleryIndex >= galleryImages.length) currentGalleryIndex = 0;
      if (galleryImages[currentGalleryIndex]) {
        img.src = galleryImages[currentGalleryIndex];
      }
    };

    document.querySelectorAll('[data-open-gallery][data-full-src]').forEach((el) => {
      const openFromAttr = () => {
        const fullSrc = (el.getAttribute('data-full-src') || '').trim();
        const idx = resolveGalleryIndex(fullSrc);
        if (idx >= 0) openGallery(idx);
      };
      el.addEventListener('click', openFromAttr);
      if (el.tagName === 'IMG') {
        el.addEventListener('keydown', (evt) => {
          if (evt.key === 'Enter' || evt.key === ' ') {
            evt.preventDefault();
            openFromAttr();
          }
        });
      }
    });

    if (modal) {
      modal.addEventListener('click', (event) => {
        if (event.target === modal) {
          closeModal();
        }
      });

      const closeBtn = modal.querySelector('[data-gallery-close]');
      const prevBtn = modal.querySelector('[data-gallery-prev]');
      const nextBtn = modal.querySelector('[data-gallery-next]');

      if (closeBtn) {
        closeBtn.addEventListener('click', (event) => {
          event.preventDefault();
          event.stopPropagation();
          closeModal();
        });
      }
      if (prevBtn) {
        prevBtn.addEventListener('click', (event) => {
          event.preventDefault();
          event.stopPropagation();
          changeSlide(-1);
        });
      }
      if (nextBtn) {
        nextBtn.addEventListener('click', (event) => {
          event.preventDefault();
          event.stopPropagation();
          changeSlide(1);
        });
      }

      modal.querySelectorAll('[data-gallery-stop-propagation]').forEach((el) => {
        el.addEventListener('click', (event) => {
          event.stopPropagation();
        });
      });
    }

    document.addEventListener('keydown', (evt) => {
      if (modal && !modal.classList.contains('hidden')) {
        if (evt.key === 'ArrowLeft') {
          evt.preventDefault();
          changeSlide(-1);
        } else if (evt.key === 'ArrowRight') {
          evt.preventDefault();
          changeSlide(1);
        } else if (evt.key === 'Escape') {
          evt.preventDefault();
          closeModal();
        }
      }
    });

    const csrf = (() => {
      const meta = document.querySelector('meta[name="csrf-token"]');
      return meta ? (meta.getAttribute('content') || '').trim() : '';
    })();

    const postJson = async (url, body) => {
      const resp = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(csrf ? { 'X-CSRFToken': csrf, 'X-CSRF-Token': csrf } : {}),
          'X-Requested-With': 'XMLHttpRequest',
        },
        credentials: 'same-origin',
        body: JSON.stringify(body),
      });
      const data = await resp.json().catch(() => ({}));
      return { resp, data };
    };

    document.querySelectorAll('[data-copy-target]').forEach((btn) => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        const target = btn.dataset.copyTarget;
        const field = target ? document.getElementById(target) : null;
        if (!field) return;
        const oldText = btn.textContent;
        try {
          if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
            await navigator.clipboard.writeText(field.value);
          } else {
            const ta = document.createElement('textarea');
            ta.value = field.value;
            ta.style.position = 'fixed';
            ta.style.left = '-9999px';
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            document.body.removeChild(ta);
          }
          btn.textContent = '✓';
          setTimeout(() => {
            btn.textContent = oldText;
          }, 1500);
        } catch (_err) {
          btn.textContent = '✗';
          setTimeout(() => {
            btn.textContent = oldText;
          }, 1500);
        }
      });
    });

    let isDirty = false;
    const form = document.getElementById('analysis-form');
    const slug = ((form && form.dataset.slug) || '').trim();

    if (form) {
      form.addEventListener('change', () => {
        isDirty = true;
      });
      form.addEventListener('input', () => {
        isDirty = true;
      });
    }

    window.addEventListener('beforeunload', (e) => {
      if (isDirty) {
        e.preventDefault();
        e.returnValue = 'You have unsaved changes.';
      }
    });

    const notify = (message, level = 'info') => {
      if (!message) return;
      if (level === 'error') {
        console.error(message);
      } else {
        console.log(message);
      }
    };

    const saveBtn = document.querySelector('[data-analysis-save]');
    if (saveBtn && form) {
      saveBtn.addEventListener('click', async () => {
        if (!slug) {
          notify('Slug not found', 'error');
          return;
        }

        const formData = new FormData(form);
        const data = {
          title: formData.get('title'),
          description: formData.get('description'),
          tags: formData.get('tags'),
          materials: formData.get('materials'),
          seo_filename: formData.get('seo_filename'),
          quantity: formData.get('quantity'),
          price: formData.get('price'),
          location: formData.get('location'),
          sentiment: formData.get('sentiment'),
          original_prompt: formData.get('original_prompt'),
          colours: formData.get('colours'),
          visual_analysis: {
            subject: formData.get('va_subject'),
            palette: formData.get('va_palette'),
            mood: formData.get('va_mood'),
          },
        };

        const saveOriginalText = saveBtn.textContent;
        saveBtn.disabled = true;
        saveBtn.textContent = 'Saving...';
        try {
          const { resp, data: result } = await postJson(`/artwork/${encodeURIComponent(slug)}/save`, data);
          if (!resp.ok) {
            throw new Error((result && result.error) || 'Save failed');
          }
          isDirty = false;
          notify('Saved successfully.');
        } catch (err) {
          notify(err && err.message ? err.message : 'Save failed', 'error');
        } finally {
          saveBtn.disabled = false;
          saveBtn.textContent = saveOriginalText;
        }
      });
    }

    const lockBtn = document.querySelector('[data-analysis-lock]');
    if (lockBtn) {
      lockBtn.addEventListener('click', async () => {
        if (!slug) return;
        lockBtn.disabled = true;
        lockBtn.textContent = 'Locking...';
        try {
          const { resp, data } = await postJson(`/artwork/${encodeURIComponent(slug)}/lock`, {});
          if (!resp.ok) {
            throw new Error((data && data.error) || 'Lock failed');
          }
          window.location.href = '/artworks/locked';
        } catch (err) {
          notify(err && err.message ? err.message : 'Lock failed', 'error');
          lockBtn.disabled = false;
          lockBtn.textContent = 'Lock Artwork';
        }
      });
    }

    document.querySelectorAll('[data-analysis-delete]').forEach((deleteBtn) => {
      deleteBtn.addEventListener('click', async () => {
        if (!slug) return;
        const ok = window.confirm('Are you sure? This will permanently delete the artwork.');
        if (!ok) return;

        const originalText = deleteBtn.textContent;
        deleteBtn.disabled = true;
        deleteBtn.textContent = 'Deleting...';
        try {
          const { resp, data } = await postJson(`/artwork/${encodeURIComponent(slug)}/delete`, {});
          if (!resp.ok) {
            throw new Error((data && data.error) || 'Delete failed');
          }
          window.location.href = '/artworks/processed';
        } catch (err) {
          notify(err && err.message ? err.message : 'Delete failed', 'error');
          deleteBtn.disabled = false;
          deleteBtn.textContent = originalText;
        }
      });
    });

    document.querySelectorAll('[data-regenerate-images]').forEach((regenBtn) => {
      regenBtn.addEventListener('click', async () => {
        if (!slug) return;
        const ok = window.confirm('Regenerate THUMB, ANALYSE, CLOSEUP-PROXY, and SEO-named copy? This may take a moment.');
        if (!ok) return;

        const originalText = regenBtn.textContent;
        regenBtn.disabled = true;
        regenBtn.textContent = 'Regenerating...';
        try {
          const { resp, data } = await postJson(`/artwork/${encodeURIComponent(slug)}/regenerate-images`, {});
          if (!resp.ok || (data && data.status && data.status.startsWith('error'))) {
            throw new Error((data && data.message) || 'Image regeneration failed');
          }
          notify('Images regenerated successfully. Page will reload.', 'success');
          setTimeout(() => {
            window.location.reload();
          }, 1500);
        } catch (err) {
          notify(err && err.message ? err.message : 'Image regeneration failed', 'error');
          regenBtn.disabled = false;
          regenBtn.textContent = originalText;
        }
      });
    });

    document.querySelectorAll('[data-reanalyse-provider]').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const provider = (btn.dataset.reanalyseProvider || '').trim().toLowerCase();
        if (!provider || !slug) return;

        const originalText = btn.textContent;
        btn.disabled = true;
        btn.textContent = 'Queueing...';
        try {
          const { resp, data } = await postJson(`/api/analysis/${encodeURIComponent(provider)}/${encodeURIComponent(slug)}`, {});
          if (!resp.ok || data.status !== 'ok') {
            throw new Error((data && data.message) || 'Reanalysis request failed');
          }
          const providerTitle = provider === 'gemini' ? 'Gemini' : 'OpenAI';
          if (typeof AnalysisLoader !== 'undefined') {
            AnalysisLoader.show(providerTitle, () => {
              window.location.reload();
            });
            try {
              await AnalysisLoader.poll(slug, provider);
              AnalysisLoader.hide();
            } catch (pollErr) {
              AnalysisLoader.showError((pollErr && pollErr.message) || 'Analysis failed');
              btn.disabled = false;
              btn.textContent = originalText;
              return;
            }
          }
          window.location.href = provider === 'gemini'
            ? `/artwork/${encodeURIComponent(slug)}/review/gemini`
            : `/artwork/${encodeURIComponent(slug)}/review/openai`;
        } catch (err) {
          notify(err && err.message ? err.message : 'Reanalysis request failed', 'error');
          btn.disabled = false;
          btn.textContent = originalText;
        }
      });
    });

    const selectAllBtn = document.querySelector('[data-select-all-mockups]');
    if (selectAllBtn) {
      selectAllBtn.addEventListener('click', () => {
        const allCheckboxes = Array.from(document.querySelectorAll('[data-mockup-select]'));
        const allChecked = allCheckboxes.every((cb) => cb.checked);

        allCheckboxes.forEach((cb) => {
          cb.checked = !allChecked;
          cb.dispatchEvent(new Event('change'));
        });

        selectAllBtn.textContent = allChecked ? 'Select All' : 'Deselect All';
      });
    }

    const deleteSelectedBtn = document.querySelector('[data-delete-selected]');
    if (deleteSelectedBtn) {
      deleteSelectedBtn.addEventListener('click', async () => {
        const selectedCheckboxes = Array.from(document.querySelectorAll('[data-mockup-select]:checked'));
        const selectedSlots = selectedCheckboxes.map((cb) => parseInt(cb.dataset.slot, 10));

        if (selectedSlots.length === 0) {
          notify('Please select mockups to delete.', 'error');
          return;
        }

        const ok = window.confirm(`Delete ${selectedSlots.length} selected mockup(s)?`);
        if (!ok) return;

        deleteSelectedBtn.disabled = true;
        deleteSelectedBtn.textContent = 'Deleting...';

        try {
          const { resp, data } = await postJson(`/artwork/${encodeURIComponent(slug)}/mockups/delete-selected`, { slots: selectedSlots });
          if (!resp.ok) {
            throw new Error((data && data.error) || 'Delete failed');
          }
          selectedSlots.forEach((slot) => {
            const card = document.querySelector(`.mockup-card[data-slot="${slot}"]`);
            if (card) card.remove();
          });
          window.dispatchEvent(new CustomEvent('mockups:changed'));
          notify(`Deleted ${selectedSlots.length} mockup(s).`);
        } catch (err) {
          notify(err && err.message ? err.message : 'Delete failed', 'error');
        } finally {
          deleteSelectedBtn.disabled = false;
          deleteSelectedBtn.textContent = 'Delete Selected';
        }
      });
    }

    document.querySelectorAll('[data-mockup-select]').forEach((checkbox) => {
      checkbox.addEventListener('change', () => {
        const card = checkbox.closest('.mockup-card');
        if (!card) return;
        if (checkbox.checked) {
          card.style.opacity = '0.6';
          card.style.borderColor = 'var(--accent-orange)';
        } else {
          card.style.opacity = '1';
          card.style.borderColor = 'rgba(128, 128, 128, 0.1)';
        }
      });
    });

    document.querySelectorAll('[data-video-panel]').forEach((panel) => {
      const generateBtn = panel.querySelector('[data-video-generate]');
      const deleteBtn = panel.querySelector('[data-video-delete]');
      const saveRegenerateBtn = panel.querySelector('[data-cinematic-save-regenerate]');
      const zoomInput = panel.querySelector('[data-cinematic-zoom]');
      const zoomValue = panel.querySelector('[data-cinematic-zoom-value]');
      const panInput = panel.querySelector('[data-cinematic-pan]');
      const durationInput = panel.querySelector('[data-cinematic-duration]');
      const statusBox = panel.querySelector('[data-video-status-box]');
      const stageEl = panel.querySelector('[data-video-stage]');
      const percentEl = panel.querySelector('[data-video-percent]');
      const msgEl = panel.querySelector('[data-video-message]');
      const fillEl = panel.querySelector('[data-video-progress-fill]');
      const previewCard = panel.querySelector('[data-video-preview]');
      const player = panel.querySelector('[data-video-player]');
      const download = panel.querySelector('[data-video-download]');
      const panelSlug = panel.dataset.slug || slug;

      if (!generateBtn || !panelSlug) return;

      const syncZoomLabel = () => {
        if (!zoomInput || !zoomValue) return;
        const val = Math.max(1.0, Math.min(1.3, Number(zoomInput.value) || 1.1));
        zoomValue.textContent = `${val.toFixed(2)}x`;
      };

      if (zoomInput) {
        zoomInput.addEventListener('input', syncZoomLabel);
      }
      syncZoomLabel();

      const collectCinematicSettings = () => {
        const zoom = Math.max(1.0, Math.min(1.3, Number((zoomInput && zoomInput.value) || 1.1)));
        const duration = Math.max(5, Math.min(60, parseInt(((durationInput && durationInput.value) || '15'), 10) || 15));
        const panningEnabled = Boolean(panInput && panInput.checked);
        return {
          video_zoom_intensity: Number(zoom.toFixed(2)),
          video_panning_enabled: panningEnabled,
          video_duration: duration,
        };
      };

      const saveCinematicSettings = async () => {
        const { resp, data } = await postJson(`/artwork/${encodeURIComponent(panelSlug)}/video/settings`, collectCinematicSettings());
        if (!resp.ok || data.status !== 'ok') {
          throw new Error((data && (data.message || data.error)) || 'Failed to save cinematic settings');
        }
      };

      const hasMockups = () => document.querySelectorAll('.mockup-card').length > 0;

      const applyMockupGuardrail = () => {
        if (!hasMockups()) {
          generateBtn.disabled = true;
          generateBtn.textContent = 'Generate 2K Mockups First';
          generateBtn.title = 'Video generation requires existing mockup frames to calculate zoom targets.';
          if (deleteBtn) deleteBtn.disabled = true;
          if (saveRegenerateBtn) saveRegenerateBtn.disabled = true;
          return false;
        }
        if (!download || download.getAttribute('href') === '#') {
          generateBtn.textContent = 'Generate Video';
        }
        generateBtn.disabled = false;
        generateBtn.title = '';
        if (saveRegenerateBtn) saveRegenerateBtn.disabled = false;
        return true;
      };

      const renderVideoStatus = (data) => {
        const pct = Math.max(0, Math.min(100, Number((data && data.percent) || 0)));
        if (fillEl) fillEl.style.width = `${pct}%`;
        if (stageEl) stageEl.textContent = (data && data.stage) || 'processing';
        if (percentEl) percentEl.textContent = `${pct}%`;
        if (msgEl) msgEl.textContent = (data && data.message) || 'Generating cinematic video...';
      };

      const applyVideoState = (data) => {
        const hasVideo = Boolean(data && data.has_video && data.video_url);
        if (hasVideo && player && download) {
          const videoUrl = String(data.video_url || '');
          player.src = `${videoUrl}${videoUrl.includes('?') ? '&' : '?'}t=${Date.now()}`;
          download.href = videoUrl;
          if (previewCard) previewCard.hidden = false;
          if (deleteBtn) deleteBtn.disabled = false;
          generateBtn.textContent = 'Regenerate Video';
        } else {
          if (previewCard) previewCard.hidden = true;
          if (download) download.href = '#';
          if (deleteBtn) deleteBtn.disabled = true;
        }

        if (data && data.status === 'processing') {
          if (statusBox) statusBox.hidden = false;
          renderVideoStatus(data);
          generateBtn.disabled = true;
          generateBtn.textContent = 'Generating...';
          if (deleteBtn) deleteBtn.disabled = true;
        } else if (!(data && data.status === 'error')) {
          if (statusBox) statusBox.hidden = true;
          applyMockupGuardrail();
        }
      };

      const deleteVideo = async ({ requireConfirmation = true, ignoreNotFound = false } = {}) => {
        if (requireConfirmation) {
          const ok = window.confirm('Delete generated video?');
          if (!ok) return false;
        }

        const resp = await fetch(`/artwork/${encodeURIComponent(panelSlug)}/video`, {
          method: 'DELETE',
          headers: {
            ...(csrf ? { 'X-CSRFToken': csrf, 'X-CSRF-Token': csrf } : {}),
            'X-Requested-With': 'XMLHttpRequest',
          },
          credentials: 'same-origin',
        });
        const payload = await resp.json().catch(() => ({}));
        if (!resp.ok || payload.status !== 'ok') {
          if (ignoreNotFound && resp.status === 404) {
            return false;
          }
          throw new Error((payload && (payload.message || payload.error)) || 'Failed to delete video');
        }

        if (previewCard) previewCard.hidden = true;
        if (statusBox) statusBox.hidden = true;
        if (download) download.href = '#';
        if (msgEl) msgEl.textContent = 'Video deleted';
        generateBtn.textContent = 'Generate Video';
        applyMockupGuardrail();
        return true;
      };

      const startGeneration = async () => {
        if (!applyMockupGuardrail()) return;
        if (previewCard) previewCard.hidden = true;
        if (statusBox) statusBox.hidden = false;

        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        if (deleteBtn) deleteBtn.disabled = true;

        const { resp, data } = await postJson(`/artwork/${encodeURIComponent(panelSlug)}/video/generate`, {});
        if (!resp.ok || data.status !== 'ok') {
          throw new Error((data && (data.message || data.error)) || 'Video generation failed');
        }
        await pollStatus();
        pollTimer = setInterval(pollStatus, 1500);
      };

      const fetchVideoStatus = async () => {
        const r = await fetch(`/artwork/${encodeURIComponent(panelSlug)}/video-status`, { credentials: 'same-origin' });
        if (!r.ok) return null;
        return r.json();
      };

      let pollTimer = null;
      const stopPolling = () => {
        if (pollTimer) {
          clearInterval(pollTimer);
          pollTimer = null;
        }
      };

      const pollStatus = async () => {
        try {
          const status = await fetchVideoStatus();
          if (!status) return;
          renderVideoStatus(status);
          applyVideoState(status);

          if (status.status === 'error') {
            stopPolling();
            if (msgEl) msgEl.textContent = status.message || 'Video generation failed';
            if (stageEl) stageEl.textContent = 'error';
            if (percentEl) percentEl.textContent = '100%';
            if (fillEl) fillEl.style.width = '100%';
            applyMockupGuardrail();
          }

          if (status.status === 'success' && status.video_url) {
            stopPolling();
            if (statusBox) statusBox.hidden = true;
            applyVideoState(status);
          }
        } catch (err) {
          stopPolling();
          if (msgEl) msgEl.textContent = (err && err.message) || 'Video generation failed';
          applyMockupGuardrail();
        }
      };

      generateBtn.addEventListener('click', async () => {
        try {
          await startGeneration();
        } catch (err) {
          if (statusBox) statusBox.hidden = false;
          if (msgEl) msgEl.textContent = err && err.message ? err.message : 'Video generation failed';
          if (stageEl) stageEl.textContent = 'error';
          if (percentEl) percentEl.textContent = '100%';
          if (fillEl) fillEl.style.width = '100%';
          applyMockupGuardrail();
        }
      });

      if (deleteBtn) {
        deleteBtn.addEventListener('click', async () => {
          deleteBtn.disabled = true;
          try {
            await deleteVideo({ requireConfirmation: true, ignoreNotFound: false });
          } catch (err) {
            notify(err && err.message ? err.message : 'Failed to delete video', 'error');
            deleteBtn.disabled = false;
          }
        });
      }

      if (saveRegenerateBtn) {
        saveRegenerateBtn.addEventListener('click', async () => {
          if (!applyMockupGuardrail()) return;
          const originalText = saveRegenerateBtn.textContent;
          saveRegenerateBtn.disabled = true;
          saveRegenerateBtn.textContent = 'Saving...';
          try {
            await saveCinematicSettings();
            saveRegenerateBtn.textContent = 'Re-rendering...';
            await deleteVideo({ requireConfirmation: false, ignoreNotFound: true });
            await startGeneration();
          } catch (err) {
            notify(err && err.message ? err.message : 'Failed to save cinematic settings', 'error');
            applyMockupGuardrail();
          } finally {
            saveRegenerateBtn.disabled = false;
            saveRegenerateBtn.textContent = originalText;
          }
        });
      }

      fetchVideoStatus()
        .then((status) => {
          if (status) {
            applyVideoState(status);
          } else {
            applyMockupGuardrail();
          }
        })
        .catch(() => applyMockupGuardrail());

      window.addEventListener('mockups:changed', () => {
        applyMockupGuardrail();
      });
    });

    document.querySelectorAll('[data-admin-export]').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const btnSlug = btn.dataset.slug || slug;
        const provider = btn.dataset.provider;
        if (!btnSlug || !provider) {
          notify('Invalid slug or provider', 'error');
          return;
        }

        const originalText = btn.textContent;
        btn.disabled = true;
        btn.textContent = 'Exporting...';

        try {
          const url = `/artwork/${encodeURIComponent(btnSlug)}/admin-export/${provider}`;
          window.location.href = url;
          setTimeout(() => {
            btn.disabled = false;
            btn.textContent = originalText;
          }, 1500);
        } catch (err) {
          notify(err && err.message ? err.message : 'Export failed', 'error');
          btn.disabled = false;
          btn.textContent = originalText;
        }
      });
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
