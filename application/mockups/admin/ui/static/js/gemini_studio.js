(function () {
  "use strict";

  var root = document.querySelector("[data-gemini-studio]");
  if (!root) {
    return;
  }

  var form = root.querySelector("[data-gemini-studio-form]");
  var promptInput = root.querySelector("[data-studio-prompt]");
  var imageInput = root.querySelector("[data-studio-image-input]");
  var placeholderTypeInput = root.querySelector("[data-studio-placeholder-type]");
  var aspectInput = root.querySelector("[data-studio-aspect]");
  var categoryInput = root.querySelector("[data-studio-category]");
  var variationsInput = root.querySelector("[data-studio-variations]");
  var autoPromptBtn = root.querySelector("[data-studio-auto-prompt]");
  var sourcePlaceholderInput = root.querySelector("[data-studio-source-placeholder]");
  var dropzone = root.querySelector("[data-studio-dropzone]");
  var uploadField = root.querySelector("[data-studio-upload-field]");
  var submitBtn = root.querySelector("[data-studio-submit]");
  var statusEl = root.querySelector("[data-studio-status]");
  var fileNameEl = root.querySelector("[data-studio-file-name]");
  var cardsEl = root.querySelector("[data-studio-cards]");
  var workerBadge = root.querySelector(".gemini-studio__worker");
  var refreshBtn = root.querySelector("[data-studio-refresh]");
  var modal = root.querySelector("[data-carousel-modal]");
  var textModal = root.querySelector("[data-studio-text-modal]");
  var textModalMeta = root.querySelector("[data-studio-text-meta]");
  var textModalContent = root.querySelector("[data-studio-text-content]");
  var queueEndpoint = root.getAttribute("data-queue-endpoint") || "";
  var statusEndpoint = root.getAttribute("data-status-endpoint") || "";
  var deleteEndpointTemplate = root.getAttribute("data-delete-endpoint-template") || "";
  var libraryEndpointTemplate = root.getAttribute("data-library-endpoint-template") || "";
  var clearPendingEndpoint = root.getAttribute("data-clear-pending-endpoint") || "";
  var csrfToken = root.getAttribute("data-csrf-token") || "";

  var carouselItems = [];
  var carouselIndex = 0;
  var pollTimer = null;
  var promptCache = {};

  if (!form || !promptInput || !imageInput || !dropzone || !submitBtn || !statusEl || !fileNameEl || !cardsEl || !modal) {
    return;
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function hasPrompt() {
    return (promptInput.value || "").trim().length > 0;
  }

  function hasImage() {
    return true;
  }

  function syncSubmitState() {
    submitBtn.disabled = !(hasPrompt() && hasImage());
  }

  function setStatus(message) {
    statusEl.textContent = message || "";
  }

  function updateWorkerBadge(isRunning) {
    if (!workerBadge) {
      return;
    }
    workerBadge.classList.toggle("is-online", Boolean(isRunning));
    workerBadge.classList.toggle("is-offline", !isRunning);
    workerBadge.textContent = isRunning ? "Celery worker online" : "Celery worker offline";
  }

  function updateFileLabel() {
    if (hasImage()) {
      if (imageInput.files && imageInput.files.length > 0) {
        fileNameEl.textContent = imageInput.files[0].name;
        return;
      }
      fileNameEl.textContent = "Auto mode active (no upload selected).";
      return;
    }
    fileNameEl.textContent = "Auto mode active (no upload selected).";
  }

  function syncSourcePlaceholder() {
    if (!sourcePlaceholderInput) {
      return;
    }
    var aspectValue = aspectInput ? String(aspectInput.value || "1x1") : "1x1";
    var placeholderType = placeholderTypeInput ? String(placeholderTypeInput.value || "artwork-only") : "artwork-only";
    sourcePlaceholderInput.value = placeholderType === "outlined"
      ? aspectValue + "-outlined-artwork.png"
      : aspectValue + "-artwork-placeholder.png";
  }

  function buildAutoPrompt() {
    var aspectValue = aspectInput ? String(aspectInput.value || "1x1") : "1x1";
    var categoryValue = categoryInput ? String(categoryInput.value || "uncategorised") : "uncategorised";
    var variationValue = variationsInput ? String(variationsInput.value || "4") : "4";
    var aspectColon = aspectValue.replace("x", ":");
    var placeholderType = placeholderTypeInput ? String(placeholderTypeInput.value || "artwork-only") : "artwork-only";
    var referenceDescriptor = placeholderType === "outlined"
      ? "outlined reference artwork placeholder"
      : "artwork placeholder reference image";

    return [
      "[THINKING_LEVEL: HIGH]",
      "Generate a square (1:1) photorealistic " + categoryValue + " interior.",
      "Treat the attached " + referenceDescriptor + " as the primary geometric anchor.",
      "Place it inside a minimalist frame on a side wall viewed from a three-quarter perspective.",
      "Preserve the attached asset exactly as a " + aspectColon + " artwork. Do not crop, warp, repaint, or stylize it.",
      "Build the room's depth and perspective around the attached asset so it remains fully visible and naturally integrated.",
      "Generate " + variationValue + " distinct variation(s) while keeping the same anchored artwork geometry."
    ].join("\n\n");
  }

  function pickFiles(fileList) {
    if (!fileList || !fileList.length) {
      return;
    }
    var dt = new DataTransfer();
    dt.items.add(fileList[0]);
    imageInput.files = dt.files;
    updateFileLabel();
    syncSubmitState();
  }

  function buildActionEndpoint(template, jobId) {
    return template.replace("/0/", "/" + String(jobId) + "/");
  }

  function getPlaceholderFolderPath() {
    var placeholderType = placeholderTypeInput ? String(placeholderTypeInput.value || "outlined") : "outlined";
    if (placeholderType === "artwork-only") {
      return "/static/placeholders/artwork-only/";
    }
    return "/static/placeholders/outlined-artworks/";
  }

  function getPlaceholderFilename(aspectRatio) {
    var placeholderType = placeholderTypeInput ? String(placeholderTypeInput.value || "outlined") : "outlined";
    var aspect = String(aspectRatio || "1x1");
    
    if (placeholderType === "artwork-only") {
      return aspect + "-artwork-placeholder.png";
    }
    return aspect + "-outlined-artwork.png";
  }

  function autoSelectPlaceholder() {
    var aspectRatio = aspectInput ? String(aspectInput.value || "1x1") : "1x1";
    var folderPath = getPlaceholderFolderPath();
    var filename = getPlaceholderFilename(aspectRatio);
    var fullUrl = folderPath + filename;
    
    if (fileNameEl) {
      var placeholderType = placeholderTypeInput ? String(placeholderTypeInput.value || "artwork-only") : "artwork-only";
      fileNameEl.textContent = (placeholderType === "artwork-only" ? "ARTWORK PLACEHOLDER: " : "OUTLINED PLACEHOLDER: ") + aspectRatio + " auto-selected";
    }
  }

  function formatDate(value) {
    if (!value) {
      return "";
    }
    var date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return String(value);
    }
    return date.toLocaleString("en-AU", {
      year: "numeric",
      month: "short",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit"
    });
  }

  function renderJobs(jobs) {
    var rows = Array.isArray(jobs) ? jobs : [];
    if (!rows.length) {
      cardsEl.innerHTML = '<div class="studio-card studio-card--empty">No studio jobs yet.</div>';
      rebuildCarouselItems();
      return;
    }

    cardsEl.innerHTML = rows.map(function (job) {
      var status = String(job.status || "Pending");
      var imageBlock = job.image_url
        ? '<button class="studio-card__image-button" type="button" data-studio-carousel-trigger data-studio-image-url="' + escapeHtml(job.image_url) + '" data-studio-image-name="' + escapeHtml(job.category + ' · ' + job.aspect_ratio + ' · v' + job.variation_index) + '"><img src="' + escapeHtml(job.image_url) + '?v=' + Date.now() + '" alt="' + escapeHtml(job.category + ' variation ' + job.variation_index) + '" class="studio-card__image" loading="lazy"></button>'
        : '<div class="studio-card__placeholder">' + escapeHtml(job.error_message || (status === "Generating" ? "Generating preview..." : "Queued and waiting for worker output...")) + '</div>';
      var addDisabled = status !== "Completed" || Boolean(job.added_to_library);
      return ''
        + '<article class="studio-card" data-studio-job-id="' + escapeHtml(job.id) + '">'
        + '  <div class="studio-card__top">'
        + '    <div>'
        + '      <div class="studio-card__title">' + escapeHtml(job.category) + ' · ' + escapeHtml(job.aspect_ratio) + ' · v' + escapeHtml(job.variation_index) + '</div>'
        + '      <div class="studio-card__meta">' + escapeHtml((job.prompt_text || '').substring(0, 60) + ((job.prompt_text || '').length > 60 ? '\u2026' : '')) + '</div>'
        + '    </div>'
        + '    <div class="studio-card__badge studio-card__badge--' + escapeHtml(status.toLowerCase()) + '">' + escapeHtml(status) + '</div>'
        + '  </div>'
        + imageBlock
        + '  <div class="studio-card__footer">'
        + '    <div class="studio-card__footer-meta">' + escapeHtml(formatDate(job.created_at)) + '</div>'
        + '    <div class="studio-card__actions">'
        + '      <button class="gallery-btn gallery-btn--primary" type="button" data-studio-add ' + (addDisabled ? 'disabled' : '') + '>' + escapeHtml(job.added_to_library ? 'Added' : 'Add to Library') + '</button>'
        + '      <button class="gallery-btn gallery-btn--outline" type="button" data-studio-view-text>View Text</button>'
        + '      <button class="gallery-btn gallery-btn--outline" type="button" data-studio-delete>Delete</button>'
        + '    </div>'
        + '  </div>'
        + '</article>';
    }).join("");

    rebuildCarouselItems();
  }

  function rebuildCarouselItems() {
    carouselItems = Array.prototype.slice.call(root.querySelectorAll("[data-studio-carousel-trigger]")).map(function (node) {
      return {
        full: node.getAttribute("data-studio-image-url") || "",
        name: node.getAttribute("data-studio-image-name") || "Generated preview"
      };
    }).filter(function (item) {
      return Boolean(item.full);
    });
  }

  function renderCarousel() {
    if (!modal || !carouselItems.length) {
      return;
    }
    var item = carouselItems[carouselIndex];
    var imageNode = modal.querySelector("[data-carousel-image]");
    var titleNode = modal.querySelector("[data-carousel-title]");
    var counterNode = modal.querySelector("[data-carousel-counter]");
    var openNode = modal.querySelector("[data-carousel-open]");
    if (imageNode) {
      imageNode.src = item.full;
      imageNode.alt = item.name || "Generated preview";
    }
    if (titleNode) {
      titleNode.textContent = item.name || "Generated preview";
    }
    if (counterNode) {
      counterNode.textContent = String(carouselIndex + 1) + " / " + String(carouselItems.length);
    }
    if (openNode) {
      openNode.href = item.full;
    }
  }

  function openCarousel(index) {
    if (!carouselItems.length) {
      return;
    }
    carouselIndex = ((index % carouselItems.length) + carouselItems.length) % carouselItems.length;
    modal.dataset.open = "true";
    modal.dataset.visible = "1";
    modal.setAttribute("aria-hidden", "false");
    renderCarousel();
  }

  function closeCarousel() {
    modal.dataset.open = "false";
    modal.dataset.visible = "";
    modal.setAttribute("aria-hidden", "true");
  }

  function openTextModal(metaText, compiledText) {
    if (!textModal || !textModalContent || !textModalMeta) {
      return;
    }
    textModalMeta.textContent = metaText || "Gemini text payload";
    textModalContent.value = compiledText || "(No compiled text available for this job.)";
    textModal.dataset.visible = "1";
    textModal.setAttribute("aria-hidden", "false");
  }

  function closeTextModal() {
    if (!textModal) {
      return;
    }
    textModal.dataset.visible = "";
    textModal.setAttribute("aria-hidden", "true");
  }

  async function loadPromptCompilation(jobId) {
    if (promptCache[jobId]) {
      return promptCache[jobId];
    }
    var response = await fetch("/admin/mockups/gemini-studio/jobs/" + String(jobId) + "/full-prompt", {
      credentials: "same-origin"
    });
    var data = await response.json();
    if (!response.ok || !data || data.status !== "ok") {
      throw new Error((data && data.message) ? data.message : "Failed to fetch full prompt text.");
    }
    promptCache[jobId] = data;
    return data;
  }

  async function fetchStatus() {
    if (!statusEndpoint) {
      return;
    }
    try {
      var response = await fetch(statusEndpoint, { credentials: "same-origin" });
      var data = await response.json();
      if (!response.ok || !data || data.status !== "ok") {
        return;
      }
      renderJobs(data.jobs || []);
      updateWorkerBadge(Boolean(data.worker_running));
    } catch (_error) {
      return;
    }
  }

  async function postJson(url, payload) {
    var response = await fetch(url, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-CSRF-Token": csrfToken
      },
      body: JSON.stringify(payload)
    });
    var data = await response.json();
    if (!response.ok || !data || (data.status !== "ok" && data.status !== "warning")) {
      throw new Error((data && data.message) ? data.message : "Request failed.");
    }
    return data;
  }

  dropzone.addEventListener("click", function () {
    imageInput.click();
  });

  dropzone.addEventListener("keydown", function (event) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      imageInput.click();
    }
  });

  imageInput.addEventListener("change", function () {
    updateFileLabel();
    syncSubmitState();
  });

  if (autoPromptBtn) {
    autoPromptBtn.addEventListener("click", function () {
      var hasExisting = (promptInput.value || "").trim().length > 0;
      if (hasExisting && !window.confirm("Replace the existing prompt with an auto-generated prompt?")) {
        return;
      }
      promptInput.value = buildAutoPrompt();
      syncSubmitState();
      setStatus("Auto prompt generated. You can edit it before queueing.");
      promptInput.focus();
      promptInput.setSelectionRange(promptInput.value.length, promptInput.value.length);
    });
  }

  if (aspectInput) {
    aspectInput.addEventListener("change", function() {
      if (imageInput && imageInput.value) {
        imageInput.value = "";
      }
      syncSourcePlaceholder();
      autoSelectPlaceholder();
      updateFileLabel();
      syncSubmitState();
    });
  }

  if (placeholderTypeInput) {
    placeholderTypeInput.addEventListener("change", function () {
      if (imageInput && imageInput.value) {
        imageInput.value = "";
      }
      syncSourcePlaceholder();
      autoSelectPlaceholder();
      updateFileLabel();
      syncSubmitState();
    });
  }

  promptInput.addEventListener("input", syncSubmitState);

  ["dragenter", "dragover"].forEach(function (type) {
    dropzone.addEventListener(type, function (event) {
      event.preventDefault();
      event.stopPropagation();
      dropzone.classList.add("is-dragover");
    });
  });

  ["dragleave", "drop"].forEach(function (type) {
    dropzone.addEventListener(type, function (event) {
      event.preventDefault();
      event.stopPropagation();
      dropzone.classList.remove("is-dragover");
    });
  });

  dropzone.addEventListener("drop", function (event) {
    pickFiles(event.dataTransfer && event.dataTransfer.files ? event.dataTransfer.files : null);
  });

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    if (submitBtn.disabled || !queueEndpoint) {
      return;
    }

    submitBtn.disabled = true;
    setStatus("Queueing Gemini Studio variations...");

    try {
      var payload = new FormData(form);
      syncSourcePlaceholder();
      if (sourcePlaceholderInput) {
        payload.set("source_placeholder", sourcePlaceholderInput.value || "");
      }
      if (placeholderTypeInput) {
        payload.set("placeholder_type", String(placeholderTypeInput.value || "artwork-only"));
      }
      var response = await fetch(queueEndpoint, {
        method: "POST",
        body: payload,
        credentials: "same-origin",
        headers: {
          "Accept": "application/json"
        }
      });
      var data = await response.json();
      if (!response.ok || !data || (data.status !== "ok" && data.status !== "warning")) {
        throw new Error((data && data.message) ? data.message : "Queueing failed.");
      }
      renderJobs(data.jobs || []);
      updateWorkerBadge(Boolean(data.worker_running));
      setStatus(data.message || "Queued.");
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Queueing failed.");
    } finally {
      syncSubmitState();
    }
  });

  root.addEventListener("click", async function (event) {
    var trigger = event.target.closest("[data-studio-carousel-trigger]");
    if (trigger) {
      event.preventDefault();
      rebuildCarouselItems();
      var nodes = Array.prototype.slice.call(root.querySelectorAll("[data-studio-carousel-trigger]"));
      openCarousel(Math.max(0, nodes.indexOf(trigger)));
      return;
    }

    var card = event.target.closest("[data-studio-job-id]");
    if (!card) {
      return;
    }
    var jobId = card.getAttribute("data-studio-job-id") || "";
    if (!jobId) {
      return;
    }

    if (event.target.closest("[data-studio-delete]")) {
      try {
        setStatus("Deleting studio result...");
        var deleteData = await postJson(buildActionEndpoint(deleteEndpointTemplate, jobId), { csrf_token: csrfToken });
        renderJobs(deleteData.jobs || []);
        setStatus("Deleted.");
      } catch (error) {
        setStatus(error instanceof Error ? error.message : "Delete failed.");
      }
      return;
    }

    if (event.target.closest("[data-studio-add]")) {
      if (event.target.disabled) {
        return;
      }
      try {
        setStatus("Adding result to mockup library...");
        var libraryData = await postJson(buildActionEndpoint(libraryEndpointTemplate, jobId), { csrf_token: csrfToken });
        renderJobs(libraryData.jobs || []);
        setStatus(libraryData.message || "Added to library.");
      } catch (error) {
        setStatus(error instanceof Error ? error.message : "Add to library failed.");
      }
      return;
    }

    if (event.target.closest("[data-studio-view-text]")) {
      try {
        setStatus("Loading complete Gemini text compilation...");
        var promptData = await loadPromptCompilation(jobId);
        var mode = promptData.delivery_mode ? "Mode: " + String(promptData.delivery_mode) : "";
        var meta = "Job " + String(jobId) + (mode ? " | " + mode : "");
        openTextModal(meta, String(promptData.full_prompt_compilation || ""));
        setStatus("Loaded full Gemini text.");
      } catch (error) {
        setStatus(error instanceof Error ? error.message : "Unable to load full text.");
      }
      return;
    }
  });

  // Handle "Stop & Clear All Pending" button
  var clearPendingBtn = root.querySelector("[data-studio-clear-pending]");
  if (clearPendingBtn) {
    clearPendingBtn.addEventListener("click", async function (event) {
      event.preventDefault();
      
      var confirmMessage = "⚠️ WARNING: This will permanently delete ALL pending jobs and their files.\n\nThis action cannot be undone.\n\nContinue?";
      if (!confirm(confirmMessage)) {
        return;
      }
      
      try {
        setStatus("Clearing all pending jobs...");
        clearPendingBtn.disabled = true;
        
        var response = await fetch(clearPendingEndpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ csrf_token: csrfToken }),
        });
        
        if (!response.ok) {
          throw new Error("Failed to clear pending jobs: " + response.status);
        }
        
        var data = await response.json();
        renderJobs(data.jobs || []);
        setStatus("✅ " + (data.message || "Cleared all pending jobs."));
      } catch (error) {
        setStatus("❌ " + (error instanceof Error ? error.message : "Clear failed."));
      } finally {
        clearPendingBtn.disabled = false;
      }
    });
  }

  if (refreshBtn) {
    refreshBtn.addEventListener("click", async function () {
      refreshBtn.disabled = true;
      try {
        setStatus("Refreshing results...");
        await fetchStatus();
        setStatus("Results refreshed.");
      } finally {
        refreshBtn.disabled = false;
      }
    });
  }

  modal.addEventListener("click", function (event) {
    if (event.target === modal) {
      closeCarousel();
    }
  });

  if (textModal) {
    textModal.addEventListener("click", function (event) {
      if (event.target === textModal || event.target.closest("[data-studio-text-close]")) {
        closeTextModal();
      }
    });
  }

  var closeButton = modal.querySelector("[data-carousel-close]");
  var prevButton = modal.querySelector("[data-carousel-prev]");
  var nextButton = modal.querySelector("[data-carousel-next]");

  if (closeButton) {
    closeButton.addEventListener("click", closeCarousel);
  }
  if (prevButton) {
    prevButton.addEventListener("click", function () {
      openCarousel(carouselIndex - 1);
    });
  }
  if (nextButton) {
    nextButton.addEventListener("click", function () {
      openCarousel(carouselIndex + 1);
    });
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      if (textModal && textModal.dataset.visible) {
        closeTextModal();
        return;
      }
      if (!modal.dataset.visible) {
        return;
      }
      closeCarousel();
    } else if (!modal.dataset.visible) {
      return;
    } else if (event.key === "ArrowLeft") {
      openCarousel(carouselIndex - 1);
    } else if (event.key === "ArrowRight") {
      openCarousel(carouselIndex + 1);
    }
  });

  updateFileLabel();
  syncSourcePlaceholder();
  autoSelectPlaceholder();
  syncSubmitState();
  rebuildCarouselItems();
  fetchStatus();
  pollTimer = window.setInterval(fetchStatus, 10000);

  window.addEventListener("beforeunload", function () {
    if (pollTimer) {
      window.clearInterval(pollTimer);
    }
  });
})();
