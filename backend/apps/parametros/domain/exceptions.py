"""Excepciones del dominio de parámetros del sistema."""


class CatalogoParametroError(Exception):
    """Base de todas las excepciones del dominio de parámetros."""


class CatalogoParametroInvalidoError(CatalogoParametroError):
    """La clave, grupo o valor del parámetro no son válidos."""


class CatalogoParametroNoEncontradoError(CatalogoParametroError):
    """No existe un parámetro con la clave solicitada."""


class CatalogoParametroDuplicadoError(CatalogoParametroError):
    """Ya existe un parámetro con la misma clave."""
