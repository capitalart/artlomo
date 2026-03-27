(function () {
  let currentIndex = 0;
  let carouselImages = [];

  const modal = document.getElementById('mockupCarouselModal');
  const image = document.getElementById('carouselImage');
  const counter = document.getElementById('carouselCounter');
  const checkbox = document.getElementById('carouselCheckbox');

  if (!modal || !image || !counter || !checkbox) {
    return;
  }

  const initCarousel = () => {
    carouselImages = Array.from(document.querySelectorAll('[data-carousel-trigger]'))
      .map((el) => {
        const parent = el.parentElement;
        return {
          fullUrl: ((parent && parent.getAttribute('data-full-url')) || '').trim(),
          mockupId: ((parent && parent.getAttribute('data-mockup-id')) || '').trim(),
          slot: ((parent && parent.getAttribute('data-slot')) || '').trim(),
        };
      })
      .filter((imgItem) => imgItem.fullUrl);
  };

  const syncCheckboxFromSlide = () => {
    if (!carouselImages[currentIndex]) return;
    const mockupId = carouselImages[currentIndex].mockupId;
    const storyboardCheckbox = document.querySelector(
      `.storyboard-item[data-mockup-id="${mockupId}"] input[data-storyboard-checkbox]`,
    );
    checkbox.checked = Boolean(storyboardCheckbox && storyboardCheckbox.checked);
  };

  const renderSlide = () => {
    if (!carouselImages[currentIndex]) return;
    image.src = carouselImages[currentIndex].fullUrl;
    image.alt = `Mockup ${carouselImages[currentIndex].slot}`;
    counter.textContent = `${currentIndex + 1} / ${carouselImages.length}`;
    syncCheckboxFromSlide();
  };

  const openCarousel = (index) => {
    if (carouselImages.length === 0) return;
    currentIndex = Math.max(0, Math.min(index, carouselImages.length - 1));
    renderSlide();
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  };

  const closeModal = () => {
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  };

  const nextSlide = () => {
    if (carouselImages.length === 0) return;
    currentIndex = (currentIndex + 1) % carouselImages.length;
    renderSlide();
  };

  const previousSlide = () => {
    if (carouselImages.length === 0) return;
    currentIndex = (currentIndex - 1 + carouselImages.length) % carouselImages.length;
    renderSlide();
  };

  const attachOpenListeners = () => {
    document.querySelectorAll('[data-carousel-trigger]').forEach((el, index) => {
      el.addEventListener('click', (event) => {
        event.stopPropagation();
        openCarousel(index);
      });
      el.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          openCarousel(index);
        }
      });
    });
  };

  const attachModalListeners = () => {
    let touchStartX = 0;
    let touchStartY = 0;
    const SWIPE_THRESHOLD = 45;

    modal.addEventListener('click', (event) => {
      if (event.target === modal) {
        closeModal();
      }
    });

    // Support horizontal swipe navigation on touch devices.
    modal.addEventListener('touchstart', (event) => {
      const touch = event.touches && event.touches[0];
      if (!touch) return;
      touchStartX = touch.clientX;
      touchStartY = touch.clientY;
    }, { passive: true });

    modal.addEventListener('touchend', (event) => {
      if (modal.classList.contains('hidden')) return;
      const touch = event.changedTouches && event.changedTouches[0];
      if (!touch) return;
      const deltaX = touch.clientX - touchStartX;
      const deltaY = touch.clientY - touchStartY;

      // Only react to primarily horizontal gestures.
      if (Math.abs(deltaX) < SWIPE_THRESHOLD || Math.abs(deltaX) <= Math.abs(deltaY)) {
        return;
      }
      if (deltaX < 0) {
        nextSlide();
      } else {
        previousSlide();
      }
    }, { passive: true });

    const closeBtn = modal.querySelector('[data-carousel-close]');
    const prevBtn = modal.querySelector('[data-carousel-prev]');
    const nextBtn = modal.querySelector('[data-carousel-next]');

    if (closeBtn) {
      closeBtn.addEventListener('click', (event) => {
        event.stopPropagation();
        closeModal();
      });
    }
    if (prevBtn) {
      prevBtn.addEventListener('click', (event) => {
        event.stopPropagation();
        previousSlide();
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', (event) => {
        event.stopPropagation();
        nextSlide();
      });
    }

    document.querySelectorAll('[data-stop-propagation]').forEach((el) => {
      el.addEventListener('click', (event) => {
        event.stopPropagation();
      });
    });

    checkbox.addEventListener('change', () => {
      if (!carouselImages[currentIndex]) return;
      const mockupId = carouselImages[currentIndex].mockupId;
      const storyboardCheckbox = document.querySelector(
        `.storyboard-item[data-mockup-id="${mockupId}"] input[data-storyboard-checkbox]`,
      );
      if (!storyboardCheckbox) return;
      storyboardCheckbox.checked = checkbox.checked;
      storyboardCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
    });

    document.addEventListener('keydown', (event) => {
      if (modal.classList.contains('hidden')) return;
      if (event.key === 'ArrowLeft') {
        event.preventDefault();
        previousSlide();
      } else if (event.key === 'ArrowRight') {
        event.preventDefault();
        nextSlide();
      } else if (event.key === 'Escape') {
        event.preventDefault();
        closeModal();
      }
    });
  };

  const init = () => {
    initCarousel();
    attachOpenListeners();
    attachModalListeners();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
