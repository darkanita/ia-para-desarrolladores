# Preparación del equipo · IA para Desarrolladores

Antes de la **sesión 2**, cada participante debe tener instaladas y con sesión iniciada tres herramientas de IA (GitHub Copilot Chat en VS Code, GitHub Copilot CLI y Claude Code) y las herramientas base del curso. La instalación toma entre 45 y 60 minutos. Al terminar, corra el script de verificación (sección 5) y envíe una captura del resultado por el canal del curso.

Si en su equipo no tiene permisos para instalar software, pida apoyo a la mesa de ayuda con esta guía: la sección 7 está escrita para el equipo de TI.

## 1. Qué debe tener su máquina

| Herramienta | Versión mínima | Para qué se usa en el curso | Cómo verificar |
| --- | --- | --- | --- |
| Sistema operativo | Windows 10 (1809) u 11 de 64 bits · macOS 13 · Ubuntu 20.04 | Base para todas las herramientas | — |
| Memoria RAM | 8 GB recomendados (4 GB mínimo) | VS Code y los agentes abiertos a la vez | — |
| PowerShell (solo Windows) | 7.x | Copilot CLI requiere PowerShell 6 o superior; el que trae Windows es 5.1 | `pwsh --version` |
| Git | 2.30 | Control de versiones; en Windows también da Git Bash, que usa Claude Code | `git --version` |
| Python | 3.10 (recomendado 3.12) | Demos y laboratorios | `python --version` |
| Node.js | 22 LTS | Instalar Copilot CLI con npm y track frontend | `node --version` |
| Visual Studio Code | Versión actual | Editor del curso | `code --version` |
| GitHub Copilot Chat (integrado en VS Code reciente; en versiones anteriores, extensión) | Versión actual | Copilot en el editor: chat, edición y modo agente | Panel Chat e ícono de Copilot en la barra inferior de VS Code |
| Extensión Python (Microsoft) | Versión actual | Ejecutar y probar Python en VS Code | Panel de Extensiones |
| GitHub Copilot CLI | Versión actual | Copilot en la terminal | `copilot version` |
| Claude Code | 2.x | Claude en la terminal | `claude --version` |
| Licencias | Copilot asignada a su cuenta de GitHub · acceso a Claude Code | Usar los asistentes | Sección 4 |

Si ya usa Claude Code o Copilot Chat en su trabajo diario, solo debe completar lo que le falte.

## 2. Instalación en Windows

Abra **PowerShell** (no hace falta abrirlo como administrador) y siga el orden. Después de cada instalación, cierre y vuelva a abrir la terminal para que reconozca el nuevo comando. Si `winget` no está disponible o está bloqueado, use el instalador de la página oficial de cada herramienta.

1. **PowerShell 7:** `winget install Microsoft.PowerShell`. Desde aquí en adelante use la terminal *PowerShell 7* (`pwsh`), no *Windows PowerShell*.
2. **Git for Windows:** `winget install Git.Git`. Incluye Git Bash, que Claude Code usa para ejecutar comandos.
3. **Python 3.12:** `winget install Python.Python.3.12`. Si usa el instalador de python.org, marque *Add python.exe to PATH*.
4. **Node.js 22 LTS:** `winget install OpenJS.NodeJS.LTS`.
5. **Visual Studio Code:** `winget install Microsoft.VisualStudioCode`. Si usa el instalador, elija *User Installer* (no requiere administrador) y marque *Agregar a PATH*.
6. **Copilot Chat y extensión Python:** abra VS Code. Si ya ve el panel **Chat** y el ícono de Copilot en la barra inferior, Copilot Chat está listo: en versiones recientes viene integrado y no aparece como extensión. Si no lo ve, instale **GitHub Copilot Chat** desde el panel de Extensiones. Instale también **Python** (Microsoft). Desde la terminal:
   - `code --install-extension GitHub.copilot-chat`
   - `code --install-extension ms-python.python`
7. **GitHub Copilot CLI:** `winget install GitHub.Copilot`. Alternativa con Node.js: `npm install -g @github/copilot`.
8. **Claude Code:** `irm https://claude.ai/install.ps1 | iex`. Alternativa: `winget install Anthropic.ClaudeCode` (esta opción no se actualiza sola; actualice con `winget upgrade Anthropic.ClaudeCode`).

Si Claude Code ya está instalado en su equipo, no lo reinstale: verifique con `claude --version` y actualice con `claude update`.

## 3. Instalación en macOS y Linux

En macOS se asume [Homebrew](https://brew.sh). En Linux use el gestor de paquetes de su distribución para Git, Python y Node.js.

1. **Git:** macOS `xcode-select --install` · Ubuntu `sudo apt install git`.
2. **Python 3.12:** macOS `brew install python@3.12` · Ubuntu `sudo apt install python3 python3-venv python3-pip`.
3. **Node.js 22 LTS:** macOS `brew install node@22` · Linux: instalador de nodejs.org o `nvm`.
4. **Visual Studio Code:** macOS `brew install --cask visual-studio-code` · Linux: paquete .deb o .rpm de code.visualstudio.com. En macOS, abra VS Code y ejecute *Shell Command: Install 'code' command in PATH* desde la paleta de comandos.
5. **Extensiones:** `code --install-extension GitHub.copilot-chat` y `code --install-extension ms-python.python`.
6. **GitHub Copilot CLI:** `brew install --cask copilot-cli` · o `curl -fsSL https://gh.io/copilot-install | bash` · o `npm install -g @github/copilot`.
7. **Claude Code:** `curl -fsSL https://claude.ai/install.sh | bash` · o `brew install --cask claude-code`.

## 4. Iniciar sesión y probar los tres asistentes

Cada asistente se prueba con una pregunta corta. Si responde, está listo. Use la cuenta de GitHub que tiene la licencia de Copilot asignada por su organización.

| Asistente | Iniciar sesión | Prueba |
| --- | --- | --- |
| Copilot Chat (VS Code) | En VS Code, clic en el ícono de Copilot → *Sign in* con su cuenta de GitHub | Abra el chat (`Ctrl+Alt+I`; en macOS `Cmd+Ctrl+I`) y escriba: *¿qué modelos tengo disponibles?* |
| Copilot CLI | En la terminal, `copilot`, luego `/login` y siga las instrucciones del navegador | Pregunte: *explica qué hay en esta carpeta* |
| Claude Code | En la terminal, `claude` y siga las instrucciones de su organización para iniciar sesión | Escriba `/status` para ver la cuenta y el modelo; luego pregunte: *explica qué hay en esta carpeta* |

La primera vez que abra Copilot CLI o Claude Code en una carpeta, le preguntarán si confía en ella: responda que sí solo en la carpeta del curso.

Si Copilot CLI responde que la política no está habilitada, su licencia viene de la organización y un administrador debe activarla (sección 7). Si Claude Code no puede conectarse, ejecute `claude doctor` y envíe el resultado.

## 5. Preparar el material del curso y verificar

El material se entrega como un archivo `.zip` por el canal del curso. Descomprímalo en una carpeta de trabajo sin espacios en la ruta, por ejemplo `C:\cursos\ia-para-desarrolladores`.

1. Abra esa carpeta en VS Code (*Archivo → Abrir carpeta*) y abra una terminal integrada (``Ctrl+` ``).
2. Cree y active un entorno virtual:
   - Windows: `python -m venv .venv` y luego `.venv\Scripts\Activate.ps1`
   - macOS/Linux: `python3 -m venv .venv` y luego `source .venv/bin/activate`
3. Instale los paquetes del curso: `pip install -r requirements.txt`
4. Corra la verificación con su track (`backend`, `frontend` o `datos`):
   - `python preparacion/verificar_entorno.py --track backend`

El script no modifica nada en su equipo: consulta las versiones instaladas y prueba la conexión a los servicios del curso. Marca cada punto como **OK**, **FALTA** u **AVISO** (opcional) y explica cómo resolverlo. Cuando termine con *Listo para el curso*, envíe una captura por el canal. Si algo sigue en **FALTA**, envíe la captura igual para resolverlo antes de la sesión.

En Windows, si PowerShell no deja activar el entorno virtual, ejecute una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` o use la terminal *Command Prompt* con `.venv\Scripts\activate.bat`.

## 6. Requisitos adicionales por track

Desde la sesión 3 los laboratorios se hacen en el stack de cada equipo. Instale lo de su track; si trabaja en varios, elija el que usará en el reto del curso.

| Track | Qué instalar | Cómo verificar |
| --- | --- | --- |
| Backend (Java) | JDK 17 o 21 (por ejemplo Eclipse Temurin: `winget install EclipseAdoptium.Temurin.21.JDK`). Gradle no hace falta: los proyectos traen su propio `gradlew` | `java -version` |
| Frontend | Node.js 22 LTS (ya instalado en la sección 2) | `node --version` y `npm --version` |
| Datos / ETL | Python 3.12 (ya instalado en la sección 2) | `python --version` |

Pendiente de confirmar con el equipo: versión exacta de Java y Spring, framework de frontend y herramientas de ETL que usan hoy. Esta tabla se actualizará antes de la sesión 3.

## 7. Para el equipo de TI

Estas cinco condiciones dependen de la organización, no de cada participante. Conviene revisarlas antes de que el equipo empiece a instalar.

- [ ] **Licencias:** cada participante tiene una licencia de GitHub Copilot asignada a su cuenta de GitHub y acceso a Claude Code con el método de autenticación de la organización.
- [ ] **Política de Copilot CLI:** Copilot CLI viene incluido en todos los planes, pero cuando la licencia la asigna una organización, un administrador debe habilitar la política *Copilot CLI* en la configuración de Copilot de la organización.
- [ ] **Instalación de software:** permiso para instalar las herramientas de la sección 1, o que la mesa de ayuda las instale. Claude Code, VS Code (*User Installer*) y Python de python.org se instalan sin permisos de administrador.
- [ ] **Red y proxy:** los dominios de la tabla siguiente deben estar permitidos.
- [ ] **Inspección TLS:** si el proxy inspecciona tráfico HTTPS, su certificado raíz debe estar en el almacén de certificados del sistema. Claude Code (instalador nativo) lo lee de ahí; si no, se configura con la variable `NODE_EXTRA_CA_CERTS`. Si el proxy requiere autenticación, se configura `HTTPS_PROXY`.

| Para qué | Dominios |
| --- | --- |
| Copilot (autenticación y servicio) | `github.com`, `api.github.com`, `github.githubassets.com`, `avatars.githubusercontent.com`, `copilot-proxy.githubusercontent.com`, `origin-tracker.githubusercontent.com`, `*.business.githubcopilot.com` (plan Business) o el dominio de su plan |
| Extensiones de VS Code | `marketplace.visualstudio.com`, `*.gallerycdn.vsassets.io`, `update.code.visualstudio.com` |
| Claude Code | `api.anthropic.com`, `claude.ai`, `claude.com`, `platform.claude.com`, `downloads.claude.ai` (instalador y actualizaciones); `sso.claude.com` si la organización usa SSO |
| Paquetes del curso | `pypi.org`, `files.pythonhosted.org`, `registry.npmjs.org`, `openaipublic.blob.core.windows.net` (vocabulario de tiktoken, opcional) |
| Track backend | `repo.maven.apache.org`, `plugins.gradle.org`, `services.gradle.org` |

Si la organización usa Claude Code a través de Amazon Bedrock, Google Cloud o Microsoft Foundry, el tráfico del modelo va a ese proveedor en lugar de los dominios de Anthropic. Las listas completas están en las fuentes al final.

## 8. Problemas comunes

| Síntoma | Causa probable | Solución |
| --- | --- | --- |
| `claude`, `copilot` o `code` no se reconoce como comando | La terminal se abrió antes de instalar | Cierre y abra la terminal; si sigue, revise que la carpeta de instalación esté en el PATH |
| `'irm' is not recognized` | Está en Command Prompt, no en PowerShell | Abra PowerShell 7 o use el comando para CMD de la guía oficial de Claude Code |
| Copilot CLI no arranca en Windows | Se está usando Windows PowerShell 5.1 | Instale PowerShell 7 y abra la terminal *PowerShell 7* |
| Copilot CLI: política deshabilitada | La organización no ha activado Copilot CLI | Pedirlo al administrador (sección 7) |
| Error de certificado al instalar o al conectar | El proxy inspecciona tráfico HTTPS | Pedir a TI el certificado raíz (sección 7) |
| `pip install` falla por conexión | PyPI bloqueado o proxy sin configurar | Pedir a TI `pypi.org` y `files.pythonhosted.org`, o el espejo interno de paquetes |
| No se puede activar `.venv` en PowerShell | Política de ejecución de scripts | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| El script marca *Vocabulario de tiktoken* en AVISO | Dominio de descarga bloqueado | Es opcional: los ejercicios usan un conteo aproximado y lo indican en pantalla |

## Fuentes

- [Claude Code: requisitos e instalación](https://code.claude.com/docs/en/setup)
- [Claude Code: red, proxy y certificados](https://code.claude.com/docs/en/network-config)
- [Instalar GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli)
- [Dominios requeridos por Copilot](https://docs.github.com/en/enterprise-cloud@latest/copilot/reference/copilot-allowlist-reference)
- [Comparación de funciones de Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/comparing-cli-features)
- [Instrucciones personalizadas de Copilot en VS Code](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
- [VS Code: sistemas operativos soportados](https://code.visualstudio.com/docs/supporting/faq)
