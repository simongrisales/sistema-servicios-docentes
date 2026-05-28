from django.db import models


class RoleModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "usuarios_rol"

    def __str__(self) -> str:
        return self.name


class PermissionModel(models.Model):
    resource = models.CharField(max_length=100)
    action = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "usuarios_permiso"
        unique_together = ("resource", "action")

    def __str__(self) -> str:
        return f"{self.resource}:{self.action}"
