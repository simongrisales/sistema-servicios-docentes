from django.apps import AppConfig


class AsignacionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.asignacion"
    verbose_name = "Asignacion"

    def ready(self) -> None:
        from .infrastructure import signals  # noqa: F401
