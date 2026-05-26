from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any, Generic, TypeVar

ModelType = TypeVar("ModelType")
IdType = TypeVar("IdType")


class BaseRepository(ABC, Generic[ModelType, IdType]):
    """Contrato base para repositorios concretos de infraestructura."""

    @abstractmethod
    def get(self, entity_id: IdType) -> ModelType | None:
        raise NotImplementedError

    @abstractmethod
    def list(self, **filters: Any) -> Iterable[ModelType]:
        raise NotImplementedError

    @abstractmethod
    def create(self, data: dict[str, Any]) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity_id: IdType, data: dict[str, Any]) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: IdType) -> None:
        raise NotImplementedError
