# Sesión 4 — Hacer: del plan al primer componente

**Módulo 4 · 2 horas**

## Objetivo
Pasar de la especificación aprobada al código con dos agentes por rol: el **Arquitecto**, que planea sin tocar código, y el **Desarrollador**, que implementa el plan aprobado con la prueba primero, sobre una estructura por capas.

## Agenda

| Tiempo | Bloque | Material |
|---|---|---|
| 0:00 – 0:10 | Repaso: especificaciones y reglas propias | Presentación |
| 0:10 – 0:25 | La estructura por capas: dominio, puertos, casos de uso, adaptadores, app | Presentación |
| 0:25 – 0:50 | Demo: el agente Arquitecto escribe el plan con `/plan-tecnico` y `validar_nombre`; se revisa y se aprueba | `proyectos/plantilla-equipo` |
| 0:50 – 1:15 | Demo: el agente Desarrollador implementa el primer componente, prueba primero | `proyectos/plantilla-equipo` |
| 1:15 – 1:45 | **Práctica:** cada persona actualiza su repositorio, escribe y aprueba su `plan.md` y arranca el primer paso | [`TAREA.md`](TAREA.md) |
| 1:45 – 2:00 | Preguntas, tarea y cierre | Presentación |

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
2. Tenga su `spec.md` **aprobado** de la sesión 3.

## Práctica en clase y tarea
[`TAREA.md`](TAREA.md) tiene el paso a paso.
