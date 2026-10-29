# Sesión 2 · La intención de mi reto

**Se hace en clase** (40 minutos) y en casa solo se termina. **Quién:** cada persona, en su máquina. Por ahora no hace falta GitHub: el repositorio es local.
**Entrega:** el `intent.md` aprobado, antes de la sesión 3.

**Llegue a clase con:** el repositorio del curso descargado, el entorno de Python activo y Claude Code o Copilot con sesión iniciada. Detalle en los [requisitos para la parte práctica](../preparacion/REQUISITOS_PRACTICA.md).

## 1. Crear su repositorio local desde la plantilla · 10 min

Abra una terminal en **la carpeta del curso**: donde descomprimió el `.zip` (por ejemplo `C:\cursos\ia-para-desarrolladores`) y donde creó el entorno virtual, según la [guía de preparación](../preparacion/README.md). Active el entorno: debe ver `(.venv)` al inicio de la línea.

- PowerShell: `.venv\Scripts\Activate.ps1`
- Git Bash: `source .venv/Scripts/activate`

Luego (los comandos funcionan igual en las dos terminales):

```bash
python proyectos/crear_repositorio.py ../mi-reto --proyecto plantilla-equipo
cd ../mi-reto
python herramientas/verificar_equipo.py
```

`../mi-reto` queda **al lado** de la carpeta del curso (por ejemplo `C:\cursos\mi-reto`), no dentro: es su repositorio, con su propio historial de git y su primer commit ya hecho.

El verificador debe terminar en "Listo para trabajar con el agente". El aviso "Casos con intent.md: ninguno todavía" es normal. Si dice que falta algo, avise.

## 2. Elegir el reto
Lea [`RETOS_SUGERIDOS.md`](RETOS_SUGERIDOS.md): cada reto trae la idea para pegar después de `/intencion` y la tabla de cómo crece su reto durante el curso. También puede proponer uno de su trabajo diario, con datos sintéticos.

## 3. Escribir la intención con el agente · 20 min
Abra **la carpeta `mi-reto`** en VS Code (si abre otra, la skill no aparece) y prepare su herramienta:

| | Claude Code (CLI o panel) | Copilot Chat |
|---|---|---|
| Abrir | En la terminal de `mi-reto`: `claude` | Conversación nueva con `+` |
| Modo | Manual: con `Shift+Tab`, sin *plan mode* ni *auto mode* | Agente **Agent**, modo **Interactive**, **Manual permissions** |
| Comprobar | Escriba `/inten`: debe aparecer `/intencion` | Escriba `/`: debe aparecer `intencion` |

Luego escriba:

```text
/intencion <la idea de su reto en una o dos frases>
```

Responda sus preguntas (máximo 5). Si no sabe algo, dígale: "No lo sabemos aún; déjalo como pregunta abierta". Cuando pida permiso para crear el archivo, lea la ruta y apruebe (en Copilot, además, **Keep**). El resultado queda en `docs/sdlc/<caso>/intent.md`.

## 4. Revisar en parejas · 5 min
Lea el `intent.md` de un compañero con esta lista:

- [ ] Están las 11 secciones; ninguna vacía (o dice "No aplica" y por qué).
- [ ] El problema está en lenguaje de negocio, sin soluciones técnicas.
- [ ] La métrica de éxito se puede medir.
- [ ] Los datos están clasificados con `banco.yaml` y son sintéticos.
- [ ] Las reglas del banco citan su clave de `banco.yaml` y no hay valores inventados.
- [ ] Los supuestos y las preguntas abiertas están escritos.

## 5. Aprobar y registrar · 5 min
Usted es el dueño de su reto. Si la revisión pasó, **edite a mano** la tabla del inicio (el agente no se aprueba a sí mismo):

```text
| Estado | aprobado |
| Aprobado por | <su nombre> |
```

Y deje el registro en git:

```bash
git add docs/sdlc
git commit -m "Intención del reto aprobada"
git log --oneline
```

Si quedaron preguntas abiertas importantes, déjelo en `borrador`, ciérrelas en casa con el agente y apruebe después.

## En casa
1. Termine lo que quedó pendiente: preguntas abiertas, aprobación y commit.
2. Envíe por el canal del curso su nombre, la herramienta que usó (Claude Code o Copilot) y el archivo `intent.md`.
3. Instale lo de la sesión 3: `pip install pyyaml mcp`.

> Más adelante (sesión 5) el trabajo pasa a un repositorio compartido en GitHub, con ramas y pull requests.
