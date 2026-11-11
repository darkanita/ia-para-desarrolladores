# Sesión 6 · Práctica y tarea: su especificación probada, con el hook encendido

Al terminar, cada criterio de aceptación de su `spec.md` tiene su prueba (o está anotado como posible defecto), la matriz queda en `docs/sdlc/<caso>/pruebas.md` y el hook del equipo corre la regla de capas y las pruebas cada vez que el agente edita código.

Todo en **Git Bash**, con el entorno del curso activo (`source .venv/Scripts/activate`). **Abra `claude` desde esa terminal**: el hook usa el Python del entorno para correr `pytest`.

## 1. Poner al día · se hace en el bloque de las 0:00

```bash
bash proyectos/poner_al_dia.sh ../mi-reto
pip install pytest-cov
cd ../mi-reto
git switch main && git pull          # trae lo que fusionó en GitHub
```

Trae la **versión 4**: el agente `verificador`, la skill `/pruebas`, la herramienta `datos_sinteticos` y el hook del equipo. Cierre y vuelva a abrir `claude`; en VS Code, *Reload Window*.

Compruebe en `claude`:

| Qué | Lo que debe pasar |
|---|---|
| `/hooks` | Aparece un hook **PostToolUse** con `verificar_cambio.py` |
| `/mcp` | `banco` conectado, con la herramienta `datos_sinteticos` |
| `Dame 3 clientes sintéticos con la forma de svc-clientes` | Llama a `datos_sinteticos` y devuelve `CLI-SIN-0001`… |

En Copilot: la herramienta aparece en el selector de herramientas del chat; el hook se ve en el panel **Output → GitHub Copilot Chat Hooks** después de una edición.

## 2. Una rama para las pruebas · 2 min

```bash
git switch -c pruebas/<caso>-verificacion
```

## 3. El Verificador · 15 min

```bash
claude --agent verificador
```

```
/pruebas <caso>
```

En Copilot: agente **Verificador** y `/pruebas <caso>`.

Mientras trabaja, fíjese en:
- la matriz: ¿qué criterios de su `spec.md` no tenían prueba?
- los datos: ¿usó `datos_sinteticos`?
- si una prueba nueva falla, la marca con `@pytest.mark.xfail(strict=True, reason="Posible defecto: …")` y **no toca `src/`**.

Al final:

```bash
python -m pytest -q                  # N passed, M xfailed
python -m pytest -q --cov=src/<paquete>/dominio --cov-report=term-missing
```

## 4. Ver el hook en acción · 5 min

Pídale a `claude` (sesión normal, no el Verificador) algo que rompa la regla de capas, por ejemplo:

```
Agrega en src/<paquete>/dominio/ una función que muestre el resultado con streamlit (import streamlit as st).
```

Debe aparecer el mensaje **Hook del equipo: el cambio rompe una verificación** y el agente corregirlo solo, moviendo el código a `app/`. Si no aparece, revise el paso 1 (`/hooks`) y que abrió `claude` con el entorno activo.

## 5. Commit, push y pull request · 5 min

```bash
git add -A
git commit -m "Pruebas de los criterios de <caso> y matriz (RF-..)"
git push -u origin pruebas/<caso>-verificacion
```

En GitHub: **Compare & pull request** con la plantilla. En la descripción, el resumen de `pruebas.md` (criterios cubiertos, posibles defectos, cobertura).

## En casa

1. Para cada posible defecto: `git switch -c correccion/<caso>-<defecto>` y `claude --agent depurador`: `Corrige el posible defecto de <prueba> marcado en docs/sdlc/<caso>/pruebas.md y quita la marca xfail.` (En Copilot, el botón **Depurar los posibles defectos** del Verificador.)
2. Fíjese en que el hook corre solo después de cada edición del Depurador.
3. Revise con `/revisar <caso>`, abra el pull request y fusione sin bloqueantes.
4. Envíe por el canal el enlace (o captura) de su PR de pruebas y la cobertura del dominio.
