"""Implementacion concreta del repositorio de parametros (Django ORM)."""

from collections.abc import Iterable
from typing import Any

from core.repositories import BaseRepository
from core.sanitizers import BleachSanitizerMixin

from ..domain.entities import CatalogoParametro
from ..domain.interfaces import ICatalogoParametroRepository
from .models import CatalogoParametroModel


class CatalogoParametroRepository(
    BleachSanitizerMixin,
    BaseRepository[CatalogoParametro, str],
    ICatalogoParametroRepository,
):
    """Repositorio que persiste CatalogoParametro en PostgreSQL via Django ORM."""

    text_fields = ("clave", "grupo", "descripcion")

    @staticmethod
    def _to_entity(model: CatalogoParametroModel) -> CatalogoParametro:
        return CatalogoParametro(
            clave=model.clave,
            valor=model.valor,
            grupo=model.grupo,
            descripcion=model.descripcion,
            activo=model.activo,
        )

    def get(self, entity_id: str) -> CatalogoParametro | None:
        return self.obtener(entity_id)

    def list(self, **filters: Any) -> Iterable[CatalogoParametro]:
        grupo = filters.get("grupo")
        return self.listar(grupo=grupo)

    def create(self, data: dict[str, Any]) -> CatalogoParametro:
        parametro = CatalogoParametro(
            clave=data["clave"],
            valor=data["valor"],
            grupo=data.get("grupo", "general"),
            descripcion=data.get("descripcion", ""),
            activo=data.get("activo", True),
        )
        return self.guardar(parametro)

    def update(self, entity_id: str, data: dict[str, Any]) -> CatalogoParametro:
        existente = self.obtener(entity_id)
        parametro = CatalogoParametro(
            clave=entity_id,
            valor=data.get("valor", existente.valor if existente else {}),
            grupo=data.get("grupo", existente.grupo if existente else "general"),
            descripcion=data.get(
                "descripcion", existente.descripcion if existente else ""
            ),
            activo=data.get("activo", existente.activo if existente else True),
        )
        return self.guardar(parametro)

    def delete(self, entity_id: str) -> None:
        self.eliminar(entity_id)

    def obtener(self, clave: str) -> CatalogoParametro | None:
        try:
            model = CatalogoParametroModel.objects.get(clave=clave)
            return self._to_entity(model)
        except CatalogoParametroModel.DoesNotExist:
            return None

    def listar(self, grupo: str | None = None) -> Iterable[CatalogoParametro]:
        queryset = CatalogoParametroModel.objects.filter(activo=True)
        if grupo:
            queryset = queryset.filter(grupo=grupo)
        return [self._to_entity(model) for model in queryset]

    def guardar(self, parametro: CatalogoParametro) -> CatalogoParametro:
        data = self.sanitize_payload(
            {
                "clave": parametro.clave,
                "valor": parametro.valor,
                "grupo": parametro.grupo,
                "descripcion": parametro.descripcion,
                "activo": parametro.activo,
            }
        )
        model, _ = CatalogoParametroModel.objects.update_or_create(
            clave=data["clave"],
            defaults=data,
        )
        return self._to_entity(model)

    def eliminar(self, clave: str) -> None:
        CatalogoParametroModel.objects.filter(clave=clave).delete()

    def obtener_valor(self, clave: str, default: Any = None) -> Any:
        try:
            return CatalogoParametroModel.objects.values_list(
                "valor",
                flat=True,
            ).get(clave=clave)
        except CatalogoParametroModel.DoesNotExist:
            return default
