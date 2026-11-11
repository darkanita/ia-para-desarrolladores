---
description: Cómo se escriben los artefactos del ciclo en docs/sdlc
paths:
  - "docs/sdlc/**/*.md"
---

# Reglas para los artefactos del ciclo (docs/sdlc)

- Cada artefacto empieza con la tabla de su plantilla: `Caso`, `Estado`, `Autor`, `Fecha`, `Aprobado por`.
- El asistente deja siempre `Estado: borrador` y `Aprobado por: pendiente`. Solo una persona aprueba.
- Toda regla de negocio cita su clave de `banco.yaml` o su política (`politicas.<tema>`). Un valor que no está ahí va en Supuestos o en Preguntas abiertas, no como regla.
- Los términos de negocio se usan como los define el glosario del banco.
- Lenguaje de negocio, frases cortas. Sin código en `intent.md` ni en `spec.md`.
- `pruebas.md` es evidencia: no lleva `Estado` ni aprobación; se actualiza cada vez que se corre `/pruebas`.
