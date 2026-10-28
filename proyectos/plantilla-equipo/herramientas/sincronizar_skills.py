"""Copia las skills del equipo de .claude/skills/ a .github/skills/ para que Copilot las use.

Las skills se escriben una sola vez, en .claude/skills/ (mismo formato SKILL.md en las dos
herramientas). Este script las copia a .github/skills/.

Uso:
    python herramientas/sincronizar_skills.py             # copia
    python herramientas/sincronizar_skills.py --verificar # solo revisa que estén iguales
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ORIGEN = RAIZ / ".claude" / "skills"
DESTINO = RAIZ / ".github" / "skills"


def diferencias() -> list[str]:
    if not ORIGEN.is_dir():
        return ["no existe .claude/skills/"]
    if not DESTINO.is_dir():
        return [".github/skills/ no existe"]
    comp = filecmp.dircmp(ORIGEN, DESTINO)
    pendientes: list[str] = []

    def recorrer(c: filecmp.dircmp, prefijo: str) -> None:
        pendientes.extend(f"{prefijo}{n} (falta en .github)" for n in c.left_only)
        pendientes.extend(f"{prefijo}{n} (sobra en .github)" for n in c.right_only)
        pendientes.extend(f"{prefijo}{n} (distinto)" for n in c.diff_files)
        for nombre, sub in c.subdirs.items():
            recorrer(sub, f"{prefijo}{nombre}/")

    recorrer(comp, "")
    return pendientes


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--verificar", action="store_true", help="solo revisar, no copiar")
    args = p.parse_args()
    if args.verificar:
        pendientes = diferencias()
        for d in pendientes:
            print(f"  - {d}")
        print("Skills sincronizadas." if not pendientes else "Ejecute: python herramientas/sincronizar_skills.py")
        return 1 if pendientes else 0
    if not ORIGEN.is_dir():
        print("No existe .claude/skills/", file=sys.stderr)
        return 1
    if DESTINO.exists():
        shutil.rmtree(DESTINO)
    shutil.copytree(ORIGEN, DESTINO)
    nombres = sorted(d.name for d in DESTINO.iterdir() if d.is_dir())
    print(f"Copiadas a .github/skills/: {', '.join(nombres)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
