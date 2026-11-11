# Sesión 5 · Práctica y tarea: su primer pull request revisado

**Trabajo individual.** Usted hace con **su** reto (uno de los 7 retos sugeridos de la sesión 2) lo mismo que vio en la demo:

1. Un "compañero" deja un error en `main`. Como trabaja solo, **ese compañero es usted**: siembra el error a propósito.
2. El agente **Depurador** lo encuentra y lo corrige en una rama.
3. El agente **Revisor** revisa esa rama.
4. Usted abre un **pull request** en GitHub y decide si se fusiona.

Al terminar, su `mi-reto` está en GitHub y la corrección entra a `main` por un pull request revisado.

Todo se hace en **Git Bash**, dentro de `mi-reto`, con el entorno del curso activo (`source .venv/Scripts/activate`).

Antes de empezar, tenga a mano dos datos de su reto:

| Dato | Dónde lo ve | Ejemplo |
|---|---|---|
| **El nombre de su caso** | La carpeta en `docs/sdlc/` | `validador-transferencias` |
| **El número de la regla** que va a romper | La tabla de reglas de negocio de su `spec.md` | `RN-03` |

En esta guía, `<caso>` y `RN-xx` significan **esos** dos datos suyos.

---

## Paso 1 · Poner al día su repositorio · 3 min

Desde la carpeta del curso, con el material nuevo:

```bash
bash proyectos/poner_al_dia.sh ../mi-reto
```

Trae la **versión 3**: los agentes `depurador` y `revisor`, la skill `/revisar`, las convenciones de ramas, commits y pull requests en `banco.yaml` y la plantilla del pull request. Después cierre y vuelva a abrir `claude` en `mi-reto` (en VS Code: *Reload Window*).

## Paso 2 · ¿Funciona lo de la sesión 4? · 3 min

```bash
cd ../mi-reto
python -m pytest -q
python herramientas/verificar_capas.py
```

- **Todo en verde:** siga al paso 3. En el paso 4 va a sembrar su error.
- **Algo falla:** ya tiene un error real. Siga al paso 3 y **sáltese el paso 4**: en el paso 5 el reporte es ese error (*"Al correr python -m pytest -q falla <prueba>…"*).

## Paso 3 · Su repositorio en GitHub · 8 min

1. En https://github.com: **New repository** → nombre `mi-reto`, **Private**, sin README, sin `.gitignore` y sin licencia → **Create repository**.
2. En Git Bash, dentro de `mi-reto` (cambie `<usuario>` por el suyo):

```bash
git status                      # debe estar limpio; si no, haga commit antes
git remote add origin https://github.com/<usuario>/mi-reto.git
git push -u origin main
```

La primera vez se abre el navegador para iniciar sesión en GitHub. Recargue la página del repositorio: debe ver sus archivos y `docs/sdlc/`.

## Paso 4 · Sembrar su error en `main` · 7 min

Usted hace de "compañero del equipo": cambia **un solo operador** en una regla de su reto, para que el sistema se equivoque justo en el borde. Así como el compañero de la demo, lo hace en `main` y con un commit a su nombre. La tarjeta de su reto, más abajo en **[Las 7 tarjetas](#las-7-tarjetas-qué-error-sembrar-en-su-reto)**, dice qué buscar, qué cambiar y qué reporte usar.

1. **Esté en `main` y sin cambios pendientes:**

   ```bash
   git switch main
   git status --short              # no debe mostrar nada
   ```

2. **Encuentre la regla.** Use la palabra de búsqueda de su tarjeta:

   ```bash
   grep -rn "<palabra>" src/
   ```

   Abra en VS Code el archivo que aparece y ubique la línea de la tarjeta. Su código puede estar escrito distinto: lo que busca es **la comparación que decide la regla**. ¿No la encuentra? Pregúntele a Claude en una sesión normal: `¿En qué archivo y línea se decide <la regla>? No cambies nada.`, y salga con `/exit`.

3. **Cambie solo el operador** como dice su tarjeta y guarde. Si su código está escrito al revés (por ejemplo `<=` para aceptar en vez de `>` para rechazar), cambie el operador contrario (`<=` por `<`).

4. **Compruebe que cambió una sola línea:**

   ```bash
   git diff                        # una línea en rojo (antes) y una en verde (después)
   ```

5. **Haga commit como si fuera otra persona:**

   ```bash
   git -c user.name="Compañero del equipo" -c user.email=companero@equipo.example commit -am "Ajuste en <la regla>"
   git log --oneline -2            # el último commit es del Compañero del equipo
   ```

6. **Corra las pruebas:**

   ```bash
   python -m pytest -q
   ```

   - **En verde:** el error quedó escondido, como en la demo: ninguna prueba mira justo el borde. **Siga al paso 5.**
   - **En rojo:** su suite ya tenía ese borde y atrapó el error antes que el usuario. ¡Bien por sus pruebas! Deshaga el cambio con `git revert --no-edit HEAD` y vuelva al punto 2 con el **plan B** de su tarjeta.

No haga `git push` de este commit todavía: el paso 7 sube todo junto.

## Paso 5 · El Depurador, en una rama · 12 min

1. **Cree la rama de corrección** (formato de `convenciones.ramas`; el nombre sugerido está en su tarjeta):

   ```bash
   git switch -c correccion/<caso>-<que-falla>
   claude --agent depurador
   ```

   En Copilot: elija **Depurador** en el selector de agentes del chat.

2. **Pegue el reporte de su tarjeta**, con sus números y su RN. No le diga dónde sembró el error: el reporte describe lo que vio el usuario, no la línea.

3. **Mire cómo trabaja.** Debe ver, en este orden:
   - una prueba nueva que **falla** con los datos del reporte (reproduce el error);
   - la causa raíz, explicada en una o dos frases (debe dar con su línea, y con `git log` puede ver el commit del "compañero");
   - el cambio mínimo que la corrige y la prueba en **verde**;
   - `pytest` y la regla de capas en verde.

   Si quiere corregir algo más o cambia un valor esperado de una prueba existente, no lo acepte: la política `politicas.depuracion` dice que primero se reproduce y nunca se cambia un valor esperado para que pase.

4. **Salga, revise y haga commit** (formato de `convenciones.commits`: qué y por qué, con su RN):

   ```bash
   /exit
   git diff                        # la prueba nueva y su línea corregida
   python -m pytest -q
   git add -A
   git commit -m "Corrige <qué>: <por qué> (RN-xx)"
   ```

## Paso 6 · El Revisor, en la misma rama · 7 min

En la demo, la docente revisó la rama de otro compañero, que preparó antes de clase. **Usted revisa la suya**, la del paso 5, que ya tiene la corrección. El Revisor compara la rama en la que está contra `main`.

```bash
git branch --show-current       # debe decir correccion/<caso>-...
claude --agent revisor
```

```text
/revisar <caso>
```

En Copilot: agente **Revisor** y `/revisar <caso>`, o el botón **Revisar los cambios** al final de la respuesta del Depurador.

El Revisor deja `docs/sdlc/<caso>/revision.md` con hallazgos **bloqueantes**, **importantes** y **sugerencias**. No toca el código ni aprueba: **usted decide**. En una corrección pequeña es normal que salgan hallazgos como: la prueba nueva sin el docstring `Regla: …`, falta probar el borde vecino (justo por debajo y justo por encima), o el commit no cita el RN.

Léalo y guárdelo en la rama:

```bash
/exit
git add docs/sdlc
git commit -m "Revisión de la corrección de <qué> (borrador)"
```

## Paso 7 · Su primer pull request · 5 min

```bash
git switch main
git push                        # sube el commit del "compañero" a main en GitHub
git switch correccion/<caso>-<que-falla>
git push -u origin correccion/<caso>-<que-falla>
```

En GitHub aparece **Compare & pull request**:

- **Título** (`convenciones.pull_requests`): una línea en español, como un commit, que dice qué entra a `main` y por qué, citando su RN. Use el de su tarjeta. Si GitHub propone el nombre de la rama, cámbielo.
- **Descripción:** ya trae la plantilla del equipo. Escriba el caso, la rama y la etapa (corrección); marque **solo** las casillas que sean verdad (si `revision.md` tiene bloqueantes, esa casilla queda vacía); y en la última sección, en una o dos frases, qué hizo el Depurador y qué revisó y decidió usted.

**Create pull request** y pegue como comentario la sección 7 de `revision.md`.

- **Sin bloqueantes:** cambie `Estado` de `revision.md` a `aprobado` con su nombre (dueño del código), commit, `git push` y **Merge pull request**. Luego: `git switch main && git pull`.
- **Con bloqueantes:** **no lo fusione todavía**. Queda para casa.

---

## Las 7 tarjetas: qué error sembrar en su reto

Cada tarjeta trae: la palabra para buscar la regla, cómo se ve la línea, el cambio, el reporte para el Depurador, la rama y el título del commit y del pull request. Los números son los de `banco.yaml` del curso: si su `spec.md` usa otros, use los suyos. Cambie `RN-xx` por el número de la regla en su `spec.md`.

### Reto 1 · Validador de transferencias

| | |
|---|---|
| **Buscar** | `grep -rn "limite" src/` |
| **La línea se ve como** | `if ya_debitado + monto > limite_diario:` (rechaza si se pasa del límite) |
| **Cambio** | `>` por `>=` |
| **Reporte** | `Un cliente reporta: ya había transferido 9.000.000 hoy e intentó transferir 1.000.000 más. El sistema la rechazó por límite diario, pero según la especificación 10.000.000 es justo el límite permitido (RN-xx, productos.transferencias.limite_diario). Encuentra la causa raíz y corrígela, prueba primero.` |
| **Rama** | `correccion/<caso>-limite-diario` |
| **Commit y título del PR** | `Corrige el límite diario: transferir hasta el límite es permitido (RN-xx)` |
| **Plan B** | Monto mínimo: `grep -rn "minimo" src/`, en `if monto < monto_minimo:` cambie `<` por `<=`. Reporte: *"Una transferencia de 1.000 fue rechazada por monto mínimo, y el mínimo es 1.000."* |

### Reto 2 · Modernizar la conciliación heredada

Siembre el error en **su** versión modernizada (en `src/`), no en `legacy/`.

| | |
|---|---|
| **Buscar** | `grep -rn "tolerancia" src/` |
| **La línea se ve como** | `if abs(diferencia) > tolerancia:` (reporta diferencia de monto si supera la tolerancia) |
| **Cambio** | `>` por `>=` |
| **Reporte** | `El área de conciliación reporta: dos movimientos con la misma referencia difieren en exactamente 0,01 y el reporte los marca como DIF_MONTO. Con tolerancia de 0,01 no son diferencia, igual que en el script de 2017 (RN-xx). Encuentra la causa raíz y corrígela, prueba primero.` |
| **Rama** | `correccion/<caso>-tolerancia` |
| **Commit y título del PR** | `Corrige la tolerancia: una diferencia igual a la tolerancia no se reporta (RN-xx)` |
| **Plan B** | Fechas: `grep -rn "days" src/`, en `if abs(dias) > 1:` cambie `>` por `>=`. Reporte: *"Dos movimientos con un día de diferencia en la fecha aparecen como DIF_FECHA; el script de 2017 los acepta."* |

### Reto 3 · Alertas de transacciones inusuales

| | |
|---|---|
| **Buscar** | `grep -rn "umbral\|minimo" src/` |
| **La línea se ve como** | `if cantidad >= umbral_transferencias:` (alerta con 5 o más en la ventana) |
| **Cambio** | `>=` por `>` |
| **Reporte** | `El área de fraude reporta: una cuenta recibió 5 transferencias pequeñas en 2 horas y no se generó alerta. Según la especificación, 5 o más en 2 horas deben alertar (RN-xx). Encuentra la causa raíz y corrígela, prueba primero.` |
| **Rama** | `correccion/<caso>-umbral-alerta` |
| **Commit y título del PR** | `Corrige el umbral: 5 transferencias en la ventana generan alerta (RN-xx)` |
| **Plan B** | Monto pequeño: `grep -rn "pequen\|monto" src/`, en `if monto <= monto_pequeno:` cambie `<=` por `<`. Reporte: *"Una transferencia de exactamente el monto límite de 'pequeña' no se contó para la alerta."* |

### Reto 4 · Generador de extractos

| | |
|---|---|
| **Buscar** | `grep -rn "fecha" src/` |
| **La línea se ve como** | `if inicio <= movimiento.fecha <= fin:` (movimientos del mes, ambos días incluidos) |
| **Cambio** | El segundo `<=` por `<` |
| **Reporte** | `Un cliente reporta: un movimiento del 31 de octubre no aparece en su extracto de octubre. Según la especificación, el extracto incluye todos los movimientos del mes, hasta el último día (RN-xx). Encuentra la causa raíz y corrígela, prueba primero.` |
| **Rama** | `correccion/<caso>-fin-de-mes` |
| **Commit y título del PR** | `Corrige el corte: el extracto incluye el último día del mes (RN-xx)` |
| **Plan B** | Enmascarado: `grep -rn "enmascar\|\[-4:\]" src/`, cambie `[-4:]` por `[:4]`. Reporte: *"El extracto muestra los primeros 4 dígitos de la cuenta y oculta los últimos (datos.reglas)."* |

### Reto 5 · API de productos de un cliente

| | |
|---|---|
| **Buscar** | `grep -rn "enmascar\|\[-4:\]" src/` |
| **La línea se ve como** | `return "*" * (len(numero) - 4) + numero[-4:]` (deja visibles los últimos 4) |
| **Cambio** | `numero[-4:]` por `numero[:4]` |
| **Reporte** | `El canal digital reporta: la respuesta de la API muestra los primeros 4 dígitos del número de cuenta y oculta los últimos. Según la especificación, solo se muestran los últimos 4 dígitos (RN-xx, datos.reglas). Encuentra la causa raíz y corrígela, prueba primero.` |
| **Rama** | `correccion/<caso>-enmascarado` |
| **Commit y título del PR** | `Corrige el enmascarado: muestra los últimos 4 dígitos de la cuenta (RN-xx)` |
| **Plan B** | Estado: `grep -rn "activ\|cancel" src/`, en el filtro de productos activos cambie `==` por `!=`. Reporte: *"Un producto cancelado aparece como activo y uno activo no aparece."* |

### Reto 6 · Calculadora de capacidad de pago

| | |
|---|---|
| **Buscar** | `grep -rn "endeudamiento" src/` |
| **La línea se ve como** | `if endeudamiento > endeudamiento_maximo:` (no puede pagar si se pasa del 40 %) |
| **Cambio** | `>` por `>=` |
| **Reporte** | `Un asesor reporta: para un cliente con endeudamiento resultante de exactamente 40 %, la calculadora dice que no puede pagar. Según la especificación, el máximo es 40 % e incluye el 40 % (RN-xx, productos.credito_consumo.endeudamiento_maximo). Encuentra la causa raíz y corrígela, prueba primero.` |
| **Rama** | `correccion/<caso>-endeudamiento-maximo` |
| **Commit y título del PR** | `Corrige el endeudamiento: 40 % exacto es permitido (RN-xx)` |
| **Plan B** | Plazo: `grep -rn "plazo" src/`, en `if plazo > plazo_maximo:` cambie `>` por `>=`. Reporte: *"La calculadora no recomienda 72 meses aunque es el plazo máximo permitido."* |

### Reto 7 · Pruebas para el módulo `transferencias`

El archivo es `src/transferencias/dominio/casos_uso/realizar_transferencia.py`.

| | |
|---|---|
| **Buscar** | `grep -n "limite_diario" src/transferencias/dominio/casos_uso/realizar_transferencia.py` |
| **La línea es** | `if ya_debitado + monto > self._limite_diario:` |
| **Cambio** | `>` por `>=` |
| **Reporte** | `Un cliente reporta: ya había transferido 9.000.000 hoy e intentó transferir 1.000.000 más. El sistema la rechazó por límite diario, pero 10.000.000 es justo el límite permitido (RN-xx, productos.transferencias.limite_diario). Encuentra la causa raíz y corrígela, prueba primero.` |
| **Rama** | `correccion/<caso>-limite-diario` |
| **Commit y título del PR** | `Corrige el límite diario: transferir hasta el límite es permitido (RN-xx)` |
| **Plan B** | Monto mínimo: en la misma función, `if monto < MONTO_MINIMO:` cambie `<` por `<=`. Reporte: *"Una transferencia de 1.000 fue rechazada por monto mínimo, y el mínimo es 1.000."* Como su reto es la suite de pruebas, es probable que la atrape (paso 4, punto 6): eso demuestra que su suite funciona. |

### ¿Su reto es otro?

Elija una regla de su `spec.md` con un límite (mínimo, máximo, umbral, fecha de corte) y cambie el operador de la comparación (`>` ↔ `>=`, `<` ↔ `<=`). El reporte describe al usuario que probó **justo** el valor del límite. Más ideas en [`REPORTES_DEPURADOR.md`](REPORTES_DEPURADOR.md).

---

## En casa

1. Atienda los hallazgos bloqueantes e importantes de `revision.md` (o escriba en el pull request por qué no). En Claude Code: `claude --agent desarrollador` y `Atiende los hallazgos H-01 y H-02 de docs/sdlc/<caso>/revision.md`; en Copilot, el botón **Atender los hallazgos** del Revisor.
2. Haga commit y `git push`: el pull request se actualiza solo.
3. Vuelva a revisar con `/revisar <caso>` (el Revisor agrega una ronda nueva).
4. Sin bloqueantes: cambie `Estado` de `revision.md` a `aprobado` con su nombre (dueño del código), commit, push y **Merge pull request** en GitHub. Luego, en su computador: `git switch main && git pull`.
5. Envíe por el canal el enlace de su pull request fusionado (o una captura si no quiere compartir el repositorio).
6. Opcional: practique otra vez con el plan B de su tarjeta, o con un reporte de [`REPORTES_DEPURADOR.md`](REPORTES_DEPURADOR.md).

**Comandos de Git de hoy**

| Para | Comando |
|---|---|
| Ver en qué rama está | `git branch --show-current` |
| Ver si hay cambios sin commit | `git status --short` |
| Ver qué cambió | `git diff` |
| Commit como otra persona (solo para sembrar el error) | `git -c user.name="Compañero del equipo" -c user.email=companero@equipo.example commit -am "..."` |
| Deshacer el último commit con otro commit | `git revert --no-edit HEAD` |
| Crear una rama y pasarse a ella | `git switch -c <tipo>/<caso>-<descripcion>` |
| Volver a `main` y traer lo fusionado | `git switch main && git pull` |
| Subir la rama | `git push -u origin <rama>` (la primera vez), luego `git push` |
| Ver qué cambió frente a `main` | `git diff main...HEAD --stat` |
