# Tarea de la sesión 2 · Mi primer intent.md

**Entrega:** antes de la sesión 3. **Quién:** cada persona, en su máquina. Por ahora no hace falta GitHub: el repositorio es local.

Antes de empezar, revise los [requisitos para la parte práctica](../preparacion/REQUISITOS_PRACTICA.md).

## 1. Crear su repositorio local desde la plantilla

Desde la carpeta del curso, con el entorno activo (los comandos funcionan igual en PowerShell y en Git Bash):

```bash
python proyectos/crear_repositorio.py ../mi-reto --proyecto plantilla-equipo
cd ../mi-reto
python herramientas/verificar_equipo.py
```

El verificador debe terminar en "Listo para trabajar con el agente". El aviso "Casos con intent.md: ninguno todavía" es normal.

## 2. Elegir el reto
Lea [`RETOS_SUGERIDOS.md`](RETOS_SUGERIDOS.md) o proponga uno de su trabajo diario, con datos sintéticos.

## 3. Escribir la intención con el agente
Abra `mi-reto` en VS Code y, en Claude Code o en Copilot Chat (agente **Agent**), escriba:

```text
/intencion <la idea de su reto en una o dos frases>
```

Responda las preguntas del asistente. El resultado queda en `docs/sdlc/<caso>/intent.md`.

## 4. Revisar antes de entregar
- [ ] Están las 11 secciones; ninguna vacía (o dice "No aplica" y por qué).
- [ ] La métrica de éxito se puede medir.
- [ ] Los datos están clasificados con `banco.yaml` y son sintéticos.
- [ ] Las reglas del banco citan su clave de `banco.yaml` y no hay valores inventados.
- [ ] El `Estado` sigue en `borrador`: lo aprueba la docente en la sesión 3, como dueña del producto.

## 5. Guardar y entregar
Guarde su trabajo en git:

```bash
git add .
git commit -m "Intención del reto"
```

Envíe por el canal del curso su nombre, la herramienta que usó (Claude Code o Copilot) y el archivo `intent.md`.

> Más adelante (sesión 5) el trabajo pasa a un repositorio compartido en GitHub, con ramas y pull requests.
