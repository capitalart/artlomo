document.addEventListener('DOMContentLoaded', () => {
  const workspace = document.querySelector('#darkroom-workspace');
  if (!workspace) return;

  const importBtn = document.querySelector('#darkroom-import-btn');
  const importInput = document.querySelector('#darkroom-import-input');
  const exportBtn = document.querySelector('#darkroom-export-btn');

  workspace.innerHTML = [
    '<form method="post" class="theme-form" novalidate>',
    '  <div class="theme-form__field">',
    '    <label class="form-label">Preset library</label>',
    '    <div data-preset-cards style="display:grid; gap: 10px;"></div>',
    '  </div>',
    '  <div class="theme-form__field">',
    '    <label class="form-label">Selected preset</label>',
    '    <div class="artlomo-data-card" data-selected-preset>None selected</div>',
    '  </div>',
    '  <div class="theme-form__field">',
    '    <label class="form-label">Preset name</label>',
    '    <input class="form-control" type="text" name="theme_name" value="default" required>',
    '  </div>',
    '  <div class="darkroom-panes" data-darkroom-panes>',
    '    <div class="darkroom-pane" data-theme-pane="light">',
    '      <div class="darkroom-pane__title">Light</div>',
    '      <div class="darkroom-pane__fields" data-theme-fields="light"></div>',
    '    </div>',
    '    <div class="darkroom-pane" data-theme-pane="dark">',
    '      <div class="darkroom-pane__title">Dark</div>',
    '      <div class="darkroom-pane__fields" data-theme-fields="dark"></div>',
    '    </div>',
    '  </div>',
    '  <div class="theme-form__field">',
    '    <label class="form-label">Custom CSS Override</label>',
    '    <textarea class="form-control" rows="8" data-custom-css></textarea>',
    '  </div>',
    '  <div class="theme-form__actions">',
    '    <button class="artlomo-btn" type="button" data-load-preset>SWITCH TO PRESET</button>',
    '    <button class="artlomo-btn artlomo-btn--save" type="submit">Save preset</button>',
    '    <button class="artlomo-btn artlomo-btn--save" type="button" data-save-as-new hidden>Save as New Copy</button>',
    '    <button class="artlomo-btn artlomo-btn--danger" type="button" data-delete-preset>Delete preset</button>',
    '    <button class="artlomo-btn" type="button" data-preview-light>Preview Light</button>',
    '    <button class="artlomo-btn" type="button" data-preview-dark>Preview Dark</button>',
    '    <button class="artlomo-btn" type="button" data-reset>Reset</button>',
    '    <a class="artlomo-btn" href="/admin/hub/">Back to Hub</a>',
    '  </div>',
    '</form>',
  ].join('\n');

  const form = workspace.querySelector('.theme-form');
  if (!form) return;
  const presetCardsHost = form.querySelector('[data-preset-cards]');
  const selectedPresetHost = form.querySelector('[data-selected-preset]');
  const loadBtn = form.querySelector('[data-load-preset]');
  const saveAsNewBtn = form.querySelector('[data-save-as-new]');
  const deleteBtn = form.querySelector('[data-delete-preset]');
  const nameInput = form.querySelector('input[name="theme_name"]');
  const previewLightBtn = form.querySelector('[data-preview-light]');
  const previewDarkBtn = form.querySelector('[data-preview-dark]');
  const resetBtn = form.querySelector('[data-reset]');
  const lightFieldsHost = form.querySelector('[data-theme-fields="light"]');
  const darkFieldsHost = form.querySelector('[data-theme-fields="dark"]');
  const customCssInput = form.querySelector('[data-custom-css]');

  const customCssStyle = (() => {
    const existing = document.querySelector('#darkroom-custom-css-preview');
    if (existing) return existing;
    const el = document.createElement('style');
    el.id = 'darkroom-custom-css-preview';
    document.head.appendChild(el);
    return el;
  })();

  let DEFAULTS = {};
  let bootPreset = {};
  let lastLoadedPreset = {};
  let selectedPresetKey = '';
  let selectedPresetMeta = null;

  const escapeHtml = (txt) => {
    const v = txt === null || txt === undefined ? '' : String(txt);
    return v.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  };

  const updateDeleteButtonState = () => {
    if (!deleteBtn) return;
    if (!selectedPresetMeta) {
      deleteBtn.disabled = true;
      deleteBtn.title = 'Select a preset to delete';
      return;
    }
    const folder = (selectedPresetMeta.folder || '').toString().toLowerCase();
    const name = (selectedPresetMeta.name || '').toString().toLowerCase();
    if (folder !== 'user' && folder !== 'root') {
      deleteBtn.disabled = true;
      deleteBtn.title = 'Only user or root presets can be deleted';
      return;
    }
    if (name === 'default') {
      deleteBtn.disabled = true;
      deleteBtn.title = 'The default preset cannot be deleted';
      return;
    }
    deleteBtn.disabled = false;
    deleteBtn.title = '';
  };

  const setSelectedPresetCard = (meta) => {
    selectedPresetMeta = meta;
    selectedPresetKey = meta ? meta.key : '';

    if (presetCardsHost) {
      Array.from(presetCardsHost.querySelectorAll('[data-preset-card]')).forEach((btn) => {
        const key = (btn.getAttribute('data-preset-card') || '').trim();
        if (key && key === selectedPresetKey) {
          btn.classList.add('is-selected');
        } else {
          btn.classList.remove('is-selected');
        }
      });
    }

    if (selectedPresetHost) {
      if (!meta) {
        selectedPresetHost.innerHTML = 'None selected';
      } else {
        const lines = [
          `<strong>${escapeHtml(meta.name)}</strong>`,
          escapeHtml(meta.label),
        ];
        selectedPresetHost.innerHTML = lines.join('<br>');
      }
    }

    updateDeleteButtonState();
  };

  const getCsrf = () => {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? (meta.getAttribute('content') || '').trim() : '';
  };

  const normalizeTwinPreset = (preset) => {
    if (!preset || typeof preset !== 'object') {
      return { name: 'default', light: {}, dark: {}, custom_css: '' };
    }
    const hasTwin = (preset.light && typeof preset.light === 'object') || (preset.dark && typeof preset.dark === 'object');
    if (hasTwin) {
      return {
        name: preset.name || 'default',
        folder: preset.folder,
        saved_at: preset.saved_at,
        light: preset.light || {},
        dark: preset.dark || {},
        custom_css: typeof preset.custom_css === 'string' ? preset.custom_css : '',
      };
    }
    return {
      name: preset.name || 'default',
      folder: preset.folder,
      saved_at: preset.saved_at,
      light: preset,
      dark: {},
      custom_css: typeof preset.custom_css === 'string' ? preset.custom_css : '',
    };
  };

  const applyCustomCss = (cssText) => {
    if (!customCssStyle) return;
    customCssStyle.textContent = typeof cssText === 'string' ? cssText : '';
  };

  const buildPresetCss = (twin) => {
    const p = normalizeTwinPreset(twin);
    const block = (theme, values) => {
      const get = (k) => {
        const v = values && values[k] !== undefined && values[k] !== null ? String(values[k]) : '';
        return v || (DEFAULTS && DEFAULTS[k] ? String(DEFAULTS[k]) : '');
      };

      const accent = get('accent_color');
      const background = get('background_color');
      const cardBackground = get('card_background');
      const text = get('text_color');
      const textSecondary = get('text_secondary');
      const fontFamily = get('font_family');
      const fontHeading = get('font_heading');
      const baseFontSize = get('base_font_size');
      const cardRadius = get('card_radius');
      const borderColor = get('border_color');
      const borderWidth = get('border_width');
      const gridGap = get('grid_gap');
      const letterSpacingHeading = get('letter_spacing_heading');
      const buttonPadding = get('button_padding');
      const btnText = get('artlomo_btn_text');
      const btnBg = get('artlomo_btn_bg');
      const btnShadow = get('artlomo_btn_shadow');
      const btnHoverBg = get('artlomo_btn_hover_bg') || accent;
      const btnHoverText = get('artlomo_btn_hover_text');
      const saveBg = get('artlomo_save_bg') || accent;
      const saveText = get('artlomo_save_text');
      const danger = get('danger_color') || get('artlomo_danger');
      const lockBorderLight = get('artlomo_lock_border_light');
      const lockBorderDark = get('artlomo_lock_border_dark');

      const lines = [
        `html[data-theme="${theme}"] {`,
        `  --color-bg-primary: ${background};`,
        `  --color-background: ${background};`,
        `  --color-card-bg: ${cardBackground};`,
        `  --color-text: ${text};`,
        `  --color-text-primary: ${text};`,
        `  --color-border-primary: ${borderColor};`,
        `  --color-border-subtle: ${borderColor};`,
        `  --color-action-danger: ${danger};`,
        `  --bg-body: var(--color-background);`,
        `  --bg-secondary: var(--card-bg);`,
        `  --text-primary: var(--color-text);`,
        `  --card-bg: var(--color-card-bg);`,
        `  --card-text: var(--color-text);`,
        `  --button-bg: var(--color-border-primary);`,
        `  --button-text: var(--color-bg-primary);`,
        `  --header-bg: ${background};`,
        `  --overlay-surface: var(--color-bg-primary);`,
        `  --button-danger-bg: var(--color-action-danger);`,
        `  --checkbox-accent: var(--color-action-danger);`,
        `  --artlomo-accent: ${accent};`,
        `  --accent-color: ${accent};`,
        `  --font-family-main: ${fontFamily};`,
        `  --font-primary: ${fontFamily};`,
        `  --font-heading: ${fontHeading};`,
        `  --base-font-size: ${baseFontSize};`,
        `  --card-radius: ${cardRadius};`,
        `  --border-color: ${borderColor};`,
        `  --border-width: ${borderWidth};`,
        `  --grid-gap: ${gridGap};`,
        `  --letter-spacing-heading: ${letterSpacingHeading};`,
        `  --text-secondary: ${textSecondary};`,
        `  --button-padding: ${buttonPadding};`,
        `  --artlomo-btn-text: ${btnText};`,
        `  --artlomo-btn-bg: ${btnBg};`,
        `  --artlomo-btn-shadow: ${btnShadow};`,
        `  --artlomo-btn-hover-bg: ${btnHoverBg};`,
        `  --artlomo-btn-hover-text: ${btnHoverText};`,
        `  --artlomo-save-bg: ${saveBg};`,
        `  --artlomo-save-text: ${saveText};`,
        `  --artlomo-danger: ${danger};`,
        `  --artlomo-lock-border-light: ${lockBorderLight};`,
        `  --artlomo-lock-border-dark: ${lockBorderDark};`,
        '}',
      ];
      return lines.join('\n');
    };

    const cssParts = [block('light', p.light || {}), '', block('dark', p.dark || {})];
    const custom = typeof p.custom_css === 'string' ? p.custom_css.trim() : '';
    if (custom) {
      cssParts.push('', custom);
    }
    return cssParts.join('\n');
  };

  const downloadJsonFile = (filename, obj) => {
    const content = JSON.stringify(obj, null, 2);
    const blob = new Blob([content], { type: 'application/json;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 500);
  };

  const isColorValue = (val) => typeof val === 'string' && /^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/.test(val.trim());

  const buildFieldRow = ({ theme, key, label, value }) => {
    const isColor = isColorValue(value);
    const inputType = isColor ? 'color' : 'text';
    const name = `${theme}__${key}`;
    const safeLabel = label || key.replace(/_/g, ' ');
    const safeValue = value === null || value === undefined ? '' : String(value);
    return [
      '<div class="theme-form__field">',
      `  <label class="form-label">${safeLabel}</label>`,
      `  <input class="form-control${isColor ? ' form-control-color' : ''}" type="${inputType}" name="${name}" value="${safeValue.replace(/"/g, '&quot;')}">`,
      '</div>',
    ].join('\n');
  };

  const GROUPS = [
    {
      title: 'CORE PALETTE',
      keys: ['background_color', 'text_color', 'accent_color', 'danger_color'],
    },
    {
      title: 'SURFACE & BORDERS',
      keys: ['card_background', 'border_color', 'border_width', 'grid_gap'],
    },
    {
      title: 'TYPOGRAPHY',
      keys: ['font_family', 'font_heading', 'base_font_size', 'letter_spacing_heading'],
    },
    {
      title: 'BUTTON ACTIONS',
      keys: ['artlomo_btn_bg', 'artlomo_btn_text', 'artlomo_btn_shadow', 'artlomo_btn_hover_bg', 'artlomo_btn_hover_text', 'artlomo_save_bg', 'artlomo_save_text', 'button_padding'],
    },
  ];

  const renderThemePane = (theme, host, values) => {
    if (!host) return;
    const v = values && typeof values === 'object' ? values : {};

    const known = new Set();
    GROUPS.forEach((g) => (g.keys || []).forEach((k) => known.add(k)));
    const leftovers = Object.keys(DEFAULTS).filter((k) => !known.has(k));

    const groups = GROUPS.map((g) => ({ title: g.title, keys: [...(g.keys || [])] }));
    if (leftovers.length) {
      groups[0].keys = [...groups[0].keys, ...leftovers];
    }

    const sectionsHtml = groups.map((group) => {
      const fields = (group.keys || []).filter((k) => Object.prototype.hasOwnProperty.call(DEFAULTS, k));
      const fieldsHtml = fields.map((key) => {
        const val = v[key] !== undefined && v[key] !== null && String(v[key]).length ? v[key] : DEFAULTS[key];
        return buildFieldRow({ theme, key, label: key.replace(/_/g, ' '), value: val });
      }).join('\n');
      return [
        '<div class="darkroom-section">',
        `  <div class="darkroom-section__title">${escapeHtml(group.title)}</div>`,
        `  <div class="darkroom-section__fields">${fieldsHtml}</div>`,
        '</div>',
      ].join('\n');
    }).join('\n');

    host.innerHTML = sectionsHtml;
  };

  const setFormValues = (preset) => {
    const twin = normalizeTwinPreset(preset);
    if (nameInput) nameInput.value = twin.name || 'default';
    renderThemePane('light', lightFieldsHost, twin.light);
    renderThemePane('dark', darkFieldsHost, twin.dark);
    if (customCssInput) customCssInput.value = twin.custom_css || '';
    applyCustomCss(twin.custom_css || '');
  };

  const parseImportedPreset = (raw, fallbackName) => {
    if (!raw || typeof raw !== 'object') {
      return { name: fallbackName || 'imported', light: {}, dark: {}, custom_css: '' };
    }

    const readCss = () => {
      const candidates = [
        raw.custom_css,
        raw.customCss,
        raw.css_override,
        raw.override_css,
        raw.css,
      ];
      for (let i = 0; i < candidates.length; i += 1) {
        if (typeof candidates[i] === 'string') return candidates[i];
      }
      return '';
    };

    const cssText = readCss();

    if ((raw.light && typeof raw.light === 'object') || (raw.dark && typeof raw.dark === 'object')) {
      return {
        name: raw.name || fallbackName || 'imported',
        light: (raw.light && typeof raw.light === 'object') ? raw.light : {},
        dark: (raw.dark && typeof raw.dark === 'object') ? raw.dark : {},
        custom_css: cssText,
      };
    }

    return {
      name: raw.name || fallbackName || 'imported',
      light: raw,
      dark: raw,
      custom_css: cssText,
    };
  };

  const collectThemeValues = (theme) => {
    const out = {};
    const selector = `[name^="${theme}__"]`;
    Array.from(form.querySelectorAll(selector)).forEach((el) => {
      const raw = (el.getAttribute('name') || '').trim();
      const key = raw.replace(`${theme}__`, '');
      if (!key) return;
      out[key] = (el.value || '').toString();
    });
    return out;
  };

  const collectTwinPayload = (mode) => {
    const rawName = nameInput ? (nameInput.value || '').trim() : '';
    return {
      name: rawName,
      mode: mode || 'save',
      light: collectThemeValues('light'),
      dark: collectThemeValues('dark'),
      custom_css: customCssInput ? (customCssInput.value || '') : '',
    };
  };

  const applyPreviewValues = (values) => {
    if (!values) return;
    const root = document.documentElement;

    const get = (k) => {
      const v = values[k];
      return v === null || v === undefined ? '' : String(v);
    };

    const accent = get('accent_color');
    const background = get('background_color');
    const cardBackground = get('card_background');
    const text = get('text_color');
    const textSecondary = get('text_secondary');
    const fontFamily = get('font_family');
    const fontHeading = get('font_heading');
    const baseFontSize = get('base_font_size');
    const cardRadius = get('card_radius');
    const borderColor = get('border_color');
    const borderWidth = get('border_width');
    const gridGap = get('grid_gap');
    const letterSpacingHeading = get('letter_spacing_heading');
    const buttonPadding = get('button_padding');
    const btnText = get('artlomo_btn_text');
    const btnBg = get('artlomo_btn_bg');
    const btnShadow = get('artlomo_btn_shadow');
    const btnHoverBg = get('artlomo_btn_hover_bg') || accent;
    const btnHoverText = get('artlomo_btn_hover_text');
    const saveBg = get('artlomo_save_bg') || accent;
    const saveText = get('artlomo_save_text');
    const danger = get('danger_color') || get('artlomo_danger');
    const lockBorderLight = get('artlomo_lock_border_light');
    const lockBorderDark = get('artlomo_lock_border_dark');

    const props = {
      '--color-bg-primary': background,
      '--color-background': background,
      '--color-card-bg': cardBackground,
      '--color-text': text,
      '--color-text-primary': text,
      '--color-border-primary': borderColor,
      '--color-border-subtle': borderColor,
      '--color-action-danger': danger,
      '--header-bg': background,
      '--artlomo-accent': accent,
      '--accent-color': accent,
      '--font-family-main': fontFamily,
      '--font-primary': fontFamily,
      '--font-heading': fontHeading,
      '--base-font-size': baseFontSize,
      '--card-radius': cardRadius,
      '--border-color': borderColor,
      '--border-width': borderWidth,
      '--grid-gap': gridGap,
      '--letter-spacing-heading': letterSpacingHeading,
      '--text-secondary': textSecondary,
      '--button-padding': buttonPadding,
      '--artlomo-btn-text': btnText,
      '--artlomo-btn-bg': btnBg,
      '--artlomo-btn-shadow': btnShadow,
      '--artlomo-btn-hover-bg': btnHoverBg,
      '--artlomo-btn-hover-text': btnHoverText,
      '--artlomo-save-bg': saveBg,
      '--artlomo-save-text': saveText,
      '--artlomo-danger': danger,
      '--artlomo-lock-border-light': lockBorderLight,
      '--artlomo-lock-border-dark': lockBorderDark,
    };

    Object.keys(props).forEach((key) => {
      const val = props[key];
      if (val) root.style.setProperty(key, val);
    });

  };

  const previewTheme = (theme) => {
    const values = collectThemeValues(theme);
    applyPreviewValues(values);
    document.documentElement.setAttribute('data-theme', theme);
    try {
      localStorage.setItem('theme', theme);
    } catch (e) {
      // ignore
    }
  };

  const isDarkroomControl = (el) => {
    if (!el) return false;
    const cls = (el.getAttribute && el.getAttribute('class')) || '';
    if (cls && cls.indexOf('form-control') >= 0) return true;
    return false;
  };

  const getActiveTheme = () => {
    const theme = (document.documentElement.getAttribute('data-theme') || 'light').trim() || 'light';
    return theme === 'dark' ? 'dark' : 'light';
  };

  const postJson = async (url, payload) => {
    const csrf = getCsrf();
    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    if (csrf) headers['X-CSRFToken'] = csrf;
    const resp = await fetch(url, {
      method: 'POST',
      headers,
      credentials: 'same-origin',
      body: JSON.stringify(payload || {}),
    });
    const data = await resp.json().catch(() => ({}));
    return { resp, data };
  };

  const refreshPresetGroups = (presets) => {
    if (!presetCardsHost || !presets) return;

    const buildCard = (label, folder, name) => {
      const key = `${folder}/${name}`;
      return [
        `<button type="button" class="artlomo-data-card" data-preset-card="${key}">`,
        `  <div><strong>${escapeHtml(name)}</strong></div>`,
        `  <div>${escapeHtml(label)}</div>`,
        '</button>',
      ].join('\n');
    };

    const cards = [];
    cards.push(buildCard('Root preset', 'root', 'default'));
    (presets.Root || []).filter((n) => n !== 'default').forEach((n) => cards.push(buildCard('Root preset', 'root', n)));
    (presets.System || []).forEach((n) => cards.push(buildCard('System preset', 'system', n)));
    (presets.User || []).forEach((n) => cards.push(buildCard('User preset', 'user', n)));

    presetCardsHost.innerHTML = cards.join('\n');

    presetCardsHost.querySelectorAll('[data-preset-card]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const key = (btn.getAttribute('data-preset-card') || '').trim();
        if (!key) return;
        const parts = key.split('/');
        if (parts.length !== 2) return;
        const folder = parts[0];
        const name = parts[1];
        setSelectedPresetCard({ key, folder, name, label: `${folder.toUpperCase()} preset` });
      });
    });

    if (selectedPresetKey) {
      setSelectedPresetCard(selectedPresetMeta);
    }
  };

  const loadSelectedPreset = async () => {
    if (!selectedPresetMeta || !selectedPresetMeta.folder || !selectedPresetMeta.name) {
      alert('Select a preset first');
      return;
    }
    const folder = selectedPresetMeta.folder;
    const name = selectedPresetMeta.name;
    try {
      const resp = await fetch(`/admin/style/load-preset/${encodeURIComponent(folder)}/${encodeURIComponent(name)}`, {
        method: 'GET',
        headers: { 'Accept': 'application/json' },
        credentials: 'same-origin',
      });
      const data = await resp.json().catch(() => ({}));
      if (!resp.ok || !data.ok) {
        alert(data.error || 'Failed to load preset');
        return;
      }
      setFormValues(data.preset);
      lastLoadedPreset = data.preset;
      refreshPresetGroups(data.presets);
      if (data.preset && data.preset.folder && data.preset.name) {
        setSelectedPresetCard({
          key: `${data.preset.folder}/${data.preset.name}`,
          folder: data.preset.folder,
          name: data.preset.name,
          label: 'Loaded preset',
        });
      }
      if (saveAsNewBtn) {
        if (data.preset && data.preset.folder && data.preset.folder !== 'user') {
          saveAsNewBtn.hidden = false;
        } else {
          saveAsNewBtn.hidden = true;
        }
      }
    } catch (e) {
      alert('Failed to load preset');
    }
  };

  const loadBootstrapData = async () => {
    try {
      const resp = await fetch('/admin/hub/style/data', {
        method: 'GET',
        headers: { 'Accept': 'application/json' },
        credentials: 'same-origin',
      });
      const data = await resp.json().catch(() => ({}));
      if (!resp.ok || !data.ok) {
        return;
      }

      DEFAULTS = (data.defaults && typeof data.defaults === 'object') ? data.defaults : {};
      bootPreset = (data.current && typeof data.current === 'object') ? data.current : {};
      lastLoadedPreset = bootPreset;

      refreshPresetGroups(data.presets);
      setFormValues(bootPreset);
      if (bootPreset && bootPreset.name) {
        const folder = (bootPreset.folder || 'user').toString();
        const name = (bootPreset.name || '').toString();
        if (folder && name) {
          setSelectedPresetCard({ key: `${folder}/${name}`, folder, name, label: 'Current preset' });
        }
      }
    } catch (e) {
      // ignore
    }
  };

  setSelectedPresetCard(null);

  const themeToggle = document.querySelector('.theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      // base.js handles theme switching; do NOT reload preset here (would wipe unsaved edits)
      setTimeout(() => {
        const theme = (document.documentElement.getAttribute('data-theme') || 'light').trim() || 'light';
        if (theme === 'dark') {
          // No-op
        }
      }, 50);
    });
  }

  if (previewLightBtn) {
    previewLightBtn.addEventListener('click', () => previewTheme('light'));
  }

  if (previewDarkBtn) {
    previewDarkBtn.addEventListener('click', () => previewTheme('dark'));
  }

  form.addEventListener('input', (ev) => {
    const target = ev && ev.target;
    if (customCssInput && target === customCssInput) {
      applyCustomCss(customCssInput.value || '');
      return;
    }
    if (!isDarkroomControl(target)) return;
    previewTheme(getActiveTheme());
  });

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      setFormValues(lastLoadedPreset || bootPreset || {});
    });
  }

  if (importBtn && importInput) {
    importBtn.addEventListener('click', () => {
      importInput.click();
    });

    importInput.addEventListener('change', async () => {
      const file = importInput.files && importInput.files[0];
      if (!file) return;
      try {
        const text = await file.text();
        const parsed = JSON.parse(text);
        const fallbackName = (file.name || 'imported').replace(/\.json$/i, '').trim() || 'imported';
        const preset = parseImportedPreset(parsed, fallbackName);
        setFormValues(preset);
        lastLoadedPreset = preset;
      } catch (e) {
        alert('Invalid JSON preset');
      } finally {
        importInput.value = '';
      }
    });
  }

  if (exportBtn) {
    exportBtn.addEventListener('click', () => {
      const payload = collectTwinPayload('save');
      const name = (payload.name || 'preset').toString().trim() || 'preset';
      const bundle = {
        name,
        preset: {
          name,
          light: payload.light || {},
          dark: payload.dark || {},
          custom_css: payload.custom_css || '',
        },
        css: buildPresetCss({
          name,
          light: payload.light || {},
          dark: payload.dark || {},
          custom_css: payload.custom_css || '',
        }),
      };
      downloadJsonFile(`${name}.darkroom.json`, bundle);
    });
  }

  if (loadBtn) {
    loadBtn.addEventListener('click', async () => {
      await loadSelectedPreset();
    });
  }

  if (deleteBtn) {
    deleteBtn.addEventListener('click', async () => {
      if (!selectedPresetMeta || !selectedPresetMeta.folder || !selectedPresetMeta.name) {
        alert('Select a preset first');
        return;
      }
      if (deleteBtn.disabled) {
        alert(deleteBtn.title || 'This preset cannot be deleted');
        return;
      }
      const name = selectedPresetMeta.name;
      const folder = selectedPresetMeta.folder;
      const ok = window.confirm(`Delete preset "${name}"? This cannot be undone.`);
      if (!ok) return;

      const { resp, data } = await postJson('/admin/hub/style/delete', { folder, name });
      if (!resp.ok || !data.ok) {
        alert((data && data.error) || 'Failed to delete preset');
        return;
      }

      if (data.current) {
        setFormValues(data.current);
        lastLoadedPreset = data.current;
        const currentFolder = (data.current.folder || 'user').toString();
        const currentName = (data.current.name || '').toString();
        if (currentFolder && currentName) {
          setSelectedPresetCard({
            key: `${currentFolder}/${currentName}`,
            folder: currentFolder,
            name: currentName,
            label: 'Current preset',
          });
        }
      }

      refreshPresetGroups(data.presets);
      if (saveAsNewBtn) saveAsNewBtn.hidden = true;
    });
  }

  if (saveAsNewBtn) {
    saveAsNewBtn.addEventListener('click', async () => {
      const payload = collectTwinPayload('copy');

      let saved = null;
      try {
        const legacy = await postJson('/admin/hub/style/save', payload);
        if (legacy.resp.ok && legacy.data && legacy.data.ok) {
          saved = legacy;
        }
      } catch (e) {
        saved = null;
      }
      if (!saved) {
        const fallback = await postJson('/admin/style/save-preset', { name: payload.name, values: payload.light });
        saved = fallback;
      }

      if (!saved.resp.ok || !saved.data.ok) {
        alert((saved.data && saved.data.error) || 'Failed to save preset');
        return;
      }
      if (nameInput) nameInput.value = saved.data.name;
      refreshPresetGroups(saved.data.presets);
      saveAsNewBtn.hidden = true;
      if (saved.data && saved.data.preset) lastLoadedPreset = saved.data.preset;
    });
  }

  form.addEventListener('submit', async (ev) => {
    if (!window.fetch) return;
    ev.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    const prevLabel = submitBtn ? submitBtn.textContent : '';
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Saving...';
    }

    const payload = collectTwinPayload('save');

    try {
      const { resp, data } = await postJson('/admin/hub/style/save', payload);
      if (!resp.ok || !data.ok) {
        alert((data && data.error) || 'Failed to save preset');
      } else {
        if (nameInput) nameInput.value = data.name;
        refreshPresetGroups(data.presets);
        if (saveAsNewBtn) saveAsNewBtn.hidden = true;
        if (data && data.preset) lastLoadedPreset = data.preset;
      }
    } catch (e) {
      alert('Failed to save preset');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = prevLabel || 'Save preset';
      }
    }
  });

  loadBootstrapData();
});
