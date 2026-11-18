# Plan: Simulador único de crédito de consumo

| Campo | Valor |
|---|---|
| Caso | `simulador-credito-consumo` |
| Estado | aprobado |
| Especificación | [`spec.md`](spec.md) (aprobada por la docente del curso) |
| Autor | Equipo de desarrollo (redactado por el asistente, solicitado por la docente del curso) |
| Fecha | 2026-11-05 |
| Aprobado por | la docente del curso (líder técnico) |

## 1. Resumen técnico
Se crea el paquete `simulador_credito` con cinco capas. El dominio calcula tasa mensual, cuota fija, costo total y endeudamiento, y valida monto, plazo, tasa y endeudamiento con los valores de `banco.yaml` (`productos.credito_consumo`), que llegan como parámetros. El caso de uso `simular_credito` orquesta dominio y puertos. Los datos del asesor se digitan y pasan por validación de borde; no se consulta ningún servicio del banco. Los parámetros y el registro de eventos entran por puertos, con adaptadores en memoria para pruebas y adaptadores reales (lectura de `banco.yaml` y registro JSON). La interfaz para asesores es una app Streamlit. El primer componente es el cálculo de cuota en `dominio/calculos.py` (pasos 1 a 3).

## 2. Estructura
```text
src/simulador_credito/
├── dominio/        calculos.py, reglas.py, entradas.py, simulacion.py
├── puertos/        parametros_producto.py, registro_eventos.py
├── casos_uso/      simular_credito.py
├── adaptadores/    parametros_en_memoria.py, registro_eventos_en_memoria.py,
│                   parametros_desde_banco.py, registro_eventos_json.py
└── app/            interfaz_asesor.py
tests/              test_calculos.py, test_reglas.py, test_entradas.py,
                    test_simular_credito.py, test_parametros_desde_banco.py,
                    test_registro_eventos_json.py, test_interfaz_asesor.py
```

## 3. Componentes
| Capa | Archivo | Responsabilidad | Cubre (RF / RN) |
|---|---|---|---|
| dominio | `dominio/calculos.py` | `calcular_tasa_mensual`, `calcular_cuota_mensual` (sistema de cuota fija, redondeo solo al final), `calcular_costo_total`, `calcular_endeudamiento`. Sin validaciones de rango | RF-01, RF-02, RF-03; RN-06, RN-07 |
| dominio | `dominio/reglas.py` | `validar_monto`, `validar_plazo`, `validar_tasa`, `validar_endeudamiento`. Devuelven un motivo de rechazo con la regla incumplida; no lanzan excepciones para el flujo normal | RF-03, RF-04; RN-01 a RN-05 |
| dominio | `dominio/entradas.py` | `convertir_decimal`: texto del asesor a `Decimal`; rechaza vacío, no numérico, plazo con decimales y tasa con formato no reconocible | RF-04 (último criterio); sección 9 de la spec |
| dominio | `dominio/simulacion.py` | Clases `ParametrosProducto`, `DatosSimulacion`, `ResultadoSimulacion` (incluye moneda `COP`, aviso de simulación y motivo de rechazo) | RF-02 (moneda), RF-05, RF-06 |
| puertos | `puertos/parametros_producto.py` | `ProveedorParametrosProducto` (Protocol): entrega `ParametrosProducto` | RN-01 a RN-05 (origen de los valores) |
| puertos | `puertos/registro_eventos.py` | `RegistroEventos` (Protocol): registra un evento con nivel | Política de logs |
| casos_uso | `casos_uso/simular_credito.py` | `simular_credito`: valida, calcula, arma el resultado y registra el evento | RF-01 a RF-06 |
| adaptadores | `adaptadores/parametros_en_memoria.py` | `ProveedorParametrosEnMemoria`: doble para pruebas | Pruebas |
| adaptadores | `adaptadores/registro_eventos_en_memoria.py` | `RegistroEventosEnMemoria`: guarda eventos en una lista para verificarlos | Pruebas |
| adaptadores | `adaptadores/parametros_desde_banco.py` | `ProveedorParametrosDesdeBanco`: lee `productos.credito_consumo` de `banco.yaml` con pyyaml y convierte cada valor a `Decimal` por texto | RN-01 a RN-05 |
| adaptadores | `adaptadores/registro_eventos_json.py` | `RegistroEventosJson`: escribe JSON con fecha, nivel, servicio, id_correlacion y evento | Política de logs |
| app | `app/interfaz_asesor.py` | Formulario Streamlit: captura los datos, llama a `simular_credito` y muestra resultado, motivo y aviso | RF-06; sección 9 |

## 4. Puertos y adaptadores
| Puerto | Qué abstrae | Adaptador para pruebas | Adaptador real |
|---|---|---|---|
| `ProveedorParametrosProducto` | Valores del producto (montos, plazo, tasa máxima, endeudamiento máximo) | `ProveedorParametrosEnMemoria` | `ProveedorParametrosDesdeBanco` (archivo `banco.yaml`) |
| `RegistroEventos` | Escritura de eventos de negocio y rechazos | `RegistroEventosEnMemoria` | `RegistroEventosJson` |

No hay adaptador a servicios del catálogo en esta versión:
- `svc-tasas` (tasa E.A. y `tasa_maxima_ea`): no se usa. La tasa la digita el asesor y se valida contra `banco.yaml` (supuesto S-04). Si la pregunta 9 cambia la decisión, se agrega un adaptador `svc-tasas` detrás de `ProveedorParametrosProducto`, sin tocar el dominio.
- `svc-clientes` (ingresos y otras cuotas): no se usa. La intención pide digitación (pregunta 10).

## 5. Nombres validados
| Tipo | Nombre | `validar_nombre` |
|---|---|---|
| paquete | `simulador_credito` | OK (el nombre `simulador_credito_consumo` fue rechazado por largo) |
| modulo | `calculos`, `reglas`, `entradas`, `simulacion`, `parametros_producto`, `registro_eventos`, `parametros_en_memoria`, `parametros_desde_banco`, `registro_eventos_json`, `interfaz_asesor` | OK |
| modulo | `registro_eventos_en_memoria` | Pendiente de validar (paso 8) |
| caso_uso | `simular_credito` | OK |
| funcion | `calcular_tasa_mensual`, `calcular_cuota_mensual`, `calcular_costo_total`, `calcular_endeudamiento`, `validar_monto`, `validar_plazo`, `validar_tasa`, `validar_endeudamiento`, `convertir_decimal` | OK |
| clase | `ParametrosProducto`, `DatosSimulacion`, `ResultadoSimulacion`, `ProveedorParametrosProducto`, `RegistroEventos`, `ProveedorParametrosEnMemoria`, `RegistroEventosEnMemoria`, `ProveedorParametrosDesdeBanco`, `RegistroEventosJson` | OK |
| prueba | `test_<regla>_<caso>` (ejemplos: `test_cuota_mensual_10m_36_meses`, `test_monto_minimo_999999_rechaza`, `test_tasa_mensual_desde_ea`) | OK (todas las de la sección 6 siguen el mismo patrón) |

## 6. Pruebas
Todas usan datos sintéticos y valores esperados calculados aparte (no copiados de la salida del código). Las pruebas no llaman servicios reales.

| Criterio de aceptación (spec) | Archivo | Prueba |
|---|---|---|
| RF-01 · cuota 10.000.000 / 36 meses / 26 % | `tests/test_calculos.py` | `test_cuota_mensual_10m_36_meses` (388.846) |
| RF-01 · cuota 1.000.000 / 6 meses / 26 % | `tests/test_calculos.py` | `test_cuota_mensual_1m_6_meses` (178.192) |
| RF-01 · cuota 100.000.000 / 72 meses / 26 % | `tests/test_calculos.py` | `test_cuota_mensual_100m_72_meses` (2.592.471) |
| RF-01 · tasa mensual desde E.A. (RN-06) | `tests/test_calculos.py` | `test_tasa_mensual_desde_ea` |
| RF-01 · redondeo solo al final (RN-07) | `tests/test_calculos.py` | `test_cuota_mensual_redondeo_solo_al_final` (caso elegido para que redondear la tasa antes cambie la cuota; valor esperado calculado aparte) |
| RF-02 · costo total 10.000.000 / 36 meses | `tests/test_calculos.py` | `test_costo_total_10m_36_meses` (13.998.456) |
| RF-02 · costo total 1.000.000 / 6 meses | `tests/test_calculos.py` | `test_costo_total_1m_6_meses` (1.069.152) |
| RF-02 · costo total junto a cuota, plazo y COP | `tests/test_simular_credito.py` | `test_resultado_muestra_costo_en_cop` |
| RF-03 · endeudamiento 22,2 % y sí alcanza | `tests/test_calculos.py` y `tests/test_reglas.py` | `test_endeudamiento_22_2_por_ciento_le_alcanza` |
| RF-03 · endeudamiento 52,6 % y no alcanza | `tests/test_calculos.py` y `tests/test_reglas.py` | `test_endeudamiento_52_6_por_ciento_no_le_alcanza` |
| RF-03 · ingresos 0 no calcula | `tests/test_calculos.py` | `test_endeudamiento_ingresos_cero_no_calcula` |
| RF-04 · monto 999.999 rechaza (RN-01) | `tests/test_reglas.py` | `test_monto_minimo_999999_rechaza` |
| RF-04 · monto 1.000.000 acepta (borde RN-01) | `tests/test_reglas.py` | `test_monto_minimo_1000000_acepta` |
| RF-04 · monto 100.000.001 rechaza (RN-02) | `tests/test_reglas.py` | `test_monto_maximo_100000001_rechaza` |
| RF-04 · monto 100.000.000 acepta (borde RN-02) | `tests/test_reglas.py` | `test_monto_maximo_100000000_acepta` |
| RF-04 · plazo 5 rechaza (RN-03) | `tests/test_reglas.py` | `test_plazo_5_meses_rechaza` |
| RF-04 · plazo 6 acepta (borde RN-03) | `tests/test_reglas.py` | `test_plazo_6_meses_acepta` |
| RF-04 · plazo 73 rechaza (RN-03) | `tests/test_reglas.py` | `test_plazo_73_meses_rechaza` |
| RF-04 · plazo 72 acepta (borde RN-03) | `tests/test_reglas.py` | `test_plazo_72_meses_acepta` |
| RF-04 · tasa 27 % rechaza (RN-04) | `tests/test_reglas.py` | `test_tasa_27_ea_rechaza` |
| RF-04 · tasa 26 % acepta (borde RN-04) | `tests/test_reglas.py` | `test_tasa_26_ea_acepta` |
| RF-04 · endeudamiento 52,6 % no válido (RN-05) | `tests/test_reglas.py` | `test_endeudamiento_52_6_no_valido` |
| RF-04 · endeudamiento 40 % exacto acepta (borde RN-05) | `tests/test_reglas.py` | `test_endeudamiento_40_por_ciento_acepta` |
| RF-04 · campo vacío pide corregir | `tests/test_entradas.py` | `test_campo_vacio_pide_correccion` |
| RF-04 · valor no numérico pide corregir | `tests/test_entradas.py` | `test_campo_no_numerico_pide_correccion` |
| Sección 9 · plazo 12,5 rechaza | `tests/test_entradas.py` | `test_plazo_12_5_meses_rechaza` |
| Sección 9 · tasa con formato no reconocible | `tests/test_entradas.py` | `test_tasa_formato_no_reconocible_pide_tasa` |
| Sección 9 · otras cuotas vacías piden dato | `tests/test_entradas.py` | `test_otras_cuotas_vacias_pide_dato` |
| RF-04 · rechazo no calcula cuota ni costo | `tests/test_simular_credito.py` | `test_rechazo_no_muestra_cuota_ni_costo` |
| RF-05 · misma entrada, mismo resultado | `tests/test_simular_credito.py` | `test_misma_entrada_mismo_resultado` |
| RF-05 · casos de referencia (0 diferencias) | pendiente | `test_resultado_coincide_casos_referencia`. Se escribe cuando la pregunta 5 tenga casos saneados |
| RF-06 · resultado válido con aviso | `tests/test_simular_credito.py` | `test_resultado_valido_muestra_aviso` |
| RF-06 · rechazo solo con motivo y aviso | `tests/test_simular_credito.py` | `test_rechazo_muestra_motivo_y_aviso` |
| Política de logs · rechazo en WARNING | `tests/test_simular_credito.py` | `test_rechazo_registra_warning` |
| Política de logs · sin datos restringidos | `tests/test_registro_eventos_json.py` | `test_registro_json_no_incluye_ingresos_ni_otras_cuotas` |
| RN-01 a RN-05 · valores leídos de `banco.yaml` como `Decimal` | `tests/test_parametros_desde_banco.py` | `test_parametros_desde_banco_convierte_tasa_a_decimal` (usa un `banco.yaml` sintético en directorio temporal) |
| RF-06 · aviso visible en la interfaz | `tests/test_interfaz_asesor.py` | `test_aviso_visible_en_interfaz` (con `streamlit.testing.v1.AppTest`) |

## 7. Pasos (en orden, prueba primero)
- [x] **Paso 1 · Estructura.** `python herramientas/crear_estructura.py simulador_credito`. Listo cuando: existen las cinco capas y `python herramientas/verificar_capas.py` dice OK.
- [x] **Paso 2 · Tasa y cuota (RF-01).** Prueba: `test_tasa_mensual_desde_ea`, `test_cuota_mensual_10m_36_meses`, `test_cuota_mensual_1m_6_meses`, `test_cuota_mensual_100m_72_meses`, `test_cuota_mensual_redondeo_solo_al_final`. Ver las cinco fallar. Implementación: `dominio/calculos.py` (`calcular_tasa_mensual`, `calcular_cuota_mensual`) con `Decimal`. Listo cuando: pasan en verde.
- [x] **Paso 3 · Costo total (RF-02).** Prueba: `test_costo_total_10m_36_meses`, `test_costo_total_1m_6_meses`. Implementación: `calcular_costo_total` en `dominio/calculos.py`. Listo cuando: pasan en verde.

**Primer componente:** pasos 1 a 3 (cálculo de cuota y costo total, dominio puro, con pruebas en verde).

- [x] **Paso 4 · Endeudamiento (RF-03).** Prueba: `test_endeudamiento_22_2_por_ciento_le_alcanza`, `test_endeudamiento_52_6_por_ciento_no_le_alcanza`, `test_endeudamiento_ingresos_cero_no_calcula`. Implementación: `calcular_endeudamiento` en `dominio/calculos.py`. Listo cuando: pasan en verde.
- [x] **Paso 5 · Reglas del banco (RF-04, RN-01 a RN-05).** Prueba: las 12 pruebas de `tests/test_reglas.py` de la sección 6 (bordes incluidos). Implementación: `dominio/reglas.py`. Los valores llegan como parámetros, no se leen de archivos. Listo cuando: pasan en verde.
- [x] **Paso 6 · Entradas del asesor (validación en el borde).** Prueba: las cinco pruebas de `tests/test_entradas.py`. Implementación: `dominio/entradas.py` (`convertir_decimal`). Listo cuando: pasan en verde.
- [x] **Paso 7 · Modelos y puertos.** Sin prueba propia: `dominio/simulacion.py` (`ParametrosProducto`, `DatosSimulacion`, `ResultadoSimulacion` con moneda `COP`), `puertos/parametros_producto.py` y `puertos/registro_eventos.py`. Las pruebas de los pasos 8 y 9 los cubren. Listo cuando: `verificar_capas.py` dice OK.
- [x] **Paso 8 · Caso de uso con dobles (RF-02 moneda, RF-05, RF-06).** Prueba: `test_resultado_valido_muestra_aviso`, `test_rechazo_no_muestra_cuota_ni_costo`, `test_rechazo_muestra_motivo_y_aviso`, `test_rechazo_registra_warning`, `test_misma_entrada_mismo_resultado`, `test_resultado_muestra_costo_en_cop`. Implementación: `casos_uso/simular_credito.py`, `adaptadores/parametros_en_memoria.py`, `adaptadores/registro_eventos_en_memoria.py`. Antes, validar `registro_eventos_en_memoria` con `validar_nombre`. Listo cuando: pasan en verde.
- [x] **Paso 9 · Adaptador de parámetros desde `banco.yaml`.** Prueba: `test_parametros_desde_banco_convierte_tasa_a_decimal` (con `banco.yaml` sintético en directorio temporal). Implementación: `adaptadores/parametros_desde_banco.py`. Convierte `0.26` a `Decimal("0.26")` por texto, nunca desde float. Listo cuando: pasa en verde.
- [x] **Paso 10 · Registro de eventos en JSON.** Prueba: `test_registro_json_no_incluye_ingresos_ni_otras_cuotas`. Implementación: `adaptadores/registro_eventos_json.py` con los campos fecha, nivel, servicio, id_correlacion y evento. Solo registra el id de la regla (por ejemplo RN-01), nunca ingresos ni otras cuotas. Listo cuando: pasa en verde.
- [x] **Paso 11 · Interfaz de asesor (RF-06).** Prueba: `test_aviso_visible_en_interfaz`. Implementación: `app/interfaz_asesor.py` con Streamlit. Los mensajes de error no muestran trazas. Listo cuando: pasa en verde y la app arranca.
- [ ] **Paso 12 · Casos de referencia (RF-05, pendiente).** Solo cuando la pregunta 5 tenga casos saneados: `test_resultado_coincide_casos_referencia` con 0 diferencias.
- [x] **Paso 13 · Cierre.** `python herramientas/verificar_capas.py` dice OK; `python -m pytest -q` en verde; cobertura del dominio ≥ 0,80 (`convenciones.pruebas.cobertura_minima_dominio`).

## 8. Dependencias
| Paquete | Para qué | ¿Aprobada en `banco.yaml`? |
|---|---|---|
| pytest | Pruebas | sí |
| pyyaml | Leer `banco.yaml` en `ProveedorParametrosDesdeBanco` | sí |
| streamlit | Interfaz del asesor (`app/interfaz_asesor.py`) y `AppTest` para su prueba | sí |

No se agregan dependencias. `decimal` es de la biblioteca estándar.

## 9. Decisiones técnicas y riesgos
- **D1 · Cálculo con `Decimal`.** Todo el dinero y las tasas usan `decimal.Decimal`; el redondeo es `ROUND_HALF_UP` al peso y solo al final. La potencia fraccionaria `(1 + ea) ** (1/12)` se calcula con precisión de contexto alta (por ejemplo 50 dígitos) para no redondear antes.
- **D2 · Tasa mensual.** Se deriva siempre como `(1 + ea) ** (1/12) - 1`; nunca `ea / 12` (RN-06).
- **D3 · Costo total.** Por defecto es la cuota redondeada por el plazo (S-02 y S-03). Si la pregunta 7 cambia la última cuota, se ajusta solo `calcular_costo_total`.
- **D4 · Fuente de la tasa y de los ingresos.** Se digitan (S-04 e intención). No se consulta `svc-tasas` ni `svc-clientes` hasta resolver las preguntas 9 y 10. El diseño por puertos permite agregarlos sin tocar el dominio.
- **D5 · Rechazo y endeudamiento.** Si una regla falla, no se muestran cuota ni costo (RF-06, sección 9). Para endeudamiento por encima del máximo, el resultado muestra el porcentaje y el veredicto "no le alcanza", sin cuota ni costo. Esto es un valor por defecto hasta resolver la pregunta 11.
- **D6 · Interfaz.** Streamlit es la única interfaz de esta versión y está aprobada. La especificación no fija la tecnología de interfaz; **el líder técnico debe confirmar esta elección.** Si el banco necesita una API, sería una capa `app` nueva con FastAPI y ruta `/v1/simulaciones`, con errores en formato `{codigo, mensaje, id_correlacion}` (`politicas.apis`). Queda fuera de este plan.
- **D7 · Logs.** Se registra el evento y el id de la regla rechazada (WARNING). Nunca se registran ingresos ni otras cuotas (datos restringidos).
- **R1 · Valores de ejemplo.** Tasa máxima (0,26) y endeudamiento máximo (0,40) están marcados como ejemplos en `banco.yaml`. Las constantes no se fijan en el código: cambian solo en `banco.yaml`.
- **R2 · pyyaml convierte decimales a `float`.** `ProveedorParametrosDesdeBanco` debe convertir por texto (`Decimal(str(valor))`) y la prueba del paso 9 lo verifica.
- **R3 · Valores esperados.** Los valores de la spec se verifican con un cálculo aparte (no copiado de la salida del código). Si una cifra de la spec no coincide, se corrige la spec antes de cerrar la prueba.
- **R4 · Contradicción en la spec.** Los criterios de RF-03 y RF-04 (52,6 % mostrado) y RF-04 (sin cifras válidas) se contradicen hasta resolver la pregunta 11. La prueba `test_endeudamiento_52_6_no_valido` sigue D5.

## 10. Fuera de este plan
- Aprobación o negación de crédito, scoring y consulta a centrales de riesgo o core (fuera de alcance en la intención y la spec).
- Desembolso, registro de solicitud y contrato.
- Seguros, comisiones y otros cargos (pregunta 2 de la spec).
- Retiro de las hojas de cálculo actuales (etapa posterior).
- Integración con `svc-tasas` y `svc-clientes` (preguntas 9 y 10).
- API pública (hoy la interfaz es Streamlit).
- Texto legal del aviso (pregunta 8); el plan implementa el aviso como constante configurable.

## 11. Preguntas abiertas
1. **Estado de la spec.** La tabla de cabecera dice `aprobada`, pero el pie dice `Estado: borrador. Pendiente de aprobación del dueño del producto`. Confirmar que la aprobación vigente es la de cabecera antes de aprobar este plan.
2. **RN-08 en la spec.** S-01 cita "RN-08", que no existe en la tabla de reglas (sección 5). Confirmar si la cuota fija debe agregarse como regla o queda como supuesto.
3. **Tecnología de interfaz (D6).** ¿Streamlit es aceptable para los asesores, o se necesita otra forma de acceso?
4. **Preguntas de la spec que este plan asume:** 1 y 9 (tasa digitada, sin `svc-tasas`), 2 (costo total sin cargos), 7 (última cuota), 10 (ingresos digitados) y 11 (qué se muestra al superar el endeudamiento). Si alguna cambia, se revisa el paso correspondiente.
5. **Valores del banco (pregunta 3 de la spec):** tasa máxima 26 % y endeudamiento 40 % son ejemplos; deben confirmarse antes de producción.
6. **Casos de referencia (pregunta 5 de la spec):** sin casos saneados no se puede cerrar RF-05 (paso 12).
7. **Dependencias:** ninguna nueva. Si durante la implementación se necesita otra, se pregunta antes de instalarla.
