---
name: pruebas
description: Comprueba que cada criterio de aceptación y cada regla de negocio de un spec.md aprobado tenga su prueba en tests/, escribe las que faltan (bordes, rechazos, casos con datos sintéticos del banco), mide la cobertura del dominio y deja la matriz en docs/sdlc/<caso>/pruebas.md. Úsela antes de revisar o entregar un caso de uso.
argument-hint: "Nombre del caso (la carpeta en docs/sdlc)"
---

# Verificar que la especificación está probada

Las pruebas son la evidencia de que lo construido cumple lo aprobado. Esta skill no prueba "el código": prueba **la especificación**. Cada criterio de aceptación y cada regla RN debe tener al menos una prueba que falle si el código no lo cumple.

## Pasos

1. **Lea lo aprobado.** `docs/sdlc/<caso>/spec.md` (criterios de aceptación de cada RF, reglas RN y la sección de casos borde y errores) y `plan.md` (la tabla de pruebas por criterio). Si la spec no está aprobada, deténgase.
2. **Corra lo que hay:** `python -m pytest -q`. Si algo falla antes de empezar, dígalo y no siga: primero el depurador.
3. **Arme la matriz criterio → prueba.** Para cada criterio, regla RN y fila de casos borde, busque en `tests/` la prueba que lo cubre (por nombre, docstring `Regla: ...` o contenido). Marque: cubierto, parcial (falta un borde) o sin prueba. Si el criterio habla de lo que **ve** el usuario ("cuando el asesor ve el resultado", un mensaje, lo que aparece o no en pantalla), la prueba tiene que mirar la interfaz (por ejemplo con `streamlit.testing`); una prueba solo del caso de uso cuenta como **parcial**.
4. **Escriba las pruebas que faltan**, siguiendo la regla de pruebas (`.claude/rules/pruebas.md`): nombre `test_<regla>_<caso>` validado con `validar_nombre`, docstring que cita la regla, bordes en un `parametrize` con ids en español.
   - Para datos de entrada use la herramienta `datos_sinteticos` del banco (por ejemplo `datos_sinteticos("credito_consumo", 10, semilla=1, incluir_bordes=true)`), o valores escritos a mano.
   - El valor esperado sale de la especificación o se calcula aparte; **nunca** copie lo que devuelve el código.
5. **Córralas.** Si una prueba nueva falla, **no toque `src/`** ni cambie el valor esperado: márquela con `@pytest.mark.xfail(strict=True, reason="Posible defecto: <criterio>")`, para que la suite (y el hook del equipo) quede en verde mientras el defecto sigue abierto, y anótela como **posible defecto** con el criterio y la diferencia. Corra `python -m pytest -q` otra vez: debe salir `N xfailed`.
6. **Mida la cobertura del dominio**, si `pytest-cov` está instalado: `python -m pytest -q --cov=src/<paquete>/dominio --cov-report=term-missing`. Compárela con `convenciones.pruebas.cobertura_minima_dominio`.
7. **Escriba `docs/sdlc/<caso>/pruebas.md`** con la plantilla `plantilla-pruebas.md` de esta skill. Si ya existe, actualícela.
8. **Termine** con 3 líneas: criterios cubiertos de cuántos, pruebas nuevas, posibles defectos (si hay, sugiera el agente depurador) y cobertura.

## Reglas
- Solo escriba en `tests/` y en `docs/sdlc/<caso>/pruebas.md`.
- Datos sintéticos siempre; nada de cédulas, cuentas o nombres reales.
- Una prueba que falla es información, no un error suyo: repórtela.
