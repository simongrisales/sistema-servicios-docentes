from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notificaciones.infrastructure.broadcasts import broadcast_panel_sync

from .models import RoleModel, UsuarioModel


@receiver(post_save, sender=UsuarioModel)
def broadcast_usuario_sync(
    sender, instance: UsuarioModel, created: bool, **kwargs
) -> None:
    accion = "creado" if created else "actualizado"
    broadcast_panel_sync(
        entidad="usuarios",
        accion=accion,
        detalle=f"Usuario {instance.username} {accion}.",
        payload={
            "username": instance.username,
            "role_code": instance.role_code,
        },
    )


@receiver(post_save, sender=RoleModel)
def broadcast_role_sync(sender, instance: RoleModel, created: bool, **kwargs) -> None:
    accion = "creado" if created else "actualizado"
    broadcast_panel_sync(
        entidad="roles",
        accion=accion,
        detalle=f"Rol {instance.code or instance.name} {accion}.",
        payload={
            "code": instance.code,
            "name": instance.name,
        },
    )
