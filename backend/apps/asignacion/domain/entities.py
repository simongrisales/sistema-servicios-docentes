from dataclasses import dataclass, field


@dataclass(frozen=True)
class Asignacion:
    id: int
    grupo_id: int
    aula_id: int
    bloque_horario_id: int
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
    aula_sugerida_id: int | None = None
    conflicto_detalles: list[str] = field(default_factory=list)
