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
                
                # Casilla central libre
        centro = self.tam // 2
        tarjeta[centro][centro] = "X"

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

    def _es_esquinas(self) -> bool:
        """Verifica el patrón de las cuatro esquinas."""
        return (
            self.tarjeta[0][0] == "X"
            and self.tarjeta[0][self.tam - 1] == "X"
            and self.tarjeta[self.tam - 1][0] == "X"
            and self.tarjeta[self.tam - 1][self.tam - 1] == "X"
        )

    def _es_cruz_central(self) -> bool:
        """Verifica el patrón de cruz central (fila y columna del medio)."""
        centro = self.tam // 2
        return (
            all(self.tarjeta[centro][col] == "X" for col in range(self.tam))
            and all(self.tarjeta[fila][centro] == "X" for fila in range(self.tam))
        )

    def _es_borde(self) -> bool:
        """Verifica el patrón de borde (todos los extremos de la tarjeta)."""
        if not all(self.tarjeta[0][col] == "X" for col in range(self.tam)):
            return False
        if not all(self.tarjeta[self.tam - 1][col] == "X" for col in range(self.tam)):
            return False
        if not all(self.tarjeta[fila][0] == "X" for fila in range(self.tam)):
            return False
        if not all(self.tarjeta[fila][self.tam - 1] == "X" for fila in range(self.tam)):
            return False
        return True

    def _es_cuadro_central(self) -> bool:
        """Verifica el patrón del cuadro central 3x3."""
        inicio = 1
        fin = self.tam - 1
        return all(
            self.tarjeta[fila][col] == "X"
            for fila in range(inicio, fin)
            for col in range(inicio, fin)
        )
    
    def verificar_bingo(self, modo: str | None = None) -> bool:
        """Verifica si el cartón tiene bingo.

        Args:
            modo: Opcional. Si se pasa un modo, solo se valida ese tipo
                de patrón. Valores aceptados: 'horizontal', 'vertical',
                'diagonal', 'filas_columnas', 'esquinas', 'cruz', 'borde',
                'central', 'completo'. Si es None o 'todos', se mantiene
                el comportamiento completo original.
        """

        # Normaliza el modo
        if modo is None:
            modo = "todos"
        modo = modo.lower()

        def filas() -> bool:
            for fila in self.tarjeta:
                if all(valor == "X" for valor in fila):
                    return True
            return False

        def columnas() -> bool:
            for col in range(self.tam):
                if all(self.tarjeta[fila][col] == "X" for fila in range(self.tam)):
                    return True
            return False

        def diagonales() -> bool:
            if all(self.tarjeta[i][i] == "X" for i in range(self.tam)):
                return True
            if all(self.tarjeta[i][self.tam - 1 - i] == "X" for i in range(self.tam)):
                return True
            return False

        def completo() -> bool:
            return all(self.tarjeta[i][j] == "X" for i in range(self.tam) for j in range(self.tam))

        # Mapear modos a comprobaciones específicas
        if modo in ("todos", ""):
            # Comportamiento original: evaluar todos los patrones
            if filas():
                return True
            if columnas():
                return True
            if diagonales():
                return True
            if self._es_esquinas():
                return True
            if self._es_cruz_central():
                return True
            if self._es_borde():
                return True
            if self._es_cuadro_central():
                return True
            if completo():
                return True
            return False

        if modo == "horizontal":
            return filas()

        if modo == "vertical":
            return columnas()

        if modo == "diagonal":
            return diagonales()

        if modo == "filas_columnas":
            return filas() or columnas()

        if modo == "esquinas":
            return self._es_esquinas()

        if modo == "cruz":
            return self._es_cruz_central()

        if modo == "borde":
            return self._es_borde()

        if modo == "central":
            return self._es_cuadro_central()

        if modo == "completo":
            return completo()

        # Si se pasa un modo desconocido, no declarar ganador por seguridad
        return False