# Repositorio del equipo · Banco Orquídea (ficticio)

Punto de partida de cada equipo del curso **IA para Desarrolladores**. Trae el agente del equipo en su versión inicial, para Claude Code y para GitHub Copilot.

| Archivo | Qué es | Lo lee |
|---|---|---|
| `banco.yaml` | Definiciones del banco ficticio: productos, límites, datos, convenciones | Las reglas y las skills |
| `AGENTS.md` | Reglas del equipo y ciclo de trabajo | Copilot (y Claude Code vía `CLAUDE.md`) |
| `CLAUDE.md` | Entrada de Claude Code: importa `AGENTS.md` y `banco.yaml` | Claude Code |
| `.github/copilot-instructions.md` | Entrada de Copilot | Copilot |
| `.claude/skills/` | Skills del equipo (fuente) | Claude Code |
| `.github/skills/` | Copia de las skills para Copilot | Copilot |
| `docs/sdlc/` | Artefactos de cada caso de uso | Todos |
| `herramientas/` | `verificar_equipo.py` y `sincronizar_skills.py` | Ustedes |

## Primeros pasos

```bash
python herramientas/verificar_equipo.py
```

Luego, en su asistente, escriba `/intencion` seguido de la idea de su reto.

> Todo lo que hay aquí es ficticio. Al terminar el curso, el banco reemplaza `banco.yaml` y `AGENTS.md` con sus propias definiciones.
