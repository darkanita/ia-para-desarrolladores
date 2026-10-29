# Requisitos para la parte práctica · IA para Desarrolladores

En la sesión 2 cada persona practica **en clase, en su propio repositorio local** (desde la sesión 5, en uno compartido en GitHub). **Valide estos puntos en su máquina antes de esa clase.** Si algo falla, envíe una captura por el canal del curso.

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

Haga una prueba con un repositorio de práctica (en clase creará el definitivo, `mi-reto`). Desde la carpeta del curso: `python proyectos/crear_repositorio.py ../prueba --proyecto plantilla-equipo`, abra `../prueba` en VS Code y compruebe:

- [ ] `python herramientas/verificar_equipo.py` termina en "Listo para trabajar con el agente".
- [ ] Pregúntele al asistente: *"¿Qué reglas del equipo tienes que seguir?"*. Debe mencionar el Banco Orquídea, `Decimal` y las tasas E.A. Si no, no está leyendo `AGENTS.md` (Copilot) o `CLAUDE.md` (Claude Code).
- [ ] Escriba `/` en el chat: debe aparecer **`intencion`**. En Copilot, use el agente **Agent**; si no aparece, verifique que exista `.github/skills/intencion/` y recargue VS Code.

## 4. Git

- [ ] `git config user.name` y `git config user.email` devuelven su nombre y correo. Sin esto, el commit de la práctica falla. Si están vacíos: `git config --global user.name "Su nombre"` y `git config --global user.email "su@correo"`.
- [ ] En la carpeta `../prueba`, `git log --oneline` muestra el commit inicial. Cuando todo funcione, puede borrar esa carpeta.
- [ ] Sabe hacer `git add` y `git commit`.
- [ ] Desde la sesión 5 el trabajo pasa a un repositorio compartido en GitHub, con ramas y pull requests: confirme que puede crear o recibir acceso a un repositorio privado en la organización.

## 5. Lo que se suma en las próximas sesiones

Instálelo con tiempo para no perder la sesión:

| Sesión | Qué se necesita | Cómo validarlo |
|---|---|---|
| S3 | Paquetes `pyyaml` y `mcp` (servidor de herramientas del banco, local) | `pip install pyyaml mcp`; el verificador del equipo los muestra en OK |
| S3 | Que su asistente pueda usar servidores MCP locales | Claude Code: `/mcp` abre sin error · Copilot: la política de MCP de la organización debe estar habilitada (ver sección 6) |
| S4 | `pip install copier` (plantilla del proyecto) | `copier --version` |
| S6 | Que el asistente pueda ejecutar hooks (comandos de Python) | Se valida en la sesión 6 |
| S6–S8 | GitHub Actions en el repositorio del equipo | Pestaña Actions habilitada; el workflow de pruebas corre en cada pull request |
| S7 | Análisis de dependencias y de código en GitHub (Dependabot, code scanning), si la organización los tiene | Pestaña Security del repositorio |

## 6. Para el equipo de TI

| Qué | Para quién | Por qué |
|---|---|---|
| Política **MCP servers in Copilot** habilitada en la organización | Personas con Copilot Business | Desde la sesión 3 el agente usa un servidor MCP local con herramientas ficticias del banco (no sale a internet) |
| Política **Copilot CLI** habilitada | Personas con Copilot Business | Uso de Copilot en la terminal |
| Agentes personalizados, skills e instrucciones habilitados en Copilot | Personas con Copilot Business | El agente del equipo usa esas piezas |
| Claude Code sin restricciones administradas sobre skills, subagentes, hooks y servidores MCP locales del proyecto | Personas con Claude Code | Son las piezas del agente del equipo |
| Acceso a PyPI (`pypi.org`, `files.pythonhosted.org`) | Todos | Instalar `pyyaml`, `mcp` y `copier` |
| Repositorios privados de los equipos en la organización de GitHub, con GitHub Actions | Todos | Pull requests, revisión y pruebas automáticas desde la sesión 5 |
| Revisión de código de Copilot en pull requests habilitada | Personas con Copilot Business | Revisión automática del PR en la sesión 5 |

Todo el trabajo usa **datos sintéticos** y un banco ficticio. Ninguna pieza del agente se conecta a sistemas del banco.

## 7. Si algo falla

Envíe por el canal del curso: su sistema operativo, la herramienta (Claude Code o Copilot), una captura del error y la salida de `verificar_equipo.py`.
