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
from .serializers import CrearReservaSerializer, ReservaOutputSerializer


class ReservasViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = CrearReservaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reserva = ReservaService().crear_reserva(
            CrearReservaInputDTO(**serializer.validated_data)
        )
        return Response(
            ReservaOutputSerializer(reserva).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], url_path="confirmar")
    def confirmar(self, request, pk=None):
        reserva = ReservaService().confirmar_reserva(
            ConfirmarReservaInputDTO(reserva_id=str(pk))
        )
        return Response(ReservaOutputSerializer(reserva).data)

    @action(detail=True, methods=["post"], url_path="cancelar")
    def cancelar(self, request, pk=None):
        ReservaService().cancelar_reserva(CancelarReservaInputDTO(reserva_id=str(pk)))
        return Response(status=status.HTTP_204_NO_CONTENT)
