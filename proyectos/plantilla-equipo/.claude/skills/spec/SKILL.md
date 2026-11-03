---
name: spec
description: Convierte un intent.md aprobado en la especificación funcional (docs/sdlc/<caso>/spec.md) del ciclo AI SDLC del Banco Orquídea, con requisitos, criterios de aceptación, reglas, datos, servicios y políticas. Úsela cuando una intención esté aprobada y haya que definir qué debe hacer el sistema, antes del plan técnico o del código.
argument-hint: "Nombre del caso (la carpeta en docs/sdlc), por ejemplo simulador-credito"
---

# Escribir la especificación de un caso de uso

La especificación es la segunda etapa del ciclo AI SDLC: dice **qué debe hacer el sistema y cómo sabremos que lo hace bien**, en lenguaje que el dueño del producto puede aprobar. No dice cómo se construye: eso es el `plan.md`.

## Pasos

1. **Ubique la intención.** Lea `docs/sdlc/<caso>/intent.md`. Si la persona no dijo el caso y hay varios, pregunte cuál.
2. **Compruebe que está aprobada.** Si `Estado` no es `aprobado`, deténgase: diga que falta la aprobación y no escriba la especificación.
3. **Consulte al banco antes de escribir**, con las herramientas del servidor MCP `banco`:
   - `glosario` para cada término de negocio que use (por ejemplo, capacidad de pago, usura).
   - `consultar_politica` para los temas que toque el caso; como mínimo `datos`, y además `logs`, `seguridad`, `apis` o `nombres` si aplican.
   - `catalogo_servicios` para saber qué APIs internas ya existen y de dónde sale cada dato.
   Si las herramientas no están disponibles, lea esas secciones en `banco.yaml` y dígalo al final.
4. **Pregunte lo que falte, de una vez.** Como máximo 3 preguntas en un solo mensaje, solo si la intención no alcanza para escribir los criterios de aceptación. Si la persona prefiere no responder, siga y anote supuestos.
5. **Escriba `docs/sdlc/<caso>/spec.md`** con la plantilla `plantilla-spec.md` de esta skill, sin quitar secciones:
   - Cada requisito funcional (`RF-01`, `RF-02`...) con criterios de aceptación en formato *Dado / Cuando / Entonces*, con valores concretos.
   - Cada regla de negocio (`RN-01`...) con su clave de `banco.yaml` o su política. No invente valores.
   - Cada dato con su clasificación y su origen (un servicio del catálogo o la entrada del usuario).
   - La trazabilidad: qué objetivo o métrica de la intención cubre cada requisito.
6. **Deje el estado en `borrador`** y `Aprobado por: pendiente`. Usted no aprueba: lo hace el dueño del producto.
7. **Termine** con un resumen de 3 líneas: cuántos requisitos y reglas, qué servicios del catálogo usa, y las preguntas abiertas. Pida la revisión.

## Reglas
- No escriba código, clases, tablas de base de datos ni el plan técnico.
- Lo que la intención dejó fuera del alcance sigue fuera; si algo nuevo parece necesario, propóngalo como pregunta abierta.
- No use datos reales de clientes, ni siquiera en los ejemplos de los criterios de aceptación.
- Si ya existe un `spec.md` para ese caso, propóngale cambios en lugar de reemplazarlo.
