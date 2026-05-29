# carton_doble.py - Refactorizado para LSP
from carton import Carton
from generador_carton import GeneradorCarton
from verificador_bingo import VerificadorBingo


class CartonDoble(Carton):
    """
    Cartón con dos tarjetas independientes. Gana si cualquiera completa un patrón.
    
    Cumple LSP: Mantiene la misma interfaz pública que Carton.
    Cualquier función que espere un Carton puede recibir un CartonDoble sin modificaciones.
    """
    
    def __init__(self, palabra: str, max_num: int, 
                 verificador: VerificadorBingo = None):
        # 1. Generar ambas tarjetas
        gen = GeneradorCarton(palabra, max_num)
        t1 = gen.generar()
        t2 = gen.generar()
        
        # 2. Inicializar como Carton normal (hereda validación y atributos base)
        super().__init__(palabra, max_num, t1)
        
        # 3. Configurar segunda tarjeta y estados independientes
        # Guardar explícitamente la primera tarjeta para acceso directo
        self.tarjeta1 = t1

        self.tarjeta2 = t2
        self._marcados1 = self._marcados.copy()  # Centro ya marcado por super()
        self._marcados2: set[tuple[int, int]] = {(2, 2)}
        self._verificador = verificador or VerificadorBingo()
        
        # Compatibilidad LSP: por defecto apunta a la primera tarjeta
        self.tarjeta = self.tarjeta1
    
    def marcar_numero(self, numero: int) -> bool:
        """Marca en ambas tarjetas. Retorna True si se marcó en al menos una."""
        m1 = self._marcar_en_tarjeta(numero, self.tarjeta1, self._marcados1)
        m2 = self._marcar_en_tarjeta(numero, self.tarjeta2, self._marcados2)
        return m1 or m2
    
    def _marcar_en_tarjeta(self, numero: int, tarjeta: list[list], 
                          marcados: set[tuple[int, int]]) -> bool:
        for i in range(5):
            for j in range(5):
                if tarjeta[i][j] == numero and (i, j) not in marcados:
                    marcados.add((i, j))
                    return True
        return False
    
    def esta_marcado(self, fila: int, col: int) -> bool:
        return ((fila, col) in self._marcados1 or self.tarjeta1[fila][col] == "X" or
                (fila, col) in self._marcados2 or self.tarjeta2[fila][col] == "X")
    
    def verificar_bingo(self, modo: str = None) -> bool:
        c1 = Carton(self.palabra, self.max_num, self.tarjeta1)
        c1._marcados = self._marcados1.copy()
        
        c2 = Carton(self.palabra, self.max_num, self.tarjeta2)
        c2._marcados = self._marcados2.copy()
        
        bingo1, _ = self._verificador.tiene_bingo(c1, modo)
        if bingo1: return True
        bingo2, _ = self._verificador.tiene_bingo(c2, modo)
        return bingo2
    
    def grilla_mas_cerca(self) -> str:
        total1 = len(self._marcados1)
        total2 = len(self._marcados2)
        if total1 > total2: return "Cartón 1"
        if total2 > total1: return "Cartón 2"
        return "Ambos están igual de cerca"
    
    def imprimir(self, presentador=None) -> None:
        if presentador and hasattr(presentador, 'imprimir_carton_doble'):
            presentador.imprimir_carton_doble(self)
        else:
            print("=== Cartón 1 ===")
            self._imprimir_basico(self.tarjeta1, self._marcados1)
            print("\n=== Cartón 2 ===")
            self._imprimir_basico(self.tarjeta2, self._marcados2)
    
    def _imprimir_basico(self, tarjeta: list[list], marcados: set) -> None:
        print("   ".join(self.palabra))
        print("-" * 15)
        for i, fila in enumerate(tarjeta):
            linea = [" X" if (i, j) in marcados or valor == "X" else f"{valor:2}" 
                     for j, valor in enumerate(fila)]
            print("  ".join(linea))