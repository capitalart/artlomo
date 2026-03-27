document.addEventListener('DOMContentLoaded', () => {
  const root = document.getElementById('detailCloseupApp');
  if (!root || typeof DetailCloseupEditor === 'undefined') {
    return;
  }

  const csrfMeta = document.querySelector('meta[name="csrf-token"]');
  const csrfToken = csrfMeta ? csrfMeta.getAttribute('content') || '' : '';

  const editor = new DetailCloseupEditor({
    viewportId: 'detailViewport',
    imageId: 'detailProxyImage',
    scaleDisplayId: 'scaleDisplay',
    zoomInBtnId: 'zoomInBtn',
    zoomOutBtnId: 'zoomOutBtn',
    snap1to1BtnId: 'snap1to1Btn',
    saveBtnId: 'saveBtn',
    updatePreviewBtnId: 'updatePreviewBtn',
    loadingOverlayId: 'detailLoadingOverlay',
    slug: root.getAttribute('data-slug') || '',
    csrfToken,
  });

  editor.init();
});
