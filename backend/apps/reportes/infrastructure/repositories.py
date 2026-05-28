from collections.abc import Iterable
from typing import Any

from core.repositories import BaseRepository

from ..domain.entities import Reporte
from ..domain.interfaces import IReporteRepository
from .models import ReporteModel, ReporteTipoModel


class ReporteRepository(BaseRepository[Reporte, int], IReporteRepository):
    def get(self, entity_id: int) -> Reporte | None:
        return self.get_reporte_by_id(entity_id)

    def list(self, **filters: Any) -> Iterable[Reporte]:
        return [
            self._to_domain(model) for model in ReporteModel.objects.filter(**filters)
        ]

    def create(self, data: dict[str, Any]) -> Reporte:
        return self._to_domain(ReporteModel.objects.create(**data))

    def update(self, entity_id: int, data: dict[str, Any]) -> Reporte:
        model = ReporteModel.objects.get(pk=entity_id)
        for field, value in data.items():
            setattr(model, field, value)
        model.save(update_fields=[*data.keys()])
        return self._to_domain(model)

    def delete(self, entity_id: int) -> None:
        ReporteModel.objects.filter(pk=entity_id).delete()

    def get_reporte_by_id(self, reporte_id: int) -> Reporte | None:
        model = (
            ReporteModel.objects.filter(pk=reporte_id).select_related("tipo").first()
        )
        return self._to_domain(model) if model else None

    def find_reports_by_criteria(self, criteria: dict[str, Any]) -> list[Reporte]:
        return list(self.list(**criteria))

    def create_report_request(self, reporte: Reporte) -> int:
        tipo = ReporteTipoModel.objects.get(codigo=reporte.tipo_codigo)
        model = ReporteModel.objects.create(
            tipo=tipo,
            titulo=reporte.titulo,
            periodo_inicio=reporte.periodo_inicio,
            periodo_fin=reporte.periodo_fin,
            estado=reporte.estado,
            usuario_solicitante_id=reporte.usuario_solicitante_id,
        )
        return model.pk

    def update_report_status(
        self,
        reporte_id: int,
        status: str,
        data: dict[str, Any] | None = None,
    ) -> bool:
        updated = ReporteModel.objects.filter(pk=reporte_id).update(
            estado=status,
            datos_raw=data,
        )
        return updated == 1

    @staticmethod
    def _to_domain(model: ReporteModel) -> Reporte:
        return Reporte(
            reporte_id=model.pk,
            tipo_codigo=model.tipo.codigo,
            titulo=model.titulo,
            fecha_generacion=model.fecha_solicitud.date(),
            periodo_inicio=model.periodo_inicio,
            periodo_fin=model.periodo_fin,
            descripcion_detallada="",
            estado=model.estado,
            usuario_solicitante_id=model.usuario_solicitante_id,
            datos_raw=model.datos_raw,
        )
