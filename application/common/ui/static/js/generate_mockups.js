document.addEventListener('DOMContentLoaded', () => {
  const buttons = Array.from(document.querySelectorAll('[data-generate-mockups]'));
  if (!buttons.length) return;

  buttons.forEach((btn) => {
    const form = btn.closest('form');
    if (!form) return;
    form.addEventListener('submit', () => {
      if (!(btn instanceof HTMLButtonElement)) return;
      if (btn.classList.contains('is-loading')) return;
      btn.dataset.originalText = btn.textContent || '';
      btn.textContent = 'Generating...';
      btn.classList.add('is-loading');
      btn.disabled = true;
    });
  });
});
