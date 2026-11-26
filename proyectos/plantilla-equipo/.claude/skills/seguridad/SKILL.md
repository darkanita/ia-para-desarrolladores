---
name: seguridad
description: Revisa la seguridad de un caso de uso o de los cambios de una rama con la lista OWASP Top 10 y las políticas de seguridad, datos y logs del Banco Orquídea, y escribe docs/sdlc/<caso>/seguridad.md con hallazgos por severidad. Úsela antes de abrir un pull request y para la revisión cruzada.
argument-hint: "Nombre del caso (la carpeta en docs/sdlc) y, si quiere, 'rama' para revisar solo lo que cambió frente a main"
---

# Revisar la seguridad

La revisión de seguridad acompaña a la revisión (etapa 5 del ciclo AI SDLC): busca lo que un atacante, un auditor o un incidente encontrarían. Señala; el dueño del código decide. No es una corrección.

## Pasos

1. **Defina el alcance.** Con `rama`: solo lo que cambió (`git diff main...HEAD --stat` y luego el diff de código, pruebas y configuración). Sin `rama`: el código del caso (`src/`, `tests/`, la configuración de la raíz). Lea `docs/sdlc/<caso>/spec.md` para saber qué datos maneja el caso.
2. **Corra la verificación automática** y anote el resultado:
   - `python herramientas/buscar_secretos.py --historia` (secretos en archivos y en la historia de git; los muestra enmascarados);
   - `python -m pytest -q` y `python herramientas/verificar_capas.py`.
   **No abra** `.env` ni llaves para "confirmar": un hook lo bloquea y no hace falta.
3. **Consulte al banco**, con el servidor MCP `banco`: `consultar_politica` con `seguridad`, `datos`, `logs` y `apis`; `catalogo_servicios` para saber qué campos de cada servicio son restringidos o confidenciales.
4. **Revise con la lista OWASP Top 10** (la tabla de abajo), en el alcance definido. Para cada categoría: ¿aplica a este código? Si aplica, ¿qué encontró? Además revise los **permisos del agente**: que `.claude/settings.json` y `.github/hooks/` tengan el hook `proteger.py` y que ningún agente tenga más herramientas de las que su rol necesita.
5. **Clasifique cada hallazgo** con `politicas.revision`: **bloqueante** (un secreto en el repositorio, inyección, un dato restringido en logs o mensajes, TLS sin verificar), **importante** (entrada sin validar en el borde, dependencia no aprobada, error que revela detalles internos) o **sugerencia**. Cada uno con: ID (`S-01`...), categoría OWASP, archivo:línea, evidencia **sin** el secreto ni el dato completo, la política que incumple y una recomendación concreta.
6. **Escriba `docs/sdlc/<caso>/seguridad.md`** con la plantilla `plantilla-seguridad.md` de esta skill, sin quitar secciones. Deje `Estado: borrador` y `Aprobado por: pendiente (dueño del código)`. Si ya existe, agregue una ronda nueva al final.
7. **Termine** con 3 líneas: cuántos hallazgos por severidad, si hay que rotar algún secreto, y qué decide el dueño del código.

## OWASP Top 10 (edición 2025) en un proyecto Python del banco

| Categoría | Qué buscar aquí |
|---|---|
| A01 Control de acceso roto (incluye SSRF) | Funciones que devuelven datos de otro cliente sin verificar a quién; rutas sin autenticación; el servidor llama a una URL que viene de la entrada |
| A02 Configuración insegura | Modo depuración encendido; trazas al usuario; permisos amplios |
| A03 Fallas en la cadena de suministro | Dependencias fuera de `convenciones.dependencias_aprobadas`; versiones sin fijar; paquetes de origen dudoso |
| A04 Fallas criptográficas | Secretos en el código o en `.env` versionado; datos restringidos sin enmascarar; TLS sin verificar (`verify=False`, contexto SSL sin verificación) |
| A05 Inyección | `eval`, `exec`; SQL o comandos armados con f-strings; `subprocess(..., shell=True)`; URLs armadas con la entrada sin validar |
| A06 Diseño inseguro | Validación que no está en el borde; reglas de negocio que se pueden saltar |
| A07 Fallas de autenticación | Tokens fijos en el código; credenciales por defecto |
| A08 Integridad de software o datos | `pickle`, `yaml.load` (sin `safe_load`) o `eval` sobre datos externos |
| A09 Fallas de registro y alertas | Datos restringidos en logs (`politicas.logs`); eventos de seguridad sin registrar |
| A10 Manejo inadecuado de condiciones excepcionales | `except: pass`; errores que dejan pasar (aprueban si algo falla); trazas o datos internos en el mensaje de error |

## Reglas
- No modifique código, pruebas ni configuración; las correcciones van como recomendaciones.
- Nunca escriba en el informe un secreto ni un dato restringido completo: archivo, línea y tipo bastan.
- No apruebe, no haga commit y no instale nada.
- No invente hallazgos para llenar categorías: si una no aplica, dígalo en una línea.
