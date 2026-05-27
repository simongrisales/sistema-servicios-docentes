# reservas/presentation/views.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import CrearReservaSerializer, ReservaOutputSerializer
from sistema_servicios_docentes.backend.apps.reservas.application.use_cases import ReservaService
from sistemaserviciosdocentes.backend.core.repositories import BaseRepository # Para obtener el repo y servicios base

class ReservasViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar la creación, confirmación y cancelación de reservas de aula.
    Implementa la lógica transaccional delegando a ReservaService.
    Permisos: Requiere autenticación (ejemplo genérico).
    """

    # Nota: En una implementación real se debería usar un Permission Class que verifique el rol del usuario.

    def get_serializer_class(self):
        if self.action == 'create':
            return CrearReservaSerializer
        elif self.action in ['confirm', 'cancel']: # Usaremos acciones personalizadas para estos estados
             # Podríamos usar un serializer de acción simple aquí, por ahora, el DTO es suficiente.
             from .serializers import ReservaOutputSerializer
             return ReservaOutputSerializer
        else:
            return serializers.ModelSerializer

    def get_queryset(self):
        # Este queryset se usará para listar todas las reservas (filtrado por usuario/estado)
        # Por ahora, retornamos el queryset base del ORM si fuera necesario listarlas directamente.
        from .infrastructure.models import ReservaModel
        return ReservaModel.objects.all()


    def create(self, request, *args, **kwargs):
        """Implementa la creación de una nueva reserva."""
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        input_dto = CrearReservaInputDTO(**serializer.validated_data)

        # 1. Inicializar dependencias (deben ser inyectadas en un entorno real, aquí se instancian por simplicidad)
        repo = BaseRepository() # Usar el repositorio concreto de reservas
        asignacion_repo = BaseRepository() # Requerido para validar conflictos con asignaciones existentes

        try:
            # 2. Ejecutar la lógica de negocio crítica (Capa de Aplicación)
            reserva_service = ReservaService(reserva_repo=repo, asignacion_repo=asignacion_repo)
            output_dto = reserva_service.crear_reserva(input_dto)

            # 3. Devolver la respuesta serializada del DTO de salida
            serializer_output = ReservaOutputSerializer(output_dto)
            return Response(serializer_output.data, status=status.HTTP_201_CREATED)

        except from .domain.exceptions import ReservaConflictoError as ConflictError:
            return Response({"error": str(ConflictError)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
             # Capturar otras excepciones del negocio (ej. datos incompletos, etc.)
            return Response({"error": f"Error de procesamiento de reserva: {e}"}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Endpoint para confirmar una reserva pendiente (requiere rol 'Líder DOC')."""
        # Validación de permisos debe ir aquí
        try:
            serializer = self.get_serializer_class()(data=request.data)
            serializer.is_valid(raise_exception=True)
            input_dto = ConfirmarReservaInputDTO(**serializer.validated_data)

            repo = BaseRepository()
            asignacion_repo = BaseRepository() # Requerido para re-validación crítica del conflicto
            reserva_service = ReservaService(reserva_repo=repo, asignacion_repo=asignacion_repo)

            output_dto = reserva_service.confirmar_reserva(input_dto)
            return Response(ReservaOutputSerializer(output_dto).data, status=status.HTTP_200_OK)

        except Exception as e:
             # Capturar la excepción específica del servicio
            if "conflicto" in str(e):
                 return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
            return Response({"error": f"Error al confirmar reserva: {e}"}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Endpoint para cancelar una reserva."""
        # Validación de permisos debe ir aquí
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        input_dto = CancelarReservaInputDTO(**serializer.validated_data)

        repo = BaseRepository()
        reserva_service = ReservaService(reserva_repo=repo, asignacion_repo=BaseRepository()) # Asignaciones no necesarias para cancelación simple

        try:
            reserva_service.cancelar_reserva(input_dto)
            return Response({"status": "success", "message": f"Reserva {input_dto.reserva_id} cancelada con éxito."}, status=status.HTTP_200_OK)
        except Exception as e:
             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)