(function () {
  const grid = document.querySelector('#mockup-grid');
  if (!grid) return;

  const artworkId = grid.dataset.artworkId;
  const csrf = grid.dataset.csrf || '';

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

  const updateCard = (card, payload) => {
    const img = card.querySelector('img');
    if (img && payload.thumb_url) {
      const bust = `t=${Date.now()}`;
      img.src = `${payload.thumb_url}?${bust}`;
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
      const resp = await fetch(`/admin/artworks/${artworkId}/manual/mockups/${slot}/swap`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(csrf ? { 'X-CSRFToken': csrf } : {}),
        },
        credentials: 'same-origin',
        body: JSON.stringify({ category }),
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
})();
