"""

Responsabilidad: Definir contratos específicos por capacidad.
Principio: ISP — Muchas interfaces pequeñas son mejor que una interfaz gigante.
"""
from abc import ABC, abstractmethod
from typing import Optional

class IMarcable(ABC):
    """Capacidad de recibir y registrar números."""
    @abstractmethod
    def marcar_numero(self, numero: int) -> bool:
        pass

class IVerificable(ABC):
    """Capacidad de verificar si se completó un patrón de victoria."""
    @abstractmethod
    def verificar_bingo(self, modo: Optional[str] = None) -> bool:
        pass

class IImprimible(ABC):
    """Capacidad de mostrar su estado actual en pantalla."""
    @abstractmethod
    def imprimir(self) -> None:
        pass
    

class IVerificadorBingo(ABC):
    """
    Capacidad de verificar si un cartón tiene bingo.
    Clientes: Carton, CartonDoble, VerificadorBingo.
    """
    @abstractmethod
    def tiene_bingo(self, carton, modo: Optional[str] = None) -> tuple[bool, str]:
        """
        Verifica bingo y retorna (tiene_bingo, nombre_del_patron).
        """
        pass

class IValidadorVictoria(ABC):
    """
    Capacidad de determinar qué jugador ganó.
    Clientes: Juego, flujo de partida.
    """
    @abstractmethod
    def verificar_ganador(self, jugadores: list) -> Optional[object]:
        """
        Retorna el primer jugador ganador o None.
        """
        pass

class IMarcableVerificable(IMarcable, IVerificable, ABC):
    """Contrato combinado para cartones que se pueden marcar y verificar."""
    pass

class IGestorPatrones(ABC):
    """
    Capacidad de administrar y extender la colección de patrones.
    Clientes: main.py, configuración, pruebas.
    """
    @abstractmethod
    def agregar_patron(self, patron) -> None:
        pass

    @abstractmethod
    def listar_patrones(self) -> list[str]:
        pass