"""Adaptador para pruebas: entrega parámetros fijos del producto, sin leer archivos."""
from simulador_credito.dominio.simulacion import ParametrosProducto


class ProveedorParametrosEnMemoria:
    """Doble del puerto ProveedorParametrosProducto con valores dados al crear el objeto."""

    def __init__(self, parametros: ParametrosProducto) -> None:
        self._parametros = parametros

    def obtener(self) -> ParametrosProducto:
        """Devuelve los parámetros recibidos."""
        return self._parametros
