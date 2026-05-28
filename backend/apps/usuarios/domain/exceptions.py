class SistemaError(Exception):
    """Error base del modulo usuarios."""


class CredencialesInvalidasError(SistemaError):
    def __init__(self, message: str = "Credenciales invalidas.") -> None:
        super().__init__(message)


class PermisoInsuficienteError(SistemaError):
    def __init__(self, required_permission: str, user_role: str) -> None:
        message = (
            f"El rol {user_role} no tiene el permiso requerido: "
            f"{required_permission}"
        )
        super().__init__(message)
        self.required_permission = required_permission
        self.user_role = user_role


class TokenInvalidoError(SistemaError):
    def __init__(self, message: str = "Token invalido.") -> None:
        super().__init__(message)
