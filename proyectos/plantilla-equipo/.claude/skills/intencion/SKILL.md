---
name: intencion
description: Convierte una idea o necesidad de negocio en el documento de intención (docs/sdlc/<caso>/intent.md) del ciclo AI SDLC del Banco Orquídea. Úsela cuando alguien proponga un caso de uso nuevo, un cambio o un reto, antes de cualquier especificación o código.
argument-hint: "Describa la idea o el problema de negocio en una o dos frases"
---

# Redactar la intención de un caso de uso

La intención es la primera etapa del ciclo AI SDLC: dice **qué problema se resuelve, para quién y cómo sabremos que funcionó**. No dice cómo construirlo.

## Pasos

1. **Entienda la idea.** Lea lo que escribió la persona. Lea `banco.yaml` (productos, clasificación de datos, reglas) y `AGENTS.md`.
2. **Pregunte lo que falte, de una vez.** Si no está claro, haga como máximo 5 preguntas en un solo mensaje sobre: el problema, los usuarios, la métrica de éxito, los datos que usa y lo que queda fuera. Si la persona prefiere no responder, siga y anote supuestos.
3. **Elija el nombre del caso**: corto, en minúsculas con guiones (por ejemplo `simulador-credito`).
4. **Escriba `docs/sdlc/<caso>/intent.md`** con la plantilla `plantilla-intent.md` de esta skill, sin quitar secciones. Si una sección no aplica, escriba "No aplica" y por qué.
5. **Clasifique los datos** con las categorías de `banco.yaml` (`datos.clasificacion`). Si el caso toca datos restringidos, dígalo en Riesgos y exija datos sintéticos.
6. **Cite las reglas del banco que aplican** (por ejemplo, la tasa máxima o el límite diario) con su clave de `banco.yaml`. No invente valores.
7. **Deje el estado en `borrador`** y `Aprobado por: pendiente`. Usted no aprueba: lo hace el dueño del producto.
8. **Termine** mostrando un resumen de 3 líneas, los supuestos y las preguntas abiertas, y pida la revisión.

## Reglas
- No escriba código, especificaciones técnicas ni planes: eso viene en etapas siguientes.
- No use datos reales de clientes, ni siquiera como ejemplo.
- Si ya existe un `intent.md` para ese caso, propóngale cambios en lugar de reemplazarlo.
