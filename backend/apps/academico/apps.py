from django.apps import AppConfig


class AcademicoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.academico"
    verbose_name = "Academico"

    def ready(self) -> None:
        from .infrastructure import signals  # noqa: F401
