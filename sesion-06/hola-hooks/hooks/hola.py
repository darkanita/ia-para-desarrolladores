"""Hola mundo de hooks: un solo script que atiende los cinco eventos más usados.

Claude Code lo llama en cada evento (ver .claude/settings.json) y le pasa por la
entrada estándar (stdin) un JSON con lo que está pasando. El script:
  - escribe una línea en hola-hooks.log para que usted vea CUÁNDO corre cada evento;
  - en algunos eventos responde algo, para que vea QUÉ puede hacer un hook.

Códigos de salida:
  0 -> todo bien, sigue.
  2 -> el mensaje que se escribe en stderr le llega a Claude (y en algunos eventos bloquea).
"""
import json
import sys
from datetime import datetime
from pathlib import Path

LOG = Path(__file__).resolve().parents[1] / "hola-hooks.log"


def anotar(texto: str) -> None:
    """Agrega una línea con la hora al archivo hola-hooks.log."""
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%H:%M:%S}  {texto}\n")


def main() -> int:
    evento = json.loads(sys.stdin.read() or "{}")
    # Claude Code y Copilot mandan casi el mismo JSON; los nombres de algunos campos cambian.
    nombre = evento.get("hook_event_name") or evento.get("hookEventName", "?")
    herramienta = evento.get("tool_name") or evento.get("toolName") or ""
    entrada = evento.get("tool_input") or evento.get("toolArgs") or {}
    if isinstance(entrada, str):
        try:
            entrada = json.loads(entrada)
        except json.JSONDecodeError:
            entrada = {"command": entrada}
    archivo = (entrada.get("file_path") or entrada.get("filePath") or entrada.get("path")
               or entrada.get("command") or "")
    es_lectura = herramienta in ("Read", "read_file", "readFile") or "read" in herramienta.lower()

    if nombre == "SessionStart":
        anotar("SessionStart      se abrió la sesión")
        # Lo que se imprime aquí, con código 0, Claude lo recibe como contexto.
        print("Dato del hook SessionStart: hoy es la sesión 6 del curso y el saludo oficial es «¡Hola, hooks!».")
        return 0

    if nombre == "UserPromptSubmit":
        prompt = evento.get("prompt", "")
        anotar(f"UserPromptSubmit  usted escribió: {prompt[:60]}")
        if "contraseña" in prompt.lower():
            print("Hook UserPromptSubmit: BLOQUEADO. No escriba contraseñas en el prompt.", file=sys.stderr)
            return 2  # el prompt no llega a Claude
        return 0

    if nombre == "PreToolUse":
        anotar(f"PreToolUse        Claude va a usar {herramienta}: {archivo}")
        if es_lectura and archivo.endswith("secreto.txt"):
            print("Hook PreToolUse: BLOQUEADO. secreto.txt no se lee. Dígale a la persona que ese archivo está protegido.",
                  file=sys.stderr)
            return 2  # la herramienta no se ejecuta
        return 0

    if nombre == "PostToolUse":
        anotar(f"PostToolUse       Claude ya usó {herramienta}: {archivo}")
        return 0  # con 2, Claude recibiría el mensaje y tendría que corregir (es el hook del equipo)

    if nombre == "Stop":
        anotar("Stop              Claude terminó de responder")
        return 0  # con 2, Claude tendría que seguir trabajando

    anotar(f"{nombre}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
