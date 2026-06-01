"""Cartón doble construido por composición de dos cartones simples."""

from interfaces import IGeneradorCarton, IImprimible, IMarcableVerificable, IVerificadorBingo
from carton import Carton


class CartonDoble(IMarcableVerificable, IImprimible):
    """Agrupa dos cartones independientes y gana si cualquiera completa un patrón."""

    def __init__(
        self,
        palabra: str,
        max_num: int,
        generador: IGeneradorCarton,
        verificador: IVerificadorBingo,
    ):
        self.palabra = palabra.strip().upper()
        self.max_num = max_num
        self._generador = generador
        self._verificador = verificador

        self.carton1 = Carton(self.palabra, self.max_num, self._generador, self._verificador)
        self.carton2 = Carton(self.palabra, self.max_num, self._generador, self._verificador)
        self.tarjeta = self.carton1.tarjeta

    def marcar_numero(self, numero: int) -> bool:
        """Marca el número en ambos cartones y retorna si al menos uno cambió."""
        marcado_1 = self.carton1.marcar_numero(numero)
        marcado_2 = self.carton2.marcar_numero(numero)
        return marcado_1 or marcado_2

    def esta_marcado(self, fila: int, col: int) -> bool:
        """Indica si la posición está marcada en alguna de las dos grillas."""
        return self.carton1.esta_marcado(fila, col) or self.carton2.esta_marcado(fila, col)

    def verificar_bingo(self, modo: str | None = None) -> bool:
        """Verifica bingo en cualquiera de las dos grillas."""
        return self.carton1.verificar_bingo(modo) or self.carton2.verificar_bingo(modo)

    def grilla_mas_cerca(self) -> str:
        """Indica cuál grilla tiene más posiciones marcadas."""
        total_1 = len(self.carton1.obtener_marcados())
        total_2 = len(self.carton2.obtener_marcados())
        if total_1 > total_2:
            return "Carton 1"
        if total_2 > total_1:
            return "Carton 2"
        return "Ambos estan igual de cerca"

    def imprimir(self, presentador=None) -> None:
        """Imprime ambas grillas usando un presentador o un formato básico."""
        if presentador and hasattr(presentador, "imprimir_carton_doble"):
            presentador.imprimir_carton_doble(self)
            return

        print("=== Carton 1 ===")
        self._imprimir_basico(self.carton1.palabra, self.carton1.obtener_tarjeta(), self.carton1.obtener_marcados())
        print("\n=== Carton 2 ===")
        self._imprimir_basico(self.carton2.palabra, self.carton2.obtener_tarjeta(), self.carton2.obtener_marcados())

    def _imprimir_basico(self, palabra: str, tarjeta: list[list], marcados: set[tuple[int, int]]) -> None:
        """Dibuja una grilla del cartón doble en consola."""
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