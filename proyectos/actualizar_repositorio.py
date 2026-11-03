"""Actualiza un repositorio ya creado a la versión más reciente de su plantilla, sin pisar su trabajo.

Uso (desde la carpeta del curso, con el entorno activo):
    python proyectos/actualizar_repositorio.py ../mi-reto
    python proyectos/actualizar_repositorio.py ../mi-reto --probar   # muestra qué haría, sin cambiar nada

Para cada archivo de la plantilla:
  - si no existe en su repositorio, lo agrega;
  - si existe y usted no lo modificó (es igual a una versión anterior de la plantilla), lo actualiza;
  - si usted lo modificó, NO lo toca: deja la versión nueva al lado como <archivo>.nuevo para que la compare.
Su carpeta docs/sdlc/ (sus artefactos) nunca se toca. Al final configura el servidor MCP y hace un commit.
Solo usa la librería estándar y git.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
IGNORAR = {"__pycache__", ".pytest_cache", ".git"}
NUNCA_TOCAR = ("docs/sdlc/",)
POR_MAQUINA = {".mcp.json", ".vscode/mcp.json"}  # los reescribe configurar_mcp.py


def huella(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def archivos(raiz: Path) -> list[str]:
    return sorted(p.relative_to(raiz).as_posix() for p in raiz.rglob("*")
                  if p.is_file() and not IGNORAR.intersection(p.relative_to(raiz).parts))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("destino", type=Path, help="su repositorio, por ejemplo ../mi-reto")
    p.add_argument("--proyecto", default="plantilla-equipo")
    p.add_argument("--probar", action="store_true", help="mostrar qué haría, sin cambiar nada")
    p.add_argument("--sin-commit", action="store_true", help="no hacer commit al final")
    args = p.parse_args()

    plantilla, destino = AQUI / args.proyecto, args.destino.resolve()
    if not (destino / ".git").exists():
        print(f"{destino} no es un repositorio git. Para crear uno nuevo use crear_repositorio.py.", file=sys.stderr)
        return 1
    versiones = json.loads((AQUI / "versiones_plantilla.json").read_text(encoding="utf-8")).get(args.proyecto, {})
    conocidas: dict[str, set[str]] = {}
    for huellas in versiones.values():
        for ruta, h in huellas.items():
            conocidas.setdefault(ruta, set()).add(h)

    agregados, actualizados, conflictos, iguales = [], [], [], 0
    for ruta in archivos(plantilla):
        if ruta.startswith(NUNCA_TOCAR) and ruta != "docs/sdlc/README.md":
            continue
        origen, final = plantilla / ruta, destino / ruta
        if not final.exists():
            agregados.append(ruta)
        elif huella(final) == huella(origen):
            iguales += 1
            continue
        elif ruta in POR_MAQUINA or huella(final) in conocidas.get(ruta, set()):
            actualizados.append(ruta)
        else:
            conflictos.append(ruta)
            if not args.probar:
                shutil.copy2(origen, final.with_name(final.name + ".nuevo"))
            continue
        if not args.probar:
            final.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origen, final)

    print(f"Actualización de {destino.name} con la plantilla {args.proyecto}" + (" (prueba, sin cambios)" if args.probar else ""))
    for titulo, lista in [("Agregados", agregados), ("Actualizados", actualizados)]:
        if lista:
            print(f"\n{titulo} ({len(lista)}):\n" + "\n".join(f"  + {r}" for r in lista))
    if conflictos:
        print(f"\nUsted los modificó, no se tocaron ({len(conflictos)}). La versión nueva quedó al lado como .nuevo:")
        print("\n".join(f"  ! {r}  ->  {r}.nuevo" for r in conflictos))
        print("  Compare cada par, quédese con lo que sirva y borre el .nuevo (o pídale ayuda a su asistente).")
    print(f"\nSin cambios: {iguales} archivos.")
    if args.probar:
        return 0

    configurar = destino / "herramientas" / "configurar_mcp.py"
    if configurar.exists():
        r = subprocess.run([sys.executable, str(configurar)], capture_output=True, text=True, cwd=destino)
        print("Servidor MCP configurado con este Python." if r.returncode == 0 else r.stdout + r.stderr)
    if not args.sin_commit and (agregados or actualizados):
        tocados = agregados + actualizados + [r for r in POR_MAQUINA if (destino / r).exists()]
        subprocess.run(["git", "add", "--", *tocados], cwd=destino, capture_output=True)
        r = subprocess.run(["git", "commit", "-q", "-m", "Agente del equipo actualizado a la última versión de la plantilla"],
                           cwd=destino, capture_output=True, text=True)
        if r.returncode == 0:
            print("Commit hecho: \"Agente del equipo actualizado a la última versión de la plantilla\".")
        else:
            print("No se pudo hacer el commit; revise git status y haga el commit usted:\n" + (r.stderr or r.stdout).strip())
    print(f"\nSiguiente paso: cd \"{destino}\" y python herramientas/verificar_equipo.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
