"""Puerto: de dónde salen los límites del producto. Solo el contrato."""
from typing import Protocol

from simulador_credito.dominio.simulacion import ParametrosProducto


class ProveedorParametrosProducto(Protocol):
    """Entrega los límites vigentes del producto de crédito de consumo."""

    def obtener(self) -> ParametrosProducto:
        """Devuelve los parámetros del producto."""
        ...
