"""Conversión de los textos que digita el asesor a Decimal. Valida formato; no valida reglas del banco."""
import re
from decimal import Decimal


class ErrorEntrada(Exception):
    """Entrada que no se puede convertir. El mensaje es el que ve el asesor."""

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje


MENSAJE_NUMERO = "Revise este campo: debe ser un número."
MENSAJE_PLAZO = "El plazo debe ser un número entero de meses."
MENSAJE_TASA = "Indique la tasa efectiva anual, por ejemplo 26 %."


def convertir_decimal(texto: str, campo: str) -> Decimal:
    """Convierte el texto del campo a Decimal. Coma o punto como separador decimal; el plazo debe ser entero."""
    limpio = texto.strip()
    if campo == "tasa":
        return _convertir_tasa(limpio)
    if campo == "otras_cuotas" and limpio == "":
        raise ErrorEntrada("Indique las otras cuotas del cliente, o 0 si no tiene.")
    if not re.fullmatch(r"-?\d+([.,]\d+)?", limpio):
        raise ErrorEntrada(MENSAJE_NUMERO)
    valor = Decimal(limpio.replace(",", "."))
    if campo == "plazo" and valor != valor.to_integral_value():
        raise ErrorEntrada(MENSAJE_PLAZO)
    return valor


def _convertir_tasa(limpio: str) -> Decimal:
    """Tasa E.A. como fracción. Acepta 26, 26 % o 26,5 %. Sin % solo se acepta de 1 a 100 (no leer 0,26 como 0,26 %)."""
    con_porcentaje = limpio.endswith("%")
    numero = limpio[:-1].strip() if con_porcentaje else limpio
    if not re.fullmatch(r"\d+([.,]\d+)?", numero):
        raise ErrorEntrada(MENSAJE_TASA)
    valor = Decimal(numero.replace(",", "."))
    if valor <= 0 or valor > 100 or (not con_porcentaje and valor < 1):
        raise ErrorEntrada(MENSAJE_TASA)
    return valor / 100
