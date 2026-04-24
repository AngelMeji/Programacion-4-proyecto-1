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