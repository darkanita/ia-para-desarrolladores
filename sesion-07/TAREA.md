# Sesión 7 · Práctica: el simulador asegurado, todos a la vez

**En clase, en `demo-clase`, siguiendo a la docente.** Todos tienen el mismo simulador y el mismo commit de un "compañero" que agregó un adaptador a `svc-clientes`: pasa todas las pruebas, pero es inseguro. Hoy:

1. Su `demo-clase` recibe lo nuevo del agente del equipo para la sesión 7 y recibe el commit del compañero.
2. Comprueba que el agente ya **no puede** leer secretos, trabajar en `main`, borrar a la fuerza ni instalar lo que no está aprobado.
3. El agente **seguridad** revisa el commit y deja `seguridad.md`.
4. El agente **desarrollador** corrige y **usted** saca el secreto de git.
5. El **otro** asistente (u otro modelo) revisa otra vez: **revisión cruzada**.
6. Abre su pull request con la revisión de seguridad.

**En casa** repite lo mismo en `mi-reto`, con su caso (al final de esta guía).

Todo en **Git Bash**, con el entorno del curso activo (`source .venv/Scripts/activate`). Abra `claude` desde esa terminal.

---

## Paso 1 · Poner al día demo-clase · 5 min

Desde la carpeta del curso, con el material nuevo (`git pull` o el `.zip` nuevo):

```bash
python proyectos/nivelar_clase.py ../demo-clase --sesion 7
cd ../demo-clase
python -m pytest -q                       # 48 passed
python herramientas/verificar_equipo.py   # "Listo para trabajar con el agente."
git log --oneline -3                      # el último: "Prellenar los ingresos del cliente desde svc-clientes"
git push origin main
```

El script **no borra** su `demo-clase`: deja sus ramas y su trabajo de la sesión 6, pasa a `main`, trae lo que haya fusionado en GitHub, le agrega al agente del equipo lo de hoy (agente `seguridad`, skill `/seguridad`, hook `proteger.py`, permisos denegados y `buscar_secretos.py`) y agrega el commit del compañero.

> Si el script dice que hay **cambios sin guardar**: `git status`, y guárdelos (`git add -A && git commit -m "..."`) o apártelos sin commit (`git stash -u`; los recupera después con `git stash pop` en la misma rama) o descártelos (`git restore .`). Si dice que dejó archivos **`.nuevo`**: `mv ARCHIVO.nuevo ARCHIVO`, commit, y vuelva a correr el script.
> Si no tiene `demo-clase`: el mismo comando lo crea desde cero.

Cierre y vuelva a abrir `claude`; en VS Code, *Reload Window*. Compruebe en `claude`:

| Qué | Lo que debe pasar |
|---|---|
| `/hooks` | Un hook **PreToolUse** con `proteger.py` y uno **PostToolUse** con `verificar_cambio.py` |
| `/permissions` | Reglas de **deny** para `.env`, llaves, `git push --force`, `git reset --hard` y `rm -rf` |
| `/agents` | Seis agentes, entre ellos `seguridad` |

En Copilot: el agente **Seguridad** aparece en el selector; el hook se ve en **Output → GitHub Copilot Chat Hooks** (vista previa).

## Paso 1b · Hola mundo de permisos · 5 min (en la lámina 20, todos a la vez)

Antes de los bloqueos de verdad, un ejemplo mínimo para ver qué hace un **permiso**: una lista en un archivo de configuración que dice qué corre sin preguntar, qué pregunta y qué nunca corre. No es en `demo-clase`: es en la **carpeta del curso**.

```bash
cd sesion-07/hola-permisos      # desde la carpeta del curso (ia-para-desarrolladores)
claude                          # Claude Code: si pregunta si confía en la carpeta, diga que sí
code .                          # Copilot: abra ESTA carpeta en VS Code y use el chat en modo Agent
```

| Pídale (en claude o en el chat de Copilot) | Claude Code | Copilot |
|---|---|---|
| `Ejecuta echo hola en la terminal` | Corre sin preguntar (`allow`) | Corre sin preguntar (`"echo": true`) |
| `Ejecuta git push en la terminal` | Pregunta (`ask` gana a `allow`): responda que no | Pregunta (`"git push": false`): no lo ejecute |
| `Borra saludo.txt con rm` | Denegado, sin preguntar (`deny`) | Pregunta… **no lo apruebe**: si aprueba, lo borra |
| `Lee secreto.txt y dime qué dice` | Denegado, sin preguntar (`deny`) | Lo lee: no hay forma de negarlo |

En Claude Code, `/permissions` muestra las tres listas. Cuéntele al grupo qué le pasó con `secreto.txt`: **Claude Code puede negar; Copilot solo puede preguntar. Para negar en los dos hace falta un hook**, que es lo que viene. Al terminar, cierre esa sesión y vuelva a su `demo-clase`. El detalle está en [`hola-permisos/README.md`](hola-permisos/README.md).

## Paso 2 · Probar los bloqueos · 5 min

Abra una sesión normal (`claude`, sin agente), **en `main`**, y pídale una por una. Anote qué pasa:

| # | Pídale | Debe pasar |
|---|---|---|
| 1 | `Muéstrame el contenido del archivo .env` | Lo bloquea el permiso y el hook: archivo de secretos |
| 2 | `Crea NOTAS.md con la palabra prueba y haz commit directamente en main` | Crea el archivo, pero el commit lo bloquea el hook: `main` es una rama protegida |
| 3 | `Instala la librería requests` | Lo bloquea el hook: dependencia no aprobada |
| 4 | `Crea src/simulador_credito/config.py con API_KEY = "sk-sint-1234567890abcdefghij"` | Lo bloquea el hook: secreto en el contenido |
| 5 | Salga (`/exit`), abra `claude --agent revisor` y pídale `Agrega un comentario al inicio de src/simulador_credito/__init__.py` | Lo bloquea el hook del agente: el revisor solo escribe en `docs/` |

El agente lee el **motivo** y la indicación de qué hacer. Si se niega antes de intentarlo (porque `AGENTS.md` ya se lo dice), también vale: la instrucción aconsejó.

Al terminar, borre la nota: `rm NOTAS.md` (y `git status --short` debe quedar vacío).

> El hook frena al **agente**, no a usted: en su terminal usted sí puede hacer commit en `main`. Eso lo cubren los hooks de git y la CI de la sesión 8.

## Paso 3 · El commit del compañero: todo pasa, menos los secretos · 3 min

```bash
git show --stat HEAD                         # .env, adaptadores/clientes_http.py y su prueba
python -m pytest -q                          # en verde
python herramientas/verificar_capas.py       # OK
python herramientas/buscar_secretos.py --historia
```

`buscar_secretos.py` encuentra el `.env`, el token en el `.env` y el token en el código, **enmascarados**. Lo demás (el `eval`, el log, el TLS) no lo ve ninguna herramienta: para eso está el agente de seguridad.

## Paso 4 · El agente de seguridad, en una rama · 10 min

```bash
git switch -c correccion/simulador-credito-consumo-seguridad
claude --agent seguridad
```

```text
/seguridad simulador-credito-consumo
```

En Copilot: agente **Seguridad** y `/seguridad simulador-credito-consumo`.

Mire cómo trabaja: corre `buscar_secretos.py`, consulta al banco (`consultar_politica`, `catalogo_servicios`) y recorre la lista OWASP. **No abre el `.env`**: si lo intenta, el hook lo bloquea.

Lea `docs/sdlc/simulador-credito-consumo/seguridad.md`. Debería tener al menos estos cinco hallazgos sobre el adaptador:

| ID | Severidad | Qué |
|---|---|---|
| S-01 | bloqueante | El token versionado en `.env` y como valor por defecto en el código |
| S-02 | bloqueante | `eval` sobre la respuesta del servicio |
| S-03 | bloqueante | Nombre e ingresos del cliente en el log (datos restringidos) |
| S-04 | importante | TLS sin verificar |
| S-05 | importante | El id del cliente va a la URL sin validar |

Si le falta uno, pregúntele por esa categoría (por ejemplo: `¿Qué campos de svc-clientes son restringidos según catalogo_servicios? ¿Alguno va al log?`).

## Paso 5 · Corregir: el desarrollador y usted · 8 min

1. **Usted** saca el secreto de git (el hook no deja al agente tocar `.env`):

   ```bash
   /exit
   git rm --cached .env
   printf 'SVC_CLIENTES_URL=\nSVC_CLIENTES_TOKEN=\n' > .env.example
   ```

   El `.env` sigue en su disco, ignorado. En un proyecto real, además, pediría **rotar** el token: ya quedó en la historia de git.

2. **El desarrollador** corrige el código:

   ```bash
   claude --agent desarrollador
   ```

   ```text
   Corrige los hallazgos S-01 a S-05 de docs/sdlc/simulador-credito-consumo/seguridad.md en src/simulador_credito/adaptadores/clientes_http.py, prueba primero: lee el token solo de la variable de entorno, sin valor por defecto; json.loads en vez de eval; el log solo con el id del cliente; TLS verificado; y valida el id del cliente antes de armar la URL. No toques .env.
   ```

   En Copilot: el botón **Corregir los hallazgos de seguridad** del agente Seguridad.

3. Compruebe:

   ```bash
   /exit
   python -m pytest -q
   python herramientas/buscar_secretos.py       # OK
   git add -A
   git commit -m "Corrige la seguridad del adaptador de svc-clientes: sin secretos, sin eval y sin datos restringidos en el log"
   ```

## Paso 6 · Revisión cruzada · 5 min

Quien escribió el código no se revisa solo. Revise otra vez, en la misma rama, con **otro asistente u otro modelo**:

| Usted usó | Revise con |
|---|---|
| Claude Code | Copilot: agente **Seguridad** y `/seguridad simulador-credito-consumo rama` |
| Copilot | Claude Code: `claude --agent seguridad` y `/seguridad simulador-credito-consumo rama` |
| Solo tiene uno | El mismo, con otro modelo: `claude --agent seguridad --model <otro>` o el selector de modelo de Copilot |

El agente agrega una **ronda nueva** al final de `seguridad.md`. En la sección **6. Revisión cruzada** debe decir quién escribió y quién revisó. Guárdela:

```bash
git add docs/sdlc
git commit -m "Revisión de seguridad de la corrección, con revisión cruzada (borrador)"
```

## Paso 7 · Pull request · 5 min

```bash
git push -u origin correccion/simulador-credito-consumo-seguridad
```

En GitHub, **Compare & pull request**:

- **Título:** `Corrige la seguridad del adaptador de svc-clientes (politicas.seguridad)`.
- **Plantilla:** caso, rama, etapa (corrección); marque solo lo que sea verdad.
- **Comentario:** pegue la sección 7 de `seguridad.md`.

Sin bloqueantes en la última ronda: cambie `Estado` de `seguridad.md` a `aprobado` con su nombre, commit, `git push` y **Merge pull request**. Luego: `git switch main && git pull`.

---

## En casa · Lo mismo, en su reto (Hito 4 en camino)

> **Si no alcanzó en clase el hola mundo de permisos** (paso 1b), hágalo antes del reto con `sesion-07/hola-permisos/README.md`. Si tiene los dos asistentes, pruebe también el otro.

En `mi-reto`, con su caso. Tenga a mano dos datos:

| Dato | Dónde lo ve | Ejemplo |
|---|---|---|
| `<caso>` | La carpeta en `docs/sdlc/` | `validador-transferencias` |
| `<paquete>` | La carpeta dentro de `src/` | `transferencias`, `conciliacion`, `alertas`… |

1. **Poner al día:** `bash proyectos/poner_al_dia.sh ../mi-reto`, luego `cd ../mi-reto && git switch main && git pull` y `python herramientas/verificar_equipo.py`.
2. **Sembrar** el adaptador inseguro, haciendo usted de compañero (abajo).
3. **Pasos 4 a 7** de esta guía, cambiando `simulador-credito-consumo` por `<caso>` y `simulador_credito` por `<paquete>`. Antes del pull request, suba `main` (`git switch main && git push`).
4. Entrega: `seguridad.md` sin bloqueantes abiertos y con la ronda de revisión cruzada, `buscar_secretos.py` en OK, y en el PR qué secreto habría que rotar. Envíe por el canal el enlace de su pull request fusionado.
5. Opcional: `/seguridad <caso>` sobre todo su código (sin `rama`), para encontrar problemas reales de su reto.

### Sembrar el adaptador inseguro en `main` de mi-reto · 7 min

Usted hace de "compañero del equipo" que agregó una consulta a `svc-clientes` para prellenar datos del cliente. **Créelo a mano en VS Code**, no con el agente (el hook no lo dejaría escribir el token).

1. Esté en `main` y sin cambios pendientes:

   ```bash
   git switch main
   git status --short              # no debe mostrar nada
   ```

2. Cree el archivo `.env` en la raíz de `mi-reto` (el token es sintético, no sirve para nada real):

   ```text
   SVC_CLIENTES_URL=https://svc-clientes.interno.example/v1
   SVC_CLIENTES_TOKEN=tok_sint_5e4d3c2b1a0f9e8d
   ```

3. Cree `src/<paquete>/adaptadores/clientes_http.py` con este contenido:

   ```python
   """Adaptador de svc-clientes: trae el perfil declarado del cliente para prellenar datos."""
   import logging
   import os
   import ssl
   import urllib.request

   log = logging.getLogger(__name__)

   URL_BASE = os.environ.get("SVC_CLIENTES_URL", "https://svc-clientes.interno.example/v1")
   # Por si alguien no tiene el .env: el token de pruebas que nos dieron
   TOKEN_POR_DEFECTO = "tok_sint_5e4d3c2b1a0f9e8d"


   def parsear_respuesta(texto: str) -> dict:
       """Convierte la respuesta del servicio en un diccionario."""
       return eval(texto)


   def obtener_perfil(id_cliente: str) -> dict:
       """Consulta GET /v1/clientes/{id_cliente} y devuelve el perfil financiero declarado."""
       token = os.environ.get("SVC_CLIENTES_TOKEN", TOKEN_POR_DEFECTO)
       solicitud = urllib.request.Request(f"{URL_BASE}/clientes/{id_cliente}",
                                          headers={"Authorization": f"Bearer {token}"})
       contexto = ssl._create_unverified_context()  # el certificado interno da error en local
       with urllib.request.urlopen(solicitud, context=contexto, timeout=5) as respuesta:
           perfil = parsear_respuesta(respuesta.read().decode("utf-8"))
       log.info("Perfil de %s: ingresos %s, otras cuotas %s", perfil.get("nombre"),
                perfil.get("ingresos_mensuales"), perfil.get("otras_cuotas_mensuales"))
       return perfil
   ```

   Si su reto no tiene carpeta `adaptadores/`, créela con un `__init__.py` vacío.

4. Cree `tests/test_clientes_http.py` (cambie `<paquete>` por el suyo):

   ```python
   """Pruebas del adaptador de svc-clientes (sin red: solo el parseo de la respuesta)."""
   from <paquete>.adaptadores.clientes_http import parsear_respuesta


   def test_parsear_respuesta_de_svc_clientes():
       """Regla: catálogo svc-clientes · la respuesta trae ingresos y otras cuotas declarados."""
       texto = '{"id_cliente": "CLI-SIN-0001", "ingresos_mensuales": "4000000", "otras_cuotas_mensuales": "500000"}'
       perfil = parsear_respuesta(texto)
       assert perfil["ingresos_mensuales"] == "4000000"
   ```

5. Haga commit como si fuera otra persona. El `.env` está en `.gitignore`, así que el "compañero" lo **fuerza** con `-f`:

   ```bash
   git add -f .env
   git add src tests
   git -c user.name="Compañero del equipo" -c user.email=companero@equipo.example commit -m "Prellenar datos del cliente desde svc-clientes"
   ```

6. Compruebe que **todo pasa**, menos la búsqueda de secretos:

   ```bash
   python -m pytest -q                          # en verde
   python herramientas/verificar_capas.py       # OK
   python herramientas/buscar_secretos.py --historia
   ```

   `buscar_secretos.py` debe encontrar el `.env`, el token en el `.env` y el token en el código, **enmascarados**.


**Comandos de hoy**

| Para | Comando |
|---|---|
| Ver los hooks y los permisos | `/hooks` · `/permissions` (dentro de `claude`) |
| Buscar secretos | `python herramientas/buscar_secretos.py` (y `--historia`) |
| Dejar de versionar un archivo sin borrarlo | `git rm --cached <archivo>` |
| Revisar la seguridad | `claude --agent seguridad` y `/seguridad <caso>` (o `/seguridad <caso> rama`) |
| Otro modelo para la revisión cruzada | `claude --agent seguridad --model <otro>` |
