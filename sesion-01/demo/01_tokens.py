"""Demo 1 — El modelo no lee caracteres ni palabras: lee tokens.

Preguntas que responde:
  * ¿Cómo se parte un fragmento de código en tokens?
  * ¿Cuesta lo mismo escribir en español que en inglés?
  * ¿Cuánto "pesa" un archivo en la ventana de contexto y en la factura?

Ejecutar:  python sesion-01/demo/01_tokens.py
"""
from __future__ import annotations

from tokenizador import aviso, contar, tokenizar

# Precio de entrada de referencia (Claude Sonnet 5.5, lista oficial oct-2026) en USD por millón de tokens.
# Verifícalo el día de la clase. El conteo usa el tokenizador de OpenAI (tiktoken):
# cada proveedor tiene el suyo, así que las cifras son aproximadas para otros modelos.
PRECIO_ENTRADA_USD_1M = 2.00
VENTANA_CONTEXTO = 128_000  # ventana ilustrativa; varía según el modelo y la herramienta

CODIGO = '''def calcular_interes_mensual(saldo: float, tasa_ea: float) -> float:
    """Convierte una tasa efectiva anual a mensual y la aplica al saldo."""
    tasa_mensual = (1 + tasa_ea) ** (1 / 12) - 1
    return round(saldo * tasa_mensual, 2)
'''

COMPARACIONES = {
    "Comentario en español": "# Valida que el número de cuenta tenga el dígito de verificación correcto",
    "Comentario en inglés": "# Validates that the account number has the correct check digit",
    "JSON": '{"cliente": {"id": 1023, "nombre": "Ana", "productos": ["ahorros", "tarjeta"]}}',
    "YAML": "cliente:\n  id: 1023\n  nombre: Ana\n  productos: [ahorros, tarjeta]",
    "Identificador snake_case": "calcular_interes_mensual",
    "Identificador abreviado": "calcIntMens",
}


def mostrar_tokens(texto: str) -> None:
    piezas = tokenizar(texto)
    visibles = " | ".join(p.replace("\n", "⏎") for p in piezas)
    print(f"{len(piezas):>4} tokens  →  {visibles}")


def main() -> None:
    print(aviso(), "\n")

    print("1) Un fragmento de código partido en tokens")
    print("-" * 60)
    for linea in CODIGO.splitlines():
        mostrar_tokens(linea)

    print("\n2) Mismo contenido, distinta forma")
    print("-" * 60)
    for nombre, texto in COMPARACIONES.items():
        print(f"{nombre:<26} {contar(texto):>4} tokens   ({len(texto)} caracteres)")

    print("\n3) ¿Cuánto pesa un archivo en contexto y en costo?")
    print("-" * 60)
    with open(__file__, encoding="utf-8") as f:
        este_archivo = f.read()
    tokens = contar(este_archivo)
    costo = tokens / 1_000_000 * PRECIO_ENTRADA_USD_1M
    print(f"Este archivo: {tokens} tokens")
    print(f"Ocupa {tokens / VENTANA_CONTEXTO:.2%} de una ventana de {VENTANA_CONTEXTO:,} tokens")
    print(f"Enviarlo 1.000 veces cuesta ~USD {costo * 1000:.2f} (a USD {PRECIO_ENTRADA_USD_1M}/1M)")


if __name__ == "__main__":
    main()
