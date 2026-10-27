# Reglas del equipo

Estas reglas aplican a todo el código de este repositorio. Si una instrucción del chat las contradice, pregunte antes de seguir.

## Stack
- Python 3.10 o superior. Dependencias permitidas: `streamlit` y `pytest`. No agregue otras sin preguntar.
- Interfaz en `app.py` con Streamlit. Lógica de negocio en el paquete `simulador/`. Pruebas en `tests/`.
- El paquete `simulador/` no importa Streamlit: debe poder probarse sin interfaz.

## Dinero y tasas
- El dinero se maneja con `decimal.Decimal`, nunca con `float`. Los montos se expresan en pesos colombianos (COP).
- Los valores en pesos se redondean al peso con `ROUND_HALF_UP`.
- Las tasas de interés que reciben las funciones son efectivas anuales (E.A.), expresadas como fracción (24 % = `Decimal("0.24")`), salvo que el nombre diga lo contrario.
- Para pasar de E.A. a mensual se usa `(1 + tasa_ea) ** (1/12) - 1`. Nunca `tasa_ea / 12`.

## Código
- Nombres en español, en `snake_case`; clases en `PascalCase`. Sin abreviaturas crípticas.
- Funciones con anotaciones de tipo y un docstring corto en español.
- Los errores de validación lanzan la excepción del dominio con un mensaje que entienda el usuario.

## Pruebas
- Una prueba por regla de negocio, con valores calculados a mano o con otra fuente, no con el mismo código.
- Antes de dar una tarea por terminada, ejecute `python -m pytest -q` y muestre el resultado.

## Datos y seguridad
- Solo datos sintéticos. Nada de nombres, documentos ni cuentas reales.
- No escriba secretos ni llaves en el código.
