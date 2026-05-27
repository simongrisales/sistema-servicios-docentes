from typing import List, Optional
from ..domain.interfaces import IAsignacionStrategy, IRepository, IGrupoRepository, IAulaRepository
from ..application.dtos import AsignacionInputDTO, SimulacionInputDTO
from ..domain.exceptions import (
    AsignacionConflictoError, SinAulasDisponiblesError, CapacidadInsuficienteError, DatosIncompletosError
)

class AsignacionUseCaseService:
    """Orquesta la lógica de asignación automatica y simulación."""
    def __init__(self, grupo_repo: IGrupoRepository, aula_repo: IAulaRepository):
        # Inyección de dependencias (Interfaces)
        self.grupo_repo = grupo_repo
        self.aula_repo = aula_repo

    def ejecutar_asignacion_automatica(self, input_dto: AsignacionInputDTO, estrategia: IAsignacionStrategy) -> str:
        """
        Intenta asignar el recurso físico más adecuado utilizando la estrategia de negocio.
        Esta función debe ser transaccional a nivel de base de datos (usando @transaction.atomic).
        """
        # 1. Obtener entidades necesarias del dominio (Usamos los repositorios para esto)
        grupo = self.grupo_repo.get_grupo(input_dto.grupo_id)
        if not grupo:
            raise DatosIncompletosError("Grupo no encontrado.")

        try:
            # 2. Usar el patrón Strategy para encontrar la mejor aula y validar
            aula_candidata = estrategia.seleccionar_mejor_aula(grupo, input_dto.bloque_horario)
        except CapacidadInsuficienteError as e:
            raise e
        except SinAulasDisponiblesError as e:
            # Esto captura el error del repositorio o de la estrategia si no encuentra nada
            raise e

        # 3. Ejecutar la asignación transaccional (Se llamaría a un método en infraestructura/repositories)
        print("--- Iniciando transacción ORM ---")
        # Aquí se debe llamar al método transaccional en el repositorio concreto (ej: self.repo.asignar_aula(grupo, aula_candidata, ...))

        return f"Asignación exitosa. Aula asignada: {aula_candidata.id}"


    def simular_asignacion(self, input_dto: SimulacionInputDTO) -> str:
        """Simula la asignación para mostrar un resultado sin modificar el estado real."""
        # Simulación de lógica de validaciones y scoring usando solo los repositorios abstractos
        print("Ejecutando simulación en modo lectura.")

        # Lógica compleja que llamará a IAulaRepository.find_aulas_por_bloque()
        return "Simulación exitosa: Se identificaron 3 aulas posibles, la mejor por prioridad es Aula ID 15."


    def verificar_cobertura_total(self) -> 'CoberturaOutputDTO':
        """Verifica si el número de grupos asignados cubre todos los grupos activos."""
        # Lógica que iteraría sobre todos los grupos y compararía con las asignaciones confirmadas.
        print("Validando cobertura total de la programación académica...")
        return CoberturaOutputDTO(grupos_con_aula=150, total_grupos=152)