---
description: Cómo escribimos las pruebas del equipo
paths:
  - "tests/**/*.py"
  - "**/test_*.py"
---

# Reglas para las pruebas

- Archivo `tests/test_<modulo>.py`; cada función `test_<regla>_<caso>`, en español: `test_gmf_cuenta_exenta`.
- Cada prueba empieza con un docstring que cita la regla que verifica con su clave de `banco.yaml`: `"""Regla: productos.transferencias.gmf."""`
- Los bordes (mínimo, máximo, justo por encima y por debajo) van en una sola prueba con `pytest.mark.parametrize` e `ids` en español.
- Dinero y tasas con `Decimal("...")` escrito como texto, nunca con `float`.
- Los valores esperados se calculan aparte y se escriben literales; no se recalculan con el código que se prueba.
- Solo datos sintéticos: cuentas con el formato `SINT-0000-####` y clientes con nombres claramente inventados.
- Para varios casos de entrada, pida datos a la herramienta `datos_sinteticos` del banco (por ejemplo `datos_sinteticos("credito_consumo", 10, semilla=1, incluir_bordes=true)`) y cite la semilla en el docstring.
- Si una prueba nueva falla, no cambie el valor esperado para que pase: es un posible defecto. Márquela con `@pytest.mark.xfail(strict=True, reason="Posible defecto: <criterio>")` y repórtela (`politicas.pruebas`). Quien corrige el defecto quita la marca: con `strict=True`, si la prueba ya pasa y la marca sigue, la suite falla.
- Sin llamadas a servicios reales ni a internet: use adaptadores en memoria.
