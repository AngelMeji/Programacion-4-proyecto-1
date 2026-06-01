"""Gestión de la colección de jugadores del juego."""

from typing import Optional

from exceptions import JugadorDuplicadoError
from interfaces import IGestorJugadores
from jugador import Jugador


class GestorJugadores(IGestorJugadores):
    """Administra altas, bajas y consultas de jugadores registrados."""

    def __init__(self):
        self.jugadores: list[Jugador] = []

    def buscar_jugador_por_nombre(self, nombre: str) -> Optional[Jugador]:
        """Busca un jugador por su nombre sin distinguir mayúsculas."""
        nombre_normalizado = nombre.strip().lower()
        for jugador in self.jugadores:
            if jugador.nombre.strip().lower() == nombre_normalizado:
                return jugador
        return None

    def obtener_nombres_jugadores(self) -> list[str]:
        """Devuelve la lista de nombres de los jugadores registrados."""
        return [jugador.nombre for jugador in self.jugadores]

    def agregar_jugador(self, jugador: Jugador) -> None:
        """Agrega un jugador, evitando duplicados por nombre."""
        if self.buscar_jugador_por_nombre(jugador.nombre) is not None:
            raise JugadorDuplicadoError(
                f"Ya existe un jugador registrado con el nombre '{jugador.nombre}'."
            )
        self.jugadores.append(jugador)

    def eliminar_jugador(self, jugador: Jugador) -> None:
        """Elimina un jugador de la lista si existe."""
        if jugador in self.jugadores:
            self.jugadores.remove(jugador)

    def obtener_jugadores(self) -> list[Jugador]:
        """Devuelve una copia de la lista de jugadores."""
        return self.jugadores.copy()

    def hay_jugadores(self) -> bool:
        """Verifica si hay jugadores en el juego."""
        return len(self.jugadores) > 0