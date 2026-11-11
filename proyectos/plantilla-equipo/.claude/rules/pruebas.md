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
- Sin llamadas a servicios reales ni a internet: use adaptadores en memoria.
