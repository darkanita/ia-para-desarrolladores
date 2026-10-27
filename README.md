# IA para Desarrolladores — Laboratorios

Material práctico del curso **IA para Desarrolladores**: 20 horas, 10 sesiones de 2 horas, 2 por semana.

Herramientas del curso: **GitHub Copilot** (Copilot Chat en VS Code y Copilot CLI) y **Claude Code** (extensión de VS Code y Claude Code CLI). Todos los datos de los ejercicios son sintéticos y los casos de uso son del sector financiero.

El curso termina con un **cerebro del equipo**: los estándares, plantillas y buenas prácticas del equipo escritos una sola vez (instrucciones, reglas, skills, agentes y hooks) para que Copilot y Claude Code los apliquen igual.

## Cómo está organizada cada sesión

| Carpeta | Para qué |
|---|---|
| `demo/` | Lo que la docente muestra en vivo |
| `laboratorio/` | El ejercicio parecido que cada participante resuelve en clase; tiene pruebas o una plantilla de entrega |
| `autonomo/` | Trabajo para antes de la siguiente sesión |
| `reto-del-curso/` | El reto en equipos que avanza de la sesión 2 a la 10 |

Las presentaciones se publican en `slides/` después de cada sesión.

## Preparación del entorno (una sola vez)

Siga la guía [`preparacion/README.md`](preparacion/README.md) y, al terminar, verifique su máquina:

```bash
python preparacion/verificar_entorno.py
```

## Cronograma

Cada sesión usa los dos asistentes en sus dos formas: **Copilot Chat** y **Claude Code** en VS Code, **Copilot CLI** y **Claude Code CLI** en la terminal.

| Semana | Sesión | Módulo | Tema | Pieza del cerebro del equipo | Hito del reto |
|---|---|---|---|---|---|
| 1 | S1 | M1 Entender | Cómo "lee" un LLM tu código; cómo trabaja un agente (lee, planea, usa herramientas, verifica) | — | — |
| 1 | S2 | M2 Explorar | Copilot Chat, Copilot CLI y Claude Code: modos, modelos, permisos y costos; la misma tarea con los tres | — | **Hito 1:** reto definido |
| 2 | S3 | M3 Hacer | Prompt y context engineering | Instrucciones del equipo (`AGENTS.md`, `CLAUDE.md`) | — |
| 2 | S4 | M3 Hacer | De historia de usuario a caso de uso con la plantilla del equipo; modo plan | Reglas por tipo de código y primera skill | **Hito 2:** primer componente |
| 3 | S5 | M4 Transformar | Depuración y code review con agentes | Agente revisor | — |
| 3 | S6 | M4 Transformar | Pruebas automatizadas y refactorización | Hooks: lint y pruebas en cada cambio | **Hito 3:** suite de pruebas |
| 4 | S7 | M4 Transformar | Seguridad: OWASP, secretos, permisos del agente, revisión cruzada | Agente de seguridad y bloqueos | — |
| 4 | S8 | M4 Transformar | Buenas prácticas y gobierno del cerebro: versionar, revisar, compartir | Empaquetado para otros repositorios | **Hito 4:** refactorizado y asegurado |
| 5 | S9 | M5 Apropiar | Cada equipo construye y aplica la parte de su tipo de proyecto | Partes por tipo de proyecto (APIs, ETL, automatizaciones) | — |
| 5 | S10 | M5 Apropiar | Demos y recomendaciones de adopción | Cerebro del equipo integrado | **Entregable final** |

Certificación: asistencia mínima del 80 % (máximo 2 inasistencias de 10 sesiones).

## Material de referencia

El curso se apoya en los módulos de GitHub Copilot de **Microsoft Learn** y en **Claude Code 101** de **Anthropic Academy**. El mapa de lecturas por sesión está en [`REFERENCIAS.md`](REFERENCIAS.md).
