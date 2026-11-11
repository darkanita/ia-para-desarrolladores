@AGENTS.md

## Notas para Claude Code
- Las definiciones del banco están en `banco.yaml`. No se importa aquí para no cargarlo en cada conversación: léalo cuando la tarea lo necesite, y para el glosario, las políticas y el catálogo use el servidor MCP `banco`.
- Las skills (`.claude/skills/`) y las reglas por tipo de archivo (`.claude/rules/`) se escriben aquí y se copian a `.github/` para Copilot con `python herramientas/sincronizar_skills.py`.
- El servidor MCP del banco se configura en `.mcp.json`; revise que esté conectado con `/mcp`.
- Los agentes por rol están en `.claude/agents/` (los de Copilot, en `.github/agents/`). Abra una sesión como uno de ellos con `claude --agent <nombre>`: arquitecto, desarrollador, depurador, verificador o revisor.
- Los hooks del proyecto están en `.claude/settings.json`; véalos con `/hooks`. Abra `claude` con el entorno del curso activo para que el hook encuentre `pytest`.
