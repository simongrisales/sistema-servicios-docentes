from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class RolSistema(models.TextChoices):
    ADMINISTRADOR = "administrador", _("Administrador")
    LIDER_SD = "lider_sd", _("Lider SD")
    AUXILIAR_SD = "auxiliar_sd", _("Auxiliar SD")
    FACULTAD = "facultad", _("Facultad")
    ADMISIONES = "admisiones", _("Admisiones")


class RoleModel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Nombre"))
    description = models.TextField(blank=True, verbose_name=_("Descripcion"))
    code = models.CharField(
        max_length=50,
        choices=RolSistema.choices,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Codigo"),
    )

    class Meta:
        db_table = "usuarios_rol"
        verbose_name = _("Rol")
        verbose_name_plural = _("Roles")

    def __str__(self) -> str:
        return self.name


class UsuarioModel(AbstractUser):
    role = models.ForeignKey(
        RoleModel,
        on_delete=models.PROTECT,
        related_name="usuarios",
        null=True,
        blank=True,
        verbose_name=_("Rol"),
    )
    departamento = models.CharField(
        max_length=120, blank=True, verbose_name=_("Departamento")
    )
    cargo = models.CharField(max_length=120, blank=True, verbose_name=_("Cargo"))

    class Meta:
        db_table = "usuarios_usuario"
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")

    @property
    def role_code(self) -> str:
        return self.role.code if self.role else ""


class PermissionModel(models.Model):
    resource = models.CharField(max_length=100, verbose_name=_("Recurso"))
    action = models.CharField(max_length=50, verbose_name=_("Accion"))
    description = models.TextField(blank=True, verbose_name=_("Descripcion"))

    class Meta:
        db_table = "usuarios_permiso"
        unique_together = ("resource", "action")
        verbose_name = _("Permiso")
        verbose_name_plural = _("Permisos")

    def __str__(self) -> str:
        return f"{self.resource}:{self.action}"
