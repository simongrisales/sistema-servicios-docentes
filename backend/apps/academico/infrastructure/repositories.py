from collections.abc import Iterable
from typing import Any
from uuid import UUID

from core.repositories import BaseRepository

from ..domain.entities import Aula, Docente, Grupo, TipoAula
from ..domain.interfaces import IAulaRepository, IDocenteRepository, IGrupoRepository
from .models import AulaModel, DocenteModel, GrupoModel


class AulaRepository(BaseRepository[Aula, UUID], IAulaRepository):
    def get(self, entity_id: UUID) -> Aula | None:
        model = AulaModel.objects.filter(id=entity_id).first()
        return self._to_domain(model) if model else None

    def list(self, **filters: Any) -> Iterable[Aula]:
        return [self._to_domain(model) for model in AulaModel.objects.filter(**filters)]

    def create(self, data: dict[str, Any]) -> Aula:
        return self._to_domain(AulaModel.objects.create(**data))

    def update(self, entity_id: UUID, data: dict[str, Any]) -> Aula:
        model = AulaModel.objects.get(id=entity_id)
        for field, value in data.items():
            setattr(model, field, value)
        model.save(update_fields=[*data.keys()])
        return self._to_domain(model)

    def delete(self, entity_id: UUID) -> None:
        AulaModel.objects.filter(id=entity_id).update(activa=False)

    def list_disponibles(self) -> Iterable[Aula]:
        return self.list(disponible=True, activa=True)

    def list_con_capacidad_minima(self, capacidad_minima: int) -> Iterable[Aula]:
        return self.list(capacidad__gte=capacidad_minima, activa=True)

    @staticmethod
    def _to_domain(model: AulaModel) -> Aula:
        return Aula(
            id=model.id,
            nombre=model.nombre,
            capacidad=model.capacidad,
            tipo=TipoAula(model.tipo),
            disponible=model.disponible,
            activa=model.activa,
        )


class DocenteRepository(BaseRepository[Docente, UUID], IDocenteRepository):
    def get(self, entity_id: UUID) -> Docente | None:
        model = DocenteModel.objects.filter(id=entity_id, activo=True).first()
        return self._to_domain(model) if model else None

    def list(self, **filters: Any) -> Iterable[Docente]:
        return [
            self._to_domain(model) for model in DocenteModel.objects.filter(**filters)
        ]

    def create(self, data: dict[str, Any]) -> Docente:
        return self._to_domain(DocenteModel.objects.create(**data))

    def update(self, entity_id: UUID, data: dict[str, Any]) -> Docente:
        model = DocenteModel.objects.get(id=entity_id)
        for field, value in data.items():
            setattr(model, field, value)
        model.save(update_fields=[*data.keys()])
        return self._to_domain(model)

    def delete(self, entity_id: UUID) -> None:
        DocenteModel.objects.filter(id=entity_id).update(activo=False)

    def get_por_email(self, email: str) -> Docente | None:
        model = DocenteModel.objects.filter(email=email, activo=True).first()
        return self._to_domain(model) if model else None

    @staticmethod
    def _to_domain(model: DocenteModel) -> Docente:
        return Docente(
            id=model.id,
            nombre=model.nombre,
            email=model.email,
            disponibilidad=model.disponibilidad,
            activo=model.activo,
        )


class GrupoRepository(BaseRepository[Grupo, UUID], IGrupoRepository):
    def get(self, entity_id: UUID) -> Grupo | None:
        model = GrupoModel.objects.filter(id=entity_id, activo=True).first()
        return self._to_domain(model) if model else None

    def list(self, **filters: Any) -> Iterable[Grupo]:
        return [
            self._to_domain(model) for model in GrupoModel.objects.filter(**filters)
        ]

    def create(self, data: dict[str, Any]) -> Grupo:
        return self._to_domain(GrupoModel.objects.create(**data))

    def update(self, entity_id: UUID, data: dict[str, Any]) -> Grupo:
        model = GrupoModel.objects.get(id=entity_id)
        for field, value in data.items():
            setattr(model, field, value)
        model.save(update_fields=[*data.keys()])
        return self._to_domain(model)

    def delete(self, entity_id: UUID) -> None:
        GrupoModel.objects.filter(id=entity_id).update(activo=False)

    def list_por_semestre(self, semestre: str) -> Iterable[Grupo]:
        return self.list(semestre=semestre, activo=True)

    def list_por_curso(self, curso_id: UUID) -> Iterable[Grupo]:
        return self.list(curso_id=curso_id, activo=True)

    @staticmethod
    def _to_domain(model: GrupoModel) -> Grupo:
        return Grupo(
            id=model.id,
            curso_id=model.curso_id,
            docente_id=model.docente_id,
            codigo=model.codigo,
            num_estudiantes=model.num_estudiantes,
            semestre=model.semestre,
            activo=model.activo,
        )
