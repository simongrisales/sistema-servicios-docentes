from typing import Optional, List
from django.contrib.auth import get_user_model
from ..domain.interfaces import IUsuarioRepository
from ..domain.entities import User, Role
# Importar modelos ORM (debe apuntar al modelo UsuarioModel que extendió AbstractUser)
# from .models import UsuarioModel, RoleModel # Esto sería necesario en la implementación real

class UsuariosRepository(IUsuarioRepository):
    """Implementación concreta del repositorio de usuarios utilizando el ORM de Django."""

    def get_by_username(self, username: str) -> Optional[User]:
        try:
            # Utiliza la lógica nativa de Django para buscar usuarios.
            return get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[User]:
        try:
            return get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return None

    def save(self, user: User):
        """Guarda o actualiza un objeto Usuario."""
        # Lógica real de persistencia (Ej: usuario.set_password(...) antes de guardar).
        try:
            # En la vida real: se debería actualizar el password hash y llamar a .save() en el modelo ORM asociado.
            user_model = get_user_model().objects.get(pk=user.user_id) # Asumiendo que user_id existe
            # Lógica para actualizar campos específicos de roles/permisos si es necesario
        except Exception as e:
             raise Exception(f"Error al guardar el usuario en la base de datos: {e}")

    def find_by_id(self, user_id: int) -> Optional[User]:
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None

    def list_all_roles(self) -> List[Role]:
        """Lista todos los roles disponibles (usando RoleModel)."""
        # En la implementación real, esto queryearía el modelo RoleModel.
        return [Role(role_id=1, name="Admin", description="Superusuario")] # Placeholder

    def list_all_permissions(self) -> List[Permission]:
        """Lista todos los permisos definidos en el sistema (usando PermissionModel)."""
        # Esto se usaría para verificar si un rol tiene derecho a hacer algo.
        return []