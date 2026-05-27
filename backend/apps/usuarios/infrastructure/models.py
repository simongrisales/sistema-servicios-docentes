from django.contrib.auth import get_user_model
from django.db import models
from ..domain.entities import Role, Permission
# Asumimos que el modelo de usuario extendirá el modelo por defecto de Django para simplicidad en este paso

User = get_user_model()

class UsuarioModel(User):
    """Modelo ORM para la entidad Usuario."""
    # Sobrescribir campos o añadir lógica si fuera necesario.
    # Por ahora, solo extends AbstractUser, lo que maneja username, password, email y etc.
    pass # No se requiere código adicional aquí por defecto

class RoleModel(models.Model):
    """Modelo ORM para el Rol de usuario."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class PermissionModel(models.Model):
    """Modelo ORM para los permisos específicos del sistema."""
    resource = models.CharField(max_length=100) # Ej: 'user', 'aula'
    action = models.CharField(max_length=50)   # Ej: 'read', 'write'

    class Meta:
        unique_together = ('resource', 'action')
        verbose_name = "Permiso"

    def __str__(self):
        return f"{self.resource}:{self.action}"