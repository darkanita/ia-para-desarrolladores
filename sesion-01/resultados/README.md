# Resultados de la sesión 1

Dos carpetas con el mismo punto de partida: los requisitos del simulador de crédito y las reglas del equipo. En clase, cada asistente construye la aplicación en la suya.

| Carpeta | Asistente | Archivo de reglas que lee |
|---|---|---|
| `simulador-copilot/` | GitHub Copilot Chat (agente Agent) | `AGENTS.md` |
| `simulador-claude-code/` | Claude Code CLI | `CLAUDE.md` → `AGENTS.md` |

El código se guarda tal como lo dejó cada asistente, sin corregirlo: sirve para compararlos en la sesión 2.

Para abrir cualquiera de las dos aplicaciones (con el entorno del curso activo y `streamlit` instalado):

```bash
cd sesion-01/resultados/simulador-copilot      # o simulador-claude-code
python -m pytest -q
streamlit run app.py
```
