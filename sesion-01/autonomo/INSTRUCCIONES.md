# Trabajo autónomo · Sesión 1

**Entrega:** antes de la sesión 2, en el canal del curso.

## 1. Verificar accesos (obligatorio)
La sesión 2 usa las dos herramientas autorizadas por la organización. Comprueben que pueden:
- [ ] Abrir Copilot Chat en VS Code y recibir una respuesta.
- [ ] Ingresar al sandbox de Claude y enviar un mensaje de prueba.

Si alguna falla, avisen en el canal antes de la sesión 2.

## 2. Ejercicio: cazar errores con Copilot (~40 min)
Archivo: `validador_transacciones.py`. El código corre sin errores, pero tiene problemas de lógica y de buenas prácticas para un entorno financiero.

1. Pidan a Copilot que explique el archivo.
2. Pidan que genere tests con `pytest` a partir del **docstring** de `validar_transferencia` (las reglas de negocio están ahí).
3. Ejecuten los tests. ¿Cuáles fallan y por qué?
4. Pregunten explícitamente: *¿qué riesgos de seguridad o de manejo de dinero ves en este código?*
5. Llenen `BITACORA.md`: cada hallazgo, quién lo encontró (la IA o ustedes) y el prompt que lo reveló.

Pista: hay al menos 5 problemas.

## 3. Lectura de apoyo
- Lineamientos de la organización sobre uso de herramientas de IA (documento por confirmar).

## 4. Traer una idea
Una tarea real y repetitiva de su trabajo, sin datos sensibles, donde la IA podría ayudar. Será la semilla del reto del curso, que se define en equipos en la sesión 2.
