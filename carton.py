"""
Módulo: carton.py
Responsabilidad única: Representar el estado de un cartón de bingo y permitir marcar números.
Razón para cambiar: Si cambia la estructura interna de almacenamiento o la lógica de marcado.
"""

from typing import Optional
from exceptions import NumeroInvalidoError
from generador_carton import GeneradorCarton


class Carton:
    """
    Representa el estado de un cartón de bingo.
    
    Esta clase SOLO maneja:
    - Almacenamiento de la tarjeta y palabra
    - Marcado de números
    - Consulta del estado de marcación
    
    NO genera tarjetas, NO verifica patrones, NO imprime.
    """
    
    def __init__(self, palabra: str, max_num: int, tarjeta: Optional[list[list]] = None):
        """
        Inicializa un cartón con una tarjeta existente o vacía.
        
        Args:
            palabra: Palabra de 5 letras para los encabezados.
            max_num: Número máximo del juego (50-90, múltiplo de 5).
            tarjeta: Matriz 5x5 generada externamente. Si es None, crea una vacía.
        """
        self.palabra = palabra.upper()
        self.tam = len(self.palabra)  # Siempre 5
        self.max_num = max_num
        
        # Recibe la tarjeta generada externamente (inyección de dependencia)
        self.tarjeta = tarjeta if tarjeta is not None else self._generar_tarjeta()

        # Conjunto de posiciones marcadas: {(fila, col), ...}
        self._marcados: set[tuple[int, int]] = set()
        
        # Marcar automáticamente la casilla central si ya es "X"
        centro = self.tam // 2
        if self.tarjeta[centro][centro] == "X":
            self._marcados.add((centro, centro))
    
    def marcar_numero(self, numero: int) -> bool:
        """
        Marca un número en la tarjeta si existe y no está marcado.
        
        Args:
            numero: Número a marcar.
            
        Returns:
            bool: True si se marcó, False si no estaba en el cartón.
            
        Raises:
            NumeroInvalidoError: Si el número está fuera de rango.
        """
        if not (1 <= numero <= self.max_num):
            raise NumeroInvalidoError(
                f"El número {numero} está fuera del rango [1, {self.max_num}]"
            )
        
        for i in range(self.tam):
            for j in range(self.tam):
                if self.tarjeta[i][j] == numero and (i, j) not in self._marcados:
                    self._marcados.add((i, j))
                    return True
        return False
    
    def esta_marcado(self, fila: int, col: int) -> bool:
        """
        Consulta si una posición específica está marcada.
        
        Args:
            fila: Índice de fila (0-4).
            col: Índice de columna (0-4).
            
        Returns:
            bool: True si la posición está marcada o es la casilla libre.
        """
        if not (0 <= fila < self.tam and 0 <= col < self.tam):
            return False
        return (fila, col) in self._marcados or self.tarjeta[fila][col] == "X"
    
    def obtener_tarjeta(self) -> list[list]:
        """
        Devuelve una copia de la matriz de la tarjeta (solo lectura).
        
        Returns:
            list[list]: Copia profunda de la tarjeta con valores actuales.
        """
        return [fila.copy() for fila in self.tarjeta]
    
    def obtener_marcados(self) -> set[tuple[int, int]]:
        """
        Devuelve una copia del conjunto de posiciones marcadas.
        
        Returns:
            set: Copia del conjunto de tuplas (fila, col) marcadas.
        """
        return self._marcados.copy()
    
    def _crear_matriz_vacia(self) -> list[list]:
        """Crea una matriz 5x5 inicial con ceros."""
        return [[0] * self.tam for _ in range(self.tam)]

    def _generar_tarjeta(self) -> list[list]:
        """Genera una tarjeta aleatoria usando el generador de cartones."""
        generador = GeneradorCarton(self.palabra, self.max_num)
        return generador.generar()

    def verificar_bingo(self, modo: str | None = None) -> bool:
        """Verifica si este cartón tiene bingo según el modo seleccionado."""
        from verificador_bingo import VerificadorBingo

        verificador = VerificadorBingo()
        tiene_bingo, _ = verificador.tiene_bingo(self, modo)
        return tiene_bingo
    
    # Métodos de presentación delegados a una clase externa (SRP)
    def imprimir(self, presentador=None) -> None:
        """
        Imprime el cartón usando un presentador externo.
        
        Args:
            presentador: Objeto con método imprimir_carton(carton: Carton).
                        Si es None, usa impresión básica por consola.
        """
        if presentador and hasattr(presentador, 'imprimir_carton'):
            presentador.imprimir_carton(self)
        else:
            # Fallback básico (podría moverse a PresentadorCarton después)
            print("   ".join(self.palabra))
            print("-" * (self.tam * 3))
            for i, fila in enumerate(self.tarjeta):
                linea = []
                for j, valor in enumerate(fila):
                    if (i, j) in self._marcados or valor == "X":
                        linea.append(" X")
                    else:
                        linea.append(f"{valor:2}")
                print("  ".join(linea))