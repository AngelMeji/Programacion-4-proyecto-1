
"""Presentacion por consola del flujo y resultados del Bingo."""

from typing import Optional, TYPE_CHECKING

from interfaces import IPresentadorResultados

if TYPE_CHECKING:
    from carton import Carton
    from carton_doble import CartonDoble
    from jugador import Jugador


class PresentadorResultados(IPresentadorResultados):
    """Centraliza toda la salida textual del juego."""

    @staticmethod
    def inicio_partida() -> None:
        """Muestra el mensaje de inicio de la partida."""
        print("\n=== INICIO DEL JUEGO DE BINGO ===")

    @staticmethod
    def mostrar_turno(numero: str, turno: int) -> None:
        """Muestra el número extraído y el turno actual."""
        print(f"\n--- Turno {turno} ---")
        print(f"Numero extraido: {numero}")

    @staticmethod
    def jugador_marco(jugador: "Jugador") -> None:
        """Notifica que un jugador marcó el número correctamente."""
        print(f"{jugador.nombre} marco el numero")

    @staticmethod
    def jugador_no_marco(jugador: "Jugador") -> None:
        """Notifica que un jugador no tenía el número extraído."""
        print(f"{jugador.nombre} no tiene el numero")

    @staticmethod
    def mostrar_error(mensaje: str) -> None:
        """Muestra un error controlado sin romper el flujo de la consola."""
        print(f"Error: {mensaje}")

    @staticmethod
    def mostrar_resultado_final(
        ganador: Optional["Jugador"],
        historial: list[str],
        resumen_jugadores: list[tuple[str, int]]
    ) -> None:
        """Muestra el estado final del juego, historial y resumen de jugadores."""
        print("\n=== FIN DEL JUEGO ===")

        if ganador:
            print(f"\nGANADOR: {ganador.nombre}")
        else:
            print("\nNo hubo ganador en esta partida.")

        print("\nHistorial de numeros extraidos:")
        if historial:
            print(", ".join(historial))
        else:
            print("Sin extracciones.")

        print("\nResumen de jugadores:")
        for nombre, marcados in resumen_jugadores:
            print(f"- {nombre}: {marcados} numeros marcados")
        print("-" * 40)

    @staticmethod
    def imprimir_carton(carton: "Carton") -> None:
        """Imprime un cartón normal en formato de consola."""
        PresentadorResultados._imprimir_matriz(
            titulo="Carton",
            palabra=carton.palabra,
            tarjeta=carton.obtener_tarjeta(),
            marcados=carton.obtener_marcados(),
        )

    @staticmethod
    def imprimir_carton_doble(carton_doble: "CartonDoble") -> None:
        """Imprime ambas grillas del cartón doble."""
        print("=== Carton 1 ===")
        PresentadorResultados._imprimir_matriz(
            titulo="Carton 1",
            palabra=carton_doble.carton1.palabra,
            tarjeta=carton_doble.carton1.obtener_tarjeta(),
            marcados=carton_doble.carton1.obtener_marcados(),
        )
        print("\n=== Carton 2 ===")
        PresentadorResultados._imprimir_matriz(
            titulo="Carton 2",
            palabra=carton_doble.carton2.palabra,
            tarjeta=carton_doble.carton2.obtener_tarjeta(),
            marcados=carton_doble.carton2.obtener_marcados(),
        )

    @staticmethod
    def _imprimir_matriz(titulo: str, palabra: str, tarjeta: list[list], marcados: set[tuple[int, int]]) -> None:
        """Dibuja una matriz de cartón con los números marcados resaltados."""
        print("   ".join(palabra))
        print("-" * 15)
        for fila, valores in enumerate(tarjeta):
            linea = []
            for columna, valor in enumerate(valores):
                if (fila, columna) in marcados or valor == "X":
                    linea.append(" X")
                else:
                    linea.append(f"{valor:2}")
            print("  ".join(linea))