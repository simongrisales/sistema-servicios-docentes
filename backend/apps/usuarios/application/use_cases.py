from ..domain.entities import Role, User
from ..domain.exceptions import CredencialesInvalidasError
from ..domain.interfaces import IUsuarioRepository
from .dtos import LoginInputDTO, LoginOutputDTO, UsuarioInputDTO, UsuarioOutputDTO


class AutenticarUsuario:
    def __init__(self, repository: IUsuarioRepository) -> None:
        self.repository = repository

    def execute(self, input_dto: LoginInputDTO) -> LoginOutputDTO:
        user = self.repository.get_by_username(input_dto.username)
        if user is None:
            raise CredencialesInvalidasError()
        return LoginOutputDTO("access-token", "refresh-token", user)


class CrearUsuario:
    def __init__(self, repository: IUsuarioRepository) -> None:
        self.repository = repository

    def execute(self, input_dto: UsuarioInputDTO) -> UsuarioOutputDTO:
        role = Role(0, input_dto.role_name or "usuario", "Rol por defecto")
        user = User(
            user_id=0,
            username=input_dto.username,
            email=input_dto.email,
            password=input_dto.password,
            role=role,
        )
        self.repository.save(user)
        return UsuarioOutputDTO(user.user_id, user.username, user.email)


class AsignarRol:
    def __init__(self, repository: IUsuarioRepository) -> None:
        self.repository = repository

    def execute(self, user_id: int, role_name: str) -> User:
        user = self.repository.find_by_id(user_id)
        if user is None:
            raise ValueError("Usuario no encontrado.")
        user.role = Role(0, role_name, "Rol asignado")
        self.repository.save(user)
        return user
