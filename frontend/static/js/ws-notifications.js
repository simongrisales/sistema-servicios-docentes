(function () {
    const connect = () => {
        if (!window.WebSocket) {
            return;
        }

        const protocol = window.location.protocol === "https:" ? "wss" : "ws";
        const socketUrl = `${protocol}://${window.location.host}/ws/notificaciones/`;
        const disponibilidadUrl = `${protocol}://${window.location.host}/ws/disponibilidad-aulas/`;
        const progresoUrl = `${protocol}://${window.location.host}/ws/asignacion/progreso/`;
        const syncUrl = `${protocol}://${window.location.host}/ws/panel/sync/`;

        const emitRefreshEvent = (payload) => {
            window.dispatchEvent(
                new CustomEvent("sds:catalog-changed", {
                    detail: payload || {},
                })
            );
        };

        const getNotificationList = () => {
            const existing = document.querySelector("[data-notification-list]");
            if (existing) {
                return existing;
            }

            const menu = document.getElementById("navbar-notifications-menu");
            if (!menu) {
                return null;
            }

            const list = document.createElement("div");
            list.className = "navbar-notification-list";
            list.dataset.notificationList = "true";

            const emptyState = menu.querySelector("[data-notification-empty]");
            if (emptyState) {
                emptyState.remove();
            }

            const firstAction = menu.querySelector(".navbar-menu__action");
            menu.insertBefore(list, firstAction || null);
            return list;
        };

        const prependNotificationItem = (payload) => {
            if (!payload?.id) {
                return;
            }

            if (document.querySelector(`[data-notification-item][data-notification-id="${payload.id}"]`)) {
                return;
            }

            const list = getNotificationList();
            if (!list) {
                return;
            }

            const item = document.createElement("div");
            item.className = "navbar-notification-item";
            item.dataset.notificationItem = "true";
            item.dataset.notificationId = payload.id;
            item.innerHTML = `
                <div class="navbar-notification-item__body">
                    <p class="navbar-notification-item__title">${payload.title || "Notificacion"}</p>
                    <p class="navbar-notification-item__message">${payload.message || ""}</p>
                    <p class="navbar-notification-item__meta">${new Date().toLocaleString("es-CO", {
                        dateStyle: "short",
                        timeStyle: "short",
                    })}</p>
                </div>
                <button
                    class="navbar-notification-delete"
                    type="button"
                    data-notification-delete="${payload.id}"
                    aria-label="Eliminar notificacion ${payload.title || "nueva"}"
                >
                    &times;
                </button>
            `;

            list.prepend(item);
            window.sds?.bindNotificationDeleteButtons?.();
        };

        try {
            const socket = new WebSocket(socketUrl);

            socket.addEventListener("message", (event) => {
                let payload = {};
                try {
                    payload = JSON.parse(event.data);
                } catch (error) {
                    payload = { message: event.data };
                }

                const countBadge = document.getElementById("notification-count-badge");
                if (payload.tipo === "notification" && countBadge) {
                    const currentCount = Number.parseInt(countBadge.textContent || "0", 10) || 0;
                    countBadge.textContent = String(payload.unread_count || currentCount + 1);
                }

                if (payload.tipo === "notification" && typeof window.showToast === "function") {
                    window.showToast({
                        type: payload.level || "info",
                        message: payload.message || "Nueva notificacion disponible.",
                    });
                    prependNotificationItem(payload);
                }

                if (payload.tipo === "aula_actualizada") {
                    updateAulaBadge(payload);
                }

                if (payload.tipo === "notification" || payload.tipo === "aula_actualizada") {
                    emitRefreshEvent(payload);
                }
            });

            const disponibilidadSocket = new WebSocket(disponibilidadUrl);
            disponibilidadSocket.addEventListener("message", (event) => {
                const payload = JSON.parse(event.data);
                updateAulaBadge(payload);
                emitRefreshEvent(payload);
            });

            const progresoSocket = new WebSocket(progresoUrl);
            progresoSocket.addEventListener("message", (event) => {
                const payload = JSON.parse(event.data);
                if (payload.tipo !== "progreso") {
                    return;
                }
                document.querySelectorAll("[data-asignacion-progress]").forEach((node) => {
                    node.value = payload.porcentaje;
                    node.textContent = `${payload.porcentaje}%`;
                });
                document.querySelectorAll("[data-grupos-procesados]").forEach((node) => {
                    node.textContent = String(payload.grupos_procesados);
                });
                window.dispatchEvent(
                    new CustomEvent("sds:progress-updated", {
                        detail: payload,
                    })
                );
            });

            const syncSocket = new WebSocket(syncUrl);
            syncSocket.addEventListener("message", (event) => {
                let payload = {};
                try {
                    payload = JSON.parse(event.data);
                } catch (error) {
                    payload = { tipo: "catalogo_actualizado", mensaje: event.data };
                }
                emitRefreshEvent(payload);
            });
        } catch (error) {
            window.console && window.console.warn && console.warn("No fue posible iniciar el canal WebSocket.", error);
        }
    };

    const updateAulaBadge = (payload) => {
        if (payload.tipo !== "aula_actualizada") {
            return;
        }
        document.querySelectorAll(`[data-aula-id="${payload.aula_id}"]`).forEach((node) => {
            node.textContent = payload.disponible ? "Disponible" : "Ocupada";
            node.classList.toggle("badge-success", Boolean(payload.disponible));
            node.classList.toggle("badge-error", !payload.disponible);
        });
    };

    document.addEventListener("DOMContentLoaded", connect);
})();
