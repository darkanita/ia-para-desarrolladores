# Reglas del equipo · Banco Orquídea (ficticio)

Este repositorio pertenece a un equipo de desarrollo del **Banco Orquídea**, un banco ficticio del curso. Las definiciones del banco (productos, límites, clasificación de datos, convenciones) están en `banco.yaml`: léalo antes de proponer reglas de negocio y nunca invente valores que deberían salir de ahí.

## Cómo trabajamos: el ciclo AI SDLC
Cada caso de uso pasa por etapas y cada etapa deja un artefacto en `docs/sdlc/<caso>/`:
`intent.md` → `spec.md` → `plan.md` → código y pruebas → `revision.md` → solicitud de cambio.
- Usted (el asistente) redacta y propone; **una persona aprueba** cada artefacto cambiando su `Estado` a `aprobado`.
- No pase a la etapa siguiente si el artefacto anterior no está aprobado. Si falta, dígalo y ofrezca crearlo.
- No escriba código de producción sin un `plan.md` aprobado.
- Cada etapa tiene su skill: `/intencion` escribe `intent.md`, `/spec` escribe `spec.md`, `/plan-tecnico` escribe `plan.md` y `/revisar` escribe `revision.md`.

## Agentes por rol
- **arquitecto**: lee el repositorio y la especificación aprobada y escribe solo `plan.md`. No escribe código.
- **desarrollador**: implementa un `plan.md` aprobado, paso a paso y con la prueba primero.
- **depurador**: reproduce una falla con una prueba, corrige la causa raíz con el cambio mínimo y la explica.
- **revisor**: revisa los cambios de una rama y escribe solo `revision.md`, con hallazgos por severidad. No corrige ni aprueba.
- Claude Code: `claude --agent <nombre>`. Copilot: elíjalos en el selector de agentes del chat.

## Ramas y pull requests
- Nadie hace commit directo a `main`. Cada trabajo va en una rama con el formato de `convenciones.ramas` (`funcionalidad/<caso>-<descripcion>`, `correccion/<caso>-<descripcion>`).
- Los mensajes de commit siguen `convenciones.commits`: una línea en español, citando RF/RN cuando aplique.
- El título del pull request sigue `convenciones.pull_requests`: una línea en español, como un commit, que dice qué entra y por qué (nunca el nombre de la rama).
- Todo entra a `main` por un pull request con la plantilla del repositorio, revisado antes de fusionar (`politicas.revision`). Con un hallazgo bloqueante abierto no se fusiona.
- La aprobación de un artefacto también viaja en el pull request: el commit que cambia su `Estado` a `aprobado` lo hace la persona dueña, dentro de la rama.
- El asistente no hace commit, push ni merge salvo que la persona se lo pida explícitamente.

## Herramientas del banco (servidor MCP `banco`)
- `glosario`: qué significa un término de negocio. `consultar_politica`: la política sobre datos, seguridad, nombres, logs, apis, pruebas, revision o depuracion. `catalogo_servicios`: qué APIs internas ya existen y de dónde sale cada dato. `validar_nombre`: si un nombre cumple las convenciones.
- Consúltelas antes de definir un término, proponer una regla o crear un servicio nuevo, y cite lo que encontró.
- Si no están disponibles, lea `glosario`, `politicas` y `catalogo_servicios` en `banco.yaml`.

## Stack y estructura
- Python 3.12. Estructura por capas en `src/<paquete>/`: `dominio`, `puertos`, `casos_uso`, `adaptadores`, `app` (se crea con `python herramientas/crear_estructura.py <paquete>`). El dominio no importa frameworks; el detalle está en la regla de capas.
- Antes de dar algo por terminado: `python herramientas/verificar_capas.py` debe decir OK.
- Dependencias: solo las de `convenciones.dependencias_aprobadas` en `banco.yaml`. Para otra, pregunte.

## Código
- Nombres en español y `snake_case`; clases en `PascalCase`.
- Dinero en `decimal.Decimal`, redondeo al peso con `ROUND_HALF_UP`. Nunca `float`.
- Tasas efectivas anuales (E.A.); mensual = `(1 + ea) ** (1/12) - 1`, nunca `ea / 12`.
- Funciones con anotaciones de tipo y docstring corto en español.

## Pruebas
- `pytest`, una prueba por regla de negocio, con valores esperados calculados aparte.
- Antes de dar algo por terminado: `python -m pytest -q`.

## Datos y seguridad
- Solo datos sintéticos. Nada de cédulas, cuentas, tarjetas ni nombres reales.
- No lea ni escriba secretos (`.env`, llaves). No los incluya en prompts, logs ni código.

## Reglas por tipo de archivo
Hay reglas que solo aplican a ciertos archivos (capas, pruebas, APIs, ETL, artefactos del ciclo). Viven en `.claude/rules/` y se copian a `.github/instructions/` para Copilot.

## Contexto y tokens
- Lea solo los archivos que la tarea necesita; no recorra carpetas enteras ni abra archivos de datos grandes.
- Si una salida es larga (pruebas, logs), resuma lo importante en lugar de repetirla.
- Para una tarea nueva, la persona abre una conversación nueva: no arrastre contexto de la anterior.

## Comandos útiles
- `python -m pytest -q` · `python herramientas/verificar_equipo.py` · `python herramientas/sincronizar_skills.py` · `python herramientas/mcp_banco/servidor.py --probar` · `python herramientas/verificar_capas.py`
