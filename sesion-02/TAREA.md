# Tarea de la sesión 2 · Reto definido (Hito 1)

**Entrega:** antes de la sesión 3, en el repositorio del equipo. **Quién:** el equipo (4–5 personas).

Antes de empezar, cada persona revisa los [requisitos para la parte práctica](../preparacion/REQUISITOS_PRACTICA.md).

## 1. Crear el repositorio del equipo en GitHub (una persona del equipo)

Desde la carpeta del curso, con el entorno activo:

```bash
python proyectos/crear_repositorio.py ../equipo-<nombre> --proyecto plantilla-equipo
cd ../equipo-<nombre>
python herramientas/verificar_equipo.py
```

Cree un repositorio **privado y vacío** en la organización de GitHub que usa su equipo (sin README ni .gitignore) y súbalo:

```bash
git remote add origin <url del repositorio>
git push -u origin main
```

Agregue a sus compañeros como colaboradores. Cada uno lo clona (`git clone <url>`) y corre `python herramientas/verificar_equipo.py` en su copia. Desde la sesión 5, los cambios entran por pull request.

## 2. Elegir el reto
Lean [`RETOS_SUGERIDOS.md`](RETOS_SUGERIDOS.md) o propongan uno propio del trabajo diario, con datos sintéticos.

## 3. Escribir la intención con el agente
Abran el repositorio en VS Code y, en Claude Code o en Copilot Chat (agente **Agent**), escriban:

```text
/intencion <la idea de su reto en una o dos frases>
```

Respondan las preguntas del asistente. El resultado queda en `docs/sdlc/<caso>/intent.md`.

## 4. Revisar antes de entregar
- [ ] Están las 11 secciones; ninguna vacía (o dice "No aplica" y por qué).
- [ ] La métrica de éxito se puede medir.
- [ ] Los datos están clasificados con `banco.yaml` y son sintéticos.
- [ ] Las reglas del banco citan su clave de `banco.yaml` y no hay valores inventados.
- [ ] El `Estado` sigue en `borrador`: lo aprueba la docente en la sesión 3, como dueña del producto.
- [ ] `python herramientas/verificar_equipo.py` termina en "Listo".

## 5. Entregar
Hagan commit (`git add . && git commit -m "Intención del reto"`) y envíen por el canal del curso: nombre del equipo, integrantes, herramienta de cada uno (Claude Code o Copilot) y el `intent.md`.
