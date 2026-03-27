(function () {
  'use strict';

  const uploadArea = document.getElementById('uploadArea');
  const fileInput = document.getElementById('fileInput');
  const uploadStatus = document.getElementById('uploadStatus');
  const csrfMeta = document.querySelector('meta[name="csrf-token"]');
  const csrfToken = csrfMeta ? csrfMeta.getAttribute('content') || '' : '';

  if (!uploadArea || !fileInput || !uploadStatus) {
    return;
  }

  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach((eventName) => {
    uploadArea.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ['dragenter', 'dragover'].forEach((eventName) => {
    uploadArea.addEventListener(eventName, () => {
      uploadArea.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach((eventName) => {
    uploadArea.addEventListener(eventName, () => {
      uploadArea.classList.remove('dragover');
    });
  });

  uploadArea.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt ? dt.files : null;
    if (!files || !files.length) return;
    fileInput.files = files;
    handleFileSelect();
  });

  fileInput.addEventListener('change', handleFileSelect);

  function handleFileSelect() {
    const file = fileInput.files && fileInput.files[0];
    if (!file) return;

    if (!file.name.endsWith('.json')) {
      showStatus('Please select a JSON file', 'error');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const result = e.target && typeof e.target.result === 'string' ? e.target.result : '{}';
        const data = JSON.parse(result);
        populatePresetForm(data);
      } catch (err) {
        showStatus('Invalid JSON file: ' + (err && err.message ? err.message : 'parse error'), 'error');
      }
    };
    reader.readAsText(file);
  }

  function populatePresetForm(data) {
    const presetForm = document.getElementById('presetForm');
    if (presetForm) {
      if (data.system_prompt) document.getElementById('system_prompt').value = data.system_prompt;
      if (data.user_full_prompt) document.getElementById('user_full_prompt').value = data.user_full_prompt;
      if (data.user_section_prompt) document.getElementById('user_section_prompt').value = data.user_section_prompt;
      if (data.listing_boilerplate) document.getElementById('listing_boilerplate').value = data.listing_boilerplate;
      if (data.analysis_prompt) document.getElementById('analysis_prompt').value = data.analysis_prompt;
      showStatus('Preset fields populated! Review and save.', 'success');
      return;
    }
    showPresetImportModal(data);
  }

  function showPresetImportModal(data) {
    const html = `
      <div class="import-modal-overlay" id="importModal">
        <div class="import-modal-content">
          <h2>Import Preset</h2>
          <div class="import-modal-form-group">
            <label>Provider:</label>
            <select id="importProvider">
              <option value="openai">OpenAI</option>
              <option value="gemini">Gemini</option>
            </select>
          </div>
          <div class="import-modal-form-group">
            <label>Preset Name:</label>
            <input type="text" id="importName" placeholder="e.g., Test v1.0">
          </div>
          <div class="import-modal-buttons">
            <button class="import-modal-btn-cancel modal-cancel-btn">Cancel</button>
            <button class="import-modal-btn-import modal-import-btn" data-import-data='${JSON.stringify(data)}'>Import & Edit</button>
          </div>
        </div>
      </div>
    `;

    uploadStatus.innerHTML = html;

    setTimeout(() => {
      const cancelBtn = document.querySelector('.modal-cancel-btn');
      const importBtn = document.querySelector('.modal-import-btn');

      if (cancelBtn) {
        cancelBtn.addEventListener('click', (e) => {
          e.preventDefault();
          const modal = document.getElementById('importModal');
          if (modal) modal.remove();
          fileInput.value = '';
        });
      }

      if (importBtn) {
        importBtn.addEventListener('click', (e) => {
          e.preventDefault();
          const importData = importBtn.dataset.importData || '{}';
          saveImportedPreset(importData);
          const modal = document.getElementById('importModal');
          if (modal) modal.remove();
        });
      }
    }, 0);
  }

  function saveImportedPreset(dataStr) {
    const providerEl = document.getElementById('importProvider');
    const nameEl = document.getElementById('importName');
    const provider = providerEl ? providerEl.value : 'openai';
    const name = nameEl ? nameEl.value.trim() : '';

    if (!name) {
      alert('Please enter a preset name');
      return;
    }

    window.location.href = `/admin/analysis-management/edit/${provider}/0?imported_data=${encodeURIComponent(dataStr)}&name=${encodeURIComponent(name)}`;
  }

  function showStatus(message, type) {
    uploadStatus.innerHTML = `<div class="status-message status-${type}">${message}</div>`;
    if (type === 'success') {
      setTimeout(() => {
        uploadStatus.innerHTML = '';
      }, 5000);
    }
  }

  function deletePreset(presetId, presetName) {
    if (!confirm(`Delete preset "${presetName}"? This cannot be undone.`)) {
      return;
    }

    fetch(`/admin/analysis-management/delete/${presetId}`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json',
      },
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.status === 'ok') {
          location.reload();
        } else {
          alert('Error: ' + (data.message || 'Unknown error'));
        }
      })
      .catch((err) => alert('Error: ' + err.message));
  }

  function exportPreset(presetId) {
    fetch(`/admin/analysis-management/export/${presetId}`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    })
      .then((r) => {
        if (!r.ok) throw new Error('Export failed');
        return r.json();
      })
      .then((data) => {
        if (data.status === 'ok') {
          const filename = `preset-${data.preset.provider}-${data.preset.id}.json`;
          const json = JSON.stringify(data.preset, null, 2);
          const blob = new Blob([json], { type: 'application/json' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = filename;
          document.body.appendChild(a);
          a.click();
          URL.revokeObjectURL(url);
          document.body.removeChild(a);
        } else {
          alert('Error: ' + (data.message || 'Unknown error'));
        }
      })
      .catch((err) => alert('Export error: ' + err.message));
  }

  document.querySelectorAll('.delete-preset-btn').forEach((btn) => {
    btn.addEventListener('click', function () {
      deletePreset(this.dataset.presetId, this.dataset.presetName);
    });
  });

  document.querySelectorAll('.export-preset-btn').forEach((btn) => {
    btn.addEventListener('click', function () {
      exportPreset(this.dataset.presetId);
    });
  });

  document.addEventListener('DOMContentLoaded', () => {
    const fileSelectBtn = document.querySelector('.file-select-btn');
    if (fileSelectBtn) {
      fileSelectBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const input = document.getElementById('fileInput');
        if (input) input.click();
      });
    }

    document.querySelectorAll('.edit-preset-btn').forEach((btn) => {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        window.location.href = this.dataset.href;
      });
    });
  });
})();
