---
description: Reglas para procesos ETL y de reglas sobre transacciones
paths:
  - "**/etl/**/*.py"
  - "**/*_etl.py"
---

# Reglas para procesos ETL

- Cada paso es una función pura (`extraer`, `transformar`, `cargar`) que se puede probar por separado.
- Lea los archivos con su codificación explícita (`encoding="utf-8"`) y valide columnas y tipos al extraer.
- Las reglas de negocio (umbrales, ventanas de tiempo) salen de `banco.yaml` o de un archivo de configuración, nunca escritas a mano en el código.
- Registre cuántos registros entraron, cuántos se rechazaron y por qué, siguiendo `politicas.logs`, sin datos restringidos.
- Los datos de entrada de pruebas y ejemplos son sintéticos y viven en `tests/datos/`.
