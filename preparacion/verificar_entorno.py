"""Verifica que su máquina esté lista para el curso IA para Desarrolladores.

Uso (desde la carpeta del curso):
    python preparacion/verificar_entorno.py              # núcleo común
    python preparacion/verificar_entorno.py --track backend
    python preparacion/verificar_entorno.py --track frontend
    python preparacion/verificar_entorno.py --track datos

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
             "Instale Node.js 22 LTS (nodejs.org). Necesario para instalar Copilot CLI con npm y para el track frontend.",
             obligatorio=False)

    print("\n3. Editor")
    code = requerir("VS Code", ["code", "--version"], (1, 100),
                    "Instale VS Code (code.visualstudio.com) y marque 'Agregar a PATH'.")
    if code:
        ext = (ejecutar("code", "--list-extensions") or "").lower().split()
        for ident, nombre, ayuda in [
            ("github.copilot-chat", "Extensión Copilot Chat", "En VS Code: Extensiones → 'GitHub Copilot Chat'."),
            ("ms-python.python", "Extensión Python", "En VS Code: Extensiones → 'Python' (Microsoft)."),
        ]:
            reportar(OK if ident in ext else FALTA, nombre, "instalada" if ident in ext else "no instalada", ayuda)

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


def track(nombre: str) -> None:
    print(f"\n7. Track {nombre}")
    if nombre == "backend":
        requerir("Java (JDK)", ["java", "-version"], (17, 0), "Instale un JDK 17 o 21 (por ejemplo Eclipse Temurin).")
        red("Maven Central", "https://repo.maven.apache.org/maven2/")
        red("Gradle Plugin Portal", "https://plugins.gradle.org/m2/")
    elif nombre == "frontend":
        requerir("Node.js", ["node", "--version"], (22, 0), "Instale Node.js 22 LTS (nodejs.org).")
        requerir("npm", ["npm", "--version"], (10, 0), "Viene con Node.js 22.")
        red("Registro npm", "https://registry.npmjs.org")
    elif nombre == "datos":
        reportar(OK, "Python", "ya verificado en el núcleo")
        red("PyPI", "https://pypi.org/simple/")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--track", choices=["backend", "frontend", "datos"], help="verificar además los requisitos de su track")
    args = p.parse_args()

    print("IA para Desarrolladores · verificación del entorno")
    nucleo()
    if args.track:
        track(args.track)

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
