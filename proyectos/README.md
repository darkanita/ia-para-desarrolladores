# Proyectos de práctica

Proyectos pequeños, con datos sintéticos, para practicar con los asistentes sobre código que se parece al de un banco. Se reutilizan en varias sesiones.

| Proyecto | Qué es |
|---|---|
| `transferencias/` | Servicio de transferencias entre cuentas: casos de uso, puertos y adaptadores, GMF, límite diario, CLI y pruebas. |
| `simulador-credito/` | Solo requisitos y reglas del equipo (`REQUISITOS.md`, `AGENTS.md`): punto de partida para que un asistente construya un simulador de crédito con Streamlit. |
| `plantilla-equipo/` | El repositorio de cada equipo: `banco.yaml`, `AGENTS.md`, `CLAUDE.md` y las skills del agente del equipo. Se crea con `crear_repositorio.py --proyecto plantilla-equipo`. |

Para trabajar sobre un repositorio git con historial (recomendado), cree una copia:

```bash
python proyectos/crear_repositorio.py ../practica-transferencias
python proyectos/crear_repositorio.py ../app-simulador --proyecto simulador-credito
```

Trabaje siempre en la copia: así puede dejar que los asistentes cambien archivos sin tocar el material del curso.
