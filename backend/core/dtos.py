from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class BaseDTO:
    """DTO base reutilizable para las capas de aplicacion."""

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()
