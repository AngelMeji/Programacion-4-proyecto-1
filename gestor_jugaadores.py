from typing import Optional
from jugador import Jugador

class GestorJugadores:
    """Responsabilidad única: administrar la colección de jugadores."""
    """Clase auxiliar para gestionar jugadores en el juego."""
    def __init__(self):
        self.jugadores: list[Jugador] = []

    def agregar_jugador(self, jugador: Jugador) -> None:
        """Agrega un jugador a la lista."""
        self.jugadores.append(jugador)

    def eliminar_jugador(self, jugador: Jugador) -> None:
        """Elimina un jugador de la lista."""
        if jugador in self.jugadores:
            self.jugadores.remove(jugador)

    def obtener_jugadores(self) -> list[Jugador]:
        """Devuelve la lista de jugadores."""
        return self.jugadores
    
    def hay_jugadores(self) -> bool:
        """Verifica si hay jugadores en el juego."""
        return len(self.jugadores) > 0