"""Pruebas de las reglas del banco (RN-01 a RN-05). Los límites llegan como parámetros, no de archivos."""
from decimal import Decimal

import pytest

from simulador_credito.dominio.reglas import (
    validar_endeudamiento,
    validar_monto,
    validar_plazo,
    validar_tasa,
)

MONTO_MINIMO = Decimal("1000000")
MONTO_MAXIMO = Decimal("100000000")
PLAZO_MINIMO = 6
PLAZO_MAXIMO = 72
TASA_MAXIMA = Decimal("0.26")
ENDEUDAMIENTO_MAXIMO = Decimal("0.40")


def test_monto_minimo_999999_rechaza():
    """Regla: productos.credito_consumo.monto_minimo (RN-01)."""
    motivo = validar_monto(Decimal("999999"), MONTO_MINIMO, MONTO_MAXIMO)
    assert motivo is not None
    assert motivo.regla == "RN-01"
    assert motivo.mensaje == "El monto mínimo es 1.000.000 COP."


def test_monto_minimo_1000000_acepta():
    """Regla: productos.credito_consumo.monto_minimo (RN-01, borde)."""
    assert validar_monto(Decimal("1000000"), MONTO_MINIMO, MONTO_MAXIMO) is None


def test_monto_maximo_100000001_rechaza():
    """Regla: productos.credito_consumo.monto_maximo (RN-02)."""
    motivo = validar_monto(Decimal("100000001"), MONTO_MINIMO, MONTO_MAXIMO)
    assert motivo is not None
    assert motivo.regla == "RN-02"
    assert motivo.mensaje == "El monto máximo es 100.000.000 COP."


def test_monto_maximo_100000000_acepta():
    """Regla: productos.credito_consumo.monto_maximo (RN-02, borde)."""
    assert validar_monto(Decimal("100000000"), MONTO_MINIMO, MONTO_MAXIMO) is None


def test_plazo_5_meses_rechaza():
    """Regla: productos.credito_consumo.plazo_meses (RN-03)."""
    motivo = validar_plazo(5, PLAZO_MINIMO, PLAZO_MAXIMO)
    assert motivo is not None
    assert motivo.regla == "RN-03"
    assert motivo.mensaje == "El plazo debe estar entre 6 y 72 meses."


def test_plazo_6_meses_acepta():
    """Regla: productos.credito_consumo.plazo_meses (RN-03, borde)."""
    assert validar_plazo(6, PLAZO_MINIMO, PLAZO_MAXIMO) is None


def test_plazo_73_meses_rechaza():
    """Regla: productos.credito_consumo.plazo_meses (RN-03)."""
    motivo = validar_plazo(73, PLAZO_MINIMO, PLAZO_MAXIMO)
    assert motivo is not None
    assert motivo.mensaje == "El plazo debe estar entre 6 y 72 meses."


def test_plazo_72_meses_acepta():
    """Regla: productos.credito_consumo.plazo_meses (RN-03, borde)."""
    assert validar_plazo(72, PLAZO_MINIMO, PLAZO_MAXIMO) is None


def test_tasa_27_ea_rechaza():
    """Regla: productos.credito_consumo.tasa_maxima_ea (RN-04)."""
    motivo = validar_tasa(Decimal("0.27"), TASA_MAXIMA)
    assert motivo is not None
    assert motivo.regla == "RN-04"
    assert motivo.mensaje == "La tasa máxima permitida es 26 % E.A."


def test_tasa_26_ea_acepta():
    """Regla: productos.credito_consumo.tasa_maxima_ea (RN-04, borde)."""
    assert validar_tasa(Decimal("0.26"), TASA_MAXIMA) is None


def test_endeudamiento_52_6_no_valido():
    """Regla: productos.credito_consumo.endeudamiento_maximo (RN-05). Muestra 52,6 % y no lo acepta."""
    motivo = validar_endeudamiento(Decimal("0.526"), ENDEUDAMIENTO_MAXIMO)
    assert motivo is not None
    assert motivo.regla == "RN-05"
    assert motivo.mensaje == "El endeudamiento de 52,6 % supera el máximo permitido de 40 %."


def test_endeudamiento_40_por_ciento_acepta():
    """Regla: productos.credito_consumo.endeudamiento_maximo (RN-05, borde)."""
    assert validar_endeudamiento(Decimal("0.40"), ENDEUDAMIENTO_MAXIMO) is None


@pytest.mark.parametrize(
    ("endeudamiento", "rechaza"),
    [
        (Decimal("0.399999"), False),
        (Decimal("0.40"), False),
        (Decimal("0.400001"), True),
        (Decimal("0.4004"), True),
        (Decimal("0.4005"), True),
    ],
    ids=["justo_debajo", "igual_maximo", "justo_encima", "exceso_oculto", "exceso_visible"],
)
def test_endeudamiento_bordes(endeudamiento: Decimal, rechaza: bool) -> None:
    """Regla: productos.credito_consumo.endeudamiento_maximo (RN-05), sin redondear para validar."""
    motivo = validar_endeudamiento(endeudamiento, ENDEUDAMIENTO_MAXIMO)
    if rechaza:
        assert motivo is not None
        assert motivo.regla == "RN-05"
    else:
        assert motivo is None


def test_endeudamiento_22_2_por_ciento_le_alcanza():
    """Regla: productos.credito_consumo.endeudamiento_maximo (RN-05). 22,2 % sí le alcanza."""
    assert validar_endeudamiento(Decimal("0.222"), ENDEUDAMIENTO_MAXIMO) is None


def test_endeudamiento_52_6_por_ciento_no_le_alcanza():
    """Regla: productos.credito_consumo.endeudamiento_maximo (RN-05). 52,6 % no le alcanza."""
    motivo = validar_endeudamiento(Decimal("0.526"), ENDEUDAMIENTO_MAXIMO)
    assert motivo is not None
    assert motivo.regla == "RN-05"
