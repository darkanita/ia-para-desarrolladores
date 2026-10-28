# Reglas del equipo · Banco Orquídea (ficticio)

Este repositorio pertenece a un equipo de desarrollo del **Banco Orquídea**, un banco ficticio del curso. Las definiciones del banco (productos, límites, clasificación de datos, convenciones) están en `banco.yaml`: léalo antes de proponer reglas de negocio y nunca invente valores que deberían salir de ahí.

## Cómo trabajamos: el ciclo AI SDLC
Cada caso de uso pasa por etapas y cada etapa deja un artefacto en `docs/sdlc/<caso>/`:
`intent.md` → `spec.md` → `plan.md` → código y pruebas → `revision.md` → solicitud de cambio.
- Usted (el asistente) redacta y propone; **una persona aprueba** cada artefacto cambiando su `Estado` a `aprobado`.
- No pase a la etapa siguiente si el artefacto anterior no está aprobado. Si falta, dígalo y ofrezca crearlo.
- No escriba código de producción sin un `plan.md` aprobado.

## Stack y estructura
- Python 3.12. Estructura por capas: `dominio`, `casos_uso`, `puertos`, `adaptadores`, `app`. El dominio no importa frameworks.
- Dependencias: solo las de `convenciones.dependencias_aprobadas` en `banco.yaml`. Para otra, pregunte.

## Código
- Nombres en español y `snake_case`; clases en `PascalCase`.
- Dinero en `decimal.Decimal`, redondeo al peso con `ROUND_HALF_UP`. Nunca `float`.
- Tasas efectivas anuales (E.A.); mensual = `(1 + ea) ** (1/12) - 1`, nunca `ea / 12`.
- Funciones con anotaciones de tipo y docstring corto en español.

## Pruebas
- `pytest`, una prueba por regla de negocio, con valores esperados calculados aparte.
- Antes de dar algo por terminado: `python -m pytest -q`.

## Datos y seguridad
- Solo datos sintéticos. Nada de cédulas, cuentas, tarjetas ni nombres reales.
- No lea ni escriba secretos (`.env`, llaves). No los incluya en prompts, logs ni código.

## Comandos útiles
- `python -m pytest -q` · `python herramientas/verificar_equipo.py` · `python herramientas/sincronizar_skills.py`
