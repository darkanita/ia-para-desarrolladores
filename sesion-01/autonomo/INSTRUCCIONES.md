# Trabajo autónomo · Sesión 1

**Entrega:** antes de la sesión 2, en el canal del curso.

## 1. Preparar su máquina (obligatorio)
La sesión 2 es práctica con las tres herramientas del curso: Copilot Chat en VS Code, Copilot CLI y Claude Code.
- [ ] Siga la guía `preparacion/README.md`.
- [ ] Corra `python preparacion/verificar_entorno.py` y envíe una captura del resultado por el canal.

Si algo queda en **FALTA**, envíe la captura igual: lo resolvemos antes de la sesión 2.

## 2. Ejercicio: cazar errores con Copilot (~40 min)
Archivo: `validador_transacciones.py`. El código corre sin errores, pero tiene problemas de lógica y de buenas prácticas para un entorno financiero.

1. Pidan a Copilot que explique el archivo.
2. Pidan que genere tests con `pytest` a partir del **docstring** de `validar_transferencia` (las reglas de negocio están ahí).
3. Ejecuten los tests. ¿Cuáles fallan y por qué?
4. Pregunten explícitamente: *¿qué riesgos de seguridad o de manejo de dinero ves en este código?*
5. Llenen `BITACORA.md`: cada hallazgo, quién lo encontró (la IA o ustedes) y el prompt que lo reveló.

Pista: hay al menos 5 problemas.

## 3. Opcional: terminar el guardián de prompts
Si quiere practicar lo que hicimos en la demo guiada, complete `laboratorio/guardian_prompt.py` con Copilot hasta que `pytest sesion-01/laboratorio/tests -q` pase completo.

## 4. Lectura de apoyo (~45 min)
- **Microsoft Learn:** [Introduction to GitHub Copilot](https://learn.microsoft.com/en-us/training/modules/introduction-to-github-copilot/1-introduction).
- **Anthropic Academy:** [Claude Code 101](https://anthropic.skilljar.com/claude-code-101), lecciones *What is Claude Code?*, *How Claude Code works*, *Installing Claude Code* y *Your first prompt*.
- Lineamientos de la organización sobre uso de herramientas de IA (documento por confirmar).

El mapa de lecturas para todo el curso está en `REFERENCIAS.md`.

## 5. Traer una idea
Una tarea real y repetitiva de su trabajo, sin datos sensibles, donde la IA podría ayudar. Será la semilla del reto del curso, que se define en equipos en la sesión 2.
