from typing import Optional, List
from dataclasses import dataclass
from ..domain.entities import User, Role
# Importando excepciones para poder manejarlas en los casos de uso
from ..domain.exceptions import CredencialesInvalidasError, PermisoInsuficienteError


@dataclass
class LoginInputDTO:
    username: str
    password: str

@dataclass
class LoginOutputDTO:
    access_token: str
    refresh_token: str
    user: User # Devuelve la entidad de usuario para el cliente

@dataclass
class UsuarioInputDTO:
    username: str
    email: str
    password: str
    role_name: Optional[str] = None # Permite asignar roles al crear/actualizar

@dataclass
class UsuarioOutputDTO:
    user_id: int
    username: str
    email: str
    # Solo exponer información que el cliente debe ver, nunca la contraseña

# DTOs para respuesta de acciones de rol y permisos si es necesario en el futuro
@dataclass
class RolAssignmentDTO:
    user_id: int
    role_name: str