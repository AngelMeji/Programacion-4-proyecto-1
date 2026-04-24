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
