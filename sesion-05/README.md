# Sesión 5 — Transformar: depurar y revisar en equipo

**Módulo 4 · 2 horas**

## Objetivo
Llevar el trabajo a un flujo de equipo: cada cambio en una **rama**, entra a `main` por un **pull request** en GitHub y se revisa antes de fusionarse. Dos agentes nuevos ayudan: el **Depurador**, que reproduce una falla con una prueba antes de corregirla, y el **Revisor**, que encuentra lo que las pruebas no ven y deja `revision.md` sin tocar el código.

## Agenda

| Tiempo | Bloque | Material |
|---|---|---|
| 0:00 – 0:10 | Repaso: ¿su primer componente pasa las pruebas? Todos corren `pytest` y `verificar_capas.py` | `mi-reto` |
| 0:10 – 0:30 | Del computador al equipo: poner al día (v3), ramas, pull requests y GitHub | `mi-reto` · GitHub |
| 0:30 – 0:55 | Demo: el agente Depurador corrige una falla reportada, prueba primero, y abre su pull request | `demo-simulador` |
| 0:55 – 1:20 | Demo: el agente Revisor revisa la rama de un compañero con `/revisar` | `demo-simulador` |
| 1:20 – 1:50 | **Práctica:** su `mi-reto` en GitHub, una rama, el agente que corresponda y su primer pull request revisado | [`TAREA.md`](TAREA.md) |
| 1:50 – 2:00 | Preguntas, tarea y cierre | Presentación |

## Lo nuevo en el agente del equipo (versión 3)

| Pieza | Claude Code | Copilot |
|---|---|---|
| Agente **depurador** (reproduce con una prueba, corrige la causa raíz, explica) | `.claude/agents/depurador.md` | `.github/agents/depurador.agent.md` |
| Agente **revisor** (revisa la rama; solo escribe `revision.md`) | `.claude/agents/revisor.md` | `.github/agents/revisor.agent.md` |
| Skill `/revisar` y su plantilla `revision.md` | `.claude/skills/revisar/` | `.github/skills/revisar/` |
| Ramas, commits y pull requests | `AGENTS.md` · `convenciones.ramas` y `convenciones.commits` en `banco.yaml` | el mismo |
| Políticas `revision` y `depuracion` | `consultar_politica` del servidor `banco` | el mismo |
| Plantilla del pull request | `.github/pull_request_template.md` | el mismo |

## Antes de la clase
1. Traiga el material nuevo del curso: descargue el `.zip` nuevo y descomprímalo **sobre** la carpeta del curso (o `git pull` si clonó el repositorio).
2. Tenga una **cuenta personal de GitHub** y compruebe que puede entrar a https://github.com desde el computador de la clase. Revise la sección 9 de [`preparacion/REQUISITOS_PRACTICA.md`](../preparacion/REQUISITOS_PRACTICA.md).
3. Traiga su `mi-reto` con el código de la sesión 4.

> En GitHub solo sube su `mi-reto`, que tiene datos sintéticos y nada del banco. El repositorio es **privado**.

## Práctica en clase y tarea
[`TAREA.md`](TAREA.md) tiene el paso a paso.
