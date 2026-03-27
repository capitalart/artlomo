(function () {
  const saveAsNewCheckbox = document.getElementById('saveAsNew');
  const newPresetNameGroup = document.getElementById('newPresetNameGroup');
  const newPresetNameInput = document.getElementById('newPresetName');
  const presetForm = document.getElementById('presetForm');

  if (!presetForm) {
    return;
  }

  if (saveAsNewCheckbox && newPresetNameGroup && newPresetNameInput) {
    saveAsNewCheckbox.addEventListener('change', function () {
      if (this.checked) {
        newPresetNameGroup.classList.add('visible');
        newPresetNameInput.required = true;
      } else {
        newPresetNameGroup.classList.remove('visible');
        newPresetNameInput.required = false;
      }
    });
  }

  presetForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    const saveAsNew = !!(saveAsNewCheckbox && saveAsNewCheckbox.checked);
    if (saveAsNew && newPresetNameInput && !newPresetNameInput.value.trim()) {
      alert('Please enter a name for the new preset');
      return;
    }

    const formData = new FormData(this);
    const presetIdRaw = formData.get('preset_id');
    const parsedPresetId = parseInt(presetIdRaw, 10);

    const data = {
      preset_id: saveAsNew ? null : (Number.isNaN(parsedPresetId) ? null : parsedPresetId),
      name: saveAsNew ? formData.get('new_preset_name') : formData.get('name'),
      provider: formData.get('provider'),
      is_default: formData.get('is_default') === 'true',
      system_prompt: formData.get('system_prompt'),
      user_full_prompt: formData.get('user_full_prompt'),
      user_section_prompt: formData.get('user_section_prompt'),
      listing_boilerplate: formData.get('listing_boilerplate'),
      analysis_prompt: formData.get('analysis_prompt'),
    };

    try {
      const response = await fetch('/admin/analysis-management/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': formData.get('_csrf_token'),
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      if (result.status === 'ok') {
        const action = saveAsNew ? 'created' : 'saved';
        alert(`Preset ${action} successfully!`);
        window.location.href = '/admin/analysis-management';
      } else {
        alert('Error: ' + (result.message || 'Unknown error'));
      }
    } catch (err) {
      alert('Error: ' + (err && err.message ? err.message : 'Unknown error'));
    }
  });
})();
