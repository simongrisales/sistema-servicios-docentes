from dataclasses import dataclass, field


@dataclass(frozen=True)
class AsignacionInputDTO:
    grupo_id: str
    aula_id: str
    bloque_horario_id: str
    semestre: str


@dataclass(frozen=True)
class AsignacionOutputDTO:
    grupo_id: str
    aula_id: str
    bloque_horario_id: str
    semestre: str
    estado: str


@dataclass(frozen=True)
class SimulacionInputDTO:
    semestre: str
    grupos: list[dict] = field(default_factory=list)
    aulas: list[dict] = field(default_factory=list)


@dataclass(frozen=True)
class SimulacionOutputDTO:
    exitoso: bool
    mensaje: str
    conflictos: list[str] = field(default_factory=list)
    asignaciones: list[dict] = field(default_factory=list)


@dataclass(frozen=True)
class CoberturaOutputDTO:
    total_grupos: int
    grupos_con_aula: int
