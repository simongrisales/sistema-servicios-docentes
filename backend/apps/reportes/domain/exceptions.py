class ReporteConflictoError(Exception):
    """Conflicto al generar datos de reporte."""


class TipoReporteInvalidoError(Exception):
    """Tipo de reporte no permitido."""


class DatosInsufficientError(Exception):
    """Faltan datos para generar el reporte."""
