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

def main():
    print("=== CONFIGURACIÓN DEL JUEGO DE BINGO ===\n")

    palabra = pedir_palabra()
    max_num = pedir_entero(
        "Ingrese el número máximo (entre 50 y 90, múltiplo de 5): ",
        50,
        90,
        5,
    )

    # Crear juego
    juego = Juego(max_num)

    # Crear jugadores (mínimo 3 como pide la rúbrica)
    j1 = Jugador("Juan")
    j2 = Jugador("Ana")
    j3 = Jugador("Carlos")

    # Asignar cartones
    j1.agregar_carton(Carton(palabra, max_num))
    j1.agregar_carton(CartonDoble(palabra, max_num))  # requisito: al menos uno doble

    j2.agregar_carton(Carton(palabra, max_num))
    j2.agregar_carton(Carton(palabra, max_num))

    j3.agregar_carton(Carton(palabra, max_num))

    # Agregar jugadores al juego
    juego.agregar_jugador(j1)
    juego.agregar_jugador(j2)
    juego.agregar_jugador(j3)

    # Mostrar cartones iniciales
    print("\n=== CARTONES INICIALES ===\n")
    for jugador in juego.jugadores:
        print(f"Jugador: {jugador.nombre}")
        for i, carton in enumerate(jugador.cartones, start=1):
            print(f"\nCartón {i}:")
            carton.imprimir()  # POLIMORFISMO
        print("\n" + "=" * 40)

    # Ejecutar el juego
    juego.jugar()


if __name__ == "__main__":
    main()