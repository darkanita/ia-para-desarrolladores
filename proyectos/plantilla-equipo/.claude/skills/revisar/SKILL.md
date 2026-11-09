---
name: revisar
description: Revisa los cambios de una rama contra la especificación, el plan, las reglas del equipo y las políticas del Banco Orquídea, y escribe docs/sdlc/<caso>/revision.md con hallazgos por severidad (bloqueante, importante, sugerencia). Úsela antes de abrir o fusionar un pull request.
argument-hint: "Nombre del caso (la carpeta en docs/sdlc) y, si no es main, la rama base"
---

# Revisar un cambio antes de fusionarlo

La revisión es la quinta etapa del ciclo AI SDLC: confirma que lo construido cumple lo aprobado y las reglas del banco, **antes** de que entre a `main`. El revisor señala; el dueño del código decide. No es una corrección.

## Pasos

1. **Ubique el caso y el cambio.** Lea `docs/sdlc/<caso>/spec.md` y `plan.md` (deben estar aprobados; si no, dígalo). Identifique la rama actual y la base (por defecto `main`) y mire el cambio:
   - `git log --oneline main..HEAD`
   - `git diff main...HEAD --stat` y luego `git diff main...HEAD` de los archivos de código y pruebas.
   Revise **solo lo que cambió**; no audite todo el repositorio.
2. **Corra la verificación automática** y anote el resultado: `python -m pytest -q` y `python herramientas/verificar_capas.py`. Si alguna falla, es un hallazgo bloqueante.
3. **Consulte al banco**, con el servidor MCP `banco`: `consultar_politica` con `revision`, `datos`, `logs`, `seguridad`, `nombres` y `pruebas`; `validar_nombre` para los nombres nuevos que le parezcan dudosos.
4. **Revise el cambio contra**:
   - la especificación: ¿cada criterio de aceptación tocado tiene su prueba? ¿alguna regla RN quedó distinta a como dice?
   - el plan: ¿el código está en la capa que dice el plan?
   - las reglas de `.claude/rules/` que apliquen a los archivos cambiados;
   - las políticas: datos restringidos en logs, mensajes o pruebas; secretos; validación de entradas; nombres; dependencias.
5. **Clasifique cada hallazgo** con `politicas.revision`: **bloqueante**, **importante** o **sugerencia**. Cada uno con archivo:línea, qué pasa, qué regla o política incumple y una sugerencia concreta. Si no hay hallazgos de un tipo, dígalo; no invente.
6. **Escriba `docs/sdlc/<caso>/revision.md`** con la plantilla `plantilla-revision.md` de esta skill, sin quitar secciones. Deje `Estado: borrador` y `Aprobado por: pendiente (dueño del código)`. Si ya existe, agregue una ronda nueva al final en lugar de borrar la anterior.
7. **Termine** con 3 líneas: cuántos hallazgos por severidad, si el pull request puede fusionarse (solo si no hay bloqueantes) y qué decide el dueño del código.

## Reglas
- No modifique código, pruebas ni configuración; las correcciones van como sugerencias.
- No apruebe, no fusione y no haga commit.
- No repita lo que ya dicen las pruebas en verde; busque lo que ellas no ven.
