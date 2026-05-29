from dataclasses import dataclass, field


@dataclass(frozen=True)
class Asignacion:
    id: int | None
    grupo_id: str
    aula_id: str
    bloque_horario_id: str
    semestre: str
    estado: str


@dataclass(frozen=True)
class ReglaAsignacion:
    nombre: str
    tipo: str
    parametros: dict
    activa: bool = True


@dataclass(frozen=True)
class ResultadoAsignacion:
    exitoso: bool
    mensaje: str
    aula_sugerida_id: str | None = None
    asignaciones: list[dict] = field(default_factory=list)
    conflicto_detalles: list[str] = field(default_factory=list)
