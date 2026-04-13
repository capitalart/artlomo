(function () {
  const grid = document.querySelector('#mockup-grid');
  if (!grid) return;

  const slug = (grid.dataset.slug || '').trim();
  const csrf = (() => {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.getAttribute('content')) {
      return (meta.getAttribute('content') || '').trim();
    }
    const hidden = document.querySelector('input[name="csrf_token"]');
    return hidden ? (hidden.value || '').trim() : '';
  })();

  const showOverlay = (card, on) => {
    const overlay = card.querySelector('.overlay');
    if (!overlay) return;
    if (on) {
      card.classList.add('is-loading');
    } else {
      card.classList.remove('is-loading');
    }
    overlay.hidden = !on;
  };

  const updateCategory = async (card) => {
    const slot = card.dataset.slot;
    const categorySelect = card.querySelector('[data-category]');
    const category = categorySelect ? categorySelect.value : '';
    try {
      const endpoint = slug
        ? `/artwork/${encodeURIComponent(slug)}/mockups/${encodeURIComponent(slot)}/category`
        : `/artwork/mockups/${encodeURIComponent(slot)}/category`;
      const resp = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(csrf ? { 'X-CSRFToken': csrf, 'X-CSRF-Token': csrf } : {}),
        },
        credentials: 'same-origin',
        body: JSON.stringify({ category, ...(csrf ? { csrf_token: csrf } : {}) }),
      });
      const data = await resp.json();
      if (!resp.ok || data.status !== 'ok') {
        throw new Error(data.message || 'Category update failed');
      }
    } catch (err) {
      alert(err.message || 'Category update failed');
    }
  };

  const updateCard = (card, payload) => {
    const img = card.querySelector('img[data-mockup-thumb], img');
    const wrapper = card.querySelector('.art-card');
    const galleryTriggers = card.querySelectorAll('[data-open-gallery]');
    if (wrapper && payload.composite_url) {
      wrapper.dataset.analyseSrc = payload.composite_url;
    }
    if (wrapper && payload.thumb_url) {
      wrapper.dataset.fallbackSrc = payload.thumb_url;
    }
    if (img && payload.thumb_url) {
      const bust = `t=${Date.now()}`;
      img.src = `${payload.thumb_url}${payload.thumb_url.includes('?') ? '&' : '?'}${bust}`;
    }
    if (payload.composite_url && img) {
      img.dataset.fullSrc = payload.composite_url;
    }
    if (payload.composite_url && galleryTriggers.length) {
      galleryTriggers.forEach((el) => {
        el.setAttribute('data-full-src', payload.composite_url);
      });
    }
    const select = card.querySelector('[data-category]');
    if (select && payload.category) {
      select.value = payload.category;
    }
  };

  const swap = async (card) => {
    const slot = card.dataset.slot;
    const categorySelect = card.querySelector('[data-category]');
    const category = categorySelect ? categorySelect.value : '';
    showOverlay(card, true);
    try {
      const endpoint = slug
        ? `/artwork/${encodeURIComponent(slug)}/mockups/${encodeURIComponent(slot)}/swap`
        : `/artwork/mockups/${encodeURIComponent(slot)}/swap`;
      const resp = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(csrf ? { 'X-CSRFToken': csrf, 'X-CSRF-Token': csrf } : {}),
        },
        credentials: 'same-origin',
        body: JSON.stringify({ category, ...(csrf ? { csrf_token: csrf } : {}) }),
      });
      const data = await resp.json();
      if (!resp.ok || data.status !== 'ok') {
        throw new Error(data.message || 'Swap failed');
      }
      updateCard(card, data);
    } catch (err) {
      alert(err.message || 'Swap failed');
    } finally {
      showOverlay(card, false);
    }
  };

  grid.querySelectorAll('[data-swap]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const card = btn.closest('[data-slot]');
      if (card) swap(card);
    });
  });

  grid.querySelectorAll('[data-category]').forEach((select) => {
    select.addEventListener('change', () => {
      const card = select.closest('[data-slot]');
      if (card) updateCategory(card);
    });
  });

  const setAll = (checked) => {
    grid.querySelectorAll('[data-mockup-select]').forEach((el) => {
      if (!(el instanceof HTMLInputElement)) return;
      el.checked = checked;
      el.dispatchEvent(new Event('change', { bubbles: true }));
    });
  };

  const selectAllBtn = document.querySelector('[data-select-all-mockups], [data-select-all]');
  if (selectAllBtn) {
    selectAllBtn.addEventListener('click', (e) => {
      e.preventDefault();
      setAll(true);
    });
  }

  const deselectAllBtn = document.querySelector('[data-deselect-all-mockups], [data-deselect-all]');
  if (deselectAllBtn) {
    deselectAllBtn.addEventListener('click', (e) => {
      e.preventDefault();
      setAll(false);
    });
  }
})();
