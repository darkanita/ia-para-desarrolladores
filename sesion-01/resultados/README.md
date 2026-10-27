# Resultados de la sesión 1

Lo que construyeron los asistentes en clase, a partir de los mismos requisitos (`proyectos/simulador-credito`).

| Carpeta | Asistente | Cómo se hizo |
|---|---|---|
| `simulador-copilot/` | GitHub Copilot Chat (Agent) | Plan con `/plan`, luego implementación |
| `simulador-claude-code/` | Claude Code CLI | Modo plan, luego implementación |

El código se guarda tal como lo dejó cada asistente, sin corregirlo: sirve para compararlos en la sesión 2.

Para abrir cualquiera de las dos aplicaciones (con el entorno del curso activo y `streamlit` instalado):

```bash
cd sesion-01/resultados/simulador-copilot      # o simulador-claude-code
python -m pytest -q
streamlit run app.py
```
