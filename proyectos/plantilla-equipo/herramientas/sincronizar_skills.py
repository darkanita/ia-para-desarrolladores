"""Copia las skills y las reglas del equipo de Claude Code al formato de Copilot.

Se escriben una sola vez, en la carpeta de Claude Code, y este script las lleva a Copilot:
  - Skills:  .claude/skills/<nombre>/   ->  .github/skills/<nombre>/            (mismo SKILL.md)
  - Reglas:  .claude/rules/<nombre>.md  ->  .github/instructions/<nombre>.instructions.md
             (el campo `paths` de Claude Code se convierte en `applyTo` de Copilot)

Uso:
    python herramientas/sincronizar_skills.py             # copia
    python herramientas/sincronizar_skills.py --verificar # solo revisa que estén al día
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SKILLS_ORIGEN = RAIZ / ".claude" / "skills"
SKILLS_DESTINO = RAIZ / ".github" / "skills"
REGLAS_ORIGEN = RAIZ / ".claude" / "rules"
REGLAS_DESTINO = RAIZ / ".github" / "instructions"
MARCA = "<!-- Generado desde .claude/rules/{nombre}.md con herramientas/sincronizar_skills.py: edite el original. -->"


# --------------------------------------------------------------------------- reglas

def leer_regla(ruta: Path) -> tuple[str, list[str], str]:
    """Devuelve (description, paths, cuerpo) de una regla de Claude Code."""
    texto = ruta.read_text(encoding="utf-8").replace("\r\n", "\n")
    descripcion, rutas, cuerpo = "", [], texto
    if texto.startswith("---\n") and "\n---" in texto[4:]:
        cabecera, cuerpo = texto[4:].split("\n---", 1)
        cuerpo = cuerpo.lstrip("\n")
        en_paths = False
        for linea in cabecera.splitlines():
            limpia = linea.strip()
            if limpia.startswith("description:"):
                descripcion, en_paths = limpia.split(":", 1)[1].strip().strip("\"'"), False
            elif limpia.startswith("paths:"):
                en_paths = True
                resto = limpia.split(":", 1)[1].strip()
                if resto:  # paths: "a, b"  o  paths: ["a", "b"]
                    rutas += [p.strip().strip("\"'") for p in resto.strip("[]").split(",") if p.strip()]
            elif en_paths and limpia.startswith("- "):
                rutas.append(limpia[2:].strip().strip("\"'"))
            elif limpia and not limpia.startswith("#"):
                en_paths = False
    return descripcion, rutas, cuerpo


def instruccion_para(ruta: Path) -> str:
    descripcion, rutas, cuerpo = leer_regla(ruta)
    cabecera = ["---"]
    if descripcion:
        cabecera.append(f"description: \"{descripcion}\"")
    cabecera.append(f"applyTo: \"{','.join(rutas) if rutas else '**'}\"")
    cabecera.append("---")
    return "\n".join(cabecera) + "\n" + MARCA.format(nombre=ruta.stem) + "\n\n" + cuerpo


def reglas_esperadas() -> dict[str, str]:
    if not REGLAS_ORIGEN.is_dir():
        return {}
    return {f"{r.stem}.instructions.md": instruccion_para(r) for r in sorted(REGLAS_ORIGEN.glob("*.md"))}


def generadas_existentes() -> dict[str, str]:
    """Instrucciones de Copilot que salieron de una regla (las escritas a mano no se tocan)."""
    if not REGLAS_DESTINO.is_dir():
        return {}
    return {p.name: p.read_text(encoding="utf-8").replace("\r\n", "\n") for p in REGLAS_DESTINO.glob("*.instructions.md")
            if "Generado desde .claude/rules/" in p.read_text(encoding="utf-8")}


# --------------------------------------------------------------------------- verificación

def diferencias() -> list[str]:
    pendientes: list[str] = []
    if not SKILLS_ORIGEN.is_dir():
        pendientes.append("no existe .claude/skills/")
    elif not SKILLS_DESTINO.is_dir():
        pendientes.append(".github/skills/ no existe")
    else:
        def recorrer(c: filecmp.dircmp, prefijo: str) -> None:
            pendientes.extend(f"skills/{prefijo}{n} (falta en .github)" for n in c.left_only)
            pendientes.extend(f"skills/{prefijo}{n} (sobra en .github)" for n in c.right_only)
            pendientes.extend(f"skills/{prefijo}{n} (distinto)" for n in c.diff_files)
            for nombre, sub in c.subdirs.items():
                recorrer(sub, f"{prefijo}{nombre}/")
        recorrer(filecmp.dircmp(SKILLS_ORIGEN, SKILLS_DESTINO), "")
    esperadas, existentes = reglas_esperadas(), generadas_existentes()
    for nombre, contenido in esperadas.items():
        if nombre not in existentes:
            pendientes.append(f"instructions/{nombre} (falta en .github)")
        elif existentes[nombre] != contenido:
            pendientes.append(f"instructions/{nombre} (distinto)")
    pendientes.extend(f"instructions/{n} (sobra: su regla ya no existe)" for n in existentes if n not in esperadas)
    return pendientes


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--verificar", action="store_true", help="solo revisar, no copiar")
    args = p.parse_args()
    if args.verificar:
        pendientes = diferencias()
        for d in pendientes:
            print(f"  - {d}")
        print("Skills y reglas sincronizadas." if not pendientes else "Ejecute: python herramientas/sincronizar_skills.py")
        return 1 if pendientes else 0
    if not SKILLS_ORIGEN.is_dir():
        print("No existe .claude/skills/", file=sys.stderr)
        return 1
    if SKILLS_DESTINO.exists():
        shutil.rmtree(SKILLS_DESTINO)
    shutil.copytree(SKILLS_ORIGEN, SKILLS_DESTINO)
    print(f"Skills en .github/skills/: {', '.join(sorted(d.name for d in SKILLS_DESTINO.iterdir() if d.is_dir()))}")
    esperadas = reglas_esperadas()
    if esperadas or REGLAS_DESTINO.is_dir():
        REGLAS_DESTINO.mkdir(parents=True, exist_ok=True)
        for nombre in generadas_existentes():
            if nombre not in esperadas:
                (REGLAS_DESTINO / nombre).unlink()
        for nombre, contenido in esperadas.items():
            (REGLAS_DESTINO / nombre).write_text(contenido, encoding="utf-8", newline="\n")
        print(f"Reglas en .github/instructions/: {', '.join(esperadas) or 'ninguna'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
