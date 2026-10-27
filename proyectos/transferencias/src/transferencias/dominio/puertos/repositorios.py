"""Puertos: lo que el dominio necesita del mundo exterior, sin saber cómo se implementa."""
from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Protocol

from transferencias.dominio.modelo.cuenta import Cuenta
from transferencias.dominio.modelo.transferencia import Transferencia


class RepositorioCuentas(Protocol):
    def obtener(self, numero: str) -> Cuenta | None: ...
    def guardar(self, cuenta: Cuenta) -> None: ...


class RepositorioTransferencias(Protocol):
    def registrar(self, transferencia: Transferencia) -> None: ...
    def total_debitado_en(self, cuenta: str, dia: date) -> Decimal: ...
    def de_cuenta(self, cuenta: str) -> list[Transferencia]: ...


class Notificador(Protocol):
    def transferencia_realizada(self, transferencia: Transferencia) -> None: ...
