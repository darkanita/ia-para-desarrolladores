"""Resultado de una transferencia ya aplicada."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import uuid4


@dataclass(frozen=True)
class Transferencia:
    origen: str
    destino: str
    monto: Decimal
    gmf: Decimal
    fecha: datetime
    referencia: str = field(default_factory=lambda: uuid4().hex[:12].upper())

    @property
    def total_debitado(self) -> Decimal:
        return self.monto + self.gmf
