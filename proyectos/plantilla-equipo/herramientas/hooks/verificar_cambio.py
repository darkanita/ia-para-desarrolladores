"""Hook del equipo: después de que el agente edita código, corre la regla de capas y las pruebas.

Lo llaman Claude Code (.claude/settings.json) y Copilot (.github/hooks/verificar-cambio.json)
después de cada edición. Recibe por la entrada estándar el JSON del evento (PostToolUse).

- Si el archivo editado no es .py de src/ o tests/, no hace nada.
- Si la regla de capas o las pruebas fallan, escribe el resumen en la salida de error y termina
  con código 2: el agente lo lee y debe corregir antes de seguir.
- Si no puede correr (no hay pytest en este Python), avisa y no bloquea.

Probarlo a mano (desde la raíz del repositorio):
    echo '{"tool_input": {"file_path": "src/x.py"}}' | python herramientas/hooks/verificar_cambio.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
LIMITE_LINEAS = 25


def rutas_editadas(evento: object) -> list[str]:
    """Busca rutas de archivo en el JSON del evento, venga de Claude Code o de Copilot."""
    encontradas: list[str] = []

    def recorrer(valor: object, clave: str = "") -> None:
        if isinstance(valor, dict):
            for k, v in valor.items():
                recorrer(v, k)
        elif isinstance(valor, list):
            for v in valor:
                recorrer(v, clave)
        elif isinstance(valor, str) and valor.endswith(".py") and ("path" in clave.lower() or "file" in clave.lower()):
            encontradas.append(valor)

    if isinstance(evento, dict):
        recorrer(evento.get("tool_input") or evento.get("toolArgs") or evento)
    return encontradas


def es_codigo(ruta: str) -> bool:
    """True si la ruta es un .py de src/ o tests/ de este repositorio."""
    p = Path(ruta)
    try:
        relativa = (p if p.is_absolute() else RAIZ / p).resolve().relative_to(RAIZ)
    except ValueError:
        return False
    return relativa.parts[:1] in (("src",), ("tests",))


def correr(*args: str) -> tuple[int, str]:
    r = subprocess.run([sys.executable, *args], cwd=RAIZ, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=120)
    return r.returncode, (r.stdout + r.stderr).strip()


def main() -> int:
    try:
        evento = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0
    if not any(es_codigo(r) for r in rutas_editadas(evento)):
        return 0
    if not (RAIZ / "src").exists():
        return 0

    problemas: list[str] = []
    codigo, salida = correr("herramientas/verificar_capas.py")
    if codigo != 0:
        problemas.append("Regla de capas:\n" + salida)

    codigo, salida = correr("-c", "import pytest")
    if codigo != 0:
        print("Hook del equipo: este Python no tiene pytest; no se corrieron las pruebas. "
              "Abra el asistente con el entorno del curso activo.", file=sys.stderr)
        return 1  # aviso para la persona, no bloquea
    codigo, salida = correr("-m", "pytest", "-q", "-x", "--no-header", "-p", "no:cacheprovider")
    if codigo not in (0, 5):  # 5 = no hay pruebas todavía
        lineas = salida.splitlines()
        problemas.append("Pruebas (python -m pytest -q):\n" + "\n".join(lineas[-LIMITE_LINEAS:]))

    if problemas:
        print("Hook del equipo: el cambio rompe una verificación. Corríjalo antes de seguir "
              "(no cambie el valor esperado de una prueba para que pase). Si es una prueba nueva que "
              "descubre un posible defecto, márquela con @pytest.mark.xfail(strict=True, reason=...) "
              "y repórtela.\n\n" + "\n\n".join(problemas),
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(main())
