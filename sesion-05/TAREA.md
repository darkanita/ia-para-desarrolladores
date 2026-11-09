# Sesión 5 · Práctica y tarea: su primer pull request revisado

Al terminar, su `mi-reto` está en GitHub, el trabajo nuevo vive en una rama y entra a `main` por un pull request revisado por el agente Revisor.

Todo se hace en **Git Bash**, con el entorno del curso activo (`source .venv/Scripts/activate`).

## 1. Poner al día su repositorio · se hace en el bloque de las 0:10

Desde la carpeta del curso, con el material nuevo:

```bash
bash proyectos/poner_al_dia.sh ../mi-reto
```

Trae la **versión 3**: los agentes `depurador` y `revisor`, la skill `/revisar`, las políticas de revisión y depuración y la plantilla nueva del pull request. Después cierre y vuelva a abrir `claude` en `mi-reto` (en VS Code: *Reload Window*).

## 2. ¿Funciona lo de la sesión 4? · 3 min

```bash
cd ../mi-reto
python -m pytest -q
python herramientas/verificar_capas.py
```

Anote el resultado: lo usa en el paso 4.

## 3. Su repositorio en GitHub · 8 min

1. En https://github.com: **New repository** → nombre `mi-reto`, **Private**, sin README, sin `.gitignore` y sin licencia (su repositorio ya los tiene) → **Create repository**.
2. En Git Bash, dentro de `mi-reto` (cambie `<usuario>` por el suyo):

```bash
git status                      # debe estar limpio; si no, haga commit antes
git remote add origin https://github.com/<usuario>/mi-reto.git
git push -u origin main
```

La primera vez se abre el navegador para iniciar sesión en GitHub (Git Credential Manager). Recargue la página del repositorio: debe ver sus archivos y `docs/sdlc/`.

## 4. Una rama y el agente que corresponde · 12 min

Nadie trabaja en `main`. Cree la rama según lo que salió en el paso 2 (formato de `convenciones.ramas`):

**Si algo falló (pruebas en rojo o capas con violaciones)** → rama de corrección y agente **depurador**:

```bash
git switch -c correccion/<caso>-<que-falla>
claude --agent depurador
```

```
Al correr python -m pytest -q falla <prueba o error>. Encuentra la causa raíz y corrígela, prueba primero.
```

**Si todo está en verde** → rama de funcionalidad y el siguiente paso de su plan con el agente **desarrollador**:

```bash
git switch -c funcionalidad/<caso>-paso-<n>
claude --agent desarrollador
```

```
Implementa el paso <n> del plan aprobado de <caso>.
```

En Copilot: elija **Depurador** o **Desarrollador** en el selector de agentes del chat.

Revise lo que hizo (`git diff`) y haga commit con un mensaje que diga qué y por qué (`convenciones.commits`):

```bash
git add -A
git commit -m "Corrige <qué> (RN-xx)"        # o "Agrega <qué> (RF-xx)"
```

## 5. La revisión · 7 min

```bash
claude --agent revisor
```

```
/revisar <caso>
```

En Copilot: agente **Revisor** y `/revisar <caso>` (o el botón **Revisar los cambios** al final de la respuesta del Desarrollador o del Depurador).

El Revisor deja `docs/sdlc/<caso>/revision.md` con hallazgos **bloqueantes**, **importantes** y **sugerencias**. Léalo: ¿está de acuerdo con cada uno? Guárdelo en la rama:

```bash
git add docs/sdlc
git commit -m "Revisión de <qué> (borrador)"
```

## 6. Su primer pull request · 3 min

```bash
git push -u origin <nombre-de-su-rama>
```

En GitHub aparece **Compare & pull request**. La descripción ya trae la plantilla del equipo: complétela, pegue como comentario la sección 7 de `revision.md` y cree el pull request. **No lo fusione todavía** si tiene hallazgos bloqueantes.

## En casa

1. Atienda los hallazgos bloqueantes e importantes (o escriba en el pull request por qué no). En Claude Code: `claude --agent desarrollador` y `Atiende los hallazgos H-01 y H-02 de docs/sdlc/<caso>/revision.md`; en Copilot, el botón **Atender los hallazgos** del Revisor.
2. Haga commit y `git push`: el pull request se actualiza solo.
3. Vuelva a revisar con `/revisar <caso>` (el Revisor agrega una ronda nueva).
4. Sin bloqueantes: cambie `Estado` de `revision.md` a `aprobado` con su nombre (dueño del código), commit, push y **Merge pull request** en GitHub. Luego, en su computador: `git switch main && git pull`.
5. Envíe por el canal el enlace de su pull request fusionado (o una captura si no quiere compartir el repositorio).

**Comandos de Git de hoy**

| Para | Comando |
|---|---|
| Ver en qué rama está | `git branch --show-current` |
| Crear una rama y pasarse a ella | `git switch -c <tipo>/<caso>-<descripcion>` |
| Volver a `main` y traer lo fusionado | `git switch main && git pull` |
| Subir la rama | `git push -u origin <rama>` (la primera vez), luego `git push` |
| Ver qué cambió frente a `main` | `git diff main...HEAD --stat` |
