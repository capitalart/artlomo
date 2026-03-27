(function () {
  "use strict";

  var studioRoot = document.querySelector("[data-basic-mockups]");
  if (!studioRoot) {
    return;
  }

  // --- DOM references ---
  var form = studioRoot.querySelector("[data-basic-mockups-form]");
  var categorySelect = studioRoot.querySelector("[data-basic-category]");
  var promptDisplay = studioRoot.querySelector("[data-basic-prompt-display]");
  var dropzone = studioRoot.querySelector("[data-basic-dropzone]");
  var fileInput = studioRoot.querySelector("[data-basic-image-input]");
  var fileName = studioRoot.querySelector("[data-basic-file-name]");
  var submitBtn = studioRoot.querySelector("[data-basic-submit]");
  var statusEl = studioRoot.querySelector("[data-basic-status]");
  var cardsContainer = studioRoot.querySelector("[data-basic-cards]");
  var emptyState = studioRoot.querySelector("[data-basic-empty-state]");
  var carouselModal = studioRoot.querySelector("[data-basic-carousel-modal]");
  var textModal = studioRoot.querySelector("[data-basic-text-modal]");
  var refreshBtn = studioRoot.querySelector("[data-basic-refresh]");
  var clearPendingBtn = studioRoot.querySelector("[data-basic-clear-pending]");

  // --- Endpoint config from data attributes ---
  var queueEndpoint = studioRoot.dataset.queueEndpoint || "";
  var statusEndpoint = studioRoot.dataset.statusEndpoint || "";
  var deleteEndpointTemplate = studioRoot.dataset.deleteEndpointTemplate || "";
  var promptEndpointTemplate = studioRoot.dataset.promptEndpointTemplate || "";
  var clearPendingEndpoint = studioRoot.dataset.clearPendingEndpoint || "";
  var libraryEndpointTemplate = studioRoot.dataset.libraryEndpointTemplate || "";
  var csrfToken = studioRoot.dataset.csrfToken || "";

  // --- Category prompts ---
  var promptTemplates = {
    "kitchen":
      "Generate a square (1:1) photorealistic kitchen interior. The attached image is the primary geometric anchor. Place it inside a minimalist frame on a side wall viewed from an oblique three-quarter perspective. Preserve the attached asset exactly as a {aspect} artwork. Do not crop, warp, repaint, or stylize it. Build the kitchen's depth and daylight around the asset so it remains fully visible and naturally integrated.",
    "living-room":
      "Generate a square (1:1) photorealistic living room interior. The attached image is the primary geometric anchor. Place it inside a refined frame on a side wall viewed diagonally across the room. Preserve the attached asset exactly as a {aspect} artwork. Do not crop, warp, repaint, or stylize it. Expand the room composition around the artwork so it remains fully visible and architecturally grounded.",
    "bedroom":
      "Generate a square (1:1) photorealistic bedroom interior with the attached image as the immutable centerpiece. Place it inside a minimalist frame on a bedroom wall from a three-quarter camera angle. Preserve the attached asset exactly as a {aspect} artwork. Do not crop, warp, repaint, or stylize it. Build the room softly around the artwork with natural depth and lighting.",
    "office":
      "Generate a square (1:1) photorealistic office or study interior with the attached image as the primary geometric anchor. Place it inside a clean frame on the wall in a professional three-quarter composition. Preserve the attached asset exactly as a {aspect} artwork. Do not crop, warp, repaint, or stylize it. Build the room around the artwork with realistic perspective and restrained materials.",
    "dining-room":
      "Generate a square (1:1) photorealistic dining room interior. The attached image is the primary geometric anchor. Place it inside a minimalist frame near the dining setting from an oblique perspective. Preserve the attached asset exactly as a {aspect} artwork. Do not crop, warp, repaint, or stylize it. Let the room composition expand naturally around the artwork while keeping it fully visible.",
    "gallery":
      "Generate a square (1:1) photorealistic gallery-style interior. The attached image is the immutable centerpiece on a clean wall. Preserve the attached asset exactly as a {aspect} artwork. Do not crop, warp, repaint, or stylize it. Keep the presentation minimal, evenly lit, and architecturally composed so the artwork remains dominant and undisturbed.",
  };

  function buildPrompt(category, aspectValue) {
    var aspect = String(aspectValue || "4x5").replace("x", ":");
    var template = promptTemplates[category] || promptTemplates["gallery"];
    return template.replace("{aspect}", aspect);
  }

  // ----- Prompt textarea sync -----
  function syncPrompt() {
    if (promptDisplay) {
      var aspectSelect = studioRoot.querySelector("[data-basic-aspect]");
      promptDisplay.value = buildPrompt(categorySelect.value, aspectSelect ? aspectSelect.value : "4x5");
    }
  }
  categorySelect.addEventListener("change", syncPrompt);
  var basicAspectInput = studioRoot.querySelector("[data-basic-aspect]");
  if (basicAspectInput) {
    basicAspectInput.addEventListener("change", function () {
      syncPrompt();
      if (fileInput && fileInput.value) {
        fileInput.value = "";
      }
      updateFileName();
    });
  }
  syncPrompt();

  // ----- Dropzone -----
  dropzone.addEventListener("click", function () {
    fileInput.click();
  });
  dropzone.addEventListener("keydown", function (e) {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      fileInput.click();
    }
  });
  dropzone.addEventListener("dragover", function (e) {
    e.preventDefault();
    dropzone.classList.add("is-dragover");
  });
  dropzone.addEventListener("dragleave", function () {
    dropzone.classList.remove("is-dragover");
  });
  dropzone.addEventListener("drop", function (e) {
    e.preventDefault();
    dropzone.classList.remove("is-dragover");
    if (e.dataTransfer.files.length > 0) {
      fileInput.files = e.dataTransfer.files;
      updateFileName();
    }
  });
  fileInput.addEventListener("change", updateFileName);

  function updateFileName() {
    if (!fileName) {
      return;
    }
    fileName.textContent =
      fileInput.files.length > 0
        ? "Selected: " + fileInput.files[0].name
        : "Using auto-selected placeholder for " + (basicAspectInput ? basicAspectInput.value : "4x5") + ".";
  }

  // ----- Form submission -----
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    submitBtn.disabled = true;
    statusEl.textContent = "Queuing...";

    var formData = new FormData(form);
    fetch(queueEndpoint, { method: "POST", body: formData })
      .then(function (response) {
        var ct = response.headers.get("content-type") || "";
        if (!ct.includes("application/json")) {
          statusEl.textContent =
            "Error: Server returned non-JSON response (status " + response.status + ")";
          submitBtn.disabled = false;
          return null;
        }
        return response.json().then(function (data) {
          if (response.ok) {
            statusEl.textContent = data.message || "Queued successfully";
            fileInput.value = "";
            updateFileName();
            refreshJobs();
          } else {
            statusEl.textContent = "Error: " + (data.message || "Unknown error");
          }
          submitBtn.disabled = false;
        });
      })
      .catch(function (err) {
        statusEl.textContent = "Error: " + err.message;
        submitBtn.disabled = false;
      });
  });

  // ----- Refresh -----
  if (refreshBtn) {
    refreshBtn.addEventListener("click", refreshJobs);
  }

  function refreshJobs() {
    fetch(statusEndpoint)
      .then(function (r) {
        var ct = r.headers.get("content-type") || "";
        if (!ct.includes("application/json")) {
          console.error("Status endpoint returned non-JSON response");
          return null;
        }
        return r.json();
      })
      .then(function (data) {
        if (data && data.jobs) {
          renderJobs(data.jobs);
        }
      })
      .catch(function (err) {
        console.error("Failed to refresh jobs:", err);
      });
  }

  // ----- Clear pending -----
  if (clearPendingBtn) {
    clearPendingBtn.addEventListener("click", function () {
      if (!confirm("Delete all pending jobs? This cannot be undone.")) {
        return;
      }
      fetch(clearPendingEndpoint, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
      })
        .then(function (r) {
          return r.json();
        })
        .then(function () {
          refreshJobs();
        })
        .catch(function (err) {
          console.error("Error clearing pending:", err);
        });
    });
  }

  // ----- Render jobs -----
  function renderJobs(jobs) {
    cardsContainer.innerHTML = "";
    var recent = jobs.slice(0, 12);
    if (recent.length === 0) {
      emptyState.classList.add("is-visible");
      return;
    }
    emptyState.classList.remove("is-visible");
    recent.forEach(function (job) {
      cardsContainer.appendChild(createJobCard(job));
    });
  }

  function esc(str) {
    return String(str == null ? "" : str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function createJobCard(job) {
    var article = document.createElement("article");
    article.className = "studio-card";
    article.dataset.basicJobId = job.id;
    var meta =
      (job.prompt_text || "").substring(0, 60) +
      (job.prompt_text && job.prompt_text.length > 60 ? "…" : "");
    var label = esc(job.category) + " · " + esc(job.aspect_ratio) + " · v" + esc(job.variation_index);

    article.innerHTML =
      '<div class="studio-card__top">' +
        '<div>' +
          '<div class="studio-card__title">' + label + "</div>" +
          '<div class="studio-card__meta">' + esc(meta) + "</div>" +
        "</div>" +
        '<div class="studio-card__badge studio-card__badge--' +
          esc(job.status.toLowerCase()) + '">' + esc(job.status) + "</div>" +
      "</div>" +
      (job.image_url
        ? '<button class="studio-card__image-button" type="button"' +
            ' data-basic-carousel-trigger' +
            ' data-basic-image-url="' + esc(job.image_url) + '"' +
            ' data-basic-image-name="' + label + '">' +
            '<img src="' + esc(job.image_url) + '"' +
              ' alt="' + esc(job.category + " variation " + job.variation_index) + '"' +
              ' class="studio-card__image" loading="lazy">' +
          "</button>"
        : "") +
      '<div class="studio-card__actions">' +
        (job.image_url
          ? '<button class="gallery-btn gallery-btn--sm gallery-btn--outline" type="button"' +
              ' data-basic-view-prompt="' + esc(job.id) + '">📋 View Prompt</button>' +
            '<button class="gallery-btn gallery-btn--sm gallery-btn--outline" type="button"' +
              ' data-basic-add-to-library="' + esc(job.id) + '">➕ Add to Library</button>'
          : "") +
        '<button class="gallery-btn gallery-btn--sm gallery-btn--outline gallery-btn--danger"' +
          ' type="button" data-basic-delete="' + esc(job.id) + '">🗑 Delete</button>' +
      "</div>";

    return article;
  }

  // ----- Carousel modal -----
  function showCarousel(imageUrl, title) {
    var imageEl = carouselModal.querySelector("[data-basic-carousel-image]");
    var titleEl = carouselModal.querySelector("[data-basic-carousel-title]");
    if (imageEl) {
      imageEl.src = imageUrl;
    }
    if (titleEl) {
      titleEl.textContent = title || "Mockup";
    }
    carouselModal.dataset.visible = "1";
    carouselModal.setAttribute("aria-hidden", "false");
  }

  function closeCarousel() {
    if (!carouselModal) {
      return;
    }
    carouselModal.dataset.visible = "";
    carouselModal.setAttribute("aria-hidden", "true");
  }

  // ----- Prompt text modal -----
  function openTextModal(content) {
    var el = textModal.querySelector("[data-basic-prompt-modal-content]");
    if (el) {
      el.value = content || "No prompt text available.";
    }
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

  function viewPrompt(jobId) {
    openTextModal("Loading...");
    fetch(promptEndpointTemplate.replace("/0/full-prompt", "/" + jobId + "/full-prompt"))
      .then(function (r) {
        var ct = r.headers.get("content-type") || "";
        if (!ct.includes("application/json")) {
          openTextModal("Error: Server returned invalid response (status " + r.status + ")");
          return null;
        }
        return r.json();
      })
      .then(function (data) {
        if (data && data.full_prompt_compilation) {
          openTextModal(String(data.full_prompt_compilation));
        }
      })
      .catch(function (err) {
        openTextModal("Error loading prompt: " + err.message);
      });
  }

  function deleteJob(jobId) {
    if (!confirm("Delete this job and its output?")) {
      return;
    }
    fetch(deleteEndpointTemplate.replace("/0/delete", "/" + jobId + "/delete"), {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken },
    })
      .then(function (r) {
        if (!r.ok) {
          alert("Error deleting job: HTTP " + r.status);
          return null;
        }
        return r.json();
      })
      .then(function () {
        refreshJobs();
      })
      .catch(function (err) {
        alert("Error deleting job: " + err.message);
      });
  }

  function addToLibrary(jobId) {
    if (!libraryEndpointTemplate) {
      alert("Add to library feature coming soon!");
      return;
    }
    fetch(libraryEndpointTemplate.replace("/0/add-to-library", "/" + jobId + "/add-to-library"), {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken },
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        alert(data.message || "Added to library.");
        refreshJobs();
      })
      .catch(function (err) {
        alert("Error adding to library: " + err.message);
      });
  }

  // ----- Delegated card click handler -----
  cardsContainer.addEventListener("click", function (event) {
    var target = event.target;
    if (!(target instanceof Element)) {
      return;
    }

    var previewBtn = target.closest("[data-basic-carousel-trigger]");
    if (previewBtn) {
      event.preventDefault();
      var imageUrl = previewBtn.getAttribute("data-basic-image-url") || "";
      var imageName = previewBtn.getAttribute("data-basic-image-name") || "Mockup";
      if (imageUrl) {
        showCarousel(imageUrl, imageName);
      }
      return;
    }

    var promptBtn = target.closest("[data-basic-view-prompt]");
    if (promptBtn) {
      var jobId = Number(promptBtn.getAttribute("data-basic-view-prompt") || "0");
      if (jobId > 0) {
        viewPrompt(jobId);
      }
      return;
    }

    var deleteBtn = target.closest("[data-basic-delete]");
    if (deleteBtn) {
      var jobId = Number(deleteBtn.getAttribute("data-basic-delete") || "0");
      if (jobId > 0) {
        deleteJob(jobId);
      }
      return;
    }

    var addBtn = target.closest("[data-basic-add-to-library]");
    if (addBtn) {
      var jobId = Number(addBtn.getAttribute("data-basic-add-to-library") || "0");
      if (jobId > 0) {
        addToLibrary(jobId);
      }
    }
  });

  // ----- Modal close handlers -----
  var carouselCloseBtn = studioRoot.querySelector("[data-basic-carousel-close]");
  if (carouselCloseBtn) {
    carouselCloseBtn.addEventListener("click", closeCarousel);
  }

  var textCloseBtn = studioRoot.querySelector("[data-basic-text-close]");
  if (textCloseBtn) {
    textCloseBtn.addEventListener("click", closeTextModal);
  }

  carouselModal.addEventListener("click", function (e) {
    if (e.target === carouselModal) {
      closeCarousel();
    }
  });

  textModal.addEventListener("click", function (e) {
    if (e.target === textModal) {
      closeTextModal();
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      closeCarousel();
      closeTextModal();
    }
  });
})();
