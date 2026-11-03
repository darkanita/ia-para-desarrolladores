# Demo de la sesión 3: un error que se repite se vuelve regla

En clase se le pide al asistente las pruebas de un módulo de pagos dos veces: primero sin reglas de pruebas, luego con la regla del equipo. Se compara qué cambió.

- El proyecto de la demo está en `proyectos/demo-reglas/` (un módulo de GMF sin pruebas). Se crea una copia con historial con:

  ```bash
  python proyectos/crear_repositorio.py ../demo-reglas --proyecto demo-reglas
  ```
- Esta carpeta trae la regla que se agrega a mitad de la demo, en los dos formatos:
  - `pruebas.md` → va en `.claude/rules/` (Claude Code; el campo `paths` dice a qué archivos aplica).
  - `pruebas.instructions.md` → va en `.github/instructions/` (Copilot; el campo `applyTo` dice lo mismo).

Es la misma regla que trae la plantilla del equipo en `.claude/rules/pruebas.md`.

Para repetirla en su máquina, siga la sección 2 de [`../REPLICAR_DEMOS.md`](../REPLICAR_DEMOS.md).
