import random


class Bingo:
    """Generador de tarjetas de Bingo genéricas."""

    def __init__(self, palabra="BINGO", max_num=75):
        self.palabra = palabra.upper()
        self.tam = len(self.palabra)
        self.max_num = max_num
        self._validar_parametros()
        self.intervalo_columna = self.max_num // self.tam

    def _validar_parametros(self):
        """Valida la palabra y el máximo número básicos del juego."""
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
            # Números posibles para esta columna sin repetir en la tarjeta
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
        """Genera 'cantidad' de tarjetas."""
        return [self.generar_tarjeta() for _ in range(cantidad)]

    def imprimir_tarjeta(self, tarjeta):
        """Imprime una tarjeta con la cabecera de la palabra."""
        print("   ".join(self.palabra))
        print("-" * (self.tam * 3))
        for fila in tarjeta:
            print("  ".join("{:2d}".format(n) for n in fila)) # :2d solo para que se alinien las columnas


def pedir_palabra():
    """Pide una palabra de 5 letras sin repetir."""
    while True:
        p = input("Ingrese la palabra del juego (ej. BINGO o PLENO): ").strip().upper()
        if len(p) != 5:
            print("La palabra debe tener 5 letras.\n")
        elif len(set(p)) != 5:
            print("Las letras no deben repetirse.\n")
        else:
            return p


def pedir_entero(mensaje, minimo, maximo, multiplo=None):
    """Pide un entero entre [minimo, maximo], opcionalmente múltiplo de 'multiplo'."""
    while True:
        texto = input(mensaje).strip()
        try:
            n = int(texto)
        except ValueError:
            print("Debe ingresar un número entero.\n")
            continue

        if not (minimo <= n <= maximo):
            print("El número debe estar entre {} y {}.\n".format(minimo, maximo))
            continue

        if multiplo is not None and n % multiplo != 0:
            print("El número debe ser múltiplo de {}.\n".format(multiplo))
            continue

        return n


def main():
    print("=== Generador de tarjetas de Bingo ===\n")

    palabra = pedir_palabra()
    max_num = pedir_entero(
        "Ingrese el número máximo (entre 50 y 90, múltiplo de 5): ",
        minimo=50,
        maximo=90,
        multiplo=5,
    )
    cantidad = pedir_entero(
        "¿Cuántas tarjetas desea generar?: ",
        minimo=1,
        maximo=1000,
    )

    juego = Bingo(palabra=palabra, max_num=max_num)
    tarjetas = juego.generar_varias_tarjetas(cantidad)

    print("\nTarjetas generadas:\n")
    for i, tarjeta in enumerate(tarjetas, start=1):
        print("Tarjeta #{}".format(i))
        juego.imprimir_tarjeta(tarjeta)
        print()


if __name__ == "__main__":
    main()
