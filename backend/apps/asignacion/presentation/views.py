from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.usuarios.infrastructure.permissions import EsAdministradorOLiderDOC

from ..application.dtos import AsignacionInputDTO, SimulacionInputDTO
from ..application.use_cases import AsignacionUseCaseService
from ..domain.exceptions import (
    AsignacionConflictoError,
    CapacidadInsuficienteError,
    DatosIncompletosError,
)
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

    @staticmethod
    def _error_response(error: Exception) -> Response:
        if isinstance(error, AsignacionConflictoError):
            details = getattr(error, "detalles_conflicto", None) or [str(error)]
            return Response(
                {"detail": details[0], "detalles": details},
                status=status.HTTP_409_CONFLICT,
            )
        if isinstance(error, CapacidadInsuficienteError):
            return Response(
                {"detail": str(error) or "Capacidad insuficiente."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if isinstance(error, DatosIncompletosError):
            return Response(
                {"detail": str(error) or "Faltan datos para ejecutar la asignacion."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": "No fue posible completar la operacion."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @action(detail=False, methods=["post"], url_path="ejecutar")
    def ejecutar(self, request):
        serializer = SerializacionAsignacion(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not EsAdministradorOLiderDOC().has_permission(request, self):
            return Response(
                {"detail": "No tiene permisos para ejecutar la asignacion."},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            resultado = self._service().ejecutar_asignacion_automatica(
                AsignacionInputDTO(**serializer.validated_data)
            )
        except (
            AsignacionConflictoError,
            CapacidadInsuficienteError,
            DatosIncompletosError,
        ) as error:
            return self._error_response(error)
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

    @action(detail=False, methods=["post"], url_path="simular-semestre")
    def simular_semestre(self, request):
        serializer = SerializacionSimulacion(data=request.data)
        serializer.is_valid(raise_exception=True)
        resultado = self._service().simular_asignacion(
            SimulacionInputDTO(**serializer.validated_data)
        )
        return Response(SerializacionResultadoAsignacion(resultado).data)

    @action(detail=False, methods=["post"], url_path="ejecutar-semestre")
    def ejecutar_semestre(self, request):
        if not EsAdministradorOLiderDOC().has_permission(request, self):
            return Response(
                {"detail": "No tiene permisos para ejecutar la asignacion."},
                status=status.HTTP_403_FORBIDDEN,
            )
        semestre = request.data.get("semestre", "")
        if not semestre:
            return Response(
                {"detail": "El semestre es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            resultado = self._service().ejecutar_asignacion_automatica_semestre(
                semestre
            )
        except (
            AsignacionConflictoError,
            CapacidadInsuficienteError,
            DatosIncompletosError,
        ) as error:
            return self._error_response(error)
        return Response(
            SerializacionResultadoAsignacion(resultado).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["get"], url_path="cobertura")
    def cobertura(self, request):
        resultado = self._service().verificar_cobertura_total(
            request.query_params.get("semestre", "")
        )
        return Response(SerializacionCoberturaOutput(resultado).data)
