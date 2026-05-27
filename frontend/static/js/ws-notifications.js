// frontend/static/js/ws-notifications.js

/**
 * Conecta el cliente WebSocket al canal de notificaciones del sistema.
 * Este script se debe cargar en base.html y es responsable de la conectividad
 * en tiempo real para las alertas críticas (Conflictos, Asignaciones confirmadas).
 */
document.addEventListener('DOMContentLoaded', function () {
    // Buscar el contenedor principal de la aplicación
    const container = document.getElementById('main-app');
    if (!container) {
        console.warn("Elemento #main-app no encontrado. El sistema de notificaciones WebSocket podría fallar.");
        return;
    }

    // 1. Establecer la conexión WebSocket (Usamos ws:// o wss:// dependiendo del entorno, asumiremos que Django lo maneja)
    const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
    const socketUrl = `${protocol}${window.location.host}/ws/notifications/`;
    const socket = new WebSocket(socketUrl);

    console.log(`Intentando conectar a WebSocket en: ${socketUrl}`);

    // 2. Manejar la apertura de la conexión
    socket.onopen = function(event) {
        console.log("WebSocket conectado exitosamente al canal de notificaciones.");
        // Opcionalmente, enviar un mensaje de prueba para validar el canal.
        // socket.send(JSON.stringify({ action: "subscribe", topic: "global_notifications" }));
    };

    // 3. Manejar mensajes entrantes (El core de la funcionalidad)
    socket.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);

            // Asegurarse que el mensaje contiene los campos esperados
            if (typeof data.message === 'string' && typeof data.type === 'string') {
                console.log("Mensaje de notificación recibido:", data);

                // Llamar a la función AlpineJS para mostrar el toast,
                // lo que asegura que se use el contexto global del frontend.
                window.showToast(data);

            } else {
                console.warn("Formato de mensaje WebSocket inesperado:", data);
            }
        } catch (e) {
            console.error("Error al parsear o procesar mensaje WebSocket:", e);
        }
    };

    // 4. Manejar el cierre o error de la conexión
    socket.onerror = function(event) {
        console.error("WebSocket Error:", event);
    };

    socket.onclose = function(event) {
        if (event.wasClean) {
            console.log(`WebSocket cerrado limpiamente con código ${event.code} y razón '${event.reason}'`);
        } else {
            // Esto ocurre si el proceso muere o hay una interrupción
            console.warn("WebSocket desconectado inesperadamente. Reintentando conexión en 5 segundos...");
            setTimeout(() => window.location.reload(), 5000); // Simple reintento recargando la página
        }
    };
});

// NOTA: Esta función 'showToast' DEBE ser global para que AlpineJS pueda llamarla desde partials/navbar.html
window.showToast = function(data) {
    if (typeof Alpine === 'undefined') {
         console.error("Alpine.js no está cargado, no se puede mostrar el toast.");
        return;
    }

    // Llama al store de AlpineJS para manejar la lógica de visualización en el partial.
    const toastStore = window.Alpine.store('toast');
    if (typeof toastStore.showToast === 'function') {
        toastStore.showToast(data);
    } else {
        console.error("El store AlpineJS 'toast' no está disponible para mostrar la notificación.");
    }
};