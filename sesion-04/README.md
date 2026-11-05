# Sesión 4 — Hacer: del plan al primer componente

**Módulo 4 · 2 horas**

## Objetivo
Pasar de la especificación aprobada al código con dos agentes por rol: el **Arquitecto**, que planea sin tocar código, y el **Desarrollador**, que implementa el plan aprobado con la prueba primero, sobre una estructura por capas.

## Agenda

| Tiempo | Bloque | Material |
|---|---|---|
| 0:00 – 0:10 | Repaso y aprobación del `spec.md` | Presentación |
| 0:10 – 0:30 | Su repositorio: poner al día con `poner_al_dia.sh`; qué es una regla y las reglas del equipo (`.claude/rules`); el servidor del banco (`.mcp.json`, `banco.yaml`) | `mi-reto` |
| 0:30 – 0:40 | La estructura por capas: dominio, puertos, casos de uso, adaptadores, app | Presentación |
| 0:40 – 1:00 | Demo: el agente Arquitecto escribe el plan con `/plan-tecnico` y `validar_nombre`; se revisa y se aprueba | `proyectos/plantilla-equipo` |
| 1:00 – 1:20 | Demo: el agente Desarrollador implementa el primer componente, prueba primero | `proyectos/plantilla-equipo` |
| 1:20 – 1:50 | **Práctica:** cada persona escribe y aprueba su `plan.md` y arranca el primer paso | [`TAREA.md`](TAREA.md) |
| 1:50 – 2:00 | Preguntas, tarea y cierre | Presentación |

## Lo nuevo en el agente del equipo (versión 2)

| Pieza | Claude Code | Copilot |
|---|---|---|
| Agente **arquitecto** (lee y planea; solo escribe `plan.md`) | `.claude/agents/arquitecto.md` | `.github/agents/arquitecto.agent.md` |
| Agente **desarrollador** (implementa el plan, prueba primero) | `.claude/agents/desarrollador.md` | `.github/agents/desarrollador.agent.md` |
| Skill `/plan-tecnico` | `.claude/skills/plan-tecnico/` | `.github/skills/plan-tecnico/` |
| Herramienta `validar_nombre` | servidor MCP `banco` | servidor MCP `banco` |
| Regla de capas y su verificador | `.claude/rules/capas.md` · `herramientas/verificar_capas.py` | `.github/instructions/capas.instructions.md` |
| Estructura del proyecto por capas | `herramientas/crear_estructura.py` | (el mismo) |

## Antes de la clase
1. Traiga el material nuevo del curso: descargue el `.zip` nuevo y descomprímalo **sobre** la carpeta del curso (o `git pull` si clonó el repositorio).
2. Traiga su `spec.md` de la sesión 3 (si no está aprobado, lo aprueba al inicio de la clase).

## Práctica en clase y tarea
[`TAREA.md`](TAREA.md) tiene el paso a paso.
