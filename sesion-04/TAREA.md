# Sesión 4 · Del plan al primer componente

**Se hace en clase** (30 minutos) y en casa se termina. **Quién:** cada persona, en su `mi-reto`.
**Entrega (hito):** el `plan.md` aprobado y el **primer componente con sus pruebas en verde**, antes de la sesión 5.

## 1. Poner al día y comprobar su repositorio · 5 min (se empieza en el bloque de las 0:05)

Desde **la carpeta del curso** (con el material nuevo), con el entorno activo:

```bash
bash proyectos/poner_al_dia.sh ../mi-reto
```

El script guarda primero en commits lo que tenga suelto en `docs/sdlc/`, luego trae **todo** lo que le falta al agente (reglas, skills, servidor MCP, agentes): no copie carpetas a mano. Actualiza lo que usted no tocó, deja `.nuevo` al lado de lo que usted cambió (el script le muestra cómo compararlos) y no toca `docs/sdlc/`. Al final corre el verificador: todo debe quedar en `OK`. Si no alcanzó a actualizar en la sesión 3, este mismo comando lo pone al día.

Después cierre y vuelva a abrir `claude` en `mi-reto` y escriba `/mcp` (debe aparecer `banco`); en VS Code recargue la ventana y dele **Start** a `banco` en `.vscode/mcp.json`.

Compruebe en `claude`, abierto en `mi-reto` (en Copilot Chat, las mismas preguntas):

| Pregunta | Lo que debe pasar |
|---|---|
| `/mcp` | Aparece `banco`, conectado |
| `Según el glosario del banco, ¿qué es usura y dónde está su valor?` | Llama a la herramienta `glosario` y responde con `productos.credito_consumo.tasa_maxima_ea` |
| `¿Qué reglas de .claude/rules se aplican a tests/test_cuota.py y a src/<paquete>/dominio/cuota.py?` | `pruebas` para el primero y `capas` para el segundo, según sus `paths` |

**Qué es una regla:** una instrucción para el agente que solo aplica a ciertos archivos. No se llama: se carga sola cuando el agente va a leer o escribir un archivo que coincide con sus `paths` (en la terminal verá `Loaded .claude/rules/<regla>.md`). Las del equipo son `artefactos`, `pruebas`, `capas`, `api` y `etl`; la sexta es la suya (ver "En casa").

**Qué trajo el script** (lo vimos en clase): las reglas del equipo en `.claude/rules/` (y su copia para Copilot en `.github/instructions/`), que el agente carga solo al tocar ciertos archivos; el servidor del banco (`herramientas/mcp_banco/`, configurado en `.mcp.json` y `.vscode/mcp.json`), que responde con lo que dice `banco.yaml`; y, de hoy, los agentes, `/plan-tecnico` y la regla de capas.

### Revisar y aprobar su `spec.md` · 3 min

Su especificación se escribió sin las reglas ni el servidor del banco. Antes de aprobarla, pídale al agente (en `claude` o en Copilot Chat):

```
Revisa docs/sdlc/<caso>/spec.md con las herramientas del banco (glosario, consultar_politica, catalogo_servicios). Lista las reglas que no citan su clave o política y los términos que no usan el glosario. No cambies el archivo.
```

Si la lista tiene cosas: `Aplica las correcciones de la lista. No cambies el Estado.` (o regenere con `/spec <caso>`). Revise el resultado con `git diff`. Luego apruébela usted, a mano: `Estado: aprobado` y `Aprobado por: <su nombre> (dueño del producto)`, y commit:

```bash
git add docs/sdlc
git commit -m "Especificación aprobada"
```

## 2. El plan con el agente Arquitecto · 12 min

| | Claude Code | Copilot Chat |
|---|---|---|
| Abrir el agente | En la terminal de `mi-reto`: `claude --agent arquitecto` | En el selector de agentes del chat, elija **Arquitecto** |
| Pedir el plan | `/plan-tecnico <caso>` | `/plan-tecnico <caso>` |

El Arquitecto lee la especificación, consulta al banco (`catalogo_servicios`, `consultar_politica`) y valida cada nombre con `validar_nombre` (le pedirá permiso: apruébelo). **Solo escribe** `docs/sdlc/<caso>/plan.md`; si intenta tocar otro archivo, no lo apruebe.

## 3. Revisar y aprobar el plan · 5 min

Revíselo con esta lista:

- [ ] Cada componente está en la capa correcta y dice qué requisitos (RF) y reglas (RN) cubre.
- [ ] Lo que viene de otro sistema entra por un puerto, con un adaptador en memoria para las pruebas.
- [ ] Cada criterio de aceptación de la especificación tiene su prueba.
- [ ] Los nombres están validados.
- [ ] Los pasos van en orden, prueba primero, y dice cuál es el primer componente.
- [ ] Solo usa dependencias aprobadas; no trae nada que la especificación dejó fuera.

Si pasa, edite a mano `Estado: aprobado` y `Aprobado por: <su nombre> (líder técnico)` y haga commit:

```bash
git add docs/sdlc
git commit -m "Plan técnico aprobado"
```

## 4. El primer paso con el agente Desarrollador · 5 min

| | Claude Code | Copilot Chat |
|---|---|---|
| Abrir el agente | Salga (`/exit`) y abra `claude --agent desarrollador` | Botón **Implementar el plan aprobado** al final de la respuesta del Arquitecto, o elija **Desarrollador** en el selector |
| Pedir | `Implementa el paso 1 del plan aprobado de <caso>.` | `Implementa el paso 1 del plan aprobado de <caso>.` |

Observe el orden: primero la prueba, la ve fallar, implementa y la ve pasar. Al final corre `python herramientas/verificar_capas.py`.

## En casa

1. Termine el **primer componente**: `Implementa los pasos 2 a <n> del plan aprobado de <caso>.` (el plan dice hasta qué paso llega). Mejor de a dos o tres pasos por conversación.
2. Revise cada paso antes de seguir: lea la prueba (¿verifica lo que dice el criterio?) y el código (¿está en la capa correcta?).
3. Compruebe:

   ```bash
   python -m pytest -q
   python herramientas/verificar_capas.py
   ```
4. Commit: `git add -A && git commit -m "Primer componente con pruebas en verde"`.
5. Envíe por el canal el `plan.md` y la salida de `pytest` y de `verificar_capas.py`.

**Pendiente de la sesión 3: su regla propia.** Piense en algo que su asistente hizo distinto a como lo hace su equipo, al menos dos veces. Copie una regla de `.claude/rules/` (por ejemplo `pruebas.md`), cámbiele `description`, `paths` y el contenido, y corra `python herramientas/sincronizar_skills.py` para generar la de Copilot. Commit: `git add .claude .github && git commit -m "Regla propia: <nombre>"`. Envíela por el canal con lo demás. La guía completa está en `sesion-03/TAREA.md`.

**Lectura:** Claude Code 101 (skills y subagentes) y, de GH-600, *Designing Agent Architecture and SDLC Integration*.
