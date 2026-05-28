from abc import ABC, abstractmethod
from typing import Any

from .entities import Reporte


class IReporteRepository(ABC):
    @abstractmethod
    def get_reporte_by_id(self, reporte_id: int) -> Reporte | None:
        raise NotImplementedError

    @abstractmethod
    def find_reports_by_criteria(self, criteria: dict[str, Any]) -> list[Reporte]:
        raise NotImplementedError

    @abstractmethod
    def create_report_request(self, reporte: Reporte) -> int:
        raise NotImplementedError

    @abstractmethod
    def update_report_status(
        self,
        reporte_id: int,
        status: str,
        data: dict[str, Any] | None = None,
    ) -> bool:
        raise NotImplementedError


class IReporteGenerador(ABC):
    @abstractmethod
    def generate_report(self, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError
