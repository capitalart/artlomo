document.addEventListener('DOMContentLoaded', () => {
  const dropzone = document.querySelector('[data-upload-dropzone]');
  const fileInput = document.querySelector('[data-upload-input]');
  const selection = document.querySelector('[data-upload-selection]');
  const constraints = document.querySelector('[data-upload-constraints]');
  const maxFiles = Number(dropzone?.dataset.uploadMax || 25);
  const form = dropzone ? dropzone.closest('form') : null;
  const progressRoot = document.querySelector('[data-mockup-upload-progress]');
  const submitBtn = document.querySelector('[data-mockup-upload-submit]');
  const completeBtn = document.querySelector('[data-mockup-upload-complete]');

  const updateSelection = (files) => {
    if (!selection) return;
    if (!files || !files.length) {
      selection.textContent = 'No files selected yet.';
      return;
    }
    const names = Array.from(files).map((f) => f.name).slice(0, 3);
    const suffix = files.length > 3 ? ` …and ${files.length - 3} more` : '';
    selection.textContent = `${files.length} file(s): ${names.join(', ')}${suffix}`;
  };

  const applyFiles = (files) => {
    if (!fileInput || !files) return;
    const data = new DataTransfer();
    let accepted = 0;
    let rejected = 0;
    for (const file of Array.from(files)) {
      const isPng = file && (file.type === 'image/png' || file.name.toLowerCase().endsWith('.png'));
      if (!isPng) {
        rejected += 1;
        continue;
      }
      if (accepted >= maxFiles) {
        rejected += 1;
        continue;
      }
      data.items.add(file);
      accepted += 1;
    }
    fileInput.files = data.files;
    updateSelection(fileInput.files);
    if (constraints) {
      const details = [];
      if (rejected) details.push(`${rejected} file(s) ignored`);
      if (accepted > maxFiles) details.push(`max ${maxFiles} files per batch`);
      constraints.dataset.state = details.length ? 'warning' : '';
    }
  };

  if (!dropzone || !fileInput) return;

  dropzone.addEventListener('click', () => fileInput.click());

  ['dragenter', 'dragover'].forEach((evt) => {
    dropzone.addEventListener(evt, (event) => {
      event.preventDefault();
      dropzone.classList.add('dragover');
    });
  });

  ['dragleave', 'dragend', 'drop'].forEach((evt) => {
    dropzone.addEventListener(evt, () => dropzone.classList.remove('dragover'));
  });

  dropzone.addEventListener('drop', (event) => {
    event.preventDefault();
    applyFiles(event.dataTransfer?.files);
  });

  fileInput.addEventListener('change', (event) => {
    applyFiles(event.target.files);
  });

  // Ensure selection text matches any pre-filled FileList
  updateSelection(fileInput.files);

  const clearProgress = () => {
    if (!progressRoot) return;
    progressRoot.innerHTML = '';
    progressRoot.hidden = true;
  };

  const makeProgressItem = (fileName) => {
    if (!progressRoot) return null;
    const item = document.createElement('div');
    item.className = 'progress-item';

    const header = document.createElement('div');
    header.className = 'progress-header';

    const name = document.createElement('span');
    name.textContent = fileName;
    const pct = document.createElement('span');
    pct.textContent = '0%';
    pct.dataset.pct = 'true';

    header.appendChild(name);
    header.appendChild(pct);

    const bar = document.createElement('div');
    bar.className = 'progress-bar';
    const fill = document.createElement('div');
    fill.className = 'progress-fill';
    fill.style.width = '0%';
    fill.dataset.fill = 'true';
    bar.appendChild(fill);

    const status = document.createElement('p');
    status.className = 'progress-status';
    status.textContent = 'Queued';
    status.dataset.status = 'true';

    item.appendChild(header);
    item.appendChild(bar);
    item.appendChild(status);
    progressRoot.appendChild(item);
    progressRoot.hidden = false;
    return item;
  };

  const setItemProgress = (item, percent, statusText) => {
    if (!item) return;
    const pct = item.querySelector('[data-pct]');
    const fill = item.querySelector('[data-fill]');
    const status = item.querySelector('[data-status]');
    const clamped = Math.max(0, Math.min(100, Math.round(percent)));
    if (pct) pct.textContent = `${clamped}%`;
    if (fill) fill.style.width = `${clamped}%`;
    if (statusText && status) status.textContent = statusText;
  };

  const uploadSingle = (file, fields, item) => new Promise((resolve, reject) => {
    if (!form) {
      reject(new Error('Upload form not found.'));
      return;
    }
    const xhr = new XMLHttpRequest();
    xhr.open('POST', form.action);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    xhr.upload.onprogress = (evt) => {
      if (!evt.lengthComputable) return;
      const pct = (evt.loaded / evt.total) * 90;
      setItemProgress(item, pct, 'Uploading…');
    };

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const data = JSON.parse(xhr.responseText || '{}');
          if (!data || data.status !== 'ok') {
            reject(new Error((data && data.message) || 'Upload failed'));
            return;
          }
          setItemProgress(item, 100, 'Complete');
          resolve(data);
        } catch (err) {
          reject(err);
        }
        return;
      }
      try {
        const data = JSON.parse(xhr.responseText || '{}');
        reject(new Error((data && data.message) || `Upload failed (${xhr.status})`));
      } catch (err) {
        reject(new Error(`Upload failed (${xhr.status})`));
      }
    };

    xhr.onerror = () => reject(new Error('Network error during upload'));

    const fd = new FormData();
    Object.entries(fields || {}).forEach(([k, v]) => {
      if (v !== undefined && v !== null) fd.append(k, String(v));
    });
    fd.append('base_image', file, file.name);
    xhr.send(fd);
    setItemProgress(item, 0, 'Starting…');
  });

  const setButtonsDisabled = (disabled) => {
    if (submitBtn) submitBtn.disabled = !!disabled;
    if (fileInput) fileInput.disabled = !!disabled;
  };

  const runSequentialUpload = async () => {
    if (!form || !fileInput || !fileInput.files || !fileInput.files.length) return;
    if (submitBtn) submitBtn.hidden = false;
    if (completeBtn) completeBtn.hidden = true;
    clearProgress();
    setButtonsDisabled(true);

    const fields = {
      slug: form.querySelector('input[name="slug"]')?.value || '',
      category: form.querySelector('select[name="category"]')?.value || '',
      aspect_ratio: form.querySelector('input[name="aspect_ratio"]')?.value || '',
    };

    const files = Array.from(fileInput.files);
    for (const file of files) {
      const item = makeProgressItem(file.name);
      try {
        setItemProgress(item, 0, 'Queued');
        await uploadSingle(file, fields, item);
      } catch (err) {
        setItemProgress(item, 0, err instanceof Error ? err.message : 'Upload failed');
        setButtonsDisabled(false);
        return;
      }
    }

    setButtonsDisabled(false);
    if (submitBtn) submitBtn.hidden = true;
    if (completeBtn) completeBtn.hidden = false;
  };

  if (form) {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      runSequentialUpload();
    });
  }
});
