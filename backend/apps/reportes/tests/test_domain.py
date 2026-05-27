# backend/apps/reportes/tests/test_domain.py
import unittest
from datetime import date
from backend.apps.reportes.domain.entities import Reporte, ReporteTipo, DatoReporteItem
from backend.apps.reportes.domain.exceptions import ReporteConflictoError, TipoReporteInvalidoError

class TestReportDomain(unittest.TestCase):
    """Pruebas unitarias para las entidades y excepciones de Reporte."""

    def test_reporte_dataclass_initialization(self):
        # Prueba básica de inicialización de la entidad principal.
        reporte = Reporte(
            tipo_codigo="OCCU",
            titulo="Ocupación Semestre 2026",
            fecha_generacion=date(2026, 5, 1),
            periodo_inicio=date(2026, 9, 1),
            periodo_fin=date(2026, 12, 31),
            descripcion_detallada="Reporte de ocupación general.",
            estado="PENDIENTE",
            usuario_solicitante_id=1
        )
        self.assertEqual(reporte.titulo, "Ocupación Semestre 2026")
        self.assertEqual(reporte.periodo_inicio, date(2026, 9, 1))

    def test_dataloreporteitem(self):
        # Prueba de la estructura simple de datos para reportes.
        item = DatoReporteItem(key="TotalAulas", valor=50)
        self.assertEqual(item.key, "TotalAulas")

    def test_custom_exceptions_handling(self):
        # Verifica que las excepciones son lanzadas y capturables correctamente.
        with self.assertRaises(TipoReporteInvalidoError):
            raise TipoReporteInvalidoError("Código desconocido.")

        with self.assertRaisesRegex(ReporteConflictoError, "conflicto"):
             raise ReporteConflictoError("Se detectó un conflicto de recursos críticos.", {"recursos": ["A", "B"]})

# Nota: Se pueden añadir tests para lógica compleja como la validación de rangos de fechas
# o consistencias entre campos si fuera necesario en las entidades.
