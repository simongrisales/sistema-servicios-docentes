"""Entidades del dominio de parámetros del sistema.

Sin imports de Django — Python puro.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CatalogoParametro:
    """Representa un parámetro de configuración del sistema.

    Attributes:
        clave: Identificador único del parámetro (ej. "max_aulas_por_semestre").
        valor: Valor estructurado del parámetro en formato libre (dict/list/str/int).
        grupo: Agrupación lógica del parámetro (ej. "asignacion", "general").
        descripcion: Descripción legible del propósito del parámetro.
        activo: Indica si el parámetro está vigente.
    """

    clave: str
    valor: Any
    grupo: str = "general"
    descripcion: str = ""
    activo: bool = True

    def __post_init__(self) -> None:
        if not self.clave or not self.clave.strip():
            from .exceptions import CatalogoParametroInvalidoError

            raise CatalogoParametroInvalidoError(
                "La clave del parámetro no puede estar vacía."
            )
        if self.grupo not in GRUPOS_VALIDOS:
            from .exceptions import CatalogoParametroInvalidoError

            raise CatalogoParametroInvalidoError(
                f"Grupo '{self.grupo}' no reconocido. " f"Válidos: {GRUPOS_VALIDOS}"
            )


# Grupos de parámetros permitidos en el sistema
GRUPOS_VALIDOS: frozenset[str] = frozenset(
    {
        "general",
        "asignacion",
        "reservas",
        "reportes",
        "notificaciones",
        "seguridad",
    }
)
