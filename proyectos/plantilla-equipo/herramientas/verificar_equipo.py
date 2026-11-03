"""Verifica que el repositorio del equipo y su máquina están listos para trabajar con el agente.

Uso (desde la raíz del repositorio del equipo):
    python herramientas/verificar_equipo.py

Solo usa la librería estándar. No modifica nada.
"""
from __future__ import annotations

import json
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
                          (".claude/skills/intencion/SKILL.md", "skill /intencion"),
                          (".claude/skills/spec/SKILL.md", "skill /spec (sesión 3)"),
                          (".claude/rules", "reglas por tipo de archivo (sesión 3)")]:
        existe = (RAIZ / archivo).exists()
        reportar(OK if existe else FALTA, archivo, para if existe else "no existe",
                 "Actualice el repositorio: desde la carpeta del curso, python proyectos/actualizar_repositorio.py <su repo>")
    sincronizadas = subprocess.run([sys.executable, str(RAIZ / "herramientas" / "sincronizar_skills.py"), "--verificar"],
                                   capture_output=True, text=True).returncode == 0
    reportar(OK if sincronizadas else FALTA, "Skills y reglas para Copilot", ".github/skills e instructions",
             "Ejecute: python herramientas/sincronizar_skills.py")
    casos = sorted(p.parent.name for p in (RAIZ / "docs" / "sdlc").glob("*/intent.md"))
    reportar(OK if casos else AVISO, "Casos con intent.md", ", ".join(casos) if casos else "ninguno todavía",
             "Use /intencion en su asistente para crear el primero.")

    print("\n3. Herramientas del banco (servidor MCP)")
    try:
        import yaml  # noqa: F401
        reportar(OK, "PyYAML", "instalado")
    except ImportError:
        reportar(FALTA, "PyYAML", "no instalado", "Con el entorno del curso activo: pip install pyyaml")
    servidor = RAIZ / "herramientas" / "mcp_banco" / "servidor.py"
    if servidor.exists():
        prueba = subprocess.run([sys.executable, str(servidor), "--probar"], capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=30)
        reportar(OK if prueba.returncode == 0 else FALTA, "Servidor MCP del banco", "responde" if prueba.returncode == 0 else "no responde",
                 "Ejecute: python herramientas/mcp_banco/servidor.py --probar y lea el error")
    else:
        reportar(FALTA, "Servidor MCP del banco", "no existe", "Actualice el repositorio a la versión de la sesión 3")
    for config, quien, clave in [(".mcp.json", "Claude Code", "mcpServers"), (".vscode/mcp.json", "Copilot", "servers")]:
        ruta = RAIZ / config
        try:
            comando_mcp = json.loads(ruta.read_text(encoding="utf-8"))[clave]["banco"]["command"]
        except (OSError, ValueError, KeyError, TypeError):
            reportar(FALTA, f"{config} ({quien})", "no existe o no tiene el servidor banco", "Ejecute: python herramientas/configurar_mcp.py")
            continue
        existe = Path(comando_mcp).exists() if ("/" in comando_mcp or "\\" in comando_mcp) else bool(shutil.which(comando_mcp))
        mismo = existe and ("/" in comando_mcp or "\\" in comando_mcp) and Path(comando_mcp).resolve() == Path(sys.executable).resolve()
        if mismo:
            reportar(OK, f"{config} ({quien})", "usa el Python de este entorno")
        else:
            reportar(AVISO, f"{config} ({quien})", f"usa '{comando_mcp}'",
                     "Para usar el Python del curso (con PyYAML), ejecute: python herramientas/configurar_mcp.py")

    faltan = [n for e, n in resultados if e == FALTA]
    print("\n" + ("Listo para trabajar con el agente." if not faltan else f"Faltan {len(faltan)}: " + ", ".join(faltan)))
    return 1 if faltan else 0


if __name__ == "__main__":
    sys.exit(main())
