from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..application.dtos import ReporteInputDTO, SimulacionInputDTO
from ..application.use_cases import ReporteService
from .serializers import ReporteSerializer, ReporteSolicitudSerializer


class ReporteViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response([])

    @action(detail=False, methods=["post"], url_path="solicitar")
    def solicitar(self, request):
        serializer = ReporteSolicitudSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reporte_id = ReporteService().ejecutar_generacion_asincrona(
            ReporteInputDTO(
                usuario_id=request.user.id,
                **serializer.validated_data,
            )
        )
        return Response({"reporte_id": reporte_id}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["get"], url_path="estado")
    def obtener_estado(self, request, pk=None):
        output = ReporteService().obtener_estado_reporte(int(pk))
        return Response(ReporteSerializer(output).data)

    @action(detail=False, methods=["post"], url_path="simular")
    def simular(self, request):
        serializer = ReporteSolicitudSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        output = ReporteService().simular_generacion(
            SimulacionInputDTO(
                periodo_inicio=serializer.validated_data["periodo_inicio"],
                periodo_fin=serializer.validated_data["periodo_fin"],
            )
        )
        return Response(ReporteSerializer(output).data)
