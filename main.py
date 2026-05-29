"""
Script principal para ejecutar el juego de bingo.
Responsabilidad única: Composition Root + Orquestación de CLI.
Principios aplicados: DIP (inyección en Juego), OCP (mapeo de modos a estrategias), SRP.
"""

# === IMPORTS ACTUALIZADOS ===
from gestor_jugaadores import GestorJugadores
from presentador_resultados import PresentadorResultados
from bombo import Bombo
from juego import Juego
from jugador import Jugador
from carton import Carton
from carton_doble import CartonDoble
from interfaces import IValidadorVictoria
from validador_victoria import ValidadorVictoria


def configurar_validador_por_modo(modo: str) -> IValidadorVictoria:
    """Devuelve un validador que cumple el contrato `IValidadorVictoria`."""
    return ValidadorVictoria(modo)


# === TUS FUNCIONES CLI (INTACTAS) ===
def pedir_palabra() -> str:
    while True:
        p = input("Ingrese la palabra del juego (ej. BINGO o PLENO): ").strip().upper()
        if len(p) != 5:
            print("La palabra debe tener 5 letras.\n")
        elif len(set(p)) != 5:
            print("Las letras no deben repetirse.\n")
        else:
            return p
        
def pedir_entero(mensaje: str, minimo: int, maximo: int, multiplo: int = None) -> int:
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
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El texto no puede estar vacío.\n")

def pedir_modo() -> str | None:
    opciones = {
        1: ("horizontal", "Filas completas"),
        2: ("vertical", "Columnas completas"),
        3: ("diagonal", "Diagonales"),
        4: ("filas_columnas", "Filas o Columnas"),
        5: ("todos", "Todas las formas (por defecto)")
    }
    print("\nSeleccione la forma de jugar:")
    for k, v in opciones.items():
        print(f"  {k}. {v[1]}")
    while True:
        try:
            sel = int(input("Opción: ").strip())
        except ValueError:
            print("Seleccione una opción válida (número).\n")
            continue
        if sel in opciones:
            modo = opciones[sel][0]
            if modo is None:
                print("Se usará el modo por defecto: todas las formas.\n")
            else:
                print(f"Se jugará con la regla: {opciones[sel][1]}.\n")
            return modo
        else:
            print("Seleccione una opción válida.\n")

def mostrar_jugadores(juego: Juego) -> None:
    if not juego.jugadores:
        print("No hay jugadores activos.")
        return
    print("Jugadores registrados:")
    for indice, jugador in enumerate(juego.jugadores, 1):
        print(f"  {indice}. {jugador.nombre}")

def agregar_jugadores_predeterminados(juego: Juego, palabra: str, max_num: int) -> None:
    ejemplos = [("Juan", CartonDoble), ("Ana", CartonDoble), ("Carlos", Carton)]
    for nombre, clase_carton in ejemplos:
        if juego.buscar_jugador_por_nombre(nombre) is None:
            jugador = Jugador(nombre)
            jugador.agregar_carton(clase_carton(palabra, max_num))
            juego.agregar_jugador(jugador)
            print(f"Se registró el jugador de ejemplo: {nombre}")

def registrar_jugador_interactivo(juego: Juego, palabra: str, max_num: int) -> None:
    nombre = pedir_texto("Ingrese el nombre del nuevo jugador: ")
    if juego.buscar_jugador_por_nombre(nombre) is not None:
        print(f"Ya existe un jugador con el nombre '{nombre}'.\n")
        return
    tipo_carton = pedir_entero("Seleccione el tipo de cartón (1 = Normal, 2 = Doble): ", 1, 2)
    jugador = Jugador(nombre)
    if tipo_carton == 1:
        jugador.agregar_carton(Carton(palabra, max_num))
    else:
        jugador.agregar_carton(CartonDoble(palabra, max_num))
    juego.agregar_jugador(jugador)
    print(f"Jugador '{nombre}' registrado con éxito.\n")

def retirar_jugador_interactivo(juego: Juego) -> None:
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


# === ENTRY POINT ACTUALIZADO (DIP + COMPOSITION ROOT) ===
def main():
    print("=== CONFIGURACIÓN DEL JUEGO DE BINGO ===\n")
    palabra = pedir_palabra()
    max_num = pedir_entero("Ingrese el número máximo (entre 50 y 90, múltiplo de 5): ", 50, 90, 5)
    modo = pedir_modo()

    # 🔹 DIP: main.py es el Composition Root. Decide QUÉ implementaciones usar.
    juego = Juego(
        bombo=Bombo(max_num),
        gestor=GestorJugadores(),
        validador=configurar_validador_por_modo(modo),  # ← OCP: mapeo extensible
        presentador=PresentadorResultados()
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
            carton.imprimir()
        print("\n" + "=" * 40)

    juego.jugar(lambda turno: tomar_decision_post_turno(juego, palabra, max_num, turno))


if __name__ == "__main__":
    main()