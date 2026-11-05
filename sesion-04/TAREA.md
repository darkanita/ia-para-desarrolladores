# Sesión 4 · Del plan al primer componente

**Se hace en clase** (30 minutos) y en casa se termina. **Quién:** cada persona, en su `mi-reto`.
**Entrega (hito):** el `plan.md` aprobado y el **primer componente con sus pruebas en verde**, antes de la sesión 5.

## 1. Actualizar su repositorio al agente v2 · 5 min

Desde **la carpeta del curso** (con el material nuevo), con el entorno activo:

```bash
bash proyectos/poner_al_dia.sh ../mi-reto
```

El script guarda primero en commits lo que tenga suelto en `docs/sdlc/`, luego trae **todo** lo que le falta al agente (reglas, skills, servidor MCP, agentes): no copie carpetas a mano. Actualiza lo que usted no tocó, deja `.nuevo` al lado de lo que usted cambió (el script le muestra cómo compararlos) y no toca `docs/sdlc/`. Al final corre el verificador: todo debe quedar en `OK`. Si no alcanzó a actualizar en la sesión 3, este mismo comando lo pone al día.

Después cierre y vuelva a abrir `claude` en `mi-reto` y escriba `/mcp` (debe aparecer `banco`); en VS Code recargue la ventana y dele **Start** a `banco` en `.vscode/mcp.json`.

Revise que su `docs/sdlc/<caso>/spec.md` diga `Estado: aprobado`. Si no, apruébelo primero (usted es el dueño de su reto).

## 2. El plan con el agente Arquitecto · 15 min

| | Claude Code | Copilot Chat |
|---|---|---|
| Abrir el agente | En la terminal de `mi-reto`: `claude --agent arquitecto` | En el selector de agentes del chat, elija **Arquitecto** |
| Pedir el plan | `/plan-tecnico <caso>` | `/plan-tecnico <caso>` |

El Arquitecto lee la especificación, consulta al banco (`catalogo_servicios`, `consultar_politica`) y valida cada nombre con `validar_nombre` (le pedirá permiso: apruébelo). **Solo escribe** `docs/sdlc/<caso>/plan.md`; si intenta tocar otro archivo, no lo apruebe.

## 3. Revisar y aprobar el plan · 5 min

Revíselo con esta lista:

- [ ] Cada componente está en la capa correcta y dice qué requisitos (RF) y reglas (RN) cubre.
- [ ] Lo que viene de otro sistema entra por un puerto, con un adaptador en memoria para las pruebas.
- [ ] Cada criterio de aceptación de la especificación tiene su prueba.
- [ ] Los nombres están validados.
- [ ] Los pasos van en orden, prueba primero, y dice cuál es el primer componente.
- [ ] Solo usa dependencias aprobadas; no trae nada que la especificación dejó fuera.

Si pasa, edite a mano `Estado: aprobado` y `Aprobado por: <su nombre> (líder técnico)` y haga commit:

```bash
git add docs/sdlc
git commit -m "Plan técnico aprobado"
```

## 4. El primer paso con el agente Desarrollador · 5 min

| | Claude Code | Copilot Chat |
|---|---|---|
| Abrir el agente | Salga (`/exit`) y abra `claude --agent desarrollador` | Botón **Implementar el plan aprobado** al final de la respuesta del Arquitecto, o elija **Desarrollador** en el selector |
| Pedir | `Implementa el paso 1 del plan aprobado de <caso>.` | `Implementa el paso 1 del plan aprobado de <caso>.` |

Observe el orden: primero la prueba, la ve fallar, implementa y la ve pasar. Al final corre `python herramientas/verificar_capas.py`.

## En casa

1. Termine el **primer componente**: `Implementa los pasos 2 a <n> del plan aprobado de <caso>.` (el plan dice hasta qué paso llega). Mejor de a dos o tres pasos por conversación.
2. Revise cada paso antes de seguir: lea la prueba (¿verifica lo que dice el criterio?) y el código (¿está en la capa correcta?).
3. Compruebe:

   ```bash
   python -m pytest -q
   python herramientas/verificar_capas.py
   ```
4. Commit: `git add -A && git commit -m "Primer componente con pruebas en verde"`.
5. Envíe por el canal el `plan.md` y la salida de `pytest` y de `verificar_capas.py`.

**Lectura:** Claude Code 101 (skills y subagentes) y, de GH-600, *Designing Agent Architecture and SDLC Integration*.
