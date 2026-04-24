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