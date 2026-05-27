# backend/apps/notificaciones/application/use_cases.py

from datetime import datetime
from typing import List
from sistemaserviciosdocentes.backend.apps.notificaciones.domain.interfaces import INotificacionRepository
from sistemaserviciosdocentes.backend.apps.notificaciones.domain.entities import Notificacion, TipoNotificacion
from sistemaserviciosdocentes.backend.apps.notificaciones.domain.exceptions import *
# Dependencia externa simulada para verificar usuarios/roles
# from sistemaserviciosdocentes.backend.apps.usuarios.application.use_cases import IUsuarioRepository

class NotificacionService:
    """
    Orquesta la lógica de negocio para gestionar notificaciones.
    Este servicio será llamado por eventos críticos (ej. ConfirmarReserva).
    """

    def __init__(self, repo: INotificacionRepository):
        self.repo = repo

    def enviar_notificacion(self, input_dto: CrearNotificacionInputDTO) -> NotificacionOutputDTO:
        """
        Crea y persiste una notificación para un usuario destino específico.
        """
        # 1. Validación de negocio (ej. Verificar si el tipo existe o si el usuario existe)
        if not self._is_valid_notification_type(input_dto.tipo_notificacion):
            raise TipoNotificacionInvalidoError(f"Tipo de notificación '{input_dto.tipo_notificacion}' no permitido.")

        # 2. Crear la entidad de dominio
        try:
            nueva_notif = Notificacion.crear(
                notification_id=str(hash(input_dto)), # Placeholder para ID único real
                tipo=input_dto.tipo_notificacion,
                titulo=input_dto.titulo,
                mensaje=input_dto.mensaje,
                destino_id=input_dto.usuario_destino_id
            )

            # 3. Persistencia (Transaccionalidad manejada por el repositorio)
            self.repo.create_notification(nueva_notif)

            return NotificacionOutputDTO(
                notificacion_id=nueva_notif.notificacion_id,
                titulo=nueva_notif.titulo,
                mensaje=nueva_notif.mensaje,
                fecha_creacion=nueva_notif.fecha_creacion,
                tipo=nueva_notif.tipo,
                es_leida=False
            )

        except Exception as e:
            # Capturar y re-lanzar excepciones de dominio/sistema
            raise SistemaError(f"Fallo al enviar notificación: {e}")

    def listar_notificaciones_no_leidas(self, user_id: str) -> List[NotificacionOutputDTO]:
        """Recupera un listado paginado y filtrado de notificaciones no leídas."""
        # 1. Consultar al repositorio
        notificaciones = self.repo.get_unread_notifications_for_user(user_id)

        # 2. Mapeo a DTOs de salida para asegurar consistencia en el frontend
        output_dtos: List[NotificacionOutputDTO] = []
        for notif in notificaciones:
            output_dtos.append(NotificacionOutputDTO(
                notificacion_id=notif.notificacion_id,
                titulo=notif.titulo,
                mensaje=notif.mensaje,
                fecha_creacion=notif.fecha_creacion,
                tipo=notif.tipo,
                es_leida=False
            ))
        return output_dtos

    def marcar_leida(self, input: MarcarLeidaInputDTO) -> bool:
        """Marca la notificación como leída."""
        # La lógica de negocio aquí podría incluir una validación de permisos (¿puede el usuario X leer notif Y?)
        success = self.repo.mark_as_read(input.notificacion_id, input.user_id)
        return success

    @staticmethod
    def _is_valid_notification_type(tipo: str) -> bool:
        """Helper para validar el tipo de notificación."""
        # Usar los tipos definidos en la entidad para evitar errores tipográficos
        allowed_types = [TipoNotificacion.CONFLICTO, TipoNotificacion.CONFIRMACION, TipoNotificacion.ALERTA_MANTENIMIENTO]
        return tipo in allowed_types