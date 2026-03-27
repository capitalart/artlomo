// CLINE_DIRECTIVE: High-res images are 2048px. Modal must be appended to document.body. Do not use fixed pixel constraints.

(function () {
  const modal = document.querySelector('[data-carousel-modal]');
  if (!modal) return;

  const backdrop = modal;
  const imgEl = modal.querySelector('[data-carousel-image]');
  const titleEl = modal.querySelector('[data-carousel-title]');
  const counterEl = modal.querySelector('[data-carousel-counter]');
  const openLink = modal.querySelector('[data-carousel-open]');
  const closeBtn = modal.querySelector('[data-carousel-close]');
  const prevBtn = modal.querySelector('[data-carousel-prev]');
  const nextBtn = modal.querySelector('[data-carousel-next]');

  let items = [];
  let current = 0;

  const render = () => {
    if (!items.length || !imgEl) return;
    const item = items[current];
    imgEl.src = item.full;
    imgEl.alt = item.name || 'Base image';
    if (titleEl) titleEl.textContent = item.name || 'Base preview';
    if (counterEl) counterEl.textContent = `${current + 1} / ${items.length}`;
    if (openLink) openLink.href = item.full;
  };

  const openAt = (idx) => {
    if (!items.length) return;
    current = ((idx % items.length) + items.length) % items.length;
    backdrop.dataset.open = 'true';
    backdrop.dataset.visible = '1';
    render();
  };

  const close = () => {
    backdrop.dataset.open = 'false';
    backdrop.dataset.visible = '';
  };

  const collect = () => {
    // Ensure modal is at the end of body to avoid stacking context issues
    if (modal.parentNode !== document.body) {
      document.body.appendChild(modal);
    }

    items = [];
    
    // Collect artwork (ANALYSE 2048px version)
    document.querySelectorAll('[data-carousel-artwork]').forEach((thumb) => {
      const full = thumb.getAttribute('data-analyse-src') || thumb.getAttribute('data-fallback-src');
      const name = thumb.getAttribute('data-title') || 'Artwork';
      if (!full) return;
      const record = { full, name, thumb, type: 'artwork' };
      items.push(record);
      thumb.style.cursor = 'pointer';
    });
    
    // Collect detail closeups (2000px version)
    document.querySelectorAll('[data-carousel-detail]').forEach((thumb) => {
      const full = thumb.getAttribute('data-analyse-src') || thumb.getAttribute('data-fallback-src');
      const name = thumb.getAttribute('data-title') || 'Detail Closeup';
      if (!full) return;
      const record = { full, name, thumb, type: 'detail' };
      items.push(record);
      thumb.style.cursor = 'pointer';
    });
    
    // Collect mockups (2000px version)
    document.querySelectorAll('[data-mockup-thumb]').forEach((thumb) => {
      const full = thumb.getAttribute('data-full-image') || thumb.getAttribute('data-analyse-src');
      const name = thumb.getAttribute('data-mockup-name') || thumb.getAttribute('data-title') || 'Mockup';
      if (!full) return;
      const record = { full, name, thumb, type: 'mockup' };
      items.push(record);
      thumb.style.cursor = 'pointer';
    });
  };

  collect();

  if (closeBtn) closeBtn.addEventListener('click', close);
  
  // Enhanced click-outside-to-close functionality
  if (backdrop) {
    backdrop.addEventListener('click', (evt) => {
      // Only close if clicking directly on the backdrop (black blurry area)
      if (evt.target === backdrop) {
        close();
      }
    });
  }
  
  // Prevent accidental closes when clicking the image or navigation
  if (imgEl) {
    imgEl.addEventListener('click', (evt) => {
      evt.stopPropagation();
    });
  }
  
  // Prevent closes when clicking metadata/controls
  const modalCard = modal.querySelector('.modal-card');
  if (modalCard) {
    modalCard.addEventListener('click', (evt) => {
      evt.stopPropagation();
    });
  }
  
  if (prevBtn) prevBtn.addEventListener('click', () => openAt(current - 1));
  if (nextBtn) nextBtn.addEventListener('click', () => openAt(current + 1));
  document.addEventListener('keydown', (evt) => {
    if (backdrop.dataset.visible) {
      if (evt.key === 'Escape') close();
      if (evt.key === 'ArrowLeft') openAt(current - 1);
      if (evt.key === 'ArrowRight') openAt(current + 1);
    }
  });

  // Global event delegation for opening carousel from dynamically created elements
  document.addEventListener('click', (e) => {
    // Check for carousel trigger elements (could be direct clicks or bubbled)
    const trigger = e.target.closest('[data-carousel-artwork], [data-carousel-detail], [data-mockup-thumb], .open-carousel, .artwork-card, .detail-thumb');
    
    if (trigger && !trigger.closest('[data-carousel-modal]')) {
      // Find which item was clicked and open at that index
      const clickedThumb = trigger.closest('[data-carousel-artwork], [data-carousel-detail], [data-mockup-thumb]');
      if (clickedThumb) {
        const itemIndex = Array.from(document.querySelectorAll('[data-carousel-artwork], [data-carousel-detail], [data-mockup-thumb]')).indexOf(clickedThumb);
        if (itemIndex !== -1 && itemIndex < items.length) {
          e.preventDefault();
          e.stopPropagation();
          openAt(itemIndex);
        }
      }
    }
  }, true); // Use capture phase for better event delegation

})();
