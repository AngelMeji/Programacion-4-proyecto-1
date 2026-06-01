"""Modelo de un jugador del juego de Bingo."""

from interfaces import IMarcableVerificable


class Jugador:
    """Agrupa los cartones y el estado de marcado de un jugador."""

    def __init__(self, nombre: str):
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            raise ValueError("El nombre del jugador no puede estar vacío.")

        self.nombre = nombre_limpio
        self.cartones: list[IMarcableVerificable] = []
        self.numeros_marcados = 0

    def agregar_carton(self, carton: IMarcableVerificable) -> None:
        """Agrega un cartón al jugador."""
        self.cartones.append(carton)

    def eliminar_carton(self, carton: IMarcableVerificable) -> None:
        """Elimina un cartón del jugador si existe."""
        if carton in self.cartones:
            self.cartones.remove(carton)

    def marcar_numero(self, numero: int) -> None:
        """Marca un número en todos los cartones del jugador."""
        marcados = 0
        for carton in self.cartones:
            if carton.marcar_numero(numero):
                marcados += 1
        self.numeros_marcados += marcados

    def verificar_bingo(self, modo: str | None = None) -> bool:
        """Verifica si alguno de sus cartones completo un patrón ganador."""
        return any(carton.verificar_bingo(modo) for carton in self.cartones)