from abc import ABC, abstractmethod

from .entities import Role, User


class IUsuarioRepository(ABC):
    """Contrato de persistencia para usuarios y roles."""

    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def list_all_roles(self) -> list[Role]:
        raise NotImplementedError
