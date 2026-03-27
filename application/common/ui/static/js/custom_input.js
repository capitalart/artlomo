document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.seed-form');
  const root = document.getElementById('customInputApp');
  if (!form || !root) {
    return;
  }

  const formAction = form.getAttribute('action') || '';
  const slug = root.getAttribute('data-slug') || '';
  const unprocessedUrl = root.getAttribute('data-unprocessed-url') || '/artworks/unprocessed';

  form.addEventListener('submit', async (e) => {
    const submitter = e.submitter;
    const action = submitter ? submitter.getAttribute('data-action') : null;

    if (action === 'save_only' || !action) {
      return;
    }

    if (action !== 'analyze_openai' && action !== 'analyze_gemini') {
      return;
    }

    e.preventDefault();

    const provider = action === 'analyze_openai' ? 'OpenAI' : 'Gemini';
    const providerLower = provider.toLowerCase();

    try {
      const handleCancel = () => {
        window.location.href = unprocessedUrl;
      };

      AnalysisLoader.show(provider, handleCancel);

      const formData = new FormData(form);
      const response = await fetch(formAction, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to save context and start analysis');
      }

      const maxWaitMs = 300000;
      const startTime = Date.now();
      const checkInterval = 1000;

      const pollAnalysis = setInterval(async () => {
        const elapsed = Date.now() - startTime;

        if (elapsed > maxWaitMs) {
          clearInterval(pollAnalysis);
          AnalysisLoader.showError('Analysis took too long to complete. Please try again.');
          return;
        }

        try {
          const statusResponse = await fetch(`/api/analysis/status/${slug}?provider=${providerLower}`);
          if (!statusResponse.ok) return;

          const statusData = await statusResponse.json();

          if (statusData.error || statusData.stage === 'error') {
            clearInterval(pollAnalysis);
            AnalysisLoader.showError(statusData.error || statusData.message || 'Analysis failed with an unknown error');
            return;
          }

          if (statusData.done === true) {
            clearInterval(pollAnalysis);
            AnalysisLoader.hide();
            window.location.href = `/artwork/${slug}/review/${providerLower}`;
          }
        } catch (err) {
          console.error('Poll error:', err);
        }
      }, checkInterval);
    } catch (err) {
      AnalysisLoader.hide();
      alert('Error: ' + (err && err.message ? err.message : 'Unknown error'));
    }
  });
});
