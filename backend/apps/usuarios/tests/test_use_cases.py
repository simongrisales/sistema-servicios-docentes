import pytest

from ..application.dtos import LoginInputDTO, UsuarioInputDTO
from ..application.use_cases import (
    AsignarRol,
    AutenticarUsuario,
    CrearUsuario,
    ListarRoles,
    ListarUsuarios,
)
from ..domain.entities import Role, User
from ..domain.exceptions import CredencialesInvalidasError


class FakeUsuarioRepository:
    def __init__(self) -> None:
        self.role = Role(1, "Facultad", "Ingreso de datos", code="facultad")
        self.user = User(
            user_id=1,
            username="facultad",
            email="facultad@uco.edu.co",
            password="secret",
            role=self.role,
            departamento="Ingenieria",
            cargo="Coordinador",
        )
        self.created_payload = None
        self.saved_user = None

    def get_by_username(self, username: str):
        return self.user if username == self.user.username else None

    def create(self, payload: dict):
        self.created_payload = payload
        return User(
            user_id=2,
            username=payload["username"],
            email=payload["email"],
            password=payload["password"],
            role=Role(2, payload["role_code"], "Creado", code=payload["role_code"]),
            departamento=payload["departamento"],
            cargo=payload["cargo"],
        )

    def find_by_id(self, user_id: int):
        return self.user if user_id == self.user.user_id else None

    def save(self, user: User) -> None:
        self.saved_user = user

    def list_all_roles(self):
        return [self.role, Role(2, "Administrador", "Admin", code="administrador")]

    def list(self):
        return [self.user]


def test_autenticar_usuario_devuelve_tokens_si_existe():
    output = AutenticarUsuario(FakeUsuarioRepository()).execute(
        LoginInputDTO(username="facultad", password="secret")
    )

    assert output.access_token == "access-token"
    assert output.user.username == "facultad"


def test_autenticar_usuario_lanza_error_si_no_existe():
    with pytest.raises(CredencialesInvalidasError):
        AutenticarUsuario(FakeUsuarioRepository()).execute(
            LoginInputDTO(username="nadie", password="secret")
        )


def test_crear_usuario_usa_rol_por_defecto_facultad():
    repo = FakeUsuarioRepository()

    output = CrearUsuario(repo).execute(
        UsuarioInputDTO(
            username="nuevo",
            email="nuevo@uco.edu.co",
            password="secret",
            departamento="Admisiones",
            cargo="Analista",
        )
    )

    assert repo.created_payload["role_code"] == "facultad"
    assert output.username == "nuevo"
    assert output.role_code == "facultad"


def test_asignar_rol_actualiza_usuario_existente():
    repo = FakeUsuarioRepository()

    output = AsignarRol(repo).execute(1, "lider_sd")

    assert output.role.code == "lider_sd"
    assert repo.saved_user is output


def test_asignar_rol_falla_si_usuario_no_existe():
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        AsignarRol(FakeUsuarioRepository()).execute(99, "lider_sd")


def test_listar_roles_y_usuarios_mapea_dtos():
    repo = FakeUsuarioRepository()

    roles = ListarRoles(repo).execute()
    usuarios = ListarUsuarios(repo).execute()

    assert [role.code for role in roles] == ["facultad", "administrador"]
    assert usuarios[0].email == "facultad@uco.edu.co"
