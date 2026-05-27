# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist

class TestAsignacionDominio:
    """Pruebas de las entidades y la lógica de validación del dominio de asignación."""

    def test_asignacion_es_valida(self):
        # Prueba básica de validez de una entidad Asignacion (solo simulación)
        # Implementar la lógica que chequea si los campos son coherentes.
        pass # A implementar

    def test_detectar_conflicto_horario(self):
        """Verifica que el sistema detecte correctamente dos asignaciones en el mismo Aula y HorarioBloque."""
        # Datos simulados de conflicto: Asignación 1 y Asignación 2 con mismas coordenadas.
        pass # A implementar

    def test_priorizacion_estudiantes(self):
        """Verifica que la regla de negocio priorice grupos con mayor número de estudiantes."""
        # Se debe crear una función o método estático en el dominio para calcular/validar esto.
        pass # A implementar

class TestExcepcionesDominio:
    """Pruebas de las excepciones del módulo asignacion."""
    def test_manejo_excepciones(self):
        # Se debe probar que al fallar una validación, se levante la excepción correcta (ej. CapacidadInsuficienteError).
        pass # A implementar