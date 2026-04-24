import random


class Bombo:
    """
    Representa el bombo del juego de bingo.

    Responsabilidades:
    - Mantener los números disponibles.
    - Extraer números aleatorios sin repetir.
    - Registrar el historial de números extraídos.

    Relación:
    - Forma parte del Juego (composición).
    """

    def __init__(self, max_num: int):
        self.numeros = list(range(1, max_num + 1))
        random.shuffle(self.numeros)
        self.historial: list[int] = []

    def extraer_numero(self) -> int:
        """Extrae un número aleatorio sin repetir."""
        if not self.numeros:
            raise ValueError("No quedan números en el bombo.")

        numero = self.numeros.pop()
        self.historial.append(numero)
        return numero
    
    def obtener_historial(self) -> list[int]:
        """Devuelve una copia de los números ya extraídos."""
        return self.historial.copy()

    def hay_numeros(self) -> bool:
        """Indica si aún quedan números por extraer."""
        return bool(self.numeros)