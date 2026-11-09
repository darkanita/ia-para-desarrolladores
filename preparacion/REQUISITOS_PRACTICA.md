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

## 4. Las herramientas del banco (MCP)

En la misma carpeta `../prueba`, con el entorno activo. Esta prueba confirma que su asistente tiene permiso para usar servidores MCP locales; si no lo tiene, lo habilita el administrador de su organización, no usted.

```bash
python herramientas/mcp_banco/servidor.py --probar
```

- [ ] El comando muestra las respuestas de `glosario`, `consultar_politica`, `catalogo_servicios` y `validar_nombre`. Si dice que falta PyYAML: `pip install pyyaml` y luego `python herramientas/configurar_mcp.py`.
- [ ] En `python herramientas/verificar_equipo.py`, la sección "3. Herramientas del banco" sale en OK.
- [ ] **Claude Code:** abra `claude` en `../prueba`, acepte el servidor `banco` cuando lo pregunte y escriba `/mcp`: debe mostrar `banco` conectado.
- [ ] **Copilot:** abra `.vscode/mcp.json`, pulse **Start** sobre `banco`; en el chat, con el agente **Agent**, el ícono de herramientas debe mostrar `banco`.
- [ ] Pregunte en su asistente *"¿Qué es la usura según el banco?"*. Apruebe el uso de la herramienta `glosario`. La respuesta debe mencionar `tasa_maxima_ea`: así sabe que salió de las herramientas del banco y no del modelo.

Si Copilot no arranca el servidor o no muestra sus herramientas, lo más probable es que la política **MCP servers in Copilot** no esté habilitada para su cuenta (ver sección 7). Envíe una captura por el canal.

## 5. Git

- [ ] `git config user.name` y `git config user.email` devuelven su nombre y correo. Sin esto, el commit de la práctica falla. Si están vacíos: `git config --global user.name "Su nombre"` y `git config --global user.email "su@correo"`.
- [ ] En la carpeta `../prueba`, `git log --oneline` muestra el commit inicial. Cuando todo funcione, puede borrar esa carpeta.
- [ ] Sabe hacer `git add` y `git commit`.
- [ ] Desde la sesión 5 el trabajo pasa a un repositorio compartido en GitHub, con ramas y pull requests: confirme que puede crear o recibir acceso a un repositorio privado en la organización.

## 6. Lo que se suma en las próximas sesiones

Instálelo con tiempo para no perder la sesión:

| Sesión | Qué se necesita | Cómo validarlo |
|---|---|---|
| S3 | Paquete `pyyaml` (el servidor MCP del banco lo usa; corre local, sin internet) | `pip install pyyaml`; en `mi-reto`, `python herramientas/verificar_equipo.py` muestra la sección 3 en OK |
| S3 | Que su asistente pueda usar servidores MCP locales | Claude Code: `/mcp` abre sin error · Copilot: la política de MCP de la organización debe estar habilitada (ver sección 7) |
| S4 | Nada adicional: la estructura del proyecto se crea con `herramientas/crear_estructura.py` | En `mi-reto`, `python herramientas/verificar_equipo.py` en OK |
| S5 | Cuenta personal de GitHub y acceso a github.com desde el computador de la clase | Sección 9 de esta guía |
| S6 | Que el asistente pueda ejecutar hooks (comandos de Python) | Se valida en la sesión 6 |
| S6–S8 | GitHub Actions en su repositorio de GitHub | Pestaña Actions habilitada; el workflow de pruebas corre en cada pull request |
| S7 | Análisis de dependencias y de código en GitHub (Dependabot, code scanning), si la organización los tiene | Pestaña Security del repositorio |

## 7. Para el equipo de TI

| Qué | Para quién | Por qué |
|---|---|---|
| Política **MCP servers in Copilot** habilitada en la organización | Personas con Copilot Business | Desde la sesión 3 el agente usa un servidor MCP local con herramientas ficticias del banco (no sale a internet) |
| Política **Copilot CLI** habilitada | Personas con Copilot Business | Uso de Copilot en la terminal |
| Agentes personalizados, skills e instrucciones habilitados en Copilot | Personas con Copilot Business | El agente del equipo usa esas piezas |
| Claude Code sin restricciones administradas sobre skills, subagentes, hooks y servidores MCP locales del proyecto | Personas con Claude Code | Son las piezas del agente del equipo |
| Acceso a PyPI (`pypi.org`, `files.pythonhosted.org`) | Todos | Instalar `pyyaml`, `mcp` y `copier` |
| Acceso a `github.com` (web y `git push` por HTTPS) desde los equipos de la clase | Todos | Desde la sesión 5 cada persona sube su `mi-reto` (datos sintéticos) a un repositorio privado de su cuenta personal |
| Revisión de código de Copilot en pull requests (opcional) | Personas con Copilot Business | Solo funciona si su licencia de Copilot cubre su cuenta personal; el curso usa el agente Revisor, que no la necesita |

Todo el trabajo usa **datos sintéticos** y un banco ficticio. Ninguna pieza del agente se conecta a sistemas del banco.

## 8. Si algo falla

Envíe por el canal del curso: su sistema operativo, la herramienta (Claude Code o Copilot), una captura del error y la salida de `verificar_equipo.py`.

## 9. Para la sesión 5: GitHub

Desde la sesión 5 su `mi-reto` vive también en GitHub, en un repositorio **privado** de su **cuenta personal**. Solo tiene datos sintéticos y nada del banco.

1. **Cuenta.** Si no tiene, créela en https://github.com/signup (gratis).
2. **Acceso.** Desde el computador de la clase abra https://github.com e inicie sesión. Si la red no deja entrar, avise por el canal antes de la clase.
3. **Prueba de `git push`** (2 minutos, con un repositorio de prueba que luego puede borrar):

```bash
cd ~/Downloads
mkdir prueba-github && cd prueba-github
git init -b main && echo "prueba" > README.md && git add . && git commit -m "Prueba"
# En github.com: New repository → prueba-github, Private, sin README → Create repository
git remote add origin https://github.com/<usuario>/prueba-github.git
git push -u origin main
```

La primera vez se abre el navegador para iniciar sesión (Git Credential Manager, viene con Git para Windows). Si el `push` termina sin error y el archivo aparece en GitHub, está listo. Luego puede borrar el repositorio de prueba en *Settings → Danger Zone*.

> `.mcp.json` y `.vscode/mcp.json` guardan la ruta de su Python (con su usuario de Windows). Por eso el repositorio es privado.

