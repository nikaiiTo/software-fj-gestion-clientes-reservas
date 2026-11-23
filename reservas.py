
"""
Modulo de reservas del sistema Software FJ.
Gestiona la creacion, confirmacion, cancelacion
y procesamiento de reservas.
"""

from datetime import datetime
from entidades import Entidad, Cliente
from servicios import Servicio
from excepciones import (
    ErrorReserva,
    ErrorValidacion,
    ReservaNoPermitida,
    ServicioNoDisponible
)


class Reserva(Entidad):
    """
    Representa una reserva realizada por un cliente.
    Integra cliente, servicio, duracion, costo y estado.
    """

    def __init__(self, cliente, servicio, duracion, **parametros):
        super().__init__()

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._parametros = parametros
        self._estado = "Pendiente"
        self._fecha_reserva = datetime.now()
        self._costo_total = 0.0

        self.validar()

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    @property
    def fecha_reserva(self):
        return self._fecha_reserva

    def validar(self):
        """Comprueba que los datos de la reserva sean correctos."""

        if not isinstance(self._cliente, Cliente):
            raise ErrorValidacion(
                "La reserva debe estar asociada a un cliente valido."
            )

        if not isinstance(self._servicio, Servicio):
            raise ErrorValidacion(
                "La reserva debe estar asociada a un servicio valido."
            )

        if isinstance(self._duracion, bool) or not isinstance(
            self._duracion, (int, float)
        ):
            raise ErrorValidacion(
                "La duracion debe ser un valor numerico."
            )

        if self._duracion <= 0:
            raise ErrorValidacion(
                "La duracion de la reserva debe ser mayor que cero."
            )

        if not isinstance(self._parametros, dict):
            raise ErrorValidacion(
                "Los parametros de la reserva no son validos."
            )

    def calcular_costo(self):
        """
        Calcula el costo mediante el servicio seleccionado.
        Utiliza polimorfismo para ejecutar el metodo correspondiente.
        """

        return self._servicio.calcular_costo(
            self._duracion,
            **self._parametros
        )

    def confirmar(self):
        """Confirma una reserva que se encuentra pendiente."""

        if self._estado != "Pendiente":
            raise ReservaNoPermitida(
                "Solo se pueden confirmar reservas pendientes."
            )

        if not self._servicio.disponible:
            raise ServicioNoDisponible(
                "No se puede confirmar: el servicio no esta disponible."
            )

        self._costo_total = self.calcular_costo()
        self._estado = "Confirmada"

        return (
            f"Reserva {self.identificador} confirmada correctamente. "
            f"Costo total: ${self._costo_total:,.2f}"
        )

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada."""

        if self._estado not in ("Pendiente", "Confirmada"):
            raise ReservaNoPermitida(
                "La reserva no puede cancelarse en su estado actual."
            )

        self._estado = "Cancelada"

        return (
            f"Reserva {self.identificador} cancelada correctamente."
        )

    def procesar(self):
        """
        Procesa la reserva utilizando manejo de excepciones.
        Encadena los errores para conservar su causa original.
        """

        try:
            resultado = self.confirmar()

        except Exception as error:
            raise ErrorReserva(
                f"No fue posible procesar la reserva "
                f"{self.identificador}."
            ) from error

        else:
            return resultado

        finally:
            # Este bloque se ejecuta tanto si hay error como si no.
            pass

    def __str__(self):
        """Presenta la informacion general de la reserva."""

        return (
            f"Reserva: {self.identificador} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duracion: {self.duracion} horas | "
            f"Estado: {self.estado} | "
            f"Costo: ${self.costo_total:,.2f}"
        )
