"""Configuración leída de variables de entorno, con valores por defecto para desarrollo."""
from __future__ import annotations

import os
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Config:
    archivo_cuentas: Path
    archivo_transferencias: Path
    limite_diario: Decimal


def cargar() -> Config:
    return Config(
        archivo_cuentas=Path(os.getenv("TRANSFERENCIAS_CUENTAS", RAIZ / "datos" / "cuentas.json")),
        archivo_transferencias=Path(os.getenv("TRANSFERENCIAS_HISTORIAL", RAIZ / "datos" / "historial.json")),
        limite_diario=Decimal(os.getenv("TRANSFERENCIAS_LIMITE_DIARIO", "10000000")),
    )
