"""
Módulo: exceptions.py
Responsabilidad: Definir excepciones de dominio para tolerancia a fallos.
"""

class BingoException(Exception):
    """Excepción base para errores del dominio Bingo."""
    pass


class CartonConfigError(BingoException):
    """Error en la configuración de un cartón (palabra, max_num)."""
    pass


class NumeroInvalidoError(BingoException):
    """El número está fuera del rango permitido del juego."""
    pass


class PatronNoRegistradoError(BingoException):
    """Se solicitó verificar un patrón no registrado en el sistema."""
    pass


class GeneracionCartonError(BingoException):
    """Error durante la generación de una tarjeta de bingo."""
    pass