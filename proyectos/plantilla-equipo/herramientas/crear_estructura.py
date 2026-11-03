"""Crea la estructura por capas del proyecto del equipo (plantilla del proyecto v0).

    src/<paquete>/
        dominio/       reglas de negocio puras: entidades, cálculos, validaciones. No importa frameworks.
        casos_uso/     lo que el usuario quiere lograr (simular_credito). Orquesta el dominio y los puertos.
        puertos/       interfaces hacia afuera (repositorios, servicios del catálogo). Solo contratos.
        adaptadores/   implementaciones de los puertos: en memoria (pruebas) o servicios reales.
        app/           la entrada: interfaz Streamlit, API FastAPI o línea de comandos.
    tests/             pruebas con pytest (dominio primero)

Uso (desde la raíz del repositorio):
    python herramientas/crear_estructura.py <paquete>      por ejemplo: simulador
No borra ni reemplaza nada que ya exista.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CAPAS = {
    "dominio": "Reglas de negocio puras: entidades, cálculos y validaciones. No importa frameworks ni otras capas.",
    "casos_uso": "Lo que el usuario quiere lograr. Orquesta el dominio y usa los puertos. Puede importar dominio y puertos.",
    "puertos": "Contratos hacia afuera (protocolos): repositorios y servicios del catálogo. Puede importar dominio.",
    "adaptadores": "Implementaciones de los puertos: en memoria para pruebas o clientes de servicios reales.",
    "app": "La entrada del sistema: Streamlit, FastAPI o línea de comandos. Arma los casos de uso con sus adaptadores.",
}
PYPROJECT = """[project]
name = "{paquete}"
version = "0.1.0"
requires-python = ">=3.10"

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
"""


def escribir_si_falta(ruta: Path, contenido: str, creados: list[str]) -> None:
    if not ruta.exists():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(contenido, encoding="utf-8")
        creados.append(ruta.relative_to(RAIZ).as_posix())


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"[a-z][a-z0-9_]*", sys.argv[1]):
        print(__doc__)
        print("Indique el nombre del paquete en snake_case, por ejemplo: simulador")
        return 1
    paquete = sys.argv[1]
    base = RAIZ / "src" / paquete
    creados: list[str] = []
    escribir_si_falta(base / "__init__.py", f'"""Paquete {paquete} del equipo (Banco Orquídea, ficticio)."""\n', creados)
    for capa, descripcion in CAPAS.items():
        escribir_si_falta(base / capa / "__init__.py", f'"""{descripcion}"""\n', creados)
    escribir_si_falta(RAIZ / "tests" / "__init__.py", "", creados)
    escribir_si_falta(RAIZ / "pyproject.toml", PYPROJECT.format(paquete=paquete), creados)
    if creados:
        print("Creado:\n" + "\n".join(f"  + {c}" for c in creados))
    else:
        print("La estructura ya existía; no se cambió nada.")
    print("\nRegla de capas: python herramientas/verificar_capas.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
