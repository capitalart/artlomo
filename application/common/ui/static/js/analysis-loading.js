/**
 * Analysis Loading Overlay
 * * Shows a dark transparent overlay with animated spinning arrows
 * while AI analysis is being performed.
 * * Usage:
 * AnalysisLoader.show("OpenAI");
 * AnalysisLoader.hide();
 * AnalysisLoader.poll(slug, provider, maxWaitMs);
 */

const AnalysisLoader = (() => {
  let overlayElement = null;
  let pollInterval = null;
  let cancelCallback = null;

  const createOverlay = (provider) => {
    if (overlayElement) {
      return overlayElement;
    }

    const overlay = document.createElement("div");
    overlay.id = "analysisLoadingOverlay";
    overlay.className = "analysis-loading-overlay";
    overlay.innerHTML = `
      <div class="analysis-loading-content">
        <img src="/static/icons/arrows-clockwise-dark.svg" class="analysis-spinner" alt="Loading...">
        <p class="analysis-loading-text">${provider} Analysis in Progress</p>
        <div class="analysis-loading-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <div class="analysis-loading-actions">
          <button class="analysis-cancel-btn" id="analysisCancelBtn">Cancel</button>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);
    overlayElement = overlay;
    
    // Add cancel button listener
    const cancelBtn = overlay.querySelector("#analysisCancelBtn");
    if (cancelBtn) {
      cancelBtn.addEventListener("click", () => {
        if (cancelCallback) {
          cancelCallback();
        } else {
          AnalysisLoader.hide();
        }
      });
    }
    
    return overlay;
  };

  return {
    show: (provider = "AI", onCancel = null) => {
      cancelCallback = onCancel;
      createOverlay(provider);
      overlayElement.classList.add("visible");
      // Remove error state if showing again
      const content = overlayElement.querySelector(".analysis-loading-content");
      if (content) {
        content.classList.remove("error");
      }
      document.body.style.overflow = "hidden";
    },

    hide: () => {
      if (overlayElement) {
        overlayElement.classList.remove("visible");
        document.body.style.overflow = "";
        // Give animation time to complete
        setTimeout(() => {
          if (overlayElement && overlayElement.parentNode) {
            overlayElement.parentNode.removeChild(overlayElement);
            overlayElement = null;
          }
        }, 300);
      }
      if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
      }
      cancelCallback = null;
    },

    showError: (errorMessage) => {
      if (!overlayElement) {
        createOverlay("AI");
        overlayElement.classList.add("visible");
      }
      
      const content = overlayElement.querySelector(".analysis-loading-content");
      if (content) {
        content.classList.add("error");
        const spinner = content.querySelector(".analysis-spinner");
        const text = content.querySelector(".analysis-loading-text");
        const dots = content.querySelector(".analysis-loading-dots");
        
        if (spinner) spinner.style.display = "none";
        if (dots) dots.style.display = "none";
        if (text) {
          text.textContent = "Analysis Failed";
          text.classList.add("error-title");
        }
        
        // Add error message
        let errorMsg = content.querySelector(".analysis-error-message");
        if (!errorMsg) {
          errorMsg = document.createElement("p");
          errorMsg.className = "analysis-error-message";
          content.appendChild(errorMsg);
        }
        errorMsg.textContent = errorMessage;
        
        // Update button text to allow user to exit
        const btn = content.querySelector(".analysis-cancel-btn");
        if (btn) {
          btn.textContent = "Back to Gallery";
          btn.onclick = () => { window.location.reload(); };
        }
      }
    },

    poll: (slug, provider, maxWaitMs = 300000) => {
      return new Promise((resolve, reject) => {
        const startTime = Date.now();
        const checkInterval = 1500; // Check every 1.5 seconds
        let lastData = null;

        const buildTimeoutMessage = (data) => {
          const stage = ((data && data.stage) || '').toString().toLowerCase();
          const message = (data && (data.error || data.message)) || '';
          if (stage === 'queued') {
            return message || 'Analysis queue is still queued. The analysis worker may be offline.';
          }
          return message || 'Analysis timeout - no response from server after 5 minutes';
        };

        pollInterval = setInterval(async () => {
          const elapsed = Date.now() - startTime;

          if (elapsed > maxWaitMs) {
            clearInterval(pollInterval);
            pollInterval = null;
            const timeoutErr = new Error(buildTimeoutMessage(lastData));
            timeoutErr.code = lastData && String(lastData.stage || '').toLowerCase() === 'queued' ? 'QUEUE_STALLED' : 'TIMEOUT';
            timeoutErr.stage = lastData && lastData.stage;
            reject(timeoutErr);
            return;
          }

          try {
            // Include provider in the status query
            const response = await fetch(
              `/api/analysis/status/${slug}?provider=${provider}`,
              { method: "GET" }
            );

            if (!response.ok) {
              return; // Keep polling
            }

            const data = await response.json();
            lastData = data;

            // Update overlay status text with pipeline stage when available
            if (overlayElement) {
              const textEl = overlayElement.querySelector('.analysis-loading-text');
              if (textEl && data.stage) {
                const stageMap = {
                  queued: 'QUEUED — Waiting for analysis worker',
                  stage1_image: 'RUNNING — Stage 1/3',
                  stage2_etsy: 'RUNNING — Stage 2/3',
                  stage3_marketing: 'RUNNING — Stage 3/3',
                };
                const providerLabel = provider ? `${String(provider).toUpperCase()} ` : '';
                const stageLabel = stageMap[data.stage] || `${providerLabel}Analysis in Progress`;
                textEl.textContent = stageLabel;
              }
            }

            // Check for errors first
            if (data.error || data.stage === "error") {
              clearInterval(pollInterval);
              pollInterval = null;
              const err = new Error(data.error || data.message || "Analysis failed");
              err.code = data.error_code || "ERR_UNKNOWN";
              err.stage = data.stage;
              reject(err);
              return;
            }

            // Check if analysis is complete
            if (data.done === true) {
              clearInterval(pollInterval);
              pollInterval = null;
              resolve(data);
              return;
            }
          } catch (err) {
            console.error("Poll error:", err);
            // Continue polling on network error
          }
        }, checkInterval);
      });
    }
  };
})();

/**
 * Entry point for buttons in the HTML template.
 * Effectively bridges the UI click to the AnalysisLoader logic.
 */
async function handleAnalysisClick(event, provider, slug) {
  event.preventDefault();
  
  const providerTitle = provider.charAt(0).toUpperCase() + provider.slice(1);
  
  try {
    // 1. Show the overlay
    AnalysisLoader.show(providerTitle, () => {
      // Logic if user hits "Cancel"
      window.location.reload();
    });
    
    // 2. Start polling and wait for completion
    await AnalysisLoader.poll(slug, provider);
    
    // 3. Success! Hide and redirect to review
    AnalysisLoader.hide();
    window.location.href = `/artwork/${slug}/review/${provider}`;
    
  } catch (err) {
    console.error("Analysis handle error:", err);
    // 4. Show the error state inside the overlay instead of a generic alert
    AnalysisLoader.showError(err.message || "An unexpected error occurred during analysis.");
  }
}

document.addEventListener("click", (event) => {
  const trigger = event.target instanceof Element
    ? event.target.closest("[data-analysis-provider][data-slug]")
    : null;
  if (!trigger) {
    return;
  }
  const provider = (trigger.getAttribute("data-analysis-provider") || "").trim().toLowerCase();
  const slug = (trigger.getAttribute("data-slug") || "").trim();
  if (!provider || !slug) {
    return;
  }
  handleAnalysisClick(event, provider, slug);
});