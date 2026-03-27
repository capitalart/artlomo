(function () {
  'use strict';

  var generatorCarouselItems = [];
  var generatorCarouselIndex = 0;
  var deleteModalState = {
    jobIds: [],
    mode: 'single',
    label: ''
  };
  var _refreshIntervalId = null;
  var _activeJobStartedAt = null; // ISO string from last poll
  var _activeJobTimerInterval = null;

  function parseIntSafe(value, fallback) {
    var parsed = Number.parseInt(String(value || ''), 10);
    return Number.isNaN(parsed) ? fallback : parsed;
  }

  function updateProgressBar(fillEl, percentage) {
    if (!fillEl) {
      return;
    }
    var pct = Math.max(0, Math.min(100, parseIntSafe(percentage, 0)));
    fillEl.style.width = String(pct) + '%';
    fillEl.textContent = pct > 5 ? String(pct) + '%' : '';
  }

  function updateStateBadge(state) {
    var badge = document.getElementById('pipeline-state-badge');
    if (!badge) {
      return;
    }
    var nextState = (state || 'running').toLowerCase();
    badge.className = 'pipeline-state-badge state-' + nextState;
    badge.textContent = nextState.toUpperCase();
  }

  function updateCoordinateDetectionUI(skipDetection) {
    var badge = document.getElementById('coordinate-detection-badge');
    var button = document.getElementById('toggle-coordinate-detection-button');
    var skip = Boolean(skipDetection);
    if (badge) {
      badge.dataset.skipCoordinateDetection = skip ? 'true' : 'false';
      badge.className = 'pipeline-state-badge ' + (skip ? 'state-stopped' : 'state-running');
      badge.textContent = skip ? 'DISABLED (FALLBACK)' : 'ENABLED';
    }
    if (button) {
      button.textContent = skip ? 'Enable Coordinate Detection' : 'Disable Coordinate Detection';
    }
  }

  function showStatusMessage(message, tone) {
    var banner = document.getElementById('dashboard-status-banner');
    if (!banner) {
      return;
    }

    var nextTone = tone || 'info';
    banner.className = 'dashboard-status-banner is-' + nextTone;
    banner.textContent = String(message || '');
    banner.hidden = !message;
  }

  function updateLastRefreshed() {
    var line = document.getElementById('refresh-status-line');
    if (!line) {
      return;
    }
    var now = new Date();
    var hms = now.toLocaleTimeString('en-AU', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
    line.textContent = 'Last updated: ' + hms;
  }

  function startActiveJobTimer(startedAtIso, updatedAtIso) {
    if (_activeJobTimerInterval) {
      clearInterval(_activeJobTimerInterval);
      _activeJobTimerInterval = null;
    }
    var timerEl = document.getElementById('active-job-timer');
    if (!timerEl) {
      return;
    }
    var ref = startedAtIso || updatedAtIso;
    if (!ref) {
      return;
    }
    // Ensure UTC interpretation.
    if (!/[zZ]|[+-]\d\d:?\d\d$/.test(ref)) {
      ref = ref + 'Z';
    }
    var startMs = new Date(ref).getTime();
    if (Number.isNaN(startMs)) {
      return;
    }
    function tick() {
      var elapsed = Math.max(0, Math.floor((Date.now() - startMs) / 1000));
      var mins = Math.floor(elapsed / 60);
      var secs = elapsed % 60;
      timerEl.textContent = mins > 0
        ? String(mins) + 'm ' + String(secs) + 's'
        : String(elapsed) + 's';
    }
    tick();
    _activeJobTimerInterval = setInterval(tick, 1000);
  }

  function stopActiveJobTimer() {
    if (_activeJobTimerInterval) {
      clearInterval(_activeJobTimerInterval);
      _activeJobTimerInterval = null;
    }
  }

  function renderActiveJob(activeJob) {
    var panel = document.getElementById('active-job-panel');
    if (!panel) {
      return;
    }

    if (!activeJob) {
      stopActiveJobTimer();
      panel.innerHTML = '<div class="active-job-idle" id="active-job-idle">No job is actively running right now. Worker may be between jobs, paused, or waiting on a rate-limit retry delay.</div>';
      panel.removeAttribute('data-started-at');
      panel.removeAttribute('data-updated-at');
      return;
    }

    var scope = escapeHtml(activeJob.aspect_ratio) + ' &middot; ' + escapeHtml(activeJob.category) + ' &middot; v' + escapeHtml(activeJob.variation_index);
    var stageName = escapeHtml(activeJob.stage || activeJob.status);
    var attempts = parseIntSafe(activeJob.attempts, 0);

    panel.innerHTML =
      '<div class="active-job-header">' +
        '<span class="active-job-pulse"></span>' +
        '<strong>Currently running:</strong> ' + scope +
      '</div>' +
      '<div class="active-job-meta">' +
        '<span>Stage: <strong>' + stageName + '</strong></span>' +
        ' &nbsp;&middot;&nbsp; ' +
        '<span>Attempts: <strong>' + String(attempts) + '</strong></span>' +
        ' &nbsp;&middot;&nbsp; ' +
        '<span>Running: <strong id="active-job-timer">...</strong></span>' +
      '</div>' +
      ((activeJob.placeholder_mode || activeJob.guide_path)
        ? '<div class="active-job-meta">' +
            '<span>Placeholder Mode: <strong>' + escapeHtml(activeJob.placeholder_mode || '—') + '</strong></span>' +
            ' &nbsp;&middot;&nbsp; ' +
            '<span title="' + escapeHtml(activeJob.guide_path || '') + '">Guide: <strong>' + escapeHtml(activeJob.guide_path || '—') + '</strong></span>' +
          '</div>'
        : '');

    panel.dataset.startedAt = activeJob.started_at || '';
    panel.dataset.updatedAt = activeJob.updated_at || '';
    startActiveJobTimer(activeJob.started_at, activeJob.updated_at);
  }

  function renderNextPending(nextPending, retryQueuedJobs) {
    var wrap = document.getElementById('next-pending-wrap');
    var empty = document.getElementById('next-pending-empty');
    var tbody = document.getElementById('next-pending-body');
    var badge = document.getElementById('next-pending-badge');

    var pending = Array.isArray(nextPending) ? nextPending : [];
    var retrying = Array.isArray(retryQueuedJobs) ? retryQueuedJobs : [];
    var total = pending.length + retrying.length;

    if (badge) {
      badge.textContent = String(total);
    }

    if (!total) {
      if (wrap) { wrap.hidden = true; }
      if (empty) { empty.hidden = false; }
      return;
    }

    if (wrap) { wrap.hidden = false; }
    if (empty) { empty.hidden = true; }

    if (!tbody) {
      return;
    }

    var rows = pending.map(function (job) {
      return '<tr>' +
        '<td>' + escapeHtml(job.aspect_ratio) + ' &middot; ' + escapeHtml(job.category) + ' &middot; v' + escapeHtml(job.variation_index) + '</td>' +
        '<td><span class="badge badge-queued">Queued</span></td>' +
        '<td>' + escapeHtml(job.attempts || 0) + '</td>' +
        '<td></td>' +
        '</tr>';
    });

    rows = rows.concat(retrying.map(function (job) {
      return '<tr class="retry-queued-row">' +
        '<td>' + escapeHtml(job.aspect_ratio) + ' &middot; ' + escapeHtml(job.category) + ' &middot; v' + escapeHtml(job.variation_index) + '</td>' +
        '<td><span class="badge badge-retryqueued">Retry Queued</span></td>' +
        '<td>' + escapeHtml(job.attempts || 0) + '</td>' +
        '<td><button class="gallery-btn gallery-btn--compact force-retry-btn" type="button" data-force-retry-job-id="' + escapeHtml(job.id) + '">Retry Now</button></td>' +
        '</tr>';
    }));

    tbody.innerHTML = rows.join('');
  }

  function setAdaptiveInterval(hasActivity) {
    var targetMs = hasActivity ? 10000 : 30000;
    if (_refreshIntervalId) {
      clearInterval(_refreshIntervalId);
    }
    _refreshIntervalId = setInterval(refreshStatus, targetMs);
  }

  function forceRetryJob(jobId, button) {
    var root = document.getElementById('mockup-dashboard-root');
    if (!root) {
      return;
    }
    var baseUrl = root.dataset.forceRetryBaseUrl || '';
    if (!baseUrl) {
      showStatusMessage('Missing force-retry endpoint configuration.', 'error');
      return;
    }
    var url = baseUrl.replace('{id}', String(jobId));

    if (button) {
      button.disabled = true;
      button.textContent = 'Retrying…';
    }

    window.fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' } })
      .then(function (response) {
        return response.json().then(function (data) { return { ok: response.ok, data: data }; });
      })
      .then(function (result) {
        if (!result.ok || result.data.error) {
          throw new Error(result.data.error || 'Force retry failed');
        }
        showStatusMessage('Job dispatched immediately.', 'success');
        window.setTimeout(refreshStatus, 1200);
      })
      .catch(function (error) {
        showStatusMessage('Error: ' + error.message, 'error');
        if (button) {
          button.disabled = false;
          button.textContent = 'Retry Now';
        }
      });
  }

  function collectScopePayload() {
    var modeEl = document.getElementById('generation-mode');
    var aspectEl = document.getElementById('generation-aspect');
    var categoryEl = document.getElementById('generation-category');
    var quantityEl = document.getElementById('generation-quantity');
    var retryEl = document.getElementById('retry-failed-toggle');
    var inlineSingleEl = document.getElementById('inline-single-toggle');
    var maxRetriesEl = document.getElementById('max-retries-select');
    var placeholderModeEl = document.getElementById('placeholder-mode-select');
    var customPromptEl = document.getElementById('custom-prompt-text');
    var rawPromptOnlyEl = document.getElementById('raw-prompt-only-toggle');
    var rawPromptTextEl = document.getElementById('raw-prompt-text');

    return {
      mode: modeEl ? modeEl.value : 'full_batch',
      aspect_ratio: aspectEl ? aspectEl.value : '',
      category: categoryEl ? categoryEl.value : '',
      quantity: quantityEl ? parseIntSafe(quantityEl.value, 20) : 20,
      retry_failed: Boolean(retryEl && retryEl.checked),
      run_inline_single: Boolean(inlineSingleEl && inlineSingleEl.checked),
      max_retries: maxRetriesEl ? parseIntSafe(maxRetriesEl.value, 3) : 3,
      placeholder_mode: placeholderModeEl ? placeholderModeEl.value : 'artwork_trojan',
      custom_prompt_text: customPromptEl ? String(customPromptEl.value || '').trim() : '',
      raw_prompt_only_enabled: Boolean(rawPromptOnlyEl && rawPromptOnlyEl.checked),
      raw_prompt_text: rawPromptTextEl ? String(rawPromptTextEl.value || '') : ''
    };
  }

  function buildAutoPromptText() {
    var aspectEl = document.getElementById('generation-aspect');
    var categoryEl = document.getElementById('generation-category');
    var workflowEl = document.getElementById('placeholder-mode-select');

    var aspect = aspectEl && aspectEl.value ? aspectEl.value : '{{aspect_ratio}}';
    var category = categoryEl && categoryEl.value ? categoryEl.value : '{{category}}';
    var workflow = workflowEl && workflowEl.value ? workflowEl.value : 'artwork_only_composite';
    var variation = '{{variation_index}}';

    if (workflow === 'artwork_trojan') {
      return [
        'Create one photorealistic square (1:1) interior mockup for a ' + category + '.',
        'Use the supplied artwork reference exactly as provided.',
        'Keep the artwork fully visible, unobstructed, and centered on the wall.',
        'Preserve the artwork geometry exactly at aspect ratio ' + aspect + ' (width:height).',
        'Do not crop, warp, repaint, replace, stylize, or add overlays/watermarks.',
        'Use a direct frontal camera angle with minimal perspective distortion.',
        'Produce one distinct composition for variation ' + variation + '.'
      ].join(' ');
    }

    if (workflow === 'chromakey_auto') {
      return [
        'Create one photorealistic square (1:1) interior mockup for a ' + category + '.',
        'Render a clean rectangular artwork area filled with solid #00FFCC chromakey color.',
        'Keep the chromakey rectangle unobstructed and fully visible with natural perspective.',
        'Preserve the visible artwork area exact aspect ratio ' + aspect + ' (width:height).',
        'Do not add texture, gradients, text, logos, watermark, or frame overlap on the chromakey region.',
        'Generate one distinct composition for variation ' + variation + '.'
      ].join(' ');
    }

    return [
      'Create one photorealistic square (1:1) interior mockup for a ' + category + '.',
      'Use the supplied artwork image as the wall artwork.',
      'Keep the visible artwork area exact aspect ratio ' + aspect + ' (width:height).',
      'Keep the artwork fully visible and unobstructed with a direct frontal view.',
      'Do not crop, warp, repaint, replace, stylize, or add text/watermarks.',
      'Generate one distinct composition for variation ' + variation + '.'
    ].join(' ');
  }

  function estimateScopeCount(payload) {
    var aspectEl = document.getElementById('generation-aspect');
    var categoryEl = document.getElementById('generation-category');
    var totalAspects = aspectEl ? Math.max(1, aspectEl.options.length - 1) : 13;
    var totalCategories = categoryEl ? Math.max(1, categoryEl.options.length - 1) : 23;
    var totalVariations = parseIntSafe(payload.quantity, 20);

    if (payload.mode === 'aspect_only') {
      return 1 * totalCategories * totalVariations;
    }
    if (payload.mode === 'category_only') {
      return totalAspects * 1 * totalVariations;
    }
    if (payload.mode === 'aspect_and_category') {
      return 1 * 1 * totalVariations;
    }
    return totalAspects * totalCategories * totalVariations;
  }

  function setButtonsDisabled(disabled) {
    ['start-pipeline-button', 'clear-pending-button', 'clear-failed-button', 'toggle-coordinate-detection-button', 'pause-pipeline-button', 'resume-pipeline-button', 'stop-pipeline-button', 'select-all-previews-button', 'clear-selection-previews-button', 'delete-selected-previews-button']
      .forEach(function (id) {
        var el = document.getElementById(id);
        if (el) {
          el.disabled = disabled;
        }
      });
  }

  function startGenerationPipeline(button) {
    var root = document.getElementById('mockup-dashboard-root');
    if (!root || !button) {
      return;
    }

    var startUrl = root.dataset.startUrl || '';
    if (!startUrl) {
      showStatusMessage('Missing queue endpoint configuration.', 'error');
      return;
    }

    var payload = collectScopePayload();
    var est = estimateScopeCount(payload);

    setButtonsDisabled(true);
    button.textContent = 'Queueing...';
    showStatusMessage(
      'Queueing ' + String(est) + ' combination(s) for ' + payload.mode.replace(/_/g, ' ') + '...',
      'info'
    );

    window.fetch(startUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
      .then(function (response) {
        return response.json().then(function (data) {
          return { ok: response.ok, data: data };
        });
      })
      .then(function (result) {
        if (!result.ok || result.data.error) {
          throw new Error(result.data.error || 'Queue request failed');
        }

        var summary = 'Queued scope successfully. ' +
          'Quantity: ' + String(result.data.quantity || payload.quantity || 0) + '. ' +
          'Created: ' + String(result.data.created || 0) + '. ' +
          'Retried: ' + String(result.data.retried || 0) + '. ' +
          'Scope total: ' + String(result.data.scope_total || 0) + '.';
        if (result.data.run_inline_single) {
          var inlineStatus = result.data.inline_result && result.data.inline_result.status
            ? String(result.data.inline_result.status)
            : 'completed';
          summary += ' Inline mode: ' + inlineStatus + '.';
        }
        showStatusMessage(summary, 'success');
        window.setTimeout(function () {
          window.location.reload();
        }, 800);
      })
      .catch(function (error) {
        showStatusMessage('Error: ' + error.message, 'error');
      })
      .finally(function () {
        setButtonsDisabled(false);
        button.textContent = 'Start Queue';
      });
  }

  function previewRenderedPrompt(button) {
    var root = document.getElementById('mockup-dashboard-root');
    var outputEl = document.getElementById('rendered-prompt-preview-output');
    if (!root || !outputEl) {
      return;
    }

    var previewUrl = root.dataset.promptPreviewUrl || '';
    if (!previewUrl) {
      showStatusMessage('Missing prompt preview endpoint configuration.', 'error');
      return;
    }

    var payload = collectScopePayload();
    payload.variation_index = 1;

    if (button) {
      button.disabled = true;
      button.textContent = 'Rendering...';
    }

    showStatusMessage('Rendering prompt preview for current scope...', 'info');

    window.fetch(previewUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
      .then(function (response) {
        return response.json().then(function (data) {
          return { ok: response.ok, data: data };
        });
      })
      .then(function (result) {
        if (!result.ok || result.data.error) {
          throw new Error(result.data.error || 'Prompt preview failed');
        }
        var promptText = String(result.data.prompt_text || '');
        var guideNote = String(result.data.guide_note || '');
        outputEl.value = promptText + (guideNote ? ('\n\n---\n' + guideNote) : '');
        showStatusMessage('Prompt preview rendered.', 'success');
      })
      .catch(function (error) {
        showStatusMessage('Error: ' + error.message, 'error');
      })
      .finally(function () {
        if (button) {
          button.disabled = false;
          button.textContent = 'Preview Rendered Prompt';
        }
      });
  }

  function sendControlAction(action, button, extraPayload) {
    var root = document.getElementById('mockup-dashboard-root');
    if (!root) {
      return;
    }

    var controlUrl = root.dataset.controlUrl || '';
    if (!controlUrl) {
      showStatusMessage('Missing control endpoint configuration.', 'error');
      return;
    }

    setButtonsDisabled(true);
    showStatusMessage('Applying pipeline action: ' + action + '...', 'info');

    var payload = { action: action };
    if (extraPayload && typeof extraPayload === 'object') {
      Object.keys(extraPayload).forEach(function (key) {
        payload[key] = extraPayload[key];
      });
    }

    window.fetch(controlUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
      .then(function (response) {
        return response.json().then(function (data) {
          return { ok: response.ok, data: data };
        });
      })
      .then(function (result) {
        if (!result.ok || result.data.error) {
          throw new Error(result.data.error || 'Control action failed');
        }
        var state = result.data.control_state && result.data.control_state.state;
        updateStateBadge(state || 'running');
        var skip = result.data.control_state && String(result.data.control_state.skip_coordinate_detection || 'false').toLowerCase() === 'true';
        updateCoordinateDetectionUI(skip);
        if (action === 'set_skip_coordinate_detection') {
          showStatusMessage(skip ? 'Coordinate detection disabled. Jobs will use fallback coordinates if extraction fails.' : 'Coordinate detection enabled.', 'success');
        } else {
          showStatusMessage('Pipeline state updated to ' + String(state || 'running').toUpperCase() + '.', 'success');
        }
      })
      .catch(function (error) {
        showStatusMessage('Error: ' + error.message, 'error');
      })
      .finally(function () {
        setButtonsDisabled(false);
        if (button) {
          button.blur();
        }
      });
  }

  function escapeHtml(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function formatTimestamp(value, preformatted) {
    if (preformatted) {
      return String(preformatted);
    }

    if (!value) {
      return '—';
    }

    var raw = String(value);
    var withTimezone = /[zZ]|[+-]\d\d:?\d\d$/.test(raw) ? raw : raw + 'Z';
    var parsed = new Date(withTimezone);
    if (Number.isNaN(parsed.getTime())) {
      return raw.slice(0, 19).replace('T', ' ');
    }

    return new Intl.DateTimeFormat('en-AU', {
      timeZone: 'Australia/Adelaide',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    }).format(parsed).replace(',', '');
  }

  function renderRecentFailures(items) {
    var tbody = document.getElementById('recent-failures-body');
    var emptyState = document.getElementById('recent-failures-empty');
    var tableWrap = document.getElementById('recent-failures-table-wrap');

    if (!tbody) {
      return;
    }

    var failures = Array.isArray(items) ? items : [];
    if (!failures.length) {
      tbody.innerHTML = '';
      if (emptyState) {
        emptyState.hidden = false;
      }
      if (tableWrap) {
        tableWrap.hidden = true;
      }
      return;
    }

    tbody.innerHTML = failures.map(function (job) {
      return '' +
        '<tr>' +
        '<td><div class="failure-job-id">' + escapeHtml(job.job_id) + '</div><div class="failure-meta">Attempt ' + escapeHtml(job.attempts || 0) + '</div></td>' +
        '<td>' + escapeHtml(job.aspect_ratio) + ' · ' + escapeHtml(job.category) + ' · v' + escapeHtml(job.variation_index) + '</td>' +
        '<td>' + escapeHtml(job.stage || 'Failed') + '</td>' +
        '<td>' + escapeHtml(job.reason || '—') + '</td>' +
        '<td class="failure-message-cell" title="' + escapeHtml(job.error_message || '') + '">' +
          '<div>' + escapeHtml(job.error_message || '—') + '</div>' +
          ((job.placeholder_mode || job.guide_path)
            ? '<div class="failure-meta">' + escapeHtml(job.placeholder_mode || '—') + ((job.guide_path) ? ' · ' + escapeHtml(job.guide_path) : '') + '</div>'
            : '') +
        '</td>' +
        '<td>' + escapeHtml(formatTimestamp(job.updated_at, job.updated_at_adelaide)) + '</td>' +
        '</tr>';
    }).join('');

    if (emptyState) {
      emptyState.hidden = true;
    }
    if (tableWrap) {
      tableWrap.hidden = false;
    }
  }

  function renderRecentCompleted(items) {
    var grid = document.getElementById('recent-completed-grid');
    var emptyState = document.getElementById('recent-completed-empty');
    var controls = document.getElementById('completed-preview-controls');

    if (!grid) {
      return;
    }

    var completed = Array.isArray(items) ? items.filter(function (job) {
      return Boolean(job && job.image_preview_url);
    }) : [];

    if (!completed.length) {
      grid.innerHTML = '';
      grid.hidden = true;
      if (controls) {
        controls.hidden = true;
      }
      if (emptyState) {
        emptyState.hidden = false;
      }
      return;
    }

    grid.innerHTML = completed.map(function (job) {
      return '' +
        '<article class="completed-preview-card" data-completed-job-id="' + escapeHtml(job.id) + '" data-completed-job-name="' + escapeHtml(job.job_id || '') + '">' +
        '<div class="completed-preview-card-actions">' +
        '<label class="completed-preview-select">' +
        '<input type="checkbox" class="completed-preview-checkbox" data-select-completed-job-id="' + escapeHtml(job.id) + '">' +
        '<span>Select</span>' +
        '</label>' +
        '<button class="gallery-btn gallery-btn--outline completed-preview-delete-btn" type="button" data-delete-completed-job-id="' + escapeHtml(job.id) + '" data-delete-completed-job-name="' + escapeHtml(job.job_id || '') + '">Delete</button>' +
        '</div>' +
        '<div class="completed-preview-image-wrap">' +
        '<img class="completed-preview-image" src="' + escapeHtml(job.image_preview_url) + '" alt="' + escapeHtml(job.job_id) + ' preview" loading="lazy" data-generator-carousel-trigger data-generator-preview-url="' + escapeHtml(job.image_preview_url) + '" data-generator-preview-name="' + escapeHtml(job.job_id) + '">' +
        '</div>' +
        '<div class="completed-preview-meta">' +
        '<div class="completed-preview-job">' + escapeHtml(job.job_id) + '</div>' +
        '<div class="completed-preview-scope">' + escapeHtml(job.aspect_ratio) + ' · ' + escapeHtml(job.category) + ' · v' + escapeHtml(job.variation_index) + '</div>' +
        ((job.placeholder_mode || job.guide_path)
          ? '<div class="completed-preview-scope">' + escapeHtml(job.placeholder_mode || '—') + ((job.guide_path) ? ' · ' + escapeHtml(job.guide_path) : '') + '</div>'
          : '') +
        '<div class="completed-preview-time">' + escapeHtml(formatTimestamp(job.updated_at, job.updated_at_adelaide)) + '</div>' +
        '</div>' +
        '</article>';
    }).join('');

    grid.hidden = false;
    if (controls) {
      controls.hidden = false;
    }
    if (emptyState) {
      emptyState.hidden = true;
    }

    rebuildGeneratorCarouselItems();
    updateCompletedPreviewSelectionState();
  }

  function renderRecentAttemptLogs(items) {
    var tbody = document.getElementById('recent-attempt-log-body');
    var emptyState = document.getElementById('recent-attempt-log-empty');
    var tableWrap = document.getElementById('recent-attempt-log-table-wrap');

    if (!tbody) {
      return;
    }

    var attempts = Array.isArray(items) ? items : [];
    if (!attempts.length) {
      tbody.innerHTML = '';
      if (emptyState) {
        emptyState.hidden = false;
      }
      if (tableWrap) {
        tableWrap.hidden = true;
      }
      return;
    }

    tbody.innerHTML = attempts.map(function (job) {
      var promptText = String(job.submitted_prompt_text || '—');
      return '' +
        '<tr>' +
        '<td><span class="badge badge-' + escapeHtml(String(job.status || '').toLowerCase()) + '">' + escapeHtml(job.status || '—') + '</span><div class="failure-meta">Attempt ' + escapeHtml(job.attempts || 0) + '</div></td>' +
        '<td>' + escapeHtml(job.aspect_ratio) + ' · ' + escapeHtml(job.category) + ' · v' + escapeHtml(job.variation_index) + '</td>' +
        '<td class="failure-message-cell" title="' + escapeHtml(job.submitted_guide_image || '') + '"><div>' + escapeHtml(job.submitted_guide_image || '—') + '</div></td>' +
        '<td class="failure-message-cell" title="' + escapeHtml(promptText) + '">' +
          '<details>' +
            '<summary>View prompt text</summary>' +
            '<pre style="white-space:pre-wrap;max-width:560px;">' + escapeHtml(promptText) + '</pre>' +
          '</details>' +
        '</td>' +
        '<td>' + escapeHtml(formatTimestamp(job.updated_at, job.updated_at_adelaide)) + '</td>' +
        '</tr>';
    }).join('');

    if (emptyState) {
      emptyState.hidden = true;
    }
    if (tableWrap) {
      tableWrap.hidden = false;
    }
  }

  function getCompletedPreviewCheckboxes() {
    return Array.prototype.slice.call(document.querySelectorAll('.completed-preview-checkbox'));
  }

  function getSelectedCompletedJobIds() {
    return getCompletedPreviewCheckboxes()
      .filter(function (node) { return Boolean(node && node.checked); })
      .map(function (node) { return parseIntSafe(node.getAttribute('data-select-completed-job-id'), 0); })
      .filter(function (id) { return id > 0; });
  }

  function updateCompletedPreviewSelectionState() {
    var boxes = getCompletedPreviewCheckboxes();
    var selected = getSelectedCompletedJobIds();
    var selectedBadge = document.getElementById('selected-previews-count-badge');

    var deleteSelectedBtn = document.getElementById('delete-selected-previews-button');
    if (deleteSelectedBtn) {
      deleteSelectedBtn.disabled = !selected.length;
      deleteSelectedBtn.textContent = selected.length > 0
        ? 'Delete Selected (' + String(selected.length) + ')'
        : 'Delete Selected';
    }

    var approveSelectedBtn = document.getElementById('approve-selected-previews-button');
    if (approveSelectedBtn) {
      approveSelectedBtn.disabled = !selected.length;
      approveSelectedBtn.textContent = selected.length > 0
        ? 'Approve Selected (' + String(selected.length) + ')'
        : 'Approve Selected';
    }

    if (selectedBadge) {
      selectedBadge.textContent = String(selected.length) + ' selected';
    }

    var selectAllBtn = document.getElementById('select-all-previews-button');
    if (selectAllBtn) {
      var allChecked = boxes.length > 0 && selected.length === boxes.length;
      selectAllBtn.textContent = allChecked ? 'Unselect All' : 'Select All';
    }
  }

  function setAllPreviewSelections(checked) {
    getCompletedPreviewCheckboxes().forEach(function (node) {
      node.checked = Boolean(checked);
    });
    updateCompletedPreviewSelectionState();
  }

  function getDeleteModal() {
    return document.querySelector('[data-delete-modal]');
  }

  function closeDeleteConfirmModal() {
    var modal = getDeleteModal();
    if (!modal) {
      return;
    }
    modal.dataset.open = 'false';
    modal.dataset.visible = '';
  }

  function openDeleteConfirmModal(payload) {
    var modal = getDeleteModal();
    if (!modal) {
      return;
    }

    deleteModalState.jobIds = Array.isArray(payload.jobIds) ? payload.jobIds.slice() : [];
    deleteModalState.mode = payload.mode || 'single';
    deleteModalState.label = payload.label || '';

    var msg = modal.querySelector('[data-delete-modal-message]');
    if (msg) {
      if (deleteModalState.mode === 'single') {
        msg.textContent = 'Delete preview "' + (deleteModalState.label || 'selected item') + '"?';
      } else {
        msg.textContent = 'Delete ' + String(deleteModalState.jobIds.length) + ' selected preview(s)?';
      }
    }

    var title = modal.querySelector('[data-delete-modal-title]');
    if (title) {
      title.textContent = 'Confirm Delete';
    }

    modal.dataset.open = 'true';
    modal.dataset.visible = '1';
  }

  function deleteCompletedJobs(jobIds, triggerButton) {
    var root = document.getElementById('mockup-dashboard-root');
    if (!root) {
      return;
    }

    var url = root.dataset.deleteCompletedUrl || '';
    if (!url) {
      showStatusMessage('Missing delete-completed endpoint configuration.', 'error');
      return;
    }

    var ids = Array.isArray(jobIds) ? jobIds.filter(function (id) { return parseIntSafe(id, 0) > 0; }) : [];
    if (!ids.length) {
      showStatusMessage('No completed previews were selected for deletion.', 'info');
      return;
    }

    if (triggerButton) {
      triggerButton.disabled = true;
    }
    setButtonsDisabled(true);
    showStatusMessage('Deleting ' + String(ids.length) + ' completed preview(s)...', 'info');

    window.fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ job_ids: ids })
    })
      .then(function (response) {
        return response.json().then(function (data) {
          return { ok: response.ok, data: data };
        });
      })
      .then(function (result) {
        if (!result.ok || result.data.error) {
          throw new Error(result.data.error || 'Delete completed request failed');
        }

        showStatusMessage('Deleted ' + String(result.data.cleared || 0) + ' completed preview(s).', 'success');
        closeDeleteConfirmModal();
        refreshStatus();
      })
      .catch(function (error) {
        showStatusMessage('Error: ' + error.message, 'error');
      })
      .finally(function () {
        if (triggerButton) {
          triggerButton.disabled = false;
        }
        setButtonsDisabled(false);
        updateCompletedPreviewSelectionState();
      });
  }

  function approveCompletedJobs(jobIds, triggerButton) {
    var root = document.getElementById('mockup-dashboard-root');
    if (!root) {
      return;
    }

    var url = root.dataset.approveCompletedUrl || '';
    if (!url) {
      showStatusMessage('Missing approve-completed endpoint configuration.', 'error');
      return;
    }

    var ids = Array.isArray(jobIds) ? jobIds.filter(function (id) { return parseIntSafe(id, 0) > 0; }) : [];
    if (!ids.length) {
      showStatusMessage('No completed previews were selected for approval.', 'info');
      return;
    }

    if (triggerButton) {
      triggerButton.disabled = true;
    }
    setButtonsDisabled(true);
    showStatusMessage('Approving ' + String(ids.length) + ' completed preview(s) to Live...', 'info');

    window.fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ job_ids: ids })
    })
      .then(function (response) {
        return response.json().then(function (data) {
          return { ok: response.ok, data: data };
        });
      })
      .then(function (result) {
        if (!result.ok || result.data.error) {
          throw new Error(result.data.error || 'Approve completed request failed');
        }

        var summary = 'Approved ' + String(result.data.approved || 0) + ' preview(s) to Live.';
        if (parseIntSafe(result.data.skipped, 0) > 0) {
          summary += ' Skipped: ' + String(result.data.skipped) + '.';
        }
        showStatusMessage(summary, 'success');
        refreshStatus();
      })
      .catch(function (error) {
        showStatusMessage('Error: ' + error.message, 'error');
      })
      .finally(function () {
        if (triggerButton) {
          triggerButton.disabled = false;
        }
        setButtonsDisabled(false);
        updateCompletedPreviewSelectionState();
      });
  }

  function wireDeleteConfirmModal() {
    var modal = getDeleteModal();
    if (!modal) {
      return;
    }

    Array.prototype.slice.call(modal.querySelectorAll('[data-delete-modal-cancel]')).forEach(function (btn) {
      btn.addEventListener('click', function () {
        closeDeleteConfirmModal();
      });
    });

    var confirmBtn = modal.querySelector('[data-delete-modal-confirm]');
    if (confirmBtn) {
      confirmBtn.addEventListener('click', function () {
        deleteCompletedJobs(deleteModalState.jobIds, confirmBtn);
      });
    }

    modal.addEventListener('click', function (evt) {
      if (evt.target === modal) {
        closeDeleteConfirmModal();
      }
    });

    document.addEventListener('keydown', function (evt) {
      if (!modal.dataset.visible) {
        return;
      }
      if (evt.key === 'Escape') {
        closeDeleteConfirmModal();
      }
    });
  }

  function rebuildGeneratorCarouselItems() {
    generatorCarouselItems = Array.prototype.slice.call(
      document.querySelectorAll('[data-generator-carousel-trigger]')
    ).map(function (node) {
      return {
        full: node.getAttribute('data-generator-preview-url') || '',
        name: node.getAttribute('data-generator-preview-name') || 'Generated preview'
      };
    }).filter(function (item) {
      return Boolean(item.full);
    });
  }

  function renderGeneratorCarousel(modal) {
    if (!modal || !generatorCarouselItems.length) {
      return;
    }

    var imageNode = modal.querySelector('[data-carousel-image]');
    var titleNode = modal.querySelector('[data-carousel-title]');
    var counterNode = modal.querySelector('[data-carousel-counter]');
    var openNode = modal.querySelector('[data-carousel-open]');

    var item = generatorCarouselItems[generatorCarouselIndex];
    if (!item || !imageNode) {
      return;
    }

    imageNode.src = item.full;
    imageNode.alt = item.name || 'Generated preview';
    if (titleNode) {
      titleNode.textContent = item.name || 'Generated preview';
    }
    if (counterNode) {
      counterNode.textContent = String(generatorCarouselIndex + 1) + ' / ' + String(generatorCarouselItems.length);
    }
    if (openNode) {
      openNode.href = item.full;
    }
  }

  function openGeneratorCarousel(modal, index) {
    if (!modal || !generatorCarouselItems.length) {
      return;
    }

    var safeLength = generatorCarouselItems.length;
    generatorCarouselIndex = ((index % safeLength) + safeLength) % safeLength;
    modal.dataset.open = 'true';
    modal.dataset.visible = '1';
    renderGeneratorCarousel(modal);
  }

  function closeGeneratorCarousel(modal) {
    if (!modal) {
      return;
    }
    modal.dataset.open = 'false';
    modal.dataset.visible = '';
  }

  function wireGeneratorCarousel() {
    var modal = document.querySelector('[data-carousel-modal]');
    if (!modal) {
      return;
    }

    var closeButton = modal.querySelector('[data-carousel-close]');
    var prevButton = modal.querySelector('[data-carousel-prev]');
    var nextButton = modal.querySelector('[data-carousel-next]');

    if (closeButton) {
      closeButton.addEventListener('click', function () {
        closeGeneratorCarousel(modal);
      });
    }

    if (prevButton) {
      prevButton.addEventListener('click', function () {
        if (!generatorCarouselItems.length) {
          return;
        }
        openGeneratorCarousel(modal, generatorCarouselIndex - 1);
      });
    }

    if (nextButton) {
      nextButton.addEventListener('click', function () {
        if (!generatorCarouselItems.length) {
          return;
        }
        openGeneratorCarousel(modal, generatorCarouselIndex + 1);
      });
    }

    modal.addEventListener('click', function (evt) {
      if (evt.target === modal) {
        closeGeneratorCarousel(modal);
      }
    });

    document.addEventListener('click', function (evt) {
      var trigger = evt.target.closest('[data-generator-carousel-trigger]');
      if (!trigger) {
        return;
      }

      rebuildGeneratorCarouselItems();
      var triggerNodes = Array.prototype.slice.call(document.querySelectorAll('[data-generator-carousel-trigger]'));
      var index = triggerNodes.indexOf(trigger);
      if (index < 0) {
        index = 0;
      }
      openGeneratorCarousel(modal, index);
    });

    document.addEventListener('keydown', function (evt) {
      if (!modal.dataset.visible) {
        return;
      }

      if (evt.key === 'Escape') {
        closeGeneratorCarousel(modal);
      } else if (evt.key === 'ArrowLeft') {
        openGeneratorCarousel(modal, generatorCarouselIndex - 1);
      } else if (evt.key === 'ArrowRight') {
        openGeneratorCarousel(modal, generatorCarouselIndex + 1);
      }
    });

    rebuildGeneratorCarouselItems();
  }

  function clearPendingJobs(button) {
    var root = document.getElementById('mockup-dashboard-root');
    if (!root || !button) {
      return;
    }

    var clearUrl = root.dataset.clearPendingUrl || '';
    if (!clearUrl) {
      showStatusMessage('Missing clear-pending endpoint configuration.', 'error');
      return;
    }

    var pendingCountNode = document.getElementById('status-count-pending');
    var retryQueuedCountNode = document.getElementById('status-count-retry-queued');
    var pendingCount = parseIntSafe(pendingCountNode ? pendingCountNode.textContent : '0', 0);
    var retryQueuedCount = parseIntSafe(retryQueuedCountNode ? retryQueuedCountNode.textContent : '0', 0);
    if (pendingCount + retryQueuedCount < 1) {
      showStatusMessage('There are no pending jobs to clear.', 'info');
      return;
    }

    setButtonsDisabled(true);
    showStatusMessage('Clearing pending jobs...', 'info');

    window.fetch(clearUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(function (response) {
        return response.json().then(function (data) {
          return { ok: response.ok, data: data };
        });
      })
      .then(function (result) {
        if (!result.ok || result.data.error) {
          throw new Error(result.data.error || 'Clear pending request failed');
        }
        showStatusMessage('Cleared ' + String(result.data.cleared || 0) + ' pending job(s).', 'success');
        refreshStatus();
      })
      .catch(function (error) {
        showStatusMessage('Error: ' + error.message, 'error');
      })
      .finally(function () {
        setButtonsDisabled(false);
        button.blur();
      });
  }

  function clearFailedJobs(button) {
    var root = document.getElementById('mockup-dashboard-root');
    if (!root || !button) {
      return;
    }

    var clearUrl = root.dataset.clearFailedUrl || '';
    if (!clearUrl) {
      showStatusMessage('Missing clear-failed endpoint configuration.', 'error');
      return;
    }

    var failedCountNode = document.getElementById('status-count-failed');
    var failedCount = parseIntSafe(failedCountNode ? failedCountNode.textContent : '0', 0);
    if (failedCount < 1) {
      showStatusMessage('There are no failed jobs to clear.', 'info');
      return;
    }

    setButtonsDisabled(true);
    showStatusMessage('Clearing failed jobs...', 'info');

    window.fetch(clearUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(function (response) {
        return response.json().then(function (data) {
          return { ok: response.ok, data: data };
        });
      })
      .then(function (result) {
        if (!result.ok || result.data.error) {
          throw new Error(result.data.error || 'Clear failed request failed');
        }
        showStatusMessage('Cleared ' + String(result.data.cleared || 0) + ' failed job(s).', 'success');
        refreshStatus();
      })
      .catch(function (error) {
        showStatusMessage('Error: ' + error.message, 'error');
      })
      .finally(function () {
        setButtonsDisabled(false);
        button.blur();
      });
  }

  function refreshStatus() {
    var root = document.getElementById('mockup-dashboard-root');
    if (!root) {
      return;
    }

    var statusUrl = root.dataset.statusUrl || '';
    if (!statusUrl) {
      return;
    }

    window.fetch(statusUrl)
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (!data || !data.status_counts) {
          return;
        }

        var statusCounts = data.status_counts;
        var processingTotal = parseIntSafe(statusCounts.ProcessingCoordinates, 0) + parseIntSafe(statusCounts.Processing, 0);
        var retryQueuedCount = parseIntSafe(data.retry_queued_count, 0);
        var rawPending = parseIntSafe(statusCounts.Pending, 0);
        var mapping = {
          Pending: 'status-count-pending',
          Generating: 'status-count-generating',
          Completed: 'status-count-completed',
          Failed: 'status-count-failed'
        };

        Object.keys(mapping).forEach(function (statusKey) {
          var node = document.getElementById(mapping[statusKey]);
          if (node) {
            var val = parseIntSafe(statusCounts[statusKey] || 0, 0);
            // Pending card shows non-retry-queued count only.
            if (statusKey === 'Pending') {
              val = Math.max(0, val - retryQueuedCount);
            }
            node.textContent = String(val);
          }
        });

        var processingNode = document.getElementById('status-count-processing');
        if (processingNode) {
          processingNode.textContent = String(processingTotal);
        }

        var retryQueuedNode = document.getElementById('status-count-retry-queued');
        if (retryQueuedNode) {
          retryQueuedNode.textContent = String(retryQueuedCount);
        }

        if (data.control_state && data.control_state.state) {
          updateStateBadge(data.control_state.state);
        }
        if (data.control_state) {
          var skip = String(data.control_state.skip_coordinate_detection || 'false').toLowerCase() === 'true';
          updateCoordinateDetectionUI(skip);
        }

        if (data.recent_failed_jobs) {
          renderRecentFailures(data.recent_failed_jobs);
        }

        if (data.recent_completed_jobs) {
          renderRecentCompleted(data.recent_completed_jobs);
        }

        if (data.recent_attempt_logs) {
          renderRecentAttemptLogs(data.recent_attempt_logs);
        }

        renderActiveJob(data.active_job || null);
        renderNextPending(data.next_pending || [], data.retry_queued_jobs || []);
        updateLastRefreshed();

        var total = parseIntSafe(data.total_jobs, 0);
        var completed = parseIntSafe(statusCounts.Completed, 0);
        var pct = total > 0 ? Math.floor((completed / total) * 100) : 0;
        updateProgressBar(document.getElementById('progress-fill'), pct);

        // Adaptive polling: fast (10s) while anything is happening, slow (30s) when idle.
        var active = parseIntSafe(statusCounts.Generating, 0) + processingTotal;
        var pendingLeft = Math.max(0, rawPending - retryQueuedCount);
        setAdaptiveInterval(active > 0 || pendingLeft > 0 || retryQueuedCount > 0);
      })
      .catch(function () {
        return undefined;
      });
  }

  function wireModeInputs() {
    var modeEl = document.getElementById('generation-mode');
    var aspectEl = document.getElementById('generation-aspect');
    var categoryEl = document.getElementById('generation-category');

    if (!modeEl || !aspectEl || !categoryEl) {
      return;
    }

    function syncVisibility() {
      var mode = modeEl.value;
      aspectEl.disabled = !(mode === 'aspect_only' || mode === 'aspect_and_category');
      categoryEl.disabled = !(mode === 'category_only' || mode === 'aspect_and_category');
    }

    modeEl.addEventListener('change', syncVisibility);
    syncVisibility();
  }

  document.addEventListener('DOMContentLoaded', function () {
    var root = document.getElementById('mockup-dashboard-root');
    if (!root) {
      return;
    }

    updateProgressBar(
      document.getElementById('progress-fill'),
      parseIntSafe(root.dataset.completionPercentage, 0)
    );
    updateCoordinateDetectionUI(String(root.dataset.skipCoordinateDetection || 'false').toLowerCase() === 'true');

    wireModeInputs();

    var startButton = document.getElementById('start-pipeline-button');
    if (startButton) {
      startButton.addEventListener('click', function () {
        startGenerationPipeline(startButton);
      });
    }

    var clearPendingButton = document.getElementById('clear-pending-button');
    if (clearPendingButton) {
      clearPendingButton.addEventListener('click', function () {
        clearPendingJobs(clearPendingButton);
      });
    }

    var clearFailedButton = document.getElementById('clear-failed-button');
    if (clearFailedButton) {
      clearFailedButton.addEventListener('click', function () {
        clearFailedJobs(clearFailedButton);
      });
    }

    var toggleCoordinateDetectionButton = document.getElementById('toggle-coordinate-detection-button');
    if (toggleCoordinateDetectionButton) {
      toggleCoordinateDetectionButton.addEventListener('click', function () {
        var badge = document.getElementById('coordinate-detection-badge');
        var currentlySkip = badge && String(badge.dataset.skipCoordinateDetection || 'false').toLowerCase() === 'true';
        sendControlAction('set_skip_coordinate_detection', toggleCoordinateDetectionButton, {
          skip_coordinate_detection: !currentlySkip
        });
      });
    }

    var autoPromptButton = document.getElementById('auto-generate-custom-prompt-button');
    if (autoPromptButton) {
      autoPromptButton.addEventListener('click', function () {
        var customPromptEl = document.getElementById('custom-prompt-text');
        if (!customPromptEl) {
          return;
        }
        customPromptEl.value = buildAutoPromptText();
        showStatusMessage('Custom prompt generated. This text will be sent directly with the selected guide image.', 'success');
      });
    }

    var previewPromptButton = document.getElementById('preview-rendered-prompt-button');
    if (previewPromptButton) {
      previewPromptButton.addEventListener('click', function () {
        previewRenderedPrompt(previewPromptButton);
      });
    }

    var selectAllPreviewsButton = document.getElementById('select-all-previews-button');
    if (selectAllPreviewsButton) {
      selectAllPreviewsButton.addEventListener('click', function () {
        var boxes = getCompletedPreviewCheckboxes();
        var selected = getSelectedCompletedJobIds();
        var shouldSelectAll = boxes.length > 0 && selected.length !== boxes.length;
        setAllPreviewSelections(shouldSelectAll);
      });
    }

    var clearSelectionPreviewsButton = document.getElementById('clear-selection-previews-button');
    if (clearSelectionPreviewsButton) {
      clearSelectionPreviewsButton.addEventListener('click', function () {
        setAllPreviewSelections(false);
      });
    }

    var deleteSelectedPreviewsButton = document.getElementById('delete-selected-previews-button');
    if (deleteSelectedPreviewsButton) {
      deleteSelectedPreviewsButton.addEventListener('click', function () {
        var selectedIds = getSelectedCompletedJobIds();
        if (!selectedIds.length) {
          showStatusMessage('Select at least one completed preview to delete.', 'info');
          return;
        }
        openDeleteConfirmModal({
          mode: 'bulk',
          label: '',
          jobIds: selectedIds
        });
      });
    }

    var approveSelectedPreviewsButton = document.getElementById('approve-selected-previews-button');
    if (approveSelectedPreviewsButton) {
      approveSelectedPreviewsButton.addEventListener('click', function () {
        var selectedIds = getSelectedCompletedJobIds();
        if (!selectedIds.length) {
          showStatusMessage('Select at least one completed preview to approve.', 'info');
          return;
        }
        approveCompletedJobs(selectedIds, approveSelectedPreviewsButton);
      });
    }

    var pauseButton = document.getElementById('pause-pipeline-button');
    if (pauseButton) {
      pauseButton.addEventListener('click', function () {
        sendControlAction('pause', pauseButton);
      });
    }

    var resumeButton = document.getElementById('resume-pipeline-button');
    if (resumeButton) {
      resumeButton.addEventListener('click', function () {
        sendControlAction('resume', resumeButton);
      });
    }

    var stopButton = document.getElementById('stop-pipeline-button');
    if (stopButton) {
      stopButton.addEventListener('click', function () {
        sendControlAction('stop', stopButton);
      });
    }

    wireGeneratorCarousel();
    wireDeleteConfirmModal();

    // Force-retry delegation — handles both static (server-rendered) and
    // dynamic (JS-rendered) Retry Now buttons inside the next-pending table.
    document.addEventListener('click', function (evt) {
      var btn = evt.target.closest('.force-retry-btn');
      if (!btn) {
        var deleteBtn = evt.target.closest('[data-delete-completed-job-id]');
        if (!deleteBtn) {
          var approveBtn = evt.target.closest('[data-approve-completed-job-id]');
          if (!approveBtn) {
            return;
          }
          var approveJobId = parseIntSafe(approveBtn.getAttribute('data-approve-completed-job-id'), 0);
          if (approveJobId > 0) {
            approveCompletedJobs([approveJobId], approveBtn);
          }
          return;
        }
        var deleteJobId = parseIntSafe(deleteBtn.getAttribute('data-delete-completed-job-id'), 0);
        if (deleteJobId > 0) {
          openDeleteConfirmModal({
            mode: 'single',
            label: String(deleteBtn.getAttribute('data-delete-completed-job-name') || ''),
            jobIds: [deleteJobId]
          });
        }
        return;
      }
      var jobId = btn.getAttribute('data-force-retry-job-id');
      if (jobId) {
        forceRetryJob(jobId, btn);
      }
    });

    document.addEventListener('change', function (evt) {
      var checkbox = evt.target.closest('.completed-preview-checkbox');
      if (!checkbox) {
        return;
      }
      updateCompletedPreviewSelectionState();
    });

    // Initial active-job timer (if a job was already running at page load).
    var initialPanel = document.getElementById('active-job-panel');
    if (initialPanel && initialPanel.dataset.startedAt) {
      startActiveJobTimer(initialPanel.dataset.startedAt, initialPanel.dataset.updatedAt || '');
    }

    updateCompletedPreviewSelectionState();

    refreshStatus();
    _refreshIntervalId = setInterval(refreshStatus, 30000);
  });
})();
