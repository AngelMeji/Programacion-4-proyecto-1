"""
Responsabilidad única: Determinar si un jugador cumple la condición de victoria.
Razón para cambiar: Si cambia la regla de ganar (ej: cartón lleno, línea, patrón especial).
"""
from typing import Optional
from jugador import Jugador

class ValidadorVictoria:
    """Valida si un jugador ha ganado según la regla actual."""
    
    @staticmethod
    def verificar_ganador(jugadores: list[Jugador]) -> Optional[Jugador]:
        """Retorna el primer jugador que cumpla la condición de victoria, o None."""
        for jugador in jugadores:
            if jugador.verificar_bingo():
                return jugador
        return None