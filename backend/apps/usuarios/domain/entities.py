from dataclasses import dataclass


@dataclass
class Role:
    role_id: int
    name: str
    description: str
    can_access_api: bool = False


@dataclass
class Permission:
    permission_id: int
    resource: str
    action: str
    description: str


@dataclass
class User:
    user_id: int
    username: str
    email: str
    password: str
    role: Role
    is_active: bool = True
