from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..application.dtos import AsignacionInputDTO, SimulacionInputDTO
from ..application.use_cases import AsignacionUseCaseService
from ..infrastructure.repositories import AsignacionRepository
from ..infrastructure.strategies import PrioridadEstudiantesStrategy
from .serializers import (
    SerializacionAsignacion,
    SerializacionCoberturaOutput,
    SerializacionResultadoAsignacion,
    SerializacionSimulacion,
)


class AsignacionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _service(self) -> AsignacionUseCaseService:
        return AsignacionUseCaseService(
            asignacion_repo=AsignacionRepository(),
            strategy=PrioridadEstudiantesStrategy(),
        )

    @action(detail=False, methods=["post"], url_path="ejecutar")
    def ejecutar(self, request):
        serializer = SerializacionAsignacion(data=request.data)
        serializer.is_valid(raise_exception=True)
        resultado = self._service().ejecutar_asignacion_automatica(
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
        resultado = self._service().simular_asignacion(
            SimulacionInputDTO(**serializer.validated_data)
        )
        return Response(SerializacionResultadoAsignacion(resultado).data)

    @action(detail=False, methods=["get"], url_path="cobertura")
    def cobertura(self, request):
        resultado = self._service().verificar_cobertura_total(
            request.query_params.get("semestre", "")
        )
        return Response(SerializacionCoberturaOutput(resultado).data)
