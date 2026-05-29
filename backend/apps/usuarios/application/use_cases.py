from ..domain.entities import Role, User
from ..domain.exceptions import CredencialesInvalidasError
from ..domain.interfaces import IUsuarioRepository
from .dtos import (
    LoginInputDTO,
    LoginOutputDTO,
    RolOutputDTO,
    UsuarioInputDTO,
    UsuarioOutputDTO,
)


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
        user = self.repository.create(
            {
                "username": input_dto.username,
                "email": input_dto.email,
                "password": input_dto.password,
                "role_code": input_dto.role_code or input_dto.role_name or "facultad",
                "departamento": input_dto.departamento,
                "cargo": input_dto.cargo,
            }
        )
        return _usuario_output(user)


class AsignarRol:
    def __init__(self, repository: IUsuarioRepository) -> None:
        self.repository = repository

    def execute(self, user_id: int, role_name: str) -> User:
        user = self.repository.find_by_id(user_id)
        if user is None:
            raise ValueError("Usuario no encontrado.")
        user.role = Role(0, role_name, "Rol asignado", code=role_name)
        self.repository.save(user)
        return user


class ListarRoles:
    def __init__(self, repository: IUsuarioRepository) -> None:
        self.repository = repository

    def execute(self) -> list[RolOutputDTO]:
        return [
            RolOutputDTO(
                role_id=role.role_id,
                code=role.code,
                name=role.name,
                description=role.description,
            )
            for role in self.repository.list_all_roles()
        ]


class ListarUsuarios:
    def __init__(self, repository: IUsuarioRepository) -> None:
        self.repository = repository

    def execute(self) -> list[UsuarioOutputDTO]:
        return [_usuario_output(user) for user in self.repository.list()]


def _usuario_output(user: User) -> UsuarioOutputDTO:
    return UsuarioOutputDTO(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        role_code=user.role.code,
        role_name=user.role.name,
        departamento=user.departamento,
        cargo=user.cargo,
    )
