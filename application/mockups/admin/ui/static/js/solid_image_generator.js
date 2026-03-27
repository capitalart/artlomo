(function () {
  'use strict';

  function updateColorUI(colorInput, valueNode, previewNode) {
    var hexValue = (colorInput.value || '').toUpperCase();
    if (valueNode) {
      valueNode.textContent = hexValue;
    }
    if (previewNode) {
      previewNode.style.backgroundColor = hexValue;
    }
  }

  function updateRatioLabel(ratioSelect, selectedRatioNode) {
    if (!selectedRatioNode) {
      return;
    }
    selectedRatioNode.textContent = ratioSelect.value || 'None';
  }

  document.addEventListener('DOMContentLoaded', function () {
    var ratioSelect = document.getElementById('aspect-ratio');
    var colorInput = document.getElementById('color');
    var colorValue = document.getElementById('color-value');
    var previewColor = document.getElementById('preview-color');
    var selectedRatio = document.getElementById('selected-ratio');

    if (!ratioSelect || !colorInput || !previewColor) {
      return;
    }

    var defaultColor = (previewColor.dataset.defaultColor || '').trim();
    if (!colorInput.value && defaultColor) {
      colorInput.value = defaultColor;
    }

    updateColorUI(colorInput, colorValue, previewColor);
    updateRatioLabel(ratioSelect, selectedRatio);

    colorInput.addEventListener('input', function () {
      updateColorUI(colorInput, colorValue, previewColor);
    });

    ratioSelect.addEventListener('change', function () {
      updateRatioLabel(ratioSelect, selectedRatio);
    });
  });
})();
