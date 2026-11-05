# Proyectos de práctica

Proyectos pequeños, con datos sintéticos, para practicar con los asistentes sobre código que se parece al de un banco. Se reutilizan en varias sesiones.

| Proyecto | Qué es |
|---|---|
| `transferencias/` | Servicio de transferencias entre cuentas: casos de uso, puertos y adaptadores, GMF, límite diario, CLI y pruebas. |
| `simulador-credito/` | Solo requisitos y reglas del equipo (`REQUISITOS.md`, `AGENTS.md`): punto de partida para que un asistente construya un simulador de crédito con Streamlit. |
| `plantilla-equipo/` | El repositorio de cada equipo con el agente del equipo: `banco.yaml`, reglas, skills y el servidor MCP del banco. Se crea con `crear_repositorio.py --proyecto plantilla-equipo` y se pone al día con `actualizar_repositorio.py`. |

Para trabajar sobre un repositorio git con historial (recomendado), cree una copia:

```bash
python proyectos/crear_repositorio.py ../practica-transferencias
python proyectos/crear_repositorio.py ../app-simulador --proyecto simulador-credito
```

Trabaje siempre en la copia: así puede dejar que los asistentes cambien archivos sin tocar el material del curso.

Cuando la plantilla crece (cada sesión agrega piezas al agente), actualice su repositorio sin perder su trabajo:

```bash
bash proyectos/poner_al_dia.sh ../mi-reto
```

Trae todo lo que falta (no copie carpetas a mano), primero guarda en commits lo que tenga suelto en `docs/sdlc/` y al final corre el verificador. Los archivos que usted modificó no se tocan: la versión nueva queda al lado como `.nuevo`. Su carpeta `docs/sdlc/` nunca se toca. Por debajo usa `python proyectos/actualizar_repositorio.py ../mi-reto`, que también puede correr solo.
