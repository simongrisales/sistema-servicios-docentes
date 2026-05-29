from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..application.dtos import AulaInputDTO, GrupoInputDTO
from ..application.use_cases import AcademicoService
from ..infrastructure.repositories import (
    AulaRepository,
    DocenteRepository,
    GrupoRepository,
)
from .serializers import AulaInputSerializer, AulaOutputSerializer, GrupoSerializer


class AcademicoViewSet(viewsets.ViewSet):
    """Endpoints academicos basicos para aulas y grupos."""

    permission_classes = [IsAuthenticated]

    def _service(self) -> AcademicoService:
        return AcademicoService(
            aula_repo=AulaRepository(),
            grupo_repo=GrupoRepository(),
            docente_repo=DocenteRepository(),
        )

    def list(self, request):
        aulas = self._service().listar_aulas_disponibles()
        return Response(AulaOutputSerializer(aulas, many=True).data)

    def create(self, request):
        serializer = AulaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        aula = self._service().crear_aula(AulaInputDTO(**serializer.validated_data))
        return Response(
            AulaOutputSerializer(aula).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"], url_path="grupos")
    def crear_grupo(self, request):
        serializer = GrupoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        grupo = self._service().crear_grupo(GrupoInputDTO(**serializer.validated_data))
        return Response(GrupoSerializer(grupo).data, status=status.HTTP_201_CREATED)
