# reservas/domain/exceptions.py

class ReservaError(Exception):
    """Base exception for the reservations module."""
    pass

class ReservaConflictoError(ReservaError):
    """Raised when a proposed reservation conflicts with an existing, confirmed assignment or other reservation."""
    def __init__(self, message="Conflict detected with another scheduled event"):
        super().__init__(message)

class ReservaExpiradaError(ReservaError):
    """Raised when attempting to operate on a reservation that has passed its expiration date."""
    def __init__(self, message="The reservation has expired and cannot be modified"):
        super().__init__(message)

class ReservaNoEncontradaError(ReservaError):
    """Raised when the requested reservation ID does not exist."""
    pass