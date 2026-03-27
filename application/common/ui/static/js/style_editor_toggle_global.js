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

  function applyState(enabled) {
    const darkroomLink = document.getElementById('darkroom-stylesheet');
    if (!darkroomLink) {
      return;
    }
    darkroomLink.media = enabled ? '' : 'not all';
  }

  let isEnabled = getStoredState();

  function init() {
    applyState(isEnabled);
  }

  window.toggleStyleEditor = function (enable) {
    isEnabled = enable !== undefined ? Boolean(enable) : !isEnabled;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(isEnabled));
    applyState(isEnabled);
    return isEnabled;
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
