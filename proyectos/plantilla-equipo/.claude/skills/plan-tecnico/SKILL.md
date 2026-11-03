---
name: plan-tecnico
description: Convierte un spec.md aprobado en el plan técnico (docs/sdlc/<caso>/plan.md) del ciclo AI SDLC del Banco Orquídea, con la estructura por capas, los componentes, los nombres validados, las pruebas de cada criterio de aceptación y los pasos en orden, prueba primero. Úsela cuando una especificación esté aprobada y haya que decidir cómo construirla, antes de escribir código.
argument-hint: "Nombre del caso (la carpeta en docs/sdlc), por ejemplo simulador-credito"
---

# Escribir el plan técnico de un caso de uso

El plan es la tercera etapa del ciclo AI SDLC: dice **cómo se construye lo que pide la especificación**, en pasos pequeños que otra persona (o el agente Desarrollador) puede seguir. Lo aprueba el líder técnico. No es código.

## Pasos

1. **Ubique la especificación.** Lea `docs/sdlc/<caso>/spec.md`. Si la persona no dijo el caso y hay varios, pregunte cuál.
2. **Compruebe que está aprobada.** Si `Estado` no es `aprobado`, deténgase: diga que falta la aprobación y no escriba el plan.
3. **Mire lo que ya existe.** Si hay código en `src/`, revise su estructura; no proponga rehacer lo que funciona. Lea la regla de capas (`.claude/rules/capas.md`).
4. **Consulte al banco**, con las herramientas del servidor MCP `banco`:
   - `catalogo_servicios` para cada dato que venga de otro sistema: se usará a través de un puerto.
   - `consultar_politica` con `nombres`, `pruebas` y, si aplica, `apis` o `logs`.
   - `validar_nombre` para **cada** nombre nuevo que proponga: paquete, módulos, funciones, clases, casos de uso, rutas y pruebas. Corrija los que no cumplan antes de escribirlos en el plan.
5. **Diseñe en capas** (`dominio`, `puertos`, `casos_uso`, `adaptadores`, `app`): qué archivo va en cada una y qué requisitos (RF) y reglas (RN) cubre. Lo de afuera (servicios, archivos, interfaz) entra por un puerto con un adaptador en memoria para las pruebas.
6. **Convierta cada criterio de aceptación en una prueba** con su archivo y su nombre `test_<regla>_<caso>`.
7. **Ordene los pasos, prueba primero:** el primer paso crea la estructura (`python herramientas/crear_estructura.py <paquete>`); los siguientes construyen primero el dominio y luego hacia afuera. Cada paso: escribir la prueba, verla fallar, implementar lo mínimo, verla pasar. Los primeros pasos deben dejar un **primer componente** funcionando con sus pruebas en verde.
8. **Escriba `docs/sdlc/<caso>/plan.md`** con la plantilla `plantilla-plan.md` de esta skill, sin quitar secciones. Deje `Estado: borrador` y `Aprobado por: pendiente (líder técnico)`.
9. **Termine** con un resumen de 3 líneas: cuántas capas y componentes, cuántas pruebas, cuál es el primer componente; y las preguntas abiertas. Pida la revisión del líder técnico.

## Reglas
- No escriba código ni cree archivos fuera de `docs/sdlc/<caso>/plan.md`.
- Solo dependencias de `convenciones.dependencias_aprobadas`; si hace falta otra, déjela como pregunta abierta.
- Nada que la especificación dejó fuera del alcance.
- Si ya existe un `plan.md` para ese caso, propóngale cambios en lugar de reemplazarlo.
