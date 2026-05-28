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


@dataclass
class UsuarioOutputDTO:
    user_id: int
    username: str
    email: str


@dataclass
class RolAssignmentDTO:
    user_id: int
    role_name: str
