"""Pruebas de la validación de entradas del asesor en el borde (sección 9 de la especificación)."""
from decimal import Decimal

import pytest

from simulador_credito.dominio.entradas import ErrorEntrada, convertir_decimal


def test_campo_vacio_pide_correccion():
    """Regla: RF-04. Campo obligatorio vacío: no calcula y pide corregir el campo."""
    with pytest.raises(ErrorEntrada) as error:
        convertir_decimal("", "monto")
    assert error.value.mensaje == "Revise este campo: debe ser un número."


def test_campo_no_numerico_pide_correccion():
    """Regla: RF-04. Valor no numérico: no calcula y pide corregir el campo."""
    with pytest.raises(ErrorEntrada) as error:
        convertir_decimal("diez millones", "monto")
    assert error.value.mensaje == "Revise este campo: debe ser un número."


def test_plazo_12_5_meses_rechaza():
    """Regla: sección 9. El plazo debe ser un número entero de meses."""
    with pytest.raises(ErrorEntrada) as error:
        convertir_decimal("12,5", "plazo")
    assert error.value.mensaje == "El plazo debe ser un número entero de meses."


def test_tasa_formato_no_reconocible_pide_tasa():
    """Regla: sección 9. Tasa con formato no reconocible: pide la tasa efectiva anual."""
    with pytest.raises(ErrorEntrada) as error:
        convertir_decimal("veintiséis", "tasa")
    assert error.value.mensaje == "Indique la tasa efectiva anual, por ejemplo 26 %."


def test_otras_cuotas_vacias_pide_dato():
    """Regla: sección 9. Otras cuotas vacías: pide el dato o un 0 confirmado por el asesor."""
    with pytest.raises(ErrorEntrada) as error:
        convertir_decimal("", "otras_cuotas")
    assert error.value.mensaje == "Indique las otras cuotas del cliente, o 0 si no tiene."
