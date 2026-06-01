"""Modelo de un cartón de Bingo."""

from typing import Optional

from exceptions import CartonConfigError, NumeroInvalidoError
from interfaces import IGeneradorCarton, IImprimible, IMarcableVerificable, IVerificadorBingo


class Carton(IMarcableVerificable, IImprimible):
    """Representa un cartón de Bingo con una sola grilla."""

    def __init__(
        self,
        palabra: str,
        max_num: int,
        generador: IGeneradorCarton,
        verificador: IVerificadorBingo,
        tarjeta: Optional[list[list]] = None,
    ):
        palabra_limpia = palabra.strip().upper()
        self._validar_palabra(palabra_limpia)
        self._validar_max_num(max_num)

        self.palabra = palabra_limpia
        self.tam = len(self.palabra)
        self.max_num = max_num
        self._generador = generador
        self._verificador = verificador
        self.tarjeta = self._normalizar_tarjeta(tarjeta if tarjeta is not None else self._generador.generar())

        self._marcados: set[tuple[int, int]] = set()
        centro = self.tam // 2
        if self.tarjeta[centro][centro] == "X":
            self._marcados.add((centro, centro))

    def marcar_numero(self, numero: int) -> bool:
        """Marca un número en la tarjeta si existe y todavía no fue marcado."""
        if not (1 <= numero <= self.max_num):
            raise NumeroInvalidoError(
                f"El numero {numero} esta fuera del rango [1, {self.max_num}]."
            )

        for fila in range(self.tam):
            for columna in range(self.tam):
                if self.tarjeta[fila][columna] == numero and (fila, columna) not in self._marcados:
                    self._marcados.add((fila, columna))
                    return True
        return False

    def esta_marcado(self, fila: int, col: int) -> bool:
        """Indica si una posicion está marcada o si es la casilla libre."""
        if not (0 <= fila < self.tam and 0 <= col < self.tam):
            return False
        return (fila, col) in self._marcados or self.tarjeta[fila][col] == "X"

    def obtener_tarjeta(self) -> list[list]:
        """Devuelve una copia de la matriz del cartón."""
        return [fila.copy() for fila in self.tarjeta]

    def obtener_marcados(self) -> set[tuple[int, int]]:
        """Devuelve una copia del conjunto de posiciones marcadas."""
        return self._marcados.copy()

    def verificar_bingo(self, modo: str | None = None) -> bool:
        """Verifica si el cartón completo un patrón ganador."""
        tiene_bingo, _ = self._verificador.tiene_bingo(self, modo)
        return tiene_bingo

    def imprimir(self, presentador=None) -> None:
        """Imprime el cartón con un presentador externo o con un formato básico."""
        if presentador and hasattr(presentador, "imprimir_carton"):
            presentador.imprimir_carton(self)
            return

        print("   ".join(self.palabra))
        print("-" * (self.tam * 3))
        for fila, valores in enumerate(self.tarjeta):
            linea = []
            for columna, valor in enumerate(valores):
                if (fila, columna) in self._marcados or valor == "X":
                    linea.append(" X")
                else:
                    linea.append(f"{valor:2}")
            print("  ".join(linea))

    def _validar_palabra(self, palabra: str) -> None:
        """Valida la palabra que identifica las columnas del cartón."""
        if len(palabra) != 5:
            raise CartonConfigError("La palabra debe tener exactamente 5 letras.")
        if len(set(palabra)) != 5:
            raise CartonConfigError("La palabra no debe tener letras repetidas.")

    def _validar_max_num(self, max_num: int) -> None:
        """Valida el rango máximo permitido por el juego."""
        if not (50 <= max_num <= 90):
            raise CartonConfigError("El maximo de numeros debe estar entre 50 y 90.")
        if max_num % 5 != 0:
            raise CartonConfigError("El maximo de numeros debe ser multiplo de 5.")

    def _normalizar_tarjeta(self, tarjeta: list[list]) -> list[list]:
        """Valida la estructura del cartón y devuelve una copia segura."""
        if len(tarjeta) != self.tam or any(len(fila) != self.tam for fila in tarjeta):
            raise CartonConfigError("La tarjeta debe tener una estructura 5x5.")
        return [fila.copy() for fila in tarjeta]