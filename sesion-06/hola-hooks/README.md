# Hola mundo de hooks

Un ejemplo mínimo para **ver cuándo corre cada hook y qué puede hacer**, sin código del banco de por medio. Un solo script, `hooks/hola.py`, atiende los cinco eventos más usados y anota cada uno en `hola-hooks.log`.

| Evento | Cuándo corre | Qué hace en este ejemplo |
|---|---|---|
| `SessionStart` | Al abrir `claude` | Le pasa un dato a Claude: «el saludo oficial es ¡Hola, hooks!» |
| `UserPromptSubmit` | Cuando usted envía un prompt | Si el prompt dice «contraseña», lo **bloquea** |
| `PreToolUse` | Antes de que Claude use una herramienta | Si va a leer `secreto.txt`, lo **bloquea** |
| `PostToolUse` | Después de usarla | Solo lo anota (el hook del equipo aquí corre capas y pruebas) |
| `Stop` | Cuando Claude termina de responder | Solo lo anota |

Los cinco están registrados en `.claude/settings.json`.

## 1. Abrir dos terminales · 1 min

**Terminal A**, para ver el registro en vivo:

```bash
cd sesion-06/hola-hooks
touch hola-hooks.log
tail -f hola-hooks.log
```

**Terminal B**, para hablar con Claude:

```bash
cd sesion-06/hola-hooks
claude
```

Si `claude` pregunta si confía en esta carpeta, diga que sí: así carga los hooks de `.claude/settings.json`. En la terminal A ya debe salir `SessionStart  se abrió la sesión`.

## 2. Verlos uno por uno · 8 min

Escriba en `claude` y mire la terminal A después de cada prompt:

| Escriba en claude | En hola-hooks.log aparece | Lo que se aprende |
|---|---|---|
| `/hooks` | (nada) | Claude Code muestra los cinco hooks cargados |
| `¿Cuál es el saludo oficial de hoy?` | `UserPromptSubmit` y `Stop` | Claude responde «¡Hola, hooks!»: lo supo por el hook `SessionStart` |
| `Lee el archivo saludo.txt` | `UserPromptSubmit`, `PreToolUse … Read`, `PostToolUse … Read`, `Stop` | El orden del ciclo: antes y después de cada herramienta |
| `Lee el archivo secreto.txt` | `PreToolUse … secreto.txt` y **no** hay `PostToolUse` | Código 2 en `PreToolUse`: la lectura nunca ocurrió y Claude recibió el motivo |
| `Mi contraseña es 1234, guárdala` | `UserPromptSubmit` y nada más | Código 2 en `UserPromptSubmit`: el prompt no llegó a Claude |

## 3. Probarlo a mano, sin Claude · 2 min

Un hook es solo un programa que lee un JSON y devuelve un código. Se puede probar enviándole el JSON con `echo`:

```bash
echo '{"hook_event_name":"PreToolUse","tool_name":"Read","tool_input":{"file_path":"saludo.txt"}}' | python hooks/hola.py; echo "código $?"
# código 0: sigue

echo '{"hook_event_name":"PreToolUse","tool_name":"Read","tool_input":{"file_path":"secreto.txt"}}' | python hooks/hola.py; echo "código $?"
# Hook PreToolUse: BLOQUEADO. secreto.txt no se lee...
# código 2: bloquea
```

## 4. Cambiarlo usted · opcional

- En `hooks/hola.py`, cambie el saludo de `SessionStart`, cierre y vuelva a abrir `claude`, y pregunte otra vez por el saludo.
- Haga que `PreToolUse` también bloquee el comando `rm` (pista: `herramienta == "Bash"` y `"rm " in archivo`).

**Para recordar:** los hooks se leen al abrir `claude`. Si cambia `.claude/settings.json`, cierre y vuelva a abrir.
