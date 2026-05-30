from datetime import timedelta
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.academico.infrastructure.models import AulaModel
from apps.reservas.infrastructure.models import ReservaModel
from apps.reservas.infrastructure.repositories import ReservaRepository
from apps.reservas.infrastructure.tasks import expiracion_automatica_reservas

from ..application.dtos import (
    CancelarReservaInputDTO,
    ConfirmarReservaInputDTO,
    CrearReservaInputDTO,
)
from ..application.use_cases import ReservaService
from ..domain.entities import Reserva, ReservaEstado
from ..domain.exceptions import ReservaConflictoError, ReservaNoEncontradaError


class FakeReservaRepository:
    def __init__(self, conflicts: bool = False, reserva: Reserva | None = None) -> None:
        self.conflicts = conflicts
        self.reserva = reserva
        self.created = None
        self.updated = None

    def find_conflicts(self, aula_id, inicio, fin):
        return [self.reserva] if self.conflicts and self.reserva else []

    def crear_reserva(self, reserva):
        self.created = reserva
        return reserva

    def create(self, reserva):
        self.created = reserva
        return reserva

    def get_by_id(self, reserva_id):
        if self.reserva and self.reserva.reserva_id == reserva_id:
            return self.reserva
        return None

    def update_state(self, reserva_id, new_estado):
        self.updated = (reserva_id, new_estado)


def _reserva() -> Reserva:
    now = timezone.now() + timedelta(minutes=5)
    return Reserva.crear(
        reserva_id="r1",
        aula_id="a1",
        inicio=now,
        fin=now + timedelta(hours=1),
        solicitante_id="u1",
    )


class ReservaServiceUnitTests(TestCase):
    def test_crear_reserva_sin_repositorio_devuelve_dto(self):
        service = ReservaService()
        now = timezone.now() + timedelta(minutes=5)

        output = service.crear_reserva(
            CrearReservaInputDTO(
                aula_id="a1",
                inicio=now,
                fin=now + timedelta(hours=1),
                solicitante_id="u1",
            )
        )

        assert output.aula_id == "a1"
        assert output.estado == ReservaEstado.PENDIENTE

    def test_crear_reserva_rechaza_fecha_final_invalida(self):
        now = timezone.now() + timedelta(minutes=5)

        with self.assertRaises(ReservaConflictoError) as ctx:
            ReservaService().crear_reserva(
                CrearReservaInputDTO(
                    aula_id="a1",
                    inicio=now,
                    fin=now,
                    solicitante_id="u1",
                )
            )

        assert "fecha final" in str(ctx.exception)

    def test_crear_reserva_rechaza_fecha_de_inicio_pasada(self):
        now = timezone.now()

        with self.assertRaises(ReservaConflictoError) as ctx:
            ReservaService().crear_reserva(
                CrearReservaInputDTO(
                    aula_id="a1",
                    inicio=now - timedelta(minutes=10),
                    fin=now + timedelta(minutes=10),
                    solicitante_id="u1",
                )
            )

        assert "pasado" in str(ctx.exception)

    def test_crear_reserva_rechaza_conflictos_del_repo(self):
        reserva = _reserva()

        with self.assertRaises(ReservaConflictoError) as ctx:
            ReservaService(
                FakeReservaRepository(conflicts=True, reserva=reserva)
            ).crear_reserva(
                CrearReservaInputDTO(
                    aula_id="a1",
                    inicio=reserva.bloque_horario_inicio,
                    fin=reserva.bloque_horario_fin,
                    solicitante_id="u1",
                )
            )

        assert "ya tiene una reserva" in str(ctx.exception)

    def test_crear_reserva_usa_metodo_transaccional_si_existe(self):
        repo = FakeReservaRepository(reserva=_reserva())
        now = timezone.now() + timedelta(minutes=5)

        output = ReservaService(repo).crear_reserva(
            CrearReservaInputDTO(
                aula_id="a1",
                inicio=now,
                fin=now + timedelta(hours=1),
                solicitante_id="u1",
            )
        )

        assert repo.created is not None
        assert output.estado == ReservaEstado.PENDIENTE

    def test_confirmar_y_cancelar_reserva_actualizan_estado(self):
        repo = FakeReservaRepository(reserva=_reserva())
        service = ReservaService(repo)

        confirmada = service.confirmar_reserva(ConfirmarReservaInputDTO("r1"))
        service.cancelar_reserva(CancelarReservaInputDTO("r1"))

        assert confirmada.estado == ReservaEstado.CONFIRMADA
        assert repo.updated == ("r1", ReservaEstado.CANCELADA)

    def test_confirmar_reserva_sin_repo_o_inexistente_lanza_error(self):
        with self.assertRaises(ReservaNoEncontradaError) as ctx_repo:
            ReservaService().confirmar_reserva(ConfirmarReservaInputDTO("r1"))
        assert "Repositorio" in str(ctx_repo.exception)

        with self.assertRaises(ReservaNoEncontradaError) as ctx_missing:
            ReservaService(FakeReservaRepository()).confirmar_reserva(
                ConfirmarReservaInputDTO("r1")
            )
        assert "no encontrada" in str(ctx_missing.exception)


class ReservaIntegrationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="solicitante_reserva",
            password="Test1234!",
        )
        self.aula = AulaModel.objects.create(
            id=uuid4(),
            nombre="Aula 101",
            capacidad=40,
            tipo="aula_regular",
            disponible=True,
        )
        self.repo = ReservaRepository()
        self.service = ReservaService(self.repo)

    def _dto(self, inicio, fin):
        return CrearReservaInputDTO(
            aula_id=str(self.aula.id),
            inicio=inicio,
            fin=fin,
            solicitante_id=str(self.user.pk),
        )

    def test_reserva_sin_conflicto_se_persiste(self):
        inicio = timezone.now() + timedelta(hours=2)
        fin = inicio + timedelta(hours=1)

        output = self.service.crear_reserva(self._dto(inicio, fin))

        assert output.aula_id == str(self.aula.id)
        assert output.estado == ReservaEstado.PENDIENTE
        assert ReservaModel.objects.count() == 1

    def test_reserva_con_conflicto_es_rechazada(self):
        inicio = timezone.now() + timedelta(hours=2)
        fin = inicio + timedelta(hours=1)
        self.service.crear_reserva(self._dto(inicio, fin))

        with self.assertRaises(ReservaConflictoError):
            self.service.crear_reserva(
                self._dto(inicio + timedelta(minutes=30), fin + timedelta(minutes=30))
            )

        assert ReservaModel.objects.count() == 1

    def test_expiracion_automatica_solo_expira_reservas_vencidas(self):
        now = timezone.now()
        ReservaModel.objects.create(
            reserva_id="r-past-pending",
            aula=self.aula,
            inicio=now - timedelta(hours=2),
            fin=now - timedelta(minutes=30),
            solicitante=self.user,
            estado=ReservaEstado.PENDIENTE,
        )
        ReservaModel.objects.create(
            reserva_id="r-past-confirmed",
            aula=self.aula,
            inicio=now - timedelta(hours=3),
            fin=now - timedelta(hours=2),
            solicitante=self.user,
            estado=ReservaEstado.CONFIRMADA,
        )
        ReservaModel.objects.create(
            reserva_id="r-future-pending",
            aula=self.aula,
            inicio=now + timedelta(hours=1),
            fin=now + timedelta(hours=2),
            solicitante=self.user,
            estado=ReservaEstado.PENDIENTE,
        )

        updated = expiracion_automatica_reservas()

        assert updated == 1
        assert (
            ReservaModel.objects.get(reserva_id="r-past-pending").estado
            == ReservaEstado.EXPIRADA
        )
        assert (
            ReservaModel.objects.get(reserva_id="r-past-confirmed").estado
            == ReservaEstado.CONFIRMADA
        )
        assert (
            ReservaModel.objects.get(reserva_id="r-future-pending").estado
            == ReservaEstado.PENDIENTE
        )

    def test_crear_reservas_en_lote_es_atomico(self):
        inicio = timezone.now() + timedelta(hours=4)
        fin = inicio + timedelta(hours=1)

        with self.assertRaises(ReservaConflictoError):
            self.service.crear_reservas_en_lote(
                [
                    self._dto(inicio, fin),
                    self._dto(
                        inicio + timedelta(minutes=15), fin + timedelta(minutes=15)
                    ),
                ]
            )

        assert ReservaModel.objects.count() == 0
