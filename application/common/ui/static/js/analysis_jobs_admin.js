(function () {
  'use strict';

  const root = document.querySelector('[data-jobs-admin]');
  if (!root) return;

  const tableBody = root.querySelector('[data-jobs-table-body]');
  const feedback = root.querySelector('[data-feedback]');
  const statusFilter = root.querySelector('[data-filter="status"]');
  const refreshButton = root.querySelector('[data-action="refresh"]');
  const csrf = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';

  function statusClass(status) {
    return String(status || '').toLowerCase();
  }

  function setFeedback(message) {
    if (feedback) {
      feedback.textContent = message || '';
    }
  }

  function formatDate(iso) {
    if (!iso) return '-';
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return '-';
    return d.toLocaleString();
  }

  function renderRows(jobs) {
    if (!tableBody) return;
    if (!jobs.length) {
      tableBody.innerHTML = '<tr><td colspan="9">No jobs found.</td></tr>';
      return;
    }

    tableBody.innerHTML = jobs.map((job) => {
      const status = String(job.status || '').toUpperCase();
      const canCancel = ['QUEUED', 'RUNNING', 'FAILED', 'DONE', 'CANCEL_REQUESTED'].includes(status);
      const shortJobId = String(job.job_id || '').slice(0, 8);
      return `
        <tr>
          <td><code title="${job.job_id || ''}">${shortJobId || '-'}</code></td>
          <td>${job.slug || '-'}</td>
          <td>${job.provider || '-'}</td>
          <td><span class="status-pill status-pill--${statusClass(status)}">${status || '-'}</span></td>
          <td>${job.stage || '-'}</td>
          <td>${job.progress ?? 0}%</td>
          <td>${job.attempts ?? 0}</td>
          <td>${formatDate(job.updated_at)}</td>
          <td>
            <div class="job-actions">
              <button type="button" class="btn btn-danger btn-sm" data-action="cancel" data-job-id="${job.job_id}" ${canCancel ? '' : 'disabled'}>
                Cancel + Cleanup
              </button>
            </div>
          </td>
        </tr>
      `;
    }).join('');

    tableBody.querySelectorAll('[data-action="cancel"]').forEach((button) => {
      button.addEventListener('click', () => {
        const jobId = button.getAttribute('data-job-id') || '';
        cancelJob(jobId);
      });
    });
  }

  async function loadJobs() {
    if (!tableBody) return;
    tableBody.innerHTML = '<tr><td colspan="9">Loading jobs...</td></tr>';

    const status = statusFilter?.value || '';
    const params = new URLSearchParams({ limit: '250' });
    if (status) params.set('status', status);

    try {
      const res = await fetch(`/api/jobs/admin/list?${params.toString()}`, {
        headers: { Accept: 'application/json' },
      });
      if (!res.ok) throw new Error('Failed to load jobs');
      const data = await res.json();
      renderRows(Array.isArray(data.jobs) ? data.jobs : []);
      setFeedback(`Showing ${data.count || 0} jobs`);
    } catch (err) {
      setFeedback(`Error loading jobs: ${err.message || 'Unknown error'}`);
      tableBody.innerHTML = '<tr><td colspan="9">Failed to load jobs.</td></tr>';
    }
  }

  async function cancelJob(jobId) {
    if (!jobId) return;
    const ok = window.confirm(`Cancel job ${jobId} and clean up generated files/DB records?`);
    if (!ok) return;

    setFeedback(`Cancelling ${jobId}...`);
    try {
      const res = await fetch(`/api/jobs/${encodeURIComponent(jobId)}/cancel`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrf,
          Accept: 'application/json',
        },
        body: JSON.stringify({
          cleanup: true,
          remove_artwork_record: true,
          csrf_token: csrf,
        }),
      });
      const data = await res.json();
      if (!res.ok || !data.ok) {
        throw new Error(data.error || data.message || 'Cancel failed');
      }
      setFeedback(data.message || 'Cancelled.');
      await loadJobs();
    } catch (err) {
      setFeedback(`Cancel failed: ${err.message || 'Unknown error'}`);
    }
  }

  refreshButton?.addEventListener('click', loadJobs);
  statusFilter?.addEventListener('change', loadJobs);

  loadJobs();
})();
