"""Implementación concreta del repositorio de parámetros (Django ORM)."""

from collections.abc import Iterable
from typing import Any

from ..domain.entities import CatalogoParametro
from ..domain.interfaces import ICatalogoParametroRepository
from .models import CatalogoParametroModel


class CatalogoParametroRepository(ICatalogoParametroRepository):
    """Repositorio que persiste CatalogoParametro en PostgreSQL via Django ORM."""

    # ------------------------------------------------------------------
    # Helpers de conversión
    # ------------------------------------------------------------------

    @staticmethod
    def _to_entity(model: CatalogoParametroModel) -> CatalogoParametro:
        return CatalogoParametro(
            clave=model.clave,
            valor=model.valor,
            grupo=model.grupo,
            descripcion=model.descripcion,
            activo=model.activo,
        )

    # ------------------------------------------------------------------
    # Implementación de ICatalogoParametroRepository
    # ------------------------------------------------------------------

    def obtener(self, clave: str) -> CatalogoParametro | None:
        try:
            model = CatalogoParametroModel.objects.get(clave=clave)
            return self._to_entity(model)
        except CatalogoParametroModel.DoesNotExist:
            return None

    def listar(
        self, grupo: str | None = None
    ) -> Iterable[CatalogoParametro]:
        qs = CatalogoParametroModel.objects.filter(activo=True)
        if grupo:
            qs = qs.filter(grupo=grupo)
        return [self._to_entity(m) for m in qs]

    def guardar(self, parametro: CatalogoParametro) -> CatalogoParametro:
        model, _ = CatalogoParametroModel.objects.update_or_create(
            clave=parametro.clave,
            defaults={
                "valor": parametro.valor,
                "grupo": parametro.grupo,
                "descripcion": parametro.descripcion,
                "activo": parametro.activo,
            },
        )
        return self._to_entity(model)

    def eliminar(self, clave: str) -> None:
        CatalogoParametroModel.objects.filter(clave=clave).delete()

    def obtener_valor(self, clave: str, default: Any = None) -> Any:
        try:
            return CatalogoParametroModel.objects.values_list(
                "valor", flat=True
            ).get(clave=clave)
        except CatalogoParametroModel.DoesNotExist:
            return default
