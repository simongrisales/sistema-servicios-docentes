class ReservaError(Exception):
    """Error base del modulo de reservas."""


class ReservaConflictoError(ReservaError):
    """La reserva se cruza con otra ocupacion."""


class ReservaExpiradaError(ReservaError):
    """La reserva ya expiro y no puede modificarse."""


class ReservaNoEncontradaError(ReservaError):
    """La reserva solicitada no existe."""
