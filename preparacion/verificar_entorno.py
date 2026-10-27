"""Verifica que su máquina esté lista para el curso IA para Desarrolladores.

Uso (desde la carpeta del curso, con el entorno virtual activo):
    python preparacion/verificar_entorno.py

Solo usa la librería estándar. No modifica nada en su equipo: ejecuta comandos
de consulta de versión (como `git --version`) y prueba la conexión a los
servicios que usa el curso. Al final, envíe una captura del resumen por el
canal del curso si algo aparece en rojo.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import platform
import re
import shutil
import socket
import ssl
import subprocess
import sys
import urllib.error
import urllib.request

OK, FALTA, AVISO = "OK", "FALTA", "AVISO"
COLOR = {OK: "\033[32m", FALTA: "\033[31m", AVISO: "\033[33m"}
FIN = "\033[0m"
WINDOWS = platform.system() == "Windows"


def _color_activo() -> bool:
    if os.getenv("NO_COLOR"):
        return False
    if WINDOWS:
        os.system("")  # habilita secuencias ANSI en consolas modernas de Windows
    return sys.stdout.isatty()


USAR_COLOR = _color_activo()
resultados: list[tuple[str, str, str, str]] = []


def reportar(estado: str, nombre: str, detalle: str, ayuda: str = "") -> None:
    resultados.append((estado, nombre, detalle, ayuda))
    etiqueta = f"{COLOR[estado]}{estado:<5}{FIN}" if USAR_COLOR else f"{estado:<5}"
    print(f"  [{etiqueta}] {nombre:<28} {detalle}")
    if ayuda and estado != OK:
        print(f"          → {ayuda}")


def ejecutar(*cmd: str, timeout: int = 20) -> str | None:
    """Ejecuta un comando de consulta y devuelve su salida, o None si no existe o falla."""
    exe = shutil.which(cmd[0])
    if exe is None:
        return None
    try:
        r = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired):
        return None
    salida = (r.stdout or "") + (r.stderr or "")
    return salida.strip() if r.returncode == 0 or salida.strip() else None


def version(texto: str | None) -> tuple[int, ...] | None:
    if not texto:
        return None
    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", texto)
    return tuple(int(g) for g in m.groups() if g is not None) if m else None


def texto_version(v: tuple[int, ...] | None) -> str:
    return ".".join(map(str, v)) if v else "?"


def requerir(nombre: str, cmd: list[str], minimo: tuple[int, ...] | None, ayuda: str,
             obligatorio: bool = True) -> tuple[int, ...] | None:
    salida = ejecutar(*cmd)
    v = version(salida)
    if salida is None:
        reportar(FALTA if obligatorio else AVISO, nombre, "no encontrado", ayuda)
    elif minimo and (v is None or v < minimo):
        reportar(FALTA if obligatorio else AVISO, nombre,
                 f"versión {texto_version(v)} (mínimo {texto_version(minimo)})", ayuda)
    else:
        reportar(OK, nombre, f"versión {texto_version(v)}")
    return v


def red(nombre: str, url: str, obligatorio: bool = True) -> None:
    """Prueba HTTPS hasta el servidor. Cualquier respuesta HTTP (incluso 401/404) cuenta como alcanzable."""
    try:
        urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=10)
        reportar(OK, nombre, url)
    except urllib.error.HTTPError:
        reportar(OK, nombre, url)
    except ssl.SSLError as e:
        reportar(FALTA if obligatorio else AVISO, nombre, f"error de certificado: {e.reason}",
                 "Probable inspección TLS del proxy corporativo: pida a TI el certificado raíz (ver guía, sección TI).")
    except (urllib.error.URLError, socket.timeout, OSError) as e:
        motivo = getattr(e, "reason", e)
        reportar(FALTA if obligatorio else AVISO, nombre, f"sin conexión ({motivo})",
                 "Pida a TI habilitar este dominio en el proxy o firewall.")


def copilot_integrado() -> bool:
    """Busca Copilot entre las extensiones que trae la instalación de VS Code.

    Se parte de la ubicación del comando `code` y se sube por sus carpetas buscando
    `resources/app/extensions` (Windows y Linux) o `Resources/app/extensions` (macOS),
    incluida la subcarpeta por versión que usan las instalaciones recientes en Windows.
    """
    from pathlib import Path

    exe = shutil.which("code")
    if not exe:
        return False
    try:
        ruta = Path(exe).resolve()
    except OSError:
        return False
    candidatas: list[Path] = []
    for carpeta in list(ruta.parents)[:5]:
        candidatas += [carpeta / "resources" / "app" / "extensions",
                       carpeta / "Resources" / "app" / "extensions"]
        if carpeta.name == "app":
            candidatas.append(carpeta / "extensions")
        try:
            candidatas += list(carpeta.glob("*/resources/app/extensions"))
        except OSError:
            pass
    for ext_dir in candidatas:
        try:
            if ext_dir.is_dir() and any("copilot" in d.name.lower() for d in ext_dir.iterdir() if d.is_dir()):
                return True
        except OSError:
            continue

    # Copilot Chat aparece como "Built-in" pero VS Code lo descarga y lo guarda en la
    # carpeta de datos del usuario, no en la instalación. Se busca "github.copilot-chat"
    # (su identificador) en esas carpetas, con profundidad limitada.
    inicio = Path.home()
    datos = [inicio / ".vscode" / "extensions",
             inicio / "Library" / "Application Support" / "Code",
             inicio / ".config" / "Code"]
    if os.getenv("APPDATA"):
        datos.append(Path(os.environ["APPDATA"]) / "Code")
    if os.getenv("LOCALAPPDATA"):
        datos.append(Path(os.environ["LOCALAPPDATA"]) / "Programs" / "Microsoft VS Code")
    for raiz in datos:
        if _contiene(raiz, "github.copilot-chat", profundidad=4):
            return True
    return False


def _contiene(raiz, texto: str, profundidad: int) -> bool:
    """True si algún archivo o carpeta bajo `raiz` (hasta `profundidad` niveles) tiene `texto` en el nombre."""
    pendientes = [(raiz, 0)]
    vistos = 0
    while pendientes:
        carpeta, nivel = pendientes.pop()
        try:
            for hijo in carpeta.iterdir():
                vistos += 1
                if vistos > 20_000:  # evita recorrer carpetas enormes
                    return False
                if texto in hijo.name.lower():
                    return True
                if nivel < profundidad and hijo.is_dir() and not hijo.is_symlink():
                    pendientes.append((hijo, nivel + 1))
        except OSError:
            continue
    return False


def nucleo() -> None:
    print("\n1. Sistema")
    so = f"{platform.system()} {platform.release()} ({platform.machine()})"
    reportar(OK, "Sistema operativo", so)
    v = sys.version_info
    if v < (3, 10):
        reportar(FALTA, "Python", f"versión {v.major}.{v.minor}", "Instale Python 3.12 (python.org).")
    else:
        reportar(OK, "Python", f"versión {v.major}.{v.minor}.{v.micro}")
    if WINDOWS:
        requerir("PowerShell 7", ["pwsh", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"],
                 (7, 0), "Copilot CLI necesita PowerShell 6 o superior: winget install Microsoft.PowerShell")

    print("\n2. Herramientas base")
    requerir("Git", ["git", "--version"], (2, 30), "Windows: winget install Git.Git · macOS: xcode-select --install")
    requerir("Node.js", ["node", "--version"], (22, 0),
             "Opcional: solo si instala Copilot CLI con npm (Node.js 22 LTS, nodejs.org).",
             obligatorio=False)

    print("\n3. Editor")
    code = requerir("VS Code", ["code", "--version"], (1, 100),
                    "Instale VS Code (code.visualstudio.com) y marque 'Agregar a PATH'.")
    if code:
        ext = (ejecutar("code", "--list-extensions") or "").lower().split()
        # En versiones recientes de VS Code el chat de Copilot viene integrado y ya no
        # aparece en --list-extensions; por eso su ausencia es un aviso, no un faltante.
        if {"github.copilot-chat", "github.copilot"} & set(ext):
            reportar(OK, "Copilot Chat", "extensión instalada")
        elif copilot_integrado():
            reportar(OK, "Copilot Chat", "integrado en VS Code")
        else:
            reportar(AVISO, "Copilot Chat", "no aparece como extensión (puede venir integrado)",
                     "Abra VS Code: si ve el panel 'Chat' y el ícono de Copilot en la barra inferior, está listo. "
                     "Si no, instale 'GitHub Copilot Chat' desde Extensiones.")
        reportar(OK if "anthropic.claude-code" in ext else AVISO, "Extensión Claude Code",
                 "instalada" if "anthropic.claude-code" in ext else "no instalada (recomendada)",
                 "En VS Code: Extensiones → 'Claude Code' (Anthropic). Da el panel de Claude Code dentro del editor.")
        reportar(OK if "ms-python.python" in ext else FALTA, "Extensión Python",
                 "instalada" if "ms-python.python" in ext else "no instalada",
                 "En VS Code: Extensiones → 'Python' (Microsoft).")

    print("\n4. Asistentes de IA")
    requerir("GitHub Copilot CLI", ["copilot", "version"], None,
             "winget install GitHub.Copilot · o: npm install -g @github/copilot · luego ejecute 'copilot' y /login")
    requerir("Claude Code", ["claude", "--version"], (2, 0),
             "Windows: irm https://claude.ai/install.ps1 | iex · macOS/Linux: curl -fsSL https://claude.ai/install.sh | bash")

    print("\n5. Paquetes de Python del curso")
    faltan = [p for p in ("numpy", "pytest", "tiktoken") if importlib.util.find_spec(p) is None]
    if faltan:
        reportar(FALTA, "numpy, pytest, tiktoken", "faltan: " + ", ".join(faltan),
                 "Active su entorno virtual y ejecute: pip install -r requirements.txt")
    else:
        reportar(OK, "numpy, pytest, tiktoken", "instalados")
    if sys.prefix == sys.base_prefix:
        reportar(AVISO, "Entorno virtual", "no activo",
                 "Recomendado: python -m venv .venv y activarlo antes de instalar paquetes.")
    else:
        reportar(OK, "Entorno virtual", "activo")

    print("\n6. Conexión a los servicios")
    red("GitHub (Copilot)", "https://api.github.com")
    # Opcionales: si la organización usa Claude Code a través de un proveedor de nube
    # (Bedrock, Foundry, Vertex) o un gateway, el tráfico va a ese proveedor y no aquí.
    red("Anthropic (Claude Code)", "https://api.anthropic.com", obligatorio=False)
    red("Inicio de sesión Claude", "https://platform.claude.com", obligatorio=False)
    red("PyPI (paquetes Python)", "https://pypi.org/simple/")
    red("Vocabulario de tiktoken", "https://openaipublic.blob.core.windows.net", obligatorio=False)


def main() -> int:
    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()

    print("IA para Desarrolladores · verificación del entorno")
    nucleo()

    faltan = [r for r in resultados if r[0] == FALTA]
    avisos = [r for r in resultados if r[0] == AVISO]
    print("\n" + "=" * 64)
    if not faltan:
        print("Listo para el curso." + (f" ({len(avisos)} aviso(s) opcional(es))" if avisos else ""))
        print("Último paso: inicie sesión en Copilot (VS Code y 'copilot') y en Claude Code ('claude').")
    else:
        print(f"Faltan {len(faltan)} requisito(s):")
        for _, nombre, detalle, _ in faltan:
            print(f"  - {nombre}: {detalle}")
        print("Revise la guía de preparación o envíe una captura de esta pantalla por el canal del curso.")
    return 1 if faltan else 0


if __name__ == "__main__":
    sys.exit(main())
