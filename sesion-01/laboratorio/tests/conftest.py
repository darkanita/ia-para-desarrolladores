"""Hace importable `guardian_prompt`.

Por defecto se prueba la versión del laboratorio. Para probar la solución de referencia:
    GUARDIAN_SOLUCION=1 pytest sesion-01/laboratorio/tests -q
"""
import os
import sys
from pathlib import Path

base = Path(__file__).resolve().parents[2]
carpeta = "solucion" if os.getenv("GUARDIAN_SOLUCION") else "laboratorio"
sys.path.insert(0, str(base / carpeta))
