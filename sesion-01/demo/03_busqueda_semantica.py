"""Demo 3 — Embeddings: convertir código en vectores y buscar por significado.

Un embedding es un vector que representa un texto. Textos parecidos quedan
cerca (alta similitud coseno). Así funcionan la búsqueda semántica de código,
el RAG y parte del contexto que un asistente como Copilot recupera.

Aquí construimos un embedding sencillo y 100 % local (TF-IDF sobre las
palabras de identificadores y docstrings). Un modelo de embeddings real
(lo usaremos en la sesión 2) captura sinónimos y semántica mucho mejor.

Ejecutar:  python sesion-01/demo/03_busqueda_semantica.py
"""
from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter

import numpy as np

# Pequeño "repositorio" de funciones de un sistema bancario ficticio.
FUNCIONES = {
    "validar_digito_verificacion": "Valida el dígito de verificación de un número de cuenta.",
    "calcular_interes_mensual": "Convierte la tasa efectiva anual a mensual y calcula el interés del saldo.",
    "registrar_transferencia": "Registra una transferencia entre dos cuentas y descuenta el monto del saldo.",
    "enmascarar_tarjeta": "Oculta los dígitos de una tarjeta y deja visibles los últimos cuatro.",
    "generar_extracto_pdf": "Genera el extracto mensual de movimientos del cliente en PDF.",
    "detectar_fraude_por_monto": "Marca transacciones con monto atípico respecto al historial del cliente.",
    "actualizarDatosContacto": "Actualiza correo electrónico y teléfono del cliente.",
}

PALABRAS_VACIAS = {"de", "del", "la", "el", "los", "las", "un", "una", "y", "a", "al", "en", "entre", "con", "por", "que", "respecto"}


def partir_identificador(nombre: str) -> list[str]:
    """snake_case y camelCase → palabras: 'actualizarDatosContacto' → ['actualizar', 'datos', 'contacto']."""
    nombre = re.sub(r"([a-z])([A-Z])", r"\1_\2", nombre)
    return [sin_tildes(p.lower()) for p in nombre.split("_") if p]


def sin_tildes(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def normalizar(texto: str) -> list[str]:
    palabras = re.findall(r"[a-z]+", sin_tildes(texto.lower()))
    return [p for p in palabras if p not in PALABRAS_VACIAS]


def documentos() -> dict[str, list[str]]:
    return {n: partir_identificador(n) + normalizar(d) for n, d in FUNCIONES.items()}


def construir_vocabulario(docs: dict[str, list[str]]) -> tuple[list[str], dict[str, float]]:
    vocab = sorted({p for palabras in docs.values() for p in palabras})
    n = len(docs)
    df = Counter(p for palabras in docs.values() for p in set(palabras))
    idf = {p: math.log((1 + n) / (1 + df[p])) + 1 for p in vocab}
    return vocab, idf


def embedding(palabras: list[str], vocab: list[str], idf: dict[str, float]) -> np.ndarray:
    tf = Counter(palabras)
    v = np.array([tf[p] * idf[p] for p in vocab], dtype=float)
    norma = np.linalg.norm(v)
    return v / norma if norma else v


def buscar(consulta: str, top: int = 3) -> list[tuple[str, float]]:
    docs = documentos()
    vocab, idf = construir_vocabulario(docs)
    q = embedding(normalizar(consulta), vocab, idf)
    puntajes = {n: float(embedding(p, vocab, idf) @ q) for n, p in docs.items()}
    return sorted(puntajes.items(), key=lambda kv: kv[1], reverse=True)[:top]


def main() -> None:
    consultas = [
        "ocultar número de tarjeta",
        "interés de la cuenta de ahorros",
        "cambiar el correo del cliente",
        "transacción sospechosa",  # sinónimo de fraude: aquí falla, un embedding real no
    ]
    for c in consultas:
        print(f"\nConsulta: '{c}'")
        for nombre, sim in buscar(c):
            barra = "█" * int(sim * 30)
            print(f"  {sim:5.2f} {barra:<30} {nombre}")
    print("\nObserva la última consulta: sin coincidencia de palabras no hay similitud.")
    print("Los embeddings de un LLM resuelven eso porque aprenden significado, no solo palabras.")


if __name__ == "__main__":
    main()
