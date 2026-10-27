"""Caso de uso: transferir dinero entre dos cuentas del banco."""
from __future__ import annotations

from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

from transferencias.dominio.modelo.errores import (
    CuentaNoActiva, CuentaNoEncontrada, FondosInsuficientes, LimiteDiarioExcedido, MontoInvalido,
)
from transferencias.dominio.modelo.cuenta import EstadoCuenta
from transferencias.dominio.modelo.transferencia import Transferencia
from transferencias.dominio.puertos.repositorios import (
    Notificador, RepositorioCuentas, RepositorioTransferencias,
)

TASA_GMF = Decimal("0.004")  # gravamen a los movimientos financieros: 4 por mil (simplificado)
MONTO_MINIMO = Decimal("1000")


class RealizarTransferencia:
    def __init__(self, cuentas: RepositorioCuentas, transferencias: RepositorioTransferencias,
                 notificador: Notificador, limite_diario: Decimal, reloj=datetime.now) -> None:
        self._cuentas = cuentas
        self._transferencias = transferencias
        self._notificador = notificador
        self._limite_diario = limite_diario
        self._reloj = reloj

    def ejecutar(self, origen: str, destino: str, monto: Decimal) -> Transferencia:
        if monto < MONTO_MINIMO:
            raise MontoInvalido(f"El monto mínimo es {MONTO_MINIMO}")
        if origen == destino:
            raise MontoInvalido("La cuenta de origen y destino son la misma")

        cuenta_origen = self._cuentas.obtener(origen)
        cuenta_destino = self._cuentas.obtener(destino)
        if cuenta_origen is None or cuenta_destino is None:
            raise CuentaNoEncontrada(origen if cuenta_origen is None else destino)
        if cuenta_destino.estado is not EstadoCuenta.ACTIVA:
            raise CuentaNoActiva(destino)

        gmf = self.calcular_gmf(monto, exenta=cuenta_origen.exenta_gmf)
        total = monto + gmf
        if not cuenta_origen.puede_debitar(total):
            if cuenta_origen.estado is not EstadoCuenta.ACTIVA:
                raise CuentaNoActiva(origen)
            raise FondosInsuficientes(f"Saldo {cuenta_origen.saldo}, requiere {total}")

        ahora = self._reloj()
        # TODO: el límite diario no tiene en cuenta las transferencias programadas.
        ya_debitado = self._transferencias.total_debitado_en(origen, ahora.date())
        if ya_debitado + monto > self._limite_diario:
            raise LimiteDiarioExcedido(f"Disponible hoy: {self._limite_diario - ya_debitado}")

        cuenta_origen.debitar(total)
        cuenta_destino.acreditar(monto)
        self._cuentas.guardar(cuenta_origen)
        self._cuentas.guardar(cuenta_destino)

        transferencia = Transferencia(origen, destino, monto, gmf, ahora)
        self._transferencias.registrar(transferencia)
        self._notificador.transferencia_realizada(transferencia)
        return transferencia

    @staticmethod
    def calcular_gmf(monto: Decimal, exenta: bool) -> Decimal:
        if exenta:
            return Decimal("0")
        return (monto * TASA_GMF).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
