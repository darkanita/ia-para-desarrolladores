# Requisitos para la parte práctica · IA para Desarrolladores

Desde la sesión 2, los ejercicios se hacen **en casa, en el repositorio del equipo**. Antes de empezar, cada persona valida estos puntos en su máquina. Si algo falla, envíe una captura por el canal del curso.

## 1. La base (guía de preparación)

- [ ] `python preparacion/verificar_entorno.py` termina en "Listo para el curso" (ver [`README.md`](README.md) de esta carpeta).
- [ ] VS Code abre la carpeta del curso y la terminal integrada usa el entorno virtual (`(.venv)` al inicio de la línea).

## 2. Su asistente de IA responde

Use **una** de las dos, según su licencia:

| Comprobación | Claude Code | GitHub Copilot Business |
|---|---|---|
| Inicia sesión | `claude` → `/status` muestra su cuenta | Ícono de Copilot activo en VS Code; `copilot` → `/login` |
| Responde en una carpeta | En `practica-transferencias`: "Explícame qué hace este proyecto" | Lo mismo en Copilot Chat (Ask) |
| Puede editar y ejecutar con permiso | Pídale "Ejecuta las pruebas": pide permiso antes de correr `pytest` | En **Agent**, lo mismo |
| Modelos disponibles | `/model` → anote la lista | Clic en el nombre del modelo → anote la lista |

Modelos recomendados para el curso: en Claude Code, `sonnet` u `opus` para el trabajo principal y `haiku` para tareas rápidas. En Copilot, Claude Sonnet 5 para el trabajo principal y Claude Haiku 4.5 para tareas rápidas.

## 3. El asistente lee las reglas y las skills del equipo

En el repositorio del equipo (creado con `python proyectos/crear_repositorio.py ../equipo-<nombre> --proyecto plantilla-equipo`):

- [ ] `python herramientas/verificar_equipo.py` termina en "Listo para trabajar con el agente".
- [ ] Pregúntele al asistente: *"¿Qué reglas del equipo tienes que seguir?"*. Debe mencionar el Banco Orquídea, `Decimal` y las tasas E.A. Si no, no está leyendo `AGENTS.md` (Copilot) o `CLAUDE.md` (Claude Code).
- [ ] Escriba `/` en el chat: debe aparecer **`intencion`**. En Copilot, use el agente **Agent**; si no aparece, verifique que exista `.github/skills/intencion/` y recargue VS Code.

## 4. Git y el repositorio compartido del equipo

- [ ] `git log --oneline` muestra el commit inicial del repositorio del equipo.
- [ ] El equipo tiene dónde compartir el repositorio: el sistema de repositorios que use la organización o, si no hay, una carpeta compartida. El curso no requiere acceso a GitHub.
- [ ] Saben hacer `git add`, `git commit` y traer los cambios de los compañeros.

## 5. Lo que se suma en las próximas sesiones

Instálelo con tiempo para no perder la sesión:

| Sesión | Qué se necesita | Cómo validarlo |
|---|---|---|
| S3 | Paquetes `pyyaml` y `mcp` (servidor de herramientas del banco, local) | `pip install pyyaml mcp`; el verificador del equipo los muestra en OK |
| S3 | Que su asistente pueda usar servidores MCP locales | Claude Code: `/mcp` abre sin error · Copilot: la política de MCP de la organización debe estar habilitada (ver sección 6) |
| S4 | `pip install copier` (plantilla del proyecto) | `copier --version` |
| S6 | Que el asistente pueda ejecutar hooks (comandos de Python) | Se valida en la sesión 6 |

## 6. Para el equipo de TI

| Qué | Para quién | Por qué |
|---|---|---|
| Política **MCP servers in Copilot** habilitada en la organización | Personas con Copilot Business | Desde la sesión 3 el agente usa un servidor MCP local con herramientas ficticias del banco (no sale a internet) |
| Política **Copilot CLI** habilitada | Personas con Copilot Business | Uso de Copilot en la terminal |
| Agentes personalizados, skills e instrucciones habilitados en Copilot | Personas con Copilot Business | El agente del equipo usa esas piezas |
| Claude Code sin restricciones administradas sobre skills, subagentes, hooks y servidores MCP locales del proyecto | Personas con Claude Code | Son las piezas del agente del equipo |
| Acceso a PyPI (`pypi.org`, `files.pythonhosted.org`) | Todos | Instalar `pyyaml`, `mcp` y `copier` |

Todo el trabajo usa **datos sintéticos** y un banco ficticio. Ninguna pieza del agente se conecta a sistemas del banco.

## 7. Si algo falla

Envíe por el canal del curso: su sistema operativo, la herramienta (Claude Code o Copilot), una captura del error y la salida de `verificar_equipo.py`.
