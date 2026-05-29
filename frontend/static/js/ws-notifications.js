document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("main-app");
    if (!container) {
        return;
    }

    const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
    const socketUrl = `${protocol}${window.location.host}/ws/notifications/`;

    try {
        const socket = new WebSocket(socketUrl);

        socket.onmessage = function (event) {
            try {
                const data = JSON.parse(event.data);
                if (typeof data.message === "string") {
                    window.showToast({
                        type: data.type || "info",
                        message: data.message
                    });
                }
            } catch (error) {
                console.error("No se pudo procesar la notificacion.", error);
            }
        };

        socket.onerror = function () {
            console.warn("Canal de notificaciones no disponible en este momento.");
        };
    } catch (error) {
        console.warn("No se pudo abrir el canal WebSocket.", error);
    }
});
