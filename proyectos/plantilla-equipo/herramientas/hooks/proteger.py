"""Hook de seguridad del equipo: bloquea ANTES de que el agente actúe (PreToolUse).

Lo llaman Claude Code (.claude/settings.json) y Copilot (.github/hooks/proteger.json) antes de cada
herramienta. Recibe por la entrada estándar el JSON del evento. Lee las reglas de banco.yaml
(sección `proteccion` y `convenciones.dependencias_aprobadas`) y bloquea, con código 2 y el motivo
en la salida de error, si el agente va a:

  1. leer o escribir un archivo de secretos (.env, llaves...)          proteccion.archivos_secretos
  2. hacer commit o push en una rama protegida (main)                   proteccion.ramas_protegidas
  3. ejecutar un comando destructivo (rm -rf, push --force...)          proteccion.comandos_bloqueados
  4. instalar una dependencia que no está aprobada                      convenciones.dependencias_aprobadas
  5. escribir un secreto dentro de un archivo                          proteccion.patrones_secretos
  6. (con --solo) escribir fuera de las carpetas de su rol              p. ej. el revisor solo escribe docs/

Si no hay nada que bloquear, termina en 0 sin decir nada.

Probarlo a mano (desde la raíz del repositorio):
    echo '{"tool_name": "Read", "tool_input": {"file_path": ".env"}}' | python herramientas/hooks/proteger.py
    echo '{"tool_name": "Bash", "tool_input": {"command": "pip install requests"}}' | python herramientas/hooks/proteger.py
    echo '{"tool_name": "Write", "tool_input": {"file_path": "src/x.py"}}' | python herramientas/hooks/proteger.py --solo docs
"""
from __future__ import annotations

import fnmatch
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

# Si no se puede leer banco.yaml, el hook protege igual con estas reglas mínimas.
POR_DEFECTO: dict[str, Any] = {
    "archivos_secretos": [".env", ".env.*", "*.pem", "*.key", "id_rsa*"],
    "archivos_permitidos": [".env.example"],
    "ramas_protegidas": ["main"],
    "comandos_bloqueados": [{"patron": r"rm\s+-[a-z]*r[a-z]*f|git\s+push\b.*(--force\b|\s-f\b)|git\s+reset\s+--hard",
                             "motivo": "comando destructivo"}],
    "patrones_secretos": [{"nombre": "llave privada", "patron": r"-----BEGIN [A-Z ]*PRIVATE KEY-----"}],
}
HERRAMIENTAS_QUE_ESCRIBEN = {
    "write", "edit", "multiedit", "notebookedit",                                   # Claude Code
    "create_file", "createfile", "replace_string_in_file", "multi_replace_string_in_file",
    "insert_edit_into_file", "edit_file", "editfiles", "apply_patch", "edit_notebook_file",  # Copilot
}
CLAVES_DE_CONTENIDO = {"content", "new_string", "newstring", "new_str", "newcode", "code", "text", "input", "patch"}
CLAVES_DE_COMANDO = {"command", "cmd", "commandline"}


def raiz_proyecto() -> Path:
    """La raíz del repositorio: la que dice Claude Code, la carpeta actual o la de este archivo."""
    for candidata in (os.environ.get("CLAUDE_PROJECT_DIR"), os.getcwd(), str(Path(__file__).resolve().parents[2])):
        if candidata and (Path(candidata) / "banco.yaml").exists():
            return Path(candidata).resolve()
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()


RAIZ = raiz_proyecto()


def reglas() -> tuple[dict[str, Any], list[str]]:
    try:
        import yaml  # PyYAML

        banco = yaml.safe_load((RAIZ / "banco.yaml").read_text(encoding="utf-8")) or {}
    except Exception:  # sin PyYAML o sin banco.yaml: reglas mínimas
        return POR_DEFECTO, []
    return {**POR_DEFECTO, **(banco.get("proteccion") or {})}, list(
        (banco.get("convenciones") or {}).get("dependencias_aprobadas") or [])


# --------------------------------------------------------------------------- leer el evento

def recorrer(valor: Any, clave: str, comandos: list[str], rutas: list[str], contenidos: list[str]) -> None:
    if isinstance(valor, dict):
        for k, v in valor.items():
            recorrer(v, str(k), comandos, rutas, contenidos)
    elif isinstance(valor, list):
        for v in valor:
            recorrer(v, clave, comandos, rutas, contenidos)
    elif isinstance(valor, str):
        c = clave.lower().replace("-", "_")
        if c in CLAVES_DE_COMANDO:
            comandos.append(valor)
        elif "path" in c or "file" in c:
            rutas.append(valor)
        elif c.replace("_", "") in {x.replace("_", "") for x in CLAVES_DE_CONTENIDO}:
            contenidos.append(valor)


def leer_evento(texto: str) -> tuple[str, list[str], list[str], list[str]]:
    """Devuelve (herramienta, comandos, rutas, contenidos), venga el evento de Claude Code o de Copilot."""
    evento = json.loads(texto or "{}")
    if not isinstance(evento, dict):
        return "", [], [], []
    herramienta = str(evento.get("tool_name") or evento.get("toolName") or "")
    entrada = evento.get("tool_input", evento.get("toolArgs", {}))
    if isinstance(entrada, str):
        try:
            entrada = json.loads(entrada)
        except json.JSONDecodeError:
            entrada = {"command": entrada}
    comandos: list[str] = []
    rutas: list[str] = []
    contenidos: list[str] = []
    recorrer(entrada, "", comandos, rutas, contenidos)
    return herramienta, comandos, rutas, contenidos


# --------------------------------------------------------------------------- reglas

def relativa(ruta: str) -> str:
    p = Path(ruta)
    try:
        return (p if p.is_absolute() else RAIZ / p).resolve().relative_to(RAIZ).as_posix()
    except (ValueError, OSError):
        return p.as_posix()


def es_secreto(ruta: str, r: dict[str, Any]) -> bool:
    rel = relativa(ruta)
    nombre = Path(rel).name
    if any(fnmatch.fnmatch(nombre, p) or fnmatch.fnmatch(rel, p) for p in r["archivos_permitidos"]):
        return False
    return any(fnmatch.fnmatch(nombre, p) or fnmatch.fnmatch(rel, p) for p in r["archivos_secretos"])


def palabras(comando: str) -> list[str]:
    try:
        return shlex.split(comando, posix=True)
    except ValueError:
        return comando.split()


def rama_actual() -> str:
    try:
        r = subprocess.run(["git", "branch", "--show-current"], cwd=RAIZ, capture_output=True, text=True, timeout=5)
        return r.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def normalizar_paquete(p: str) -> str:
    return re.split(r"[=<>!~\[; ]", p, maxsplit=1)[0].strip().lower().replace("_", "-")


def paquetes_no_aprobados(comando: str, aprobadas: list[str]) -> list[str]:
    m = re.search(r"\bpip3?\s+install\b(.*)", comando)
    if not m:
        return []
    aprobados = {normalizar_paquete(a) for a in aprobadas}
    fuera: list[str] = []
    saltar = False
    for w in palabras(m.group(1)):
        if saltar:
            saltar = False
            continue
        if w in ("-r", "--requirement", "-e", "--editable", "-c", "--constraint", "-i", "--index-url", "-t", "--target"):
            saltar = True
            continue
        if w.startswith("-") or "/" in w or "\\" in w or w in (".", "..") or w.endswith((".txt", ".whl")):
            continue
        if re.search(r"[;&|]", w):
            break
        nombre = normalizar_paquete(w)
        if nombre and nombre not in aprobados:
            fuera.append(nombre)
    return fuera


def revisar(herramienta: str, comandos: list[str], rutas: list[str], contenidos: list[str],
            solo: list[str]) -> tuple[str, str] | None:
    """Devuelve (motivo, qué hacer) si hay que bloquear, o None."""
    r, aprobadas = reglas()

    for ruta in rutas:
        if es_secreto(ruta, r):
            return (f"'{relativa(ruta)}' es un archivo de secretos (proteccion.archivos_secretos)",
                    "El agente no lee ni escribe secretos. Si necesita saber qué variables existen, use .env.example "
                    "(sin valores). Si hay que cambiar un secreto, lo hace una persona.")

    for comando in comandos:
        for w in palabras(comando):
            if es_secreto(w, r):
                return (f"el comando usa '{w}', un archivo de secretos (proteccion.archivos_secretos)",
                        "El agente no lee ni copia secretos. Use .env.example (sin valores).")
        for regla in r["comandos_bloqueados"]:
            if re.search(regla["patron"], comando):
                return (f"comando bloqueado: {regla.get('motivo', 'comando peligroso')} (proteccion.comandos_bloqueados)",
                        "Si de verdad hace falta, que lo ejecute una persona en su terminal, sabiendo lo que hace.")
        if re.search(r"\bgit\b.*\b(commit|push|merge)\b", comando):
            rama = rama_actual()
            protegidas = r["ramas_protegidas"]
            hacia_protegida = re.search(r"\bgit\b.*\bpush\b.*[\s:](" + "|".join(map(re.escape, protegidas)) + r")\b", comando)
            if rama in protegidas or hacia_protegida:
                return (f"commit o push directo en '{rama if rama in protegidas else 'main'}', que es una rama protegida "
                        "(proteccion.ramas_protegidas)",
                        "Cree una rama (convenciones.ramas): git switch -c <tipo>/<caso>-<descripcion>. "
                        "Todo entra a main por un pull request revisado.")
        fuera = paquetes_no_aprobados(comando, aprobadas)
        if fuera:
            return (f"dependencia no aprobada: {', '.join(fuera)} (convenciones.dependencias_aprobadas)",
                    "Una dependencia nueva la aprueba el líder técnico (politicas.seguridad). Mientras tanto, "
                    "use la librería estándar o una dependencia aprobada.")

    for contenido in contenidos:
        for patron in r["patrones_secretos"]:
            if re.search(patron["patron"], contenido):
                return (f"el contenido tiene un {patron.get('nombre', 'secreto')} (proteccion.patrones_secretos)",
                        "Los secretos viven en variables de entorno: léalos con os.environ['NOMBRE'] y documente la "
                        "variable, sin valor, en .env.example.")

    escribe = herramienta.lower() in HERRAMIENTAS_QUE_ESCRIBEN or bool(contenidos)
    if solo and escribe:
        for ruta in rutas:
            rel = relativa(ruta)
            if not any(rel == d or rel.startswith(d.rstrip("/") + "/") for d in solo):
                return (f"este agente solo escribe en {', '.join(d + '/' for d in solo)} y quiso escribir '{rel}'",
                        "Proponga el cambio en su documento (por ejemplo, como hallazgo o sugerencia) y que lo haga "
                        "el agente desarrollador.")
    return None


def main(argv: list[str]) -> int:
    for flujo in (sys.stdin, sys.stdout, sys.stderr):  # consola de Windows (cp1252): tildes y símbolos sin error
        try:
            flujo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    solo: list[str] = []
    if "--solo" in argv:
        i = argv.index("--solo")
        solo = [d.strip().strip("/") for d in (argv[i + 1] if i + 1 < len(argv) else "").split(",") if d.strip()]
    try:
        herramienta, comandos, rutas, contenidos = leer_evento(sys.stdin.read())
    except json.JSONDecodeError:
        return 0
    bloqueo = revisar(herramienta, comandos, rutas, contenidos, solo)
    if bloqueo:
        motivo, que_hacer = bloqueo
        print(f"Hook de seguridad del equipo: BLOQUEADO. Motivo: {motivo}.\nQué hacer: {que_hacer}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(main(sys.argv[1:]))
