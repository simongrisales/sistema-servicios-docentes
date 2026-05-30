(function () {
    const connect = () => {
        if (!window.WebSocket) {
            return;
        }

        const protocol = window.location.protocol === "https:" ? "wss" : "ws";
        const socketUrl = `${protocol}://${window.location.host}/ws/notificaciones/`;
        const disponibilidadUrl = `${protocol}://${window.location.host}/ws/disponibilidad-aulas/`;
        const progresoUrl = `${protocol}://${window.location.host}/ws/asignacion/progreso/`;

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
                }

                if (payload.tipo === "aula_actualizada") {
                    updateAulaBadge(payload);
                }
            });

            const disponibilidadSocket = new WebSocket(disponibilidadUrl);
            disponibilidadSocket.addEventListener("message", (event) => {
                updateAulaBadge(JSON.parse(event.data));
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
