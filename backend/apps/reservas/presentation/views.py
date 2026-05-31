from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..application.dtos import (
    CancelarReservaInputDTO,
    ConfirmarReservaInputDTO,
    CrearReservaInputDTO,
)
from ..application.use_cases import ReservaService
from ..domain.entities import ReservaEstado
from ..domain.exceptions import ReservaConflictoError
from .serializers import CrearReservaSerializer, ReservaOutputSerializer


class ReservasViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _service(self) -> ReservaService:
        from ..infrastructure.repositories import ReservaRepository

        return ReservaService(reserva_repo=ReservaRepository())

    def create(self, request):
        serializer = CrearReservaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            reserva = self._service().crear_reserva(
                CrearReservaInputDTO(**serializer.validated_data)
            )
        except ReservaConflictoError as error:
            return Response(
                {"detail": str(error) or "No fue posible crear la reserva."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            ReservaOutputSerializer(reserva).data,
            status=status.HTTP_201_CREATED,
        )

    def list(self, request):
        from ..infrastructure.repositories import ReservaRepository

        reservas = [
            reserva
            for reserva in ReservaRepository().list()
            if reserva.estado in {ReservaEstado.PENDIENTE, ReservaEstado.CONFIRMADA}
        ]
        reservas.sort(key=lambda item: item.bloque_horario_inicio, reverse=True)
        payload = [
            {
                "reserva_id": reserva.reserva_id,
                "aula_id": reserva.aula_id,
                "inicio": reserva.bloque_horario_inicio,
                "fin": reserva.bloque_horario_fin,
                "solicitante_id": reserva.solicitante_id,
                "estado": reserva.estado,
            }
            for reserva in reservas
        ]
        return Response(ReservaOutputSerializer(payload, many=True).data)

    @action(detail=True, methods=["post"], url_path="confirmar")
    def confirmar(self, request, pk=None):
        reserva = self._service().confirmar_reserva(
            ConfirmarReservaInputDTO(reserva_id=str(pk))
        )
        return Response(ReservaOutputSerializer(reserva).data)

    @action(detail=True, methods=["post"], url_path="cancelar")
    def cancelar(self, request, pk=None):
        self._service().cancelar_reserva(CancelarReservaInputDTO(reserva_id=str(pk)))
        return Response(status=status.HTTP_204_NO_CONTENT)
