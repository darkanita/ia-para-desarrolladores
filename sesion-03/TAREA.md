# Sesión 3 · La especificación de mi reto

**Se hace en clase** (30 minutos) y en casa se termina. **Quién:** cada persona, en su `mi-reto`.
**Entrega:** el `spec.md` aprobado y una regla propia, antes de la sesión 4.

## 1. Actualizar su repositorio al agente v1 · 5 min

Desde **la carpeta del curso** (ya con el material nuevo), con el entorno activo:

```bash
python proyectos/actualizar_repositorio.py ../mi-reto
```

El script agrega las piezas nuevas (reglas, skill `/spec`, servidor MCP), actualiza los archivos que usted no tocó y hace un commit. **No toca su `docs/sdlc/`.** Si usted había modificado un archivo de la plantilla (por ejemplo `AGENTS.md`), no lo pisa: deja la versión nueva al lado como `AGENTS.md.nuevo` para que la compare.

Luego:

```bash
cd ../mi-reto
python herramientas/verificar_equipo.py
```

La sección **3. Herramientas del banco** debe salir en OK. Si el servidor no responde, revise que el entorno esté activo y ejecute `pip install pyyaml`.

## 2. Conectar las herramientas del banco · 5 min

Abra `mi-reto` en VS Code.

| | Claude Code | Copilot Chat |
|---|---|---|
| Arrancar | En la terminal: `claude`. La primera vez pregunta si confía en el servidor `banco` de `.mcp.json`: acepte. | Abra `.vscode/mcp.json` y pulse **Start** sobre `banco` (o acéptelo cuando VS Code lo pida). |
| Comprobar | `/mcp` muestra `banco` conectado con 3 herramientas. | En el chat (agente **Agent**), el ícono de herramientas lista `banco` con 3 herramientas. |
| Probar | `¿Qué es la usura según el banco?` | `¿Qué es la usura según el banco?` |

El asistente debe usar la herramienta `glosario` (le pedirá permiso: apruébelo) y responder con la definición del banco, no con una general.

## 3. Escribir la especificación · 15 min

Revise que su `docs/sdlc/<caso>/intent.md` diga `Estado: aprobado`. Si no, apruébelo primero (usted es el dueño de su reto). Luego:

```text
/spec <caso>
```

Donde `<caso>` es el nombre de la carpeta de su reto en `docs/sdlc/`. Responda sus preguntas (máximo 3) y apruebe el uso de las herramientas del banco cuando lo pida. El resultado queda en `docs/sdlc/<caso>/spec.md`, en `borrador`.

## 4. Compartir · 5 min
Una o dos personas comparten pantalla y lo revisamos juntos con la lista de abajo.

## En casa

### Terminar y aprobar el spec.md
Revíselo con esta lista. Si algo falta, pídaselo a su asistente en la misma conversación.

- [ ] Cada requisito (`RF-01`...) tiene criterios *Dado / Cuando / Entonces* con valores concretos y sintéticos.
- [ ] Cada regla de negocio (`RN-01`...) cita su clave de `banco.yaml` o su política. No hay valores inventados.
- [ ] Cada dato tiene clasificación y origen (un servicio del catálogo o la entrada del usuario).
- [ ] Dice qué servicios del catálogo usa, o por qué no usa ninguno.
- [ ] La trazabilidad cubre las métricas de la intención.
- [ ] Lo que la intención dejó fuera sigue fuera.
- [ ] Supuestos y preguntas abiertas escritos. No hay código.

Si pasa la lista, edite a mano `Estado: aprobado` y `Aprobado por: <su nombre>`, y haga commit:

```bash
git add docs/sdlc
git commit -m "Especificación del reto aprobada"
```

### Una regla propia del equipo
Piense en algo que su asistente hizo mal o distinto a como lo hace su equipo, al menos dos veces. Conviértalo en una regla:

1. Cree `.claude/rules/<nombre>.md` con esta forma (vea `.claude/rules/pruebas.md` como ejemplo):

   ```markdown
   ---
   description: <para qué es la regla>
   paths:
     - "<archivos a los que aplica, por ejemplo src/**/*.py>"
   ---

   # <Título>

   - <regla 1>
   - <regla 2>
   ```
2. Llévela a Copilot: `python herramientas/sincronizar_skills.py`
3. Commit: `git add .claude .github && git commit -m "Regla propia: <nombre>"`

### Entregar
Envíe por el canal del curso su `spec.md` y su regla.

### Leer
Claude Code 101 (contexto y `CLAUDE.md`) y, de GH-600, *Designing Agent Architecture and SDLC Integration*.
