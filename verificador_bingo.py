"""
Módulo: verificador_bingo.py
Responsabilidad única: Coordinar múltiples verificadores de patrones.
Razón para cambiar: Si cambia la lógica de combinación/prioridad de patrones.
Principio: SRP + OCP — Coordinación separada, patrones extensibles.
"""

from typing import Optional
from carton import Carton
from verificador_patron import (
    VerificadorPatron,
    VerificadorFila, VerificadorColumna, VerificadorDiagonal,
    VerificadorEsquinas, VerificadorCruz, VerificadorBorde,
    VerificadorCentral, VerificadorCompleto
)


class VerificadorBingo:
    """
    Coordina la verificación de múltiples patrones de victoria.
    
    Esta clase NO contiene lógica de patrones específicos.
    Para agregar un nuevo patrón: instanciar su verificador y agregarlo a la lista.
    """
    
    PATRONES_POR_DEFECTO = [
        VerificadorFila(), VerificadorColumna(), VerificadorDiagonal(),
        VerificadorEsquinas(), VerificadorCruz(), VerificadorBorde(),
        VerificadorCentral(), VerificadorCompleto()
    ]
    
    # Mapeo de modos de texto a claves de patrón para filtrado
    MODO_A_CLAVES = {
        "horizontal": ["horizontal"],
        "vertical": ["vertical"],
        "diagonal": ["diagonal"],
        "filas_columnas": ["horizontal", "vertical"],
        "esquinas": ["esquinas"],
        "cruz": ["cruz"],
        "borde": ["borde"],
        "central": ["central"],
        "completo": ["completo"],
        "todos": None,  # None = verificar todos
    }
    
    def __init__(self, patrones: Optional[list[VerificadorPatron]] = None):
        """
        Inicializa el verificador con una lista de patrones a verificar.
        
        Args:
            patrones: Lista de instancias de VerificadorPatron.
                     Si es None, usa los patrones por defecto.
        """
        self._patrones = patrones if patrones is not None else self.PATRONES_POR_DEFECTO.copy()
    
    def tiene_bingo(self, carton: "Carton", modo: Optional[str] = None) -> tuple[bool, str]:
        """
        Verifica si el cartón tiene bingo según el modo especificado.
        
        Args:
            carton: Instancia de Carton a verificar.
            modo: Clave de modo ('horizontal', 'esquinas', etc.) o None para todos.
            
        Returns:
            tuple[bool, str]: (tiene_bingo, nombre_del_patron_ganador)
        """
        tarjeta = carton.obtener_tarjeta()
        marcados = carton.obtener_marcados()
        centro = len(tarjeta) // 2
        
        # Filtrar patrones según el modo solicitado
        patrones_a_verificar = self._filtrar_por_modo(modo)
        
        # Verificar cada patrón en orden
        for patron in patrones_a_verificar:
            if patron.cumple(tarjeta, marcados, centro):
                return True, patron.nombre
        
        return False, ""
    
    def _filtrar_por_modo(self, modo: Optional[str]) -> list[VerificadorPatron]:
        """Filtra la lista de patrones según el modo solicitado."""
        if not modo or modo.lower() in ("todos", ""):
            return self._patrones
        
        modo_key = modo.lower()
        claves_permitidas = self.MODO_A_CLAVES.get(modo_key)
        
        if claves_permitidas is None:
            # Modo no reconocido: no verificar nada por seguridad
            return []
        
        return [p for p in self._patrones if p.modo_clave in claves_permitidas]
    
    def agregar_patron(self, patron: VerificadorPatron) -> None:
        """
        Agrega un nuevo patrón a verificar (OCP en acción).
        
        Args:
            patron: Instancia de VerificadorPatron a agregar.
        """
        if patron not in self._patrones:
            self._patrones.append(patron)
    
    def listar_patrones(self) -> list[str]:
        """Devuelve la lista de nombres de patrones registrados."""
        return [p.nombre for p in self._patrones]