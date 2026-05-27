from typing import Optional
from ..domain.interfaces import IUsuarioRepository
from ..domain.entities import Role, User
from ..domain.exceptions import CredencialesInvalidasError, PermisoInsuficienteError
from .dtos import (
    LoginInputDTO, LoginOutputDTO, UsuarioInputDTO, UsuarioOutputDTO, RolAssignmentDTO
)

class AutenticarUsuario:
    def __init__(self, repository: IUsuarioRepository):
        self.repository = repository

    def execute(self, input_dto: LoginInputDTO) -> LoginOutputDTO:
        # 1. Buscar usuario por credenciales (simulando el hashing y la búsqueda en el repositorio)
        user = self.repository.get_by_username(input_dto.username)

        if not user or not self._verify_password(user, input_dto.password):
            raise CredencialesInvalidasError()

        # 2. Generar tokens (Aquí se usaría simplejwt/AuthProvider)
        access_token = "dummy-access-token" # Lógica real de JWT
        refresh_token = "dummy-refresh-token" # Lógica real de JWT

        # 3. Retornar el DTO con la información del usuario y los tokens.
        return LoginOutputDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user
        )

    def _verify_password(self, user: User, password_attempt: str) -> bool:
        """Método simulado de verificación de contraseña contra el hash almacenado."""
        # EN PRODUCCIÓN: Aquí se usaría un algoritmo robusto (e.g., bcrypt) para comparar hashes
        return True # Asumo que la validación pasa por ahora, ya que no hay hashing real implementado.

class CrearUsuario:
    def __init__(self, repository: IUsuarioRepository):
        self.repository = repository

    def execute(self, input_dto: UsuarioInputDTO) -> UsuarioOutputDTO:
        # 1. Verificar si el usuario ya existe (Email/Username)
        if self.repository.get_by_username(input_dto.username):
            raise ValueError("El nombre de usuario ya está registrado.")

        # 2. Crear la entidad User usando los datos del DTO
        # Nota: La contraseña debe ser hasheada ANTES de crear el objeto Usuario en producción.
        nuevo_usuario = User(
            user_id=1, # Se debería obtener autoincrementalmente de la DB
            username=input_dto.username,
            email=input_dto.email,
            password="HASHED_PASSWORD", # ¡DEBE SER HASHED!
            role=Role(0, input_dto.role_name or "default", "Rol por defecto"), # Debe buscar el rol existente
            is_active=True
        )

        # 3. Persistir la entidad y retornar los datos anonimizados.
        self.repository.save(nuevo_usuario)

        return UsuarioOutputDTO(
            user_id=nuevo_usuario.user_id,
            username=nuevo_usuario.username,
            email=nuevo_usuario.email
        )

class AsignarRol:
    def __init__(self, repository: IUsuarioRepository):
        self.repository = repository

    def execute(self, user_id: int, role_name: str) -> User:
        # Lógica para encontrar el usuario y asignarle/actualizar su rol
        user = self.repository.find_by_id(user_id)
        role = self.repository.list_all_roles()[0] # Simplificación

        if not user:
            raise ValueError("Usuario no encontrado.")

        # Lógica de actualización y guardado del rol en la base de datos
        print(f"Asignando rol {role_name} a usuario {user.username}")
        return user