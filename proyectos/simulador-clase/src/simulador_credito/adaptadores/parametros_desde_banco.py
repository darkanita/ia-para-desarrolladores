"""Adaptador real: lee productos.credito_consumo de banco.yaml. Los números se convierten por texto, nunca desde float."""
from decimal import Decimal
from pathlib import Path

import yaml

from simulador_credito.dominio.simulacion import ParametrosProducto


class ProveedorParametrosDesdeBanco:
    """Implementa ProveedorParametrosProducto leyendo el archivo banco.yaml indicado."""

    def __init__(self, ruta: Path) -> None:
        self._ruta = ruta

    def obtener(self) -> ParametrosProducto:
        """Lee el archivo y devuelve los límites del crédito de consumo."""
        datos = yaml.safe_load(self._ruta.read_text(encoding="utf-8"))
        credito = datos["productos"]["credito_consumo"]
        plazo = credito["plazo_meses"]
        return ParametrosProducto(
            monto_minimo=Decimal(str(credito["monto_minimo"])),
            monto_maximo=Decimal(str(credito["monto_maximo"])),
            plazo_minimo=int(plazo["minimo"]),
            plazo_maximo=int(plazo["maximo"]),
            tasa_maxima_ea=Decimal(str(credito["tasa_maxima_ea"])),
            endeudamiento_maximo=Decimal(str(credito["endeudamiento_maximo"])),
        )
