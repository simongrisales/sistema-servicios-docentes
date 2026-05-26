from typing import List, Optional
from ..domain.interfaces import IAulaRepository, IGrupoRepository, ICursoRepository, IDocenteRepository
from .dtos import GrupoInputDTO, CargaMasivaInputDTO, AulaOutputDTO
from .domain.exceptions import GrupoSinDocenteError, CapacidadInvalidaError

class UseCasesService:
    """Clase de orquestación que contiene la lógica de negocio para el módulo académico."""
    def __init__(self, aula_repo: IAulaRepository, grupo_repo: IGrupoRepository, curso_repo: ICursoRepository, docente_repo: IDocenteRepository):
        # Inyección de dependencias (Interfaces)
        self.aula_repo = aula_repo
        self.grupo_repo = grupo_repo
        self.curso_repo = curso_repo
        self.docente_repo = docente_repo

    # --- Lógica de Gestión de Grupos ---

    def crear_grupo(self, dto: GrupoInputDTO) -> 'GrupoOutputDTO':
        """Crea un grupo verificando las dependencias necesarias (Curso, Docente)."""
        # Aquí iría la lógica para verificar Curso/Docente antes de crear.
        if not self.curso_repo.get_by_id(dto.curso_id): # Usar IFacultadRepository si fuera necesario
             raise ValueError("Curso no encontrado.")
        if not self.docente_repo.get_by_usuario_id(dto.docente_id):
            # Esto debería ser capturado por una excepción de dominio, pero usamos esta validación simple aquí.
            raise GrupoSinDocenteError(grupo_id=None) # Error que debe ser mejorado

        # Simular creación y obtener el ID real del grupo
        nuevo_grupo_id = 999 # Placeholder para el nuevo ID
        return GrupoOutputDTO(
            grupo_id=nuevo_grupo_id,
            curso_id=dto.curso_id,
            docente_id=dto.docente_id,
            num_estudiantes=dto.num_estudiantes
        )

    def cargar_masiva_grupos(self, dtos: List[CargaMasivaInputDTO]) -> List['GrupoOutputDTO']:
        """Procesa una lista de DTOs para crear múltiples grupos."""
        resultados = []
        for dto in dtos:
            try:
                # Iteramos sobre cada lote usando la misma lógica de creación individual.
                resultado = self.crear_grupo(GrupoInputDTO(
                    grupo_id=dto.grupo_id,
                    curso_id=dto.curso_id,
                    docente_id=dto.docente_id,
                    num_estudiantes=dto.num_estudiantes
                ))
                resultados.append(resultado)
            except (ValueError, GrupoSinDocenteError) as e:
                print(f"ADVERTENCIA: Falló la carga de un grupo. Error: {e}")
        return resultados

    # --- Lógica de Asignación y Disponibilidad de Aulas (Núcleo) ---

    def listar_aulas_disponibles(self, horario_bloque: 'HorarioBloque') -> List[AulaOutputDTO]:
        """Lista todas las aulas que no tienen conflictos en el bloque horario dado."""
        # Este método utilizará el IAulaRepository.find_available_aulas()
        aulas = self.aula_repo.find_available_aulas(horario_bloque) # Uso del repositorio abstracto

        return [AulaOutputDTO(
            aula_id=a.id,
            nombre=a.nombre,
            capacidad=a.capacidad,
            tipo=a.tipo,
            disponible=True
        ) for a in aulas]

    # --- Lógica de Negocio Compleja (Ejemplo: Asignación Automática) ---

    def ejecutar_asignacion_automatica(self, grupo_output: 'GrupoOutputDTO', horario: 'HorarioBloque') -> str:
        """Intenta asignar el aula óptima para un grupo dado en un momento específico."""
        # Aquí se llamaría al patrón Strategy para determinar la mejor asignación.
        print("Ejecutando lógica de asignación automática...")

        # 1. Buscar aulas disponibles (Usamos repositorio)
        aulas_disponibles = self.aula_repo.find_available_aulas(horario)

        # 2. Aplicar estrategias (Lógica del patrón Strategy aquí)
        if not aulas_disponibles:
             raise AulaNoDisponibleError("No hay aulas disponibles que cumplan con el horario.")

        # Simulación de elección: elegir la primera aula disponible por simplicidad en este ejemplo
        aula_asignada = aulas_disponibles[0]

        # 3. Realizar la asignación (Requiere una transacción y lógica ORM)
        print(f"Asignando Aula {aula_asignada.id} al Grupo {grupo_output.grupo_id}.")
        return f"Éxito: Aula {aula_asignada.id} asignada con éxito."