document.addEventListener('DOMContentLoaded', () => {
  const dropzone = document.querySelector('[data-upload-dropzone]');
  const fileInput = document.querySelector('[data-upload-input]');
  const directoryInput = document.querySelector('[data-upload-directory-input]');
  const directoryTrigger = document.querySelector('[data-upload-directory-trigger]');
  const selection = document.querySelector('[data-upload-selection]');
  const constraints = document.querySelector('[data-upload-constraints]');
  const maxFiles = Number(dropzone?.dataset.uploadMax || 25);
  const form = dropzone ? dropzone.closest('form') : null;
  const progressRoot = document.querySelector('[data-mockup-upload-progress]');
  const submitBtn = document.querySelector('[data-mockup-upload-submit]');
  const completeBtn = document.querySelector('[data-mockup-upload-complete]');
  let queuedItems = [];

  const inferMeta = (relativePath, fileName) => {
    const cleaned = String(relativePath || fileName || '').replace(/\\/g, '/');
    const parts = cleaned.split('/').filter(Boolean);
    const stem = String(fileName || '').replace(/\.[^.]+$/, '');

    let aspect = '';
    let category = '';
    if (parts.length >= 3) {
      // Prefer immediate parent folders of the asset stem for nested exports:
      // <root>/<aspect>/<category>/<asset>/<asset>.png
      const stemIndex = parts.findIndex((segment) => {
        const normalized = String(segment || '').replace(/\.[^.]+$/, '');
        return normalized === stem;
      });
      if (stemIndex >= 2) {
        aspect = parts[stemIndex - 2] || '';
        category = parts[stemIndex - 1] || '';
      } else {
        aspect = parts[0] || '';
        category = parts[1] || '';
      }
    }

    if (!aspect || !category) {
      const match = stem.match(/^(\d+x\d+)-([a-z0-9-]+)-\d+$/i);
      if (match) {
        aspect = aspect || match[1];
        category = category || match[2];
      }
    }

    return {
      slug: stem,
      aspectRatio: aspect,
      category,
    };
  };

  const updateSelection = (items) => {
    if (!selection) return;
    if (!items || !items.length) {
      selection.textContent = 'No files selected yet.';
      return;
    }
    const names = Array.from(items).map((item) => item.displayName || item.file?.name || 'unknown').slice(0, 3);
    const suffix = items.length > 3 ? ` …and ${items.length - 3} more` : '';
    const pairedCount = items.filter((item) => item.coordsFile).length;
    const label = pairedCount ? `${items.length} item(s), ${pairedCount} with JSON` : `${items.length} file(s)`;
    selection.textContent = `${label}: ${names.join(', ')}${suffix}`;
  };

  const syncQueuedItemsToSelection = () => {
    updateSelection(queuedItems);
  };

  const buildDirectItems = (files) => Array.from(files || []).map((file) => {
    const inferred = inferMeta(file.name, file.name);
    return {
      file,
      coordsFile: null,
      displayName: file.name,
      inferredSlug: inferred.slug,
      inferredAspectRatio: inferred.aspectRatio,
      inferredCategory: inferred.category,
    };
  });

  const buildDirectoryItems = (files) => {
    const grouped = new Map();
    let rejected = 0;
    for (const file of Array.from(files || [])) {
      const relativePath = String(file.webkitRelativePath || file.name || '').replace(/\\/g, '/');
      const lower = relativePath.toLowerCase();
      const isPng = file && (file.type === 'image/png' || lower.endsWith('.png'));
      const isJson = lower.endsWith('.json') || file.type === 'application/json';
      if (!isPng && !isJson) {
        rejected += 1;
        continue;
      }
      const key = relativePath.replace(/\.(png|json)$/i, '');
      if (!grouped.has(key)) {
        grouped.set(key, { png: null, json: null, relativePath });
      }
      const entry = grouped.get(key);
      if (isPng) {
        entry.png = file;
      } else if (isJson) {
        entry.json = file;
      }
    }

    const items = [];
    for (const [key, entry] of Array.from(grouped.entries()).sort((a, b) => a[0].localeCompare(b[0]))) {
      if (!entry.png) {
        rejected += 1;
        continue;
      }
      if (items.length >= maxFiles) {
        rejected += 1;
        continue;
      }
      const relativePath = String(entry.png.webkitRelativePath || entry.png.name || key).replace(/\\/g, '/');
      const inferred = inferMeta(relativePath, entry.png.name);
      items.push({
        file: entry.png,
        coordsFile: entry.json,
        displayName: relativePath,
        inferredSlug: inferred.slug,
        inferredAspectRatio: inferred.aspectRatio,
        inferredCategory: inferred.category,
      });
    }

    return { items, rejected };
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
    queuedItems = buildDirectItems(fileInput.files);
    syncQueuedItemsToSelection();
    if (constraints) {
      const details = [];
      if (rejected) details.push(`${rejected} file(s) ignored`);
      if (files.length > maxFiles) details.push(`max ${maxFiles} files per batch`);
      constraints.dataset.state = details.length ? 'warning' : '';
    }
  };

  const applyDirectoryFiles = (files) => {
    const { items, rejected } = buildDirectoryItems(files);
    queuedItems = items;
    if (fileInput) {
      fileInput.value = '';
    }
    syncQueuedItemsToSelection();
    if (constraints) {
      const details = [];
      if (rejected) details.push(`${rejected} folder item(s) ignored`);
      constraints.dataset.state = details.length ? 'warning' : '';
    }
  };

  if (!dropzone || !fileInput) return;

  dropzone.addEventListener('click', () => fileInput.click());
  if (directoryTrigger && directoryInput) {
    directoryTrigger.addEventListener('click', (event) => {
      event.preventDefault();
      directoryInput.click();
    });
  }

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

  if (directoryInput) {
    directoryInput.addEventListener('change', (event) => {
      applyDirectoryFiles(event.target.files);
    });
  }

  // Ensure selection text matches any pre-filled FileList
  queuedItems = buildDirectItems(fileInput.files || []);
  syncQueuedItemsToSelection();

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

  const uploadSingle = (uploadItem, fields, item) => new Promise((resolve, reject) => {
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
    fd.append('base_image', uploadItem.file, uploadItem.file.name);
    if (uploadItem.coordsFile) {
      fd.append('coords_json', uploadItem.coordsFile, uploadItem.coordsFile.name);
    }
    xhr.send(fd);
    setItemProgress(item, 0, 'Starting…');
  });

  const setButtonsDisabled = (disabled) => {
    if (submitBtn) submitBtn.disabled = !!disabled;
    if (fileInput) fileInput.disabled = !!disabled;
  };

  const runSequentialUpload = async () => {
    if (!form || !queuedItems.length) return;
    if (submitBtn) submitBtn.hidden = false;
    if (completeBtn) completeBtn.hidden = true;
    clearProgress();
    setButtonsDisabled(true);

    const explicitSlug = form.querySelector('input[name="slug"]')?.value || '';
    const explicitCategory = form.querySelector('select[name="category"]')?.value || '';
    const explicitAspectRatio = form.querySelector('input[name="aspect_ratio"]')?.value || '';
    const csrfToken = form.querySelector('input[name="csrf_token"]')?.value || '';

    for (const uploadItem of queuedItems) {
      const item = makeProgressItem(uploadItem.displayName || uploadItem.file.name);
      const fields = {
        csrf_token: csrfToken,
        slug: queuedItems.length === 1 && explicitSlug ? explicitSlug : (uploadItem.inferredSlug || ''),
        category: explicitCategory || uploadItem.inferredCategory || '',
        aspect_ratio: explicitAspectRatio || uploadItem.inferredAspectRatio || '',
      };
      try {
        setItemProgress(item, 0, uploadItem.coordsFile ? 'Queued with coordinates' : 'Queued');
        await uploadSingle(uploadItem, fields, item);
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
