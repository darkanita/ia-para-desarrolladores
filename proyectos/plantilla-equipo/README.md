# Repositorio del equipo · Banco Orquídea (ficticio)

Punto de partida de cada persona (y, desde la sesión 5, de cada equipo) en el curso **IA para Desarrolladores**. Trae el agente del equipo, para Claude Code y para GitHub Copilot. Esta es la **versión 2** (sesión 4).

| Archivo | Qué es | Lo lee |
|---|---|---|
| `banco.yaml` | Definiciones del banco ficticio: productos, límites, datos, convenciones, glosario, políticas y catálogo de servicios | Las reglas, las skills y el servidor MCP |
| `AGENTS.md` | Reglas del equipo y ciclo de trabajo | Copilot (y Claude Code vía `CLAUDE.md`) |
| `CLAUDE.md` | Entrada de Claude Code: importa `AGENTS.md` | Claude Code |
| `.github/copilot-instructions.md` | Entrada de Copilot | Copilot |
| `.claude/skills/` | Skills del equipo: `intencion`, `spec`, `plan-tecnico` (fuente) | Claude Code |
| `.github/skills/` | Copia de las skills para Copilot | Copilot |
| `.claude/rules/` | Reglas por tipo de archivo: capas, pruebas, APIs, ETL, artefactos (fuente) | Claude Code |
| `.claude/agents/` · `.github/agents/` | Agentes por rol: arquitecto y desarrollador | Claude Code · Copilot |
| `.github/instructions/` | Copia de las reglas para Copilot | Copilot |
| `.mcp.json` · `.vscode/mcp.json` | Conexión al servidor MCP del banco | Claude Code · Copilot |
| `docs/sdlc/` | Artefactos de cada caso de uso | Todos |
| `herramientas/` | `verificar_equipo.py`, `sincronizar_skills.py`, `configurar_mcp.py`, `crear_estructura.py`, `verificar_capas.py` y el servidor `mcp_banco/` | Ustedes |

## Primeros pasos

Con el entorno del curso activo:

```bash
python herramientas/configurar_mcp.py
python herramientas/verificar_equipo.py
```

Luego, en su asistente: `/intencion` con la idea de su reto; con la intención aprobada, `/spec`; con la especificación aprobada, el agente arquitecto y `/plan-tecnico`; y con el plan aprobado, el agente desarrollador.

Si cambia una skill o una regla en `.claude/`, ejecute `python herramientas/sincronizar_skills.py` para llevarla a Copilot.

> Todo lo que hay aquí es ficticio. Al terminar el curso, el banco reemplaza `banco.yaml` y `AGENTS.md` con sus propias definiciones.
