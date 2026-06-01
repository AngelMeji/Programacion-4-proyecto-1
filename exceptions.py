"""Excepciones de dominio del sistema de Bingo."""


class BingoException(Exception):
    """Excepción base para todos los errores del dominio."""


class ConfiguracionJuegoError(BingoException):
    """Error en la configuración general del juego."""


class CartonConfigError(ConfiguracionJuegoError):
    """Error en la configuración de un cartón o del generador."""


class BomboConfigError(ConfiguracionJuegoError):
    """Error en la configuración del bombo de números."""


class NumeroInvalidoError(BingoException):
    """El número está fuera del rango permitido del juego."""


class BomboVacioError(BingoException):
    """Se intentó extraer un número cuando el bombo ya estaba vacío."""


class PatronNoRegistradoError(BingoException):
    """Se solicitó verificar un patrón o modo no registrado."""


class GeneracionCartonError(BingoException):
    """Error durante la generación de una tarjeta de bingo."""


class JugadorDuplicadoError(BingoException):
    """Se intentó registrar un jugador con un nombre ya existente."""


class JuegoError(BingoException):
    """Error de coordinación durante el flujo de la partida."""


class SinJugadoresError(JuegoError):
    """Se intentó iniciar la partida sin jugadores registrados."""


class ExtraccionBomboError(JuegoError):
    """Fallo inesperado al extraer números del bombo."""