"""Pruebas del adaptador que lee productos.credito_consumo de banco.yaml (RN-01 a RN-05).

Usa un banco.yaml sintético en un directorio temporal; nunca el archivo real.
"""
from decimal import Decimal

from simulador_credito.adaptadores.parametros_desde_banco import ProveedorParametrosDesdeBanco

BANCO_SINTETICO = """\
productos:
  credito_consumo:
    tasa_maxima_ea: 0.26
    monto_minimo: 1000000
    monto_maximo: 100000000
    plazo_meses: {minimo: 6, maximo: 72}
    endeudamiento_maximo: 0.40
"""


def test_parametros_desde_banco_convierte_tasa_a_decimal(tmp_path):
    """Regla: productos.credito_consumo (RN-01 a RN-05). La tasa 0.26 llega como Decimal("0.26"), no como float."""
    ruta = tmp_path / "banco.yaml"
    ruta.write_text(BANCO_SINTETICO, encoding="utf-8")

    parametros = ProveedorParametrosDesdeBanco(ruta).obtener()

    assert isinstance(parametros.tasa_maxima_ea, Decimal)
    assert parametros.tasa_maxima_ea == Decimal("0.26")
    assert parametros.endeudamiento_maximo == Decimal("0.40")
    assert parametros.monto_minimo == Decimal("1000000")
    assert parametros.monto_maximo == Decimal("100000000")
    assert (parametros.plazo_minimo, parametros.plazo_maximo) == (6, 72)
