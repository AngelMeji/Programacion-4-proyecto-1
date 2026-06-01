
"""Orquestador principal de la partida de Bingo."""

from typing import Callable, Optional

from exceptions import BomboVacioError, ExtraccionBomboError, JuegoError, SinJugadoresError
from interfaces import IBombo, IGestorJugadores, IPresentadorResultados, IValidadorVictoria
from jugador import Jugador


class Juego:
    """Coordina bombo, jugadores, validación y presentación del flujo."""

    def __init__(
        self,
        bombo: IBombo,
        gestor: IGestorJugadores,
        validador: IValidadorVictoria,
        presentador: IPresentadorResultados,
    ) -> None:
        self._bombo = bombo
        self._gestor = gestor
        self._validador = validador
        self._presentador = presentador
        self._ganador: Optional[Jugador] = None

    @property
    def jugadores(self) -> list[Jugador]:
        """Retorna la lista actual de jugadores registrados."""
        return self._gestor.obtener_jugadores()

    def agregar_jugador(self, jugador: Jugador) -> None:
        """Delega el alta de jugadores en el gestor especializado."""
        self._gestor.agregar_jugador(jugador)

    def eliminar_jugador(self, jugador: Jugador) -> None:
        """Delega la eliminación de jugadores en el gestor especializado."""
        self._gestor.eliminar_jugador(jugador)

    def buscar_jugador_por_nombre(self, nombre: str) -> Optional[Jugador]:
        """Busca un jugador activo por su nombre."""
        return self._gestor.buscar_jugador_por_nombre(nombre)

    def hay_jugadores(self) -> bool:
        """Indica si aún hay jugadores activos."""
        return self._gestor.hay_jugadores()

    def retirar_jugador_por_nombre(self, nombre: str) -> bool:
        """Retira un jugador por nombre y retorna si la operación fue exitosa."""
        jugador = self.buscar_jugador_por_nombre(nombre)
        if jugador is None:
            return False

        self._gestor.eliminar_jugador(jugador)
        return True

    def jugar(self, continuar: Optional[Callable[[int], bool]] = None) -> None:
        """Ejecuta la partida completa hasta ganar, agotar el bombo o detenerla."""
        try:
            if not self._gestor.hay_jugadores():
                raise SinJugadoresError("No se puede iniciar la partida sin jugadores registrados.")

            self._presentador.inicio_partida()
            turno = 1

            while self._bombo.hay_numeros() and self._ganador is None and self._gestor.hay_jugadores():
                try:
                    numero = self._bombo.extraer_numero()
                except BomboVacioError as error:
                    self._presentador.mostrar_error(str(error))
                    break
                except Exception as error:
                    raise ExtraccionBomboError(f"Error inesperado al extraer un numero: {error}") from error

                numero_formateado = self._bombo.formatear_numero(numero)
                self._presentador.mostrar_turno(numero_formateado, turno)

                for jugador in list(self._gestor.obtener_jugadores()):
                    marcados_antes = jugador.numeros_marcados

                    try:
                        jugador.marcar_numero(numero)
                    except Exception as error:
                        self._presentador.mostrar_error(
                            f"No se pudo marcar el numero en {jugador.nombre}: {error}"
                        )
                        continue

                    if jugador.numeros_marcados > marcados_antes:
                        self._presentador.jugador_marco(jugador)
                    else:
                        self._presentador.jugador_no_marco(jugador)

                    try:
                        posible_ganador = self._validador.verificar_ganador([jugador])
                    except Exception as error:
                        self._presentador.mostrar_error(
                            f"No se pudo verificar a {jugador.nombre}: {error}"
                        )
                        continue

                    if posible_ganador is not None:
                        self._ganador = posible_ganador
                        break

                if self._ganador is not None:
                    break

                if not self._gestor.hay_jugadores():
                    self._presentador.mostrar_error("No quedan jugadores activos. La partida termino.")
                    break

                if continuar is not None:
                    try:
                        if not continuar(turno):
                            break
                    except Exception as error:
                        self._presentador.mostrar_error(f"El callback de continuidad fallo: {error}")
                        break

                turno += 1

        except JuegoError as error:
            self._presentador.mostrar_error(str(error))
        finally:
            self._presentador.mostrar_resultado_final(
                ganador=self._ganador,
                historial=[self._bombo.formatear_numero(numero) for numero in self._bombo.obtener_historial()],
                resumen_jugadores=[
                    (jugador.nombre, jugador.numeros_marcados)
                    for jugador in self._gestor.obtener_jugadores()
                ],
            )