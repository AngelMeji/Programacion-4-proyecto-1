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

class IBombo(ABC):
    """Contrato para el bombo de extracción de números del juego."""

    @abstractmethod
    def extraer_numero(self) -> int:
        pass

    @abstractmethod
    def obtener_historial(self) -> list[int]:
        pass

    @abstractmethod
    def hay_numeros(self) -> bool:
        pass

class IGestorJugadores(ABC):
    """Contrato para gestión de jugadores en el juego."""

    @abstractmethod
    def buscar_jugador_por_nombre(self, nombre: str):
        pass

    @abstractmethod
    def obtener_jugadores(self) -> list:
        pass

    @abstractmethod
    def agregar_jugador(self, jugador) -> None:
        pass

    @abstractmethod
    def eliminar_jugador(self, jugador) -> None:
        pass

    @abstractmethod
    def hay_jugadores(self) -> bool:
        pass

class IPresentadorResultados(ABC):
    """Contrato para mostrar el estado y resultados del juego."""

    @abstractmethod
    def inicio_partida(self) -> None:
        pass

    @abstractmethod
    def mostrar_turno(self, numero: int, turno: int) -> None:
        pass

    @abstractmethod
    def jugador_marco(self, jugador) -> None:
        pass

    @abstractmethod
    def jugador_no_marco(self, jugador) -> None:
        pass

    @abstractmethod
    def mostrar_resultado_final(
        self,
        ganador,
        historial: str,
        resumen_jugadores: list[tuple[str, int]]
    ) -> None:
        pass

class IGeneradorCarton(ABC):
    """Contrato para generar tarjetas de bingo."""

    @abstractmethod
    def generar(self) -> list[list]:
        pass

    @abstractmethod
    def generar_varias(self, cantidad: int) -> list[list[list]]:
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