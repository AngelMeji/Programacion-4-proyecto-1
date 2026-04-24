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