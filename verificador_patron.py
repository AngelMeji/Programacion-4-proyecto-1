"""
Módulo: verificador_patron.py
Responsabilidad: Definir la abstracción para patrones de victoria y sus implementaciones.
Razón para cambiar: Si se agregan, modifican o eliminan patrones de victoria.
Principio: OCP — Abierto para extensión, cerrado para modificación.
"""

from abc import ABC, abstractmethod
from typing import Optional


class VerificadorPatron(ABC):
    """
    Abstracción para verificar un patrón de victoria en bingo.
    
    Cada subclase implementa la lógica de un patrón específico.
    Para agregar un nuevo patrón: crear nueva clase, NO modificar esta.
    """
    
    @abstractmethod
    def cumple(self, tarjeta: list[list], marcados: set[tuple[int, int]], centro: int) -> bool:
        """
        Verifica si el patrón se cumple en la tarjeta dada.
        
        Args:
            tarjeta: Matriz 5x5 con los valores del cartón.
            marcados: Conjunto de tuplas (fila, col) que están marcadas.
            centro: Índice de la casilla central (usualmente 2).
            
        Returns:
            bool: True si el patrón está completo.
        """
        pass
    
    @property
    @abstractmethod
    def nombre(self) -> str:
        """Nombre descriptivo del patrón para presentación."""
        pass
    
    @property
    def modo_clave(self) -> Optional[str]:
        """Clave de texto para identificar el patrón (opcional, para filtrado)."""
        return None


# ===== Implementaciones concretas de patrones =====

class VerificadorFila(VerificadorPatron):
    """Verifica si alguna fila está completamente marcada."""
    
    def cumple(self, tarjeta, marcados, centro):
        for fila in range(5):
            if all((fila, col) in marcados or tarjeta[fila][col] == "X" for col in range(5)):
                return True
        return False
    
    @property
    def nombre(self): return "Fila completa"
    @property
    def modo_clave(self): return "horizontal"


class VerificadorColumna(VerificadorPatron):
    """Verifica si alguna columna está completamente marcada."""
    
    def cumple(self, tarjeta, marcados, centro):
        for col in range(5):
            if all((fila, col) in marcados or tarjeta[fila][col] == "X" for fila in range(5)):
                return True
        return False
    
    @property
    def nombre(self): return "Columna completa"
    @property
    def modo_clave(self): return "vertical"


class VerificadorDiagonal(VerificadorPatron):
    """Verifica si alguna diagonal está completamente marcada."""
    
    def cumple(self, tarjeta, marcados, centro):
        # Diagonal principal
        if all((i, i) in marcados or tarjeta[i][i] == "X" for i in range(5)):
            return True
        # Diagonal secundaria
        if all((i, 4-i) in marcados or tarjeta[i][4-i] == "X" for i in range(5)):
            return True
        return False
    
    @property
    def nombre(self): return "Diagonal completa"
    @property
    def modo_clave(self): return "diagonal"


class VerificadorEsquinas(VerificadorPatron):
    """Verifica el patrón de las cuatro esquinas."""
    
    def cumple(self, tarjeta, marcados, centro):
        esquinas = [(0,0), (0,4), (4,0), (4,4)]
        return all((f,c) in marcados or tarjeta[f][c] == "X" for f,c in esquinas)
    
    @property
    def nombre(self): return "Cuatro esquinas"
    @property
    def modo_clave(self): return "esquinas"


class VerificadorCruz(VerificadorPatron):
    """Verifica el patrón de cruz central (fila y columna del medio)."""
    
    def cumple(self, tarjeta, marcados, centro):
        # Fila central
        fila_ok = all((centro, col) in marcados or tarjeta[centro][col] == "X" for col in range(5))
        # Columna central
        col_ok = all((fila, centro) in marcados or tarjeta[fila][centro] == "X" for fila in range(5))
        return fila_ok and col_ok
    
    @property
    def nombre(self): return "Cruz central"
    @property
    def modo_clave(self): return "cruz"


class VerificadorBorde(VerificadorPatron):
    """Verifica el patrón de borde (perímetro completo)."""
    
    def cumple(self, tarjeta, marcados, centro):
        # Borde superior e inferior
        for col in range(5):
            if (0, col) not in marcados and tarjeta[0][col] != "X":
                return False
            if (4, col) not in marcados and tarjeta[4][col] != "X":
                return False
        # Borde izquierdo y derecho (sin repetir esquinas)
        for fila in range(1, 4):
            if (fila, 0) not in marcados and tarjeta[fila][0] != "X":
                return False
            if (fila, 4) not in marcados and tarjeta[fila][4] != "X":
                return False
        return True
    
    @property
    def nombre(self): return "Borde completo"
    @property
    def modo_clave(self): return "borde"


class VerificadorCentral(VerificadorPatron):
    """Verifica el patrón del cuadro central 3x3."""
    
    def cumple(self, tarjeta, marcados, centro):
        for fila in range(1, 4):
            for col in range(1, 4):
                if (fila, col) not in marcados and tarjeta[fila][col] != "X":
                    return False
        return True
    
    @property
    def nombre(self): return "Cuadro central 3x3"
    @property
    def modo_clave(self): return "central"


class VerificadorCompleto(VerificadorPatron):
    """Verifica si toda la tarjeta está marcada (cartón lleno)."""
    
    def cumple(self, tarjeta, marcados, centro):
        for fila in range(5):
            for col in range(5):
                if (fila, col) not in marcados and tarjeta[fila][col] != "X":
                    return False
        return True
    
    @property
    def nombre(self): return "Cartón lleno"
    @property
    def modo_clave(self): return "completo"