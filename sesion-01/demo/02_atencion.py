"""Demo 2 — Auto-atención (self-attention) en 30 líneas de NumPy.

Es la operación central del transformer:

    Atención(Q, K, V) = softmax(Q · Kᵀ / √d) · V

Cada token produce una consulta (Q), una llave (K) y un valor (V). La matriz
softmax(Q·Kᵀ/√d) dice cuánto "mira" cada token a los demás.

Los vectores aquí son de juguete y están elegidos a mano para que el resultado
sea legible; en un modelo real tienen miles de dimensiones y se aprenden.

Ejecutar:  python sesion-01/demo/02_atencion.py
"""
from __future__ import annotations

import numpy as np

TOKENS = ["saldo", "=", "cuenta", ".", "saldo", "-", "monto"]

# Embeddings de juguete (d=4), escalados ×3 para que la atención sea más nítida. Dimensiones aproximadas:
# [es-dinero, es-operador, es-objeto, es-variable]
EMBEDDINGS = 3 * np.array(
    [
        [0.9, 0.0, 0.1, 0.8],  # saldo
        [0.0, 1.0, 0.0, 0.0],  # =
        [0.6, 0.0, 0.9, 0.3],  # cuenta
        [0.0, 0.9, 0.1, 0.0],  # .
        [0.9, 0.0, 0.1, 0.8],  # saldo
        [0.0, 1.0, 0.0, 0.0],  # -
        [0.8, 0.0, 0.0, 0.9],  # monto
    ]
)

rng = np.random.default_rng(seed=7)
D = EMBEDDINGS.shape[1]
# Proyecciones: en un modelo real se aprenden. Aquí, identidad + un poco de ruido.
W_Q = np.eye(D) + 0.05 * rng.standard_normal((D, D))
W_K = np.eye(D) + 0.05 * rng.standard_normal((D, D))
W_V = np.eye(D)


def softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - x.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def auto_atencion(x: np.ndarray, causal: bool = True) -> tuple[np.ndarray, np.ndarray]:
    q, k, v = x @ W_Q, x @ W_K, x @ W_V
    puntajes = q @ k.T / np.sqrt(D)
    if causal:  # un modelo generativo no puede mirar tokens futuros
        mascara = np.triu(np.ones_like(puntajes, dtype=bool), k=1)
        puntajes = np.where(mascara, -np.inf, puntajes)
    pesos = softmax(puntajes)
    return pesos @ v, pesos


def imprimir_matriz(pesos: np.ndarray) -> None:
    ancho = 8
    print(" " * ancho + "".join(f"{t:>{ancho}}" for t in TOKENS))
    for t, fila in zip(TOKENS, pesos):
        celdas = "".join(f"{p:>{ancho}.2f}" if p > 0.005 else f"{'·':>{ancho}}" for p in fila)
        print(f"{t:>{ancho}}{celdas}")


def main() -> None:
    _, pesos = auto_atencion(EMBEDDINGS)
    print("Matriz de atención causal (fila = token que pregunta, columna = token observado)\n")
    imprimir_matriz(pesos)

    i = TOKENS.index("monto")
    orden = np.argsort(pesos[i])[::-1]
    print(f"\n'{TOKENS[i]}' presta más atención a: ", end="")
    print(", ".join(f"{TOKENS[j]}#{j} ({pesos[i, j]:.0%})" for j in orden[:3]))
    print("\nIdea clave: la atención mezcla información de otros tokens según su relevancia,")
    print("por eso 'monto' toma contexto de 'saldo' e ignora casi por completo a los operadores.")


if __name__ == "__main__":
    main()
