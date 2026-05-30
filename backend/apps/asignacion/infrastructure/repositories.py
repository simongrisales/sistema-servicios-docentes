from collections.abc import Iterable
from typing import Any

from django.apps import apps
from django.db import IntegrityError, transaction

from core.repositories import BaseRepository

from ..domain.entities import Asignacion
from ..domain.exceptions import AsignacionConflictoError
from ..domain.interfaces import IAsignacionRepository
from .models import AsignacionModel


class AsignacionRepository(
    BaseRepository[Asignacion, int],
    IAsignacionRepository,
):
    def get(self, entity_id: int) -> Asignacion | None:
        model = AsignacionModel.objects.filter(id=entity_id).first()
        return self._to_domain(model) if model else None

    def list(self, **filters: Any) -> Iterable[Asignacion]:
        return [
            self._to_domain(model)
            for model in AsignacionModel.objects.filter(**filters)
        ]

    def create(self, data: dict[str, Any]) -> Asignacion:
        return self._to_domain(AsignacionModel.objects.create(**data))

    def update(self, entity_id: int, data: dict[str, Any]) -> Asignacion:
        model = AsignacionModel.objects.get(id=entity_id)
        for field, value in data.items():
            setattr(model, field, value)
        model.save(update_fields=[*data.keys()])
        return self._to_domain(model)

    def delete(self, entity_id: int) -> None:
        AsignacionModel.objects.filter(id=entity_id).delete()

    def existe_conflicto(
        self,
        aula_id: str,
        bloque_horario_id: str,
        semestre: str,
    ) -> bool:
        return AsignacionModel.objects.filter(
            aula_id=aula_id,
            bloque_horario_id=bloque_horario_id,
            semestre=semestre,
            estado="CONFIRMADO",
        ).exists()

    @transaction.atomic
    def guardar(self, asignacion: Asignacion) -> Asignacion:
        try:
            model = AsignacionModel.objects.create(
                grupo_id=asignacion.grupo_id,
                aula_id=asignacion.aula_id,
                bloque_horario_id=asignacion.bloque_horario_id,
                semestre=asignacion.semestre,
                estado=asignacion.estado,
            )
        except IntegrityError as exc:
            raise AsignacionConflictoError(
                ["El aula ya fue asignada en ese bloque y semestre."]
            ) from exc
        return self._to_domain(model)

    def listar_por_semestre(self, semestre: str) -> Iterable[Asignacion]:
        return self.list(semestre=semestre)

    def contar_grupos_por_semestre(self, semestre: str) -> int:
        grupo_model = apps.get_model("academico", "GrupoModel")
        return grupo_model.objects.filter(semestre=semestre, activo=True).count()

    def contar_grupos_asignados_por_semestre(self, semestre: str) -> int:
        return (
            AsignacionModel.objects.filter(semestre=semestre, estado="CONFIRMADO")
            .values("grupo_id")
            .distinct()
            .count()
        )

    def obtener_grupo(self, grupo_id: str):
        grupo_model = apps.get_model("academico", "GrupoModel")
        return grupo_model.objects.filter(id=grupo_id, activo=True).first()

    def obtener_aula(self, aula_id: str):
        aula_model = apps.get_model("academico", "AulaModel")
        return aula_model.objects.filter(id=aula_id, activa=True).first()

    @staticmethod
    def _to_domain(model: AsignacionModel) -> Asignacion:
        return Asignacion(
            id=model.id,
            grupo_id=model.grupo_id,
            aula_id=model.aula_id,
            bloque_horario_id=model.bloque_horario_id,
            semestre=model.semestre,
            estado=model.estado,
        )
