# Artefactos del ciclo AI SDLC

Cada caso de uso tiene su carpeta `docs/sdlc/<caso>/` con un archivo por etapa. El asistente los redacta; una persona los aprueba cambiando `Estado` a `aprobado` y escribiendo su nombre en `Aprobado por`.

| Etapa | Archivo | Skill | Aprueba |
|---|---|---|---|
| 1. Intención | `intent.md` | `/intencion` | Dueño del producto |
| 2. Especificación | `spec.md` | `/spec` | Dueño del producto |
| 3. Plan | `plan.md` | `/plan-tecnico` (agente arquitecto) | Líder técnico |
| 4. Construcción | código y pruebas, en una rama | agente desarrollador (y depurador si algo falla) | Desarrollador |
| 4b. Pruebas | `pruebas.md` (evidencia, no se aprueba) | `/pruebas` (agente verificador) | — |
| 5. Revisión | `revision.md` | `/revisar` (agente revisor), en el pull request | Dueño del código |
| 6. Entrega | solicitud `CAMB-####` | `crear_solicitud_cambio` (sesión 8) | Gestor de cambios |
