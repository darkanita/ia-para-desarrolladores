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
    "demo-reglas": [
        ("2026-11-03T10:00:00", "Módulo de GMF del equipo de pagos, todavía sin pruebas", ["."]),
    ],
    "plantilla-equipo": [
        ("2026-11-11T09:00:00", "Repositorio del equipo desde la plantilla del curso (agente v3)", ["."]),
    ],
    # Demo de la sesión 5: el repositorio del equipo con el simulador construido hasta el paso 6
    # y una rama de un compañero con el caso de uso, lista para revisar.
    "simulador-equipo": [
        ("2026-10-27T09:00:00", "Repositorio del equipo desde la plantilla del curso",
         [".", ":!src", ":!tests", ":!pyproject.toml", ":!docs/sdlc/simulador-credito"]),
        ("2026-10-29T10:00:00", "Intención del simulador aprobada", ["docs/sdlc/simulador-credito/intent.md"]),
        ("2026-11-04T10:00:00", "Especificación del simulador aprobada", ["docs/sdlc/simulador-credito/spec.md"]),
        ("2026-11-05T10:00:00", "Plan técnico aprobado; pasos 1 a 6 hechos", ["docs/sdlc/simulador-credito/plan.md"]),
        ("2026-11-05T11:00:00", "Primer componente: validación, cuota, total y costo (pasos 1 a 5)",
         ["pyproject.toml", "src", "tests", ":!src/simulador_credito/dominio/capacidad_pago.py",
          ":!src/simulador_credito/dominio/resultado_simulacion.py", ":!src/simulador_credito/puertos/proveedor_parametros.py",
          ":!src/simulador_credito/adaptadores/proveedor_parametros_en_memoria.py",
          ":!src/simulador_credito/casos_uso/simular_credito.py", ":!tests/test_capacidad_pago.py",
          ":!tests/test_simular_credito.py"]),
        ("2026-11-06T16:00:00", "Capacidad de pago (paso 6, RF-04)",
         ["src/simulador_credito/dominio/capacidad_pago.py", "tests/test_capacidad_pago.py"]),
        ("rama", "funcionalidad/simulador-credito-caso-de-uso"),
        ("2026-11-07T15:00:00", "Caso de uso simular_credito con puerto de parámetros (pasos 7 y 8)",
         ["src/simulador_credito/dominio/resultado_simulacion.py", "src/simulador_credito/puertos/proveedor_parametros.py",
          "src/simulador_credito/adaptadores/proveedor_parametros_en_memoria.py",
          "src/simulador_credito/casos_uso/simular_credito.py", "tests/test_simular_credito.py"]),
        ("rama", "main"),
    ],
    # Demo de la sesión 6: el simulador hasta el paso 10, ya corregido y revisado, con la presentación
    # (paso 10) probada a medias. El Verificador debe encontrar lo que falta.
    "simulador-equipo-s6": [
        ("2026-10-27T09:00:00", "Repositorio del equipo desde la plantilla del curso",
         [".", ":!src", ":!tests", ":!pyproject.toml", ":!docs/sdlc/simulador-credito"]),
        ("2026-11-05T10:00:00", "Intención, especificación y plan del simulador aprobados", ["docs/sdlc/simulador-credito"]),
        ("2026-11-09T11:00:00", "Simulador: validación, cuota, capacidad de pago y caso de uso (pasos 1 a 8)",
         ["pyproject.toml", "src", "tests", ":!src/simulador_credito/app/presentacion.py", ":!tests/test_presentacion.py"]),
        ("2026-11-10T16:00:00", "Presentación del resultado para el asesor (paso 10)",
         ["src/simulador_credito/app/presentacion.py", "tests/test_presentacion.py"]),
    ],
}

# Proyectos que se arman sobre otro: se copia primero la base y encima el proyecto.
BASES = {"simulador-equipo": ["plantilla-equipo"], "simulador-equipo-s6": ["plantilla-equipo", "simulador-equipo"]}


def git(destino: Path, *args: str, fecha: str | None = None) -> None:
    env = {**os.environ, **AUTOR}
    if fecha:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = fecha
    subprocess.run(["git", *args], cwd=destino, env=env, check=True, capture_output=True, text=True)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("destino", type=Path)
    p.add_argument("--proyecto", default="transferencias", choices=sorted(k for k in HISTORIAL if (AQUI / k).exists()))
    args = p.parse_args()

    if shutil.which("git") is None:
        print("No se encontró git. Instálelo (ver preparacion/README.md).", file=sys.stderr)
        return 1
    destino = args.destino.resolve()
    if destino.exists():
        print(f"{destino} ya existe: elija otra carpeta o bórrela.", file=sys.stderr)
        return 1

    ignorar = shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.egg-info")
    for capa in [*BASES.get(args.proyecto, []), args.proyecto]:
        shutil.copytree(AQUI / capa, destino, ignore=ignorar, dirs_exist_ok=True)
    configurar = destino / "herramientas" / "configurar_mcp.py"
    if configurar.exists():  # el servidor MCP usará el Python con el que se creó el repositorio
        subprocess.run([sys.executable, str(configurar)], capture_output=True, text=True)
    git(destino, "init", "-q", "-b", "main")
    for paso in HISTORIAL[args.proyecto]:
        if paso[0] == "rama":  # cambia de rama (la crea si no existe)
            existe = subprocess.run(["git", "rev-parse", "--verify", "-q", paso[1]], cwd=destino,
                                    capture_output=True).returncode == 0
            git(destino, "switch", "-q", *([] if existe else ["-c"]), paso[1])
            continue
        fecha, mensaje, rutas = paso
        git(destino, "add", "--", *rutas)
        git(destino, "commit", "-q", "-m", mensaje, fecha=fecha)
    print(f"Repositorio listo en {destino}")
    print(f"Ábralo con:  code \"{destino}\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
