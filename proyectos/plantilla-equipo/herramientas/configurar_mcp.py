"""Conecta el servidor MCP del banco a Claude Code (.mcp.json) y a Copilot (.vscode/mcp.json).

Escribe en los dos archivos la ruta del Python con el que usted ejecuta este script, para que
las herramientas arranquen el servidor con el entorno del curso (el que tiene PyYAML).

Uso (con el entorno del curso activo, desde la raíz del repositorio):
    python herramientas/configurar_mcp.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SERVIDOR = "herramientas/mcp_banco/servidor.py"


def escribir(ruta: Path, contenido: dict) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(contenido, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  {ruta.relative_to(RAIZ).as_posix()}")


def main() -> int:
    try:
        import yaml  # noqa: F401
    except ImportError:
        print("Este Python no tiene PyYAML. Active el entorno del curso y ejecute: pip install pyyaml")
        return 1
    python = Path(sys.executable).as_posix()
    print(f"Servidor MCP del banco con {python}:")
    escribir(RAIZ / ".mcp.json", {"mcpServers": {"banco": {"type": "stdio", "command": python,
                                                           "args": [str((RAIZ / SERVIDOR).as_posix())]}}})
    escribir(RAIZ / ".vscode" / "mcp.json", {"servers": {"banco": {"type": "stdio", "command": python,
                                                                   "args": ["${workspaceFolder}/" + SERVIDOR]}}})
    print("\nListo. Claude Code: salga y vuelva a abrir claude, y revise con /mcp.")
    print("Copilot: abra .vscode/mcp.json y pulse Start sobre \"banco\" (o recargue VS Code).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
