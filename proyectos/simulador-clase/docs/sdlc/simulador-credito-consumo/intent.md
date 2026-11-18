# Intención: Simulador único de crédito de consumo

| Campo | Valor |
|---|---|
| Caso | `simulador-credito-consumo` |
| Estado | aprobado |
| Autor | Equipo de desarrollo (solicitado por la docente del curso) |
| Fecha | 2026-10-29 |
| Aprobado por | la docente del curso (dueño del producto) |

## 1. Problema
Cada oficina calcula los créditos de consumo en su propia hoja de cálculo, así que el mismo cliente con los mismos datos puede recibir cuotas y totales distintos según quién lo atienda. Esto genera desconfianza con el cliente, reprocesos y riesgo de que se comprometa una condición que el banco no respalda. Hace falta un único punto de cálculo.

## 2. Usuarios
- **Usuario directo:** asesores comerciales de todas las oficinas, que hacen la simulación frente al cliente.
- **Beneficiarios:** el cliente, que recibe una cifra clara y comparable; el dueño del producto de crédito de consumo, que controla una sola versión de las condiciones; el área de control, que puede verificar los cálculos en un solo lugar.

## 3. Resultado esperado
Para los mismos datos de entrada, cualquier oficina obtiene el mismo resultado. Al simular un crédito de consumo, el asesor ve:
1. **Cuota mensual** que paga el cliente.
2. **Costo total del crédito** a lo largo del plazo.
3. **Si le alcanza con sus ingresos**: si el nivel de endeudamiento resultante (cuota nueva más otras cuotas, sobre ingresos) queda dentro del máximo permitido por el banco.

Si la simulación incumple una regla del banco (monto, plazo, tasa o endeudamiento), el simulador lo indica en lugar de mostrar una cifra como válida.

## 4. Cómo sabremos que funcionó
| Métrica | Hoy | Meta |
|---|---|---|
| Diferencias de resultado entre oficinas para un mismo conjunto de casos de referencia | Por medir (hoy hay hojas distintas) | 0 diferencias |
| Simulaciones aceptadas con tasa por encima de `tasa_maxima_ea` | Por medir | 0 |
| Oficinas que usan el simulador como única fuente de cálculo | Por medir | Todas las oficinas, al terminar el piloto (meta propuesta; confirmar) |
| Tiempo para entregar una cotización al cliente | Por medir | Por definir con el dueño del producto |

Nota: no hay línea base porque no existe una medición consolidada. Antes de la meta, hay que medir cuántas diferencias aparecen hoy con un mismo conjunto de casos.

## 5. Alcance
**Incluye:**
- Cálculo de la cuota mensual, el costo total y el indicador de endeudamiento para un crédito de consumo.
- Validación de monto, plazo, tasa y endeudamiento contra las reglas de `banco.yaml`.
- Un único origen de cálculo que usen todas las oficinas.

**No incluye:**
- Aprobación o negación del crédito, ni scoring o perfil de riesgo del cliente.
- Consulta a centrales de riesgo o a sistemas del core bancario.
- Desembolso, registro de la solicitud o contrato.
- Otros productos (transferencias, tarjetas, libranzas, etc.).
- Seguros, comisiones y otros cargos, salvo que el dueño del producto los incluya (ver preguntas abiertas).
- Reemplazo inmediato de las hojas actuales: su retiro se planea en una etapa posterior.

## 6. Tipo de entregable
Componente (simulador con interfaz para asesores) respaldado por un servicio de cálculo reutilizable. La elección concreta se define en la especificación y el plan.

## 7. Datos
| Dato | Clasificación (`banco.yaml`) | Origen | ¿Sintético? |
|---|---|---|---|
| Ingresos mensuales del cliente | restringida (datos financieros de clientes) | Digitados por el asesor | Sí, en desarrollo y pruebas |
| Otras cuotas mensuales del cliente | restringida (datos financieros de clientes) | Digitadas por el asesor | Sí, en desarrollo y pruebas |
| Monto, plazo y tasa E.A. de la simulación | confidencial (condiciones de negocio) | Digitados por el asesor o tomados de la tarifa vigente (ver preguntas) | Sí, en desarrollo y pruebas |
| Reglas del producto (montos, plazos, tasa máxima, endeudamiento máximo) | interna | `banco.yaml` | No aplica (son definiciones del banco) |
| Casos de referencia para validar resultados | restringida si provienen de hojas reales | Hojas actuales de las oficinas | Sí: deben sanearse antes de usarse |

## 8. Reglas del banco que aplican
| Regla | Clave en `banco.yaml` | Valor |
|---|---|---|
| Tasa efectiva anual máxima | `productos.credito_consumo.tasa_maxima_ea` | 0.26 (marcado en el archivo como valor de ejemplo) |
| Monto mínimo | `productos.credito_consumo.monto_minimo` | 1.000.000 COP |
| Monto máximo | `productos.credito_consumo.monto_maximo` | 100.000.000 COP |
| Plazo en meses | `productos.credito_consumo.plazo_meses` | Entre 6 y 72 meses |
| Endeudamiento máximo: (cuota + otras cuotas) / ingresos | `productos.credito_consumo.endeudamiento_maximo` | 0.40 (marcado en el archivo como valor de ejemplo) |
| Tasa en efectivas anuales; mensual = (1 + ea) ** (1/12) − 1 | `convenciones.tasas` | Convención de cálculo |
| Dinero en `Decimal`, redondeo al peso con ROUND_HALF_UP | `convenciones.dinero` | Convención de cálculo |

## 9. Riesgos y restricciones
- **Datos restringidos:** ingresos, deudas y condiciones de clientes reales no pueden usarse en desarrollo ni en pruebas, ni guardarse en logs, prompts o archivos del repositorio. Las hojas actuales pueden contener datos reales y deben revisarse antes de tomarse como referencia.
- **Valores de ejemplo:** la tasa máxima (26 %) y el endeudamiento máximo (40 %) están marcados como ejemplos en `banco.yaml`. Si no son los vigentes, todo el simulador queda mal calibrado.
- **Diferencias heredadas:** si las hojas actuales usan fórmulas distintas, el simulador cambiará resultados que los asesores ya comunicaron a clientes. Hay que decidir cómo tratar esos casos.
- **Cumplimiento y comunicación:** el resultado es una simulación, no una oferta. El texto que ve el cliente debe dejarlo claro; el contenido de ese texto lo define el área legal o de producto.
- **Cambio de hábito:** los asesores pueden seguir usando sus hojas. La meta de uso único depende de capacitación y de retirar o restringir las hojas.

## 10. Supuestos
- El cálculo usa **sistema de cuota fija** (amortización francesa): cada mes se paga la misma cuota.
- El **costo total** es la suma de las cuotas durante el plazo, sin seguros ni comisiones.
- La **tasa E.A.** la define el banco y el asesor no la modifica por encima de la tasa máxima.
- El indicador de "si le alcanza" es el **endeudamiento** de `banco.yaml` (cuota nueva más otras cuotas, sobre ingresos), comparado con el máximo permitido.
- Los **usuarios** son asesores de oficina; el cliente ve el resultado a través de ellos.
- Se trabaja con **datos sintéticos** en desarrollo y pruebas.

## 11. Preguntas abiertas
1. ¿La tasa E.A. la digita el asesor en cada simulación, o sale de una tabla de tarifas vigente? Esto cambia quién puede fijarla.
2. ¿El costo total debe incluir seguros, comisiones u otros cargos, o solo capital e intereses?
3. ¿Los valores 26 % (tasa máxima) y 40 % (endeudamiento máximo) de `banco.yaml` son los vigentes? Hoy están marcados como ejemplos.
4. ¿Las hojas actuales usan el sistema de cuota fija? Si usan otro, ¿cuál, y cuál debe quedar como oficial?
5. ¿Pueden compartirse casos de referencia ya saneados (datos sintéticos) que reproduzcan los resultados de cada oficina?
