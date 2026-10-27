from datetime import datetime
from decimal import Decimal

import pytest

from transferencias.adaptadores.memoria import CuentasEnMemoria, NotificadorEnMemoria, TransferenciasEnMemoria
from transferencias.dominio.casos_uso.realizar_transferencia import RealizarTransferencia
from transferencias.dominio.modelo.cuenta import Cuenta, EstadoCuenta, TipoCuenta

AHORA = datetime(2026, 10, 27, 10, 0)


@pytest.fixture
def cuentas():
    return CuentasEnMemoria([
        Cuenta("A1", "C1", TipoCuenta.AHORROS, Decimal("1000000"), exenta_gmf=True),
        Cuenta("A2", "C1", TipoCuenta.CORRIENTE, Decimal("20000000")),
        Cuenta("B1", "C2", TipoCuenta.AHORROS, Decimal("50000")),
        Cuenta("X1", "C3", TipoCuenta.AHORROS, Decimal("500000"), estado=EstadoCuenta.BLOQUEADA),
    ])


@pytest.fixture
def historial():
    return TransferenciasEnMemoria()


@pytest.fixture
def notificador():
    return NotificadorEnMemoria()


@pytest.fixture
def caso(cuentas, historial, notificador):
    return RealizarTransferencia(cuentas, historial, notificador, Decimal("10000000"), reloj=lambda: AHORA)
