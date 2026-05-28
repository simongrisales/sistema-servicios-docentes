from collections.abc import Iterable
from typing import Any

from django.contrib.auth import get_user_model

from core.repositories import BaseRepository

from ..domain.entities import Role, User
from ..domain.interfaces import IUsuarioRepository
from .models import RoleModel


class UsuariosRepository(BaseRepository[User, int], IUsuarioRepository):
    def get(self, entity_id: int) -> User | None:
        return self.find_by_id(entity_id)

    def list(self, **filters: Any) -> Iterable[User]:
        return [
            self._to_domain(model)
            for model in get_user_model().objects.filter(**filters)
        ]

    def create(self, data: dict[str, Any]) -> User:
        password = data.pop("password")
        model = get_user_model().objects.create_user(password=password, **data)
        return self._to_domain(model)

    def update(self, entity_id: int, data: dict[str, Any]) -> User:
        model = get_user_model().objects.get(pk=entity_id)
        for field, value in data.items():
            setattr(model, field, value)
        model.save(update_fields=[*data.keys()])
        return self._to_domain(model)

    def delete(self, entity_id: int) -> None:
        get_user_model().objects.filter(pk=entity_id).update(is_active=False)

    def get_by_username(self, username: str) -> User | None:
        model = get_user_model().objects.filter(username=username).first()
        return self._to_domain(model) if model else None

    def get_by_email(self, email: str) -> User | None:
        model = get_user_model().objects.filter(email=email).first()
        return self._to_domain(model) if model else None

    def save(self, user: User) -> None:
        self.update(
            user.user_id,
            {
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
            },
        )

    def find_by_id(self, user_id: int) -> User | None:
        model = get_user_model().objects.filter(pk=user_id).first()
        return self._to_domain(model) if model else None

    def list_all_roles(self) -> list[Role]:
        return [
            Role(role_id=model.id, name=model.name, description=model.description)
            for model in RoleModel.objects.all()
        ]

    @staticmethod
    def _to_domain(model) -> User:
        role = Role(role_id=0, name="usuario", description="Usuario autenticado")
        return User(
            user_id=model.pk,
            username=model.username,
            email=model.email,
            password="",
            role=role,
            is_active=model.is_active,
        )
