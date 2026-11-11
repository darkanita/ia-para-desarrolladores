# Sesión 6 — Transformar: probar la especificación y automatizar con hooks

**Módulo 4 · 2 horas**

## Objetivo
Comprobar que lo que pide la especificación está probado, no solo que "las pruebas pasan". El agente **Verificador** arma la matriz criterio → prueba, escribe las pruebas que faltan con **datos sintéticos** que genera el banco y reporta los posibles defectos sin tocar el código. Y los **hooks** hacen que la regla de capas y las pruebas se corran solas después de cada edición: una regla aconseja, un hook obliga.

## Agenda

| Tiempo | Bloque | Material |
|---|---|---|
| 0:00 – 0:10 | Repaso: su pull request fusionado. Poner al día (v4) | `mi-reto` |
| 0:10 – 0:25 | Probar la especificación: matriz criterio → prueba, cobertura, datos sintéticos | Presentación · `mi-reto` |
| 0:25 – 0:50 | Demo: el agente Verificador y `/pruebas` encuentran tres huecos en lo que ve el asesor del simulador | `demo-equipo` |
| 0:50 – 1:15 | Hooks: qué son, dónde viven y demo del hook que no deja romper la regla de capas | `demo-equipo` |
| 1:15 – 1:45 | **Práctica:** `/pruebas` sobre su reto en una rama, con el hook encendido, y su pull request | [`TAREA.md`](TAREA.md) |
| 1:45 – 2:00 | Preguntas, tarea y cierre | Presentación |

## Lo nuevo en el agente del equipo (versión 4)

| Pieza | Claude Code | Copilot |
|---|---|---|
| Agente **verificador** (matriz y pruebas que faltan; no toca `src/`) | `.claude/agents/verificador.md` | `.github/agents/verificador.agent.md` |
| Skill `/pruebas` y su plantilla `pruebas.md` | `.claude/skills/pruebas/` | `.github/skills/pruebas/` |
| Herramienta `datos_sinteticos` | servidor MCP `banco` | servidor MCP `banco` |
| Hook del equipo: capas y pruebas después de cada edición | `.claude/settings.json` | `.github/hooks/verificar-cambio.json` |
| El script del hook | `herramientas/hooks/verificar_cambio.py` | el mismo |
| Posibles defectos marcados con `xfail` estricto | `politicas.pruebas` · regla de pruebas | el mismo |

## Antes de la clase
1. Traiga el material nuevo del curso: descargue el `.zip` nuevo y descomprímalo **sobre** la carpeta del curso (o `git pull`).
2. Instale `pytest-cov` en el entorno del curso: `pip install pytest-cov`.
3. Traiga su pull request de la sesión 5 fusionado (o abierto, si le quedaron hallazgos).

## Práctica en clase y tarea
[`TAREA.md`](TAREA.md) tiene el paso a paso.
