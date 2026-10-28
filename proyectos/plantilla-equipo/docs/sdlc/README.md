# Artefactos del ciclo AI SDLC

Cada caso de uso tiene su carpeta `docs/sdlc/<caso>/` con un archivo por etapa. El asistente los redacta; una persona los aprueba cambiando `Estado` a `aprobado` y escribiendo su nombre en `Aprobado por`.

| Etapa | Archivo | Skill | Aprueba |
|---|---|---|---|
| 1. Intención | `intent.md` | `/intencion` | Dueño del producto |
| 2. Especificación | `spec.md` | `/spec` (sesión 3) | Dueño del producto |
| 3. Plan | `plan.md` | `/plan` (sesión 4) | Líder técnico |
| 4. Construcción | código y pruebas | agente Desarrollador (sesión 4) | Desarrollador |
| 5. Revisión | `revision.md` | `/revisar` (sesión 5) | Dueño del código |
| 6. Entrega | solicitud `CAMB-####` | `crear_solicitud_cambio` (sesión 8) | Gestor de cambios |
