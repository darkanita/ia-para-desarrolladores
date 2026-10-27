from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from transferencias.dominio.casos_uso.consultar_movimientos import ConsultarMovimientos
from transferencias.dominio.modelo.errores import CuentaNoEncontrada
from transferencias.dominio.modelo.transferencia import Transferencia


def test_ordena_del_mas_reciente_al_mas_antiguo(cuentas, historial):
    base = datetime(2026, 10, 1)
    for i in range(3):
        historial.registrar(Transferencia("A1", "B1", Decimal(1000 * (i + 1)), Decimal("0"), base + timedelta(days=i)))
    movimientos = ConsultarMovimientos(cuentas, historial).ejecutar("B1", ultimos=2)
    assert [m.monto for m in movimientos] == [Decimal("3000"), Decimal("2000")]


def test_cuenta_inexistente(cuentas, historial):
    with pytest.raises(CuentaNoEncontrada):
        ConsultarMovimientos(cuentas, historial).ejecutar("ZZ")
