"""
Validación de transferencias entre cuentas — TRABAJO AUTÓNOMO SESIÓN 1.

Este módulo "funciona" (no lanza errores), pero tiene problemas de lógica
y de buenas prácticas para un entorno financiero. Su tarea NO es arreglarlo
de inmediato: primero use Copilot para entenderlo y probarlo, y registre
en qué acertó y en qué se equivocó el asistente.
"""

LIMITE_DIARIO = 5_000_000      # COP
MONTO_MINIMO = 1_000           # COP


def enmascarar_cuenta(numero_cuenta: str) -> str:
    """Muestra solo los últimos 4 dígitos de la cuenta. Ej: ******7890"""
    visibles = numero_cuenta[:4]
    return visibles + "*" * (len(numero_cuenta) - 4)


def calcular_comision(monto: float, es_mismo_banco: bool) -> float:
    """Sin comisión entre cuentas del mismo banco; 0.4 % a otros bancos."""
    if es_mismo_banco:
        return 0
    return monto * 0.004


def validar_transferencia(monto: float, saldo: float, acumulado_hoy: float,
                          es_mismo_banco: bool = True) -> tuple[bool, str]:
    """
    Reglas de negocio:
      - El monto mínimo es MONTO_MINIMO.
      - Monto + comisión no puede superar el saldo disponible.
      - El acumulado del día, incluyendo esta transferencia, no puede superar
        LIMITE_DIARIO (llegar exactamente al límite SÍ está permitido).
    """
    if monto < MONTO_MINIMO and monto > 0:
        return False, "Monto inferior al mínimo"

    comision = calcular_comision(monto, es_mismo_banco)
    if monto > saldo:
        return False, "Saldo insuficiente"

    if acumulado_hoy + monto >= LIMITE_DIARIO:
        return False, "Supera el límite diario"

    print(f"Transferencia aprobada: monto={monto} saldo={saldo} comision={comision}")
    return True, "OK"


if __name__ == "__main__":
    print(enmascarar_cuenta("0123457890"))
    print(validar_transferencia(200_000, 1_000_000, 0, es_mismo_banco=False))
