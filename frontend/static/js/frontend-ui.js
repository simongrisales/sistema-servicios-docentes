document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    document.querySelectorAll("[data-sidebar-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            sidebar?.classList.toggle("is-open");
        });
    });

    const navbarMenuButtons = Array.from(document.querySelectorAll("[data-navbar-menu-toggle]"));
    const navbarMenus = Array.from(document.querySelectorAll("[data-navbar-menu]"));

    const closeNavbarMenus = () => {
        navbarMenuButtons.forEach((button) => {
            button.setAttribute("aria-expanded", "false");
        });
        navbarMenus.forEach((menu) => {
            menu.hidden = true;
        });
    };

    const openNavbarMenu = (menuName) => {
        navbarMenus.forEach((menu) => {
            menu.hidden = menu.dataset.navbarMenu !== menuName;
        });
        navbarMenuButtons.forEach((button) => {
            button.setAttribute(
                "aria-expanded",
                button.dataset.navbarMenuToggle === menuName ? "true" : "false"
            );
        });
    };

    navbarMenuButtons.forEach((button) => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            const menuName = button.dataset.navbarMenuToggle;
            const targetMenu = navbarMenus.find((menu) => menu.dataset.navbarMenu === menuName);
            if (!targetMenu) {
                return;
            }

            const shouldOpen = targetMenu.hidden;
            closeNavbarMenus();
            if (shouldOpen) {
                openNavbarMenu(menuName);
            }
        });
    });

    const sidebarLinks = Array.from(document.querySelectorAll(".sidebar-link[href^='#']"));
    const syncSidebarActive = () => {
        if (!sidebarLinks.length) {
            return;
        }
        const targetHash = window.location.hash || sidebarLinks[0].getAttribute("href") || "";
        sidebarLinks.forEach((link) => {
            link.classList.toggle("is-active", link.getAttribute("href") === targetHash);
        });
    };

    sidebarLinks.forEach((link) => {
        link.addEventListener("click", () => {
            window.requestAnimationFrame(syncSidebarActive);
            sidebar?.classList.remove("is-open");
        });
    });

    window.addEventListener("hashchange", syncSidebarActive);
    syncSidebarActive();

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
        const hash = window.location.hash.replace("#", "");
        if (hash) setView(hash);
    }

    const focusTargetForQuickAction = (hash) => {
        if (!hash || hash.charAt(0) !== "#") {
            return;
        }

        const target = document.querySelector(hash);
        if (!target) {
            return;
        }

        if (typeof target.scrollIntoView === "function") {
            target.scrollIntoView({ behavior: "smooth", block: "start" });
        }

        const preferredFocus =
            target.querySelector("input, select, textarea, button") ||
            target.parentElement?.querySelector("input, select, textarea, button");
        if (preferredFocus && typeof preferredFocus.focus === "function") {
            window.setTimeout(() => preferredFocus.focus({ preventScroll: true }), 120);
        }
    };

    document.addEventListener("click", (event) => {
        const quickAction = event.target.closest?.("[data-quick-action]");
        if (quickAction) {
            const href = quickAction.getAttribute("href") || "";
            if (href.startsWith("#")) {
                event.preventDefault();
                window.location.hash = href;
                focusTargetForQuickAction(href);
            }
        }

        const closeButton = event.target.closest?.("[data-toast-close]");
        if (closeButton) {
            event.preventDefault();
            window.hideToast();
            return;
        }

        const insideNavbar = event.target.closest?.("[data-navbar-menu], [data-navbar-menu-toggle]");
        if (!insideNavbar) {
            closeNavbarMenus();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeNavbarMenus();
        }
    });

    document.querySelectorAll("[data-navbar-refresh]").forEach((button) => {
        button.addEventListener("click", () => {
            closeNavbarMenus();
            window.dispatchEvent(
                new CustomEvent("sds:catalog-changed", {
                    detail: { tipo: "refresh_manual" },
                })
            );
        });
    });

    document.querySelectorAll("[data-toast-close]").forEach((button) => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            window.hideToast();
        });
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
    if (window.toastTimer) {
        window.clearTimeout(window.toastTimer);
        window.toastTimer = null;
    }
    if (toast) {
        toast.hidden = true;
    }
};
