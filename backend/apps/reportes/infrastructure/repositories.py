# backend/apps/reportes/infrastructure/repositories.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from django.contrib.auth.models import User
from django.db import transaction
from backend.apps.reportes.domain.interfaces import IReporteRepository
from backend.apps.reportes.domain.entities import Reporte, ReporteTipo, DatoReporteItem
from backend.apps.reportes.infrastructure.models import ReporteModel, ReporteTipoModel

class Repository(ABC):
    """Clase base para interactuar con modelos Django (generalista)."""
    # Aquí se pueden añadir métodos comunes de utilidad como soft delete o chequeo básico.
    pass

class ReporteRepository(Repository):
    """Implementación del repositorio IReporteRepository."""

    def get_reporte_by_id(self, reporte_id: int) -> Optional[Reporte]:
        """Consulta el estado y datos de un reporte dado su ID."""
        try:
            model = ReporteModel.objects.get(pk=reporte_id)
            # Mapear modelo a la entidad del dominio para desacoplar la lógica de negocio del ORM
            return Reporte(
                reporte_id=model.pk,
                tipo_codigo=model.tipo.codigo,
                titulo=model.titulo,
                fecha_generacion=model.fecha_solicitud.date(),
                periodo_inicio=model.periodo_inicio,
                periodo_fin=model.periodo_fin,
                descripcion_detallada="", # Se puede expandir con más campos del modelo
                estado=model.estado,
                usuario_solicitante_id=model.usuario_solicitante_id,
                datos_raw=model.datos_raw
            )
        except ReporteModel.DoesNotExist:
            return None

    def find_reports_by_criteria(self, criteria: dict) -> List[Reporte]:
        """Busca reportes usando el modelo ORM basado en los criterios proporcionados."""
        # Implementación a completar con lógica de filtrado avanzada por fechas/tipos.
        return []

    def create_report_request(self, reporte: Reporte) -> int:
        """Crea una solicitud de reporte y devuelve el ID generado."""
        with transaction.atomic():
            # 1. Buscar o crear el TipoReporteModel
            try:
                tipo_model = ReporteTipoModel.objects.get(codigo=reporte.tipo_codigo)
            except ReporteTipoModel.DoesNotExist:
                raise ValueError(f"El tipo de reporte {reporte.tipo_codigo} no existe.")

            # 2. Crear el registro del modelo
            model = ReporteModel.objects.create(
                tipo=tipo_model,
                titulo=reporte.titulo,
                periodo_inicio=reporte.periodo_inicio,
                periodo_fin=reporte.periodo_fin,
                estado="PENDIENTE",
                usuario_solicitante_id=reporte.usuario_solicitante_id
            )
            return model.pk

    def update_report_status(self, reporte_id: int, status: str, data: Optional[dict] = None) -> bool:
        """Actualiza el estado del reporte y guarda los datos."""
        try:
            model = ReporteModel.objects.get(pk=reporte_id)
            # Restringir estados posibles en la capa de infraestructura para seguridad
            allowed_statuses = ['COMPLETO', 'FALLIDO']
            if status not in allowed_statuses:
                 raise ValueError("Estado no permitido.")

            model.estado = status
            if data is not None:
                model.datos_raw = data # Guardamos los datos completos aquí
                model.metadata = {"revision": 1}
            model.save()
            return True
        except ReporteModel.DoesNotExist:
            return False