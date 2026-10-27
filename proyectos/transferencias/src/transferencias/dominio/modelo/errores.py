"""Errores de negocio. La capa app los traduce a mensajes para el usuario."""


class ErrorTransferencia(Exception):
    """Base de los errores de negocio."""


class CuentaNoEncontrada(ErrorTransferencia):
    pass


class CuentaNoActiva(ErrorTransferencia):
    pass


class FondosInsuficientes(ErrorTransferencia):
    pass


class MontoInvalido(ErrorTransferencia):
    pass


class LimiteDiarioExcedido(ErrorTransferencia):
    pass
