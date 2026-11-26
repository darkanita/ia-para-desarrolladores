# Sesión 7 — Transformar: seguridad con agentes

**Módulo 4 · 2 horas**

## Objetivo
Un agente que programa también puede **leer** lo que no debe (secretos), **hacer** lo que no debe (commit en `main`, comandos destructivos, dependencias sin aprobar) y **escribir** código que pasa las pruebas pero es inseguro. Hoy, todos en `demo-clase` con el simulador de la docente, el agente del equipo suma un **agente de seguridad** que revisa con la lista OWASP Top 10 y las políticas del banco, la **revisión cruzada** (lo que escribió un asistente lo revisa otro) y **hooks que bloquean antes de actuar**.

## Agenda

| Tiempo | Bloque | Material |
|---|---|---|
| 0:00 – 0:15 | Repaso: `demo-clase` al día y el commit de un compañero que pasa todas las pruebas | `demo-clase` |
| 0:15 – 0:30 | Seguridad con agentes: tres riesgos nuevos, OWASP Top 10 y secretos | Presentación |
| 0:30 – 0:40 | El agente de seguridad y la revisión cruzada | Presentación |
| 0:40 – 1:00 | Bloqueos: permisos y hooks en Claude Code y en Copilot; **hola mundo de permisos, todos a la vez**; del hola mundo de hooks al hook de seguridad `proteger.py`; casos de uso | Presentación · [`hola-permisos/`](hola-permisos/) |
| 1:00 – 1:45 | **Demos, todos a la vez:** cinco cosas que el agente ya no puede hacer, `/seguridad` encuentra cinco problemas, corregir y revisión cruzada | `demo-clase` · [`TAREA.md`](TAREA.md) |
| 1:45 – 2:00 | Pull request, tarea y cierre | Presentación |

## Lo nuevo en el agente del equipo (sesión 7)

| Pieza | Claude Code | Copilot |
|---|---|---|
| Agente **seguridad** (OWASP Top 10, secretos, datos restringidos; no corrige ni lee secretos) | `.claude/agents/seguridad.md` | `.github/agents/seguridad.agent.md` |
| Skill `/seguridad` y su plantilla `seguridad.md` | `.claude/skills/seguridad/` | `.github/skills/seguridad/` |
| Hook de seguridad **antes** de actuar: secretos, `main`, comandos destructivos, dependencias, secretos en el código | `.claude/settings.json` (PreToolUse) | `.github/hooks/proteger.json` |
| El script del hook, que lee sus reglas de `banco.yaml` (`proteccion`) | `herramientas/hooks/proteger.py` | el mismo |
| Permisos denegados: `.env`, llaves y comandos destructivos | `.claude/settings.json` (`permissions.deny`) | — (lo cubre el hook) |
| Hooks por rol: arquitecto, revisor y seguridad solo escriben en `docs/`; verificador en `tests/` y `docs/` | frontmatter de `.claude/agents/` | frontmatter de `.github/agents/` (vista previa) |
| Búsqueda de secretos en archivos y en la historia de git | `herramientas/buscar_secretos.py` | el mismo |
| Políticas nuevas: nunca `eval`, TLS verificado, revisión cruzada, un secreto en git se rota | `banco.yaml` · `politicas.seguridad` | el mismo |

## Antes de la clase
1. Traiga el material nuevo del curso: descargue el `.zip` nuevo y descomprímalo **sobre** la carpeta del curso (o `git pull`).
2. Tenga su `demo-clase` de la sesión 6 sin cambios pendientes (`git status` limpio). En clase lo ponemos al día con un comando:

   ```bash
   python proyectos/nivelar_clase.py ../demo-clase --sesion 7
   ```

   No lo borra: deja sus ramas de la sesión 6, actualiza el agente del equipo con lo de la sesión 7 y agrega el commit de un compañero. Si no tiene `demo-clase`, el mismo comando lo crea.

## Práctica en clase y tarea
[`TAREA.md`](TAREA.md) tiene el paso a paso: en clase, en `demo-clase`, todos a la vez; en casa, lo mismo en `mi-reto` (sección «En casa»).
