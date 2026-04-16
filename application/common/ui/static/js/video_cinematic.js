(function () {
  // Debug flag: set window.__VIDEO_DEBUG = true to enable logging
  const DEBUG = window.__VIDEO_DEBUG !== false;
  const log = (...args) => DEBUG && console.log('[Director Suite]', ...args);
  
  const root = document.querySelector('[data-video-suite]');
  if (!root) {
    log('FATAL: Root [data-video-suite] not found');
    return;
  }
  
  log('Initialization starting...');

  // DOM references
  const slug = root.dataset.slug;
  const csrfMeta = document.querySelector('meta[name="csrf-token"]');
  const csrf = csrfMeta ? (csrfMeta.getAttribute('content') || '').trim() : '';
  const settingsUrl = root.dataset.settingsUrl || '';
  const statusUrl = root.dataset.statusUrl || '';
  const generateUrl = root.dataset.generateUrl || '';
  const deleteUrl = root.dataset.deleteUrl || '';

  // Duration controls
  const durationButtonsWrap = root.querySelector('[data-duration-buttons]');
  const durationLabel = root.querySelector('[data-duration-label]');

  //Artwork controls
  const artworkZoomIntensityInput = root.querySelector('[data-artwork-zoom-intensity]');
  const artworkZoomIntensityValue = root.querySelector('[data-artwork-zoom-intensity-value]');
  const artworkZoomDurationInput = root.querySelector('[data-artwork-zoom-duration]');
  const artworkZoomDurationValue = root.querySelector('[data-artwork-zoom-duration-value]');
  const artworkPanToggle = root.querySelector('[data-artwork-pan-toggle]');
  const artworkPanDirectionBlock = root.querySelector('[data-artwork-direction-block]');
  const artworkPanDirectionButtons = root.querySelector('[data-artwork-pan-direction]');

  // Mockup controls removed - use per-mockup controls in storyboard instead

  // Action controls
  const startBtn = root.querySelector('[data-start-render]');
  const deleteBtn = root.querySelector('[data-delete-btn]');
  const downloadBtn = root.querySelector('[data-download-btn]');
  const statusBox = root.querySelector('[data-status-box]');
  const stageEl = root.querySelector('[data-status-stage]');
  const percentEl = root.querySelector('[data-status-percent]');
  const fillEl = root.querySelector('[data-status-fill]');
  const msgEl = root.querySelector('[data-status-message]');
  const player = root.querySelector('[data-suite-player]');
  const storyboardGrid = root.querySelector('[data-storyboard-grid]');
  const storyboardCount = root.querySelector('[data-storyboard-count]');
  const renderOverlay = root.querySelector('[data-render-overlay]');
  const chosenPanel = root.querySelector('[data-chosen-panel]');
  const chosenList = root.querySelector('[data-chosen-list]');
  const chosenEmpty = root.querySelector('[data-chosen-empty]');
  const chosenNoMockups = root.querySelector('[data-chosen-no-mockups]');
  const chosenTitle = root.querySelector('[data-chosen-title]');
  const chosenSubtitle = root.querySelector('[data-chosen-subtitle]');

  // Output settings
  const outputFpsSelect = root.querySelector('[data-output-fps]');
  const outputSizeSelect = root.querySelector('[data-output-size]');
  const outputPresetSelect = root.querySelector('[data-output-preset]');
  const outputSourceSelect = root.querySelector('[data-output-source]');
  const outputWarning = root.querySelector('[data-output-warning]');

  // Load persisted video suite settings from template
  const parseVideoSuite = (value) => {
    if (!value) return {};
    try {
      const parsed = JSON.parse(value);
      return parsed && typeof parsed === 'object' ? parsed : {};
    } catch (_err) {
      return {};
    }
  };
  
  const persistedVideoSuite = parseVideoSuite(root.dataset.videoSuiteJson);
  log('📦 Persisted video suite loaded:', {
    artwork_pan_direction: readPersistedMainPanDirection(persistedVideoSuite, 'up'),
    artwork_pan_enabled: readPersistedMainPanEnabled(persistedVideoSuite, true),
    persistedSuiteKeys: Object.keys(persistedVideoSuite)
  });

  const readDuration = () => {
    if (durationLabel) {
      const labelValue = Number(String(durationLabel.textContent || '').replace(/[^0-9.]/g, ''));
      if (Number.isFinite(labelValue) && labelValue > 0) return labelValue;
    }
    if (durationButtonsWrap) {
      const active = durationButtonsWrap.querySelector('.btn-dark[data-duration-value]');
      if (active) {
        const activeValue = Number(active.dataset.durationValue);
        if (Number.isFinite(activeValue) && activeValue > 0) return activeValue;
      }
    }
    return 15;
  };

  const readDirection = (buttons, fallback) => {
    if (!buttons) return fallback;
    const active = buttons.querySelector('.btn-dark[data-direction]');
    return (active && active.dataset.direction) || fallback;
  };

  const safeNumber = (value, fallback) => {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
  };

  function normalizeMainPanDirection(value, fallback = 'up') {
    const normalized = String(value || '').trim().toLowerCase();
    return ['center', 'top-left', 'top-right', 'bottom-right', 'bottom-left', 'up', 'down', 'left', 'right'].includes(normalized) ? normalized : fallback;
  }

  function readPersistedMainPanDirection(suite, fallback = 'up') {
    if (!suite || typeof suite !== 'object') return fallback;
    if (suite.artwork_pan_direction !== undefined) {
      return normalizeMainPanDirection(suite.artwork_pan_direction, fallback);
    }
    if (suite.artwork && typeof suite.artwork === 'object') {
      return normalizeMainPanDirection(suite.artwork.pan_direction, fallback);
    }
    return fallback;
  }

  function readPersistedMainPanEnabled(suite, fallback = true) {
    if (!suite || typeof suite !== 'object') return fallback;
    if (suite.artwork_pan_enabled !== undefined) return Boolean(suite.artwork_pan_enabled);
    if (suite.artwork && typeof suite.artwork === 'object' && suite.artwork.pan_enabled !== undefined) {
      return Boolean(suite.artwork.pan_enabled);
    }
    return fallback;
  }

  const parseJsonList = (value) => {
    if (!value) return [];
    try {
      const parsed = JSON.parse(value);
      return Array.isArray(parsed) ? parsed : [];
    } catch (_err) {
      return [];
    }
  };

  const normalizeOrderList = (ids) => {
    const seen = new Set();
    const cleaned = [];
    ids.forEach((id) => {
      const value = String(id || '').trim();
      if (!value || seen.has(value)) return;
      seen.add(value);
      cleaned.push(value);
    });
    return cleaned;
  };

  const getCardMockupId = (card) => {
    if (!card) return null;
    const raw = card.dataset.mockupId || card.dataset.filename || '';
    const value = String(raw || '').trim();
    return value.length > 0 ? value : null;
  };

  let mockupCards = [];
  const mockupMap = new Map();
  const refreshMockupMap = () => {
    mockupCards = Array.from(root.querySelectorAll('[data-storyboard-item]'));
    mockupMap.clear();
    mockupCards.forEach((card) => {
      const id = getCardMockupId(card);
      if (!id) return;
      mockupMap.set(id, {
        id,
        card,
        checkbox: card.querySelector('[data-storyboard-checkbox]'),
        thumbUrl: card.dataset.thumbUrl || '',
        fullUrl: card.dataset.fullUrl || '',
        label: id,
      });
    });
  };
  refreshMockupMap();

  // Use persisted video suite for order and shots when available, fall back to data attributes
  const storedOrderIds = normalizeOrderList(
    persistedVideoSuite.video_mockup_order && Array.isArray(persistedVideoSuite.video_mockup_order)
      ? persistedVideoSuite.video_mockup_order
      : parseJsonList(root.dataset.videoMockupOrder)
  );
  const storedAutoIds = normalizeOrderList(parseJsonList(root.dataset.autoMockupIds));
  let currentOrderIds = storedOrderIds.slice();

  // Load per-mockup shots from persisted suite
  const parseShots = (value) => {
    if (!value) return [];
    try {
      const parsed = JSON.parse(value);
      return Array.isArray(parsed) ? parsed : [];
    } catch (_err) {
      return [];
    }
  };
  
  const storedShots = persistedVideoSuite.video_mockup_shots && typeof persistedVideoSuite.video_mockup_shots === 'object' && Array.isArray(persistedVideoSuite.video_mockup_shots)
    ? persistedVideoSuite.video_mockup_shots
    : parseShots(root.dataset.videoMockupShots);
  let currentShots = storedShots.slice();
  
  const getShotById = (id) => {
    return currentShots.find((shot) => shot.id === id);
  };

  const PAN_DIRECTIONS = new Set(['none', 'aim', 'center', 'top-left', 'top-right', 'bottom-right', 'bottom-left', 'up', 'down', 'left', 'right']);
  
  const setShotById = (id, panDirection, zoomEnabled = true, zoomIntensity = null) => {
    let normalizedPanDirection = panDirection;
    let normalizedZoomEnabled = zoomEnabled;
    let normalizedZoomIntensity = zoomIntensity;

    // Backward-safe guard: recover if args are passed as (id, zoomEnabled, panDirection)
    if (typeof normalizedPanDirection === 'boolean' && typeof normalizedZoomEnabled === 'string') {
      const recoveredPanDirection = normalizedZoomEnabled;
      normalizedZoomEnabled = normalizedPanDirection;
      normalizedPanDirection = recoveredPanDirection;
    }

    if (typeof normalizedPanDirection !== 'string') {
      normalizedPanDirection = 'right';
    }
    normalizedPanDirection = normalizedPanDirection.trim().toLowerCase();
    if (!PAN_DIRECTIONS.has(normalizedPanDirection)) {
      normalizedPanDirection = 'right';
    }

    // Clamp zoom intensity to 1.0-2.25 range
    if (normalizedZoomIntensity !== null && normalizedZoomIntensity !== undefined) {
      normalizedZoomIntensity = Math.max(1.0, Math.min(2.25, Number(normalizedZoomIntensity) || 1.1));
    }

    // Derive pan_enabled and auto_target from pan_direction
    const panEnabled = normalizedPanDirection !== 'none';
    const autoAim = normalizedPanDirection === 'aim';
    
    const existing = getShotById(id);
    if (existing) {
      existing.pan_enabled = Boolean(panEnabled);
      existing.pan_direction = normalizedPanDirection;
      existing.zoom_enabled = Boolean(normalizedZoomEnabled);
      if (normalizedZoomIntensity !== null && normalizedZoomIntensity !== undefined) {
        existing.zoom_intensity = normalizedZoomIntensity;
      }
      existing.pan_to_artwork_center = Boolean(autoAim);
      existing.auto_target = Boolean(autoAim);
    } else {
      const newShot = {
        id,
        pan_enabled: Boolean(panEnabled),
        pan_direction: normalizedPanDirection,
        zoom_enabled: Boolean(normalizedZoomEnabled),
        pan_to_artwork_center: Boolean(autoAim),
        auto_target: Boolean(autoAim),
      };
      if (normalizedZoomIntensity !== null && normalizedZoomIntensity !== undefined) {
        newShot.zoom_intensity = normalizedZoomIntensity;
      }
      currentShots.push(newShot);
    }
  };
  
  const removeShotById = (id) => {
    currentShots = currentShots.filter((shot) => shot.id !== id);
  };

  // ========== TIMING SYSTEM ==========
  // Per-mockup timing state: maps mockup_id -> duration_seconds
  // Only includes mockups with locked (manual) durations
  let videoMockupTimings = {};
  if (persistedVideoSuite.video_mockup_timings && typeof persistedVideoSuite.video_mockup_timings === 'object') {
    videoMockupTimings = Object.assign({}, persistedVideoSuite.video_mockup_timings);
  }
  
  // Main artwork seconds (default 4.0)
  let mainArtworkSeconds = safeNumber(persistedVideoSuite.main_artwork_seconds, 4.0);
  
  // Allowed per-mockup durations (seconds)
  const ALLOWED_DURATIONS = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0];
  const MAX_MOCKUPS = 10;  // Hard limit on chosen mockups
  
  const clampDuration = (sec) => {
    const val = Math.max(1.0, Math.min(4.0, Number(sec) || 1.0));
    // Snap to nearest 0.5
    return Math.round(val * 2) / 2;
  };
  
  const setMockupTiming = (mockupId, durationSeconds) => {
    if (durationSeconds === null || durationSeconds === undefined) {
      delete videoMockupTimings[mockupId];
    } else {
      videoMockupTimings[mockupId] = clampDuration(durationSeconds);
    }
  };
  
  const getMockupTiming = (mockupId) => {
    return videoMockupTimings[mockupId] || null;
  };
  
  // Auto-math calculation
  // Returns: {
  //   lockedSum, autoCount, remainingForAuto, eachAuto,
  //   lockedScaled (dict of scaled durations if needed),
  //   scale,
  //   mockupDurations (dict of mockup_id -> effective duration),
  //   warning (str or null)
  // }
  const computeTimingBreakdown = (orderedMockupIds) => {
    const totalDuration = safeNumber(currentSettings.video_duration || 15, 15);
    const mainSeconds = Math.max(1.0, Math.min(10.0, mainArtworkSeconds));
    // Mirror backend timing math: each mockup crossfade contributes 0.5s overlap,
    // so usable mockup time includes crossfade savings.
    const crossfadeSeconds = 0.5;
    const crossfadeSavings = orderedMockupIds.length * crossfadeSeconds;
    const availableForMockups = Math.max(0, totalDuration - mainSeconds + crossfadeSavings);
    
    let lockedSum = 0;
    let lockedIds = [];
    let autoIds = [];
    
    orderedMockupIds.forEach((id) => {
      const timing = getMockupTiming(id);
      if (timing !== null) {
        lockedSum += timing;
        lockedIds.push(id);
      } else {
        autoIds.push(id);
      }
    });
    
    const autoCount = autoIds.length;
    let eachAuto = autoCount > 0 ? availableForMockups / autoCount : 0;
    let scale = 1.0;
    let warning = null;
    let lockedScaled = {};
    
    // If locked exceeds available, scale down all locked durations
    if (lockedSum > availableForMockups && lockedSum > 0) {
      scale = availableForMockups / lockedSum;
      warning = `Locked time exceeds available. Scaled to fit: ×${scale.toFixed(2)}`;
      lockedIds.forEach((id) => {
        const original = videoMockupTimings[id];
        lockedScaled[id] = original * scale;
      });
    } else {
      lockedIds.forEach((id) => {
        lockedScaled[id] = videoMockupTimings[id];
      });
    }
    
    // Recompute remainingForAuto after scaling
    let lockedSumAfterScale = Object.values(lockedScaled).reduce((a, b) => a + b, 0);
    let remainingForAuto = Math.max(0, availableForMockups - lockedSumAfterScale);
    eachAuto = autoCount > 0 ? remainingForAuto / autoCount : 0;
    
    // Build final mockupDurations dict
    const mockupDurations = {};
    orderedMockupIds.forEach((id) => {
      if (lockedScaled[id] !== undefined) {
        mockupDurations[id] = lockedScaled[id];
      } else if (autoIds.includes(id)) {
        mockupDurations[id] = eachAuto;
      }
    });
    
    return {
      totalDuration,
      mainSeconds,
      availableForMockups,
      lockedSum,
      lockedScaled,
      autoCount,
      eachAuto,
      remainingForAuto,
      scale,
      mockupDurations,
      warning,
    };
  };

  let duration = readDuration();
  let pollTimer = null;

  // Current settings state - use persisted values when available
  let currentSettings = {
    video_duration: safeNumber(persistedVideoSuite.video_duration || duration, duration),
    artwork_zoom_intensity: safeNumber(persistedVideoSuite.artwork_zoom_intensity || (artworkZoomIntensityInput && artworkZoomIntensityInput.value), 1.1),
    artwork_zoom_duration: safeNumber(persistedVideoSuite.artwork_zoom_duration || (artworkZoomDurationInput && artworkZoomDurationInput.value), 3.0),
    artwork_pan_enabled: readPersistedMainPanEnabled(persistedVideoSuite, Boolean(artworkPanToggle && artworkPanToggle.checked)),
    artwork_pan_direction: readPersistedMainPanDirection(persistedVideoSuite, readDirection(artworkPanDirectionButtons, 'up')),
    video_fps: safeNumber(persistedVideoSuite.video_fps || (outputFpsSelect && outputFpsSelect.value), 24),
    video_output_size: safeNumber(persistedVideoSuite.video_output_size || (outputSizeSelect && outputSizeSelect.value), 1024),
    video_encoder_preset: persistedVideoSuite.video_encoder_preset || (outputPresetSelect && outputPresetSelect.value ? String(outputPresetSelect.value) : 'fast'),
    video_artwork_source: persistedVideoSuite.video_artwork_source || (outputSourceSelect && outputSourceSelect.value ? String(outputSourceSelect.value) : 'auto'),
  };

  const postJson = async (url, body) => {
    const resp = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(csrf ? { 'X-CSRFToken': csrf, 'X-CSRF-Token': csrf } : {}),
        'X-Requested-With': 'XMLHttpRequest',
      },
      credentials: 'same-origin',
      body: JSON.stringify(body),
    });
    const text = await resp.text().catch(() => '');
    let data = {};
    if (text) {
      try {
        data = JSON.parse(text);
      } catch (_err) {
        data = {};
      }
    }
    return { resp, data, text };
  };

  const buildErrorMessage = (fallback, resp, data, text) => {
    const detail = [];
    const dataMessage = data && (data.message || data.error);
    if (dataMessage) {
      detail.push(String(dataMessage));
    } else if (text && text.trim()) {
      detail.push(text.trim());
    }
    if (resp && !resp.ok) {
      detail.push(`HTTP ${resp.status}`);
    }
    return detail.length ? detail.join(' | ') : fallback;
  };

  const patchStatus = (data) => {
    const pct = Math.max(0, Math.min(100, Number(data && data.percent) || 0));
    const framesCompleted = Number(data && data.frames_completed) || 0;
    const totalFrames = Number(data && data.total_frames) || 0;
    const startedAt = data && data.started_at ? Date.parse(data.started_at) : null;
    let etaText = '';
    if (framesCompleted > 0 && totalFrames > 0 && startedAt && Number.isFinite(startedAt)) {
      const elapsed = Math.max(1, (Date.now() - startedAt) / 1000);
      const fps = framesCompleted / elapsed;
      const remaining = fps > 0 ? Math.max(0, Math.round((totalFrames - framesCompleted) / fps)) : 0;
      etaText = `Render: ${pct}% Complete (Approx. ${remaining} seconds remaining)`;
    }
    if (statusBox) statusBox.hidden = false;
    if (fillEl) fillEl.style.width = `${pct}%`;
    if (stageEl) stageEl.textContent = (data && data.stage) || 'processing';
    if (percentEl) percentEl.textContent = `${pct}%`;
    if (msgEl) msgEl.textContent = etaText || (data && data.message) || 'Rendering...';
  };

  /**
   * Update info summary lines for all chosen items (when timing breakdown changes)
   */
  const updateAllSummaryLines = () => {
    if (!chosenList) return;
    Array.from(chosenList.querySelectorAll('[data-mockup-id]')).forEach((item) => {
      const mockupId = item.dataset.mockupId;
      const shot = getShotById(mockupId);
      if (shot) {
        updateShotSummaryLine(item, shot);
      }
    });
  };

  const setDuration = (value) => {
    duration = Math.max(10, Math.min(20, Number(value) || 15));
    if (![10, 15, 20].includes(duration)) duration = 15;
    currentSettings.video_duration = duration;
    if (durationLabel) durationLabel.textContent = `${duration}s`;
    if (!durationButtonsWrap) return;
    durationButtonsWrap.querySelectorAll('[data-duration-value]').forEach((btn) => {
      const on = Number(btn.dataset.durationValue) === duration;
      btn.classList.toggle('btn-dark', on);
      btn.classList.toggle('btn-outline-secondary', !on);
    });
    // Update summary lines since Auto duration breakdown changed
    updateAllSummaryLines();
  };

  const updateArtworkZoomIntensity = () => {
    if (!artworkZoomIntensityInput) return;
    const val = Math.max(1.0, Math.min(2.25, Number(artworkZoomIntensityInput.value) || 1.1));
    currentSettings.artwork_zoom_intensity = val;
    if (artworkZoomIntensityValue) artworkZoomIntensityValue.textContent = `${val.toFixed(2)}x`;
  };

  const updateArtworkZoomDuration = () => {
    if (!artworkZoomDurationInput) return;
    const val = Math.max(0.0, Math.min(8.0, Number(artworkZoomDurationInput.value) || 3.0));
    currentSettings.artwork_zoom_duration = val;
    if (artworkZoomDurationValue) artworkZoomDurationValue.textContent = `${val.toFixed(1)}s`;
  };

  // Mockup update functions removed - use per-mockup controls in storyboard

  const getSelectedMockups = () => {
    const selected = Array.from(root.querySelectorAll('[data-storyboard-checkbox]'))
      .filter((box) => box && box.checked)
      .map((box) => String(box.value || '').trim())
      .filter((name) => name.length > 0)
      .slice(0, MAX_MOCKUPS);  // Enforce hard limit
    return selected;
  };

  const updateStoryboardCounter = () => {
    if (!storyboardCount) return;
    const count = getSelectedMockups().length;
    const countText = count === 0 ? 'No mockups selected' : `${count} Mockup${count !== 1 ? 's' : ''} Selected`;
    storyboardCount.textContent = countText;
  };

  const attachStoryboardCheckboxListeners = () => {
    Array.from(root.querySelectorAll('[data-storyboard-checkbox]')).forEach((box) => {
      if (!box || box.dataset.chosenListener === 'true') return;
      box.dataset.chosenListener = 'true';
      box.addEventListener('change', () => {
        updateStoryboardCounter();
        renderChosenList();
        persistOrder();
      });
    });
  };

  const getSelectedIds = () => {
    refreshMockupMap();
    const selected = mockupCards
      .filter((card) => {
        const checkbox = card.querySelector('[data-storyboard-checkbox]');
        return checkbox && checkbox.checked;
      })
      .map((card) => getCardMockupId(card))
      .filter((id) => id && mockupMap.has(id))
      .slice(0, MAX_MOCKUPS);  // Enforce hard limit
    log('✅ getSelectedIds() returning:', selected);
    return selected;
  };

  const getAutoIds = () => {
    refreshMockupMap();
    // Check if any mockups exist at all
    if (mockupCards.length === 0 || mockupMap.size === 0) {
      log('WARNING: NO MOCKUPS AVAILABLE - Cannot auto-select');
      return [];
    }
    
    // Try storedAutoIds first (from backend auto-selection)
    const filtered = storedAutoIds.filter((id) => mockupMap.has(id));
    if (filtered.length) {
      log('Using stored auto IDs:', filtered);
      return filtered;
    }
    
    // Fall back to all mockupCards, select first 5
    const all = mockupCards
      .map((card) => getCardMockupId(card))
      .filter((id) => id && mockupMap.has(id));
    
    const selected = all.slice(0, 5);
    log('Auto-selecting from available mockups:', selected);
    if (!selected.length) {
      log('WARNING: No mockups available for auto-selection!', {
        mockupCardsCount: mockupCards.length,
        mockupMapSize: mockupMap.size,
        storedAutoIdsCount: storedAutoIds.length,
      });
    }
    return selected;
  };

  // ========== ACTIVE MOCKUP SELECTION LOGIC ==========
  // FIXED: Only render what user explicitly selected. Never auto-populate.
  // Auto-select logic is ONLY for initialization, not every render.
  const getActiveMockupIds = () => {
    const selectedIds = getSelectedIds();
    // Always use manual mode based on actual checkbox state
    // If nothing selected, renderChosenList will show empty state (not auto-fill)
    return {
      mode: 'manual',
      ids: selectedIds,
      count: selectedIds.length,
    };
  };

  const applyOrder = (baseIds, orderIds) => {
    const ordered = orderIds.filter((id) => baseIds.includes(id));
    const remainder = baseIds.filter((id) => !ordered.includes(id));
    return ordered.concat(remainder);
  };

  const updateOrderBadges = () => {
    if (!chosenList) return;
    const items = Array.from(chosenList.querySelectorAll('.chosen-item'));
    log(`updateOrderBadges: updating ${items.length} badges to sequential 1..${items.length}`);
    items.forEach((item, index) => {
      const badge = item.querySelector('[data-order-badge]');
      if (badge) {
        badge.textContent = String(index + 1);
        log(`  Badge ${index}: set to ${index + 1} for mockup ${item.dataset.mockupId}`);
      }
    });
  };

  const persistOrder = async () => {
    if (!settingsUrl) return;
    try {
      await saveSettings();
    } catch (err) {
      patchStatus({ stage: 'error', percent: 100, message: err && err.message ? err.message : 'Failed to save mockup order' });
    }
  };

  const persistShots = async () => {
    if (!settingsUrl) return;
    try {
      await saveSettings();
    } catch (err) {
      patchStatus({ stage: 'error', percent: 100, message: err && err.message ? err.message : 'Failed to save mockup shots' });
    }
  };

  // Persist timing changes
  let persistTimingsTimer = null;
  const persistTimings = async () => {
    if (!settingsUrl) return;
    try {
      await saveSettings();
    } catch (err) {
      log('Failed to persist timings:', err);
    }
  };

  // Update timing summary bar with computed values
  const updateTimingSummary = () => {
    const timingSummary = root.querySelector('[data-timing-summary]');
    if (!timingSummary) return;
    
    // Use active mockup list (auto or manual)
    const active = getActiveMockupIds();
    const orderedIds = applyOrder(active.ids, currentOrderIds);
    const breakdown = computeTimingBreakdown(orderedIds);
    
    // Update summary stats
    const totalEl = root.querySelector('[data-timing-total]');
    const availableEl = root.querySelector('[data-timing-available]');
    const lockedCountEl = root.querySelector('[data-timing-locked-count]');
    const lockedTimeEl = root.querySelector('[data-timing-locked-time]');
    const autoCountEl = root.querySelector('[data-timing-auto-count]');
    const autoEachEl = root.querySelector('[data-timing-auto-each]');
    
    if (totalEl) totalEl.textContent = `${breakdown.totalDuration}s`;
    if (availableEl) availableEl.textContent = `${breakdown.availableForMockups.toFixed(1)}s`;
    if (lockedCountEl) lockedCountEl.textContent = String(Object.keys(breakdown.lockedScaled).length);
    if (lockedTimeEl) lockedTimeEl.textContent = `${Object.values(breakdown.lockedScaled).reduce((a,b) => a+b, 0).toFixed(1)}s`;
    if (autoCountEl) autoCountEl.textContent = String(breakdown.autoCount);
    if (autoEachEl) autoEachEl.textContent = `${breakdown.eachAuto.toFixed(2)}s`;
    
    // Show/hide warning (both old and new inline version)
    const warningEl = root.querySelector('[data-timing-warning]');
    const warningTextEl = root.querySelector('[data-timing-warning-text]');
    const warningInlineEl = root.querySelector('[data-timing-warning-inline]');
    
    if (breakdown.warning) {
      // Show old warning (in timing panel)
      if (warningEl) {
        warningEl.hidden = false;
        if (warningTextEl) warningTextEl.textContent = breakdown.warning;
      }
      // Show new inline warning (in chosen mockups panel)
      if (warningInlineEl) {
        warningInlineEl.hidden = false;
      }
    } else {
      if (warningEl) warningEl.hidden = true;
      if (warningInlineEl) warningInlineEl.hidden = true;
    }
    
    // Update effective time displays for each mockup
    if (chosenList) {
      chosenList.querySelectorAll('.chosen-item').forEach((item) => {
        const mockupId = item.dataset.mockupId;
        if (!mockupId) return;
        const effectiveDisplay = item.querySelector('.chosen-effective-time');
        if (!effectiveDisplay) return;
        const timing = getMockupTiming(mockupId);
        if (timing !== null) {
          effectiveDisplay.textContent = `= ${timing.toFixed(2)}s`;
        } else {
          effectiveDisplay.textContent = `= Auto (${breakdown.eachAuto.toFixed(2)}s)`;
        }
      });
    }
  };

  /**
   * Update pan direction button states to reflect current selection
   */
  const updateDirectionButtons = (block, buttons, activeDirection) => {
    if (!buttons) return;
    log(`🎨 updateDirectionButtons called with activeDirection: ${activeDirection}`);
    const dirButtons = buttons.querySelectorAll('[data-direction]');
    dirButtons.forEach((btn) => {
      const isActive = btn.dataset.direction === activeDirection;
      btn.classList.toggle('btn-dark', isActive);
      btn.classList.toggle('btn-outline-secondary', !isActive);
      btn.classList.toggle('is-active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
      if (isActive) {
        log(`🎨   Button ${btn.dataset.direction} set to ACTIVE (btn-dark)`);
      }
    });
  };

  /**
   * Enable/disable pan direction buttons based on pan toggle state
   */
  const updateArtworkPanStateButtons = () => {
    if (!artworkPanDirectionBlock || !artworkPanToggle) return;
    const enabled = artworkPanToggle.checked;
    // Show/hide direction buttons or disable them
    if (enabled) {
      artworkPanDirectionBlock.style.opacity = '1';
      artworkPanDirectionBlock.style.pointerEvents = 'auto';
    } else {
      artworkPanDirectionBlock.style.opacity = '0.4';
      artworkPanDirectionBlock.style.pointerEvents = 'none';
    }
  };

  /**
   * Update chosen panel visibility based on mockup count
   */
  const updateChosenPanel = () => {
    if (!chosenPanel) return;
    const active = getActiveMockupIds();
    if (active.count === 0 && mockupMap.size === 0) {
      // No mockups at all - show "no mockups" state
      chosenPanel.hidden = false;
      if (chosenNoMockups) chosenNoMockups.hidden = false;
      if (chosenEmpty) chosenEmpty.hidden = true;
    } else if (active.count === 0) {
      // Mockups exist but none selected - show "empty" state
      chosenPanel.hidden = false;
      if (chosenNoMockups) chosenNoMockups.hidden = true;
      if (chosenEmpty) chosenEmpty.hidden = false;
    } else {
      // Has selected mockups - show list
      chosenPanel.hidden = false;
      if (chosenNoMockups) chosenNoMockups.hidden = true;
      if (chosenEmpty) chosenEmpty.hidden = true;
    }
  };

  // ========== HELPER FUNCTIONS FOR CHOSEN LIST UI ==========
  
  /**
   * Format a shot summary string for display
   * E.g., "Time: Auto (2.00s) • Pan: Right • Zoom: On • Aim: Center"
   */
  const formatShotSummary = (shot, computedAutoSeconds) => {
    const items = [];
    
    // Duration
    const duration = getMockupTiming(shot.id);
    if (duration !== null) {
      items.push(`Time: ${duration.toFixed(1)}s`);
    } else if (computedAutoSeconds !== undefined && computedAutoSeconds > 0) {
      items.push(`Time: Auto (${computedAutoSeconds.toFixed(2)}s)`);
    } else {
      items.push('Time: Auto');
    }
    
    // Pan movement
    if (!shot.pan_enabled || shot.pan_direction === 'none') {
      items.push('Pan: Off');
    } else if (shot.pan_direction === 'aim') {
      items.push('Pan: Aim');
    } else {
      items.push(`Pan: ${shot.pan_direction.charAt(0).toUpperCase() + shot.pan_direction.slice(1)}`);
    }
    
    // Zoom animation
    if (shot.zoom_enabled !== false) {
      const zoomIntensity = shot.zoom_intensity ? Number(shot.zoom_intensity).toFixed(2) : '1.10';
      items.push(`Zoom: ${zoomIntensity}x`);
    } else {
      items.push('Zoom: Off');
    }
    
    return items.join(' • ');
  };

  /**
   * Create a labeled toggle control with ✓/✕ state indicator
   * Returns a label element with checkbox, label text, and state icon
   */
  const createToggleControl = (labelText, isChecked, mockupId, titleText) => {
    const wrapper = document.createElement('label');
    wrapper.className = 'chosen-toggle';
    if (isChecked) wrapper.classList.add('is-enabled');
    wrapper.setAttribute('title', titleText || '');
    
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.style.display = 'none';
    checkbox.checked = isChecked;
    checkbox.setAttribute('data-mockup-id', mockupId);
    
    const labelSpan = document.createElement('span');
    labelSpan.className = 'chosen-toggle__label';
    labelSpan.textContent = labelText;
    
    const stateSpan = document.createElement('span');
    stateSpan.className = 'chosen-toggle__state';
    stateSpan.setAttribute('aria-hidden', 'true');
    stateSpan.textContent = isChecked ? '✓' : '✕';
    
    wrapper.appendChild(checkbox);
    wrapper.appendChild(labelSpan);
    wrapper.appendChild(stateSpan);
    
    // Update state on change
    checkbox.addEventListener('change', () => {
      if (checkbox.checked) {
        wrapper.classList.add('is-enabled');
      } else {
        wrapper.classList.remove('is-enabled');
      }
      stateSpan.textContent = checkbox.checked ? '✓' : '✕';
    });
    
    return { wrapper, checkbox };
  };

  /**
   * Create a zoom intensity slider control
   * Returns a wrapper div with label, slider, and value display
   */
  const createZoomIntensityControl = (value = 1.1, mockupId) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'chosen-zoom-slider';
    wrapper.style.cssText = 'display: flex; align-items: center; gap: 8px; margin-top: 6px; padding: 4px 0;';
    
    const label = document.createElement('label');
    label.className = 'chosen-zoom-label';
    label.style.cssText = 'font-size: 12px; white-space: nowrap; min-width: 60px;';
    label.textContent = 'Zoom:';
    
    const slider = document.createElement('input');
    slider.type = 'range';
    slider.min = '1.00';
    slider.max = '2.25';
    slider.step = '0.01';
    slider.value = Number(value || 1.1).toFixed(2);
    slider.style.cssText = 'flex: 1; cursor: pointer;';
    slider.setAttribute('data-mockup-id', mockupId);
    slider.setAttribute('data-zoom-slider', 'true');
    
    const valueDisplay = document.createElement('span');
    valueDisplay.className = 'chosen-zoom-value';
    valueDisplay.style.cssText = 'font-weight: 500; min-width: 35px; text-align: right; font-size: 12px;';
    valueDisplay.textContent = Number(value || 1.1).toFixed(2) + 'x';
    
    // Update display when slider changes
    slider.addEventListener('input', () => {
      const val = Number(slider.value).toFixed(2);
      valueDisplay.textContent = val + 'x';
    });
    
    // Prevent card drag when interacting with slider
    // Use capture phase to stop drag bubbling without breaking slider interaction
    const stopDragBubble = (e) => {
      e.stopPropagation();
    };
    slider.addEventListener('mousedown', stopDragBubble, true);
    slider.addEventListener('touchstart', stopDragBubble, true);
    slider.addEventListener('pointerdown', stopDragBubble, true);
    slider.addEventListener('dragstart', (e) => e.preventDefault(), true);
    slider.addEventListener('selectstart', (e) => e.preventDefault(), true);
    
    wrapper.appendChild(label);
    wrapper.appendChild(slider);
    wrapper.appendChild(valueDisplay);
    
    return { wrapper, slider };
  };

  /**
   * Update the info summary line for a chosen item
   */
  const updateShotSummaryLine = (item, shot) => {
    if (!item) return;
    let summaryLine = item.querySelector('[data-chosen-summary]');
    if (!summaryLine) {
      summaryLine = document.createElement('div');
      summaryLine.className = 'chosen-row-summary';
      summaryLine.setAttribute('data-chosen-summary', '');
      item.appendChild(summaryLine);
    }
    
    // Calculate auto seconds for this mockup if applicable
    const active = getActiveMockupIds();
    const orderedIds = applyOrder(active.ids, currentOrderIds);
    const breakdown = computeTimingBreakdown(orderedIds);
    let compAuto = breakdown ? breakdown.eachAuto : undefined;
    
    summaryLine.textContent = formatShotSummary(shot, compAuto);
  };

  const renderChosenList = () => {
    // Verify chosenList element exists
    if (!chosenList) {
      log('FATAL: chosenList element not found! Selectors not matching template.');
      log('Attempted selectors:', {
        root_exists: !!root,
        chosen_list_selector: '[data-chosen-list]',
        html_check: root ? root.innerHTML.includes('data-chosen-list') : 'N/A'
      });
      return;
    }
    
    // Get ONLY what user selected (never auto-populate)
    const active = getActiveMockupIds();
    let availableIds = applyOrder(active.ids, currentOrderIds);
    
    // Enforce max limit hard cap
    availableIds = availableIds.slice(0, MAX_MOCKUPS);
    
    log('🎯 renderChosenList (FIXED):', {
      selectedCount: active.ids.length,
      cappedCount: availableIds.length,
      maxLimit: MAX_MOCKUPS,
      availableIds: availableIds
    });

    // Reset currentOrderIds to exactly what we have (prevents stale duplication)
    currentOrderIds = availableIds.slice();
    
    // CRITICAL: Clean orphaned shots FIRST, before rendering
    // This prevents duplication when user deletes/readds mockups
    const availableIdSet = new Set(availableIds);
    currentShots = currentShots.filter((shot) => availableIdSet.has(shot.id));
    
    // Ensure shots are in same order as chosen items, add missing shots
    const shotMap = new Map(currentShots.map((shot) => [shot.id, shot]));
    const newShots = [];
    availableIds.forEach((id) => {
      if (shotMap.has(id)) {
        newShots.push(shotMap.get(id));
      } else {
        // New mockup being added to chosen list—create default shot
        newShots.push({
          id,
          pan_enabled: true,
          pan_direction: 'right',
          zoom_enabled: true,
          pan_to_artwork_center: false,
          auto_target: false,
        });
      }
    });
    currentShots = newShots;
    
    chosenList.innerHTML = '';

    // Update headers (always manual mode now)
    if (chosenTitle) {
      chosenTitle.textContent = `Chosen Mockups (${availableIds.length})`;
    }
    if (chosenSubtitle) {
      chosenSubtitle.textContent = 'Drag to reorder. Max 10 mockups.';
    }

    // Handle empty state
    if (!availableIds.length) {
      if (chosenEmpty) chosenEmpty.hidden = false;
      log('No mockups selected - showing empty state');
      return;
    }
    if (chosenEmpty) chosenEmpty.hidden = true;

    let draggingItem = null;

    availableIds.forEach((id, index) => {
      const info = mockupMap.get(id);
      if (!info) return;
      
      // Shot is guaranteed to exist now (created in newShots above)
      // No need to create it again here
      
      const item = document.createElement('div');
      item.className = 'chosen-item';
      item.setAttribute('draggable', 'true');
      item.dataset.mockupId = id;

      const thumbWrapper = document.createElement('div');
      thumbWrapper.className = 'chosen-thumb-wrapper';

      const badge = document.createElement('span');
      badge.className = 'chosen-badge';
      badge.dataset.orderBadge = 'true';
      const badgeNumber = index + 1;
      badge.textContent = String(badgeNumber);
      log(`🏷️  Creating badge ${badgeNumber} for mockup ${id} (index ${index})`);

      const thumb = document.createElement('img');
      thumb.className = 'chosen-thumb';
      thumb.src = info.thumbUrl;
      thumb.alt = `${id} thumbnail`;
      thumb.loading = 'lazy';

      const removeBtn = document.createElement('button');
      removeBtn.type = 'button';
      removeBtn.className = 'chosen-remove';
      removeBtn.setAttribute('aria-label', 'Remove mockup');
      removeBtn.textContent = '×';
      removeBtn.addEventListener('click', () => {
        if (info.checkbox) {
          info.checkbox.checked = false;
          updateStoryboardCounter();
          renderChosenList();
          persistOrder();
        }
      });

      // Create per-mockup controls
      const controlsBlock = document.createElement('div');
      controlsBlock.className = 'chosen-controls';

      // === TIMING CONTROLS ===
      const timingGroup = document.createElement('div');
      timingGroup.className = 'chosen-timing-group';
      
      const timingLabel = document.createElement('span');
      timingLabel.className = 'chosen-timing-label';
      timingLabel.textContent = 'TIME';
      timingGroup.appendChild(timingLabel);
      
      const timingSelect = document.createElement('select');
      timingSelect.className = 'form-select form-select-sm chosen-timing-select';
      timingSelect.setAttribute('data-mockup-id', id);
      timingSelect.setAttribute('title', 'Mockup duration');
      
      // First option: Auto
      const autoOpt = document.createElement('option');
      autoOpt.value = 'auto';
      autoOpt.textContent = 'Auto';
      timingSelect.appendChild(autoOpt);
      
      // Locked duration options
      ALLOWED_DURATIONS.forEach((dur) => {
        const opt = document.createElement('option');
        opt.value = String(dur);
        opt.textContent = `${dur.toFixed(1)}s`;
        timingSelect.appendChild(opt);
      });
      
      // Set current value
      const currentTiming = getMockupTiming(id);
      if (currentTiming !== null) {
        timingSelect.value = String(currentTiming);
      } else {
        timingSelect.value = 'auto';
      }
      
      timingGroup.appendChild(timingSelect);
      
      // "Make Longer" button
      const makeInfoBtn = document.createElement('button');
      makeInfoBtn.type = 'button';
      makeInfoBtn.className = 'btn btn-xs btn-outline-secondary chosen-info-btn';
      makeInfoBtn.setAttribute('title', 'Lock to 4.0s');
      makeInfoBtn.textContent = 'Info';
      timingGroup.appendChild(makeInfoBtn);
      
      // Effective time display
      const effectiveDisplay = document.createElement('span');
      effectiveDisplay.className = 'chosen-effective-time';
      effectiveDisplay.textContent = '= Auto';
      timingGroup.appendChild(effectiveDisplay);
      
      // Event handler for timing select change
      const updateTimingAndPersist = async () => {
        if (timingSelect.value === 'auto') {
          setMockupTiming(id, null);
        } else {
          const dur = parseFloat(timingSelect.value);
          setMockupTiming(id, dur);
        }
        updateTimingSummary();
        // Update summary line for this row
        const updatedShot = getShotById(id);
        if (updatedShot && item) {
          updateShotSummaryLine(item, updatedShot);
        }
        await persistTimings();
      };
      
      // Event handler for Info button
      makeInfoBtn.addEventListener('click', async () => {
        setMockupTiming(id, 4.0);
        timingSelect.value = '4.0';
        updateTimingAndPersist();
      });
      
      timingSelect.addEventListener('change', updateTimingAndPersist);
      
      // Add to controls
      controlsBlock.appendChild(timingGroup);

      // Get shot data with backward compatibility
      const shot = getShotById(id);
      
      // Backward compatibility: if pan_direction missing, derive from legacy fields
      let initialPanDirection = 'up'; // default
      if (shot) {
        if (shot.pan_direction) {
          initialPanDirection = shot.pan_direction;
        } else if (shot.pan_to_artwork_center || shot.auto_target) {
          initialPanDirection = 'aim';
        } else if (shot.pan_enabled === false) {
          initialPanDirection = 'none';
        }
      }

      // Create pan direction select with aim option
      const panSelect = document.createElement('select');
      panSelect.className = 'form-select form-select-sm chosen-pan-select';
      panSelect.setAttribute('data-mockup-id', id);
      panSelect.setAttribute('title', 'Pan direction');
      
      const panOptions = [
        { value: 'none', label: 'None' },
        { value: 'aim', label: 'Aim Toward Artwork' },
        { value: 'center', label: 'Center' },
        { value: 'top-left', label: 'Top Left' },
        { value: 'top-right', label: 'Top Right' },
        { value: 'bottom-right', label: 'Bottom Right' },
        { value: 'bottom-left', label: 'Bottom Left' },
        { value: 'up', label: 'Up' },
        { value: 'down', label: 'Down' },
        { value: 'left', label: 'Left' },
        { value: 'right', label: 'Right' }
      ];
      
      panOptions.forEach((option) => {
        const opt = document.createElement('option');
        opt.value = option.value;
        opt.textContent = option.label;
        if (initialPanDirection === option.value) opt.selected = true;
        panSelect.appendChild(opt);
      });

      // Create zoom toggle using new component style
      const { wrapper: zoomToggle, checkbox: zoomCheckbox } = createToggleControl(
        'Zoom Animation',
        shot ? (shot.zoom_enabled !== false) : true,
        id,
        'Enable zoom animation'
      );

      // Create zoom intensity slider
      const { wrapper: zoomSliderWrapper, slider: zoomSlider } = createZoomIntensityControl(
        shot ? (shot.zoom_intensity || 1.1) : 1.1,
        id
      );

      const updateShotAndPersist = async () => {
        setShotById(id, panSelect.value, zoomCheckbox.checked, Number(zoomSlider.value));
        await persistShots();
        // Update summary line in middleSection
        const updatedShot = getShotById(id);
        if (updatedShot) {
          updateShotSummaryLine(middleSection, updatedShot);
        }
      };

      // Real-time summary updates as user interacts (before save)
      const updateSummaryPreview = () => {
        // Create a temporary shot object with current form values
        const previewShot = {
          id,
          pan_enabled: panSelect.value !== 'none',
          pan_direction: panSelect.value,
          zoom_enabled: zoomCheckbox.checked,
          zoom_intensity: Number(zoomSlider.value),
        };
        // Update summary in middleSection where it actually lives
        updateShotSummaryLine(middleSection, previewShot);
      };

      panSelect.addEventListener('change', () => {
        updateSummaryPreview();
        updateShotAndPersist();
      });
      zoomCheckbox.addEventListener('change', () => {
        updateSummaryPreview();
        updateShotAndPersist();
      });
      zoomSlider.addEventListener('input', updateSummaryPreview);
      zoomSlider.addEventListener('change', updateShotAndPersist);

      controlsBlock.appendChild(panSelect);
      controlsBlock.appendChild(zoomToggle);
      controlsBlock.appendChild(zoomSliderWrapper);

      // Create middle section wrapper for controls + info
      const middleSection = document.createElement('div');
      middleSection.className = 'chosen-middle';
      middleSection.appendChild(controlsBlock);
      
      // Add initial summary line to middle section
      if (shot) {
        updateShotSummaryLine(middleSection, shot);
      } else {
        // Also create summary for new shots with defaults
        const defaultShot = {
          id,
          pan_enabled: true,
          pan_direction: 'right',
          zoom_enabled: true,
          zoom_intensity: 1.1,
        };
        updateShotSummaryLine(middleSection, defaultShot);
      }
      
      // Create actions section for remove button
      const actionsSection = document.createElement('div');
      actionsSection.className = 'chosen-actions';
      actionsSection.appendChild(removeBtn);

      thumbWrapper.appendChild(thumb);
      thumbWrapper.appendChild(badge);
      item.appendChild(thumbWrapper);
      item.appendChild(middleSection);
      item.appendChild(actionsSection);
      chosenList.appendChild(item);

      // Track if slider is being interacted with
      let sliderActive = false;
      zoomSlider.addEventListener('pointerdown', () => { sliderActive = true; });
      zoomSlider.addEventListener('pointerup', () => { sliderActive = false; });
      zoomSlider.addEventListener('pointercancel', () => { sliderActive = false; });
      
      item.addEventListener('dragstart', (event) => {
        // Prevent drag if slider is being interacted with
        if (sliderActive || event.target.closest('[data-zoom-slider]')) {
          event.preventDefault();
          return false;
        }
        draggingItem = item;
        item.classList.add('is-dragging');
        event.dataTransfer.effectAllowed = 'move';
        event.dataTransfer.setData('text/plain', id);
      });

      item.addEventListener('dragover', (event) => {
        event.preventDefault();
        if (!draggingItem || draggingItem === item) return;
        const rect = item.getBoundingClientRect();
        const next = (event.clientY - rect.top) > rect.height / 2;
        chosenList.insertBefore(draggingItem, next ? item.nextSibling : item);
      });

      item.addEventListener('drop', (event) => {
        event.preventDefault();
        const ids = Array.from(chosenList.querySelectorAll('[data-mockup-id]'))
          .map((el) => el.dataset.mockupId)
          .filter(Boolean);
        currentOrderIds = ids;
        updateOrderBadges();
        persistOrder();
      });

      item.addEventListener('dragend', () => {
        if (draggingItem) draggingItem.classList.remove('is-dragging');
        draggingItem = null;
        const ids = Array.from(chosenList.querySelectorAll('[data-mockup-id]'))
          .map((el) => el.dataset.mockupId)
          .filter(Boolean);
        currentOrderIds = ids;
        
        // Reorder shots to match new order
        const shotMap = new Map(currentShots.map((shot) => [shot.id, shot]));
        currentShots = ids
          .map((id) => shotMap.get(id))
          .filter((shot) => shot !== undefined);
        
        // Ensure order property matches index
        currentShots.forEach((shot, index) => {
          shot.order = index + 1;
        });
        
        updateOrderBadges();
        persistOrder();
        persistShots(); // Also persist shot order
      });
    });
    
    // Show timing summary bar if there are chosen items
    const timingSummary = root.querySelector('[data-timing-summary]');
    if (timingSummary && availableIds.length > 0) {
      timingSummary.hidden = false;
    }
    
    // Update timing summary
    updateTimingSummary();
    
    // Log completion
    const finalItemCount = chosenList.querySelectorAll('.chosen-item').length;
    log(`renderChosenList completed: ${finalItemCount} items rendered`);
    
    // DEBUG: Verify badges after render
    log('🔍 POST-RENDER BADGE VERIFICATION:');
    chosenList.querySelectorAll('.chosen-item').forEach((item, idx) => {
      const badge = item.querySelector('[data-order-badge]');
      const mockupId = item.dataset.mockupId;
      log(`  Item ${idx}: mockupId=${mockupId}, badge.textContent="${badge ? badge.textContent : 'NO BADGE'}"`);
    });
    
    // Ensure badges are always correct (derived from current order)
    updateOrderBadges();
    
    // Control authority check removed - mockup global controls removed
  };
  
  /**
   * Update control authority indicator
   * When per-mockup controls exist, dim global mockup settings
   */
  // updateControlAuthority removed - mockup global controls removed

  const saveSettings = async () => {
    const payload = {
      video_duration: currentSettings.video_duration,
      artwork_zoom_intensity: currentSettings.artwork_zoom_intensity,
      artwork_zoom_duration: currentSettings.artwork_zoom_duration,
      artwork_pan_enabled: artworkPanToggle.checked,
      artwork_pan_direction: currentSettings.artwork_pan_direction,
      selected_mockups: getSelectedMockups(),
      video_mockup_order: currentOrderIds,
      video_fps: currentSettings.video_fps,
      video_output_size: currentSettings.video_output_size,
      video_encoder_preset: currentSettings.video_encoder_preset,
      video_artwork_source: currentSettings.video_artwork_source,
      video_mockup_shots: currentShots,
      main_artwork_seconds: mainArtworkSeconds,
      video_mockup_timings: videoMockupTimings,
    };
    log('💾 Saving settings with artwork_pan_direction:', payload.artwork_pan_direction);
    if (!settingsUrl) {
      throw new Error('Settings URL not configured');
    }
    const { resp, data, text } = await postJson(settingsUrl, payload);
    if (!resp.ok || data.status !== 'ok') {
      throw new Error(buildErrorMessage('Failed to save settings', resp, data, text));
    }

    // Sync with server-normalized values (response uses nested video_suite contract).
    if (data && data.video_suite && typeof data.video_suite === 'object') {
      Object.assign(persistedVideoSuite, data.video_suite);
      currentSettings.artwork_pan_enabled = readPersistedMainPanEnabled(
        data.video_suite,
        currentSettings.artwork_pan_enabled
      );
      currentSettings.artwork_pan_direction = readPersistedMainPanDirection(
        data.video_suite,
        currentSettings.artwork_pan_direction
      );
      if (artworkPanToggle) artworkPanToggle.checked = currentSettings.artwork_pan_enabled;
      updateArtworkPanStateButtons();
      updateDirectionButtons(artworkPanDirectionBlock, artworkPanDirectionButtons, currentSettings.artwork_pan_direction);
      log('💾 Server-confirmed pan settings:', {
        pan_enabled: currentSettings.artwork_pan_enabled,
        pan_direction: currentSettings.artwork_pan_direction,
      });
    }
    log('💾 Settings saved successfully');
  };

  let saveSettingsTimer = null;
  let saveStatus = null;
  const scheduleSaveSettings = () => {
    if (!settingsUrl) return;
    if (saveSettingsTimer) clearTimeout(saveSettingsTimer);
    saveSettingsTimer = setTimeout(() => {
      saveSettings().catch((err) => {
        log('Auto-save failed:', err);
      });
    }, 600);
    // Show "unsaved changes" indicator
    if (saveStatus) saveStatus.style.display = 'none';
  };

  const deleteVideo = async (ignore404) => {
    if (!deleteUrl) {
      throw new Error('Delete URL not configured');
    }
    const resp = await fetch(deleteUrl, {
      method: 'DELETE',
      headers: {
        ...(csrf ? { 'X-CSRFToken': csrf, 'X-CSRF-Token': csrf } : {}),
        'X-Requested-With': 'XMLHttpRequest',
      },
      credentials: 'same-origin',
    });
    const data = await resp.json().catch(() => ({}));
    if (!resp.ok || data.status !== 'ok') {
      if (ignore404 && resp.status === 404) return;
      throw new Error((data && (data.message || data.error)) || 'Failed to delete video');
    }
  };

  const fetchStatus = async () => {
    if (!statusUrl) return null;
    const resp = await fetch(statusUrl, { credentials: 'same-origin' });
    if (!resp.ok) return null;
    return resp.json();
  };

  const stopPolling = () => {
    if (pollTimer) {
      clearInterval(pollTimer);
      pollTimer = null;
    }
  };

  const pollStatus = async () => {
    const status = await fetchStatus();
    if (!status) return;
    patchStatus(status);
    
    // Show/hide rendering overlay based on status
    if (renderOverlay) {
      if (status.status === 'processing') {
        renderOverlay.hidden = false;
      } else {
        renderOverlay.hidden = true;
      }
    }
    
    if (status.status === 'success' && status.video_url) {
      stopPolling();
      // Update video player with cache-busting and reload
      if (player) {
        const videoUrl = `${status.video_url}${status.video_url.includes('?') ? '&' : '?'}t=${Date.now()}`;
        player.src = videoUrl;
        // Force reload by pausing and playing
        player.load();
        player.pause();
        
          // If traditional reload doesn't work, try reconstructing the element
          player.addEventListener('error', () => {
            // If loading fails, regenerate the entire video element
            const parent = player.parentElement;
            if (parent) {
              const newPlayer = document.createElement('video');
              newPlayer.controls = true;
              newPlayer.preload = 'metadata';
              newPlayer.setAttribute('data-suite-player', '');
              newPlayer.src = videoUrl;
              parent.replaceChild(newPlayer, player);
              // Update root reference if needed
              const updatedPlayer = document.querySelector('[data-suite-player]');
              if (updatedPlayer && player === updatedPlayer) {
                // Player reference still valid
              }
            }
          }, { once: true });
      }
        else {
          // No video element exists - check if there's a placeholder to replace
          const placeholder = root.querySelector('[data-suite-placeholder]');
          const playerWrap = root.querySelector('.suite-player-wrap');
          if (placeholder && playerWrap) {
            // Create and insert video element to replace placeholder
            const videoUrl = `${status.video_url}${status.video_url.includes('?') ? '&' : '?'}t=${Date.now()}`;
            const newPlayer = document.createElement('video');
            newPlayer.controls = true;
            newPlayer.preload = 'metadata';
            newPlayer.setAttribute('data-suite-player', '');
            newPlayer.src = videoUrl;
          
            // Replace placeholder with video
            placeholder.replaceWith(newPlayer);
          }
        }
      if (downloadBtn) downloadBtn.href = status.video_url;
      if (deleteBtn) deleteBtn.disabled = false;
      if (startBtn) startBtn.disabled = false;
    }
    if (status.status === 'error') {
      stopPolling();
      if (startBtn) startBtn.disabled = false;
    }
  };

  // Output settings function (must be defined before initializeFromPersistedSuite)
  const updateOutputWarning = () => {
    if (!outputWarning) return;
    const fps = safeNumber(outputFpsSelect && outputFpsSelect.value, 24);
    const size = safeNumber(outputSizeSelect && outputSizeSelect.value, 1024);
    // Show warning if fps=60 AND size>=1920
    outputWarning.hidden = !(fps >= 60 && size >= 1920);
  };

  // Initialize UI from persisted suite settings
  const initializeFromPersistedSuite = () => {
    // Duration - use persisted value if available
    if (persistedVideoSuite.video_duration) {
      setDuration(persistedVideoSuite.video_duration);
    }

    // Artwork seconds (main artwork duration)
    if (persistedVideoSuite.main_artwork_seconds) {
      mainArtworkSeconds = safeNumber(persistedVideoSuite.main_artwork_seconds, 4.0);
      if (artworkSecondsInput) artworkSecondsInput.value = mainArtworkSeconds;
      if (artworkSecondsValue) artworkSecondsValue.textContent = `${mainArtworkSeconds.toFixed(1)}s`;
      if (timingMainSecondsInput) timingMainSecondsInput.value = mainArtworkSeconds;
    }

    // Artwork zoom
    if (artworkZoomIntensityInput && persistedVideoSuite.artwork_zoom_intensity) {
      artworkZoomIntensityInput.value = persistedVideoSuite.artwork_zoom_intensity;
      updateArtworkZoomIntensity();
    }
    if (artworkZoomDurationInput && persistedVideoSuite.artwork_zoom_duration) {
      artworkZoomDurationInput.value = persistedVideoSuite.artwork_zoom_duration;
      updateArtworkZoomDuration();
    }

    // Artwork pan
    const persistedMainPanEnabled = readPersistedMainPanEnabled(
      persistedVideoSuite,
      currentSettings.artwork_pan_enabled
    );
    if (artworkPanToggle) {
      artworkPanToggle.checked = persistedMainPanEnabled;
      currentSettings.artwork_pan_enabled = persistedMainPanEnabled;
      updateArtworkPanStateButtons();
    }
    const persistedMainPanDirection = readPersistedMainPanDirection(
      persistedVideoSuite,
      currentSettings.artwork_pan_direction
    );
    currentSettings.artwork_pan_direction = persistedMainPanDirection;
    updateDirectionButtons(artworkPanDirectionBlock, artworkPanDirectionButtons, persistedMainPanDirection);



    // Output settings
    if (outputFpsSelect && persistedVideoSuite.video_fps) {
      outputFpsSelect.value = persistedVideoSuite.video_fps;
    }
    if (outputSizeSelect && persistedVideoSuite.video_output_size) {
      outputSizeSelect.value = persistedVideoSuite.video_output_size;
    }
    if (outputPresetSelect && persistedVideoSuite.video_encoder_preset) {
      outputPresetSelect.value = persistedVideoSuite.video_encoder_preset;
    }
    if (outputSourceSelect && persistedVideoSuite.video_artwork_source) {
      outputSourceSelect.value = persistedVideoSuite.video_artwork_source;
    }
    updateOutputWarning();

    // Restore mockup selection from persisted state
    // Use selected_mockups (which reflects actual user selection) not video_mockup_order (which is just ordering)
    const savedSelectedMockups = persistedVideoSuite.selected_mockups;
    if (savedSelectedMockups && Array.isArray(savedSelectedMockups) && savedSelectedMockups.length > 0) {
      const selectedSet = new Set(savedSelectedMockups);
      
      mockupCards.forEach((card) => {
        const filename = card.dataset.filename;
        const checkbox = card.querySelector('[data-storyboard-checkbox]');
        if (checkbox) {
          // Check if this mockup's filename is in the saved selection
          checkbox.checked = selectedSet.has(filename);
        }
      });
      
      log('Restored mockup checkboxes from saved selection:', Array.from(selectedSet));
    }

    // Restore per-mockup shots settings (pan_direction, zoom_enabled, zoom_intensity)
    if (persistedVideoSuite.video_mockup_shots && Array.isArray(persistedVideoSuite.video_mockup_shots)) {
      currentShots = persistedVideoSuite.video_mockup_shots.map(shot => ({
        id: shot.id,
        pan_enabled: shot.pan_enabled !== undefined ? Boolean(shot.pan_enabled) : true,
        pan_direction: shot.pan_direction || 'up',
        zoom_enabled: shot.zoom_enabled !== undefined ? Boolean(shot.zoom_enabled) : true,
        zoom_intensity: shot.zoom_intensity !== undefined ? Number(shot.zoom_intensity) : 1.1,
        pan_to_artwork_center: Boolean(shot.pan_to_artwork_center),
        auto_target: Boolean(shot.auto_target),
        order: shot.order,
      }));
      log('Restored per-mockup shots:', currentShots);
    }

    // Restore per-mockup timings
    if (persistedVideoSuite.video_mockup_timings && typeof persistedVideoSuite.video_mockup_timings === 'object') {
      videoMockupTimings = persistedVideoSuite.video_mockup_timings;
      log('Restored per-mockup timings:', videoMockupTimings);
    }
  };

  // Call initialization with verification logging
  log('Initialization sequence starting...');
  log(`mockupCards: ${mockupCards.length} total`);
  log('First 3 mockupCards inspected:', mockupCards.slice(0, 3).map(card => ({
    id: getCardMockupId(card),
    classes: card.className,
    dataAttrs: { mockupId: card.dataset.mockupId, filename: card.dataset.filename }
  })));
  log(`mockupMap: ${mockupMap.size} entries`, Array.from(mockupMap.keys()).slice(0, 5));
  log(`storedAutoIds: ${storedAutoIds.length} entries`, storedAutoIds);
  log('DOM elements:', {
    chosenPanel: !!chosenPanel,
    chosenList: !!chosenList,
    chosenTitle: !!chosenTitle,
    chosenSubtitle: !!chosenSubtitle,
    chosenEmpty: !!chosenEmpty,
    chosenNoMockups: !!chosenNoMockups,
    storyboardGrid: !!storyboardGrid,
  });
  
  updateStoryboardCounter();
  
  // DEBUG: Log state before renderChosenList (FIXED: no auto-select)
  const selectedIds = getSelectedIds();
  log(`Before renderChosenList:`, {
    selectedCount: selectedIds.length,
    maxLimit: MAX_MOCKUPS,
    willShowEmpty: selectedIds.length === 0,
  });
  
  renderChosenList();
  
  // DEBUG: Log state after renderChosenList
  const chosenItemsCount = chosenList ? chosenList.querySelectorAll('.chosen-item').length : 0;
  log(`After renderChosenList: ${chosenItemsCount} items rendered, maxLimit=${MAX_MOCKUPS}`);
  
  attachStoryboardCheckboxListeners();

  // Add Save button to UI
  const saveButton = document.createElement('button');
  saveButton.type = 'button';
  saveButton.className = 'btn btn-primary btn-sm';
  saveButton.textContent = '💾 Save Settings';
  saveButton.title = 'Save all video suite settings';
  
  saveStatus = document.createElement('span');
  saveStatus.style.cssText = 'display: none; color: #28a745; font-size: 12px; margin-left: 8px;';
  saveStatus.textContent = '✓ Saved';
  
  const saveButtonContainer = document.createElement('div');
  saveButtonContainer.style.cssText = 'display: flex; align-items: center; gap: 8px; margin-bottom: 12px;';
  saveButtonContainer.appendChild(saveButton);
  saveButtonContainer.appendChild(saveStatus);
  
  const showSavedStatus = () => {
    saveStatus.style.display = 'inline';
    clearTimeout(saveStatus.hideTimer);
    saveStatus.hideTimer = setTimeout(() => {
      saveStatus.style.display = 'none';
    }, 2000);
  };
  
  saveButton.addEventListener('click', async () => {
    try {
      saveButton.disabled = true;
      saveButton.textContent = '⏳ Saving...';
      await saveSettings();
      saveButton.textContent = '💾 Save Settings';
      showSavedStatus();
    } catch (err) {
      saveButton.textContent = '❌ Save Failed';
      log('Save failed:', err);
      setTimeout(() => {
        saveButton.textContent = '💾 Save Settings';
      }, 2000);
    } finally {
      saveButton.disabled = false;
    }
  });
  
  // Insert save button before duration buttons
  if (durationButtonsWrap) {
    durationButtonsWrap.parentNode.insertBefore(saveButtonContainer, durationButtonsWrap);
  }

  // Event listeners
  if (durationButtonsWrap) {
    durationButtonsWrap.querySelectorAll('[data-duration-value]').forEach((btn) => {
      btn.addEventListener('click', () => {
        setDuration(Number(btn.dataset.durationValue));
        scheduleSaveSettings();
      });
    });
  }

  if (artworkZoomIntensityInput) {
    artworkZoomIntensityInput.addEventListener('input', () => {
      updateArtworkZoomIntensity();
      scheduleSaveSettings();
    });
  }
  if (artworkZoomDurationInput) {
    artworkZoomDurationInput.addEventListener('input', () => {
      updateArtworkZoomDuration();
      scheduleSaveSettings();
    });
  }
  // Mockup controls removed - use per-mockup controls

  // Main artwork seconds control
  const artworkSecondsInput = root.querySelector('[data-artwork-seconds]');
  const artworkSecondsValue = root.querySelector('[data-artwork-seconds-value]');
  const timingMainSecondsInput = root.querySelector('[data-timing-main-seconds]');
  
  const updateArtworkSeconds = async () => {
    const val = Math.max(1.0, Math.min(10.0, Number(artworkSecondsInput.value) || 4.0));
    mainArtworkSeconds = Math.round(val * 2) / 2; // Round to 0.5
    
    if (artworkSecondsValue) artworkSecondsValue.textContent = `${mainArtworkSeconds.toFixed(1)}s`;
    if (timingMainSecondsInput) timingMainSecondsInput.value = mainArtworkSeconds;
    
    updateTimingSummary();
    updateAllSummaryLines();
    await persistTimings();
  };
  
  if (artworkSecondsInput) {
    artworkSecondsInput.addEventListener('input', updateArtworkSeconds);
  }
  
  if (timingMainSecondsInput) {
    timingMainSecondsInput.addEventListener('change', async () => {
      const val = Math.max(1.0, Math.min(10.0, Number(timingMainSecondsInput.value) || 4.0));
      mainArtworkSeconds = Math.round(val * 2) / 2;
      
      if (artworkSecondsInput) artworkSecondsInput.value = mainArtworkSeconds;
      if (artworkSecondsValue) artworkSecondsValue.textContent = `${mainArtworkSeconds.toFixed(1)}s`;
      
      updateTimingSummary();
      await persistTimings();
    });
  }

  if (artworkPanToggle) {
    artworkPanToggle.addEventListener('change', () => {
      currentSettings.artwork_pan_enabled = artworkPanToggle.checked;
      updateArtworkPanStateButtons();
      scheduleSaveSettings();
    });
  }

  // Mockup pan controls removed - use per-mockup controls

  if (artworkPanDirectionButtons) {
    artworkPanDirectionButtons.querySelectorAll('[data-direction]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const newDirection = btn.dataset.direction;
        log(`📍 Pan direction button clicked: ${newDirection}`);
        currentSettings.artwork_pan_direction = newDirection;
        updateDirectionButtons(artworkPanDirectionBlock, artworkPanDirectionButtons, currentSettings.artwork_pan_direction);
        log(`📍 Button states updated. currentSettings.artwork_pan_direction = ${currentSettings.artwork_pan_direction}`);
        scheduleSaveSettings();
      });
    });
  }

  // Mockup pan direction controls removed - use per-mockup controls

  // Output settings event handlers
  if (outputFpsSelect) {
    outputFpsSelect.addEventListener('change', () => {
      currentSettings.video_fps = safeNumber(outputFpsSelect.value, 24);
      updateOutputWarning();
      scheduleSaveSettings();
    });
  }

  if (outputSizeSelect) {
    outputSizeSelect.addEventListener('change', () => {
      currentSettings.video_output_size = safeNumber(outputSizeSelect.value, 1024);
      updateOutputWarning();
      scheduleSaveSettings();
    });
  }

  if (outputPresetSelect) {
    outputPresetSelect.addEventListener('change', () => {
      currentSettings.video_encoder_preset = outputPresetSelect.value ? String(outputPresetSelect.value) : 'fast';
      scheduleSaveSettings();
    });
  }

  if (outputSourceSelect) {
    outputSourceSelect.addEventListener('change', () => {
      currentSettings.video_artwork_source = outputSourceSelect.value ? String(outputSourceSelect.value) : 'auto';
      scheduleSaveSettings();
    });
  }

  root.querySelectorAll('[data-preset]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const preset = btn.dataset.preset;
      if (preset === 'minimal') {
        artworkZoomIntensityInput.value = '1.05';
        artworkPanToggle.checked = false;
        setDuration(15);
      } else if (preset === 'commercial') {
        artworkZoomIntensityInput.value = '1.20';
        artworkPanToggle.checked = true;
        setDuration(10);
      } else if (preset === 'social') {
        artworkZoomIntensityInput.value = '1.30';
        artworkPanToggle.checked = true;
        setDuration(10);
      }
      updateArtworkZoomIntensity();
      updateArtworkPanStateButtons();
      scheduleSaveSettings();
    });
  });

  startBtn.addEventListener('click', async () => {
    startBtn.disabled = true;
    startBtn.textContent = 'RENDERING...';
    try {
      await saveSettings();
      await deleteVideo(true);
      if (!generateUrl) {
        throw new Error('Generate URL not configured');
      }
      const { resp, data, text } = await postJson(generateUrl, { selected_mockups: getSelectedMockups() });
      if (!resp.ok || data.status !== 'ok') {
        throw new Error(buildErrorMessage('Failed to start render', resp, data, text));
      }
      // Show rendering overlay
      if (renderOverlay) renderOverlay.hidden = false;
      patchStatus({ stage: 'initializing', percent: 0, message: 'Queued' });
      await pollStatus();
      pollTimer = setInterval(pollStatus, 1500);
    } catch (err) {
      patchStatus({ stage: 'error', percent: 100, message: err && err.message ? err.message : 'Render failed' });
      startBtn.disabled = false;
      // Hide overlay on error
      if (renderOverlay) renderOverlay.hidden = true;
    } finally {
      startBtn.textContent = 'START RENDER';
    }
  });

  if (storyboardGrid) {
    attachStoryboardCheckboxListeners();
    storyboardGrid.querySelectorAll('[data-storyboard-item]').forEach((card) => {
      const swapBtn = card.querySelector('[data-storyboard-swap]');
      const categorySelect = card.querySelector('[data-storyboard-category]');
      const thumbEl = card.querySelector('[data-storyboard-thumb]');

      if (categorySelect) {
        categorySelect.addEventListener('change', async () => {
          categorySelect.disabled = true;
          try {
            const category = categorySelect.value;
            const { resp, data, text } = await postJson(card.dataset.categoryUrl, { category });
            if (!resp.ok || data.status !== 'ok') {
              throw new Error(buildErrorMessage('Category update failed', resp, data, text));
            }
          } catch (err) {
            patchStatus({ stage: 'error', percent: 100, message: err && err.message ? err.message : 'Category update failed' });
          } finally {
            categorySelect.disabled = false;
          }
        });
      }

      if (swapBtn) {
        swapBtn.addEventListener('click', async () => {
          swapBtn.disabled = true;
          try {
            const category = categorySelect ? categorySelect.value : '';
            const { resp, data, text } = await postJson(card.dataset.swapUrl, { category });
            if (!resp.ok || data.status !== 'ok') {
              throw new Error(buildErrorMessage('Swap failed', resp, data, text));
            }
            if (thumbEl && data.thumb_url) {
              thumbEl.src = `${data.thumb_url}${data.thumb_url.includes('?') ? '&' : '?'}t=${Date.now()}`;
            }
          } catch (err) {
            patchStatus({ stage: 'error', percent: 100, message: err && err.message ? err.message : 'Swap failed' });
          } finally {
            swapBtn.disabled = false;
          }
        });
      }
    });
  }

  if (deleteBtn) deleteBtn.addEventListener('click', async () => {
    const ok = window.confirm('Delete generated video?');
    if (!ok) return;
    deleteBtn.disabled = true;
    try {
      await deleteVideo(false);
      if (player) player.removeAttribute('src');
      if (downloadBtn) downloadBtn.href = '#';
    } catch (_err) {
      deleteBtn.disabled = false;
    }
  });

  // Initialize
  setDuration(duration);
  updateArtworkZoomIntensity();
  updateArtworkPanStateButtons();
  updateOutputWarning();
  attachStoryboardCheckboxListeners();
  
  // Initialize from persisted settings (after all DOM elements are ready)
  initializeFromPersistedSuite();
  
  // CRITICAL: Always sync button states after loading settings
  // This ensures buttons reflect the loaded/default direction even if not in persisted data
  updateDirectionButtons(artworkPanDirectionBlock, artworkPanDirectionButtons, currentSettings.artwork_pan_direction);
  log(`Pan direction buttons synced to: ${currentSettings.artwork_pan_direction}`);
  
  // After loading persisted settings, render the chosen list with restored per-mockup settings
  log('Rendering chosen list after loading persisted settings...');
  renderChosenList();
  updateChosenPanel();
  updateTimingSummary();
  
  fetchStatus().then((status) => {
    if (status) {
      patchStatus(status);
      if (status.status !== 'processing' && statusBox) statusBox.hidden = true;
      if (renderOverlay) {
        renderOverlay.hidden = status.status !== 'processing';
      }
      if (status.status === 'processing' && !pollTimer) {
        pollStatus();
        pollTimer = setInterval(pollStatus, 1500);
      }
      if (status.has_video && status.video_url) {
        if (downloadBtn) downloadBtn.href = status.video_url;
        if (deleteBtn) deleteBtn.disabled = false;
        if (player) player.src = `${status.video_url}${status.video_url.includes('?') ? '&' : '?'}t=${Date.now()}`;
      }
    }
  }).catch(() => { });
})();
