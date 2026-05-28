"""
Script principal para ejecutar el juego de bingo.

Responsabilidades:
- Crear el juego.
- Registrar jugadores.
- Asignar cartones.
- Ejecutar la partida turno a turno.
- Mostrar resultados en consola.

Este archivo se usa para la demostración del sistema.
"""
from gestor_jugaadores import GestorJugadores
from validador_victoria import ValidadorVictoria
from presentador_resultados import PresentadorResultados
from bombo import Bombo
from juego import Juego
from jugador import Jugador
from carton import Carton
from carton_doble import CartonDoble

def pedir_palabra() -> str:
    """Pide una palabra de 5 letras sin repetir."""
    while True:
        p = input("Ingrese la palabra del juego (ej. BINGO o PLENO): ").strip().upper()
        if len(p) != 5:
            print("La palabra debe tener 5 letras.\n")
        elif len(set(p)) != 5:
            print("Las letras no deben repetirse.\n")
        else:
            return p
        
def pedir_entero(mensaje: str, minimo: int, maximo: int, multiplo: int = None) -> int:
    """Pide un entero entre [minimo, maximo], opcionalmente múltiplo."""
    while True:
        texto = input(mensaje).strip()
        try:
            n = int(texto)
        except ValueError:
            print("Debe ingresar un número entero.\n")
            continue

        if not (minimo <= n <= maximo):
            print(f"El número debe estar entre {minimo} y {maximo}.\n")
            continue

        if multiplo is not None and n % multiplo != 0:
            print(f"El número debe ser múltiplo de {multiplo}.\n")
            continue

        return n


def pedir_texto(mensaje: str) -> str:
    """Pide un texto no vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El texto no puede estar vacío.\n")


def mostrar_jugadores(juego: Juego) -> None:
    """Muestra la lista de jugadores activos."""
    if not juego.jugadores:
        print("No hay jugadores activos.")
        return

    print("Jugadores registrados:")
    for indice, jugador in enumerate(juego.jugadores, 1):
        print(f"  {indice}. {jugador.nombre}")


def agregar_jugadores_predeterminados(juego: Juego, palabra: str, max_num: int) -> None:
    """Agrega jugadores de ejemplo si aún no existen."""
    ejemplos = [
        ("Juan", CartonDoble),
        ("Ana", CartonDoble),
        ("Carlos", Carton),
    ]

    for nombre, clase_carton in ejemplos:
        if juego.buscar_jugador_por_nombre(nombre) is None:
            jugador = Jugador(nombre)
            jugador.agregar_carton(clase_carton(palabra, max_num))
            juego.agregar_jugador(jugador)
            print(f"Se registró el jugador de ejemplo: {nombre}")


def registrar_jugador_interactivo(juego: Juego, palabra: str, max_num: int) -> None:
    """Registra un nuevo jugador con cartón normal o doble."""
    nombre = pedir_texto("Ingrese el nombre del nuevo jugador: ")
    if juego.buscar_jugador_por_nombre(nombre) is not None:
        print(f"Ya existe un jugador con el nombre '{nombre}'.\n")
        return

    tipo_carton = pedir_entero(
        "Seleccione el tipo de cartón (1 = Normal, 2 = Doble): ",
        1,
        2,
    )

    jugador = Jugador(nombre)
    if tipo_carton == 1:
        jugador.agregar_carton(Carton(palabra, max_num))
    else:
        jugador.agregar_carton(CartonDoble(palabra, max_num))

    juego.agregar_jugador(jugador)
    print(f"Jugador '{nombre}' registrado con éxito.\n")


def retirar_jugador_interactivo(juego: Juego) -> None:
    """Retira un jugador activo del juego."""
    if not juego.jugadores:
        print("No hay jugadores para retirar.\n")
        return

    mostrar_jugadores(juego)
    nombre = pedir_texto("Ingrese el nombre del jugador a retirar: ")
    if juego.retirar_jugador_por_nombre(nombre):
        print(f"Jugador '{nombre}' retirado del juego.\n")
    else:
        print(f"No se encontró un jugador con el nombre '{nombre}'.\n")


def tomar_decision_post_turno(juego: Juego, palabra: str, max_num: int, turno: int) -> bool:
    """Permite registrar o retirar jugadores al final de cada turno."""
    print("\nOpciones disponibles:")
    print("  1. Continuar partida")
    print("  2. Retirar jugador")
    print("  3. Registrar nuevo jugador")
    print("  4. Terminar la partida")

    opcion = pedir_entero("Seleccione una opción: ", 1, 4)
    if opcion == 2:
        retirar_jugador_interactivo(juego)
        return juego.hay_jugadores()
    if opcion == 3:
        registrar_jugador_interactivo(juego, palabra, max_num)
        return True
    if opcion == 4:
        print("Partida finalizada por el usuario.\n")
        return False
    return True


def main():
    print("=== CONFIGURACIÓN DEL JUEGO DE BINGO ===\n")

    palabra = pedir_palabra()
    max_num = pedir_entero(
        "Ingrese el número máximo (entre 50 y 90, múltiplo de 5): ",
        50,
        90,
        5,
    )

    # Crear juego con todas sus dependencias
    juego = Juego(
        Bombo(max_num),
        GestorJugadores(),
        ValidadorVictoria(),
        PresentadorResultados()
    )

    print("\n=== REGISTRO DE JUGADORES ===")
    while True:
        print("\n1. Agregar jugador")
        print("2. Retirar jugador")
        print("3. Agregar jugadores de ejemplo")
        print("4. Iniciar partida")

        opcion = pedir_entero("Seleccione una opción: ", 1, 4)
        if opcion == 1:
            registrar_jugador_interactivo(juego, palabra, max_num)
        elif opcion == 2:
            retirar_jugador_interactivo(juego)
        elif opcion == 3:
            agregar_jugadores_predeterminados(juego, palabra, max_num)
        elif opcion == 4:
            if len(juego.jugadores) < 3:
                print("Debe haber al menos 3 jugadores registrados antes de iniciar la partida.\n")
                continue
            break

    print("\n=== CARTONES INICIALES ===\n")
    for jugador in juego.jugadores:
        print(f"Jugador: {jugador.nombre}")
        for i, carton in enumerate(jugador.cartones, start=1):
            carton.imprimir()  # POLIMORFISMO
        print("\n" + "=" * 40)

    juego.jugar(lambda turno: tomar_decision_post_turno(juego, palabra, max_num, turno))


if __name__ == "__main__":
    main()