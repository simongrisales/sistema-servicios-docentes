document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    document.querySelectorAll("[data-sidebar-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            sidebar?.classList.toggle("is-open");
        });
    });

    const viewButtons = document.querySelectorAll("[data-dashboard-view]");
    const panels = document.querySelectorAll("[data-dashboard-panel]");

    const setView = (view) => {
        if (!view) return;

        viewButtons.forEach((item) => item.classList.remove("is-active"));
        viewButtons.forEach((item) => {
            if (item.dataset.dashboardView === view) {
                item.classList.add("is-active");
            }
        });

        panels.forEach((panel) => {
            panel.classList.toggle("is-hidden", panel.dataset.dashboardPanel !== view);
        });
    };

    viewButtons.forEach((button) => {
        button.addEventListener("click", (e) => {
            const view = button.dataset.dashboardView;
            // Si es un link, no navega: solo cambia vista.
            e.preventDefault();
            setView(view);
        });
    });

    // Soporta deep-link por hash: #form o #calendar
    if (window.location.hash) {
        const hash = window.location.hash.replace('#', '');
        if (hash) setView(hash);
    }


    document.querySelectorAll("[data-toast-close]").forEach((button) => {
        button.addEventListener("click", () => window.hideToast());
    });
});

window.showToast = function (data) {
    const toast = document.getElementById("notification-toast");
    const message = document.getElementById("notification-toast-message");
    const dot = document.getElementById("notification-toast-dot");

    if (!toast || !message || !dot) {
        return;
    }

    dot.className = `toast-dot ${data?.type || "info"}`;
    message.textContent = data?.message || "";
    toast.hidden = false;

    window.clearTimeout(window.toastTimer);
    window.toastTimer = window.setTimeout(() => window.hideToast(), 6000);
};

window.hideToast = function () {
    const toast = document.getElementById("notification-toast");
    if (toast) {
        toast.hidden = true;
    }
};
