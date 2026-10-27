from decimal import Decimal

import pytest

from transferencias.dominio.modelo.errores import (
    CuentaNoActiva, CuentaNoEncontrada, FondosInsuficientes, LimiteDiarioExcedido, MontoInvalido,
)


def test_transferencia_exenta_no_cobra_gmf(caso, cuentas):
    tr = caso.ejecutar("A1", "B1", Decimal("100000"))
    assert tr.gmf == 0
    assert cuentas.obtener("A1").saldo == Decimal("900000")
    assert cuentas.obtener("B1").saldo == Decimal("150000")


def test_cuenta_no_exenta_paga_cuatro_por_mil(caso, cuentas):
    tr = caso.ejecutar("A2", "B1", Decimal("1000000"))
    assert tr.gmf == Decimal("4000")
    assert cuentas.obtener("A2").saldo == Decimal("18996000")


def test_notifica_y_registra(caso, historial, notificador):
    tr = caso.ejecutar("A1", "B1", Decimal("5000"))
    assert historial.lista == [tr]
    assert notificador.enviadas == [tr]


@pytest.mark.parametrize("monto", [Decimal("0"), Decimal("-5000"), Decimal("999")])
def test_monto_por_debajo_del_minimo(caso, monto):
    with pytest.raises(MontoInvalido):
        caso.ejecutar("A1", "B1", monto)


def test_misma_cuenta(caso):
    with pytest.raises(MontoInvalido):
        caso.ejecutar("A1", "A1", Decimal("5000"))


def test_cuenta_inexistente(caso):
    with pytest.raises(CuentaNoEncontrada):
        caso.ejecutar("A1", "ZZ", Decimal("5000"))


def test_destino_bloqueado(caso):
    with pytest.raises(CuentaNoActiva):
        caso.ejecutar("A1", "X1", Decimal("5000"))


def test_origen_bloqueado(caso):
    with pytest.raises(CuentaNoActiva):
        caso.ejecutar("X1", "A1", Decimal("5000"))


def test_fondos_insuficientes_incluye_gmf(caso):
    # B1 tiene 50.000: 50.000 + GMF (200) no alcanza.
    with pytest.raises(FondosInsuficientes):
        caso.ejecutar("B1", "A1", Decimal("50000"))


def test_limite_diario(caso):
    caso.ejecutar("A2", "B1", Decimal("6000000"))
    with pytest.raises(LimiteDiarioExcedido):
        caso.ejecutar("A2", "B1", Decimal("5000000"))
