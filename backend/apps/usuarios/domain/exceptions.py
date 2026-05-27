class SistemaError(Exception):
    """Excepción base para todos los errores del sistema."""
    pass


class CredencialesInvalidasError(SistemaError):
    """Lanzado cuando el usuario o la contraseña proporcionados no son válidos."""
    def __init__(self, message="Credenciales inválidas. Intente nuevamente."):
        super().__init__(message)

class PermisoInsuficienteError(SistemaError):
    """Lanzado cuando un usuario intenta realizar una acción sin los permisos necesarios."""
    def __init__(self, required_permission: str, user_role: str, message="Permiso insuficiente para esta acción."):
        super().__init__(f"Usuario con rol '{user_role}' no tiene el permiso requerido: {required_permission}")
        self.required_permission = required_permission
        self.user_role = user_role

class TokenInvalidoError(SistemaError):
    """Lanzado cuando un token JWT está expirado, mal formado o revocado."""
    def __init__(self, message="El token de acceso ha expirado o es inválido."):
        super().__init__(message)