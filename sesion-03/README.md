# Sesión 3 — Hacer: contexto, reglas del equipo y especificación

**Módulo 3 · 2 horas**

## Objetivo
Escribir buenos prompts y gastar menos tokens, enseñarle al agente reglas por tipo de archivo, conectarlo a las herramientas del banco por MCP y pasar de la intención a la especificación con la skill `/spec`.

## Agenda

| Tiempo | Bloque | Material |
|---|---|---|
| 0:00 – 0:10 | Repaso y aprobación de las intenciones | Presentación |
| 0:10 – 0:30 | Prompts y contexto: cómo se arma un buen prompt, qué llena la ventana y cómo gastar menos tokens | Presentación |
| 0:30 – 0:45 | Demo: reglas por tipo de archivo. Un error que se repite se vuelve regla | `proyectos/demo-reglas`, `sesion-03/demo-reglas/` |
| 0:45 – 1:00 | El servidor MCP del banco en las dos herramientas: `glosario`, `consultar_politica`, `catalogo_servicios` | `proyectos/plantilla-equipo` |
| 1:00 – 1:15 | Demo: `/spec` sobre la intención del simulador | `proyectos/plantilla-equipo` |
| 1:15 – 1:45 | **Práctica:** cada persona actualiza su repositorio y escribe el `spec.md` de su reto | [`TAREA.md`](TAREA.md) |
| 1:45 – 2:00 | Preguntas, tarea y cierre | Presentación |

## Lo nuevo en el agente del equipo (versión 1)

| Pieza | Claude Code | Copilot |
|---|---|---|
| Reglas por tipo de archivo (pruebas, APIs, ETL, artefactos) | `.claude/rules/*.md` | `.github/instructions/*.instructions.md` |
| Skill `/spec` | `.claude/skills/spec/` | `.github/skills/spec/` |
| Servidor MCP del banco | `.mcp.json` | `.vscode/mcp.json` |
| Glosario, políticas y catálogo de servicios | `banco.yaml` | `banco.yaml` |

## Antes de la clase
1. Traiga el material nuevo del curso: descargue el `.zip` nuevo y descomprímalo **sobre** la carpeta del curso, reemplazando los archivos (su `.venv` no se toca), o haga `git pull` si clonó el repositorio.
2. Tenga a mano su `mi-reto` con el `intent.md` **aprobado** de la sesión 2.

## Replicar las demos
[`REPLICAR_DEMOS.md`](REPLICAR_DEMOS.md) trae las cuatro demos de la clase paso a paso, para repetirlas en su máquina.

## Práctica en clase y tarea
[`TAREA.md`](TAREA.md) tiene el paso a paso: se empieza en clase y en casa se termina el `spec.md` y se escribe una regla propia.
