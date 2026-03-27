document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.querySelector('input[name="artwork"]');
  if (!fileInput) return;
  fileInput.addEventListener('change', () => {
    if (fileInput.files && fileInput.files[0]) {
      fileInput.classList.remove('is-invalid');
    }
  });
});
