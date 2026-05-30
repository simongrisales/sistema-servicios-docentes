from collections.abc import Iterable
from typing import Any

from django.db import transaction
from django.utils import timezone

from core.repositories import BaseRepository
from core.sanitizers import BleachSanitizerMixin

from ..domain.entities import Notificacion
from ..domain.interfaces import INotificacionRepository
from .models import NotificacionModel


class NotificacionRepository(
    BleachSanitizerMixin,
    BaseRepository[Notificacion, str], INotificacionRepository
):
    """Repositorio concreto de notificaciones usando Django ORM."""

    text_fields = ("titulo", "mensaje")

    def get(self, entity_id: str) -> Notificacion | None:
        return self.get_by_id(entity_id)

    def list(self, **filters: Any) -> Iterable[Notificacion]:
        queryset = NotificacionModel.objects.filter(**filters)
        return [self._to_domain(instance) for instance in queryset]

    def create(self, data: dict[str, Any]) -> Notificacion:
        model = NotificacionModel.objects.create(**self.sanitize_payload(data))
        return self._to_domain(model)

    def update(self, entity_id: str, data: dict[str, Any]) -> Notificacion:
        model = NotificacionModel.objects.get(notificacion_id=entity_id)
        for field, value in data.items():
            setattr(model, field, value)
        model.save(update_fields=[*data.keys()])
        return self._to_domain(model)

    def delete(self, entity_id: str) -> None:
        NotificacionModel.objects.filter(notificacion_id=entity_id).update(activo=False)

    def get_by_id(self, notificacion_id: str) -> Notificacion | None:
        model = (
            NotificacionModel.objects.filter(
                notificacion_id=notificacion_id,
                activo=True,
            )
            .select_related("usuario_destino")
            .first()
        )
        if model is None:
            return None
        return self._to_domain(model)

    def create_notification(self, notification: Notificacion) -> Notificacion:
        model = NotificacionModel.objects.create(
            notificacion_id=notification.notificacion_id,
            tipo=notification.tipo,
            titulo=self.sanitize_payload({"titulo": notification.titulo})["titulo"],
            mensaje=self.sanitize_payload({"mensaje": notification.mensaje})["mensaje"],
            usuario_destino_id=notification.usuario_destino_id,
            lectura_requerida=notification.lectura_requerida,
            es_leida=notification.es_leida,
        )
        return self._to_domain(model)

    def mark_as_read(self, notificacion_id: str, user_id: str) -> bool:
        with transaction.atomic():
            updated = NotificacionModel.objects.filter(
                notificacion_id=notificacion_id,
                usuario_destino_id=user_id,
                activo=True,
                es_leida=False,
            ).update(es_leida=True, fecha_lectura=timezone.now())
        return updated == 1

    def get_unread_notifications_for_user(self, user_id: str) -> Iterable[Notificacion]:
        queryset = (
            NotificacionModel.objects.filter(
                usuario_destino_id=user_id,
                es_leida=False,
                activo=True,
            )
            .select_related("usuario_destino")
            .order_by("-fecha_creacion")[:20]
        )
        return [self._to_domain(instance) for instance in queryset]

    def list_all_notifications_for_user(self, user_id: str) -> Iterable[Notificacion]:
        queryset = (
            NotificacionModel.objects.filter(
                usuario_destino_id=user_id,
                activo=True,
            )
            .select_related("usuario_destino")
            .order_by("-fecha_creacion")
        )
        return [self._to_domain(instance) for instance in queryset]

    @staticmethod
    def _to_domain(model: NotificacionModel) -> Notificacion:
        return Notificacion(
            notificacion_id=model.notificacion_id,
            tipo=model.tipo,
            titulo=model.titulo,
            mensaje=model.mensaje,
            fecha_creacion=model.fecha_creacion,
            usuario_destino_id=str(model.usuario_destino_id),
            lectura_requerida=model.lectura_requerida,
            es_leida=model.es_leida,
        )
