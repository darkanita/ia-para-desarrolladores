"""Caso de uso: extracto de transferencias de una cuenta."""
from __future__ import annotations

from transferencias.dominio.modelo.errores import CuentaNoEncontrada
from transferencias.dominio.modelo.transferencia import Transferencia
from transferencias.dominio.puertos.repositorios import RepositorioCuentas, RepositorioTransferencias


class ConsultarMovimientos:
    def __init__(self, cuentas: RepositorioCuentas, transferencias: RepositorioTransferencias) -> None:
        self._cuentas = cuentas
        self._transferencias = transferencias

    def ejecutar(self, cuenta: str, ultimos: int = 10) -> list[Transferencia]:
        if self._cuentas.obtener(cuenta) is None:
            raise CuentaNoEncontrada(cuenta)
        movimientos = sorted(self._transferencias.de_cuenta(cuenta), key=lambda t: t.fecha, reverse=True)
        return movimientos[:ultimos]
