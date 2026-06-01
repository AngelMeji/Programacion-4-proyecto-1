"""Punto de entrada del juego de Bingo."""

from bombo import Bombo
from carton import Carton
from carton_doble import CartonDoble
from exceptions import CartonConfigError, JugadorDuplicadoError
from gestor_jugaadores import GestorJugadores
from interfaces import IValidadorVictoria
from juego import Juego
from jugador import Jugador
from presentador_resultados import PresentadorResultados
from validador_victoria import ValidadorVictoria
from generador_carton import GeneradorCarton
from verificador_bingo import VerificadorBingo


def configurar_validador_por_modo(modo: str) -> IValidadorVictoria:
    """Devuelve un validador que cumple el contrato `IValidadorVictoria`."""
    return ValidadorVictoria(modo)


def pedir_palabra() -> str:
    """Solicita la palabra base del juego y valida su estructura."""
    while True:
        palabra = input("Ingrese la palabra del juego (ej. BINGO o PLENO): ").strip().upper()
        if len(palabra) != 5:
            print("La palabra debe tener 5 letras.\n")
            continue
        if len(set(palabra)) != 5:
            print("Las letras no deben repetirse.\n")
            continue
        return palabra


def pedir_entero(mensaje: str, minimo: int, maximo: int, multiplo: int | None = None) -> int:
    """Solicita un entero dentro de un rango opcionalmente múltiplo de otro valor."""
    while True:
        texto = input(mensaje).strip()
        try:
            numero = int(texto)
        except ValueError:
            print("Debe ingresar un numero entero.\n")
            continue

        if not (minimo <= numero <= maximo):
            print(f"El numero debe estar entre {minimo} y {maximo}.\n")
            continue
        if multiplo is not None and numero % multiplo != 0:
            print(f"El numero debe ser multiplo de {multiplo}.\n")
            continue
        return numero


def pedir_texto(mensaje: str) -> str:
    """Solicita un texto no vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El texto no puede estar vacio.\n")


def pedir_modo() -> str:
    """Permite elegir el modo de verificacion de victoria."""
    opciones = {
        1: ("horizontal", "Filas completas"),
        2: ("vertical", "Columnas completas"),
        3: ("diagonal", "Diagonales"),
        4: ("filas_columnas", "Filas o columnas"),
        5: ("todos", "Todas las formas"),
    }

    print("\nSeleccione la forma de jugar:")
    for clave, (_, descripcion) in opciones.items():
        print(f"  {clave}. {descripcion}")

    while True:
        try:
            seleccion = int(input("Opcion: ").strip())
        except ValueError:
            print("Seleccione una opcion valida (numero).\n")
            continue

        if seleccion in opciones:
            modo, descripcion = opciones[seleccion]
            print(f"Se jugara con la regla: {descripcion}.\n")
            return modo

        print("Seleccione una opcion valida.\n")


def mostrar_jugadores(juego: Juego) -> None:
    """Lista los jugadores activos en pantalla."""
    if not juego.jugadores:
        print("No hay jugadores activos.")
        return

    print("Jugadores registrados:")
    for indice, jugador in enumerate(juego.jugadores, 1):
        print(f"  {indice}. {jugador.nombre}")


def crear_carton(tipo_carton: int, palabra: str, max_num: int, generador: GeneradorCarton, verificador: VerificadorBingo):
    """Crea un cartón normal o doble usando las dependencias compartidas."""
    if tipo_carton == 1:
        return Carton(palabra, max_num, generador, verificador)
    return CartonDoble(palabra, max_num, generador, verificador)


def agregar_jugadores_predeterminados(juego: Juego, palabra: str, max_num: int, generador: GeneradorCarton, verificador: VerificadorBingo) -> None:
    """Agrega jugadores de ejemplo para pruebas rápidas."""
    ejemplos = [("Juan", 2), ("Ana", 2), ("Carlos", 1)]
    for nombre, tipo_carton in ejemplos:
        if juego.buscar_jugador_por_nombre(nombre) is not None:
            continue

        jugador = Jugador(nombre)
        jugador.agregar_carton(crear_carton(tipo_carton, palabra, max_num, generador, verificador))

        try:
            juego.agregar_jugador(jugador)
            print(f"Se registro el jugador de ejemplo: {nombre}")
        except JugadorDuplicadoError as error:
            print(f"No se pudo agregar {nombre}: {error}")


def registrar_jugador_interactivo(juego: Juego, palabra: str, max_num: int, generador: GeneradorCarton, verificador: VerificadorBingo) -> None:
    """Permite registrar un jugador nuevo desde la consola."""
    nombre = pedir_texto("Ingrese el nombre del nuevo jugador: ")
    tipo_carton = pedir_entero("Seleccione el tipo de carton (1 = Normal, 2 = Doble): ", 1, 2)

    jugador = Jugador(nombre)
    jugador.agregar_carton(crear_carton(tipo_carton, palabra, max_num, generador, verificador))

    try:
        juego.agregar_jugador(jugador)
        print(f"Jugador '{nombre}' registrado con exito.\n")
    except JugadorDuplicadoError as error:
        print(f"Ya existe un jugador con ese nombre: {error}\n")


def retirar_jugador_interactivo(juego: Juego) -> None:
    """Retira un jugador por nombre desde el menú."""
    if not juego.jugadores:
        print("No hay jugadores para retirar.\n")
        return

    mostrar_jugadores(juego)
    nombre = pedir_texto("Ingrese el nombre del jugador a retirar: ")
    if juego.retirar_jugador_por_nombre(nombre):
        print(f"Jugador '{nombre}' retirado del juego.\n")
    else:
        print(f"No se encontro un jugador con el nombre '{nombre}'.\n")


def tomar_decision_post_turno(juego: Juego, palabra: str, max_num: int, generador: GeneradorCarton, verificador: VerificadorBingo, turno: int) -> bool:
    """Gestiona las decisiones disponibles después de cada turno."""
    print("\nOpciones disponibles:")
    print("  1. Continuar partida")
    print("  2. Retirar jugador")
    print("  3. Registrar nuevo jugador")
    print("  4. Terminar la partida")
    opcion = pedir_entero("Seleccione una opcion: ", 1, 4)

    if opcion == 2:
        retirar_jugador_interactivo(juego)
        return juego.hay_jugadores()

    if opcion == 3:
        registrar_jugador_interactivo(juego, palabra, max_num, generador, verificador)
        return True

    if opcion == 4:
        print("Partida finalizada por el usuario.\n")
        return False

    return True


def main() -> None:
    """Punto de entrada y composition root del proyecto."""
    print("=== CONFIGURACION DEL JUEGO DE BINGO ===\n")
    palabra = pedir_palabra()
    max_num = pedir_entero("Ingrese el numero maximo (entre 50 y 90, multiplo de 5): ", 50, 90, 5)
    modo = pedir_modo()

    try:
        generador_cartones = GeneradorCarton(palabra, max_num)
    except CartonConfigError as error:
        print(f"Error de configuracion: {error}")
        return

    verificador_cartones = VerificadorBingo()
    presentador = PresentadorResultados()

    juego = Juego(
        bombo=Bombo(max_num),
        gestor=GestorJugadores(),
        validador=configurar_validador_por_modo(modo),
        presentador=presentador,
    )

    print("\n=== REGISTRO DE JUGADORES ===")
    while True:
        print("\n1. Agregar jugador")
        print("2. Retirar jugador")
        print("3. Agregar jugadores de ejemplo")
        print("4. Iniciar partida")
        opcion = pedir_entero("Seleccione una opcion: ", 1, 4)

        if opcion == 1:
            registrar_jugador_interactivo(juego, palabra, max_num, generador_cartones, verificador_cartones)
        elif opcion == 2:
            retirar_jugador_interactivo(juego)
        elif opcion == 3:
            agregar_jugadores_predeterminados(juego, palabra, max_num, generador_cartones, verificador_cartones)
        elif opcion == 4:
            if len(juego.jugadores) < 3:
                print("Debe haber al menos 3 jugadores registrados antes de iniciar la partida.\n")
                continue
            break

    print("\n=== CARTONES INICIALES ===\n")
    for jugador in juego.jugadores:
        print(f"Jugador: {jugador.nombre}")
        for carton in jugador.cartones:
            carton.imprimir()
        print("\n" + "=" * 40)

    juego.jugar(
        lambda turno: tomar_decision_post_turno(
            juego,
            palabra,
            max_num,
            generador_cartones,
            verificador_cartones,
            turno,
        )
    )


if __name__ == "__main__":
    main()