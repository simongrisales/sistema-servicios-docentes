# backend/apps/reportes/tests/test_use_cases.py
import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from backend.apps.reportes.application.use_cases import ReporteService
from backend.apps.reportes.domain.interfaces import IReporteRepository
from backend.apps.reportes.domain.exceptions import TipoReporteInvalidoError

class TestReporteService(unittest.TestCase):
    """Pruebas de los Casos de Uso (ReporteService). Debe mockear la dependencia del repositorio."""

    def setUp(self):
        # Mockear el Repositorio para aislar la lógica de negocio del acceso a datos
        self.mock_repo = MagicMock(spec=IReporteRepository)
        self.service = ReporteService(reporte_repo=self.mock_repo)

    def test_ejecutar_generacion_asincrona_success(self):
        """Prueba exitosa al solicitar un reporte, debe devolver un ID y simular el dispatch de Celery."""
        # Configurar mocks para que el repositorio parezca funcionar
        fake_reporte = MagicMock() # Mockeo del objeto Reporte.
        self.mock_repo.get_reporte_by_id.return_value = fake_reporte
        self.mock_repo.create_report_request.return_value = 101

        # Ejecución
        input_dto = ReporteInputDTO(
            reporte_tipo_codigo='OCCU',
            periodo_inicio=date(2026, 9, 1),
            periodo_fin=date(2026, 12, 31),
            usuario_id=5
        )

        # Llamada al caso de uso principal.
        reporte_id = self.service.ejecutar_generacion_asincrona(input_dto)

        self.assertEqual(reporte_id, 101)
        # Verificar que el repositorio fue llamado para crear la solicitud
        self.mock_repo.create_report_request.assert_called_once()


    def test_ejecutar_generacion_asincrona_tipo_invalido(self):
        """Debe lanzar TipoReporteInvalidoError si el tipo no es reconocido."""
        input_dto = ReporteInputDTO('XYZ', date.today(), date.today(), 1)

        with self.assertRaises(TipoReporteInvalidoError):
            # El método interno _validar_reporte_tipo será llamado y fallará
            self.service.ejecutar_generacion_asincrona(input_dto)


    def test_obtener_estado_ok(self):
        """Prueba la lectura exitosa del estado de un reporte."""
        # Mockear el retorno completo (ReporteModel -> Reporte Entity)
        mocked_reporte = MagicMock()
        self.mock_repo.get_reporte_by_id.return_value = mocked_reporte

        dto = self.service.obtener_estado_reporte(101)

        # Verificar que el DTO está bien mapeado
        self.assertEqual(dto.estado, "COMPLETO")
        self.assertIsNotNone(dto.contenido_estructurado)

    def test_obtener_estado_no_encontrado(self):
        """Debe manejar la excepción si el reporte no existe."""
        self.mock_repo.get_reporte_by_id.return_value = None # Simula NotFoundError/None

        with self.assertRaises(ValueError) as context:
            self.service.obtener_estado_reporte(999)
        self.assertIn("Reporte no encontrado", str(context.exception))