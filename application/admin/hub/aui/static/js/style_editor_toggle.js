(function () {
  const STORAGE_KEY = 'artlomo-style-editor-enabled';

  function getStoredState() {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw === null) {
      return true;
    }
    try {
      return JSON.parse(raw);
    } catch (_err) {
      return true;
    }
  }

  function applyStatus(statusEl, enabled) {
    statusEl.textContent = enabled ? 'Enabled' : 'Disabled';
    statusEl.classList.toggle('style-editor-status--enabled', enabled);
    statusEl.classList.toggle('style-editor-status--disabled', !enabled);
  }

  function init() {
    const toggle = document.getElementById('style-editor-toggle');
    const status = document.getElementById('style-editor-status');
    if (!toggle || !status) {
      return;
    }

    const initial = getStoredState();
    toggle.checked = Boolean(initial);
    applyStatus(status, Boolean(initial));

    toggle.addEventListener('change', function () {
      const handler = window.toggleStyleEditor;
      const next = typeof handler === 'function' ? handler(toggle.checked) : toggle.checked;
      applyStatus(status, Boolean(next));
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
