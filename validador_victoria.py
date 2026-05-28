"""
Responsabilidad única: Determinar si un jugador cumple la condición de victoria.
Razón para cambiar: Si cambia la regla de ganar (ej: cartón lleno, línea, patrón especial).
"""
from typing import Optional
from jugador import Jugador

class ValidadorVictoria:
    """Validador configurable de victoria.

    Se puede inicializar con un `modo` para validar solo ciertos patrones
    (ej: 'horizontal', 'vertical', 'diagonal', etc.). Si `modo` es None,
    se valida con todas las reglas disponibles.
    """

    def __init__(self, modo: str | None = None) -> None:
        self.modo = modo

    def verificar_ganador(self, jugadores: list[Jugador]) -> Optional[Jugador]:
        """Retorna el primer jugador que cumpla la condición de victoria, o None."""
        for jugador in jugadores:
            if jugador.verificar_bingo(self.modo):
                return jugador
        return None