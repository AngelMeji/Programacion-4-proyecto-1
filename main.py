"""
Script principal para ejecutar el juego.

Responsabilidades:
- Crear el juego.
- Registrar jugadores.
- Asignar cartones.
- Ejecutar la partida turno a turno.
- Mostrar resultados en consola.

Este archivo se usa para la demostración del sistema.
"""

from carton import Carton


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

    juego = Carton(palabra=palabra, max_num=max_num)
    tarjetas = juego.generar_varias_tarjetas(cantidad)

    print("\nTarjetas generadas:\n")
    for i, tarjeta in enumerate(tarjetas, start=1):
        print("Tarjeta #{}".format(i))
        juego.imprimir_tarjeta(tarjeta)
        print()


if __name__ == "__main__":
    main()