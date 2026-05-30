from rest_framework import status


class SistemaBaseError(Exception):
    """Excepcion base para errores controlados del sistema."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code


SystemException = SistemaBaseError


class CredencialesInvalidasError(SistemaBaseError):
    def __init__(self, message: str = "Credenciales invalidas.") -> None:
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class PermisoInsuficienteError(SistemaBaseError):
    def __init__(
        self, message: str = "No tienes permisos para realizar esta accion."
    ) -> None:
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class AulaConflictoError(SistemaBaseError):
    def __init__(
        self, message: str = "El aula ya esta asignada en ese horario."
    ) -> None:
        super().__init__(message, status.HTTP_409_CONFLICT)


class CapacidadInsuficienteError(SistemaBaseError):
    def __init__(self, message: str = "La capacidad del aula es insuficiente.") -> None:
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class ReservaConflictoError(SistemaBaseError):
    def __init__(self, message: str = "El aula esta reservada en ese periodo.") -> None:
        super().__init__(message, status.HTTP_409_CONFLICT)
