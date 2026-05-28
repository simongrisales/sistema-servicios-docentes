from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..application.dtos import AsignacionInputDTO, SimulacionInputDTO
from ..application.use_cases import AsignacionUseCaseService
from .serializers import (
    SerializacionAsignacion,
    SerializacionCoberturaOutput,
    SerializacionResultadoAsignacion,
    SerializacionSimulacion,
)


class AsignacionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="ejecutar")
    def ejecutar(self, request):
        serializer = SerializacionAsignacion(data=request.data)
        serializer.is_valid(raise_exception=True)
        resultado = AsignacionUseCaseService().ejecutar_asignacion_automatica(
            AsignacionInputDTO(**serializer.validated_data)
        )
        return Response(
            SerializacionResultadoAsignacion(resultado).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"], url_path="simular")
    def simular(self, request):
        serializer = SerializacionSimulacion(data=request.data)
        serializer.is_valid(raise_exception=True)
        resultado = AsignacionUseCaseService().simular_asignacion(
            SimulacionInputDTO(**serializer.validated_data)
        )
        return Response(SerializacionResultadoAsignacion(resultado).data)

    @action(detail=False, methods=["get"], url_path="cobertura")
    def cobertura(self, request):
        resultado = AsignacionUseCaseService().verificar_cobertura_total()
        return Response(SerializacionCoberturaOutput(resultado).data)
