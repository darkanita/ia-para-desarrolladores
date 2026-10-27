# Simulador de crédito de consumo

## Pregunta de negocio

> Un cliente quiere un crédito de libre inversión. **¿Cuánto pagará cada mes, cuánto le costará en total y le alcanza con sus ingresos?**

Hoy el asesor lo calcula en una hoja de cálculo distinta en cada oficina y los resultados no coinciden. Queremos un simulador único, con las reglas del banco en un solo lugar, que el asesor use frente al cliente.

## Usuarios
- **Asesor comercial**: simula el crédito frente al cliente y le muestra el resultado en pantalla.

## Requisitos funcionales

1. **Datos de entrada**: monto solicitado, plazo en meses, tasa efectiva anual (E.A.), ingresos mensuales del cliente y cuotas mensuales que ya paga en otras deudas (puede ser 0).
2. **Validaciones** (si no se cumplen, se muestra un mensaje claro y no se calcula nada):
   - Monto entre $1.000.000 y $100.000.000.
   - Plazo entre 6 y 72 meses, entero.
   - Tasa E.A. mayor que 0 y menor o igual a la tasa máxima permitida: 26 % E.A. (valor de ejemplo, configurable en una constante).
   - Ingresos mensuales mayores que 0; otras cuotas mayores o iguales a 0.
3. **Cuota mensual** fija (sistema francés), con la tasa mensual equivalente a la E.A.
4. **Tabla de amortización**: por cada mes, número de cuota, cuota, interés, abono a capital y saldo. El saldo final es exactamente 0: la última cuota se ajusta para absorber las diferencias de redondeo.
5. **Resumen**: cuota mensual, total pagado y total de intereses.
6. **Capacidad de pago**: porcentaje de endeudamiento = (cuota + otras cuotas) / ingresos. El crédito es **aprobable** si ese porcentaje es menor o igual al 40 %. Mostrar también la **cuota máxima** que el cliente podría pagar: 40 % de los ingresos menos otras cuotas (nunca negativa).

## Interfaz (Streamlit, `app.py`)
- Formulario con los cinco datos de entrada. La tasa se escribe en porcentaje (24 = 24 % E.A.).
- Tres indicadores: cuota mensual, total de intereses y total pagado.
- Un semáforo de capacidad de pago: verde si es aprobable, rojo si no, con el porcentaje de endeudamiento y la cuota máxima.
- La tabla de amortización con los valores en pesos con separador de miles (`$1.234.567`).
- Un gráfico del saldo mes a mes.
- Un aviso visible: "Simulación con fines educativos. Datos sintéticos."

## Contrato del dominio (`simulador/dominio.py`)

Las pruebas de aceptación usan exactamente estos nombres:

| Nombre | Qué es |
|---|---|
| `DatosInvalidos` | Excepción de validación; hereda de `ValueError`. |
| `TASA_MAXIMA_EA` | `Decimal("0.26")` |
| `LIMITE_ENDEUDAMIENTO` | `Decimal("0.40")` |
| `tasa_mensual(tasa_ea) -> Decimal` | Tasa mensual equivalente, sin redondear. |
| `cuota_mensual(monto, tasa_ea, plazo_meses) -> Decimal` | Cuota fija, redondeada al peso. |
| `tabla_amortizacion(monto, tasa_ea, plazo_meses) -> list[Cuota]` | `Cuota` con los atributos `numero`, `cuota`, `interes`, `abono_capital`, `saldo` (Decimal en pesos). El interés de cada mes es el saldo anterior por la tasa mensual, redondeado al peso. |
| `resumen(monto, tasa_ea, plazo_meses) -> Resumen` | `Resumen` con `cuota`, `total_pagado`, `total_intereses`, calculados con la tabla. |
| `evaluar_capacidad(cuota, ingresos_mensuales, otras_cuotas) -> Evaluacion` | `Evaluacion` con `porcentaje_endeudamiento` (fracción, redondeada a 4 decimales), `aprobable` (bool) y `cuota_maxima` (redondeada al peso). |

Los montos llegan como `Decimal` o `int`; las tasas como `Decimal`.

## Fuera de alcance
- Seguros, comisiones, GMF y abonos extraordinarios.
- Guardar simulaciones o conectarse a sistemas del banco.

## Criterios de aceptación
- `python -m pytest -q` pasa.
- `streamlit run app.py` abre la aplicación y el ejemplo de $10.000.000 a 12 meses al 24 % E.A., con ingresos de $4.000.000 y otras cuotas de $500.000, muestra la cuota, el semáforo y la tabla completa.
