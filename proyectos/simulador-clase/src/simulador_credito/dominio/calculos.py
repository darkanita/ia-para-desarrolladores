"""Cálculos de tasa y cuota fija del crédito de consumo. Dinero y tasas en Decimal."""
from decimal import ROUND_HALF_UP, Decimal, localcontext

PRECISION_CALCULO = 50
UN_PESO = Decimal("1")


def calcular_tasa_mensual(tasa_ea: Decimal) -> Decimal:
    """Tasa mensual equivalente a una tasa efectiva anual: (1 + ea)^(1/12) - 1."""
    with localcontext() as contexto:
        contexto.prec = PRECISION_CALCULO
        return (1 + tasa_ea) ** (Decimal(1) / Decimal(12)) - 1


def calcular_cuota_mensual(monto: Decimal, plazo_meses: int, tasa_ea: Decimal) -> Decimal:
    """Cuota fija mensual en pesos enteros. Sin redondeos intermedios; redondeo ROUND_HALF_UP al final."""
    with localcontext() as contexto:
        contexto.prec = PRECISION_CALCULO
        i = calcular_tasa_mensual(tasa_ea)
        cuota_exacta = monto * i / (1 - (1 + i) ** (-plazo_meses))
    return cuota_exacta.quantize(UN_PESO, rounding=ROUND_HALF_UP)


def calcular_costo_total(monto: Decimal, plazo_meses: int, tasa_ea: Decimal) -> Decimal:
    """Costo total del crédito: la cuota redondeada multiplicada por el plazo, sin cargos adicionales (S-02, S-03)."""
    return calcular_cuota_mensual(monto, plazo_meses, tasa_ea) * plazo_meses


def calcular_endeudamiento(cuota: Decimal, otras_cuotas: Decimal, ingresos: Decimal) -> Decimal | None:
    """Endeudamiento: (cuota nueva + otras cuotas) / ingresos. Devuelve None si no hay ingresos positivos."""
    if ingresos <= 0:
        return None
    return (cuota + otras_cuotas) / ingresos
