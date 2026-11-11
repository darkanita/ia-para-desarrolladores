# Sesión 5 · Práctica y tarea: su primer pull request revisado

Al terminar, su `mi-reto` está en GitHub, el trabajo nuevo vive en una rama y entra a `main` por un pull request revisado por el agente Revisor.

Todo se hace en **Git Bash**, con el entorno del curso activo (`source .venv/Scripts/activate`).

## 1. Poner al día su repositorio · se hace en el bloque de las 0:10

Desde la carpeta del curso, con el material nuevo:

```bash
bash proyectos/poner_al_dia.sh ../mi-reto
```

Trae la **versión 3**: los agentes `depurador` y `revisor`, la skill `/revisar`, las políticas de revisión y depuración y la plantilla nueva del pull request. Después cierre y vuelva a abrir `claude` en `mi-reto` (en VS Code: *Reload Window*).

## 2. ¿Funciona lo de la sesión 4? · 3 min

```bash
cd ../mi-reto
python -m pytest -q
python herramientas/verificar_capas.py
```

Anote el resultado: lo usa en el paso 4.

## 3. Su repositorio en GitHub · 8 min

1. En https://github.com: **New repository** → nombre `mi-reto`, **Private**, sin README, sin `.gitignore` y sin licencia (su repositorio ya los tiene) → **Create repository**.
2. En Git Bash, dentro de `mi-reto` (cambie `<usuario>` por el suyo):

```bash
git status                      # debe estar limpio; si no, haga commit antes
git remote add origin https://github.com/<usuario>/mi-reto.git
git push -u origin main
```

La primera vez se abre el navegador para iniciar sesión en GitHub (Git Credential Manager). Recargue la página del repositorio: debe ver sus archivos y `docs/sdlc/`.

## 4. Una rama y el agente que corresponde · 12 min

Nadie trabaja en `main`. Cree la rama según lo que salió en el paso 2 (formato de `convenciones.ramas`):

**Si algo falló (pruebas en rojo o capas con violaciones)** → rama de corrección y agente **depurador**:

```bash
git switch -c correccion/<caso>-<que-falla>
claude --agent depurador
```

```
Al correr python -m pytest -q falla <prueba o error>. Encuentra la causa raíz y corrígela, prueba primero.
```

**Si todo está en verde y quiere practicar con el depurador** → use un reporte de su reto en [`REPORTES_DEPURADOR.md`](REPORTES_DEPURADOR.md) (uno por cada reto sugerido de la sesión 2), con la misma rama `correccion/<caso>-<que-falla>`. Si la prueba del reporte pasa, el reporte no se reproduce: la prueba queda como regresión y eso también se entrega.

**Si no encuentra ningún error y quiere ver al Depurador corregir uno** → cambie una regla, en `main` y antes de crear la rama (paso a paso en [`REPORTES_DEPURADOR.md`, sección "Si no encuentra un error"](REPORTES_DEPURADOR.md#si-no-encuentra-un-error-cambie-una-regla)):

- **En el código** (un error): cambie una sola cosa en la regla (por ejemplo `>` por `>=`), haga commit como "Compañero del equipo" y páselo al Depurador con un reporte. Mejor en pareja.
- **En `banco.yaml`** (el banco cambió la política): si el sistema no cambia, hay un valor fijo en el código y el Depurador lo corrige. Si fallan pruebas que esperaban el valor viejo, es un cambio de requisito: primero se actualiza `spec.md`, nunca el valor esperado.


**Si todo está en verde** → rama de funcionalidad y el siguiente paso de su plan con el agente **desarrollador**:

```bash
git switch -c funcionalidad/<caso>-paso-<n>
claude --agent desarrollador
```

```
Implementa el paso <n> del plan aprobado de <caso>.
```

En Copilot: elija **Depurador** o **Desarrollador** en el selector de agentes del chat.

Revise lo que hizo (`git diff`) y haga commit con un mensaje que diga qué y por qué (`convenciones.commits`):

```bash
git add -A
git commit -m "Corrige <qué> (RN-xx)"        # o "Agrega <qué> (RF-xx)"
```

## 5. La revisión · 7 min

En la demo, la docente revisó la rama de un compañero (`funcionalidad/...-casos-referencia`), que preparó antes de clase. **Usted no tiene esa rama: revisa la suya**, la del paso 4, ya con su commit. El Revisor compara la rama en la que está contra `main`. Compruebe dónde está con `git branch --show-current`.

```bash
claude --agent revisor
```

```
/revisar <caso>
```

En Copilot: agente **Revisor** y `/revisar <caso>` (o el botón **Revisar los cambios** al final de la respuesta del Desarrollador o del Depurador).

El Revisor deja `docs/sdlc/<caso>/revision.md` con hallazgos **bloqueantes**, **importantes** y **sugerencias**. Léalo: ¿está de acuerdo con cada uno? Guárdelo en la rama:

```bash
git add docs/sdlc
git commit -m "Revisión de <qué> (borrador)"
```

## 6. Su primer pull request · 3 min

```bash
git push -u origin <nombre-de-su-rama>
```

En GitHub aparece **Compare & pull request**.

- **Título** (`convenciones.pull_requests`): una línea en español, como un commit, que dice qué entra a `main` y por qué, citando RF/RN: `Agrega el cálculo de la cuota mensual (RF-02)`. Si la rama tiene varios commits, GitHub propone el nombre de la rama: cámbielo.
- **Descripción:** ya trae la plantilla del equipo. Escriba el caso, la rama y la etapa; marque solo las casillas que sean verdad (si `revision.md` tiene bloqueantes, esa casilla queda vacía); y en la última sección, en una o dos frases, qué hizo el agente y qué revisó y decidió usted.

Cree el pull request y pegue como comentario la sección 7 de `revision.md`. **No lo fusione todavía** si tiene hallazgos bloqueantes.

## Ejemplo completo con un reto

Una estudiante con el reto 1 (validador de transferencias). Su caso en `docs/sdlc/` se llama `validador-transferencias` (use el nombre de **su** carpeta). Sus pruebas están en verde y ningún reporte se reproduce, así que siembra un error para practicar.

```bash
# Paso 2: ¿funciona?
python -m pytest -q                                   # 18 passed

# Paso 4: un "compañero" cambia > por >= en el límite diario, en main
git -c user.name="Compañero del equipo" -c user.email=companero@equipo.example commit -am "Ajuste en el límite diario"
python -m pytest -q                                   # sigue en verde: el error quedó escondido

git switch -c correccion/validador-transferencias-limite-diario
claude --agent depurador
```
```text
Un cliente reporta: ya había transferido 9.000.000 hoy e intentó 1.000.000 más. El sistema la rechazó por límite diario, pero según la especificación 10.000.000 es justo el límite permitido (productos.transferencias.limite_diario). Encuentra la causa raíz y corrígela, prueba primero.
```
```bash
/exit
git diff                                              # la prueba nueva y el >= vuelto a >
git add -A
git commit -m "Corrige el límite diario: 10.000.000 es permitido (RN-03)"

# Paso 5: el Revisor, en la MISMA rama
claude --agent revisor
```
```text
/revisar validador-transferencias
```
```bash
/exit
git add docs/sdlc
git commit -m "Revisión de la corrección del límite diario (borrador)"

# Paso 6: el pull request
git push -u origin correccion/validador-transferencias-limite-diario
```

En GitHub: **Compare & pull request** → título `Corrige el límite diario: 10.000.000 es permitido (RN-03)` (GitHub propone el de un commit; si propone el nombre de la rama, cámbielo) → la plantilla → **Create pull request** → la sección 7 de `revision.md` como comentario.

Con cualquier otro reto es igual: cambian el nombre del caso, la rama, el reporte y el RN. Para los 7 retos:

| Reto | Rama de ejemplo | Título del commit y del PR |
|---|---|---|
| 1 · Transferencias | `correccion/<caso>-limite-diario` | `Corrige el límite diario: el máximo es permitido (RN-xx)` |
| 2 · Conciliación | `correccion/<caso>-tolerancia` | `Corrige la tolerancia: una diferencia igual a la tolerancia no se reporta (RN-xx)` |
| 3 · Alertas | `correccion/<caso>-umbral-alerta` | `Corrige el umbral: 5 transferencias en 2 horas generan alerta (RN-xx)` |
| 4 · Extractos | `correccion/<caso>-fin-de-mes` | `Corrige el corte: incluye los movimientos del último día del mes (RN-xx)` |
| 5 · API de productos | `correccion/<caso>-enmascarado` | `Corrige el enmascarado: muestra los últimos 4 dígitos (datos.reglas)` |
| 6 · Capacidad de pago | `correccion/<caso>-endeudamiento-maximo` | `Corrige el endeudamiento: 40 % exacto es permitido (RN-xx)` |
| 7 · Módulo `transferencias` | `correccion/<caso>-redondeo-gmf` | `Corrige el redondeo del GMF: ROUND_HALF_UP (convenciones.dinero)` |

Si en el paso 2 algo ya falló, o si prefiere avanzar con el plan, el flujo es el mismo con su rama (`correccion/...` con el depurador, o `funcionalidad/<caso>-paso-<n>` con el desarrollador).

## En casa

1. Atienda los hallazgos bloqueantes e importantes (o escriba en el pull request por qué no). En Claude Code: `claude --agent desarrollador` y `Atiende los hallazgos H-01 y H-02 de docs/sdlc/<caso>/revision.md`; en Copilot, el botón **Atender los hallazgos** del Revisor.
2. Haga commit y `git push`: el pull request se actualiza solo.
3. Vuelva a revisar con `/revisar <caso>` (el Revisor agrega una ronda nueva).
4. Sin bloqueantes: cambie `Estado` de `revision.md` a `aprobado` con su nombre (dueño del código), commit, push y **Merge pull request** en GitHub. Luego, en su computador: `git switch main && git pull`.
5. Envíe por el canal el enlace de su pull request fusionado (o una captura si no quiere compartir el repositorio).

**Comandos de Git de hoy**

| Para | Comando |
|---|---|
| Ver en qué rama está | `git branch --show-current` |
| Crear una rama y pasarse a ella | `git switch -c <tipo>/<caso>-<descripcion>` |
| Volver a `main` y traer lo fusionado | `git switch main && git pull` |
| Subir la rama | `git push -u origin <rama>` (la primera vez), luego `git push` |
| Ver qué cambió frente a `main` | `git diff main...HEAD --stat` |
