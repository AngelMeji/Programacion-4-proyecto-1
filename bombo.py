"""Bombo de números para la partida de Bingo."""

from __future__ import annotations

import random

from exceptions import BomboConfigError, BomboVacioError
from interfaces import IBombo


class Bombo(IBombo):
    """
    Representa el bombo del juego de bingo.

    Responsabilidades:
    - Mantener los números disponibles.
    - Extraer números aleatorios sin repetir.
    - Registrar el historial de números extraídos.

    Relación:
    - Forma parte del Juego (composición).
    """

    def __init__(self, max_num: int, rng: random.Random | None = None):
        self._validar_configuracion(max_num)
        self.max_num = max_num
        self._rng = rng if rng is not None else random.Random()
        self._numeros = list(range(1, max_num + 1))
        self._rng.shuffle(self._numeros)
        self._historial: list[int] = []

    def extraer_numero(self) -> int:
        """Extrae un número aleatorio sin repetir."""
        if not self._numeros:
            raise BomboVacioError("No quedan números en el bombo.")

        numero = self._numeros.pop()
        self._historial.append(numero)
        return numero
    
    def obtener_historial(self) -> list[int]:
        """Devuelve una copia de los números ya extraídos."""
        return self._historial.copy()

    def hay_numeros(self) -> bool:
        """Indica si aún quedan números por extraer."""
        return bool(self._numeros)

    def formatear_numero(self, numero: int) -> str:
        """Devuelve el número en formato clásico de bingo, por ejemplo B9 o O64."""
        letra = self._obtener_letra(numero)
        return f"{letra}{numero}"

    def _obtener_letra(self, numero: int) -> str:
        """Obtiene la letra correspondiente al rango del número extraído."""
        if not (1 <= numero <= self.max_num):
            raise BomboVacioError(f"El número {numero} está fuera del rango del bombo.")

        intervalo = self.max_num // 5
        indice = min((numero - 1) // intervalo, 4)
        return "BINGO"[indice]

    def _validar_configuracion(self, max_num: int) -> None:
        """Valida el rango del bombo antes de construirlo."""
        if not (50 <= max_num <= 90):
            raise BomboConfigError("El número máximo debe estar entre 50 y 90.")
        if max_num % 5 != 0:
            raise BomboConfigError("El número máximo debe ser múltiplo de 5.")