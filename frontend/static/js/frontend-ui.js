document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    document.querySelectorAll("[data-sidebar-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            sidebar?.classList.toggle("is-open");
        });
    });

    const navbarMenuButtons = Array.from(document.querySelectorAll("[data-navbar-menu-toggle]"));
    const navbarMenus = Array.from(document.querySelectorAll("[data-navbar-menu]"));
    const notificationBadge = document.getElementById("notification-count-badge");

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

    const initCollapsibleCards = () => {
        const cards = Array.from(document.querySelectorAll(".dashboard-shell .card"));
        cards.forEach((card, index) => {
            if (card.classList.contains("metric-card")) {
                return;
            }

            if (card.dataset.collapseReady === "true") {
                return;
            }

            const header = card.querySelector(".card-header");
            const hasMeaningfulContent = card.querySelector("form, table, .stack, .alert, .table-wrap");
            if (!header || !hasMeaningfulContent) {
                return;
            }

            card.dataset.collapseReady = "true";
            const storageKey = `sds-card-collapse:${card.id || index}`;
            const toggle = document.createElement("button");
            toggle.type = "button";
            toggle.className = "card-collapse-toggle";
            toggle.setAttribute("aria-expanded", "true");

            const applyState = (collapsed) => {
                card.classList.toggle("is-collapsed", collapsed);
                toggle.setAttribute("aria-expanded", collapsed ? "false" : "true");
                toggle.textContent = collapsed ? "Mostrar" : "Ocultar";
                try {
                    window.localStorage.setItem(storageKey, collapsed ? "1" : "0");
                } catch (_) {
                    // No-op: el panel sigue funcionando aunque no haya storage.
                }
            };

            toggle.addEventListener("click", () => {
                applyState(!card.classList.contains("is-collapsed"));
            });

            const label = card.querySelector(".card-title")?.textContent?.trim() || "Seccion";
            toggle.setAttribute("aria-label", `Ocultar o mostrar ${label}`);
            header.appendChild(toggle);

            let collapsed = false;
            try {
                collapsed = window.localStorage.getItem(storageKey) === "1";
            } catch (_) {
                collapsed = false;
            }
            applyState(collapsed);
        });
    };

    const getNotificationCount = () => {
        if (!notificationBadge) {
            return 0;
        }
        return Number.parseInt(notificationBadge.textContent || "0", 10) || 0;
    };

    const setNotificationCount = (nextCount) => {
        if (!notificationBadge) {
            return;
        }
        notificationBadge.textContent = String(Math.max(0, Number.parseInt(nextCount, 10) || 0));
    };

    const bindToastCloseButtons = () => {
        document.querySelectorAll("[data-toast-close]").forEach((button) => {
            if (button.dataset.toastBound === "true") {
                return;
            }
            button.dataset.toastBound = "true";
            button.addEventListener("click", (event) => {
                event.preventDefault();
                window.hideToast();
            });
        });
    };

    const ensureNotificationEmptyState = () => {
        const menu = document.getElementById("navbar-notifications-menu");
        if (!menu || menu.querySelector("[data-notification-empty]")) {
            return;
        }

        const emptyState = document.createElement("p");
        emptyState.className = "navbar-notification-empty";
        emptyState.dataset.notificationEmpty = "true";
        emptyState.textContent = "Sin notificaciones nuevas.";

        const firstAction = menu.querySelector(".navbar-menu__action");
        menu.insertBefore(emptyState, firstAction || null);
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

        const deleteButton = event.target.closest?.("[data-notification-delete]");
        if (deleteButton) {
            event.preventDefault();

            const notificationId = deleteButton.getAttribute("data-notification-delete");
            if (!notificationId || !window.sds?.apiClient?.del) {
                return;
            }

            deleteButton.disabled = true;
            window.sds.apiClient
                .del(`/api/notificaciones/${notificationId}/`)
                .then(() => {
                    const item = deleteButton.closest?.("[data-notification-item]");
                    if (item) {
                        item.remove();
                    }

                    setNotificationCount(getNotificationCount() - 1);

                    if (!document.querySelector("[data-notification-item]")) {
                        ensureNotificationEmptyState();
                    }
                })
                .catch(() => {
                    deleteButton.disabled = false;
                    window.sds?.toast?.show?.({
                        type: "error",
                        message: "No fue posible eliminar la notificacion.",
                    });
                });
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

    bindToastCloseButtons();

    initCollapsibleCards();
});

window.showToast = function (data) {
    const toast = document.getElementById("notification-toast");
    const message = document.getElementById("notification-toast-message");
    const dot = document.getElementById("notification-toast-dot");

    if (!toast || !message || !dot) {
        return;
    }

    document.querySelectorAll("[data-toast-close]").forEach((button) => {
        if (button.dataset.toastBound === "true") {
            return;
        }
        button.dataset.toastBound = "true";
        button.addEventListener("click", (event) => {
            event.preventDefault();
            window.hideToast();
        });
    });

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
