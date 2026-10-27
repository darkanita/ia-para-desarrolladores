"""Crea un repositorio git de práctica a partir de un proyecto de esta carpeta.

Uso:
    python proyectos/crear_repositorio.py DESTINO [--proyecto transferencias]

Copia el proyecto en DESTINO (que no debe existir), hace `git init` y arma un
historial corto de commits, como si el equipo lo hubiera construido por partes.
Así los asistentes pueden leer también el historial (`git log`, `git blame`).
Solo usa la librería estándar y git.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
AUTOR = {"GIT_AUTHOR_NAME": "Equipo Pagos", "GIT_AUTHOR_EMAIL": "pagos@ejemplo.com",
         "GIT_COMMITTER_NAME": "Equipo Pagos", "GIT_COMMITTER_EMAIL": "pagos@ejemplo.com"}

HISTORIAL = {
    "transferencias": [
        ("2026-09-01T09:00:00", "Estructura inicial: modelo de cuenta y puertos del dominio",
         ["pyproject.toml", ".gitignore", "README.md", "src/transferencias/__init__.py",
          "src/transferencias/dominio/__init__.py", "src/transferencias/dominio/modelo",
          "src/transferencias/dominio/puertos"]),
        ("2026-09-08T15:30:00", "Caso de uso: realizar transferencia con GMF y límite diario",
         ["src/transferencias/dominio/casos_uso/__init__.py",
          "src/transferencias/dominio/casos_uso/realizar_transferencia.py",
          "src/transferencias/adaptadores/__init__.py", "src/transferencias/adaptadores/memoria.py",
          "tests/conftest.py", "tests/test_realizar_transferencia.py"]),
        ("2026-09-15T11:10:00", "Caso de uso: consultar movimientos",
         ["src/transferencias/dominio/casos_uso/consultar_movimientos.py", "tests/test_consultar_movimientos.py"]),
        ("2026-09-22T17:45:00", "CLI, repositorios JSON, notificador y datos de ejemplo",
         ["."]),
    ],
    "simulador-credito": [
        ("2026-10-20T09:00:00", "Requisitos del simulador de crédito y reglas del equipo", ["."]),
    ],
}


def git(destino: Path, *args: str, fecha: str | None = None) -> None:
    env = {**os.environ, **AUTOR}
    if fecha:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = fecha
    subprocess.run(["git", *args], cwd=destino, env=env, check=True, capture_output=True, text=True)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("destino", type=Path)
    p.add_argument("--proyecto", default="transferencias", choices=sorted(HISTORIAL))
    args = p.parse_args()

    if shutil.which("git") is None:
        print("No se encontró git. Instálelo (ver preparacion/README.md).", file=sys.stderr)
        return 1
    destino = args.destino.resolve()
    if destino.exists():
        print(f"{destino} ya existe: elija otra carpeta o bórrela.", file=sys.stderr)
        return 1

    shutil.copytree(AQUI / args.proyecto, destino,
                    ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.egg-info"))
    git(destino, "init", "-q", "-b", "main")
    for fecha, mensaje, rutas in HISTORIAL[args.proyecto]:
        git(destino, "add", *rutas)
        git(destino, "commit", "-q", "-m", mensaje, fecha=fecha)
    print(f"Repositorio listo en {destino}")
    print(f"Ábralo con:  code \"{destino}\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
