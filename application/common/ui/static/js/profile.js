(function () {
  'use strict';

  const modal = document.querySelector('[data-modal="delete-account"]');
  const openBtn = document.getElementById('delete-account-btn');
  const confirmInput = document.getElementById('delete-confirm-input');
  const confirmBtn = document.getElementById('confirm-delete-btn');
  const dismissBtns = document.querySelectorAll('[data-modal-dismiss-account]');

  if (!modal || !openBtn || !confirmInput || !confirmBtn) {
    return;
  }

  const expectedUsername = modal.getAttribute('data-expected-username') || '';

  function openModal() {
    modal.classList.remove('modal-hidden');
    modal.setAttribute('aria-hidden', 'false');
    confirmInput.value = '';
    confirmBtn.disabled = true;
  }

  function closeModal() {
    modal.classList.add('modal-hidden');
    modal.setAttribute('aria-hidden', 'true');
  }

  openBtn.addEventListener('click', openModal);
  dismissBtns.forEach((btn) => btn.addEventListener('click', closeModal));

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });

  confirmInput.addEventListener('input', () => {
    confirmBtn.disabled = confirmInput.value !== expectedUsername;
  });
})();
