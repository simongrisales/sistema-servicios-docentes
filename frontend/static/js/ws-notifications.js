(function () {
    const connect = () => {
        if (!window.WebSocket) {
            return;
        }

        const protocol = window.location.protocol === "https:" ? "wss" : "ws";
        const socketUrl = `${protocol}://${window.location.host}/ws/notificaciones/`;

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
                    countBadge.textContent = String(currentCount + 1);
                }

                if (payload.tipo === "notification" && typeof window.showToast === "function") {
                    window.showToast({
                        type: payload.level || "info",
                        message: payload.message || "Nueva notificacion disponible.",
                    });
                }

                if (payload.tipo === "aula_actualizada") {
                    document.querySelectorAll(`[data-aula-id="${payload.aula_id}"]`).forEach((node) => {
                        node.textContent = payload.disponible ? "Disponible" : "Ocupada";
                    });
                }
            });
        } catch (error) {
            window.console && window.console.warn && console.warn("No fue posible iniciar el canal WebSocket.", error);
        }
    };

    document.addEventListener("DOMContentLoaded", connect);
})();
