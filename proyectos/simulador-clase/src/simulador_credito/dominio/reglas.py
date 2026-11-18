"""Reglas del banco para la simulación (RN-01 a RN-05). Los límites llegan como parámetros."""
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


@dataclass(frozen=True)
class MotivoRechazo:
    """Regla incumplida (id, por ejemplo RN-01) y el mensaje que ve el asesor."""

    regla: str
    mensaje: str


def formatear_pesos(valor: Decimal) -> str:
    """Pesos enteros con punto como separador de miles: 1000000 -> 1.000.000."""
    entero = int(valor.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    return f"{entero:,}".replace(",", ".")


def formatear_porcentaje(fraccion: Decimal) -> str:
    """Fracción a porcentaje con coma y máximo un decimal: 0.526 -> 52,6 %; 0.40 -> 40 %."""
    valor = (fraccion * 100).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    if valor == valor.to_integral_value():
        texto = str(int(valor))
    else:
        texto = str(valor).replace(".", ",")
    return f"{texto} %"


def validar_monto(monto: Decimal, minimo: Decimal, maximo: Decimal) -> MotivoRechazo | None:
    """RN-01 y RN-02: el monto debe estar entre el mínimo y el máximo, ambos incluidos."""
    if monto < minimo:
        return MotivoRechazo("RN-01", f"El monto mínimo es {formatear_pesos(minimo)} COP.")
    if monto > maximo:
        return MotivoRechazo("RN-02", f"El monto máximo es {formatear_pesos(maximo)} COP.")
    return None


def validar_plazo(plazo: int, minimo: int, maximo: int) -> MotivoRechazo | None:
    """RN-03: el plazo en meses debe estar entre el mínimo y el máximo, ambos incluidos."""
    if plazo < minimo or plazo > maximo:
        return MotivoRechazo("RN-03", f"El plazo debe estar entre {minimo} y {maximo} meses.")
    return None


def validar_tasa(tasa: Decimal, maxima: Decimal) -> MotivoRechazo | None:
    """RN-04: la tasa efectiva anual no puede superar la tasa máxima del producto."""
    if tasa > maxima:
        return MotivoRechazo("RN-04", f"La tasa máxima permitida es {formatear_porcentaje(maxima)} E.A.")
    return None


def validar_endeudamiento(endeudamiento: Decimal, maximo: Decimal) -> MotivoRechazo | None:
    """RN-05: el endeudamiento no puede superar el máximo del producto."""
    if endeudamiento > maximo:
        return MotivoRechazo(
            "RN-05",
            f"El endeudamiento de {formatear_porcentaje(endeudamiento)} supera el máximo permitido de "
            f"{formatear_porcentaje(maximo)}.",
        )
    return None


def validar_ingresos(ingresos: Decimal) -> MotivoRechazo | None:
    """RF-03: sin ingresos positivos no hay endeudamiento que calcular."""
    if ingresos <= 0:
        return MotivoRechazo("RF-03", "Los ingresos deben ser mayores que cero.")
    return None
