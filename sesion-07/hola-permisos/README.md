# Hola mundo de permisos

Un ejemplo mínimo para **ver qué hace un permiso** en Claude Code y en Copilot, sin código del banco de por medio. Es el hermano del hola mundo de hooks de la sesión 6: allá un **programa** decidía; aquí decide una **lista** en un archivo de configuración.

## La idea en una tabla

| Respuesta | Claude Code (`.claude/settings.json`) | Copilot en VS Code (`.vscode/settings.json`) |
|---|---|---|
| Corre sin preguntar | `permissions.allow` | `autoApprove: true` |
| Pregunta antes | `permissions.ask` | `autoApprove: false` |
| **Nunca corre** | `permissions.deny` | **No existe**: si usted aprueba, corre. Para negar hace falta un hook |
| Sin regla | Lo que haga por defecto (los comandos de terminal preguntan) | Lo que haga por defecto (los comandos riesgosos preguntan) |

En Claude Code, si dos reglas chocan gana la más estricta: **deny, luego ask, luego allow**.

## Los dos archivos

```json
// .claude/settings.json  (Claude Code)
"permissions": {
  "allow": ["Bash(echo:*)", "Bash(git:*)"],      // echo y cualquier git: sin preguntar
  "ask":   ["Bash(git push:*)"],                 // ...menos git push: pregunta
  "deny":  ["Read(./secreto.txt)", "Bash(rm:*)"] // nunca
}
```

```json
// .vscode/settings.json  (Copilot)
"chat.tools.terminal.autoApprove": { "echo": true, "git status": true, "git push": false, "rm": false },
"chat.tools.edits.autoApprove":    { "**/saludo.txt": false }
```

Ninguno de los dos tiene código: son listas. Por eso son fáciles de leer y de auditar, y por eso solo saben de **nombres** de archivos y comandos, no de su contenido.

## 1. Claude Code · 5 min

```bash
cd sesion-07/hola-permisos
claude
```

Si `claude` pregunta si confía en esta carpeta, diga que sí. Si no, Claude Code **ignora los `allow`** de esta carpeta (los `deny` sí los aplica): una carpeta que usted no ha aceptado no puede darse permisos a sí misma. Escriba `/permissions` para ver las tres listas. Luego, uno por uno:

| Escriba en claude | Qué pasa | Por qué |
|---|---|---|
| `Ejecuta echo hola` | Corre **sin preguntar** | `allow`: `Bash(echo:*)` |
| `Ejecuta git --version` | Corre **sin preguntar** | `allow`: `Bash(git:*)` |
| `Ejecuta git push` | **Pregunta**. Responda que no | `ask` gana a `allow`: es más estricta |
| `Ejecuta date` | **Pregunta** | No hay regla: lo que hace por defecto |
| `Lee secreto.txt` | **Denegado**, sin preguntar | `deny`: `Read(./secreto.txt)` |
| `Borra saludo.txt con rm` | **Denegado**, sin preguntar | `deny`: `Bash(rm:*)` |
| `Lee saludo.txt` | Lo lee | Leer dentro del proyecto no pregunta por defecto |

Para cambiar una regla: edite `.claude/settings.json`, cierre `claude` y ábralo otra vez.

## 2. Copilot en VS Code · 5 min

1. Abra **esta carpeta** en VS Code (`File → Open Folder…` → `hola-permisos`). Los ajustes de `.vscode/settings.json` solo valen para la carpeta abierta.
2. Abra el chat en modo **Agent**, con el nivel de aprobación por defecto (no en «aprobar todo» ni `/yolo`).
3. Uno por uno:

| Escriba en el chat de Copilot | Qué pasa | Por qué |
|---|---|---|
| `Ejecuta echo hola en la terminal` | Corre **sin preguntar** | `autoApprove`: `"echo": true` |
| `Ejecuta git push en la terminal` | **Pregunta**. Elija no ejecutar | `"git push": false` |
| `Borra saludo.txt con rm en la terminal` | **Pregunta**. Elija no ejecutar | `"rm": false`. Pregunta, pero **si usted aprueba, lo borra** |
| `Agrega la línea «hola, permisos» a saludo.txt` | **Pregunta** antes de guardar el cambio | `chat.tools.edits.autoApprove`: `"**/saludo.txt": false` |
| `Lee secreto.txt y dime qué dice` | **Lo lee** | No hay forma de negar una lectura con estos ajustes |

La última fila es la lección: **en Copilot estos ajustes preguntan, pero no prohíben**. Para que algo sea imposible hace falta el hook, igual que el del hola mundo de la sesión 6 que bloqueaba `secreto.txt`.

## 3. Lo que se llevan · 2 min

| | Permiso (lista) | Hook (programa) |
|---|---|---|
| Qué mira | El nombre de la herramienta, el archivo o el comando | Todo: el contenido, la rama de git, `banco.yaml` |
| Claude Code | allow / ask / deny | Bloquea con código 2 |
| Copilot | Sin preguntar / preguntar | Bloquea con código 2 |
| Ejemplo | `deny Read(./.env)` | «No escriba un token en el código», «no haga commit en main» |

Por eso en `demo-clase` están los dos: `permissions.deny` en `.claude/settings.json` y el hook `proteger.py`, que también corre en Copilot desde `.github/hooks/proteger.json`.

> Copilot cambia rápido. Si en su versión de VS Code alguna fila se comporta distinto (por ejemplo, `echo` pregunta igual), mire en la configuración el nivel de aprobación del chat y la documentación de VS Code sobre aprobaciones.
