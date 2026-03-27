(function () {
  "use strict";

  var root = document.querySelector("[data-precision-mockups]");
  if (!root) {
    return;
  }

  var form = root.querySelector("[data-precision-form]");
  var promptInput = root.querySelector("[data-precision-prompt]");
  var aspectInput = root.querySelector("[data-precision-aspect]");
  var dropzone = root.querySelector("[data-precision-dropzone]");
  var imageInput = root.querySelector("[data-precision-image-input]");
  var fileName = root.querySelector("[data-precision-file-name]");
  var submitBtn = root.querySelector("[data-precision-submit]");
  var refreshBtn = root.querySelector("[data-precision-refresh]");
  var statusEl = root.querySelector("[data-precision-status]");
  var cards = root.querySelector("[data-precision-cards]");
  var emptyState = root.querySelector("[data-precision-empty-state]");

  var queueEndpoint = root.dataset.queueEndpoint || "";
  var statusEndpoint = root.dataset.statusEndpoint || "";
  var deleteEndpointTemplate = root.dataset.deleteEndpointTemplate || "";
  var csrfToken = root.dataset.csrfToken || "";
  var refreshTimer = null;
  var lastRenderSignature = "";

  if (!form || !promptInput || !dropzone || !imageInput || !submitBtn || !statusEl || !cards) {
    return;
  }

  function setStatus(message) {
    statusEl.textContent = message || "";
  }

  function clearRefreshTimer() {
    if (refreshTimer) {
      window.clearTimeout(refreshTimer);
      refreshTimer = null;
    }
  }

  function scheduleRefresh(delayMs) {
    clearRefreshTimer();
    refreshTimer = window.setTimeout(function () {
      refreshJobs();
    }, Math.max(1000, Number(delayMs || 3000)));
  }

  function isActiveStatus(status) {
    var value = String(status || "").toLowerCase();
    return value === "pending" || value === "generating" || value === "processing";
  }

  function buildRenderSignature(jobs) {
    return JSON.stringify(
      (jobs || []).map(function (job) {
        return {
          id: job && job.id,
          status: job && job.status,
          room: job && job.room_image_url,
          transparent: job && job.transparent_image_url,
          updated: job && job.updated_at,
          coords: job && job.frame_coordinates_json,
        };
      })
    );
  }

  function updateFileName() {
    if (!fileName) {
      return;
    }
    if (imageInput.files && imageInput.files.length > 0) {
      fileName.textContent = "Selected: " + imageInput.files[0].name;
      return;
    }
    var aspect = aspectInput ? String(aspectInput.value || "4x5") : "4x5";
    fileName.textContent = "Using auto-selected placeholder for " + aspect + ".";
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function overlayMarkup(job) {
    var points = Array.isArray(job.frame_overlay_points) ? job.frame_overlay_points.filter(Boolean) : [];
    var width = Number(job.image_width || 0);
    var height = Number(job.image_height || 0);
    if (!points.length || !width || !height) {
      return "";
    }

    var pointString = points.map(function (point) {
      return String(point[0]) + "," + String(point[1]);
    }).join(" ");

    var circles = points.map(function (point) {
      return '<circle cx="' + escapeHtml(point[0]) + '" cy="' + escapeHtml(point[1]) + '" r="12" class="precision-overlay-point"></circle>';
    }).join("");

    return (
      '<svg class="precision-overlay-svg" viewBox="0 0 ' + escapeHtml(width) + ' ' + escapeHtml(height) + '" preserveAspectRatio="none" aria-hidden="true">' +
        '<polygon points="' + escapeHtml(pointString) + '" class="precision-overlay-polygon"></polygon>' +
        circles +
      '</svg>'
    );
  }

  function renderJobs(rows) {
    var jobs = Array.isArray(rows) ? rows : [];
    cards.innerHTML = "";

    if (!jobs.length) {
      if (emptyState) {
        emptyState.classList.add("is-visible");
      }
      return;
    }

    if (emptyState) {
      emptyState.classList.remove("is-visible");
    }

    jobs.forEach(function (job) {
      var article = document.createElement("article");
      article.className = "studio-card";
      article.dataset.precisionJobId = String(job.id || "");

      var title = escapeHtml(job.category) + " · " + escapeHtml(job.aspect_ratio);
      var meta = escapeHtml((job.prompt_text || "").substring(0, 80) + ((job.prompt_text || "").length > 80 ? "…" : ""));
      var status = escapeHtml(job.status || "Pending");
      var statusClass = escapeHtml(String(job.status || "pending").toLowerCase());
      var failureReason = "";
      if (job.error_message) {
        var shortReason = String(job.error_message);
        if (shortReason.length > 90) {
          shortReason = shortReason.substring(0, 90) + "...";
        }
        failureReason =
          '<div class="ezy-failure-reason" title="' + escapeHtml(job.error_message) + '">' +
            'Failure: ' + escapeHtml(shortReason) +
          '</div>';
      }

      var roomBlock = "";
      if (job.room_image_url) {
        roomBlock =
          '<div class="studio-card__meta">Composite Room JPEG</div>' +
          '<div class="precision-overlay-frame">' +
            '<img src="' + escapeHtml(job.room_image_url) + '" class="studio-card__image" alt="Precision room output" loading="lazy">' +
            overlayMarkup(job) +
          '</div>';
      }

      var transparentBlock = "";
      if (job.transparent_image_url) {
        transparentBlock =
          '<div class="studio-card__meta">Transparent PNG</div>' +
          '<img src="' + escapeHtml(job.transparent_image_url) + '" class="studio-card__image" alt="Precision transparent output" loading="lazy">';
      }

      var downloadBtn = "";
      if (job.transparent_image_url) {
        downloadBtn =
          '<a class="gallery-btn gallery-btn--sm gallery-btn--outline" href="' +
          escapeHtml(job.transparent_image_url) +
          '" download>Download PNG</a>';
      }

      var resultPayload = job.result_details && typeof job.result_details === "object"
        ? job.result_details
        : {};

      article.innerHTML =
        '<div class="studio-card__top">' +
          '<div>' +
            '<div class="studio-card__title">' + title + '</div>' +
            '<div class="studio-card__meta">' + meta + '</div>' +
          '</div>' +
          '<div>' +
            '<div class="studio-card__badge studio-card__badge--' + statusClass + '">' + status + '</div>' +
            failureReason +
          '</div>' +
        '</div>' +
        roomBlock +
        transparentBlock +
        '<details class="ezy-result-drawer">' +
          '<summary>Detection Data</summary>' +
          '<pre class="ezy-verifier-json">' + escapeHtml(JSON.stringify(resultPayload, null, 2)) + '</pre>' +
        '</details>' +
        '<div class="studio-card__actions">' +
          downloadBtn +
          '<button class="gallery-btn gallery-btn--sm gallery-btn--outline gallery-btn--danger" type="button" data-precision-delete="' + escapeHtml(job.id) + '">Delete</button>' +
        '</div>';

      cards.appendChild(article);
    });
  }

  function refreshJobs() {
    fetch(statusEndpoint, {
      method: "GET",
      credentials: "same-origin",
      headers: { Accept: "application/json" },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        var jobs = (data && data.jobs) || [];
        var signature = buildRenderSignature(jobs);
        var hasActive = jobs.some(function (job) {
          return isActiveStatus(job && job.status);
        });

        if (signature !== lastRenderSignature) {
          renderJobs(jobs);
          lastRenderSignature = signature;
        }

        if (hasActive) {
          scheduleRefresh(2500);
        } else {
          clearRefreshTimer();
        }
      })
      .catch(function (err) {
        console.error("Failed to refresh Precision jobs:", err);
        scheduleRefresh(5000);
      });
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

  imageInput.addEventListener("change", updateFileName);

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
    var files = event.dataTransfer && event.dataTransfer.files ? event.dataTransfer.files : null;
    if (!files || !files.length) {
      return;
    }
    var dt = new DataTransfer();
    dt.items.add(files[0]);
    imageInput.files = dt.files;
    updateFileName();
  });

  if (aspectInput) {
    aspectInput.addEventListener("change", function () {
      if (imageInput && imageInput.value) {
        imageInput.value = "";
      }
      updateFileName();
    });
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    submitBtn.disabled = true;
    setStatus("Queueing Precision Mockup...");

    var formData = new FormData(form);
    fetch(queueEndpoint, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    })
      .then(function (response) {
        return response.json().then(function (data) {
          return { ok: response.ok, data: data };
        });
      })
      .then(function (payload) {
        if (!payload.ok || !payload.data || payload.data.status === "error") {
          throw new Error((payload.data && payload.data.message) || "Failed to queue Precision Mockup.");
        }

        setStatus(payload.data.message || "Precision Mockup queued.");
        if (Array.isArray(payload.data.jobs)) {
          renderJobs(payload.data.jobs);
          lastRenderSignature = buildRenderSignature(payload.data.jobs);
        }
        scheduleRefresh(1500);
      })
      .catch(function (err) {
        console.error(err);
        setStatus(err && err.message ? err.message : "Failed to queue Precision Mockup.");
      })
      .finally(function () {
        submitBtn.disabled = false;
      });
  });

  refreshBtn.addEventListener("click", function () {
    setStatus("Refreshing jobs...");
    refreshJobs();
  });

  cards.addEventListener("click", function (event) {
    var target = event.target;
    if (!(target instanceof HTMLElement)) {
      return;
    }

    var deleteId = target.getAttribute("data-precision-delete");
    if (!deleteId) {
      return;
    }

    var deleteEndpoint = deleteEndpointTemplate.replace(/0$/, String(deleteId));
    fetch(deleteEndpoint, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        Accept: "application/json",
        "X-CSRFToken": csrfToken,
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data && Array.isArray(data.jobs)) {
          renderJobs(data.jobs);
          lastRenderSignature = buildRenderSignature(data.jobs);
        }
      })
      .catch(function (err) {
        console.error("Failed to delete Precision Mockup:", err);
      });
  });

  updateFileName();
  refreshJobs();
})();