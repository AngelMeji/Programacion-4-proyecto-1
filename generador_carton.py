"""
Módulo: generador_carton.py
Responsabilidad única: Generar tarjetas de bingo válidas según reglas del juego.
Razón para cambiar: Si cambian las reglas de generación (rangos, distribución, casilla libre).
"""

import random
from exceptions import CartonConfigError, GeneracionCartonError
from interfaces import IGeneradorCarton


class GeneradorCarton(IGeneradorCarton):
    """Genera tarjetas de bingo 5x5 con números únicos por columna."""
    
    def __init__(self, palabra: str, max_num: int):
        self._validar_configuracion(palabra, max_num)
        self.palabra = palabra.upper()
        self.tam = len(self.palabra)  # Siempre 5
        self.max_num = max_num
        self.intervalo_columna = max_num // self.tam
    
    def generar(self) -> list[list]:
        """
        Genera una tarjeta aleatoria 5x5.
        
        Returns:
            list[list]: Matriz 5x5 con números válidos y casilla central libre.
        
        Raises:
            GeneracionCartonError: Si no se pueden generar números válidos.
        """
        try:
            tarjeta = [[0] * self.tam for _ in range(self.tam)]
            usados = set()
            
            for col in range(self.tam):
                minimo, maximo = self._rango_columna(col)
                disponibles = [n for n in range(minimo, maximo + 1) if n not in usados]
                
                if len(disponibles) < self.tam:
                    raise GeneracionCartonError(
                        f"No hay suficientes números en columna {col} [{minimo}-{maximo}]"
                    )
                
                seleccionados = random.sample(disponibles, self.tam)
                for fila, valor in enumerate(seleccionados):
                    tarjeta[fila][col] = valor
                    usados.add(valor)
            
            # Casilla central libre
            centro = self.tam // 2
            tarjeta[centro][centro] = "X"
            
            return tarjeta
            
        except Exception as e:
            if isinstance(e, GeneracionCartonError):
                raise
            raise GeneracionCartonError(f"Error generando tarjeta: {e}") from e
    
    def generar_varias(self, cantidad: int) -> list[list[list]]:
        """Genera múltiples tarjetas independientes."""
        if cantidad < 1:
            raise ValueError("La cantidad debe ser al menos 1")
        return [self.generar() for _ in range(cantidad)]
    
    def _rango_columna(self, col: int) -> tuple[int, int]:
        """Calcula el rango [min, max] para una columna dada."""
        minimo = col * self.intervalo_columna + 1
        maximo = (col + 1) * self.intervalo_columna
        return minimo, maximo
    
    def _validar_configuracion(self, palabra: str, max_num: int) -> None:
        """Valida los parámetros de configuración del generador."""
        if len(palabra) != 5:
            raise CartonConfigError("La palabra debe tener exactamente 5 letras")
        if len(set(palabra)) != 5:
            raise CartonConfigError("La palabra no debe tener letras repetidas")
        if not (50 <= max_num <= 90):
            raise CartonConfigError("El máximo número debe estar entre 50 y 90")
        if max_num % 5 != 0:
            raise CartonConfigError("El máximo número debe ser múltiplo de 5")