"""Laboratorio S1 — Guardián de prompts.

Antes de enviar código a un LLM (Copilot Chat, una API, un agente) en un banco,
necesitamos responder tres preguntas:

  1. ¿Cuántos tokens es y cuánto cuesta?
  2. ¿Lleva datos sensibles que no deben salir de nuestro entorno?
  3. ¿Cabe en el presupuesto de contexto?

Implementa las funciones marcadas con TODO usando GitHub Copilot.
El laboratorio termina cuando `pytest sesion-01/laboratorio/tests -q` pasa completo.
Lee las reglas exactas en ENUNCIADO.md.
"""
from __future__ import annotations

try:  # Tokenizador real si está disponible; si no, usa la aproximación.
    import tiktoken

    _ENC = tiktoken.get_encoding("o200k_base")
except Exception:
    _ENC = None


class ContextoExcedidoError(ValueError):
    """El texto no cabe en el presupuesto de tokens."""


# ---------------------------------------------------------------- Parte 1
def contar_tokens(texto: str) -> int:
    """Cuenta los tokens de `texto`.

    - Texto vacío → 0.
    - Si `_ENC` existe, usa `_ENC.encode`.
    - Si no, aproxima con ceil(len(texto) / 4).
    """
    # TODO
    raise NotImplementedError


def estimar_costo_usd(
    tokens_entrada: int,
    tokens_salida: int,
    precio_entrada_1m: float,
    precio_salida_1m: float,
) -> float:
    """Costo en USD de una llamada. Los precios son por millón de tokens.

    - Lanza ValueError si algún valor es negativo.
    - Redondea a 6 decimales.
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------- Parte 2
def es_luhn_valido(numero: str) -> bool:
    """True si los dígitos de `numero` (se ignoran espacios y guiones) pasan el algoritmo de Luhn."""
    # TODO
    raise NotImplementedError


def redactar_datos_sensibles(texto: str) -> tuple[str, dict[str, int]]:
    """Reemplaza datos sensibles por etiquetas y cuenta cuántos encontró.

    Devuelve (texto_redactado, {"EMAIL": n, "TARJETA": n, "CEDULA": n, "SECRETO": n}).
    Las reglas de cada etiqueta están en ENUNCIADO.md.
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------- Parte 3
def preparar_contexto(
    codigo: str,
    max_tokens: int,
    recortar: bool = False,
    precio_entrada_1m: float = 2.50,
) -> dict:
    """Redacta, cuenta y valida el presupuesto de `codigo`.

    Devuelve {"texto", "tokens", "costo_usd", "hallazgos", "recortado"}.
    Ver ENUNCIADO.md para el comportamiento cuando se excede `max_tokens`.
    """
    # TODO
    raise NotImplementedError
