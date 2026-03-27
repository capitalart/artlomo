(function () {
  const modal = document.querySelector('[data-preview-modal]');
  if (!modal) return;

  const backdrop = modal;
  const baseImg = modal.querySelector('[data-preview-base]');
  const artworkSelect = modal.querySelector('[data-preview-artwork]');
  const artworkHint = modal.querySelector('[data-preview-artwork-hint]');
  const artworkEmpty = modal.querySelector('[data-preview-artwork-empty]');
  const aspectWarning = modal.querySelector('[data-preview-aspect-warning]');
  const statusText = modal.querySelector('[data-preview-status]');
  const spinner = modal.querySelector('[data-preview-spinner]');
  const output = modal.querySelector('[data-preview-output]');
  const placeholder = modal.querySelector('[data-preview-placeholder]');
  const actions = modal.querySelector('[data-preview-actions]');
  const openLink = modal.querySelector('[data-preview-open]');
  const generateBtn = modal.querySelector('[data-preview-generate]');
  const regenerateBtn = modal.querySelector('[data-preview-regenerate]');
  const closeBtn = modal.querySelector('[data-close-preview]');

  let currentMockupId = null;
  let currentSlug = null;
  let currentAspect = null;
  let availableArtworks = [];
  const csrfToken = (() => {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') || '' : '';
  })();

  const setStatus = (text, loading = false) => {
    if (statusText) statusText.textContent = text;
    if (spinner) spinner.hidden = !loading;
  };

  const closeModal = () => {
    backdrop.dataset.visible = '';
    currentMockupId = null;
    currentSlug = null;
    currentAspect = null;
    availableArtworks = [];
    if (artworkSelect) {
      artworkSelect.innerHTML = '';
    }
    if (output) {
      output.style.display = 'none';
      output.src = '';
    }
    if (placeholder) placeholder.hidden = false;
    if (actions) actions.hidden = true;
  };

  const openModal = (cardBtn) => {
    currentMockupId = cardBtn.getAttribute('data-mockup-id');
    currentSlug = cardBtn.getAttribute('data-mockup-slug');
    currentAspect = cardBtn.getAttribute('data-mockup-aspect');
    availableArtworks = [];
    try {
      const raw = cardBtn.getAttribute('data-preview-artworks') || '[]';
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) {
        availableArtworks = parsed.map((item) => {
          if (typeof item === 'string') return { filename: item, aspect: currentAspect, path: null };
          const filename = item.filename || item.name || '';
          const aspect = item.aspect || currentAspect;
          const path = item.path || null;
          return { filename, aspect, path };
        }).filter((item) => item.filename);
      }
    } catch (err) {
      console.warn('Failed to parse preview artworks', err);
    }

    if (artworkSelect) {
      artworkSelect.innerHTML = '';
      availableArtworks.forEach((record) => {
        const opt = document.createElement('option');
        opt.value = record.filename;
        opt.textContent = record.filename;
        artworkSelect.appendChild(opt);
      });
      const def = cardBtn.getAttribute('data-preview-default');
      if (def && availableArtworks.some((rec) => rec.filename === def)) {
        artworkSelect.value = def;
      } else if (availableArtworks.length > 0) {
        artworkSelect.value = availableArtworks[0].filename;
      }
    }

    if (artworkHint) {
      const aspectLabel = currentAspect || 'UNSET';
      artworkHint.textContent = aspectLabel === 'UNSET'
        ? 'Aspect is UNSET; preview requires an aspect ratio to select a test asset.'
        : `Looking for coordinate-tester-${aspectLabel}.jpg in mockup-preview-tests/`;
    }
    if (artworkEmpty) {
      const aspectLabel = currentAspect || 'UNSET';
      if (availableArtworks.length === 0) {
        artworkEmpty.textContent = aspectLabel === 'UNSET'
          ? 'Missing Test Asset: set an aspect ratio first, then add coordinate-tester-<aspect>.jpg (e.g. coordinate-tester-3x4.jpg) to mockup-preview-tests/.'
          : `Missing Test Asset: coordinate-tester-${aspectLabel}.jpg not found in mockup-preview-tests/.`;
        artworkEmpty.hidden = false;
      } else {
        artworkEmpty.hidden = true;
      }
    }
    if (aspectWarning) {
      aspectWarning.hidden = (currentAspect && currentAspect !== 'UNSET') ? true : false;
    }
    if (generateBtn) generateBtn.disabled = availableArtworks.length === 0;
    if (regenerateBtn) regenerateBtn.disabled = availableArtworks.length === 0;

    if (baseImg) {
      baseImg.src = cardBtn.getAttribute('data-base-image') || '';
    }

    setStatus('Ready', false);
    if (placeholder) placeholder.hidden = false;
    if (actions) actions.hidden = true;

    backdrop.dataset.visible = '1';
  };

  const attachButtonHandlers = () => {
    document.querySelectorAll('[data-open-preview]').forEach((btn) => {
      btn.addEventListener('click', () => openModal(btn));
    });
  };

  const submitPreview = async () => {
    if (!currentMockupId) return;
    const artwork = artworkSelect ? artworkSelect.value : null;
    setStatus('Generating preview…', true);
    if (placeholder) placeholder.hidden = true;
    if (actions) actions.hidden = true;
    try {
      const resp = await fetch(`/admin/mockups/${currentMockupId}/preview`, {
        method: 'POST',
        headers: Object.assign({ 'Content-Type': 'application/json' }, csrfToken ? { 'X-CSRFToken': csrfToken } : {}),
        credentials: 'same-origin',
        body: JSON.stringify({ preview_artwork: artwork }),
      });
      let data;
      try {
        data = await resp.json();
      } catch (parseErr) {
        throw new Error('Preview failed');
      }
      if (!resp.ok || data.status !== 'ok') {
        const message = data && (data.message || data.error)
          ? (data.message || data.error)
          : resp.status === 403
            ? 'Admin session required. Please refresh and sign in.'
            : 'Preview failed';
        throw new Error(message);
      }
      if (output) {
        const cacheBust = `t=${Date.now()}`;
        output.src = `${data.preview_url}?${cacheBust}`;
        output.style.display = 'block';
      }
      if (openLink && data.preview_url) {
        openLink.href = data.preview_url;
      }
      if (actions) actions.hidden = false;
      setStatus('Preview generated', false);
    } catch (err) {
      setStatus(err.message || 'Preview failed', false);
      if (placeholder) {
        placeholder.hidden = false;
        placeholder.textContent = 'Preview failed: ' + (err.message || 'Unknown error');
      }
    }
  };

  if (generateBtn) {
    generateBtn.addEventListener('click', submitPreview);
  }
  if (regenerateBtn) {
    regenerateBtn.addEventListener('click', submitPreview);
  }
  if (closeBtn) {
    closeBtn.addEventListener('click', () => closeModal());
  }
  document.addEventListener('keydown', (evt) => {
    if (evt.key === 'Escape') closeModal();
  });

  attachButtonHandlers();
})();
