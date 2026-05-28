# carton_doble.py - Refactorizado para LSP
from carton import Carton
from generador_carton import GeneradorCarton
from verificador_bingo import VerificadorBingo


class CartonDoble(Carton):
    """
    Cartón con dos tarjetas independientes. Gana si cualquiera completa un patrón.
    
    Cumple LSP: Puede usarse donde se espere un Carton sin efectos secundarios.
    """
    
    def __init__(self, palabra: str, max_num: int, 
                 verificador: VerificadorBingo = None):
        """
        Inicializa un cartón doble con dos tarjetas generadas independientemente.
        
        Args:
            palabra: Palabra de 5 letras para encabezados.
            max_num: Número máximo del juego.
            verificador: VerificadorBingo inyectado (opcional, usa default si None).
        """
        # No llamamos super().__init__ para evitar generar tarjeta base
        self.palabra = palabra.upper()
        self.tam = 5
        self.max_num = max_num
        
        # Generar dos tarjetas independientes
        gen = GeneradorCarton(palabra, max_num)
        self.tarjeta1 = gen.generar()
        self.tarjeta2 = gen.generar()
        
        # Estados de marcado separados
        self._marcados1: set[tuple[int, int]] = set()
        self._marcados2: set[tuple[int, int]] = set()
        
        # Marcar centro en ambas
        centro = 2
        self._marcados1.add((centro, centro))
        self._marcados2.add((centro, centro))
        
        # Verificador inyectado (DIP)
        self._verificador = verificador or VerificadorBingo()
    
    def marcar_numero(self, numero: int) -> bool:
        """Marca el número en ambas tarjetas. Retorna True si se marcó en al menos una."""
        m1 = self._marcar_en_tarjeta(numero, self.tarjeta1, self._marcados1)
        m2 = self._marcar_en_tarjeta(numero, self.tarjeta2, self._marcados2)
        return m1 or m2
    
    def _marcar_en_tarjeta(self, numero: int, tarjeta: list[list], 
                          marcados: set[tuple[int, int]]) -> bool:
        """Lógica aislada y testeable para marcar en una tarjeta específica."""
        for i in range(5):
            for j in range(5):
                if tarjeta[i][j] == numero and (i, j) not in marcados:
                    marcados.add((i, j))
                    return True
        return False
    
    def esta_marcado(self, fila: int, col: int) -> bool:
        """Consulta si una posición está marcada en ALGUNA de las dos tarjetas."""
        return ((fila, col) in self._marcados1 or self.tarjeta1[fila][col] == "X" or
                (fila, col) in self._marcados2 or self.tarjeta2[fila][col] == "X")
    
    def verificar_bingo(self, modo: str = None) -> bool:
        """Verifica si ALGUNA de las dos tarjetas tiene bingo."""
        # Crear cartones temporales para reutilizar la lógica de VerificadorBingo
        c1 = Carton(self.palabra, self.max_num, self.tarjeta1)
        c1._marcados = self._marcados1.copy()
        
        c2 = Carton(self.palabra, self.max_num, self.tarjeta2)
        c2._marcados = self._marcados2.copy()
        
        # Verificar ambas
        bingo1, _ = self._verificador.tiene_bingo(c1, modo)
        if bingo1:
            return True
        bingo2, _ = self._verificador.tiene_bingo(c2, modo)
        return bingo2
    
    def grilla_mas_cerca(self) -> str:
        """Indica cuál tarjeta está más cerca de completar bingo (por conteo de marcados)."""
        total1 = len(self._marcados1)
        total2 = len(self._marcados2)
        
        if total1 > total2:
            return "Cartón 1"
        elif total2 > total1:
            return "Cartón 2"
        else:
            return "Ambos están igual de cerca"
    
    def imprimir(self, presentador=None) -> None:
        """Imprime ambas tarjetas del cartón doble."""
        if presentador and hasattr(presentador, 'imprimir_carton_doble'):
            presentador.imprimir_carton_doble(self)
        else:
            # Fallback básico
            print("=== Cartón 1 ===")
            self._imprimir_basico(self.tarjeta1, self._marcados1)
            print("\n=== Cartón 2 ===")
            self._imprimir_basico(self.tarjeta2, self._marcados2)
    
    def _imprimir_basico(self, tarjeta: list[list], marcados: set) -> None:
        """Impresión básica por consola para una tarjeta."""
        print("   ".join(self.palabra))
        print("-" * 15)
        for i, fila in enumerate(tarjeta):
            linea = []
            for j, valor in enumerate(fila):
                if (i, j) in marcados or valor == "X":
                    linea.append(" X")
                else:
                    linea.append(f"{valor:2}")
            print("  ".join(linea))