
"""
Programa principal del sistema Software FJ.
Integra clientes, servicios, reservas y manejo avanzado
de excepciones mediante una arquitectura orientada a objetos.
"""

import logging

from entidades import Cliente
from servicios import (
    ServicioSala,
    ServicioEquipo,
    ServicioAsesoria
)
from reservas import Reserva
from excepciones import (
    ErrorValidacion,
    ErrorReserva,
    ServicioNoDisponible
)


# --------------------------------------------------
# CONFIGURACION DEL SISTEMA DE REGISTRO
# --------------------------------------------------

logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
    force=True
)


def registrar_evento(mensaje):
    """Registra un evento importante del sistema."""
    logging.info(mensaje)


def registrar_error(mensaje):
    """Registra los errores detectados durante la ejecucion."""
    logging.error(mensaje)


# --------------------------------------------------
# FUNCION GENERAL PARA EJECUTAR OPERACIONES
# --------------------------------------------------

def ejecutar_operacion(nombre, operacion):
    """
    Ejecuta una operacion controlando sus posibles errores.
    Utiliza try, except, else y finally.
    """

    print(f"\n--- {nombre} ---")

    try:
        resultado = operacion()

    except Exception as error:
        print(f"ERROR CONTROLADO: {error}")
        registrar_error(f"{nombre}: {error}")

    else:
        print(resultado)
        registrar_evento(f"{nombre}: operacion exitosa")

    finally:
        print(f"Operacion finalizada: {nombre}")


# --------------------------------------------------
# FUNCIONES DE REGISTRO
# --------------------------------------------------

def crear_cliente(nombre, correo, telefono):
    """Crea y registra un cliente valido."""

    cliente = Cliente(nombre, correo, telefono)
    clientes.append(cliente)

    return cliente


def crear_servicio_sala(nombre, tarifa, capacidad):
    """Registra un servicio de reserva de salas."""

    servicio = ServicioSala(nombre, tarifa, capacidad)
    servicios.append(servicio)

    return servicio


def crear_servicio_equipo(nombre, tarifa, cantidad):
    """Registra un servicio de alquiler de equipos."""

    servicio = ServicioEquipo(nombre, tarifa, cantidad)
    servicios.append(servicio)

    return servicio


def crear_servicio_asesoria(nombre, tarifa, especialidad):
    """Registra un servicio de asesoria especializada."""

    servicio = ServicioAsesoria(nombre, tarifa, especialidad)
    servicios.append(servicio)

    return servicio


# --------------------------------------------------
# LISTAS INTERNAS DEL SISTEMA
# --------------------------------------------------

clientes = []
servicios = []
reservas = []


# --------------------------------------------------
# OPERACION 1: REGISTRO DE CLIENTE VALIDO
# --------------------------------------------------

def operacion_1():
    cliente = crear_cliente(
        "Carlos Ramirez",
        "carlos@gmail.com",
        "3001234567"
    )

    return f"Cliente registrado: {cliente}"


# --------------------------------------------------
# OPERACION 2: REGISTRO DE CLIENTE INVALIDO
# --------------------------------------------------

def operacion_2():
    return crear_cliente(
        "Ana Lopez",
        "correo_incorrecto",
        "3009876543"
    )


# --------------------------------------------------
# OPERACION 3: CREACION DE SALA
# --------------------------------------------------

def operacion_3():
    sala = crear_servicio_sala(
        "Sala de conferencias",
        120000,
        20
    )

    return sala.describir()


# --------------------------------------------------
# OPERACION 4: CREACION DE EQUIPOS
# --------------------------------------------------

def operacion_4():
    equipo = crear_servicio_equipo(
        "Computador portatil",
        25000,
        10
    )

    return equipo.describir()


# --------------------------------------------------
# OPERACION 5: CREACION DE ASESORIA
# --------------------------------------------------

def operacion_5():
    asesoria = crear_servicio_asesoria(
        "Asesoria tecnologica",
        80000,
        "Ingenieria de sistemas"
    )

    return asesoria.describir()


# --------------------------------------------------
# OPERACION 6: CREACION DE SERVICIO INVALIDO
# --------------------------------------------------

def operacion_6():
    return crear_servicio_sala(
        "Sala invalida",
        -50000,
        0
    )


# --------------------------------------------------
# OPERACION 7: RESERVA EXITOSA DE SALA
# --------------------------------------------------

def operacion_7():
    reserva = Reserva(
        clientes[0],
        servicios[0],
        2,
        impuesto=19,
        descuento=10
    )

    reservas.append(reserva)

    resultado = reserva.procesar()

    return f"{resultado}\n{reserva}"


# --------------------------------------------------
# OPERACION 8: SERVICIO NO DISPONIBLE
# --------------------------------------------------

def operacion_8():
    servicios[0].cambiar_disponibilidad(False)

    try:
        reserva = Reserva(
            clientes[0],
            servicios[0],
            1
        )

        return reserva.procesar()

    finally:
        # Se restablece la disponibilidad de la sala.
        servicios[0].cambiar_disponibilidad(True)


# --------------------------------------------------
# OPERACION 9: ALQUILER DE VARIOS EQUIPOS
# --------------------------------------------------

def operacion_9():
    reserva = Reserva(
        clientes[0],
        servicios[1],
        3,
        cantidad=2,
        impuesto=19
    )

    reservas.append(reserva)

    resultado = reserva.procesar()

    return f"{resultado}\n{reserva}"


# --------------------------------------------------
# OPERACION 10: RESERVA CON DURACION INVALIDA
# --------------------------------------------------

def operacion_10():
    reserva = Reserva(
        clientes[0],
        servicios[2],
        -2
    )

    reservas.append(reserva)

    return reserva.procesar()


# --------------------------------------------------
# OPERACION 11: CANCELACION DE RESERVA
# --------------------------------------------------

def operacion_11():
    resultado = reservas[0].cancelar()

    return resultado


# --------------------------------------------------
# OPERACION 12: CANCELACION NO PERMITIDA
# --------------------------------------------------

def operacion_12():
    return reservas[0].cancelar()


# --------------------------------------------------
# OPERACION 13: CALCULO DE COSTO CON DESCUENTO
# --------------------------------------------------

def operacion_13():
    costo = servicios[2].calcular_costo(
        2,
        impuesto=19,
        descuento=15
    )

    return f"Costo de la asesoria: ${costo:,.2f}"


# --------------------------------------------------
# OPERACION 14: VALIDACION DE CANTIDAD DE EQUIPOS
# --------------------------------------------------

def operacion_14():
    costo = servicios[1].calcular_costo(
        2,
        impuesto=19,
        cantidad=50
    )

    return f"Costo total: ${costo:,.2f}"


# --------------------------------------------------
# EJECUCION PRINCIPAL DEL SISTEMA
# --------------------------------------------------

def iniciar_sistema():
    """Ejecuta las pruebas del sistema de forma secuencial."""

    print("=" * 60)
    print("       SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ")
    print("=" * 60)

    registrar_evento("Inicio de ejecucion del sistema Software FJ")

    operaciones = [
        ("Operacion 1: Registro de cliente valido", operacion_1),
        ("Operacion 2: Registro de cliente invalido", operacion_2),
        ("Operacion 3: Creacion de sala", operacion_3),
        ("Operacion 4: Creacion de equipos", operacion_4),
        ("Operacion 5: Creacion de asesoria", operacion_5),
        ("Operacion 6: Creacion de servicio invalido", operacion_6),
        ("Operacion 7: Reserva exitosa", operacion_7),
        ("Operacion 8: Servicio no disponible", operacion_8),
        ("Operacion 9: Alquiler de equipos", operacion_9),
        ("Operacion 10: Duracion invalida", operacion_10),
        ("Operacion 11: Cancelacion de reserva", operacion_11),
        ("Operacion 12: Cancelacion no permitida", operacion_12),
        ("Operacion 13: Calculo con descuento", operacion_13),
        ("Operacion 14: Cantidad de equipos invalida", operacion_14)
    ]

    for nombre, operacion in operaciones:
        ejecutar_operacion(nombre, operacion)

    print("\n" + "=" * 60)
    print("RESUMEN GENERAL DEL SISTEMA")
    print("=" * 60)

    print(f"Clientes registrados: {len(clientes)}")
    print(f"Servicios registrados: {len(servicios)}")
    print(f"Reservas creadas: {len(reservas)}")

    print("\nLa ejecucion del sistema ha finalizado.")
    print("Los eventos y errores se encuentran registrados en logs.txt.")

    registrar_evento("Finalizacion de ejecucion del sistema Software FJ")


# --------------------------------------------------
# PUNTO DE ENTRADA DEL PROGRAMA
# --------------------------------------------------

if __name__ == "__main__":
    try:
        iniciar_sistema()

    except Exception as error:
        registrar_error(f"Error general del sistema: {error}")
        print(f"Error general controlado: {error}")

    finally:
        print("\nSoftware FJ: proceso de ejecucion terminado.")
