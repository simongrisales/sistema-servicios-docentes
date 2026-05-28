from ..domain.entities import Asignacion


def test_asignacion_entidad_conserva_estado():
    asignacion = Asignacion(
        id=1,
        grupo_id=10,
        aula_id=20,
        bloque_horario_id=30,
        semestre="2026-1",
        estado="CONFIRMADO",
    )

    assert asignacion.estado == "CONFIRMADO"
