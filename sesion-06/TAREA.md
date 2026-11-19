# Sesión 6 · Práctica y tarea: la especificación probada, con el hook encendido

**Hoy en clase todos trabajamos el mismo caso: el simulador de crédito de la docente.** Cada uno crea con un comando una copia idéntica (mismo código, misma historia de git, mismo punto de partida) y **hace lo mismo que la docente, paso a paso**. En casa repite lo aprendido en su reto (`mi-reto`).

Todo en **Git Bash**, con el entorno del curso activo (`source .venv/Scripts/activate`). **Abra `claude` desde esa terminal**: el hook usa el Python del entorno para correr `pytest`.

## 0. Material nuevo y dependencia · antes de empezar

1. Traiga el material nuevo del curso: descargue el `.zip` y descomprímalo **sobre** la carpeta del curso (o `git pull`).
2. En la carpeta del curso:

```bash
pip install pytest-cov
```

## 1. Su copia del caso de la docente · 3 min

> **¿Hizo el [`TRABAJO_AUTONOMO.md`](TRABAJO_AUTONOMO.md)?** Ya tiene `demo-clase` en GitHub: no lo vuelva a crear. Solo entre (`cd ../demo-clase`), corra `python -m pytest -q` (47 passed) y siga con la tabla de comprobaciones de abajo.

Si no lo hizo, desde la carpeta del curso:

```bash
python proyectos/nivelar_clase.py ../demo-clase --sesion 6
cd ../demo-clase
python -m pytest -q                         # 47 passed
python herramientas/verificar_capas.py      # OK
git log --oneline -4
```

Debe ver los mismos cuatro commits que la docente; el último es **"Pantalla del asesor con lo que pidieron las oficinas"**, de un compañero. `demo-clase` ya trae el agente del equipo en la **versión 4**: el agente `verificador`, la skill `/pruebas`, la herramienta `datos_sinteticos` y el hook del equipo. Abra VS Code en `demo-clase` y, en la terminal, `claude`.

Compruebe en `claude`:

| Qué | Lo que debe pasar |
|---|---|
| `/hooks` | Aparece un hook **PostToolUse** con `verificar_cambio.py` |
| `/mcp` | `banco` conectado, con la herramienta `datos_sinteticos` |
| `Dame 3 clientes sintéticos con la forma de svc-clientes` | Llama a `datos_sinteticos` y devuelve `CLI-SIN-0001`… |

En Copilot: la herramienta aparece en el selector de herramientas del chat; el hook se ve en el panel **Output → GitHub Copilot Chat Hooks** después de una edición.

> ¿Ya existe `../demo-clase`? Use otro nombre: `python proyectos/nivelar_clase.py ../demo-clase-2 --sesion 6`.

## 2. Cobertura: verde no es cubierto · con la docente

```bash
python -m pytest -q --cov=src/simulador_credito/dominio --cov-report=term-missing
```

Fíjese en el porcentaje del dominio. Pregunta para la clase: con esa cobertura y todo en verde, ¿está probado lo que **ve** el asesor?

## 3. El Verificador · con la docente, 15 min

```bash
git switch pruebas/simulador-credito-consumo-verificacion     # ya existe si hizo el trabajo autónomo
# si dice que no existe: git switch -c pruebas/simulador-credito-consumo-verificacion
claude --agent verificador
```

```text
/pruebas simulador-credito-consumo
```

En Copilot: agente **Verificador** y `/pruebas simulador-credito-consumo`.

Mientras trabaja, fíjese en:
- la matriz: los criterios que hablan de lo que **ve** el asesor, ¿están probados en la pantalla o solo en el caso de uso?
- los datos: ¿usó `datos_sinteticos`?
- si una prueba nueva falla, la marca con `@pytest.mark.xfail(strict=True, reason="Posible defecto: …")` y **no toca `src/`**.

Al final:

```bash
/exit
python -m pytest -q                  # N passed, M xfailed
git show HEAD --stat                 # todavía es el commit del compañero: ¿qué cambió?
```

Compare con lo que encontró la docente **y con su `matriz-a-mano.md`**: ¿el agente encontró lo mismo que usted? Si a usted le salió distinto (otro número de pruebas, otro criterio), dígalo en clase: es la misma spec, revisada por otra sesión del agente.

## 4. Guardar su trabajo · 3 min

```bash
git add tests docs
git commit -m "Pruebas de lo que ve el asesor y matriz (RF-02, RF-06, sección 9)"
git push -u origin pruebas/simulador-credito-consumo-verificacion
```

En GitHub, abra el pull request de esa rama hacia `main` con la plantilla del repositorio. Título: `Pruebas de lo que ve el asesor y matriz (RF-02, RF-06, sección 9)`. No lo fusione todavía: los tres posibles defectos van al Depurador.

Si `demo-clase` todavía no está en GitHub, súbalo primero como dice el paso 2 de [`TRABAJO_AUTONOMO.md`](TRABAJO_AUTONOMO.md).

## 5. Ver el hook en acción · con la docente, 5 min

Salga del Verificador y pídale a `claude` (sesión normal) algo que rompa la regla de capas:

```text
Agrega a src/simulador_credito/dominio/simulacion.py una función mostrar_resultado(resultado) que pinte el resultado con streamlit (import streamlit as st, st.metric para la cuota).
```

Debe aparecer **Hook del equipo: el cambio rompe una verificación** y el agente corregirlo solo, moviendo el código a `app/`. Si no aparece, revise `/hooks` y que abrió `claude` con el entorno activo.

Después, deshaga ese cambio de prueba: `git restore src` (sus pruebas ya quedaron guardadas en el paso 4).

## En casa: lo mismo, en su reto

1. Ponga al día su reto: desde la carpeta del curso, `bash proyectos/poner_al_dia.sh ../mi-reto` y, en `mi-reto`, `git switch main && git pull`.
2. `git switch -c pruebas/<caso>-verificacion`, `claude --agent verificador` y `/pruebas <caso>`.
3. Para cada posible defecto: `git switch -c correccion/<caso>-<defecto>` y `claude --agent depurador`: `Corrige el posible defecto de <prueba> marcado en docs/sdlc/<caso>/pruebas.md y quita la marca xfail.` (En Copilot, el botón **Depurar los posibles defectos** del Verificador.) Fíjese en que el hook corre solo después de cada edición.
4. Revise con `/revisar <caso>`, abra el pull request y fusione sin bloqueantes.
5. Envíe por el canal el enlace (o captura) de su PR de pruebas y la cobertura del dominio (`python -m pytest -q --cov=src/<paquete>/dominio`).
