"""Revisa la regla de capas: cada capa solo importa las que tiene permitidas.

    dominio      -> nada del proyecto, y ningún framework (convenciones.paquetes_de_framework en banco.yaml)
    puertos      -> dominio
    casos_uso    -> dominio, puertos
    adaptadores  -> dominio, puertos, casos_uso
    app          -> todas

Uso (desde la raíz del repositorio):
    python herramientas/verificar_capas.py
Sale con código 1 si encuentra una violación, para que pueda usarse en pruebas, hooks o CI.
Solo usa la librería estándar (lee banco.yaml con PyYAML si está; si no, usa una lista por defecto).
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CAPAS = ["dominio", "puertos", "casos_uso", "adaptadores", "app"]
PERMITIDAS = {
    "dominio": set(),
    "puertos": {"dominio"},
    "casos_uso": {"dominio", "puertos"},
    "adaptadores": {"dominio", "puertos", "casos_uso"},
    "app": set(CAPAS),
}
FRAMEWORKS_POR_DEFECTO = ["streamlit", "fastapi", "pydantic", "flask", "django", "sqlalchemy", "requests", "httpx"]


def frameworks() -> list[str]:
    try:
        import yaml

        datos = yaml.safe_load((RAIZ / "banco.yaml").read_text(encoding="utf-8")) or {}
        return datos.get("convenciones", {}).get("paquetes_de_framework", FRAMEWORKS_POR_DEFECTO)
    except Exception:
        return FRAMEWORKS_POR_DEFECTO


def capa_de(partes: tuple[str, ...]) -> str | None:
    return next((p for p in partes if p in CAPAS), None)


def importaciones(archivo: Path) -> list[tuple[int, str]]:
    arbol = ast.parse(archivo.read_text(encoding="utf-8"), filename=str(archivo))
    nombres: list[tuple[int, str]] = []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            nombres += [(nodo.lineno, a.name) for a in nodo.names]
        elif isinstance(nodo, ast.ImportFrom):
            if nodo.level:  # import relativo: se resuelve contra el paquete del archivo
                base = archivo.parent.relative_to(RAIZ / "src").parts
                base = base[: len(base) - (nodo.level - 1)] if nodo.level > 1 else base
                nombres.append((nodo.lineno, ".".join(base + ((nodo.module,) if nodo.module else ()))))
            elif nodo.module:
                nombres.append((nodo.lineno, nodo.module))
    return nombres


def main() -> int:
    src = RAIZ / "src"
    if not src.is_dir():
        print("No hay carpeta src/. Cree la estructura con: python herramientas/crear_estructura.py <paquete>")
        return 0
    prohibidos = frameworks()
    violaciones: list[str] = []
    revisados = 0
    for archivo in sorted(src.rglob("*.py")):
        relativo = archivo.relative_to(src)
        capa = capa_de(relativo.parts[1:-1]) if len(relativo.parts) > 2 else None
        if capa is None:
            continue
        revisados += 1
        for linea, modulo in importaciones(archivo):
            partes = modulo.split(".")
            destino = capa_de(tuple(partes[1:])) if len(partes) > 1 else None
            if destino and destino != capa and destino not in PERMITIDAS[capa]:
                violaciones.append(f"{relativo.as_posix()}:{linea}  {capa} no puede importar {destino} ({modulo})")
            if capa == "dominio" and partes[0] in prohibidos:
                violaciones.append(f"{relativo.as_posix()}:{linea}  el dominio no puede importar el framework {partes[0]}")
    if violaciones:
        print("Regla de capas: hay violaciones\n" + "\n".join(f"  ✗ {v}" for v in violaciones))
        print("\nMueva el código a la capa correcta o use un puerto. Detalle de la regla en .claude/rules/capas.md")
        return 1
    print(f"Regla de capas: OK ({revisados} archivos revisados).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
