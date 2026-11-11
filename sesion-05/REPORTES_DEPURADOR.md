# Sesión 5 · Reportes para practicar con el agente Depurador

En la demo, una asesora reporta un error del simulador y el **Depurador** lo reproduce con una prueba antes de corregirlo. Aquí tiene reportes del mismo estilo para cada reto sugerido de la sesión 2. Úselos en el paso 4 de [`TAREA.md`](TAREA.md).

## Cómo usarlos

1. Elija un reporte de su reto. Cambie los números y los RN por los de **su** `spec.md` y `banco.yaml` (los de aquí usan los valores de ejemplo de `banco.yaml`). Datos siempre sintéticos.
2. Cree la rama y abra el agente:

   ```bash
   git switch -c correccion/<caso>-<que-falla>      # por ejemplo correccion/transferencias-limite-diario
   claude --agent depurador
   ```

   En Copilot: elija **Depurador** en el selector de agentes.
3. Pegue el reporte con este formato:

   ```text
   Un <usuario> reporta: <qué hizo, con datos sintéticos>. El sistema <qué pasó>, pero según la especificación <qué debería pasar> (<RN o clave de banco.yaml>). Encuentra la causa raíz y corrígela, prueba primero.
   ```

4. Lea lo que hace: primero escribe una prueba que reproduce el reporte.
   - **La prueba falla:** el reporte es real. El Depurador busca la causa raíz, la corrige con el cambio mínimo y la prueba queda en verde.
   - **La prueba pasa:** el reporte **no se reproduce**. No hay nada que corregir: la prueba se queda como prueba de regresión y usted le responde a quien reportó con esa evidencia. También es un buen resultado.
   - **La especificación no dice qué debería pasar:** el Depurador no lo decide. Queda como pregunta abierta para el dueño del producto.
5. Siga con el paso 4 de `TAREA.md`: `git diff`, commit, revisión y pull request.

Si ningún reporte se reproduce y quiere ver al Depurador corregir algo, siga [**Si no encuentra un error**](#si-no-encuentra-un-error-cambie-una-regla).

## 1. Validador de transferencias

Reglas de `banco.yaml`: monto mínimo 1.000, límite diario 10.000.000, GMF 4 por mil.

- **Límite diario en el borde.** "Un cliente ya había transferido 9.000.000 hoy e intentó 1.000.000 más. El sistema la rechazó por límite diario, pero 10.000.000 es justo el límite permitido."
- **Redondeo del GMF.** "Una transferencia de 1.000.125 cobró GMF de 4.000. 1.000.125 × 0,004 = 4.000,5, que con ROUND_HALF_UP da 4.001 (`convenciones.dinero`)."
- **Fondos con el GMF.** "Una cuenta con saldo 1.003.000 transfirió 1.000.000 y quedó en negativo. Con el GMF necesitaba 1.004.000."
- **Cuenta bloqueada.** "Se aceptó una transferencia hacia una cuenta bloqueada."
- **Datos en el mensaje.** "Al rechazar por fondos insuficientes, el mensaje muestra el saldo completo de la cuenta. Los saldos son datos restringidos (`datos.clasificacion`, `politicas.seguridad`)."

## 2. Modernizar la conciliación heredada

Estos reportes son sobre el comportamiento del script de 2017. Pruébelos contra **su** versión modernizada: si conserva el comportamiento, la pregunta es si ese comportamiento era un error.

- **Referencias duplicadas.** "El extracto trae dos movimientos con la misma referencia y montos distintos. El reporte de diferencias solo muestra uno: el otro desapareció."
- **Dos diferencias a la vez.** "Un movimiento tiene distinto monto y también distinta fecha (por más de un día). El reporte solo dice `DIF_MONTO`; la diferencia de fecha no aparece."
- **Tolerancia de un centavo.** "Dos movimientos difieren en exactamente 0,01 y a veces aparecen como diferencia y a veces no, según los montos."
- **Neto con decimales raros.** "El neto de diferencias del reporte sale como 0,30000000000000004 en vez de 0,30 (`convenciones.dinero`: nunca float)."

## 3. Alertas de transacciones inusuales

Use los umbrales de **su** spec (cantidad de transferencias, ventana de horas, monto "pequeño").

- **Borde de la ventana.** "Una cuenta recibió 5 transferencias pequeñas en exactamente 2 horas y no se generó alerta. La spec dice 5 o más en 2 horas."
- **Borde del monto.** "Una transferencia de exactamente el monto límite de 'pequeña' no se contó para la alerta."
- **Cambio de día.** "Tres transferencias a las 23:30 y dos a las 00:15 del día siguiente no generaron alerta: el sistema reinicia el conteo a medianoche."
- **Datos en la alerta.** "La alerta que llega al área de fraude trae el número de cuenta completo. Las cuentas se muestran con los últimos 4 dígitos (`datos.reglas`)."

## 4. Generador de extractos

- **Último día del mes.** "Un movimiento del 31 de octubre a las 23:30 no aparece en el extracto de octubre."
- **Saldo que no cuadra.** "En el extracto, saldo inicial + créditos − débitos no da el saldo final: difiere en 1 peso."
- **Enmascarado.** "El extracto muestra los primeros 4 dígitos de la cuenta y oculta los últimos. Debe ser al revés (`datos.reglas`)."
- **Mes sin movimientos.** "Para un cliente sin movimientos en el mes, el extracto da un error en vez de mostrar saldo inicial igual a saldo final."

## 5. API de productos de un cliente

- **Cliente sin productos.** "Para un cliente sin productos, la API responde un error 500. Debería responder que no tiene productos."
- **Formato de error.** "Con un identificador de cliente inválido, la respuesta trae la traza de Python. Los errores deben venir como `{codigo, mensaje, id_correlacion}` y no revelar detalles internos (`politicas.apis`, `politicas.seguridad`)."
- **Montos como texto.** "El saldo llega como número (`1234567.5`) y no como texto decimal (`\"1234567.50\"`) (`politicas.apis`)."
- **Producto cancelado.** "Un producto cancelado aparece con estado activo en la respuesta."
- **Enmascarado.** "La respuesta trae el número de cuenta completo y el canal solo necesita los últimos 4 dígitos (`datos.reglas`, minimización)."

## 6. Calculadora de capacidad de pago

Reglas de `banco.yaml`: endeudamiento máximo 0,40; monto de 1.000.000 a 100.000.000; plazo de 6 a 72 meses; tasa máxima 26 % E.A.

- **Endeudamiento en el borde.** "Un cliente con endeudamiento resultante de exactamente 40 % aparece como que no puede pagar. El máximo es 40 %, incluido."
- **Monto fuera del producto.** "Para un cliente con ingresos muy altos, la calculadora recomienda 150.000.000. El monto máximo del crédito de consumo es 100.000.000."
- **Plazo fuera del producto.** "Para bajar la cuota, la calculadora recomienda 84 meses. El plazo máximo es 72."
- **Ingresos en cero.** "Con ingresos de 0, la pantalla muestra un error técnico (división por cero) en vez de pedir ingresos mayores que cero."
- **Tasa mensual.** "La cuota recomendada no coincide con la del simulador: parece usar la tasa anual dividida por 12 (`convenciones.tasas`: mensual = (1 + ea)^(1/12) − 1)."

## 7. Pruebas para un módulo existente (`transferencias`)

Este módulo es el de la sesión 1. Su trabajo es la suite de pruebas: si una prueba del reporte falla, el Depurador corrige el **módulo**, nunca el valor esperado.

- **Datos en el mensaje.** "Al rechazar por fondos insuficientes, el mensaje muestra el saldo de la cuenta. Los saldos son restringidos y los errores no deben revelar detalles internos."
- **Límite diario y GMF.** "Un cliente transfirió en el día 9.990.000 más un GMF de 39.960, y el sistema aceptó otra transferencia de 10.000. ¿El límite diario incluye el GMF?" (si la spec no lo dice, es pregunta abierta, no defecto).
- **Mínimo fuera de `banco.yaml`.** "Cambiamos `productos.transferencias.monto_minimo` en `banco.yaml` a 5.000 y el módulo sigue aceptando transferencias de 1.000."
- **Origen bloqueado.** "Desde una cuenta bloqueada con saldo suficiente, el mensaje dice fondos insuficientes en vez de cuenta no activa."

## Si no encuentra un error: cambie una regla

Que ningún reporte se reproduzca es buena noticia: su código cumple esos bordes y las pruebas nuevas se quedan como regresión. Para practicar con el Depurador, cambie una regla de una de estas dos formas. Las dos se hacen **en `main` y antes de crear la rama de corrección**, como si las hubiera hecho un compañero.

### Opción 1 · Cambiar la regla en el código (un error)

El código deja de cumplir la especificación: es un error de verdad, y el Depurador lo trata así. Mejor en pareja, para que quien depura no sepa qué línea cambió.

1. En `main` y sin cambios pendientes (`git switch main` y `git status --short` vacío), busque la regla con `grep -rn "<palabra>" src/` (por ejemplo `limite`, `tolerancia`, `enmascar`, `endeudamiento`, `gmf`), ábrala en VS Code y cambie **una sola cosa**. Si su código está escrito al revés (`<=` para aceptar), cambie el operador contrario (`<=` por `<`). Con `git diff` debe ver una sola línea cambiada. Ideas por reto:

   | Reto | Cambio en el código | Reporte que lo descubre |
   |---|---|---|
   | 1 · Transferencias | En el límite diario, `>` por `>=` | "Con 9.000.000 ya transferidos rechazó 1.000.000 más; 10.000.000 es justo el límite." |
   | 1 · Transferencias | En fondos, comparar contra `monto` y no contra `monto + gmf` | "Con saldo 1.003.000 transfirió 1.000.000 y quedó en negativo." |
   | 2 · Conciliación | En la tolerancia, `>` por `>=` | "Dos movimientos que difieren en exactamente la tolerancia aparecen como diferencia." |
   | 3 · Alertas | En el conteo, `>=` por `>` | "5 transferencias pequeñas en 2 horas no generaron alerta; la spec dice 5 o más." |
   | 4 · Extractos | En el filtro de fechas, `<=` por `<` en el fin de mes | "El movimiento del último día del mes no aparece." |
   | 5 · API de productos | En el enmascarado, `[-4:]` por `[:4]` | "La respuesta muestra los primeros 4 dígitos de la cuenta y no los últimos." |
   | 6 · Capacidad de pago | En el endeudamiento, `>` por `>=` | "Con endeudamiento de exactamente 40 % dice que no puede pagar." |
   | 7 · Módulo `transferencias` | En `calcular_gmf`, `ROUND_HALF_UP` por `ROUND_DOWN` | "1.000.125 cobró GMF de 4.000; debía ser 4.001." |

2. Confírmelo como si fuera de otra persona, y mire si sus pruebas lo atrapan:

   ```bash
   git -c user.name="Compañero del equipo" -c user.email=companero@equipo.example commit -am "Ajuste en <la regla>"
   python -m pytest -q
   ```

   - **Todo en verde:** el error quedó escondido, como en la demo. Siga al paso 3.
   - **Alguna prueba falla:** su suite ya tenía ese borde y atrapó el error antes que el usuario. Eso también es una lección. Deshaga el cambio con `git revert --no-edit HEAD` y pruebe con otro de la tabla.

3. Haga el flujo de siempre: `git switch -c correccion/<caso>-<que-falla>`, `claude --agent depurador` y el reporte de la tabla. El Depurador reproduce con una prueba, encuentra el commit del "compañero" como causa raíz y lo corrige.

### Opción 2 · Cambiar la regla en `banco.yaml` (el banco cambió la política)

Sirve para descubrir **valores fijos en el código**. Ejemplo: en `banco.yaml`, `limite_diario: 10000000` pasa a `5000000`, y el reporte dice:

```text
Cambiamos productos.transferencias.limite_diario a 5.000.000 en banco.yaml y el sistema sigue aceptando una transferencia de 8.000.000. Encuentra la causa raíz y corrígela, prueba primero.
```

Puede pasar una de dos cosas:

- **El sistema sigue aceptando 8.000.000:** el código tiene el valor fijo y no lee `banco.yaml`. Es un defecto (las reglas tienen un solo origen): el Depurador lo corrige para que lea el valor de `banco.yaml`.
- **El sistema ya rechaza, pero fallan pruebas que esperaban 10.000.000:** no es un error, es un **cambio de requisito**. El Depurador no cambia los valores esperados para que pasen (`politicas.depuracion`). Primero se actualiza la regla RN en `spec.md` y se aprueba; después se ajustan las pruebas.

Si solo cambió `banco.yaml` para probar, al final déjelo como estaba (`git restore banco.yaml`) o no lo incluya en el commit.

> **La regla de oro:** si el código no hace lo que dice la spec, es un error y va al Depurador. Si lo que cambió es la regla, es un requisito nuevo y va primero a la spec.

## Si su reto no está aquí

Los errores que más aparecen en un banco caben en estos patrones. Escriba el reporte con uno de ellos:

| Patrón | Ejemplo de reporte |
|---|---|
| Borde de una regla (`>` en vez de `>=`) | "Con justo el valor máximo, el sistema lo rechazó." |
| Redondeo o `float` | "El total difiere en 1 peso del cálculo a mano." |
| Fechas y horas | "Lo del último día del mes, o de las 23:59, no aparece." |
| Datos restringidos | "El log, el mensaje o la respuesta trae la cédula, la cuenta o el saldo completos." |
| Valor fijo en el código | "Cambiamos el valor en `banco.yaml` y el sistema sigue usando el anterior." |
| Caso vacío | "Sin movimientos, sin productos o sin datos, el sistema da un error técnico." |
