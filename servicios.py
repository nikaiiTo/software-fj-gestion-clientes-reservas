
"""
Modulo de servicios del sistema Software FJ.
Implementa una clase abstracta y tres servicios especializados.
Incluye herencia, polimorfismo y calculo de costos.
"""

from abc import abstractmethod
from entidades import Entidad
from excepciones import ErrorValidacion, ErrorServicio, ServicioNoDisponible


class Servicio(Entidad):
    """
    Clase abstracta que representa los servicios ofrecidos
    por la empresa Software FJ.
    """

    def __init__(self, nombre, tarifa_base, disponible=True):
        super().__init__()

        self._nombre = nombre
        self._tarifa_base = tarifa_base
        self._disponible = disponible

        self.validar_parametros()

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        """Permite modificar la disponibilidad del servicio."""

        if not isinstance(estado, bool):
            raise ErrorValidacion("La disponibilidad debe ser verdadera o falsa.")

        self._disponible = estado

    def _validar_costo(self, horas, impuesto, descuento):
        """Valida los parámetros utilizados para calcular costos."""

        if isinstance(horas, bool) or not isinstance(horas, (int, float)):
            raise ErrorValidacion("La duración debe ser numérica.")

        if horas <= 0:
            raise ErrorValidacion("La duración debe ser mayor que cero.")

        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
            raise ErrorValidacion("El impuesto debe ser numérico.")

        if not 0 <= impuesto <= 100:
            raise ErrorValidacion("El impuesto debe estar entre 0 y 100.")

        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
            raise ErrorValidacion("El descuento debe ser numérico.")

        if not 0 <= descuento <= 100:
            raise ErrorValidacion("El descuento debe estar entre 0 y 100.")

    def _calcular_total(self, horas, impuesto=0, descuento=0):
        """Calcula el costo aplicando impuestos y descuentos."""

        self._validar_costo(horas, impuesto, descuento)

        subtotal = self._tarifa_base * horas
        valor_descuento = subtotal * (descuento / 100)
        subtotal_con_descuento = subtotal - valor_descuento

        total = subtotal_con_descuento * (1 + impuesto / 100)

        return round(total, 2)

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el costo particular del servicio."""
        pass

    @abstractmethod
    def describir(self):
        """Proporciona una descripción del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self):
        """Valida los parámetros específicos del servicio."""
        pass

    def __str__(self):
        return self.describir()


class ServicioSala(Servicio):
    """
    Servicio especializado para reservar salas.
    El costo depende de la duración de la reserva.
    """

    def __init__(self, nombre, tarifa_base, capacidad, disponible=True):
        self._capacidad = capacidad

        super().__init__(nombre, tarifa_base, disponible)

    def validar_parametros(self):
        if not isinstance(self._nombre, str) or not self._nombre.strip():
            raise ErrorValidacion("El nombre de la sala es obligatorio.")

        if isinstance(self._tarifa_base, bool) or not isinstance(self._tarifa_base, (int, float)):
            raise ErrorValidacion("La tarifa de la sala debe ser numérica.")

        if self._tarifa_base <= 0:
            raise ErrorValidacion("La tarifa de la sala debe ser positiva.")

        if isinstance(self._capacidad, bool) or not isinstance(self._capacidad, int):
            raise ErrorValidacion("La capacidad debe ser un número entero.")

        if self._capacidad <= 0:
            raise ErrorValidacion("La capacidad debe ser mayor que cero.")

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        if not self.disponible:
            raise ServicioNoDisponible("La sala no está disponible.")

        return self._calcular_total(horas, impuesto, descuento)

    def describir(self):
        return (
            f"Sala: {self.nombre} | "
            f"Capacidad: {self._capacidad} personas | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f}"
        )


class ServicioEquipo(Servicio):
    """
    Servicio de alquiler de equipos tecnológicos.
    Permite calcular el costo según horas y cantidad de equipos.
    """

    def __init__(self, nombre, tarifa_base, cantidad_disponible, disponible=True):
        self._cantidad_disponible = cantidad_disponible

        super().__init__(nombre, tarifa_base, disponible)

    def validar_parametros(self):
        if not isinstance(self._nombre, str) or not self._nombre.strip():
            raise ErrorValidacion("El nombre del equipo es obligatorio.")

        if isinstance(self._tarifa_base, bool) or not isinstance(self._tarifa_base, (int, float)):
            raise ErrorValidacion("La tarifa del equipo debe ser numérica.")

        if self._tarifa_base <= 0:
            raise ErrorValidacion("La tarifa del equipo debe ser positiva.")

        if isinstance(self._cantidad_disponible, bool) or not isinstance(self._cantidad_disponible, int):
            raise ErrorValidacion("La cantidad disponible debe ser entera.")

        if self._cantidad_disponible < 0:
            raise ErrorValidacion("La cantidad disponible no puede ser negativa.")

    def calcular_costo(self, horas, impuesto=0, descuento=0, cantidad=1):
        if not self.disponible:
            raise ServicioNoDisponible("El alquiler de equipos no está disponible.")

        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise ErrorValidacion("La cantidad de equipos debe ser entera.")

        if cantidad <= 0:
            raise ErrorValidacion("Debe alquilar al menos un equipo.")

        if cantidad > self._cantidad_disponible:
            raise ServicioNoDisponible("No hay suficientes equipos disponibles.")

        costo_unitario = self._calcular_total(horas, impuesto, descuento)

        return round(costo_unitario * cantidad, 2)

    def describir(self):
        return (
            f"Equipo: {self.nombre} | "
            f"Unidades disponibles: {self._cantidad_disponible} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f}"
        )


class ServicioAsesoria(Servicio):
    """
    Servicio especializado en asesorías profesionales.
    El costo depende de las horas de atención.
    """

    def __init__(self, nombre, tarifa_base, especialidad, disponible=True):
        self._especialidad = especialidad

        super().__init__(nombre, tarifa_base, disponible)

    def validar_parametros(self):
        if not isinstance(self._nombre, str) or not self._nombre.strip():
            raise ErrorValidacion("El nombre de la asesoría es obligatorio.")

        if isinstance(self._tarifa_base, bool) or not isinstance(self._tarifa_base, (int, float)):
            raise ErrorValidacion("La tarifa de asesoría debe ser numérica.")

        if self._tarifa_base <= 0:
            raise ErrorValidacion("La tarifa de asesoría debe ser positiva.")

        if not isinstance(self._especialidad, str) or not self._especialidad.strip():
            raise ErrorValidacion("La especialidad es obligatoria.")

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        if not self.disponible:
            raise ServicioNoDisponible("La asesoría no está disponible.")

        return self._calcular_total(horas, impuesto, descuento)

    def describir(self):
        return (
            f"Asesoría: {self.nombre} | "
            f"Especialidad: {self._especialidad} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f}"
        )
