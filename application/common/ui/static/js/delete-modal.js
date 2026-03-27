document.addEventListener('DOMContentLoaded', () => {
  if (window.location && window.location.pathname && window.location.pathname.startsWith('/artworks')) {
    return; // Artworks workflow owns its own delete modal; skip global binding.
  }
  const modal = document.querySelector('[data-modal="delete"]');
  if (!modal) return;

  const slugEl = modal.querySelector('[data-modal-slug]');
  const thumbEl = modal.querySelector('[data-modal-thumb]');
  const confirmBtn = modal.querySelector('[data-modal-confirm]');
  const dismissBtns = modal.querySelectorAll('[data-modal-dismiss]');

  const closeModal = () => {
    modal.dataset.open = 'false';
    modal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('overlay-lock');
  };

  const openModal = (slug, thumbUrl) => {
    if (slugEl) slugEl.textContent = slug || '';
    if (thumbEl) {
      thumbEl.src = thumbUrl || '';
      thumbEl.alt = slug ? `${slug} thumbnail` : 'Artwork thumbnail';
    }
    if (confirmBtn) {
      confirmBtn.disabled = true;
    }
    modal.dataset.open = 'true';
    modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('overlay-lock');
  };

  document.querySelectorAll('[data-delete-trigger]').forEach((btn) => {
    btn.addEventListener('click', (event) => {
      event.preventDefault();
      const slug = btn.dataset.slug || '';
      const thumb = btn.dataset.thumb || '';
      openModal(slug, thumb);
    });
  });

  // Explicitly wire close to any dismiss control
  dismissBtns.forEach((btn) => btn.addEventListener('click', () => closeModal()));
  modal.querySelectorAll('.modal-close').forEach((btn) => btn.addEventListener('click', () => closeModal()));

  modal.addEventListener('click', (event) => {
    if (event.target === modal) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && modal.dataset.open === 'true') {
      closeModal();
    }
  });
});
