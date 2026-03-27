(function () {
  const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content || '';

  document.querySelectorAll('img[data-thumb-fallback="true"]').forEach((img) => {
    img.addEventListener('error', () => {
      img.style.display = 'none';
      const placeholder = img.nextElementSibling;
      if (placeholder) {
        placeholder.classList.remove('thumb-placeholder-hidden');
      }
    });
  });

  document.querySelectorAll('[data-restore-trigger]').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const url = btn.dataset.restoreUrl;
      if (!url) return;
      btn.disabled = true;
      try {
        const resp = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
        });
        const data = await resp.json();
        if (data.status === 'ok') {
          btn.closest('.gallery-card')?.remove();
          if (!document.querySelector('.gallery-card')) {
            location.reload();
          }
        } else {
          alert('Failed to restore: ' + (data.message || 'Unknown error'));
          btn.disabled = false;
        }
      } catch (e) {
        alert('Error: ' + (e && e.message ? e.message : 'Unknown error'));
        btn.disabled = false;
      }
    });
  });

  const modal = document.getElementById('permanentDeleteModal');
  const input = document.querySelector('[data-permanent-delete-input]');
  const confirmBtn = document.querySelector('[data-permanent-delete-confirm]');
  const countDisplay = document.querySelector('[data-delete-count]');
  const selectAllBtn = document.querySelector('[data-bulk-select-all]');
  const deselectAllBtn = document.querySelector('[data-bulk-deselect-all]');
  const bulkRestoreBtn = document.querySelector('[data-bulk-restore-trigger]');
  const bulkDeleteBtn = document.querySelector('[data-bulk-permanent-delete-trigger]');
  const bulkCount = document.querySelector('[data-bulk-count]');
  const checkboxes = document.querySelectorAll('[data-bulk-select]');

  let pendingDeleteUrls = [];

  function openPermanentDeleteModal(urls) {
    if (!modal || !confirmBtn || !input || !countDisplay) return;
    pendingDeleteUrls = urls;
    countDisplay.textContent = String(urls.length);
    input.value = '';
    confirmBtn.disabled = true;
    confirmBtn.textContent = 'Delete Forever';
    modal.classList.remove('hidden');
    modal.setAttribute('aria-hidden', 'false');
    input.focus();
  }

  function closePermanentDeleteModal() {
    if (!modal) return;
    modal.classList.add('hidden');
    modal.setAttribute('aria-hidden', 'true');
  }

  document.querySelectorAll('[data-permanent-delete-trigger]').forEach((btn) => {
    btn.addEventListener('click', () => {
      if (!btn.dataset.deleteUrl) return;
      openPermanentDeleteModal([btn.dataset.deleteUrl]);
    });
  });

  function updateBulkState() {
    const selected = document.querySelectorAll('[data-bulk-select]:checked');
    const count = selected.length;
    if (bulkRestoreBtn) bulkRestoreBtn.disabled = count === 0;
    if (bulkDeleteBtn) bulkDeleteBtn.disabled = count === 0;
    if (bulkCount) {
      bulkCount.textContent = count > 0 ? `${count} selected` : '';
      bulkCount.hidden = count === 0;
    }
  }

  checkboxes.forEach((cb) => cb.addEventListener('change', updateBulkState));

  selectAllBtn?.addEventListener('click', () => {
    checkboxes.forEach((cb) => {
      cb.checked = true;
    });
    updateBulkState();
  });

  deselectAllBtn?.addEventListener('click', () => {
    checkboxes.forEach((cb) => {
      cb.checked = false;
    });
    updateBulkState();
  });

  bulkDeleteBtn?.addEventListener('click', () => {
    const selected = document.querySelectorAll('[data-bulk-select]:checked');
    const urls = Array.from(selected)
      .map((cb) => cb.closest('.gallery-card')?.querySelector('[data-permanent-delete-trigger]')?.dataset?.deleteUrl)
      .filter(Boolean);
    if (urls.length > 0) {
      openPermanentDeleteModal(urls);
    }
  });

  bulkRestoreBtn?.addEventListener('click', async () => {
    const selected = document.querySelectorAll('[data-bulk-select]:checked');
    if (!selected.length) return;

    bulkRestoreBtn.disabled = true;
    bulkRestoreBtn.textContent = 'Restoring...';

    for (const cb of selected) {
      const card = cb.closest('.gallery-card');
      const restoreBtn = card?.querySelector('[data-restore-trigger]');
      const restoreUrl = restoreBtn?.dataset?.restoreUrl;
      if (!restoreUrl) continue;
      try {
        await fetch(restoreUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
        });
        card?.remove();
      } catch (e) {
      }
    }

    if (!document.querySelector('.gallery-card')) {
      location.reload();
      return;
    }

    bulkRestoreBtn.textContent = 'Restore Selected';
    updateBulkState();
  });

  input?.addEventListener('input', () => {
    if (!confirmBtn || !input) return;
    confirmBtn.disabled = input.value.trim() !== 'DELETE FOREVER';
  });

  confirmBtn?.addEventListener('click', async () => {
    if (!input || input.value.trim() !== 'DELETE FOREVER') return;

    confirmBtn.disabled = true;
    confirmBtn.textContent = 'Deleting...';

    for (const url of pendingDeleteUrls) {
      try {
        await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
        });
      } catch (e) {
      }
    }

    closePermanentDeleteModal();
    location.reload();
  });

  document.querySelectorAll('[data-delete-dismiss]').forEach((el) => {
    el.addEventListener('click', closePermanentDeleteModal);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && !modal.classList.contains('hidden')) {
      closePermanentDeleteModal();
    }
  });

  updateBulkState();
})();
