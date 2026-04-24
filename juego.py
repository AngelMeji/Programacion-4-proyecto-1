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
class Juego:
    def _init_(self, max_num: int):
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
        """
        print("=== INICIO DEL JUEGO ===")

        turno = 1

        while self.bombo.hay_numeros() and self.ganador is None:
            numero = self.bombo.extraer_numero()
            print(f"\nTurno {turno} -> Número: {numero}")

            for jugador in self.jugadores:
                jugador.marcar_numero(numero)

                if jugador.verificar_bingo():
                    self.ganador = jugador
                    break

            turno += 1

        self._mostrar_resultado()

    def _mostrar_resultado(self) -> None:
        """Muestra el resultado final del juego."""
        print("\n=== FIN DEL JUEGO ===")

        if self.ganador:
            print(f"🎉 GANADOR: {self.ganador.nombre}")
        else:
            print("No hubo ganador.")

        print("\nHistorial de números:")
        print(self.bombo.obtener_historial())