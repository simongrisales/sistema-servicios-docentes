# Requiere Mocking de Repositorios
from unittest.mock import MagicMock
import pytest
from ..application.use_cases import UseCasesService
from ..domain.exceptions import AulaNoDisponibleError

@pytest.fixture
def mock_repos():
    """Fixture que devuelve mocks de los repositorios para inyección en el servicio."""
    return {
        'aula_repo': MagicMock(),
        'grupo_repo': MagicMock(),
        'curso_repo': MagicMock(),
        'docente_repo': MagicMock()
    }

@pytest.fixture
def service(mock_repos):
    """Fixture que inicializa UseCasesService con los mocks."""
    return UseCasesService(
        aula_repo=mock_repos['aula_repo'],
        grupo_repo=mock_repos['grupo_repo'],
        curso_repo=mock_repos['curso_repo'],
        docente_repo=mock_repos['docente_repo']
    )

def test_crear_grupo_exito(service, mock_repos):
    """Prueba exitosa de creación de grupo y validación de dependencias."""
    # Configurar mocks para simular que Cursos y Docentes existen
    mock_repos['curso_repo'].get_by_id.return_value = MagicMock()
    mock_repos['docente_repo'].get_by_usuario_id.return_value = MagicMock()

    # Ejecutar el caso de uso
    grupo_dto = GrupoInputDTO(grupo_id=1, curso_id=10, docente_id=20, num_estudiantes=35)
    resultado = service.crear_grupo(grupo_dto)

    assert resultado.grupo_id == 999 # Verifica que el ID placeholder se use o se actualice

def test_crear_grupo_fallo_docente(service, mock_repos):
    """Prueba que falla la creación si el docente no existe."""
    mock_repos['curso_repo'].get_by_id.return_value = MagicMock()
    # Simular que NO se encuentra un docente
    mock_repos['docente_repo'].get_by_usuario_id.return_value = None

    grupo_dto = GrupoInputDTO(grupo_id=1, curso_id=10, docente_id=999, num_estudiantes=35)

    with pytest.raises(GrupoSinDocenteError):
        service.crear_grupo(grupo_dto)

def test_listar_aulas_disponibles_exito(service, mock_repos):
    """Prueba que se listan aulas correctamente cuando hay disponibilidad."""
    # Configurar el retorno del repositorio de aulas para simular 3 aulas disponibles
    mock_aula_repo = MagicMock()
    mock_aula_repo.find_available_aulas.return_value = [
        Aula(id=1, nombre="A", capacidad=50, tipo="Sala de Clases", disponible=True),
        Aula(id=2, nombre="B", capacidad=80, tipo="Laboratorio", disponible=True),
    ]
    # Sobrescribir el mock para la prueba
    service.aula_repo = MagicMock()
    service.aula_repo.find_available_aulas = mock_aula_repo.find_available_aulas

    horario_bloque = HorarioBloque(dia="Lunes", hora_inicio=8.0, hora_fin=9.0)
    resultados = service.listar_aulas_disponibles(horario_bloque)

    assert len(resultados) == 2
    assert resultados[1].nombre == "Laboratorio"