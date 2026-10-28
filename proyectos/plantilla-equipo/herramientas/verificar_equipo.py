"""Verifica que el repositorio del equipo y su máquina están listos para trabajar con el agente.

Uso (desde la raíz del repositorio del equipo):
    python herramientas/verificar_equipo.py

Solo usa la librería estándar. No modifica nada.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
OK, FALTA, AVISO = "OK", "FALTA", "AVISO"
resultados: list[tuple[str, str]] = []


def reportar(estado: str, nombre: str, detalle: str = "", ayuda: str = "") -> None:
    resultados.append((estado, nombre))
    print(f"  [{estado:<5}] {nombre:<34} {detalle}")
    if ayuda and estado != OK:
        print(f"          → {ayuda}")


def comando(*cmd: str) -> str | None:
    exe = shutil.which(cmd[0])
    if not exe:
        return None
    try:
        r = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True, timeout=20, cwd=RAIZ,
                           encoding="utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired):
        return None
    return (r.stdout + r.stderr).strip() if r.returncode == 0 else None


def main() -> int:
    print("Repositorio del equipo · verificación\n")
    print("1. Máquina")
    v = sys.version_info
    reportar(OK if v >= (3, 10) else FALTA, "Python", f"{v.major}.{v.minor}.{v.micro}", "Instale Python 3.12.")
    git = comando("git", "--version")
    reportar(OK if git else FALTA, "Git", git or "no encontrado", "Instale Git (ver guía de preparación).")
    claude = comando("claude", "--version")
    copilot = comando("copilot", "version")
    code = shutil.which("code")
    if claude or copilot:
        reportar(OK, "Asistente en la terminal", ", ".join(x for x in ("Claude Code" if claude else "", "Copilot CLI" if copilot else "") if x))
    elif code:
        reportar(AVISO, "Asistente en la terminal", "no encontrado; use el panel de VS Code",
                 "Claude Code: irm https://claude.ai/install.ps1 | iex · Copilot CLI: winget install GitHub.Copilot")
    else:
        reportar(FALTA, "Asistente", "no se encontró Claude Code, Copilot CLI ni VS Code")

    print("\n2. Repositorio")
    reportar(OK if (RAIZ / ".git").exists() else FALTA, "Repositorio git", "",
             "Ejecute: git init && git add . && git commit -m \"Inicio\"")
    for archivo, para in [("banco.yaml", "definiciones del banco"), ("AGENTS.md", "reglas del equipo"),
                          ("CLAUDE.md", "entrada de Claude Code"), (".github/copilot-instructions.md", "entrada de Copilot"),
                          (".claude/skills/intencion/SKILL.md", "skill /intencion")]:
        existe = (RAIZ / archivo).exists()
        reportar(OK if existe else FALTA, archivo, para if existe else "no existe", "Cree el repositorio desde la plantilla del curso.")
    sincronizadas = subprocess.run([sys.executable, str(RAIZ / "herramientas" / "sincronizar_skills.py"), "--verificar"],
                                   capture_output=True, text=True).returncode == 0
    reportar(OK if sincronizadas else FALTA, "Skills para Copilot (.github/skills)", "",
             "Ejecute: python herramientas/sincronizar_skills.py")
    casos = sorted(p.parent.name for p in (RAIZ / "docs" / "sdlc").glob("*/intent.md"))
    reportar(OK if casos else AVISO, "Casos con intent.md", ", ".join(casos) if casos else "ninguno todavía",
             "Use /intencion en su asistente para crear el primero.")

    print("\n3. Para las próximas sesiones")
    try:
        import yaml  # noqa: F401
        reportar(OK, "PyYAML (sesión 3)", "instalado")
    except ImportError:
        reportar(AVISO, "PyYAML (sesión 3)", "no instalado", "pip install pyyaml")
    try:
        import mcp  # noqa: F401
        reportar(OK, "mcp (sesión 3)", "instalado")
    except ImportError:
        reportar(AVISO, "mcp (sesión 3)", "no instalado", "pip install mcp")

    faltan = [n for e, n in resultados if e == FALTA]
    print("\n" + ("Listo para trabajar con el agente." if not faltan else f"Faltan {len(faltan)}: " + ", ".join(faltan)))
    return 1 if faltan else 0


if __name__ == "__main__":
    sys.exit(main())
