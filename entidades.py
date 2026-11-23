
"""
Modulo de entidades principales del sistema Software FJ.
Contiene la clase abstracta Entidad y la clase Cliente.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re
import uuid


class Entidad(ABC):
    """
    Clase abstracta que representa una entidad general del sistema.
    Proporciona un identificador unico y fecha de creacion.
    """

    def __init__(self, identificador=None):
        self._identificador = identificador or str(uuid.uuid4())[:8]
        self._fecha_creacion = datetime.now()

    @property
    def identificador(self):
        """Retorna el identificador de la entidad."""
        return self._identificador

    @property
    def fecha_creacion(self):
        """Retorna la fecha de creacion."""
        return self._fecha_creacion

    @abstractmethod
    def validar(self):
        """Obliga a las clases derivadas a implementar validaciones."""
        pass


class Cliente(Entidad):
    """
    Representa un cliente de Software FJ.
    Protege sus datos personales mediante atributos privados.
    """

    def __init__(self, nombre, correo, telefono):
        super().__init__()

        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono

        self.validar()

    @property
    def nombre(self):
        """Permite consultar el nombre del cliente."""
        return self.__nombre

    @property
    def correo(self):
        """Permite consultar el correo del cliente."""
        return self.__correo

    @property
    def telefono(self):
        """Permite consultar el telefono del cliente."""
        return self.__telefono

    def validar(self):
        """
        Comprueba que los datos personales del cliente
        cumplan con los requisitos establecidos.
        """

        if not isinstance(self.__nombre, str):
            raise ValueError("El nombre debe ser un texto.")

        if not self.__nombre.strip():
            raise ValueError("El nombre del cliente es obligatorio.")

        if not isinstance(self.__correo, str):
            raise ValueError("El correo debe ser un texto.")

        patron_correo = r"^[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}$"

        if not re.match(patron_correo, self.__correo):
            raise ValueError("El correo electronico no es valido.")

        if not isinstance(self.__telefono, str):
            raise ValueError("El telefono debe ingresarse como texto.")

        telefono_limpio = self.__telefono.replace(" ", "")

        if not telefono_limpio.isdigit():
            raise ValueError("El telefono solo debe contener numeros.")

        if not 7 <= len(telefono_limpio) <= 15:
            raise ValueError("El telefono debe tener entre 7 y 15 digitos.")

    def __str__(self):
        """Retorna una descripcion del cliente."""
        return (
            f"Cliente: {self.__nombre} | "
            f"Correo: {self.__correo} | "
            f"Telefono: {self.__telefono} | "
            f"ID: {self.identificador}"
        )
