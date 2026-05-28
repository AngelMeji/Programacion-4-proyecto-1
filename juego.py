
"""
Módulo: juego.py
Responsabilidad única: Orquestar el flujo de la partida de Bingo.
Delega: gestión de jugadores, validación de victoria, extracción de números y presentación de resultados.
Razón para cambiar: Si cambia la secuencia de turnos, las condiciones de parada o la coordinación entre componentes.
"""

from typing import Optional, Callable
from bombo import Bombo
from jugador import Jugador
from gestor_jugaadores import GestorJugadores
from validador_victoria import ValidadorVictoria
from presentador_resultados import PresentadorResultados


# 🔹 Excepciones de dominio para tolerancia a fallos
class JuegoError(Exception):
    """Excepción base para errores lógicos del juego."""
    pass

class SinJugadoresError(JuegoError):
    """Se lanza cuando se intenta iniciar una partida sin jugadores registrados."""
    pass

class BomboError(JuegoError):
    """Se lanza cuando ocurre un fallo al extraer números del bombo."""
    pass


class Juego:
    """
    Orquestador principal de la partida de Bingo.
    Aplica SRP (solo coordina flujo), DIP (dependencias inyectadas) y deja preparado OCP.
    """

    def __init__(
        self,
        bombo: Bombo,
        gestor: GestorJugadores,
        validador: ValidadorVictoria,
        presentador: PresentadorResultados
    ) -> None:
        self._bombo = bombo
        self._gestor = gestor
        self._validador = validador
        self._presentador = presentador
        self._ganador: Optional[Jugador] = None

    @property
    def jugadores(self) -> list[Jugador]:
        """Retorna la lista de jugadores registrados en el juego."""
        return self._gestor.obtener_jugadores()

    def agregar_jugador(self, jugador: Jugador) -> None:
        """Delega la adición de jugadores al gestor especializado."""
        self._gestor.agregar_jugador(jugador)

    def eliminar_jugador(self, jugador: Jugador) -> None:
        """Delega la eliminación de jugadores al gestor especializado."""
        self._gestor.eliminar_jugador(jugador)

    def buscar_jugador_por_nombre(self, nombre: str) -> Optional[Jugador]:
        """Busca un jugador activo por su nombre."""
        return self._gestor.buscar_jugador_por_nombre(nombre)

    def hay_jugadores(self) -> bool:
        """Indica si aún hay jugadores activos en el juego."""
        return self._gestor.hay_jugadores()

    def retirar_jugador_por_nombre(self, nombre: str) -> bool:
        """Retira un jugador por nombre y retorna si la eliminación fue exitosa."""
        jugador = self.buscar_jugador_por_nombre(nombre)
        if jugador:
            self._gestor.eliminar_jugador(jugador)
            return True
        return False

    def jugar(self, continuar: Optional[Callable[[int], bool]] = None) -> None:
        """
        Ejecuta la partida completa hasta que haya un ganador o se agote el bombo.
        Delega responsabilidades a los componentes inyectados (DIP).

        Args:
            continuar: Callback opcional que se ejecuta al final de cada turno. Si retorna False,
                la partida se detiene inmediatamente.
        """
        try:
            # Validación inicial
            if not self._gestor.hay_jugadores():
                raise SinJugadoresError("No se puede iniciar la partida sin jugadores registrados.")

            self._presentador.inicio_partida()
            turno = 1

            while self._bombo.hay_numeros() and self._ganador is None and self._gestor.hay_jugadores():
                try:
                    numero = self._bombo.extraer_numero()
                except Exception as e:
                    # Convierte errores internos del bombo en excepciones de dominio
                    raise BomboError(f"Error al extraer número: {e}") from e

                self._presentador.mostrar_turno(numero, turno)

                for jugador in list(self._gestor.obtener_jugadores()):
                    marcados_antes = jugador.numeros_marcados
                    jugador.marcar_numero(numero)

                    if jugador.numeros_marcados > marcados_antes:
                        self._presentador.jugador_marco(jugador)
                    else:
                        self._presentador.jugador_no_marco(jugador)

                    # Delega la validación al componente especializado (SRP + OCP-ready)
                    posible_ganador = self._validador.verificar_ganador([jugador])
                    if posible_ganador:
                        self._ganador = posible_ganador
                        break

                if self._ganador is not None:
                    break

                if not self._gestor.hay_jugadores():
                    print("\nNo quedan jugadores activos. La partida terminará.")
                    break

                if continuar is not None and not continuar(turno):
                    break

                turno += 1

            # Presenta resultados finales independientemente de cómo terminó la partida
            self._presentador.mostrar_resultado_final(
                ganador=self._ganador,
                historial=self._bombo.obtener_historial(),
                resumen_jugadores=[
                    (j.nombre, j.numeros_marcados)
                    for j in self._gestor.obtener_jugadores()
                ]
            )

        except JuegoError as e:
            # Manejo centralizado de errores del dominio
            print(f"\nError controlado en la partida: {e}")
            self._presentador.mostrar_resultado_final(ganador=None, historial="", resumen_jugadores=[])

        except Exception as e:
            # Fallback seguro para errores inesperados
            print(f"\n Error inesperado: {e}")
            self._presentador.mostrar_resultado_final(ganador=None, historial="", resumen_jugadores=[])