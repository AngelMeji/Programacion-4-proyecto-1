from carton import Carton


class CartonDoble(Carton):
    """
    Representa un cartón doble de bingo.

    Contiene dos tarjetas independientes generadas con los mismos parámetros.
    Un jugador gana si completa cualquiera de las dos.

    Relación:
    - Hereda de Carton (herencia).
    """

    def __init__(self, palabra="BINGO", max_num=75):
        super().__init__(palabra, max_num)
        self.tarjeta1 = self.tarjeta  # reutiliza la del padre
        self.tarjeta2 = self.generar_tarjeta()

    def marcar_numero(self, numero: int) -> bool:
        """
        Marca un número en ambas tarjetas.

        Retorna True si se marcó en al menos una.
        """
        
        marcado_total = False

        for tarjeta in (self.tarjeta1, self.tarjeta2):  # tupla de tarjetas
            for i in range(self.tam):
                for j in range(self.tam):
                    if tarjeta[i][j] == numero:
                        tarjeta[i][j] = "X"
                        marcado_total = True

        return marcado_total
    
    def verificar_bingo(self) -> bool:
        """
        Verifica si alguna de las dos tarjetas tiene bingo.
        """

        def tiene_bingo(tablero):
            # Filas
            for fila in tablero:
                if all(valor == "X" for valor in fila):
                    return True

            # Columnas
            for col in range(self.tam):
                if all(tablero[fila][col] == "X" for fila in range(self.tam)):
                    return True

            # Diagonal principal
            if all(tablero[i][i] == "X" for i in range(self.tam)):
                return True

            # Diagonal secundaria
            if all(tablero[i][self.tam - 1 - i] == "X" for i in range(self.tam)):
                return True

            return False

        return tiene_bingo(self.tarjeta1) or tiene_bingo(self.tarjeta2)