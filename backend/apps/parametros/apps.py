"""App configuration for parametros."""

from django.apps import AppConfig


class ParametrosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.parametros"
    verbose_name = "Catalogo de Parametros"

    def ready(self) -> None:
        from .infrastructure import signals  # noqa: F401
