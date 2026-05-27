# reportes/domain/exceptions.py
class ReporteConflictoError(Exception):
    """Excepción lanzada cuando se detectan conflictos en la generación de datos."""
    def __init__(self, mensaje: str, detalles: dict = None):
        super().__init__(mensaje)
        self.detalles = detalles

class TipoReporteInvalidoError(Exception):
    """Excepción lanzada si el tipo de reporte solicitado no existe o es inaccesible."""
    pass

class DatosInsufficientError(Exception):
    """Excepción para indicar que faltan datos críticos para generar un reporte completo."""
    def __init__(self, mensaje: str, campos_faltantes: list = None):
        super().__init__(mensaje)
        self.campos_faltantes = campos_faltantes or []