(function () {
  function applyCollapsed(isCollapsed) {
    document.body.classList.toggle('sidebar-collapsed', isCollapsed);
    var btn = document.querySelector('[data-sidebar-toggle]');
    if (btn) {
      btn.setAttribute('aria-label', isCollapsed ? 'Expand sidebar' : 'Collapse sidebar');
    }
  }

  function applyMobileOpen(isOpen) {
    document.body.classList.toggle('sidebar-mobile-open', isOpen);
    var btn = document.querySelector('[data-sidebar-mobile-toggle]');
    if (btn) {
      btn.setAttribute('aria-label', isOpen ? 'Close sidebar' : 'Open sidebar');
    }
    var backdrop = document.querySelector('[data-sidebar-backdrop]');
    if (backdrop) {
      backdrop.setAttribute('aria-hidden', isOpen ? 'false' : 'true');
    }
  }

  function readState() {
    try {
      return localStorage.getItem('artlomo.sidebarCollapsed') === '1';
    } catch (e) {
      return false;
    }
  }

  function writeState(isCollapsed) {
    try {
      localStorage.setItem('artlomo.sidebarCollapsed', isCollapsed ? '1' : '0');
    } catch (e) {
      // ignore
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    applyCollapsed(readState());

    applyMobileOpen(false);

    var mobileBtn = document.querySelector('[data-sidebar-mobile-toggle]');
    if (mobileBtn) {
      mobileBtn.addEventListener('click', function () {
        var next = !document.body.classList.contains('sidebar-mobile-open');
        applyMobileOpen(next);
      });
    }

    var backdrop = document.querySelector('[data-sidebar-backdrop]');
    if (backdrop) {
      backdrop.addEventListener('click', function () {
        applyMobileOpen(false);
      });
    }

    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') applyMobileOpen(false);
    });

    var btn = document.querySelector('[data-sidebar-toggle]');
    if (!btn) return;

    btn.addEventListener('click', function () {
      var next = !document.body.classList.contains('sidebar-collapsed');
      applyCollapsed(next);
      writeState(next);
    });
  });
})();
