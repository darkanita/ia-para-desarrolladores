"""Copia al material del curso la aplicación que generó un asistente.

Uso:
    python proyectos/guardar_resultado.py ORIGEN DESTINO

Ejemplo (desde la carpeta del curso):
    python proyectos/guardar_resultado.py "%USERPROFILE%/Downloads/app-copilot" sesion-01/resultados/simulador-copilot

Copia todo menos el historial de git, entornos virtuales y cachés. Reemplaza el contenido
de DESTINO (salvo su README.md si el origen no trae uno). Solo usa la librería estándar.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

IGNORAR = shutil.ignore_patterns(".git", ".venv", "venv", "__pycache__", ".pytest_cache", "*.egg-info", ".streamlit/secrets.toml")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("origen", type=Path)
    p.add_argument("destino", type=Path)
    args = p.parse_args()
    origen, destino = args.origen.expanduser().resolve(), args.destino.resolve()
    if not (origen / "REQUISITOS.md").exists():
        print(f"{origen} no parece una app del curso (falta REQUISITOS.md).", file=sys.stderr)
        return 1
    if destino.exists():
        shutil.rmtree(destino)
    shutil.copytree(origen, destino, ignore=IGNORAR)
    archivos = sum(1 for f in destino.rglob("*") if f.is_file())
    print(f"Guardado en {destino} ({archivos} archivos). Revise con: git status")
    return 0


if __name__ == "__main__":
    sys.exit(main())
