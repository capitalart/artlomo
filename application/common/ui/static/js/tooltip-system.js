/**
 * ArtLomo Tooltip System
 *
 * Provides contextual help tooltips triggered by help icons.
 *
 * Usage:
 * <button class="help-icon" data-tooltip-trigger="field-name-help">?</button>
 * <div class="tooltip-content" id="field-name-help" hidden>Content</div>
 */

(function() {
  'use strict';

  let activeTooltip = null;

  function positionTooltip(tooltip, trigger) {
    const triggerRect = trigger.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    let top = triggerRect.bottom + 8;
    let left = triggerRect.left;

    // Adjust if tooltip would overflow right edge
    if (left + tooltipRect.width > viewportWidth - 20) {
      left = viewportWidth - tooltipRect.width - 20;
    }

    // Adjust if tooltip would overflow bottom edge
    if (top + tooltipRect.height > viewportHeight - 20) {
      top = triggerRect.top - tooltipRect.height - 8;
    }

    // Ensure minimum left margin
    if (left < 20) {
      left = 20;
    }

    tooltip.style.top = `${top}px`;
    tooltip.style.left = `${left}px`;
  }

  function showTooltip(tooltip, trigger) {
    // Hide any active tooltip
    hideAllTooltips();

    // Show and position new tooltip
    tooltip.classList.add('active');
    tooltip.removeAttribute('hidden');

    // Position after display to get accurate dimensions
    requestAnimationFrame(() => {
      positionTooltip(tooltip, trigger);
    });

    activeTooltip = tooltip;
  }

  function hideTooltip(tooltip) {
    if (tooltip) {
      tooltip.classList.remove('active');
      tooltip.setAttribute('hidden', '');
    }
  }

  function hideAllTooltips() {
    document.querySelectorAll('.tooltip-content.active').forEach(tooltip => {
      hideTooltip(tooltip);
    });
    activeTooltip = null;
  }

  function initTooltipSystem() {
    const triggers = document.querySelectorAll('[data-tooltip-trigger]');

    triggers.forEach(trigger => {
      const tooltipId = trigger.getAttribute('data-tooltip-trigger');
      const tooltip = document.getElementById(tooltipId);

      if (!tooltip) {
        console.warn(`Tooltip content not found: ${tooltipId}`);
        return;
      }

      // Click handler for trigger
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();

        if (activeTooltip === tooltip) {
          hideTooltip(tooltip);
          activeTooltip = null;
        } else {
          showTooltip(tooltip, trigger);
        }
      });

      // Optional: Close button inside tooltip
      const closeBtn = tooltip.querySelector('.tooltip-close');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => {
          hideTooltip(tooltip);
          activeTooltip = null;
        });
      }

      // Keyboard accessibility
      trigger.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          trigger.click();
        }
      });
    });

    // Close tooltips on outside click
    document.addEventListener('click', (e) => {
      if (!e.target.closest('[data-tooltip-trigger]') &&
          !e.target.closest('.tooltip-content')) {
        hideAllTooltips();
      }
    });

    // Close tooltips on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        hideAllTooltips();
      }
    });

    // Reposition on window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (activeTooltip) {
          const trigger = document.querySelector(
            `[data-tooltip-trigger="${activeTooltip.id}"]`
          );
          if (trigger) {
            positionTooltip(activeTooltip, trigger);
          }
        }
      }, 150);
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTooltipSystem);
  } else {
    initTooltipSystem();
  }

  // Expose global function for dynamic content
  window.ArtLomoTooltips = {
    init: initTooltipSystem,
    hideAll: hideAllTooltips
  };
})();
