
"""
Módulo: presentador_resultados.py
Responsabilidad única: Formatear y mostrar la información del juego al usuario (capa de presentación).
Razón para cambiar: Si se modifica el formato de salida, se agrega soporte para GUI/Web, 
o se requiere silenciar la salida para pruebas automatizadas.
"""

from typing import Optional
from jugador import Jugador


class PresentadorResultados:
    """
    Gestiona toda la salida por consola del juego de Bingo.
    No contiene lógica de negocio, validación ni gestión de estado.
    """

    @staticmethod
    def inicio_partida() -> None:
        """Muestra el mensaje de inicio de la partida."""
        print("\n === INICIO DEL JUEGO DE BINGO ===")

    @staticmethod
    def mostrar_turno(numero: int, turno: int) -> None:
        """Muestra el número extraído y el turno actual."""
        print(f"\n --- Turno {turno} ---")
        print(f"Número extraído: {numero}")

    @staticmethod
    def jugador_marco(jugador: Jugador) -> None:
        """Notifica que un jugador marcó el número correctamente."""
        print(f"{jugador.nombre} marcó el número")

    @staticmethod
    def jugador_no_marco(jugador: Jugador) -> None:
        """Notifica que un jugador no tenía el número extraído."""
        print(f" {jugador.nombre} no tiene el número")

    @staticmethod
    def mostrar_resultado_final(
        ganador: Optional[Jugador],
        historial: str,
        resumen_jugadores: list[tuple[str, int]]
    ) -> None:
        """Muestra el estado final del juego, historial y resumen de jugadores."""
        print("\n === FIN DEL JUEGO ===")
        
        if ganador:
            print(f"\n ¡GANADOR: {ganador.nombre}!")
        else:
            print("\n No hubo ganador en esta partida.")

        if historial:
            print("\n Historial de números extraídos:")
            print(historial)
        else:
            print("\n Historial: No disponible.")

        print("\n Resumen de jugadores:")
        for nombre, marcados in resumen_jugadores:
            print(f"  • {nombre}: {marcados} números marcados")
        print("-" * 40)