
"""
Módulo de excepciones personalizadas para el sistema Software FJ.
Permite identificar y controlar errores específicos del programa.
"""


class ErrorSistema(Exception):
    """Excepción base para los errores propios del sistema."""
    pass


class ErrorValidacion(ErrorSistema):
    """Se genera cuando los datos ingresados no son válidos."""
    pass


class ErrorCliente(ErrorSistema):
    """Se genera cuando ocurre un problema con un cliente."""
    pass


class ErrorServicio(ErrorSistema):
    """Se genera cuando un servicio presenta algún inconveniente."""
    pass


class ErrorReserva(ErrorSistema):
    """Se genera cuando una reserva no puede realizarse."""
    pass


class ServicioNoDisponible(ErrorServicio):
    """Se genera cuando un servicio no está disponible."""
    pass


class ReservaNoPermitida(ErrorReserva):
    """Se genera cuando una operación de reserva no está permitida."""
    pass


class ErrorOperacion(ErrorSistema):
    """Se genera cuando una operación no puede completarse."""
    pass
