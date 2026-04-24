"""
Clase principal que coordina la partida de bingo.

Responsabilidades:
- Gestionar jugadores.
- Controlar el flujo del juego por turnos.
- Extraer números mediante el bombo.
- Detectar ganador y finalizar la partida.

Relación:
- Usa jugadores (asociación).
- Contiene el bombo (composición).
"""

from bombo import Bombo
from jugador import Jugador


class Juego:
    def __init__(self, max_num: int):
        self.jugadores: list[Jugador] = []
        self.bombo = Bombo(max_num)
        self.ganador: Jugador | None = None

    def agregar_jugador(self, jugador: Jugador) -> None:
        """Agrega un jugador al juego."""
        self.jugadores.append(jugador)

    def eliminar_jugador(self, jugador: Jugador) -> None:
        """Elimina un jugador del juego."""
        if jugador in self.jugadores:
            self.jugadores.remove(jugador)

    def jugar(self) -> None:
        """
        Ejecuta la partida completa hasta que haya un ganador.
        Muestra el estado del juego en cada turno.
        """
        print("=== INICIO DEL JUEGO ===")

        turno = 1

        while self.bombo.hay_numeros() and self.ganador is None:
            numero = self.bombo.extraer_numero()
            print(f"\n--- Turno {turno} ---")
            print(f"Número extraído: {numero}\n")

            for jugador in self.jugadores:
                antes = jugador.numeros_marcados
                jugador.marcar_numero(numero)
                despues = jugador.numeros_marcados

                if despues > antes:
                    print(f"{jugador.nombre} marcó el número")
                else:
                    print(f"{jugador.nombre} no tiene el número")

                # Verificar si ganó
                if jugador.verificar_bingo():
                    self.ganador = jugador
                    break

            turno += 1

        self._mostrar_resultado()

    def _mostrar_resultado(self) -> None:
        """Muestra el resultado final del juego."""
        print("\n=== FIN DEL JUEGO ===")

        if self.ganador:
            print(f"\n🎉 GANADOR: {self.ganador.nombre}")
        else:
            print("\nNo hubo ganador.")

        print("\nHistorial de números extraídos:")
        print(self.bombo.obtener_historial())

        print("\nResumen de jugadores:")
        for jugador in self.jugadores:
            print(f"{jugador.nombre} marcó {jugador.numeros_marcados} números")