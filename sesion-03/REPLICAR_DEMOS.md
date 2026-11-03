# Sesión 3 · Replicar las demos en su máquina

Las cuatro demos de la clase, paso a paso, para repetirlas cuando quiera. Comandos desde **la carpeta del curso**, con el entorno activo. Se muestran en Git Bash; en PowerShell funcionan igual, salvo donde se indica.

## 1. Qué ocupa la ventana de contexto

En su `mi-reto`, con Claude Code:

```bash
cd ../mi-reto
claude
```

```text
/context
```

Revise qué parte ocupan las instrucciones, `CLAUDE.md`, las herramientas MCP, las skills y los mensajes. Luego escriba `/clear` y `/context` otra vez.

En Copilot Chat, la barra del chat muestra el modelo, el esfuerzo y el tamaño de la ventana (por ejemplo `272K`).

## 2. Un error que se repite se vuelve regla

**Preparar** un repositorio con un módulo de pagos que no tiene pruebas:

```bash
python proyectos/crear_repositorio.py ../demo-reglas --proyecto demo-reglas
cd ../demo-reglas
claude
```

**Sin regla.** Pida:

```text
Escribe las pruebas de src/pagos/gmf.py en tests/test_gmf.py y ejecútalas con python -m pytest -q.
```

Abra `tests/test_gmf.py`. ¿Dice qué regla del banco verifica cada prueba? ¿Cómo prueba los bordes?

**Agregar la regla** (salga con `/exit`). La regla viene en `sesion-03/demo-reglas/` de la carpeta del curso:

```bash
mkdir -p .claude/rules .github/instructions
cp ../<carpeta del curso>/sesion-03/demo-reglas/pruebas.md .claude/rules/
cp ../<carpeta del curso>/sesion-03/demo-reglas/pruebas.instructions.md .github/instructions/
rm tests/test_gmf.py
```

En PowerShell: `New-Item -ItemType Directory -Force .claude\rules, .github\instructions`, luego `Copy-Item` en lugar de `cp` y `Remove-Item` en lugar de `rm`.

**Con regla.** Abra `claude` de nuevo y pida exactamente lo mismo. Compare: ahora cada prueba empieza con `"""Regla: productos.transferencias.…"""` y los bordes van agrupados con `pytest.mark.parametrize`.

En Copilot Chat (agente **Agent**) se repite igual, con el mismo prompt.

**Para empezar de nuevo:** `git clean -fdx && git checkout .` dentro de `demo-reglas`.

## 3. Las herramientas del banco por MCP

En su `mi-reto` (ya actualizado a la versión 1 con `actualizar_repositorio.py`):

```bash
python herramientas/mcp_banco/servidor.py --probar
```

Eso muestra las herramientas sin IA. Luego, con el asistente:

- **Claude Code:** `claude`, acepte el servidor `banco` y escriba `/mcp`.
- **Copilot:** abra `.vscode/mcp.json` y pulse **Start** sobre `banco`.

Preguntas para probar:

```text
¿Qué es la usura según el banco?
¿Qué dice la política de logs del banco?
¿Qué servicio del banco me da la tasa vigente del crédito de consumo y qué campos devuelve?
¿Hay algún servicio que me dé los ingresos del cliente? ¿Qué clasificación tienen esos datos?
```

Fíjese en qué herramienta usa para cada una (`glosario`, `consultar_politica` o `catalogo_servicios`).

## 4. De la intención a la especificación con `/spec`

La demo de clase usó el simulador de crédito. Para repetirla completa, en un repositorio aparte:

```bash
python proyectos/crear_repositorio.py ../demo-simulador --proyecto plantilla-equipo
cd ../demo-simulador
claude
```

```text
/intencion Los asesores comerciales calculan los créditos de consumo en hojas de cálculo distintas en cada oficina y los resultados no coinciden. Queremos un simulador único que diga cuánto paga el cliente cada mes, cuánto le cuesta en total y si le alcanza con sus ingresos.
```

Apruebe la intención: en `docs/sdlc/<caso>/intent.md`, cambie `Estado` a `aprobado` y ponga su nombre en `Aprobado por`. Luego:

```text
/spec <caso>
```

Respuestas que usamos en clase, si pregunta:
- Origen de la tasa: *La digita el asesor; usar svc-tasas queda como pregunta abierta para producto.*
- Tabla de amortización: *Sí, mes a mes, con la última cuota ajustada para que el saldo quede en cero.*
- Tipo de entregable: *Componente de dominio con una interfaz en Streamlit.*
- Cualquier otra: *No lo sabemos aún; déjalo como pregunta abierta.*

Revise el `spec.md` con la lista de aprobación de [`TAREA.md`](TAREA.md).
