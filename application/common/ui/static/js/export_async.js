document.addEventListener('DOMContentLoaded', () => {
  const csrfToken = (() => {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? (meta.getAttribute('content') || '').trim() : '';
  })();

  const postJson = async (url, payload) => {
    const resp = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify(payload || {}),
      credentials: 'same-origin',
    });

    let data = null;
    try {
      data = await resp.json();
    } catch (e) {
      data = null;
    }
    return { resp, data };
  };

  const getJson = async (url) => {
    const resp = await fetch(url, {
      headers: { 'Accept': 'application/json' },
      credentials: 'same-origin',
    });

    let data = null;
    try {
      data = await resp.json();
    } catch (e) {
      data = null;
    }
    return { resp, data };
  };

  const showExportConfirmationModal = async (sku) => {
    return new Promise((resolve) => {
      const modal = document.getElementById('exportConfirmationModal');
      if (!modal) {
        console.warn('Export confirmation modal not found');
        resolve(true); // Default to continue
        return;
      }

      const continueBtn = modal.querySelector('[data-confirm-continue]');
      const cancelBtn = modal.querySelector('[data-confirm-cancel]');

      const cleanup = () => {
        modal.classList.remove('export-modal-open');
        continueBtn.removeEventListener('click', onContinue);
        cancelBtn.removeEventListener('click', onCancel);
      };

      const onContinue = () => {
        cleanup();
        resolve(true);
      };

      const onCancel = () => {
        cleanup();
        resolve(false);
      };

      continueBtn.addEventListener('click', onContinue);
      cancelBtn.addEventListener('click', onCancel);

      modal.classList.add('export-modal-open');
    });
  };

  const pollExportStatus = async ({ sku, onUpdate, timeoutMs = 10 * 60 * 1000 }) => {
    const start = Date.now();
    while (Date.now() - start < timeoutMs) {
      let resp;
      let data;
      try {
        resp = await fetch(`/api/export/status/${encodeURIComponent(sku)}`, {
          headers: { 'Accept': 'application/json' },
          credentials: 'same-origin',
        });
        data = await resp.json();
      } catch (e) {
        await new Promise((r) => setTimeout(r, 750));
        continue;
      }

      if (typeof onUpdate === 'function') onUpdate({ resp, data });

      if (resp && resp.ok && data && data.done) return data;

      await new Promise((r) => setTimeout(r, 750));
    }

    return null;
  };

  const exportButtons = Array.from(document.querySelectorAll('[data-export-async]'));
  exportButtons.forEach((el) => {
    el.addEventListener('click', async (event) => {
      if (!(el instanceof HTMLElement)) return;
      event.preventDefault();

      const sku = (el.getAttribute('data-sku') || '').trim();
      if (!sku) return;

      const includeMockupsRaw = (el.getAttribute('data-include-mockups') || '1').trim();
      const enforceRequiredRaw = (el.getAttribute('data-enforce-required') || '0').trim();
      const include_mockups = includeMockupsRaw === '1' || includeMockupsRaw.toLowerCase() === 'true';
      const enforce_required = enforceRequiredRaw === '1' || enforceRequiredRaw.toLowerCase() === 'true';

      const originalText = el.textContent;
      el.setAttribute('aria-disabled', 'true');
      el.classList.add('disabled');
      el.textContent = 'Checking mockups…';

      // Check if mockups exist
      let hasMockups = true; // Default to true to avoid blocking exports if check fails
      try {
        const { resp, data } = await getJson(`/api/export/has-mockups/${encodeURIComponent(sku)}`);
        if (resp && resp.ok && data && typeof data.has_mockups === 'boolean') {
          hasMockups = data.has_mockups;
        }
      } catch (e) {
        console.error('Failed to check mockups:', e);
        // Continue with default (hasMockups = true)
      }

      // If no mockups, show confirmation modal
      if (!hasMockups) {
        const userConfirmed = await showExportConfirmationModal(sku);
        if (!userConfirmed) {
          el.textContent = originalText;
          el.classList.remove('disabled');
          el.removeAttribute('aria-disabled');
          return;
        }
      }

      el.textContent = 'Queued…';

      const { resp, data } = await postJson(`/api/export/${encodeURIComponent(sku)}`, {
        csrf_token: csrfToken,
        include_mockups,
        enforce_required,
      });

      if (!resp.ok) {
        el.textContent = originalText;
        el.classList.remove('disabled');
        el.removeAttribute('aria-disabled');
        window.alert((data && (data.message || data.error)) || 'Failed to start export');
        return;
      }

      el.textContent = 'Exporting…';

      const result = await pollExportStatus({
        sku,
        onUpdate: ({ data: status }) => {
          if (!status) return;
          const stage = (status.stage || '').toString();
          if (stage) el.textContent = `Exporting… (${stage})`;
        },
      });

      if (!result) {
        el.textContent = originalText;
        el.classList.remove('disabled');
        el.removeAttribute('aria-disabled');
        window.alert('Timed out waiting for export to complete');
        return;
      }

      if (result.error) {
        el.textContent = originalText;
        el.classList.remove('disabled');
        el.removeAttribute('aria-disabled');
        window.alert(result.error);
        return;
      }

      if (result.download_url) {
        window.location.href = result.download_url;
        el.textContent = 'Export Again';
        el.classList.remove('disabled');
        el.removeAttribute('aria-disabled');
        return;
      }

      el.textContent = 'Export Again';
      el.classList.remove('disabled');
      el.removeAttribute('aria-disabled');
    });
  });
});
