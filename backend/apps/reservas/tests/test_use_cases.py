# backend/apps/reservas/tests/test_use_cases.py

import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock
from systemserviciosdocentes.backend.apps.reservas.application.use_cases import ReservaService
from systemserviciosdocentes.backend.apps.reservas.domain.dtos import *
from sistemaserviciosdocentes.backend.apps.reservas.domain.interfaces import IReservaRepository
from sistemaserviciosdocentes.backend.apps.reservas.domain.interfaces import IAsignacionRepository
from systemserviciosdocentes.backend.apps.reservas.domain.entities import ReservaEstado, ReservaConflictoError

class MockDependencies:
    """Clase para crear mocks de las dependencias críticas."""
    @staticmethod
    def create_mock_repo():
        # Mock del repositorio de reservas
        mock_repo = MagicMock(spec=IReservaRepository)
        return mock_repo

    @staticmethod
    def create_conflict_reserva_mock():
        # Un objeto Reserva que simula un conflicto, no es una instancia real
        class MockConflictingReserva:
            pass # Solo necesitamos el tipo para el tipado del repositorio.
        return [MockConflictingReserva()]

class TestReservaService(unittest.TestCase):
    """Tests para los Casos de Uso (ReservaService), enfocándose en la orquestación y validaciones."""

    def setUp(self):
        # Inicializar mocks antes de cada test
        self.mock_reserva_repo = MockDependencies.create_mock_repo()
        self.mock_asignacion_repo = MockDependencies.create_mock_repo()
        self.service = ReservaService(
            reserva_repo=self.mock_reserva_repo,
            asignacion_repo=self.mock_asignacion_repo
        )

    def setUpMockTime(self):
        # Definición de tiempos fijos para hacer los tests determinísticos
        today = datetime(2026, 5, 30, 10, 0, 0)
        self.now = today
        self.start_time = today + timedelta(hours=5)
        self.end_time = today + timedelta(hours=7)

    def test_crear_reserva_exitoso(self):
        """Testea la creación exitosa de una reserva sin conflictos."""
        self.setUpMockTime()
        input_dto = CrearReservaInputDTO("A101", self.start_time, self.end_time, "user_abc")

        # Configurar Mocks para el éxito: no hay conflictos y la creación pasa
        self.mock_asignacion_repo.find_conflicts.return_value = [] # Sin conflictos de asignaciones existentes
        self.mock_reserva_repo.find_conflicts.return_value = [] # Sin conflictos con reservas pendientes
        # Mockear que el repositorio no lanza excepción al crear

        output = self.service.crear_reserva(input_dto)

        # Verificaciones:
        # 1. Que se llamó a validar ambos repositorios antes de crear.
        self.mock_asignacion_repo.find_conflicts.assert_called_once()
        self.mock_reserva_repo.find_conflicts.assert_called_once()
        # 2. Que se llamó al método create del repositorio
        self.mock_reserva_repo.create.assert_called_once()
        # 3. Que el DTO de salida es correcto
        self.assertEqual(output.estado, ReservaEstado.PENDIENTE)

    def test_crear_reserva_conflicto_asignacion(self):
        """Testea que la creación falla si hay conflicto con una ASIGNACIÓN ya confirmada."""
        self.setUpMockTime()
        input_dto = CrearReservaInputDTO("A101", self.start_time, self.end_time, "user_abc")

        # Configurar Mocks para el fallo: encuentra conflictos de asignaciones
        conflicts = [MagicMock()] # Simula la detección de un conflicto de asignación
        self.mock_asignacion_repo.find_conflicts.return_value = conflicts
        self.mock_reserva_repo.find_conflicts.return_value = []

        with self.assertRaises(ReservaConflictoError):
            self.service.crear_reserva(input_dto)

        # Verificaciones: Aseguramos que el repositorio NUNCA intenta crear la reserva
        self.mock_reserva_repo.create.assert_not_called()

    def test_confirmar_reserva_conflicto_post_validacion(self):
        """Testea que confirmar falla si, entre la solicitud y la confirmación, apareció un conflicto."""
        # Preparar un objeto reserva mockeado
        mock_reserva = MagicMock()
        mock_reserva.aula_id = "A101"

        input_dto = ConfirmarReservaInputDTO("test-id")

        # 1. La creación inicial pasa (se asume que ya pasó)
        self.mock_asignacion_repo.find_conflicts.return_value = []
        self.mock_reserva_repo.get_by_id.return_value = mock_reserva # Se encuentra la reserva

        # 2. La revalidación falla por un conflicto nuevo (simulando una asignación externa)
        self.mock_asignacion_repo.find_conflicts.return_value = [MagicMock()]

        with self.assertRaises(ReservaConflictoError):
            self.service.confirmar_reserva(input_dto)

        # Verificaciones: La actualización de estado no debe ocurrir por el conflicto
        self.mock_reserva_repo.update_state.assert_not_called()

    def test_cancelar_reserva_exitoso(self):
        """Testea la cancelación exitosa de una reserva."""
        input_dto = CancelarReservaInputDTO("test-id")

        # Setup: La reserva existe y no está en estados finales.
        mock_reserva = MagicMock()
        mock_reserva.aula_id = "A101"
        self.mock_reserva_repo.get_by_id.return_value = mock_reserva

        # Ejecución
        try:
            self.service.cancelar_reserva(input_dto)
        except Exception as e:
             self.fail(f"La cancelación debería ser exitosa pero falló con: {e}")

        # Verificaciones
        self.mock_reserva_repo.update_state.assert_called_with("test-id", ReservaEstado.CANCELADA)

    def test_operacion_fallo_reserva_no_encontrada(self):
        """Testea que todas las operaciones fallan si la reserva no existe."""
        # Configurar el mock para devolver None/excepción
        self.mock_reserva_repo.get_by_id.return_value = None

        with self.assertRaises(ReservaError): # Catching the base domain exception
            self.service.confirmar_reserva(ConfirmarReservaInputDTO("non-existent"))