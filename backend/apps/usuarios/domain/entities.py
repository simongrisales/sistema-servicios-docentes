from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

class User:
    def __init__(self, user_id: int, username: str, email: str, password: str, role: 'Role', is_active: bool = True):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password # Debe ser hasheado en la vida real
        self.role = role
        self.is_active = is_active

    def __repr__(self):
        return f"<User {self.username} (ID: {self.user_id}), Role: {self.role.name}>"


class Role:
    def __init__(self, role_id: int, name: str, description: str, can_access_api: bool = False):
        self.role_id = role_id
        self.name = name
        self.description = description
        self.can_access_api = can_access_api

    def __repr__(self):
        return f"<Role {self.name}>"


class Permission:
    def __init__(self, permission_id: int, resource: str, action: str, description: str):
        self.permission_id = permission_id
        self.resource = resource # Ej: 'user', 'aula'
        self.action = action     # Ej: 'read', 'write', 'delete'
        self.description = description

    def __repr__(self):
        return f"<Permission {self.resource}:{self.action}>"