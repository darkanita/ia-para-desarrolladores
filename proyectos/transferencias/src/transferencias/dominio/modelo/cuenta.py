"""Cuenta de depósito (ahorros o corriente)."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class TipoCuenta(str, Enum):
    AHORROS = "AHORROS"
    CORRIENTE = "CORRIENTE"


class EstadoCuenta(str, Enum):
    ACTIVA = "ACTIVA"
    BLOQUEADA = "BLOQUEADA"
    CANCELADA = "CANCELADA"


@dataclass
class Cuenta:
    numero: str
    titular_id: str
    tipo: TipoCuenta
    saldo: Decimal
    estado: EstadoCuenta = EstadoCuenta.ACTIVA
    exenta_gmf: bool = False

    def puede_debitar(self, monto: Decimal) -> bool:
        return self.estado is EstadoCuenta.ACTIVA and self.saldo >= monto

    def debitar(self, monto: Decimal) -> None:
        self.saldo -= monto

    def acreditar(self, monto: Decimal) -> None:
        self.saldo += monto
