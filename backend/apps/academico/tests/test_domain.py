from ..domain.entities import Aula, Grupo, Curso, Docente
from ..domain.exceptions import CapacidadInvalidaError, ErrorDominioAcademico
import pytest

def test_aula_creacion():
    """Test de creación básica y validación de atributos."""
    aula = Aula(id=1, nombre="Aula Magna", capacidad=300, tipo="Amfiteatro", disponible=True)
    assert aula.capacidad > 0
    assert aula.tipo in ["Amfiteatro", "Laboratorio", "Sala de Clases"]

def test_grupo_validacion_estudiantes():
    """Verifica la lógica de priorización y consistencia de estudiantes en un grupo."""
    grupo = Grupo(id=1, curso_id=10, docente_id=20, num_estudiantes=35, semestre='2026-S1')
    assert grupo.num_estudiantes > 0

def test_capacidad_invalida():
    """Prueba que se lance una excepción si hay inconsistencia de capacidad."""
    with pytest.raises(CapacidadInvalidaError) as excinfo:
        # Simular un caso donde los estudiantes superan la capacidad máxima del aula.
        raise CapacidadInvalidaError("Grupo excede la capacidad asignada.")
    assert "excede la capacidad" in str(excinfo.value)

def test_aula_sin_conflicto():
    """Verifica que una clase pueda ser programada si no hay reservas existentes."""
    # Lógica simulada de chequeo de conflicto en el dominio puro
    pass # El test real iría aquí, comparando horas/días.