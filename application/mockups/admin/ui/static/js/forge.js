(function () {
  const forgeForm = document.getElementById("forge-form");
  const jobList = document.getElementById("job-list");
  const feedback = document.getElementById("form-feedback");
  const lastUpdated = document.getElementById("last-updated");

  if (!forgeForm || !jobList || !feedback || !lastUpdated) {
    return;
  }

  function escapeHtml(value) {
    const str = String(value ?? "");
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function statusClass(status) {
    const normalized = String(status || "").toLowerCase();
    if (normalized === "pending") return "status-pending";
    if (normalized === "generating" || normalized === "processing") return "status-generating";
    if (normalized === "completed") return "status-completed";
    if (normalized === "failed") return "status-failed";
    return "status-pending";
  }

  function selectedCategories() {
    const checked = Array.from(document.querySelectorAll('input[name="category"]:checked'));
    return checked.map(function (item) {
      return item.value;
    });
  }

  function renderJobs(jobs) {
    if (!Array.isArray(jobs) || jobs.length === 0) {
      jobList.innerHTML = '<li class="empty">No forge jobs found</li>';
      return;
    }

    const html = jobs
      .map(function (job) {
        const id = escapeHtml(job.id);
        const category = escapeHtml(job.category);
        const descriptor = escapeHtml(job.shape_descriptor);
        const status = escapeHtml(job.status);
        const error = job.error_message ? escapeHtml(job.error_message) : "";

        return [
          '<li class="job-item">',
          '  <div class="job-top">',
          '    <span class="job-id">JOB #' + id + '</span>',
          '    <span class="job-status ' + statusClass(status) + '">' + status + '</span>',
          '  </div>',
          '  <div class="job-category">Category: ' + category + '</div>',
          '  <div class="job-descriptor">' + descriptor + '</div>',
          error ? '  <div class="error-line">' + error + '</div>' : "",
          '</li>'
        ].join("\n");
      })
      .join("\n");

    jobList.innerHTML = html;
  }

  async function pollStatus() {
    try {
      const response = await fetch("/admin/forge/status", {
        method: "GET",
        headers: {
          Accept: "application/json"
        }
      });

      if (!response.ok) {
        throw new Error("Status request failed with HTTP " + response.status);
      }

      const payload = await response.json();
      const jobs = Array.isArray(payload) ? payload : [];
      renderJobs(jobs);
      lastUpdated.textContent = "Last update: " + new Date().toLocaleTimeString();
    } catch (_error) {
      lastUpdated.textContent = "Last update: error";
      jobList.innerHTML = '<li class="empty">Unable to load queue status</li>';
    }
  }

  forgeForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    feedback.textContent = "";

    const descriptorInput = document.getElementById("shape_descriptor");
    const quantityInput = document.getElementById("quantity");

    const shapeDescriptor = (descriptorInput && "value" in descriptorInput ? descriptorInput.value : "").trim();
    const quantity = Number(quantityInput && "value" in quantityInput ? quantityInput.value : 0);
    const categories = selectedCategories();

    if (!shapeDescriptor) {
      feedback.textContent = "Shape descriptor is required.";
      return;
    }

    if (!Number.isInteger(quantity) || quantity < 1 || quantity > 50) {
      feedback.textContent = "Quantity must be an integer from 1 to 50.";
      return;
    }

    if (categories.length === 0) {
      feedback.textContent = "Select at least one category.";
      return;
    }

    try {
      const allJobIds = [];

      for (const category of categories) {
        const response = await fetch("/admin/forge/queue", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json"
          },
          body: JSON.stringify({
            category: category,
            shape_descriptor: shapeDescriptor,
            quantity: quantity
          })
        });

        const result = await response.json();

        if (!response.ok || !result.success) {
          throw new Error(result.message || "Queue request failed");
        }

        if (Array.isArray(result.job_ids)) {
          allJobIds.push.apply(allJobIds, result.job_ids);
        }
      }

      feedback.textContent =
        "Queued " +
        allJobIds.length +
        " job(s) across " +
        categories.length +
        " categor" +
        (categories.length === 1 ? "y." : "ies.");

      forgeForm.reset();
      const livingRoom = document.getElementById("cat-living-room");
      const quantityEl = document.getElementById("quantity");
      if (livingRoom && "checked" in livingRoom) {
        livingRoom.checked = true;
      }
      if (quantityEl && "value" in quantityEl) {
        quantityEl.value = "10";
      }
      await pollStatus();
    } catch (error) {
      feedback.textContent = error instanceof Error ? error.message : "Failed to queue jobs.";
    }
  });

  pollStatus();
  setInterval(pollStatus, 3000);
})();
