from dataclasses import dataclass

from ..domain.entities import User


@dataclass
class LoginInputDTO:
    username: str
    password: str


@dataclass
class LoginOutputDTO:
    access_token: str
    refresh_token: str
    user: User


@dataclass
class UsuarioInputDTO:
    username: str
    email: str
    password: str
    role_name: str | None = None
    role_code: str | None = None
    departamento: str = ""
    cargo: str = ""


@dataclass
class UsuarioOutputDTO:
    user_id: int
    username: str
    email: str
    role_code: str = ""
    role_name: str = ""
    departamento: str = ""
    cargo: str = ""


@dataclass
class RolOutputDTO:
    role_id: int
    code: str
    name: str
    description: str


@dataclass
class RolAssignmentDTO:
    user_id: int
    role_name: str
