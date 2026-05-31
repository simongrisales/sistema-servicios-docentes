(function () {
  window.sds = window.sds || {};

  window.sds.toast = {
    show: (data) => {
      // Compat con implementation actual de frontend-ui.js
      if (typeof window.showToast === 'function') {
        window.showToast(data);
        return;
      }

      const toast = document.getElementById('notification-toast');
      const message = document.getElementById('notification-toast-message');
      const dot = document.getElementById('notification-toast-dot');
      const closeButtons = document.querySelectorAll('[data-toast-close]');

      if (!toast || !message || !dot) return;

      closeButtons.forEach((button) => {
        if (button.dataset.toastBound === 'true') {
          return;
        }
        button.dataset.toastBound = 'true';
        button.addEventListener('click', (event) => {
          event.preventDefault();
          window.hideToast && window.hideToast();
        });
      });

      dot.className = `toast-dot ${(data && data.type) || 'info'}`;
      message.textContent = (data && data.message) || '';
      toast.hidden = false;

      window.clearTimeout(window.toastTimer);
      window.toastTimer = window.setTimeout(() => window.hideToast && window.hideToast(), 6000);
    },
  };
})();

