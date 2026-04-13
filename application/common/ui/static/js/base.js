document.addEventListener('DOMContentLoaded', () => {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.classList.add('fade');
      alert.classList.remove('show');
    }, 4000);
  });

  const themeHost = document.documentElement;
  const btn = document.querySelector('.site-header .theme-toggle')
    || document.getElementById('theme-toggle')
    || document.querySelector('.theme-toggle');
  const icon = btn ? btn.querySelector('.theme-icon') : document.querySelector('.theme-icon');

  const getIcon = (theme) => (theme === 'dark'
    ? '/static/icons/light.svg'
    : '/static/icons/dark.svg');

  const setSpinnerIcons = (theme) => {
    document.querySelectorAll('[data-theme-spinner]').forEach((el) => {
      el.src = theme === 'dark'
        ? '/static/icons/arrows-clockwise-dark.svg'
        : '/static/icons/arrows-clockwise-light.svg';
    });
  };

  const setTheme = (theme) => {
    const next = theme === 'dark' ? 'dark' : 'light';
    if (themeHost) {
      themeHost.dataset.theme = next;
      themeHost.classList.toggle('theme-dark', next === 'dark');
    }
    if (document.body) {
      document.body.dataset.theme = next;
      document.body.classList.toggle('theme-dark', next === 'dark');
      document.body.classList.toggle('dark-mode', next === 'dark');
    }
    localStorage.setItem('theme', next);
    if (btn) {
      btn.setAttribute('aria-pressed', next === 'dark');
    }
    if (icon) {
      icon.src = getIcon(next);
    }
    setSpinnerIcons(next);
  };

  const saved = localStorage.getItem('theme');
  const initial = saved || 'light';
  setTheme(initial);

  if (btn) {
    btn.addEventListener('click', (event) => {
      event.preventDefault();
      const current = themeHost ? themeHost.dataset.theme : 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      setTheme(next);
    });
  }

  document.addEventListener('change', (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) return;
    const mode = target.getAttribute('data-auto-submit');
    if (mode !== 'form') return;
    const form = target.closest('form');
    if (form instanceof HTMLFormElement) {
      form.submit();
    }
  });

  document.addEventListener('submit', (event) => {
    const target = event.target;
    if (!(target instanceof HTMLFormElement)) return;
    const message = target.getAttribute('data-confirm-message');
    if (!message) return;
    const ok = window.confirm(message);
    if (!ok) {
      event.preventDefault();
    }
  });

  // Modal carousel for artwork previews (delegated, defensive)
  const modal = document.getElementById('artPreviewModal');
  const modalImg = modal ? modal.querySelector('.modal-image') : null;
  const modalTitle = modal ? modal.querySelector('.meta-title') : null;
  const modalArtist = modal ? modal.querySelector('.meta-artist') : null;
  const modalDetails = modal ? modal.querySelector('.meta-details') : null;
  const modalNotice = modal ? modal.querySelector('.meta-notice') : null;
  const modalPrev = modal ? modal.querySelector('.modal-prev') : null;
  const modalNext = modal ? modal.querySelector('.modal-next') : null;
  const modalCloseBtn = modal ? modal.querySelector('.modal-close, .carousel-close-btn') : null;
  const modalDialog = modal ? modal.querySelector('.modal-dialog') : null;
  const backdrop = modal ? modal.querySelector('.modal-backdrop') : null;

  const state = {
    cards: [],
    artworks: [],
    currentIndex: -1,
    lastTrigger: null,
    usedFallback: false,
  };

  const collectArtworks = () => {
    const cards = Array.from(document.querySelectorAll('.art-card'));
    state.cards = cards;
    state.artworks = cards.map((card) => ({
      analyseSrc: card.dataset.analyseSrc || '',
      fallbackSrc: card.dataset.fallbackSrc || '',
      title: card.dataset.title || 'Untitled',
      artist: card.dataset.artist || '',
      details: card.dataset.details || '',
      aspect: card.dataset.aspect || '',
      resolution: card.dataset.resolution || '',
      dpi: card.dataset.dpi || '',
      filesize: card.dataset.filesize || '',
      uploaded: card.dataset.uploaded || '',
      print: card.dataset.print || '',
    }));
  };

  const buildDetailText = (art) => {
    const lineOne = [
      art.details,
      art.aspect && `Aspect: ${art.aspect}`,
      art.resolution && `Resolution: ${art.resolution}`,
      art.dpi && `DPI: ${art.dpi}`,
      art.filesize && `Filesize: ${art.filesize}`,
    ].filter(Boolean).join(' • ');

    const lineTwo = [
      art.uploaded && `Uploaded: ${art.uploaded}`,
      art.print && `Print: ${art.print}`,
    ].filter(Boolean).join(' • ');

    return [lineOne, lineTwo].filter(Boolean).join('\n');
  };

  const lockScroll = () => document.body.classList.add('modal-open');
  const unlockScroll = () => document.body.classList.remove('modal-open');

  const resetModal = () => {
    state.usedFallback = false;
    if (modalImg) {
      modalImg.removeAttribute('src');
      modalImg.alt = 'Artwork preview';
    }
    if (modalNotice) modalNotice.textContent = '';
  };

  const preloadNext = () => {
    if (state.artworks.length < 2) return;
    const nextIndex = (state.currentIndex + 1) % state.artworks.length;
    const next = state.artworks[nextIndex];
    const nextSrc = next.analyseSrc || next.fallbackSrc;
    if (nextSrc) {
      const img = new Image();
      img.src = nextSrc;
    }
  };

  const renderModal = () => {
    if (!modal || !modalImg || !modalTitle || !modalArtist || !modalDetails) return;
    const art = state.artworks[state.currentIndex];
    if (!art) return;
    resetModal();
    const src = art.analyseSrc || art.fallbackSrc;
    if (src) {
      modalImg.src = src;
    } else {
      modalImg.alt = 'Preview unavailable';
      if (modalNotice) modalNotice.textContent = 'Preview unavailable';
    }
    modalTitle.textContent = art.title || 'Untitled';
    modalArtist.textContent = art.artist || '';
    modalDetails.textContent = buildDetailText(art) || '';
    preloadNext();
  };

  const closeModal = () => {
    if (!modal) return;
    modal.classList.add('hidden');
    unlockScroll();
    state.currentIndex = -1;
    if (state.lastTrigger && typeof state.lastTrigger.focus === 'function') {
      state.lastTrigger.focus();
    }
  };

  const handleImageError = () => {
    const art = state.artworks[state.currentIndex];
    if (!art || !modalImg) return;
    if (!state.usedFallback && art.fallbackSrc && modalImg.src !== art.fallbackSrc) {
      state.usedFallback = true;
      modalImg.src = art.fallbackSrc;
      if (modalNotice) modalNotice.textContent = 'Analyse preview unavailable';
      return;
    }
    modalImg.removeAttribute('src');
    modalImg.alt = 'Preview unavailable';
    if (modalNotice) modalNotice.textContent = 'Preview unavailable (analyse missing)';
  };

  const openModal = (card, trigger) => {
    if (!modal) return;
    collectArtworks();
    const index = state.cards.indexOf(card);
    if (index < 0) return;
    state.currentIndex = index;
    state.lastTrigger = trigger || null;
    renderModal();
    modal.classList.remove('hidden');
    lockScroll();
    if (modalCloseBtn) modalCloseBtn.focus({ preventScroll: true });
  };

  const step = (delta) => {
    if (state.artworks.length === 0 || state.currentIndex < 0) return;
    state.currentIndex = (state.currentIndex + delta + state.artworks.length) % state.artworks.length;
    renderModal();
  };

  if (modal && modalImg && modalTitle && modalArtist && modalDetails && backdrop && modalDialog) {
    modalImg.addEventListener('error', handleImageError);

    document.addEventListener('click', (event) => {
      const img = event.target.closest('img');
      const card = event.target.closest('.art-card');
      const inModal = modal.contains(event.target);
      const isNav = event.target.closest('.modal-prev, .modal-next');
      const isCloseBtn = event.target.closest('.modal-close, .carousel-close-btn');

      // Open on thumbnail click (only when modal is hidden)
      if (modal.classList.contains('hidden') && img && card && card.contains(img)) {
        event.preventDefault();
        openModal(card, img);
        return;
      }

      // While open: clicking anywhere inside the modal (except nav buttons) closes it
      if (!modal.classList.contains('hidden') && inModal && !isNav) {
        if (isCloseBtn) {
          event.preventDefault();
        }
        closeModal();
        return;
      }

      // Backdrop click closes
      if (event.target === backdrop) {
        closeModal();
      }
    });

    modalDialog.addEventListener('click', (e) => {
      e.stopPropagation();
    });

    if (modalPrev) {
      modalPrev.addEventListener('click', (e) => {
        e.preventDefault();
        step(-1);
      });
    }

    if (modalNext) {
      modalNext.addEventListener('click', (e) => {
        e.preventDefault();
        step(1);
      });
    }

    if (modalCloseBtn) {
      modalCloseBtn.addEventListener('click', (e) => {
        e.preventDefault();
        closeModal();
      });
    }

    document.addEventListener('keydown', (e) => {
      if (modal.classList.contains('hidden')) return;
      if (e.key === 'Escape') closeModal();
      if (e.key === 'ArrowRight') step(1);
      if (e.key === 'ArrowLeft') step(-1);
    });
  }

});

  // Job Queue Notification Polling
  const jobIndicator = document.getElementById('jobIndicator');
  const jobCount = document.getElementById('jobCount');
  const jobSpinnerIcon = jobIndicator ? jobIndicator.querySelector('.fa-spinner') : null;
  
  if (jobIndicator && jobCount) {
    let lastNotificationShown = null;
    let lastSummary = { queued: 0, running: 0, done_recent: 0, failed_recent: 0 };

    const hideJobIndicator = () => {
      jobIndicator.style.display = 'none';
      if (jobSpinnerIcon) {
        jobSpinnerIcon.classList.remove('fa-spin');
      }
      jobCount.textContent = '0';
    };
    
    const updateJobIndicator = async () => {
      try {
        const response = await fetch('/api/jobs/summary');
        if (!response.ok) {
          hideJobIndicator();
          return;
        }
        
        const data = await response.json();
        lastSummary = {
          queued: Number(data.queued || 0),
          running: Number(data.running || 0),
          done_recent: Number(data.done_recent || 0),
          failed_recent: Number(data.failed_recent || 0),
        };
        const totalActive = (data.queued || 0) + (data.running || 0);
        const hasDone = (data.done_recent || 0) > 0;
        const hasFailed = (data.failed_recent || 0) > 0;
        const completionCount = (data.done_recent || 0) + (data.failed_recent || 0);
        
        // Show/hide indicator
        if (totalActive > 0 || hasDone || hasFailed) {
          jobIndicator.style.display = 'flex';
          jobCount.textContent = String(totalActive > 0 ? totalActive : completionCount);

          // Spin only when there is actual active work.
          if (jobSpinnerIcon) {
            jobSpinnerIcon.classList.toggle('fa-spin', totalActive > 0);
          }
          
          // Update icon state
          jobIndicator.classList.remove('has-failures', 'has-completions');
          if (hasFailed) {
            jobIndicator.classList.add('has-failures');
          } else if (hasDone && totalActive === 0) {
            jobIndicator.classList.add('has-completions');
          }
          
          // Show toast notification for newly completed jobs
          if ((hasDone || hasFailed) && totalActive === 0) {
            const notificationKey = `${data.done_recent || 0}-${data.failed_recent || 0}`;
            if (lastNotificationShown !== notificationKey) {
              showJobCompletionToast(data.done_recent || 0, data.failed_recent || 0);
              lastNotificationShown = notificationKey;
            }
          }
        } else {
          hideJobIndicator();
          lastNotificationShown = null;
        }
      } catch (err) {
        console.error('Job polling error:', err);
        hideJobIndicator();
      }
    };
    
    const showJobCompletionToast = (doneCount, failedCount) => {
      const message = [];
      if (doneCount > 0) {
        message.push(`✓ ${doneCount} analysis job${doneCount > 1 ? 's' : ''} completed`);
      }
      if (failedCount > 0) {
        message.push(`✗ ${failedCount} job${failedCount > 1 ? 's' : ''} failed`);
      }
      
      if (message.length === 0) return;
      
      // Create toast element
      const toast = document.createElement('div');
      toast.className = 'job-toast';
      toast.textContent = message.join(' • ');
      toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        right: 24px;
        padding: 12px 20px;
        background: var(--color-bg-primary, #333);
        color: #fff;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        animation: slideInUp 0.3s ease;
        cursor: pointer;
        font-size: 14px;
      `;
      
      document.body.appendChild(toast);
      
      toast.addEventListener('click', () => {
        toast.remove();
      });
      
      setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
      }, 5000);
    };
    
    // Poll every 3 seconds
    updateJobIndicator();
    setInterval(updateJobIndicator, 3000);
    
    // Click handler to show recent jobs
    jobIndicator.addEventListener('click', async () => {
      try {
        const response = await fetch('/api/jobs/recent');
        if (!response.ok) return;
        
        const data = await response.json();
        const jobs = data.jobs || [];
        
        if (jobs.length === 0) {
          let queued = Number(lastSummary.queued || 0);
          let running = Number(lastSummary.running || 0);

          // Refresh from API; if this fails, keep cached values.
          try {
            const summaryResp = await fetch('/api/jobs/summary');
            if (summaryResp.ok) {
              const summary = await summaryResp.json();
              queued = Number(summary.queued || 0);
              running = Number(summary.running || 0);
            }
          } catch (_err) {
            // Keep cached summary values.
          }

          const active = queued + running;
          if (active > 0) {
            alert(`Active analysis jobs: ${active} (queued: ${queued}, running: ${running})`);
            return;
          }

          // Self-heal stale indicator state if there are no active/recent jobs.
          hideJobIndicator();
          alert('No recent jobs');
          return;
        }
        
        // Simple alert for now (can be enhanced with modal)
        const lines = jobs.slice(0, 5).map(job => 
          `${job.status === 'DONE' ? '✓' : '✗'} ${job.provider}: ${job.slug} (${job.status})`
        );
        alert('Recent Jobs:\n\n' + lines.join('\n'));
      } catch (err) {
        console.error('Failed to fetch recent jobs:', err);
      }
    });
  }
