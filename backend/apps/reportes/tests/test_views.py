# backend/apps/reportes/tests/test_views.py
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch, MagicMock

from .serializers import ReporteSerializer, ReporteTipoSerializer

class TestReporteAPIViews(unittest.TestCase):
    """Pruebas de integración para los endpoints API de reportes."""

    def setUp(self):
        # Configurar el cliente de prueba de DRF
        self.client = self.client
        self.user = MagicMock() # Simulación de usuario autenticado
        self.user.id = 5
        self.user.role = 'Líder DOC'

    @patch('backend.apps.reportes.presentation.views.ReporteService')
    def test_solicitar_reporte_endpoint(self, MockReporteService):
        """Testea la llamada POST /api/reportes/para iniciar un reporte."""
        # 1. Configurar el mock del servicio y el repositorio (usando el ciclo de vida completo)
        mock_service = MockReporteService.return_value
        self.mock_repo = MagicMock() # Simular inyección de dependencia en la View

        # El endpoint debe simular la llamada al servicio
        mock_service.ejecutar_generacion_asincrona.return_value = 102 # ID retornado

        # Configurar el Request (simulación)
        self.client.force_authenticate(user=self.user)

        # Ejecución de la prueba
        response = self.client.post(
            reverse('reporte-list', kwargs={'pk': None}), # Endpoint 'solicitar'
            {'reporte_tipo_codigo': 'OCCU', 'periodo_inicio': '2026-09-01', 'periodo_fin': '2026-12-31'},
            format='json'
        )

        # 2. Verificaciones
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        data = response.json()
        self.assertIn('reporte_id', data)
        self.assertEqual(data['message'], 'Solicitud de reporte iniciada con éxito.')

    @patch('backend.apps.reportes.presentation.views.ReporteService')
    def test_obtener_estado_reporte_completo(self, MockReporteService):
        """Testea la llamada GET /api/reportes/{pk}/estado cuando el reporte está COMPLETO."""
        # 1. Configurar el mock del servicio para retornar un DTO de éxito
        mock_service = MockReporteService.return_value
        output_dto = ReporteOutputDTO(
            reporte_id=50, titulo="Ocupación Final", estado="COMPLETO", contenido_estructurado={"data": [1, 2]}
        )
        mock_service.obtener_estado_reporte.return_value = output_dto

        # Simular la llamada GET en el detalle del reporte
        response = self.client.get(reverse('reporte-detail', kwargs={'pk': 50}), format='json')

        # 2. Verificaciones
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['estado'], 'COMPLETO')
        self.assertIsNotNone(data['contenido_estructurado'])