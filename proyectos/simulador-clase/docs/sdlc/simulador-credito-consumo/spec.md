# Especificación: Simulador único de crédito de consumo

| Campo | Valor |
|---|---|
| Caso | `simulador-credito-consumo` |
| Estado | aprobada |
| Intención | [`intent.md`](intent.md) (aprobada por la docente del curso) |
| Autor | Equipo de desarrollo (redactada por el asistente, solicitada por la docente del curso) |
| Fecha | 2026-11-03 |
| Aprobado por | la docente del curso (dueño del producto) |

## 1. Resumen
El sistema permite al asesor de cualquier oficina simular un crédito de consumo a partir de monto, plazo, tasa efectiva anual (E.A.) e ingresos y otras cuotas del cliente. Con esos datos calcula la cuota mensual de cuota fija, el costo total del crédito y el nivel de endeudamiento, y dice si queda dentro del máximo del banco. Si la simulación incumple una regla de monto, plazo, tasa o endeudamiento, no muestra una cifra válida. Para los mismos datos, el resultado es siempre el mismo sin importar la oficina. El resultado es una simulación y no una oferta de crédito.

## 2. Alcance
**Incluye:**
- Cálculo de la cuota mensual (sistema de cuota fija), del costo total del crédito y del indicador de endeudamiento.
- Validación de monto, plazo, tasa y endeudamiento contra las reglas del banco (`banco.yaml`).
- Un único origen de cálculo para todas las oficinas, con una interfaz para asesores.
- Aviso de que el resultado es una simulación y no una oferta.

**No incluye:** (lo mismo que la intención)
- Aprobación o negación del crédito, scoring o perfil de riesgo del cliente.
- Consulta a centrales de riesgo o al core bancario. El simulador no lee datos de clientes del banco: los digita el asesor.
- Desembolso, registro de la solicitud o contrato.
- Otros productos (transferencias, tarjetas, libranzas).
- Seguros, comisiones y otros cargos, salvo decisión del dueño del producto (ver preguntas abiertas).
- Retiro de las hojas de cálculo actuales. Se planea en una etapa posterior.
- Capacitación de los asesores y medición de la meta de uso único (depende del banco, no del sistema).

## 3. Actores y escenarios
| Actor | Qué hace con el sistema |
|---|---|
| Asesor comercial | Digita monto, plazo, tasa E.A., ingresos y otras cuotas del cliente; consulta el resultado y lo comunica al cliente. |
| Cliente | Recibe la cifra a través del asesor; no usa el sistema directamente. |
| Área de control | Verifica los cálculos en un solo lugar (con los casos de referencia de RF-05). |
| Dueño del producto | Define las reglas del producto en `banco.yaml` y aprueba la especificación. |

## 4. Requisitos funcionales

### RF-01 · Cuota mensual
El sistema calcula la cuota mensual fija de un crédito de consumo a partir de monto, plazo y tasa E.A. (RN-06, RN-07; sistema de cuota fija según S-01).

**Criterios de aceptación**
- **Dado** monto 10.000.000 COP, plazo 36 meses y tasa 26 % E.A. **cuando** el asesor simula **entonces** la cuota mensual es **388.846 COP**.
- **Dado** monto 1.000.000 COP, plazo 6 meses y tasa 26 % E.A. **cuando** el asesor simula **entonces** la cuota mensual es **178.192 COP**.
- **Dado** monto 100.000.000 COP, plazo 72 meses y tasa 26 % E.A. **cuando** el asesor simula **entonces** la cuota mensual es **2.592.471 COP**.
- **Dado** cualquier simulación válida **cuando** se calcula la cuota **entonces** la tasa mensual se deriva de la E.A. como (1 + ea)^(1/12) − 1 y la cuota se redondea al peso solo al final, nunca con tasas o cuotas intermedias redondeadas.

### RF-02 · Costo total del crédito
El sistema muestra el costo total del crédito a lo largo del plazo, como la suma de las cuotas del plazo (supuesto S-02).

**Criterios de aceptación**
- **Dado** monto 10.000.000 COP, plazo 36 meses y tasa 26 % E.A. **cuando** el asesor simula **entonces** el costo total es **13.998.456 COP** (388.846 × 36).
- **Dado** monto 1.000.000 COP, plazo 6 meses y tasa 26 % E.A. **cuando** el asesor simula **entonces** el costo total es **1.069.152 COP** (178.192 × 6).
- **Dado** una simulación válida **cuando** se muestra el resultado **entonces** el costo total aparece junto a la cuota y al plazo, con la misma moneda (COP).

### RF-03 · Indicador de endeudamiento
El sistema calcula el endeudamiento resultante, (cuota nueva + otras cuotas del cliente) / ingresos mensuales, y dice si queda dentro del máximo del banco (RN-05).

**Criterios de aceptación**
- **Dado** una cuota nueva de 388.846 COP, otras cuotas de 500.000 COP e ingresos de 4.000.000 COP **cuando** el asesor simula **entonces** el endeudamiento es **22,2 %** y el resultado indica que **sí** le alcanza.
- **Dado** una cuota nueva de 388.846 COP, otras cuotas de 400.000 COP e ingresos de 1.500.000 COP **cuando** el asesor simula **entonces** el endeudamiento es **52,6 %**, supera el máximo de 40 %, y el resultado indica que **no** le alcanza (ver RF-04).
- **Dado** ingresos mensuales de 0 COP **cuando** el asesor simula **entonces** el sistema no calcula el endeudamiento y pide ingresos mayores que cero.

### RF-04 · Validación de reglas del banco
El sistema verifica monto, plazo, tasa y endeudamiento antes de mostrar un resultado válido. Si una regla no se cumple, indica cuál y no muestra cifras como válidas (RN-01 a RN-05).

**Criterios de aceptación**
- **Dado** monto 999.999 COP **cuando** el asesor simula **entonces** el sistema rechaza la simulación indicando que el monto mínimo es 1.000.000 COP y no muestra cuota ni costo total.
- **Dado** monto 100.000.001 COP **cuando** el asesor simula **entonces** el sistema rechaza la simulación indicando que el monto máximo es 100.000.000 COP.
- **Dado** plazo de 5 meses **cuando** el asesor simula **entonces** el sistema rechaza la simulación indicando que el plazo va de 6 a 72 meses.
- **Dado** plazo de 73 meses **cuando** el asesor simula **entonces** el sistema rechaza la simulación con el mismo mensaje de plazo.
- **Dado** tasa de 27 % E.A. **cuando** el asesor simula **entonces** el sistema rechaza la simulación indicando que la tasa máxima es 26 % E.A. (valor pendiente de confirmar, ver preguntas abiertas).
- **Dado** monto 10.000.000 COP, plazo 36 meses, tasa 26 % E.A., ingresos de 1.500.000 COP y otras cuotas de 400.000 COP **cuando** el asesor simula **entonces** el sistema muestra el endeudamiento de 52,6 % y no lo presenta como válido, porque supera el máximo de 40 %.
- **Dado** un campo obligatorio vacío o un valor no numérico **cuando** el asesor simula **entonces** el sistema pide corregir ese campo y no calcula nada.

### RF-05 · Resultado reproducible entre oficinas
Para los mismos datos de entrada, cualquier oficina obtiene exactamente el mismo resultado. El sistema tiene un único origen de cálculo.

**Criterios de aceptación**
- **Dado** el conjunto de casos de referencia aprobado por el dueño del producto **cuando** se ejecutan en el sistema **entonces** todos los resultados coinciden con los valores esperados, con 0 diferencias.
- **Dado** los mismos datos de entrada simulados en dos oficinas distintas **cuando** se comparan los resultados **entonces** cuota, costo total, endeudamiento y veredicto son idénticos.
- **Dado** los casos de referencia que provengan de hojas actuales **cuando** se preparan para usarse **entonces** deben estar saneados (solo datos sintéticos) antes de entrar al conjunto (ver sección 6).

### RF-06 · Aviso de simulación
Todo resultado válido muestra que es una simulación y no una oferta de crédito.

**Criterios de aceptación**
- **Dado** una simulación válida **cuando** el asesor ve el resultado **entonces** aparece el aviso de que es una simulación y no una oferta, con el texto que defina el área legal o de producto.
- **Dado** una simulación rechazada por RF-04 **cuando** el asesor ve el resultado **entonces** no aparece cuota ni costo total, solo el motivo del rechazo y el aviso.

## 5. Reglas de negocio
| Id | Regla | Fuente (`banco.yaml` o política) | Valor |
|---|---|---|---|
| RN-01 | Monto mínimo de la simulación | `productos.credito_consumo.monto_minimo` | 1.000.000 COP |
| RN-02 | Monto máximo de la simulación | `productos.credito_consumo.monto_maximo` | 100.000.000 COP |
| RN-03 | Plazo permitido en meses | `productos.credito_consumo.plazo_meses` | Entre 6 y 72 meses, ambos incluidos |
| RN-04 | Tasa efectiva anual máxima | `productos.credito_consumo.tasa_maxima_ea` | 0,26 (26 %). Marcado en `banco.yaml` como valor de ejemplo; pendiente de confirmar |
| RN-05 | Endeudamiento máximo: (cuota nueva + otras cuotas) / ingresos | `productos.credito_consumo.endeudamiento_maximo` | 0,40 (40 %). Marcado en `banco.yaml` como valor de ejemplo; pendiente de confirmar |
| RN-06 | Tasas efectivas anuales; mensual = (1 + ea)^(1/12) − 1 | `convenciones.tasas` | E.A. como fracción; nunca ea / 12 |
| RN-07 | Dinero: redondeo al peso con ROUND_HALF_UP | `convenciones.dinero` | Pesos enteros (COP) |

La cuota fija no es una regla de `banco.yaml`: está como supuesto S-01 (sección 11).

## 6. Datos
| Dato | Tipo | Clasificación | Origen (servicio del catálogo o entrada) |
|---|---|---|---|
| Monto de la simulación | Número, pesos enteros | confidencial (condiciones de negocio) | Entrada del asesor |
| Plazo en meses | Número entero | confidencial (condiciones de negocio) | Entrada del asesor |
| Tasa efectiva anual | Porcentaje | confidencial (condiciones de negocio) | Entrada del asesor (pendiente: ver pregunta 1) |
| Ingresos mensuales del cliente | Número, pesos enteros | restringida (datos financieros de clientes) | Entrada del asesor; sin consulta a sistemas del banco |
| Otras cuotas mensuales del cliente | Número, pesos enteros | restringida (datos financieros de clientes) | Entrada del asesor; sin consulta a sistemas del banco |
| Cuota, costo total y endeudamiento calculados | Número | confidencial (condiciones de negocio) | Calculado por el sistema |
| Reglas del producto (montos, plazos, tasa máxima, endeudamiento máximo) | Parámetros | interna | `banco.yaml` |
| Casos de referencia para validar resultados | Tabla de entradas y resultados esperados | restringida si provienen de hojas reales; confidencial si son sintéticos | Hojas actuales de las oficinas, previo saneamiento; o datos sintéticos |

**Reglas de manejo de datos** (`datos.reglas` de `banco.yaml`): solo datos sintéticos en desarrollo y pruebas; los datos restringidos no se escriben en logs, prompts ni archivos del repositorio.

## 7. Servicios del banco que usa
| Servicio | Operación | Para qué |
|---|---|---|
| Ninguno confirmado | — | El caso no consulta servicios internos: la intención excluye centrales de riesgo y core bancario, y el asesor digita todos los datos. |
| `svc-tasas` (propuesto, pendiente de la pregunta 1) | `GET /v1/tasas/{producto}` | Fuente oficial de la tasa E.A. vigente y de `tasa_maxima_ea` (campos públicos). Solo si el dueño del producto decide que la tasa no la digita el asesor. |

`svc-clientes` (ingresos y otras cuotas, clasificados como restringida) existe en el catálogo, pero no se usa en esta versión: la intención pide que el asesor digite esos datos. Ver pregunta 2 de la sección 12.

## 8. Requisitos no funcionales y políticas
| Tema | Qué exige | Política |
|---|---|---|
| Datos | Solo datos sintéticos en desarrollo y pruebas; datos restringidos fuera de logs, prompts, errores y del repositorio; minimización de campos | `politicas.datos` y `datos.reglas` en `banco.yaml` |
| Datos | Clasificación de cada dato según la tabla de la sección 6 | `datos.clasificacion` en `banco.yaml` |
| Logs | Registros JSON con fecha, nivel, servicio, id de correlación y evento; sin datos restringidos; WARNING para simulaciones rechazadas por RF-04 | `politicas.logs` |
| Seguridad | Toda entrada (monto, plazo, tasa, ingresos, otras cuotas) se valida en el borde (tipo, rango, formato) antes de calcular; los mensajes de error no revelan detalles internos | `politicas.seguridad` |
| APIs | Si el cálculo se expone como servicio: ruta versionada (`/v1/...`), montos como texto decimal, errores con formato `{codigo, mensaje, id_correlacion}` | `politicas.apis` |
| Pruebas | Una prueba por regla (RN-01 a RN-07), con bordes (mínimo, máximo, justo por encima), valores esperados calculados aparte y sin servicios reales | `politicas.pruebas` |
| Nombres | Código en español y snake_case; servicios con prefijo `svc-` | `politicas.nombres` |
| Dinero | Montos en pesos enteros, cálculo exacto y redondeo al peso ROUND_HALF_UP | `convenciones.dinero` |
| Tasas | Tasas en E.A.; la mensual se deriva de la E.A. | `convenciones.tasas` |
| Consistencia | Mismo resultado para los mismos datos en cualquier oficina (RF-05) | Requisito de la intención §3 |
| Idioma | Interfaz y mensajes en español | `convenciones.nombres` |

## 9. Casos borde y errores
| Situación | Comportamiento esperado | Mensaje al usuario |
|---|---|---|
| Monto por debajo de 1.000.000 COP | Rechaza; no calcula | "El monto mínimo es 1.000.000 COP." |
| Monto por encima de 100.000.000 COP | Rechaza; no calcula | "El monto máximo es 100.000.000 COP." |
| Plazo fuera de 6 a 72 meses | Rechaza; no calcula | "El plazo debe estar entre 6 y 72 meses." |
| Tasa por encima de la tasa máxima | Rechaza; no calcula | "La tasa máxima permitida es 26 % E.A." (el valor se toma de `banco.yaml`) |
| Endeudamiento por encima del máximo | Muestra el indicador con el veredicto "no le alcanza"; no lo presenta como válido | "El endeudamiento de 52,6 % supera el máximo permitido de 40 %." |
| Ingresos iguales a cero | No calcula el endeudamiento; no hay división por cero | "Los ingresos deben ser mayores que cero." |
| Otras cuotas vacías | Se toman como 0 COP solo si el asesor lo confirma; si no, pide el dato | "Indique las otras cuotas del cliente, o 0 si no tiene." |
| Campo vacío o no numérico | No calcula; marca el campo | "Revise este campo: debe ser un número." |
| Plazo con decimales (por ejemplo 12,5 meses) | Rechaza; no calcula | "El plazo debe ser un número entero de meses." |
| Tasa vacía o con formato no reconocible | No calcula | "Indique la tasa efectiva anual, por ejemplo 26 %." |
| Datos de entrada idénticos a un caso de referencia | Devuelve el resultado esperado del caso | — (no hay mensaje; resultado normal) |

## 10. Trazabilidad
| Objetivo o métrica de la intención | Requisitos que lo cubren |
|---|---|
| Resultado esperado 1: cuota mensual | RF-01 |
| Resultado esperado 2: costo total del crédito | RF-02 |
| Resultado esperado 3: si le alcanza con sus ingresos | RF-03, RF-04 |
| Si la simulación incumple una regla, el simulador lo indica | RF-04 |
| Métrica: diferencias de resultado entre oficinas = 0 | RF-05 (casos de referencia y consistencia) |
| Métrica: simulaciones aceptadas con tasa por encima de `tasa_maxima_ea` = 0 | RF-04 (validación de tasa) |
| Métrica: oficinas que usan el simulador como única fuente | No cubierta por el software: depende de capacitación y del retiro de hojas (intención §9, fuera de alcance). RF-05 aporta el único origen de cálculo. |
| Métrica: tiempo para entregar una cotización al cliente | No cubierta todavía: la meta está "por definir" con el dueño del producto (pregunta abierta 6). |
| Usuarios: el cliente recibe una cifra clara | RF-06 (aviso de simulación), RF-01 a RF-03 |
| Riesgo: datos restringidos fuera de logs y repositorio | Sección 6 y sección 8 (`datos.reglas`) |

## 11. Supuestos
- **S-01 · Cuota fija:** cada mes se paga la misma cuota (intención §10; RN-08).
- **S-02 · Costo total:** es la suma de las cuotas del plazo, sin seguros ni comisiones (intención §10). Si el dueño del producto decide otra cosa, cambian RF-02 y los valores de ejemplo.
- **S-03 · Redondeo:** la cuota exacta se calcula sin redondeos intermedios y se redondea al peso al final; el costo total es la cuota redondeada por el plazo. La decisión sobre la última cuota queda pendiente (pregunta 7).
- **S-04 · Tasa:** la define el banco y el asesor no puede fijarla por encima de la tasa máxima. Mientras la pregunta 1 no esté resuelta, se asume que el asesor la digita dentro del máximo.
- **S-05 · Endeudamiento:** es el indicador de `banco.yaml` (cuota nueva más otras cuotas, sobre ingresos), comparado con el máximo.
- **S-06 · Usuarios:** los asesores de oficina; el cliente ve el resultado a través de ellos.
- **S-07 · Datos de prueba:** todos los datos de desarrollo y pruebas son sintéticos. Los ejemplos de esta especificación son sintéticos y no corresponden a clientes reales.
- **S-08 · Valores de ejemplo:** los valores de tasa máxima (26 %) y endeudamiento máximo (40 %) se usan como están en `banco.yaml`, aunque estén marcados como ejemplos. Los ejemplos numéricos de esta especificación se recalculan si cambian.

## 12. Preguntas abiertas
1. **Origen de la tasa E.A.:** ¿la digita el asesor en cada simulación, o sale de una tabla de tarifas vigente? Afecta RF-04, la sección 6 y quién puede fijarla (intención pregunta 1).
2. **Costo total:** ¿incluye seguros, comisiones u otros cargos, o solo capital e intereses? Si incluye cargos, RF-02 y sus ejemplos cambian (intención pregunta 2).
3. **Valores del banco:** ¿la tasa máxima de 26 % y el endeudamiento máximo de 40 % de `banco.yaml` son los vigentes? Hoy están marcados como ejemplos (intención pregunta 3; RN-04 y RN-05).
4. **Hojas actuales:** ¿usan sistema de cuota fija? Si usan otro, ¿cuál debe quedar como oficial? Si los resultados difieren, ¿qué se hace con los resultados que los asesores ya comunicaron a clientes? (intención pregunta 4 y sección 9 de la intención).
5. **Casos de referencia:** ¿pueden compartirse casos ya saneados, con datos sintéticos, que reproduzcan los resultados de cada oficina? Sin ellos, RF-05 no puede verificarse (intención pregunta 5).
6. **Meta de tiempo de cotización:** ¿cuál es la meta de tiempo para entregar una cotización al cliente? Hoy está "por definir" (intención §4).
7. **Última cuota:** con la cuota redondeada al peso, ¿la última cuota absorbe la diferencia de redondeo o se mantienen todas iguales (S-03)? Cambia el costo total en pocos pesos.
8. **Texto de aviso (RF-06):** ¿quién define el texto que ve el cliente y cuál es? Hoy el criterio pide solo que exista el aviso.
9. **Tasa desde `svc-tasas`:** el catálogo define `svc-tasas` como la fuente oficial de la tasa para simulaciones. ¿El banco quiere que el simulador consulte esa tasa y `tasa_maxima_ea` (en lugar de digitar la tasa), o solo debe validarla contra `banco.yaml`? Hay dos fuentes posibles para la misma regla (RN-04); hay que elegir una. Si consulta el servicio, la sección 7 y la sección 6 cambian.
10. **Ingresos y otras cuotas desde `svc-clientes`:** ese servicio devuelve ingresos y otras cuotas del cliente (restringidos). ¿Se mantiene la digitación del asesor, como pide la intención, o el simulador debe consultarlos? Consultarlos reduce errores de digitación, pero la intención excluye los sistemas del core y habría que revisar el alcance.
11. **Endeudamiento por encima del máximo:** RF-04 dice que no se muestran cifras válidas, pero la sección 9 y el criterio de endeudamiento de RF-04 muestran el 52,6 % con el veredicto "no le alcanza". ¿Se muestran la cuota y el costo total en ese caso, o solo el indicador y el motivo? RF-06 hoy oculta cuota y costo en todo rechazo.

---
*Estado: borrador. Pendiente de aprobación del dueño del producto antes de pasar al plan técnico.*
