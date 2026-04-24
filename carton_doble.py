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