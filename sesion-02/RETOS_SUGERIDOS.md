# Retos sugeridos · Banco Orquídea (ficticio)

Su reto es el caso que va a llevar por todo el ciclo AI SDLC, desde la intención hasta el proyecto final. Todos usan datos sintéticos y las reglas de `banco.yaml`. Puede proponer otro de su trabajo diario si cumple lo mismo.

El simulador de crédito de las demos es el **ejemplo resuelto**: no lo elija como reto.

## Los retos y cómo arrancar

Cada reto trae una idea para pegar después de `/intencion`. Úsela tal cual o ajústela con sus palabras.

### 1. Validador de transferencias
**Entregable:** componente o API. **Lo interesante:** límite diario, GMF, cuentas bloqueadas y enmascaramiento de datos.
```text
/intencion Antes de ejecutar una transferencia queremos validar que cumple las reglas del banco (límite diario, cuentas activas, fondos suficientes con el GMF) y explicar al usuario por qué se rechaza.
```

### 2. Modernizar la conciliación heredada
**Entregable:** modernización de código heredado. **Lo interesante:** código de 2017 sin pruebas, en `retos/conciliacion-legacy/`: entenderlo, probarlo y refactorizarlo sin cambiar lo que hace.
```text
/intencion Tenemos un script de conciliación de 2017 sin pruebas que nadie se atreve a tocar. Queremos entender qué hace, cubrirlo con pruebas y modernizarlo sin cambiar sus resultados.
```
Antes, copie el código a su repositorio (desde la carpeta del curso): `cp -r sesion-02/retos/conciliacion-legacy ../mi-reto/legacy` en Git Bash, o `Copy-Item -Recurse sesion-02\retos\conciliacion-legacy ..\mi-reto\legacy` en PowerShell. Después, `git add legacy` y `git commit -m "Código heredado de conciliación"`.

### 3. Alertas de transacciones inusuales
**Entregable:** proceso ETL más reglas. **Lo interesante:** reglas de monto, frecuencia y horario sobre datos sintéticos.
```text
/intencion Queremos alertar cuando una cuenta recibe muchas transferencias pequeñas en pocas horas, para que el área de fraude las revise.
```

### 4. Generador de extractos
**Entregable:** componente más reporte. **Lo interesante:** saldos, movimientos y formato, con los datos restringidos enmascarados.
```text
/intencion Los clientes piden su extracto mensual y hoy se arma a mano. Queremos generarlo con saldo inicial, movimientos y saldo final, sin mostrar datos restringidos completos.
```

### 5. API de productos de un cliente
**Entregable:** API con FastAPI. **Lo interesante:** contratos, validación y datos sintéticos de clientes.
```text
/intencion Los canales digitales necesitan consultar qué productos tiene un cliente y su estado, con una respuesta estándar y sin exponer datos que no necesitan.
```

### 6. Calculadora de capacidad de pago
**Entregable:** componente. **Lo interesante:** endeudamiento, otras deudas y recomendación de monto y plazo.
```text
/intencion Antes de ofrecer un crédito, el asesor quiere saber cuánto puede prestarle al cliente según sus ingresos y deudas, y con qué plazo le quedaría una cuota que pueda pagar.
```

### 7. Pruebas para un módulo existente
**Entregable:** suite de pruebas. **Lo interesante:** cobertura del dominio, casos borde y datos sintéticos. Puede usar el proyecto `proyectos/transferencias` de la sesión 1.
```text
/intencion El módulo de transferencias tiene pocas pruebas y nos da miedo cambiarlo. Queremos una suite que cubra sus reglas de negocio y los casos borde.
```
Antes, copie el módulo a su repositorio: `cp -r proyectos/transferencias/src ../mi-reto/src` (en PowerShell, `Copy-Item -Recurse proyectos\transferencias\src ..\mi-reto\src`), sin las pruebas que ya trae. Después, `git add src` y `git commit -m "Módulo de transferencias"`.

## Cuando el agente pregunte algo que no sabe

Responda lo que sepa. Para el resto: *"No lo sabemos aún; déjalo como pregunta abierta"*. Nunca invente cifras: si una regla no está en `banco.yaml`, queda como pregunta abierta o como supuesto.

## Cómo crece su reto en el curso

Cada sesión agrega un artefacto y una pieza al agente del equipo. El orden puede ajustarse.

| Sesión | Lo que hace con su reto |
|---|---|
| 2 | `intent.md`: el problema, para quién y cómo sabremos que funcionó |
| 3 | `spec.md` con `/spec`, usando las reglas del equipo y las herramientas del banco |
| 4 | `plan.md`: cómo construirlo, paso a paso |
| 5 | Construir con el agente; pasar a GitHub con ramas y pull requests |
| 6 | Pruebas y refactorización |
| 7 | Seguridad: vulnerabilidades, secretos y controles automáticos |
| 8 | Flujo DevOps con GitHub y empaquetado del agente del equipo |
| 9–10 | Proyecto final: el ciclo completo, de la intención a la entrega |
