# Laboratorio S1 — Guardián de prompts

**Tiempo:** 35 minutos · **Modalidad:** individual o en parejas · **Herramientas:** VS Code + GitHub Copilot

## Contexto

Antes de pegar código en Copilot Chat o enviarlo a la API de un modelo, en un banco hay que responder tres preguntas:

1. ¿Cuántos tokens es y cuánto cuesta?
2. ¿Lleva datos sensibles que no deben salir de nuestro entorno?
3. ¿Cabe en el presupuesto de contexto?

Vas a construir `guardian_prompt.py`, una pequeña librería que responde esas preguntas. Es el mismo tipo de ejercicio que viste en la demo: usa Copilot para escribir el código, pero **tú decides si lo que propone es correcto**. Las pruebas son el árbitro.

## Cómo trabajar

```bash
pytest sesion-01/laboratorio/tests -q                     # todas las pruebas
pytest sesion-01/laboratorio/tests -q -k Luhn             # solo un grupo
```

Formas sugeridas de usar Copilot:

- Escribe la firma y el docstring, y deja que Copilot complete el cuerpo (Tab para aceptar).
- En Copilot Chat, selecciona la función y pide: *"Implementa esta función siguiendo las reglas de ENUNCIADO.md, sección Parte 2"* (arrastra el archivo `ENUNCIADO.md` al chat para darle contexto).
- Si una prueba falla, pega la salida de `pytest` en el chat y pide que explique por qué.

## Parte 1 — Tokens y costo (10 min)

**`contar_tokens(texto)`**
- `""` → `0`.
- Si `_ENC` (tiktoken) está disponible, usa `len(_ENC.encode(texto))`.
- Si no, aproxima: `ceil(len(texto) / 4)`.

**`estimar_costo_usd(tokens_entrada, tokens_salida, precio_entrada_1m, precio_salida_1m)`**
- Precios en USD por **millón** de tokens.
- `ValueError` si algún valor es negativo.
- Redondea a 6 decimales.

## Parte 2 — Redacción de datos sensibles (20 min)

**`es_luhn_valido(numero)`**: ignora espacios y guiones; aplica el algoritmo de Luhn. Una cadena sin dígitos no es válida.

**`redactar_datos_sensibles(texto)`** devuelve `(texto_redactado, conteo)`, con `conteo` siempre igual a `{"EMAIL": n, "TARJETA": n, "CEDULA": n, "SECRETO": n}`.

| Etiqueta | Qué se reemplaza | Ejemplo |
|---|---|---|
| `[SECRETO]` | Llaves con formato conocido: `sk-` + 20 o más caracteres, `AKIA` + 16 mayúsculas/dígitos, `ghp_` + 36 alfanuméricos. | `'sk-proj-AbC…'` → `'[SECRETO]'` |
| `[SECRETO]` | El **valor** entre comillas asignado a `password`, `passwd`, `pwd`, `secret`, `token`, `api_key`, `apikey` o `clave` (sin importar mayúsculas), con `=` o `:`. Se conservan el nombre y las comillas. | `password = "x"` → `password = "[SECRETO]"` |
| `[EMAIL]` | Cualquier correo electrónico. | `ana@banco.co` → `[EMAIL]` |
| `[TARJETA]` | Secuencias de 13 a 19 dígitos (pueden tener espacios o guiones entre ellos) **que pasen Luhn**. Si no pasan Luhn, se dejan igual. | `4111 1111 1111 1111` → `[TARJETA]` |
| `[CEDULA]` | 6 a 10 dígitos que siguen a `cc`, `c.c.`, `cedula`, `cédula` o `documento` (con `:`, `=` o `#` opcional). Solo se reemplaza el número. | `CC 43123456` → `CC [CEDULA]` |

Orden recomendado: secretos → correos → tarjetas → cédulas.

## Parte 3 — Presupuesto de contexto (5 min)

**`preparar_contexto(codigo, max_tokens, recortar=False, precio_entrada_1m=2.50)`**
1. Redacta los datos sensibles.
2. Cuenta los tokens del texto **ya redactado**.
3. Si excede `max_tokens`:
   - con `recortar=False` lanza `ContextoExcedidoError`;
   - con `recortar=True` quita **líneas completas del final** hasta que quepa y marca `recortado=True`.
4. Devuelve `{"texto", "tokens", "costo_usd", "hallazgos", "recortado"}`; `costo_usd` solo considera tokens de entrada.

## Para discutir al cierre

- ¿Qué propuso Copilot que estaba **mal**? ¿Cómo lo detectaste?
- ¿Qué datos sensibles de tu día a día no cubre este guardián?
- ¿Dónde pondrías este control en un flujo real de la organización?

## Bonus

- Agrega `[TELEFONO]` para celulares colombianos (`3XX XXX XXXX`, con o sin `+57`).
- Haz que `preparar_contexto` también reporte el porcentaje de la ventana que ocupa.
