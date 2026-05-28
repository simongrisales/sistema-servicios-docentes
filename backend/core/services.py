from abc import ABC, abstractmethod
from typing import Any


class BaseService(ABC):
    """Contrato base para casos de uso y servicios de aplicacion."""

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
