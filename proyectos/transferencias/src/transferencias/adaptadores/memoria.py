"""Repositorios en memoria para las pruebas."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from transferencias.dominio.modelo.cuenta import Cuenta
from transferencias.dominio.modelo.transferencia import Transferencia


class CuentasEnMemoria:
    def __init__(self, cuentas: list[Cuenta]) -> None:
        self._cuentas = {c.numero: c for c in cuentas}

    def obtener(self, numero: str) -> Cuenta | None:
        return self._cuentas.get(numero)

    def guardar(self, cuenta: Cuenta) -> None:
        self._cuentas[cuenta.numero] = cuenta


class TransferenciasEnMemoria:
    def __init__(self) -> None:
        self.lista: list[Transferencia] = []

    def registrar(self, transferencia: Transferencia) -> None:
        self.lista.append(transferencia)

    def total_debitado_en(self, cuenta: str, dia: date) -> Decimal:
        return sum((t.monto for t in self.lista if t.origen == cuenta and t.fecha.date() == dia), Decimal("0"))

    def de_cuenta(self, cuenta: str) -> list[Transferencia]:
        return [t for t in self.lista if cuenta in (t.origen, t.destino)]


class NotificadorEnMemoria:
    def __init__(self) -> None:
        self.enviadas: list[Transferencia] = []

    def transferencia_realizada(self, transferencia: Transferencia) -> None:
        self.enviadas.append(transferencia)
