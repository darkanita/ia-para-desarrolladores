"""Busca secretos en el repositorio: archivos de secretos versionados y llaves o contraseñas escritas en el código.

Usa las reglas de banco.yaml (`proteccion.archivos_secretos` y `proteccion.patrones_secretos`). Revisa los
archivos que git conoce o que agregaría (no los ignorados). Nunca muestra el secreto completo: solo el tipo,
el archivo, la línea y los primeros caracteres.

Uso (desde la raíz del repositorio):
    python herramientas/buscar_secretos.py           # termina en 1 si encuentra algo
    python herramientas/buscar_secretos.py --historia  # además busca archivos de secretos en commits anteriores

Lo usan el agente de seguridad (/seguridad), la persona antes de un pull request y la CI (sesión 8).
"""
from __future__ import annotations

import fnmatch
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
EXCLUIR = {"banco.yaml"}  # define los patrones: no se busca a sí mismo
TAMANO_MAXIMO = 1_000_000


def cargar_reglas() -> dict:
    import yaml  # PyYAML

    banco = yaml.safe_load((RAIZ / "banco.yaml").read_text(encoding="utf-8")) or {}
    return banco.get("proteccion") or {}


def archivos_del_repositorio() -> list[str]:
    r = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=RAIZ, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        return [p.relative_to(RAIZ).as_posix() for p in RAIZ.rglob("*") if p.is_file() and ".git" not in p.parts]
    return [linea for linea in r.stdout.splitlines() if linea]


def es_archivo_de_secretos(ruta: str, reglas: dict) -> bool:
    nombre = Path(ruta).name
    if any(fnmatch.fnmatch(nombre, p) or fnmatch.fnmatch(ruta, p) for p in reglas.get("archivos_permitidos", [])):
        return False
    return any(fnmatch.fnmatch(nombre, p) or fnmatch.fnmatch(ruta, p) for p in reglas.get("archivos_secretos", []))


def enmascarar(texto: str) -> str:
    texto = texto.strip()
    return (texto[:4] + "…") if len(texto) > 4 else "…"


def buscar(reglas: dict, historia: bool) -> list[str]:
    hallazgos: list[str] = []
    patrones = [(p.get("nombre", "secreto"), re.compile(p["patron"])) for p in reglas.get("patrones_secretos", [])]
    for ruta in archivos_del_repositorio():
        if ruta in EXCLUIR:
            continue
        if es_archivo_de_secretos(ruta, reglas):
            hallazgos.append(f"{ruta}: archivo de secretos dentro del repositorio (proteccion.archivos_secretos)")
        archivo = RAIZ / ruta
        try:
            if archivo.stat().st_size > TAMANO_MAXIMO:
                continue
            texto = archivo.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for numero, linea in enumerate(texto.splitlines(), start=1):
            for nombre, patron in patrones:
                m = patron.search(linea)
                if m:
                    hallazgos.append(f"{ruta}:{numero}: {nombre} ({enmascarar(m.group(0))})")
    if historia:
        r = subprocess.run(["git", "log", "--all", "--name-only", "--format="], cwd=RAIZ, capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        en_historia = sorted({r_ for r_ in r.stdout.splitlines() if r_ and es_archivo_de_secretos(r_, reglas)})
        hallazgos += [f"{ruta}: estuvo en la historia de git: el secreto se considera expuesto, hay que rotarlo"
                      for ruta in en_historia]
    return hallazgos


def main() -> int:
    hallazgos = buscar(cargar_reglas(), "--historia" in sys.argv)
    if not hallazgos:
        print("Búsqueda de secretos: OK (no se encontró ninguno)")
        return 0
    print(f"Búsqueda de secretos: {len(hallazgos)} hallazgo(s)")
    for h in hallazgos:
        print(f"  ✗ {h}")
    print("\nLos secretos viven en variables de entorno (politicas.seguridad). Un secreto que llegó a git se rota.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
