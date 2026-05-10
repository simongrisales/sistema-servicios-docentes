class AcademicoDomainError(Exception):
    """Error base para reglas de dominio academico."""


class CampoAcademicoInvalidoError(AcademicoDomainError):
    """Se lanza cuando un campo obligatorio o de formato basico es invalido."""


class CapacidadAulaInvalidaError(AcademicoDomainError):
    """Se lanza cuando la capacidad de un aula no es valida."""


class CreditosCursoInvalidosError(AcademicoDomainError):
    """Se lanza cuando un curso tiene una cantidad invalida de creditos."""


class NumeroEstudiantesInvalidoError(AcademicoDomainError):
    """Se lanza cuando un grupo tiene una cantidad invalida de estudiantes."""


class HorarioBloqueInvalidoError(AcademicoDomainError):
    """Se lanza cuando un bloque horario no respeta el orden de horas."""
