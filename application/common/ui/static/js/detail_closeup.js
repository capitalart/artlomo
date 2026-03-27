/**
 * Detail Closeup Editor - Normalized Coordinates (v2.1)
 * Handles zoom, pan, and crop with resolution-independent 0.0-1.0 coordinates
 */
class DetailCloseupEditor {
  constructor(config) {
    this.container = document.getElementById(config.viewportId);
    this.imageElement = document.getElementById(config.imageId);
    this.loadingOverlay = document.getElementById(config.loadingOverlayId || 'detailLoadingOverlay');
    this.debugEl = document.getElementById('detailDebug');
    this.saveBtn = document.getElementById(config.saveBtnId);
    this.updatePreviewBtn = document.getElementById('updatePreviewBtn');

    // State
    this.transformState = { x: 0, y: 0, scale: 1.0 };
    this.slug = config.slug;
    this.saveUrl = `/artwork/${this.slug}/detail-closeup/save`;
    this.csrfToken = config.csrfToken || '';

    // Ensure image onload triggers debug update + overlay removal
    if (this.imageElement.complete && this.imageElement.naturalWidth > 0) {
      // Image is already loaded from cache
      this.updateDebugInfo();
      this.setLoadingState(false);
    } else {
      // Wait for image to load
      this.imageElement.onload = () => {
        this.updateDebugInfo();
        this.setLoadingState(false);
      };
      this.imageElement.onerror = () => {
        this.setLoadingState(false);
      };
    }

    this.attachListeners();
  }

  setLoadingState(isLoading) {
    if (!this.loadingOverlay) return;
    this.loadingOverlay.classList.toggle('is-hidden', !isLoading);
  }

  updateDebugInfo() {
    if (!this.debugEl) return;

    const renderedW = this.imageElement.offsetWidth || 7200;
    const renderedH = this.imageElement.offsetHeight || 7200;
    const scale = this.transformState.scale.toFixed(2);
    const zoomPercent = ((this.transformState.scale / 28.8) * 100).toFixed(1);

    this.debugEl.textContent = `Scale: ${scale} (${zoomPercent}%) | Rendered: ${renderedW}x${renderedH}px | Ready ✓`;
  }

  attachListeners() {
    // Zoom buttons
    const zoomInBtn = document.getElementById('zoomInBtn');
    const zoomOutBtn = document.getElementById('zoomOutBtn');
    const directCutBtn = document.getElementById('directCutBtn');
    const snapBtn = document.getElementById('snap1to1Btn');

    if (zoomInBtn) {
      zoomInBtn.addEventListener('click', () => this.setScale(this.transformState.scale * 1.1));
    }
    if (zoomOutBtn) {
      zoomOutBtn.addEventListener('click', () => this.setScale(this.transformState.scale * 0.9));
    }
    if (directCutBtn) {
      directCutBtn.addEventListener('click', () => this.setScale(7.03125)); // Direct Cut scale
    }
    if (snapBtn) {
      snapBtn.addEventListener('click', () => this.setScale(28.8)); // 1:1 pixel scale
    }

    // Save buttons
    if (this.saveBtn) {
      this.saveBtn.addEventListener('click', () => this.save());
    }
    if (this.updatePreviewBtn) {
      this.updatePreviewBtn.addEventListener('click', () => this.save());
    }

    // Pan/Drag Logic
    let isDragging = false;
    let startX, startY, initialX, initialY;

    this.container.addEventListener('mousedown', (e) => {
      isDragging = true;
      startX = e.clientX;
      startY = e.clientY;
      initialX = this.transformState.x;
      initialY = this.transformState.y;
      this.container.style.cursor = 'grabbing';
      e.preventDefault();
    });

    window.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      this.transformState.x = initialX + (e.clientX - startX);
      this.transformState.y = initialY + (e.clientY - startY);
      this.updateTransform();
    });

    window.addEventListener('mouseup', () => {
      isDragging = false;
      this.container.style.cursor = 'grab';
    });
  }

  setScale(newScale) {
    // Clamp scale to reasonable bounds
    newScale = Math.max(0.5, Math.min(36, newScale));

    if (newScale === this.transformState.scale) return;

    const containerW = this.container.clientWidth;
    const containerH = this.container.clientHeight;

    // Calculate focal point (what's at container center before scaling)
    const focalX = (containerW / 2 - this.transformState.x) / this.transformState.scale;
    const focalY = (containerH / 2 - this.transformState.y) / this.transformState.scale;

    // Update scale
    this.transformState.scale = newScale;

    // Recalculate offsets to keep focal point at center
    this.transformState.x = containerW / 2 - (focalX * newScale);
    this.transformState.y = containerH / 2 - (focalY * newScale);

    this.updateTransform();
    this.updateDebugInfo();
  }

  updateTransform() {
    if (!this.imageElement) return;

    this.imageElement.style.transform = `translate(${this.transformState.x}px, ${this.transformState.y}px) scale(${this.transformState.scale})`;
    this.imageElement.style.transformOrigin = '0 0';

    // Update scale display
    const scaleDisplay = document.getElementById('scaleDisplay');
    if (scaleDisplay) {
      const percent = ((this.transformState.scale / 28.8) * 100).toFixed(1);
      scaleDisplay.textContent = `${percent}%`;
    }
  }

  save() {
    const btn = this.updatePreviewBtn || this.saveBtn;
    if (!btn) return;

    const originalText = btn.textContent;
    btn.textContent = "⏳ Saving...";
    btn.disabled = true;

    // --- CRITICAL: Use Rendered Width (offsetWidth) not Natural Width ---
    const renderedW = this.imageElement.offsetWidth;
    const renderedH = this.imageElement.offsetHeight;

    // DIMENSION FAILURE CHECK
    if (!renderedW || !renderedH) {
      throw new Error("Dimension Failure: offsetWidth or offsetHeight is missing/invalid");
    }

    const containerW = this.container.clientWidth;
    const containerH = this.container.clientHeight;

    // Calculate center point on image in scaled pixels
    const centerX_px = (containerW / 2 - this.transformState.x) / this.transformState.scale;
    const centerY_px = (containerH / 2 - this.transformState.y) / this.transformState.scale;

    // Normalize to 0.0-1.0 range relative to rendered dimensions
    let normX = centerX_px / renderedW;
    let normY = centerY_px / renderedH;

    // Clamp to valid range
    normX = Math.max(0, Math.min(1, normX));
    normY = Math.max(0, Math.min(1, normY));

    console.log("Coordinate Sync v2.1 Active", { normX, normY });
    console.log("Saving Normalized Coordinates:", {
      renderedW,
      centerX_px,
      normX,
      normY,
      scale: this.transformState.scale
    });

    const payload = {
      norm_x: normX,
      norm_y: normY,
      scale: this.transformState.scale
    };

    fetch(this.saveUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': this.csrfToken || document.querySelector('meta[name="csrf-token"]')?.content || ''
      },
      body: JSON.stringify(payload)
    })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(data => {
        if (data.status === 'success') {
          const resultImg = document.getElementById('liveResultImage');
          const resultStatus = document.getElementById('resultStatus');
          if (resultImg) {
            resultImg.src = data.url;
            resultImg.style.display = 'block';
          }
          if (resultStatus) {
            resultStatus.textContent = 'Detail closeup updated.';
            resultStatus.style.color = '#888';
          }
          btn.textContent = "✅ Updated";
        } else {
          const resultStatus = document.getElementById('resultStatus');
          if (resultStatus) {
            resultStatus.textContent = "Error: " + (data.error || "Unknown error");
            resultStatus.style.color = '#c96b6b';
          }
        }
      })
      .catch(err => {
        console.error("Save error:", err);
        const resultStatus = document.getElementById('resultStatus');
        if (resultStatus) {
          resultStatus.textContent = "Error: " + err.message;
          resultStatus.style.color = '#c96b6b';
        }
      })
      .finally(() => {
        setTimeout(() => {
          btn.textContent = originalText;
          btn.disabled = false;
        }, 1000);
      });
  }

  init() {
    // Called after DOM is ready
    this.updateTransform();
    this.updateDebugInfo();
  }
}

// Make available globally
window.DetailCloseupEditor = DetailCloseupEditor;
