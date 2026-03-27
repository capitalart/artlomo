(function () {
  'use strict';

  const btn = document.getElementById('check-latest');
  if (!btn) return;

  const results = document.getElementById('latest-results');
  const openaiModels = document.getElementById('openai-models');
  const geminiModels = document.getElementById('gemini-models');
  const openaiErr = document.getElementById('openai-error');
  const geminiErr = document.getElementById('gemini-error');

  btn.addEventListener('click', async () => {
    btn.disabled = true;
    try {
      const resp = await fetch('/admin/settings/check-latest', {
        credentials: 'same-origin',
        headers: { Accept: 'application/json' },
      });
      const data = await resp.json();

      if (results) {
        results.classList.add('visible');
        results.style.display = '';
      }
      if (openaiModels) openaiModels.textContent = (data.openai && data.openai.models ? data.openai.models : []).join('\n');
      if (geminiModels) geminiModels.textContent = (data.gemini && data.gemini.models ? data.gemini.models : []).join('\n');

      if (openaiErr) openaiErr.textContent = data.openai && data.openai.error ? 'Error: ' + data.openai.error : '';
      if (geminiErr) geminiErr.textContent = data.gemini && data.gemini.error ? 'Error: ' + data.gemini.error : '';
    } catch (e) {
      if (results) {
        results.classList.add('visible');
        results.style.display = '';
      }
      if (openaiErr) openaiErr.textContent = 'Error: ' + (e && e.message ? e.message : 'Failed to fetch');
    } finally {
      btn.disabled = false;
    }
  });

  const clearAllForms = document.querySelectorAll('form[data-clear-all-exports]');
  clearAllForms.forEach((form) => {
    form.addEventListener('submit', (e) => {
      if (!confirm('This will delete ALL exports. Continue?')) {
        e.preventDefault();
      }
    });
  });
})();
