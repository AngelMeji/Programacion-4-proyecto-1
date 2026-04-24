"""
Clase base del sistema. Representa un cartón de bingo.

Responsabilidades:
- Generar la tarjeta 5x5 con números válidos.
- Permitir marcar números.
- Verificar si se ha completado el bingo.

Relación:
- Es la clase base que será extendida por CartonDoble (herencia).
"""

import random

class Carton:
    """Generador de tarjetas de Bingo"""

    def __init__(self, palabra="BINGO", max_num=75):
        self.palabra = palabra.upper()
        self.tam = len(self.palabra)
        self.max_num = max_num
        self._validar_parametros()
        self.intervalo_columna = self.max_num // self.tam

        # El cartón guarda su propia tarjeta
        self.tarjeta = self.generar_tarjeta()

    def _validar_parametros(self):
        """Valida la palabra y el máximo número del juego."""
        if self.tam != 5:
            raise ValueError("La palabra debe tener exactamente 5 letras.")
        if len(set(self.palabra)) != self.tam:
            raise ValueError("La palabra no debe tener letras repetidas.")
        if not (50 <= self.max_num <= 90):
            raise ValueError("El máximo número debe estar entre 50 y 90.")
        if self.max_num % self.tam != 0:
            raise ValueError("El máximo número debe ser múltiplo de 5.")

    def _rango_columna(self, col):
        """Devuelve el rango [min, max] para una columna."""
        minimo = col * self.intervalo_columna + 1
        maximo = (col + 1) * self.intervalo_columna
        return minimo, maximo

    def generar_tarjeta(self):
        """Genera una tarjeta aleatoria 5x5 sin números repetidos."""
        tarjeta = [[0] * self.tam for _ in range(self.tam)]
        usados = set()

        for col in range(self.tam):
            minimo, maximo = self._rango_columna(col)
            numeros_columna = random.sample(
                [n for n in range(minimo, maximo + 1) if n not in usados],
                self.tam,
            )
            for fila in range(self.tam):
                valor = numeros_columna[fila]
                tarjeta[fila][col] = valor
                usados.add(valor)

        return tarjeta

    def generar_varias_tarjetas(self, cantidad):
        """Genera varias tarjetas."""
        return [self.generar_tarjeta() for _ in range(cantidad)]

    def imprimir(self) -> None:
        """Imprime la tarjeta del cartón."""
        print("   ".join(self.palabra))
        print("-" * (self.tam * 3))
        for fila in self.tarjeta:
            print("  ".join("{:2}".format(n) if n != "X" else " X" for n in fila))

    def marcar_numero(self, numero: int) -> bool:
        """
        Marca un número en la tarjeta si existe.

        Retorna:
        - True si se marcó
        - False si no estaba en el cartón
        """
        for i in range(self.tam):
            for j in range(self.tam):
                if self.tarjeta[i][j] == numero:
                    self.tarjeta[i][j] = "X"
                    return True
        return False
    
    def verificar_bingo(self) -> bool:
        """Verifica si el cartón tiene bingo (fila, columna o diagonal)."""

        # Filas
        for fila in self.tarjeta:
            if all(valor == "X" for valor in fila):
                return True

        # Columnas
        for col in range(self.tam):
            if all(self.tarjeta[fila][col] == "X" for fila in range(self.tam)):
                return True

        # Diagonal principal
        if all(self.tarjeta[i][i] == "X" for i in range(self.tam)):
            return True

        # Diagonal secundaria
        if all(self.tarjeta[i][self.tam - 1 - i] == "X" for i in range(self.tam)):
            return True

        return False