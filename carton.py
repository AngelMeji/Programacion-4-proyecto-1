"""
Módulo: carton.py
Responsabilidad única: Representar el estado de un cartón de bingo y permitir marcar números.
Razón para cambiar: Si cambia la estructura interna de almacenamiento o la lógica de marcado.
"""
from interfaces import IMarcableVerificable, IImprimible, IGeneradorCarton, IVerificadorBingo
from typing import Optional
from exceptions import NumeroInvalidoError
from generador_carton import GeneradorCarton


class Carton(IMarcableVerificable, IImprimible):
    """
    Representa el estado de un cartón de bingo.
    Implementa 3 interfaces segregadas para que cada cliente dependa solo de lo que necesita.
    """
    
    """
    Representa el estado de un cartón de bingo.
    
    Esta clase SOLO maneja:
    - Almacenamiento de la tarjeta y palabra
    - Marcado de números
    - Consulta del estado de marcación
    
    NO genera tarjetas, NO verifica patrones, NO imprime.
    """
    
    
    def __init__(
        self,
        palabra: str,
        max_num: int,
        tarjeta: Optional[list[list]] = None,
        generador: Optional[IGeneradorCarton] = None,
        verificador: Optional[IVerificadorBingo] = None,
    ):
        """
        Inicializa un cartón con una tarjeta existente o generada por un generador inyectado.

        Args:
            palabra: Palabra de 5 letras para los encabezados.
            max_num: Número máximo del juego (50-90, múltiplo de 5).
            tarjeta: Matriz 5x5 generada externamente.
            generador: Generador inyectado que crea la tarjeta si no se proporciona una.
            verificador: Verificador de bingo inyectado para validar el cartón.
        """
        self.palabra = palabra.upper()
        self.tam = len(self.palabra)  # Siempre 5
        self.max_num = max_num
        
        # Inyección de dependencia para generación de tarjeta
        self._generador = generador if generador is not None else GeneradorCarton(palabra, max_num)
        self.tarjeta = tarjeta if tarjeta is not None else self._generador.generar()

        # Conjunto de posiciones marcadas: {(fila, col), ...}
        self._marcados: set[tuple[int, int]] = set()
        if verificador is not None:
            self._verificador = verificador
        else:
            from verificador_bingo import VerificadorBingo
            self._verificador = VerificadorBingo()
        
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
    
    def _inicializar_con_estado(self, tarjeta: list[list], marcados: set[tuple[int,int]]) -> None:
        """Inicializa el cartón con una tarjeta y estado de marcados existentes."""
        self.tarjeta = tarjeta
        self._marcados = marcados.copy()
    
    def _crear_matriz_vacia(self) -> list[list]:
        """Crea una matriz 5x5 inicial con ceros."""
        return [[0] * self.tam for _ in range(self.tam)]

    def _generar_tarjeta(self) -> list[list]:
        """Genera una tarjeta aleatoria usando el generador inyectado."""
        return self._generador.generar()

    def verificar_bingo(self, modo: str | None = None) -> bool:
        """Verifica si este cartón tiene bingo según el modo seleccionado."""
        tiene_bingo, _ = self._verificador.tiene_bingo(self, modo)
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