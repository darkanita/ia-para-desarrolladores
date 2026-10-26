"""Acceso a un tokenizador real (tiktoken) con respaldo aproximado sin red.

tiktoken descarga su vocabulario la primera vez. En redes corporativas esa
descarga puede estar bloqueada; en ese caso se usa un tokenizador ilustrativo
que parte el texto en trozos parecidos a los de un BPE real.
"""
from __future__ import annotations

import re

_ENCODING = None
ES_REAL = False

try:  # pragma: no cover - depende de la red
    import tiktoken

    _ENCODING = tiktoken.get_encoding("o200k_base")  # vocabulario de GPT-4o
    ES_REAL = True
except Exception:  # sin paquete o sin red
    _ENCODING = None

# Palabras cortas o espacios + palabra, números de hasta 3 dígitos, símbolos sueltos.
_PATRON = re.compile(r" ?[A-Za-zÁÉÍÓÚáéíóúÑñ]{1,4}| ?\d{1,3}| ?[^\sA-Za-zÁÉÍÓÚáéíóúÑñ\d]|\s+")


def tokenizar(texto: str) -> list[str]:
    """Devuelve la lista de tokens (como texto) en que se divide `texto`."""
    if _ENCODING is not None:
        return [_ENCODING.decode([t]) for t in _ENCODING.encode(texto)]
    return _PATRON.findall(texto)


def contar(texto: str) -> int:
    """Número de tokens de `texto`."""
    if _ENCODING is not None:
        return len(_ENCODING.encode(texto))
    return len(_PATRON.findall(texto))


def aviso() -> str:
    return (
        "Tokenizador: tiktoken o200k_base (real)"
        if ES_REAL
        else "Tokenizador: APROXIMADO (tiktoken no pudo descargar su vocabulario)"
    )
