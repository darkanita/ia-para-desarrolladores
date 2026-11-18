"""Pruebas de los cálculos de tasa, cuota y costo total (dominio).

Valores esperados calculados aparte con datos sintéticos; no se copian de la salida del código.
"""
from decimal import Decimal

from simulador_credito.dominio.calculos import (
    calcular_costo_total,
    calcular_cuota_mensual,
    calcular_endeudamiento,
    calcular_tasa_mensual,
)


def test_tasa_mensual_desde_ea():
    """Regla: convenciones.tasas. Mensual = (1 + ea)^(1/12) - 1, no ea / 12."""
    tasa = calcular_tasa_mensual(Decimal("0.26"))
    # Referencia calculada aparte: 0,0194459669612575...
    assert abs(tasa - Decimal("0.0194459669612575")) < Decimal("0.000000000000001")


def test_cuota_mensual_10m_36_meses():
    """Regla: convenciones.dinero. Cuota fija de 10.000.000 a 36 meses y 26 % E.A."""
    assert calcular_cuota_mensual(Decimal("10000000"), 36, Decimal("0.26")) == Decimal("388846")


def test_cuota_mensual_1m_6_meses():
    """Regla: convenciones.dinero. Cuota fija de 1.000.000 a 6 meses y 26 % E.A."""
    assert calcular_cuota_mensual(Decimal("1000000"), 6, Decimal("0.26")) == Decimal("178192")


def test_cuota_mensual_100m_72_meses():
    """Regla: convenciones.dinero. Cuota fija de 100.000.000 a 72 meses y 26 % E.A."""
    assert calcular_cuota_mensual(Decimal("100000000"), 72, Decimal("0.26")) == Decimal("2592471")


def test_cuota_mensual_redondeo_solo_al_final():
    """Regla: convenciones.dinero. Se redondea solo la cuota final; redondear la tasa antes daría 262.562.

    Valor esperado calculado aparte: 262.699.
    """
    assert calcular_cuota_mensual(Decimal("5000000"), 24, Decimal("0.26")) == Decimal("262699")


def test_costo_total_10m_36_meses():
    """Regla: convenciones.dinero. Costo total = cuota redondeada por el plazo (S-02, S-03)."""
    assert calcular_costo_total(Decimal("10000000"), 36, Decimal("0.26")) == Decimal("13998456")


def test_costo_total_1m_6_meses():
    """Regla: convenciones.dinero. Costo total = cuota redondeada por el plazo (S-02, S-03)."""
    assert calcular_costo_total(Decimal("1000000"), 6, Decimal("0.26")) == Decimal("1069152")


def test_endeudamiento_22_2_por_ciento_le_alcanza():
    """Regla: productos.credito_consumo.endeudamiento_maximo. (388.846 + 500.000) / 4.000.000 = 22,2 %."""
    endeudamiento = calcular_endeudamiento(Decimal("388846"), Decimal("500000"), Decimal("4000000"))
    assert endeudamiento.quantize(Decimal("0.001")) == Decimal("0.222")


def test_endeudamiento_52_6_por_ciento_no_le_alcanza():
    """Regla: productos.credito_consumo.endeudamiento_maximo. (388.846 + 400.000) / 1.500.000 = 52,6 %."""
    endeudamiento = calcular_endeudamiento(Decimal("388846"), Decimal("400000"), Decimal("1500000"))
    assert endeudamiento.quantize(Decimal("0.001")) == Decimal("0.526")


def test_endeudamiento_ingresos_cero_no_calcula():
    """Regla: productos.credito_consumo.endeudamiento_maximo. Sin ingresos no hay división: no calcula."""
    assert calcular_endeudamiento(Decimal("388846"), Decimal("400000"), Decimal("0")) is None
