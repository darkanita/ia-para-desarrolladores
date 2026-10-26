"""
Tabla de amortización de crédito de consumo (sistema francés, cuota fija).
"""


def tasa_mensual(tasa_ea: float) -> float:
    """Convierte la tasa efectiva anual (E.A.) del crédito a tasa mensual."""
    return tasa_ea / 12


def cuota_fija(monto: float, tasa_ea: float, meses: int) -> float:
    """Cuota mensual fija del sistema francés."""
    i = tasa_mensual(tasa_ea)
    return monto * i / (1 - (1 + i) ** -meses)


def tabla_amortizacion(monto: float, tasa_ea: float, meses: int) -> list[dict]:
    """Devuelve una fila por mes con cuota, interés, abono a capital y saldo."""
    i = tasa_mensual(tasa_ea)
    cuota = round(cuota_fija(monto, tasa_ea, meses), 2)
    saldo = monto
    filas = []
    for mes in range(1, meses + 1):
        interes = round(saldo * i, 2)
        capital = round(cuota - interes, 2)
        saldo = round(saldo - capital, 2)
        filas.append({"mes": mes, "cuota": cuota, "interes": interes,
                      "capital": capital, "saldo": saldo})
    return filas


if __name__ == "__main__":
    for fila in tabla_amortizacion(10_000_000, 0.24, 12):
        print(fila)
