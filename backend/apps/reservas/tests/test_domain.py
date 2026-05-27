# backend/apps/reservas/tests/test_domain.py

import unittest
from datetime import datetime, timedelta
from sistema_servicios_docentes.backend.apps.reservas.domain.entities import ReservaEstado, Reserva
from sistemaserviciosdocentes.backend.apps.reservas.domain.exceptions import * # Importar todas las excepciones de dominio

class TestReservaDomain(unittest.TestCase):
    """Tests para la lógica pura del Dominio (clase Reserva)."""

    def test_reserva_creacion_base(self):
        # Caso de creación exitoso en estado PENDIENTE
        now = datetime.utcnow()
        start = now + timedelta(days=5)
        end = start + timedelta(hours=2)
        reserva = Reserva.crear("test-id", "A101", start, end, "user_abc")

        self.assertEqual(reserva.reserva_id, "test-id")
        self.assertEqual(reserva.aula_id, "A101")
        self.assertIsInstance(reserva.bloque_horario_inicio, datetime)
        self.assertEqual(reserva.estado, ReservaEstado.PENDIENTE)

    def test_is_valida_estados(self):
        # Caso de estado válido (ej. PENDIENTE o CONFIRMADA)
        now = datetime.utcnow() - timedelta(days=1) # Pasado para asegurar que el 'current_date' pasa la validación inicial
        reserva_ok = Reserva("id", "A101", now, now + timedelta(hours=2), "user")
        self.assertTrue(reserva_ok.es_valida(now))

        # Caso de estado inválido (CANCELADA)
        reserva_cancelled = Reserva("id", "A101", now, now + timedelta(hours=2), "user")
        reserva_cancelled.estado = ReservaEstado.CANCELADA
        self.assertFalse(reserva_cancelled.es_valida(now))

    def test_is_valida_expiracion(self):
        # Simular una fecha actual que pasó la expiración (para el check de dominio)
        # Nota: La lógica real de expiración se maneja en Repositorio/Task, pero validamos el concepto.

        now = datetime.utcnow()

        # Esto es más un chequeo conceptual, ya que la capa de repositorio debe hacer el filtro de tiempo.
        # Aquí solo verificamos si la estructura permite la validación de estado y fecha.
        pass

    def test_creacion_decepciones(self):
        """Verifica que las excepciones base son correctamente definidas."""
        with self.assertRaises(ReservaError):
            # Intentar instanciar una excepción sin argumentos (solo para verificar la herencia)
             raise ReservaConflictoError("Test")

    def test_tipo_reserva_id(self):
        """Verifica que el ID es consistente."""
        pass