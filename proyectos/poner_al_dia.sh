#!/usr/bin/env bash
# Pone su repositorio (mi-reto) al día con la plantilla del agente del equipo, sin perder su trabajo.
#
# Uso (Git Bash), desde la carpeta del curso, con el material nuevo:
#   bash proyectos/poner_al_dia.sh ../mi-reto
#
# Qué hace:
#   1. Guarda en commits lo que esté suelto en docs/sdlc y en las skills copiadas a mano.
#   2. Corre proyectos/actualizar_repositorio.py: agrega TODO lo que falta (reglas, skills, servidor MCP,
#      agentes...), actualiza lo que usted no tocó y deja un .nuevo al lado de lo que sí tocó.
#      Nunca toca docs/sdlc.
#   3. Muestra qué quedó, qué falta revisar y corre el verificador.
set -euo pipefail

REPO="$(cd "${1:?Falta la ruta de su repositorio, por ejemplo ../mi-reto}" && pwd)"
CURSO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

[ -d "$REPO/.git" ] || { echo "$REPO no es un repositorio git."; exit 1; }
[ -f "$CURSO/proyectos/actualizar_repositorio.py" ] || {
  echo "No encuentro proyectos/actualizar_repositorio.py en $CURSO."
  echo "Descargue el .zip nuevo del curso y descomprímalo sobre esa carpeta (o haga git pull)."; exit 1; }

# Python: el del entorno activo, o el .venv de la carpeta del curso
if [ -z "${VIRTUAL_ENV:-}" ]; then
  if   [ -f "$CURSO/.venv/Scripts/activate" ]; then source "$CURSO/.venv/Scripts/activate"
  elif [ -f "$CURSO/.venv/bin/activate" ];     then source "$CURSO/.venv/bin/activate"
  else echo "(Sin entorno activo: uso el Python del sistema. Si falla, active su .venv antes.)"; fi
fi
PY="$(command -v python || command -v python3)"
"$PY" -c "import yaml" 2>/dev/null || { echo "Falta PyYAML en el entorno: pip install pyyaml"; exit 1; }

echo "== 1. Guardar lo que está suelto"
cd "$REPO"
if [ -n "$(git status --porcelain -- docs/sdlc)" ]; then
  git add docs/sdlc && git commit -q -m "Artefactos del ciclo (estado actual)" && echo "   commit: docs/sdlc"
fi
SKILLS=""
for d in .claude/skills .github/skills; do [ -d "$d" ] && SKILLS="$SKILLS $d"; done
if [ -n "$SKILLS" ] && [ -n "$(git status --porcelain -- $SKILLS)" ]; then
  git add $SKILLS && git commit -q -m "Skills copiadas a mano" && echo "   commit: skills copiadas a mano"
fi
OTROS="$(git status --porcelain)"
if [ -n "$OTROS" ]; then
  echo "   Quedan cambios sin commit (no los toco; revíselos con git diff):"
  echo "$OTROS" | sed 's/^/     /'
fi

echo; echo "== 2. Actualizar"
"$PY" "$CURSO/proyectos/actualizar_repositorio.py" "$REPO"

echo; echo "== 3. Qué quedó"
cd "$REPO"
NUEVOS="$(find . -name '*.nuevo' -not -path './.git/*' || true)"
if [ -n "$NUEVOS" ]; then
  echo "   Archivos que usted había cambiado; la versión nueva quedó al lado. Compare y decida:"
  for f in $NUEVOS; do echo "     diff ${f%.nuevo} $f    # quedarse con el nuevo: mv $f ${f%.nuevo}"; done
fi
[ -d .claude/rules ]  && echo "   reglas:  $(ls .claude/rules | tr '\n' ' ')"
[ -d .claude/agents ] && echo "   agentes: $(ls .claude/agents | tr '\n' ' ')"
[ -f .mcp.json ]      && echo "   MCP:     .mcp.json y .vscode/mcp.json configurados"
echo
"$PY" herramientas/verificar_equipo.py || true
echo
git log --oneline -5
echo
echo "Listo. Cierre y vuelva a abrir claude en esta carpeta y escriba /mcp (debe aparecer banco)."
echo "En VS Code: recargue la ventana y dele Start a 'banco' en .vscode/mcp.json."
