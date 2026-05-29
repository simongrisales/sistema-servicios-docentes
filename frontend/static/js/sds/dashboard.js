(function () {
  // Importante: el envío del formulario del dashboard se hace con HTMX (hx-post).
  // Este archivo queda solo para UX (toasts) y para no interferir con el flujo de HTMX.
  const initDashboard = () => {
    const root = document.getElementById('main-app');
    if (!root) return;

    const form = root.querySelector('.reservation-form');
    if (!form) return;

    // HTMX emite eventos globales como htmx:beforeRequest y htmx:afterRequest.
    document.addEventListener('htmx:beforeRequest', (evt) => {
      if (evt.detail && evt.detail.elt !== form) return;
      if (window.sds?.toast?.show) {
        window.sds.toast.show({ type: 'info', message: 'Enviando solicitud...' });
      }
    });

    document.addEventListener('htmx:afterRequest', (evt) => {
      if (evt.detail && evt.detail.elt !== form) return;
      if (evt.detail && evt.detail.successful) {
        if (window.sds?.toast?.show) {
          window.sds.toast.show({ type: 'success', message: 'Solicitud enviada para validación.' });
        }
      } else {
        if (window.sds?.toast?.show) {
          window.sds.toast.show({ type: 'error', message: 'Error enviando la solicitud.' });
        }
      }
    });
  };

  document.addEventListener('DOMContentLoaded', initDashboard);
})();



