from django.contrib.auth.models import AbstractUser
from django.db import models


class RolSistema(models.TextChoices):
    ADMINISTRADOR = "administrador", "Administrador"
    LIDER_SD = "lider_sd", "Lider SD"
    AUXILIAR_SD = "auxiliar_sd", "Auxiliar SD"
    FACULTAD = "facultad", "Facultad"
    ADMISIONES = "admisiones", "Admisiones"


class RoleModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    code = models.CharField(
        max_length=50,
        choices=RolSistema.choices,
        unique=True,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "usuarios_rol"

    def __str__(self) -> str:
        return self.name


class UsuarioModel(AbstractUser):
    role = models.ForeignKey(
        RoleModel,
        on_delete=models.PROTECT,
        related_name="usuarios",
        null=True,
        blank=True,
    )
    departamento = models.CharField(max_length=120, blank=True)
    cargo = models.CharField(max_length=120, blank=True)

    class Meta:
        db_table = "usuarios_usuario"

    @property
    def role_code(self) -> str:
        return self.role.code if self.role else ""


class PermissionModel(models.Model):
    resource = models.CharField(max_length=100)
    action = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "usuarios_permiso"
        unique_together = ("resource", "action")

    def __str__(self) -> str:
        return f"{self.resource}:{self.action}"
