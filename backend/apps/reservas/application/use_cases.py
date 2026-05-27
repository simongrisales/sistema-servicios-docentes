from datetime import datetime
from typing import List
from ..domain.interfaces import IReservaRepository
from ..domain.entities import ReservaEstado, ReservaError, ReservaConflictoError, ReservaExpiradaError
from .dtos import CrearReservaInputDTO, ConfirmarReservaInputDTO, CancelarReservaInputDTO

# Importación crítica de otro módulo para la validación de conflictos (Asignaciones)
# Este es el punto donde se debe orquestar con asignacion.application.use_cases
from sistema_servicios_docentes.backend.apps.asignacion.domain.interfaces import IAsignacionRepository

class ReservaService:
    """
    Orquesta la creación y gestión del ciclo de vida de las reservas,
    aplicando reglas de negocio transversales.
    """
    def __init__(self, reserva_repo: IReservaRepository, asignacion_repo: IAsignacionRepository):
        self.reserva_repo = reserva_repo
        self.asignacion_repo = asignacion_repo

    def crear_reserva(self, input: CrearReservaInputDTO) -> ReservaOutputDTO:
        """
        Crea una nueva reserva después de validar disponibilidad y conflictos.
        """
        # 1. Validar si el aula está libre durante todo el rango solicitado contra asignaciones confirmadas.
        conflicts = self.asignacion_repo.find_conflicts(input.aula_id, input.inicio, input.fin)

        if conflicts:
            raise ReservaConflictoError(
                f"El aula {input.aula_id} está en conflicto con {len(conflicts)} asignaciones confirmadas."
            )

        # 2. Validar conflictos internos de la reserva (si ya hay otras reservas pendientes que se superpongan).
        reservas_existentes = self.reserva_repo.find_conflicts(input.aula_id, input.inicio, input.fin)
        if reservas_existentes:
            # Podríamos permitir conflictos si son *propio* o si es un estado específico,
            # pero por seguridad, lanzamos error si hay superposición con otro estado PENDIENTE/CONFIRMADO.
             raise ReservaConflictoError("Este bloque horario ya está reservado de forma pendiente o confirmada.")

        # 3. Crear la entidad y persistir.
        reserva = Reserva.crear(
            reserva_id="TEMP-" + str(hash(input)), # Placeholder para ID real
            aula_id=input.aula_id,
            inicio=input.inicio,
            fin=input.fin,
            solicitante_id=input.solicitante_id
        )
        self.reserva_repo.create(reserva)

        return ReservaOutputDTO(
            reserva_id=reserva.reserva_id,
            aula_id=reserva.aula_id,
            inicio=reserva.bloque_horario_inicio,
            fin=reserva.bloque_horario_fin,
            solicitante_id=reserva.solicitante_id,
            estado=ReservaEstado.PENDIENTE
        )

    def confirmar_reserva(self, input: ConfirmarReservaInputDTO) -> ReservaOutputDTO:
        """
        Cambia el estado de la reserva a CONFIRMADA después de una validación final (ej. por un líder DOC).
        Debe re-validar conflictos contra nuevas asignaciones o cambios en datos maestros.
        """
        # Re-Validación es crítica aquí, ya que otras transacciones pudieron haber ocurrido desde la solicitud inicial.
        reserva = self.reserva_repo.get_by_id(input.reserva_id)
        if not reserva:
            raise ReservaError("Reserva no encontrada.")

        # Validar nuevamente contra asignaciones confirmadas (puede que algo haya cambiado).
        conflicts = self.asignacion_repo.find_conflicts(reserva.aula_id, reserva.bloque_horario_inicio, reserva.bloque_horario_fin)
        if conflicts:
            raise ReservaConflictoError("Imposible confirmar la reserva debido a conflictos detectados después de la solicitud.")

        # Confirmación Exitosa
        self.reserva_repo.update_state(input.reserva_id, ReservaEstado.CONFIRMADA)

        return ReservaOutputDTO(
            reserva_id=input.reserva_id,
            aula_id=reserva.aula_id,
            inicio=reserva.bloque_horario_inicio,
            fin=reserva.bloque_horario_fin,
            solicitante_id=reserva.solicitante_id,
            estado=ReservaEstado.CONFIRMADA
        )

    def cancelar_reserva(self, input: CancelarReservaInputDTO):
        """
        Cambia el estado de la reserva a CANCELADA.
        Solo debe ser llamado por el propietario o un administrador con permisos elevados.
        """
        # Aquí se añadiría la lógica de verificación de roles/permisos (usando IUsuarioRepository)
        reserva = self.reserva_repo.get_by_id(input.reserva_id)
        if not reserva:
            raise ReservaError("Reserva no encontrada.")

        self.reserva_repo.update_state(input.reserva_id, ReservaEstado.CANCELADA)
        print(f"Reserva {input.reserva_id} cancelada exitosamente.")