from django.db import models
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..application.dtos import AulaInputDTO, GrupoInputDTO
from ..application.use_cases import AcademicoService
from ..infrastructure.models import (
    AulaModel,
    CursoModel,
    DocenteModel,
    FacultadModel,
    GrupoModel,
    HorarioBloqueModel,
    ProgramaModel,
)
from ..infrastructure.repositories import (
    AulaRepository,
    DocenteRepository,
    GrupoRepository,
)
from .serializers import (
    AulaBusquedaSerializer,
    AulaEstadoSerializer,
    AulaInputSerializer,
    AulaOutputSerializer,
    CursoOutputSerializer,
    DocenteOutputSerializer,
    FacultadOutputSerializer,
    GrupoOutputSerializer,
    GrupoSerializer,
    ProgramaOutputSerializer,
)


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

    @action(detail=False, methods=["get"], url_path="buscar")
    def buscar(self, request):
        serializer = AulaBusquedaSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        q = serializer.validated_data.get("q", "").strip()
        queryset = AulaModel.objects.filter(activa=True).order_by("nombre")
        if q:
            queryset = queryset.filter(nombre__icontains=q)
        data = [
            {
                "id": aula.id,
                "nombre": aula.nombre,
                "capacidad": aula.capacidad,
                "tipo": aula.tipo,
                "disponible": aula.disponible,
                "activa": aula.activa,
            }
            for aula in queryset
        ]
        return Response(AulaOutputSerializer(data, many=True).data)

    @action(detail=True, methods=["patch"], url_path="estado")
    def estado(self, request, pk=None):
        serializer = AulaEstadoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cambios = serializer.validated_data
        if not cambios:
            return Response(
                {"detail": "Debes enviar al menos un campo de estado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        aula = AulaRepository().update(pk, cambios)
        return Response(AulaOutputSerializer(aula).data)

    @action(detail=False, methods=["get"], url_path="facultades")
    def facultades(self, request):
        facultades = (
            FacultadModel.objects.annotate(
                programas_count=models.Count("programas", distinct=True)
            )
            .filter(activa=True)
            .order_by("nombre")
        )
        data = [
            {
                "id": facultad.id,
                "codigo": facultad.codigo,
                "nombre": facultad.nombre,
                "activa": facultad.activa,
                "programas": facultad.programas_count,
            }
            for facultad in facultades
        ]
        return Response(FacultadOutputSerializer(data, many=True).data)

    @action(detail=False, methods=["get"], url_path="programas")
    def programas(self, request):
        facultad_id = request.query_params.get("facultad_id")
        queryset = (
            ProgramaModel.objects.select_related("facultad")
            .filter(activo=True)
            .order_by("facultad__nombre", "nombre")
        )
        if facultad_id:
            queryset = queryset.filter(facultad_id=facultad_id)
        data = [
            {
                "id": programa.id,
                "facultad_id": programa.facultad_id,
                "facultad_codigo": programa.facultad.codigo,
                "facultad_nombre": programa.facultad.nombre,
                "codigo": programa.codigo,
                "nombre": programa.nombre,
                "activo": programa.activo,
            }
            for programa in queryset
        ]
        return Response(ProgramaOutputSerializer(data, many=True).data)

    @action(detail=False, methods=["get"], url_path="docentes")
    def docentes(self, request):
        docentes = DocenteModel.objects.filter(activo=True).order_by("nombre")
        data = [
            {
                "id": docente.id,
                "nombre": docente.nombre,
                "email": docente.email,
                "activo": docente.activo,
            }
            for docente in docentes
        ]
        return Response(DocenteOutputSerializer(data, many=True).data)

    @action(detail=False, methods=["get"], url_path="cursos")
    def cursos(self, request):
        cursos = (
            CursoModel.objects.select_related("programa", "programa__facultad")
            .filter(activo=True)
            .order_by("programa__facultad__nombre", "codigo")
        )
        data = [
            {
                "id": curso.id,
                "programa_id": curso.programa_id,
                "programa_nombre": curso.programa.nombre,
                "facultad_nombre": curso.programa.facultad.nombre,
                "codigo": curso.codigo,
                "nombre": curso.nombre,
                "creditos": curso.creditos,
                "activo": curso.activo,
            }
            for curso in cursos
        ]
        return Response(CursoOutputSerializer(data, many=True).data)

    @action(detail=False, methods=["get"], url_path="bloques")
    def bloques(self, request):
        bloques = HorarioBloqueModel.objects.filter(activo=True).order_by(
            "dia", "hora_inicio"
        )
        return Response(
            [
                {
                    "id": bloque.id,
                    "dia": bloque.dia,
                    "hora_inicio": bloque.hora_inicio,
                    "hora_fin": bloque.hora_fin,
                    "activo": bloque.activo,
                }
                for bloque in bloques
            ]
        )

    @action(detail=False, methods=["get", "post"], url_path="grupos")
    def crear_grupo(self, request):
        if request.method.lower() == "get":
            grupos = (
                GrupoModel.objects.select_related("curso", "docente")
                .filter(activo=True)
                .order_by("semestre", "curso__codigo", "codigo")
            )
            data = [
                {
                    "id": grupo.id,
                    "curso_id": grupo.curso_id,
                    "curso_codigo": grupo.curso.codigo,
                    "curso_nombre": grupo.curso.nombre,
                    "docente_id": grupo.docente_id,
                    "docente_nombre": grupo.docente.nombre,
                    "codigo": grupo.codigo,
                    "num_estudiantes": grupo.num_estudiantes,
                    "semestre": grupo.semestre,
                    "activo": grupo.activo,
                }
                for grupo in grupos
            ]
            return Response(GrupoOutputSerializer(data, many=True).data)
        serializer = GrupoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        grupo = self._service().crear_grupo(GrupoInputDTO(**serializer.validated_data))
        return Response(GrupoSerializer(grupo).data, status=status.HTTP_201_CREATED)
