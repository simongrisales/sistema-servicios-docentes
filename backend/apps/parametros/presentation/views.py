"""Vistas REST para el catálogo de parámetros del sistema."""

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..application.dtos import ObtenerValorInputDTO, ParametroInputDTO

from ..application.use_cases import CatalogoParametroService
from ..domain.exceptions import (
    CatalogoParametroDuplicadoError,
    CatalogoParametroInvalidoError,
    CatalogoParametroNoEncontradoError,
)
from ..infrastructure.repositories import CatalogoParametroRepository
from .serializers import ObtenerValorSerializer, ParametroSerializer
from apps.usuarios.infrastructure.permissions import EsAdministrador


class CatalogoParametroViewSet(viewsets.ViewSet):
    """CRUD REST para parámetros del catálogo del sistema.

    Endpoints:
        GET  /api/parametros/                → listar (filtrables por ?grupo=)
        POST /api/parametros/                → crear
        GET  /api/parametros/{clave}/        → obtener uno
        PUT  /api/parametros/{clave}/        → actualizar
        DELETE /api/parametros/{clave}/      → eliminar
        POST /api/parametros/valor/          → obtener sólo el valor (con default)
    """

    permission_classes = [EsAdministrador]

    def _service(self) -> CatalogoParametroService:
        return CatalogoParametroService(CatalogoParametroRepository())

    # ------------------------------------------------------------------
    # CRUD estándar
    # ------------------------------------------------------------------

    def list(self, request: Request) -> Response:
        grupo = request.query_params.get("grupo")
        parametros = self._service().listar(grupo=grupo)
        return Response(
            ParametroSerializer(list(parametros), many=True).data
        )

    def create(self, request: Request) -> Response:
        serializer = ParametroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = ParametroInputDTO(**serializer.validated_data)
        try:
            output = self._service().crear(dto)
        except (CatalogoParametroDuplicadoError, CatalogoParametroInvalidoError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            ParametroSerializer(output).data,
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        try:
            output = self._service().obtener(pk)
        except CatalogoParametroNoEncontradoError as exc:
            return Response(
                {"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(ParametroSerializer(output).data)

    def update(self, request: Request, pk: str | None = None) -> Response:
        serializer = ParametroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # La clave viene en la URL (pk); forzamos coherencia
        data = {**serializer.validated_data, "clave": pk}
        dto = ParametroInputDTO(**data)
        try:
            output = self._service().actualizar(dto)
        except (CatalogoParametroNoEncontradoError, CatalogoParametroInvalidoError) as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(ParametroSerializer(output).data)

    def destroy(self, request: Request, pk: str | None = None) -> Response:
        try:
            self._service().eliminar(pk)
        except CatalogoParametroNoEncontradoError as exc:
            return Response(
                {"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    # ------------------------------------------------------------------
    # Endpoint de conveniencia: valor rápido con default
    # ------------------------------------------------------------------

    @action(detail=False, methods=["post"], url_path="valor")
    def obtener_valor(self, request: Request) -> Response:
        """Retorna sólo el valor de un parámetro, con fallback si no existe."""
        serializer = ObtenerValorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = ObtenerValorInputDTO(**serializer.validated_data)
        valor = self._service().obtener_valor(dto)
        return Response({"clave": dto.clave, "valor": valor})
