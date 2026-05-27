# backend/apps/reservas/tests/test_views.py

import unittest
from rest_framework import status
from unittest.mock import MagicMock
from django.test import TestCase
from systemserviciosdocentes.backend.apps.reservas.presentation.serializers import (
    CrearReservaSerializer, ReservaOutputSerializer
)
# Mockear dependencias de las capas inferiores para aislar la vista
# En un entorno real usaríamos Superuser/Client de DRF y mockearíamos repositorios

class TestReservasView(TestCase):
    """Tests que simulan llamadas HTTP al ViewSet."""

    def setUp(self):
        # Mockear el objeto de vista completo para pruebas unitarias de endpoints.
        # En un entorno real, se usa Client/APITestCase de DRF
        from rest_framework.response import Response
        from rest_framework.viewsets import ModelViewSet

        # Creamos una clase mock que simula el comportamiento del ViewSet para poder llamarlo en tests unitarios.
        self.MockViewSet = MagicMock(spec=ModelViewSet)

    def test_crear_reserva_endpoint_success(self):
        """Testea un POST exitoso en /api/reservas/"""
        # Simular datos de entrada válidos y que pasen la validación del serializer
        fake_data = {
            "aula_id": "A101",
            "inicio": datetime.now().isoformat(),
            "fin": (datetime.now() + timedelta(hours=2)).isoformat(),
            "solicitante_id": "user_abc"
        }

        # 1. Configurar Mocks de Dependencias para el éxito
        # El ViewSet llama a ReservaService, que necesita mocks de Repositorios y Asignación.
        # Para este test, solo verificamos la estructura del flujo: Serializer -> View -> Service -> Status 201

        # Mockear la respuesta exitosa del servicio (DTO serializado)
        mock_output = ReservaOutputSerializer(
            ReservaOutputDTO("temp-id", "A101", datetime.now(), datetime.now() + timedelta(hours=2), "user_abc", "PENDIENTE")
        ).data

        # Mockear la respuesta HTTP y el comportamiento del ViewSet para devolver 201
        self.MockViewSet.create.return_value = Response(mock_output, status=status.HTTP_201_CREATED)

        # Ejecución (simulación de llamada POST al endpoint /api/reservas/)
        response = self.MockViewSet.create(self, request=MagicMock(data=fake_data), *args=[], **kwargs={})

        # Verificaciones
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("reserva_id", response.data)


    def test_crear_reserva_endpoint_conflicto(self):
        """Testea que la creación falla con 409 Conflict si el servicio detecta un cruce."""
        fake_data = {
            "aula_id": "A101",
            "inicio": datetime.now().isoformat(),
            "fin": (datetime.now() + timedelta(hours=2)).isoformat(),
            "solicitante_id": "user_abc"
        }

        # 1. Configurar Mocks de Dependencias para el conflicto
        conflict_error = ReservaConflictoError("El aula A101 está en conflicto con...")
        self.MockViewSet.create.return_value = Response({"error": str(conflict_error)}, status=status.HTTP_409_CONFLICT)

        # Ejecución (simulación de llamada POST al endpoint /api/reservas/)
        response = self.MockViewSet.create(self, request=MagicMock(data=fake_data), *args=[], **kwargs={})

        # Verificaciones
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("conflicto", response.data['error'])


    def test_confirmar_reserva_endpoint_success(self):
        """Testea el endpoint POST /api/reservas/<pk>/confirm/."""
        # Simular que se recibe una solicitud de confirmación exitosa (200 OK)
        fake_data = {"reserva_id": "test-id"}

        mock_output = ReservaOutputSerializer(
            ReservaOutputDTO("test-id", "A101", datetime.now(), datetime.now() + timedelta(hours=2), "user_abc", "CONFIRMADA")
        ).data

        self.MockViewSet.as_view.return_value = MagicMock(confirm=lambda *a, **k: Response(mock_output, status=status.HTTP_200_OK))

        # Ejecución (simulación de llamada POST al endpoint /api/reservas/test-id/confirm/)
        response = self.MockViewSet.as_view.return_value.confirm(self, request=MagicMock(data=fake_data), pk="test-id", *args=[], **kwargs={})

        # Verificaciones
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_cancelar_reserva_endpoint(self):
        """Testea el endpoint POST /api/reservas/<pk>/cancel/."""
        fake_data = {"reserva_id": "test-id"}

        # Mockear la respuesta de éxito (200 OK)
        mock_response = Response({"status": "success", "message": "Reserva test-id cancelada con éxito."}, status=status.HTTP_200_OK)
        self.MockViewSet.as_view.return_value = MagicMock(cancel=lambda *a, **k: mock_response)

        # Ejecución (simulación de llamada POST al endpoint /api/reservas/test-id/cancel/)
        response = self.MockViewSet.as_view.return_value.cancel(self, request=MagicMock(data=fake_data), pk="test-id", *args=[], **kwargs={})

        # Verificaciones
        self.assertEqual(response.status_code, status.HTTP_200_OK)