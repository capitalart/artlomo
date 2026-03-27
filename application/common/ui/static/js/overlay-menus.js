document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.querySelector('[data-overlay="admin"]');
  const toggles = Array.from(document.querySelectorAll('[data-overlay-toggle="admin"]'));
  if (!overlay || !toggles.length) return;

  let isOpen = false;

  const syncToggles = () => {
    toggles.forEach((toggle) => {
      toggle.dataset.open = isOpen ? 'true' : 'false';
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      const arrow = toggle.querySelector('.overlay-arrow');
      if (arrow) {
        arrow.textContent = isOpen ? '↑' : '↓';
      }
    });
  };

  const lockBody = () => {
    if (isOpen) {
      document.body.dataset.overlayOpen = 'true';
      document.body.classList.add('overlay-lock');
    } else {
      document.body.removeAttribute('data-overlay-open');
      document.body.classList.remove('overlay-lock');
    }
  };

  const close = () => {
    isOpen = false;
    overlay.dataset.open = 'false';
    overlay.setAttribute('aria-hidden', 'true');
    syncToggles();
    lockBody();
  };

  const open = () => {
    isOpen = true;
    overlay.dataset.open = 'true';
    overlay.setAttribute('aria-hidden', 'false');
    syncToggles();
    lockBody();
  };

  toggles.forEach((toggle) => {
    const toggleAction = (event) => {
      event.preventDefault();
      if (isOpen) {
        close();
      } else {
        open();
      }
    };
    toggle.addEventListener('click', toggleAction);
    toggle.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        toggleAction(event);
      }
    });
  });

  overlay.addEventListener('click', (event) => {
    if (event.target === overlay || event.target.dataset.overlayBackdrop === 'admin') {
      close();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && isOpen) {
      close();
    }
  });

  syncToggles();
  lockBody();
});
