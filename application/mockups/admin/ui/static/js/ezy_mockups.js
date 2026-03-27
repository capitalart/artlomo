(function () {
  "use strict";

  var root = document.querySelector("[data-ezy-mockups]");
  if (!root) {
    return;
  }

  var form = root.querySelector("[data-ezy-form]");
  var promptInput = root.querySelector("[data-ezy-prompt]");
  var aspectInput = root.querySelector("[data-ezy-aspect]");
  var dropzone = root.querySelector("[data-ezy-dropzone]");
  var imageInput = root.querySelector("[data-ezy-image-input]");
  var fileName = root.querySelector("[data-ezy-file-name]");
  var submitBtn = root.querySelector("[data-ezy-submit]");
  var refreshBtn = root.querySelector("[data-ezy-refresh]");
  var statusEl = root.querySelector("[data-ezy-status]");
  var cards = root.querySelector("[data-ezy-cards]");
  var emptyState = root.querySelector("[data-ezy-empty-state]");

  var queueEndpoint = root.dataset.queueEndpoint || "";
  var statusEndpoint = root.dataset.statusEndpoint || "";
  var deleteEndpointTemplate = root.dataset.deleteEndpointTemplate || "";
  var csrfToken = root.dataset.csrfToken || "";
  var refreshTimer = null;
  var lastRenderSignature = "";
  var knownOutputByJob = {};

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
          harmonized: job && job.harmonized_image_url,
          updated: job && job.updated_at,
        };
      })
    );
  }

  function detectNewOutputs(jobs) {
    var hasNew = false;
    (jobs || []).forEach(function (job) {
      var id = String((job && job.id) || "");
      if (!id) {
        return;
      }
      var nowState = {
        room: Boolean(job && job.room_image_url),
        transparent: Boolean(job && job.transparent_image_url),
        harmonized: Boolean(job && job.harmonized_image_url),
      };
      var prevState = knownOutputByJob[id] || { room: false, transparent: false, harmonized: false };
      if ((!prevState.room && nowState.room) || (!prevState.transparent && nowState.transparent) || (!prevState.harmonized && nowState.harmonized)) {
        hasNew = true;
      }
      knownOutputByJob[id] = nowState;
    });
    return hasNew;
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
      article.dataset.ezyJobId = String(job.id || "");

      var title = escapeHtml(job.category) + " · " + escapeHtml(job.aspect_ratio) + " · v" + escapeHtml(job.variation_index);
      var meta = escapeHtml((job.prompt_text || "").substring(0, 60) + ((job.prompt_text || "").length > 60 ? "…" : ""));
      var status = escapeHtml(job.status || "Pending");
      var statusClass = escapeHtml(String(job.status || "pending").toLowerCase());
      var isVerified = Boolean(job.frame_coordinates_json);
      var verifierBadgeClass = isVerified ? "is-verified" : "is-manual-check";
      var verifierBadgeText = isVerified ? "Verified" : "Manual Check";

      var roomBlock = "";
      if (job.room_image_url) {
        roomBlock =
          '<div class="studio-card__meta">Room JPEG</div>' +
          '<img src="' + escapeHtml(job.room_image_url) + '" class="studio-card__image" alt="Room output" loading="lazy">';
      }

      var transparentBlock = "";
      if (job.transparent_image_url) {
        transparentBlock =
          '<div class="studio-card__meta">Transparent PNG</div>' +
          '<img src="' + escapeHtml(job.transparent_image_url) + '" class="studio-card__image" alt="Transparent template" loading="lazy">';
      }

      var downloadBtn = "";
      if (job.transparent_image_url) {
        downloadBtn =
          '<a class="gallery-btn gallery-btn--sm gallery-btn--outline" href="' +
          escapeHtml(job.transparent_image_url) +
          '" download>Download PNG</a>';
      }

      var verifierRaw = job.frame_coordinates_json || job.frame_coordinates_error || "No verifier data.";
      var verifierDrawer =
        '<details class="ezy-verifier-drawer">' +
          '<summary>Verifier Data</summary>' +
          '<pre class="ezy-verifier-json">' + escapeHtml(verifierRaw) + '</pre>' +
        '</details>';

      var resultPayload = job.result_details && typeof job.result_details === "object"
        ? job.result_details
        : {
            job_id: job.job_id || "",
            status: job.status || "",
            pipeline_stage: stage,
            error_message: job.error_message || "",
            frame_coordinates_error: job.frame_coordinates_error || "",
          };
      var resultDrawer =
        '<details class="ezy-result-drawer">' +
          '<summary>View Result</summary>' +
          '<pre class="ezy-verifier-json">' + escapeHtml(JSON.stringify(resultPayload, null, 2)) + '</pre>' +
        '</details>';

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

      var stage = job.pipeline_stage && typeof job.pipeline_stage === "object" ? job.pipeline_stage : {};
      var stageGen = escapeHtml(stage.gen || "Pending");
      var stageDetect = escapeHtml(stage.detect || "Pending");
      var stageComp = escapeHtml(stage.comp || "Pending");
      var stageHarmonize = escapeHtml(stage.harmonize || "Pending");
      var stageStrip =
        '<div class="ezy-stage-strip" aria-label="Pipeline stages">' +
          '<span class="ezy-stage-pill is-' + String(stageGen).toLowerCase() + '">Gen: ' + stageGen + '</span>' +
          '<span class="ezy-stage-pill is-' + String(stageDetect).toLowerCase() + '">Detect: ' + stageDetect + '</span>' +
          '<span class="ezy-stage-pill is-' + String(stageComp).toLowerCase() + '">Comp: ' + stageComp + '</span>' +
          '<span class="ezy-stage-pill is-' + String(stageHarmonize).toLowerCase() + '">Harmonize: ' + stageHarmonize + '</span>' +
        '</div>';

      article.innerHTML =
        '<div class="studio-card__top">' +
          '<div>' +
            '<div class="studio-card__title">' + title + '</div>' +
            '<div class="studio-card__meta">' + meta + '</div>' +
            stageStrip +
          '</div>' +
          '<div>' +
            '<div class="studio-card__badge studio-card__badge--' + statusClass + '">' + status + '</div>' +
            '<div class="ezy-verifier-badge ' + verifierBadgeClass + '">' + verifierBadgeText + '</div>' +
            failureReason +
          '</div>' +
        '</div>' +
        roomBlock +
        transparentBlock +
        verifierDrawer +
        resultDrawer +
        '<div class="studio-card__actions">' +
          downloadBtn +
          '<button class="gallery-btn gallery-btn--sm gallery-btn--outline gallery-btn--danger" type="button" data-ezy-delete="' + escapeHtml(job.id) + '">Delete</button>' +
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

        if (detectNewOutputs(jobs)) {
          setStatus("New mockup output received.");
        }

        if (hasActive) {
          scheduleRefresh(2500);
        } else {
          clearRefreshTimer();
        }
      })
      .catch(function (err) {
        console.error("Failed to refresh Ezy jobs:", err);
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

  if (refreshBtn) {
    refreshBtn.addEventListener("click", refreshJobs);
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    submitBtn.disabled = true;
    setStatus("Queueing Ezy-Mockup jobs...");

    var payload = new FormData(form);
    fetch(queueEndpoint, {
      method: "POST",
      body: payload,
      credentials: "same-origin",
      headers: { Accept: "application/json" },
    })
      .then(function (response) {
        return response.json().then(function (data) {
          return { response: response, data: data };
        });
      })
      .then(function (result) {
        if (!result.response.ok) {
          throw new Error((result.data && result.data.message) || "Queueing failed.");
        }
        renderJobs((result.data && result.data.jobs) || []);
        lastRenderSignature = buildRenderSignature((result.data && result.data.jobs) || []);
        setStatus((result.data && result.data.message) || "Queued successfully.");
        scheduleRefresh(1500);
      })
      .catch(function (err) {
        setStatus("Error: " + err.message);
      })
      .finally(function () {
        submitBtn.disabled = false;
      });
  });

  cards.addEventListener("click", function (event) {
    var target = event.target;
    if (!(target instanceof Element)) {
      return;
    }

    var deleteBtn = target.closest("[data-ezy-delete]");
    if (!deleteBtn) {
      return;
    }

    var jobId = Number(deleteBtn.getAttribute("data-ezy-delete") || "0");
    if (!jobId) {
      return;
    }

    if (!window.confirm("Delete this Ezy-Mockup job and outputs?")) {
      return;
    }

    fetch(deleteEndpointTemplate.replace("/0/delete", "/" + String(jobId) + "/delete"), {
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
        renderJobs(data.jobs || []);
        lastRenderSignature = buildRenderSignature(data.jobs || []);
      })
      .catch(function (err) {
        setStatus("Delete failed: " + err.message);
      });
  });

  updateFileName();
  if (cards.children.length === 0 && emptyState) {
    emptyState.classList.add("is-visible");
  }

  // Prime state and only auto-refresh while active jobs exist.
  refreshJobs();
})();
