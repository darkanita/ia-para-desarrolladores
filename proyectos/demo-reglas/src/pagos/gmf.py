"""Gravamen a los movimientos financieros (GMF) de una transferencia.

Reglas en banco.yaml: productos.transferencias.gmf, monto_minimo y limite_diario.
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

TASA_GMF = Decimal("0.004")          # 4 por mil
MONTO_MINIMO = Decimal("1000")
LIMITE_DIARIO = Decimal("10000000")


class MontoInvalido(ValueError):
    """El monto no cumple las reglas de transferencias del banco."""


def validar_monto(monto: Decimal, transferido_hoy: Decimal = Decimal("0")) -> None:
    """Rechaza montos por debajo del mínimo o que superan el límite diario."""
    if not isinstance(monto, Decimal):
        raise MontoInvalido("El monto debe ser Decimal")
    if monto < MONTO_MINIMO:
        raise MontoInvalido(f"El monto mínimo es {MONTO_MINIMO}")
    if transferido_hoy + monto > LIMITE_DIARIO:
        raise MontoInvalido(f"Supera el límite diario de {LIMITE_DIARIO}")


def calcular_gmf(monto: Decimal, cuenta_exenta: bool = False) -> Decimal:
    """GMF de 4 por mil redondeado al peso; cero si la cuenta está exenta."""
    validar_monto(monto)
    if cuenta_exenta:
        return Decimal("0")
    return (monto * TASA_GMF).quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def total_a_debitar(monto: Decimal, cuenta_exenta: bool = False) -> Decimal:
    """Monto más el GMF: lo que sale de la cuenta de origen."""
    return monto + calcular_gmf(monto, cuenta_exenta)
