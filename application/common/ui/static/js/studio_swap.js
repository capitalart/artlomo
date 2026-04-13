(function () {
  const grids = Array.from(document.querySelectorAll('[data-studio-grid][data-studio-slug]'));
  if (!grids.length) return;

  const getCsrf = () => {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? (meta.getAttribute('content') || '').trim() : '';
  };

  const showOverlay = (tile, on) => {
    const overlay = tile.querySelector('[data-studio-overlay]');
    if (!overlay) return;
    overlay.hidden = !on;
  };

  const bustUrl = (url) => {
    if (!url) return url;
    const sep = url.includes('?') ? '&' : '?';
    return `${url}${sep}t=${Date.now()}`;
  };

  const updateTile = (tile, payload) => {
    const card = tile.querySelector('.art-card');
    const img = tile.querySelector('img');
    const categorySelect = tile.querySelector('[data-studio-category]');
    if (card && payload.composite_url) {
      card.dataset.analyseSrc = payload.composite_url;
    }
    if (card && payload.thumb_url) {
      card.dataset.fallbackSrc = payload.thumb_url;
    }
    if (img && payload.thumb_url) {
      img.src = bustUrl(payload.thumb_url);
    }
    if (categorySelect && payload.category) {
      categorySelect.value = payload.category;
    }
    if (card && (payload.category || payload.template_slug)) {
      const tpl = payload.template_slug || '';
      const cat = payload.category || '';
      card.dataset.details = [tpl, cat].filter(Boolean).join(' • ');
    }
  };

  const swap = async (grid, tile) => {
    const slug = grid.dataset.studioSlug;
    const slot = tile.dataset.slot;
    if (!slug || !slot) return;

    const categorySelect = tile.querySelector('[data-studio-category]');
    const category = categorySelect ? categorySelect.value : '';

    const csrf = getCsrf();
    showOverlay(tile, true);
    try {
      const resp = await fetch(`/artwork/${encodeURIComponent(slug)}/mockups/${encodeURIComponent(slot)}/swap`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(csrf ? { 'X-CSRFToken': csrf } : {}),
          'Accept': 'application/json',
        },
        credentials: 'same-origin',
        body: JSON.stringify({ category }),
      });
      const data = await resp.json().catch(() => ({}));
      if (!resp.ok || !data || data.status !== 'ok') {
        throw new Error((data && (data.message || data.error)) || 'Swap failed');
      }
      updateTile(tile, data);
    } catch (err) {
      alert(err && err.message ? err.message : 'Swap failed');
    } finally {
      showOverlay(tile, false);
    }
  };

  grids.forEach((grid) => {
    grid.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-studio-swap]');
      if (!btn || !grid.contains(btn)) return;
      e.preventDefault();
      e.stopPropagation();
      const tile = btn.closest('[data-studio-tile]');
      if (!tile) return;
      if ((tile.dataset.kind || '') !== 'mockup') return;
      swap(grid, tile);
    });
  });
})();
