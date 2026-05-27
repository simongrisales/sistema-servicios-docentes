# backend/apps/notificaciones/infrastructure/repositories.py

from typing import List, Optional
from sistemaserviciosdocentes.backend.apps.notificaciones.domain.interfaces import INotificacionRepository
from sistemaserviciosdocentes.backend.apps.notificaciones.domain.entities import Notificacion
from systemserviciosdocentes.backend.apps.notificaciones.infrastructure.models import NotificacionModel # Importar el modelo ORM
# Asumiendo que existe una función para obtener un usuario activo o por ID en la capa de infraestructura/usuarios

class NotificacionRepository(INotificacionRepository):
    """Implementación concreta del repositorio de notificaciones usando Django ORM."""

    def get_by_id(self, notificacion_id: str) -> Optional[Notificacion]:
        try:
            model_instance = NotificacionModel.objects.get(UUID_NOTIFICACION=notificacion_id)
            return Notificacion(
                notificacion_id=str(model_instance.uuid_notificacion),
                tipo=model_instance.TIPO,
                titulo=model_instance.TITULO,
                mensaje=model_instance.MENSAJE,
                fecha_creacion=model_instance.fecha_creacion,
                usuario_destino_id=str(model_instance.usuario_destino_id.pk) if model_instance.usuario_destino_id else None
            )
        except NotificacionModel.DoesNotExist:
            return None

    def create_notification(self, notification: Notificacion):
        """Guarda una nueva notificación en la base de datos."""
        # Mapear la entidad de dominio a los campos del modelo ORM
        NotificacionModel.objects.create(
            UUID_NOTIFICACION=notification.notificacion_id,
            TIPO=notification.tipo,
            TITULO=notification.titulo,
            MENSAJE=notification.mensaje,
            USUARIO_DESTINO=notification.usuario_destino_id, # Asumiendo que esto se resuelve a FK de usuario
        )

    async def mark_as_read(self, notificacion_id: str, user_id: str) -> bool:
        """Marca la notificación como leída y verifica que pertenece al usuario."""
        # NOTA: En un entorno real, esto debe ejecutarse en una transacción de DB.
        from django.db import transaction

        try:
            with transaction.atomic():
                instance = NotificacionModel.objects.get(UUID_NOTIFICACION=notificacion_id)
                if instance.USUARIO_DESTINO and str(instance.USUARIO_DESTINO.pk) == user_id:
                    instance.es_leida = True
                    instance.save()
                    return True
                return False # Notificación no encontrada o no pertenece al usuario
        except NotificacionModel.DoesNotExist:
            return False

    async def get_unread_notifications_for_user(self, user_id: str) -> List[Notificacion]:
        """Recupera todas las notificaciones no leídas para el usuario."""
        # NOTA: Se asume que la consulta de ORM se ejecuta en un contexto async (ej. @select_related o similar).
        from django.db import transaction

        try:
            with transaction.atomic():
                instances = NotificacionModel.objects.filter(
                    usuario_destino__pk=user_id,
                    es_leida=False,
                    estado_activo=True
                ).order_by('-fecha_creacion')[:20] # Límite de paginación

                notifications = []
                for instance in instances:
                    # Mapeo del ORM a la entidad de Dominio
                    notifications.append(Notificacion(
                        notificacion_id=str(instance.uuid_notificacion),
                        tipo=instance.TIPO,
                        titulo=instance.TITULO,
                        mensaje=instance.MENSAJE,
                        fecha_creacion=instance.fecha_creacion,
                        usuario_destino_id=str(instance.usuario_destino.pk) if instance.usuario_destino else None
                    ))
                return notifications

        except Exception as e:
            # Loggear el error de base de datos en producción
            print(f"Error al obtener notificaciones no leídas: {e}")
            return []

    async def list_all_notifications_for_user(self, user_id: str) -> List[Notificacion]:
        """Lista el historial completo de notificaciones para un usuario."""
        from django.db import transaction
        try:
            with transaction.atomic():
                instances = NotificacionModel.objects.filter(
                    usuario_destino__pk=user_id,
                    estado_activo=True
                ).order_by('-fecha_creacion')

                notifications = []
                for instance in instances:
                    # Mapeo del ORM a la entidad de Dominio
                    notifications.append(Notificacion(
                        notificacion_id=str(instance.uuid_notificacion),
                        tipo=instance.TIPO,
                        titulo=instance.TITULO,
                        mensaje=instance.MENSAJE,
                        fecha_creacion=instance.fecha_creacion,
                        usuario_destino_id=str(instance.usuario_destino.pk) if instance.usuario_destino else None
                    ))
                return notifications

        except Exception as e:
            print(f"Error al listar notificaciones: {e}")
            return []