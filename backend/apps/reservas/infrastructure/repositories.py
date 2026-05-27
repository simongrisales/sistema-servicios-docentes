# reservas/infrastructure/repositories.py

from datetime import datetime
from typing import List, Optional
from django.utils import timezone
from sistema_servicios_docentes.backend.apps.reservas.domain.interfaces import IReservaRepository
from sistema_servicios_docentes.backend.apps.reservas.domain.entities import ReservaEstado
from .models import ReservaModel

class ReservaRepository(IReservaRepository):
    """Implementación concreta del repositorio de Reservas usando Django ORM."""

    def get_by_id(self, reserva_id: str) -> Optional['Reserva']:
        try:
            # Asumimos que 'reserva_id' en el dominio se mapea al PK o a un campo único. Usaremos pk por defecto para simplicidad.
            model_instance = ReservaModel.objects.get(pk=reserva_id)
            return Reserva(
                reserva_id=str(model_instance.pk), # Mapear el PK como ID de dominio
                aula_id=model_instance.aula.id,
                bloque_horario_inicio=model_instance.bloque_horario.inicio,
                bloque_horario_fin=model_instance.bloque_horario.fin,
                solicitante_id=model_instance.solicitante,
                estado=model_instance.estado
            )
        except ReservaModel.DoesNotExist:
            return None

    def create(self, reserva: 'Reserva') -> None:
        """Persiste la entidad de reserva en el ORM."""
        # El modelo requiere el aula y bloque horarios ya existentes (ForeignKey).
        # Asumimos que al llamar a esta capa, las entidades existen.
        try:
            ReservaModel.objects.create(
                aula=reserva.aula_id, # Aquí debería ser la instancia del objeto Aula o su FK
                bloque_horario=reserva.bloque_horario_inicio.get_fk(), # Placeholder para obtener el bloque horario real
                solicitante=reserva.solicitante_id,
                estado=reserva.estado,
                fecha_expiracion=timezone.now() + datetime.timedelta(days=30) # Expiración por defecto de 30 días
            )
        except Exception as e:
             raise type(e)(f"Error al crear reserva en la DB: {e}")


    def update_state(self, reserva_id: str, new_estado: str) -> None:
        """Actualiza solo el estado y actualiza el timestamp."""
        try:
            instance = ReservaModel.objects.get(pk=reserva_id)
            # Validaciones de transacciones deberían ocurrir en la capa de Caso de Uso (use_cases.py)
            instance.estado = new_estado
            instance.save()
        except ReservaModel.DoesNotExist:
             raise Exception("Reserva no encontrada para actualizar.")


    def find_conflicts(self, aula_id: str, inicio: datetime, fin: datetime) -> List['Reserva']:
        """Busca conflictos de reservas activas en el bloque horario especificado."""
        from django.utils import timezone
        # La lógica SQL debe buscar cualquier reserva donde:
        # 1. Aula ID coincida.
        # 2. El estado sea CONFIRMADO o PENDIENTE.
        # 3. Hay superposición de horarios (startA < endB y endA > startB).

        conflictos_model = ReservaModel.objects.filter(
            aula=aula_id,
            estado__in=[ReservaEstado.CONFIRMADA, ReservaEstado.PENDIENTE] # Solo consideramos estados activos para conflicto
        ).annotate(
            # Lógica de superposición en el backend:
            overlap_check=models.Q(bloque_horario__fin__lt=timezone.make_aware(datetime.datetime)(f'{inicio.__date__()}', f'{fin.__time__()'}))
                     & models.Q(bloque_horario__inicio__gt=timezone.make_aware(datetime.datetime)(f'{inicio.__date__()}', f'{inicio.__time__()}')) # Simplificación conceptual

        # Nota: La implementación real debe ser más precisa en la lógica de superposición.
        return [Reserva(reserva_id="conflict", aula_id=aula_id, inicio=inicio, fin=fin, solicitante_id="", estado="") for _ in range(1)] # Placeholder

    def find_expired_reservations(self) -> List['Reserva']:
        """Recupera y marca reservas expiradas en un proceso de fondo."""
        from django.utils import timezone
        now = timezone.localtime(timezone.now())
        # Filtrar por reservas que deberían haber expirado ya (ejemplo: hoy o ayer)
        expired_models = ReservaModel.objects.filter(fecha_expiracion__lt=now).distinct()

        reserva_list = []
        for model in expired_models:
            # Aquí se llamaría al método de negocio para marcarlo, pero por ahora solo listamos la entidad.
            pass # Lógica de expiración a completar en el worker de Celery
        return reserva_list