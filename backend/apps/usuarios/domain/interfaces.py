from abc import ABC, abstractmethod
from typing import Optional, List, Any
from .entities import User, Role, Permission

class IUsuarioRepository(ABC):
    """Interfaz para el manejo de la persistencia y lógica del repositorio de Usuarios."""

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Busca un usuario por su nombre de usuario."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por su correo electrónico."""
        pass

    @abstractmethod
    def save(self, user: User):
        """Guarda o actualiza un objeto Usuario. Debe manejar la lógica de transacciones."""
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Busca un usuario por su ID primario."""
        pass

    @abstractmethod
    def list_all_roles(self) -> List[Role]:
        """Lista todos los roles definidos en el sistema."""
        pass

    # Se pueden añadir más métodos de repositorio aquí (e.g., find_users_by_role)