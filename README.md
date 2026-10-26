# IA para Desarrolladores — Laboratorios

Material práctico del curso **IA para Desarrolladores**: 20 horas, 10 sesiones de 2 horas, 2 por semana.

Herramientas del curso: **VS Code + GitHub Copilot** (principal) y **Claude** en el sandbox de la organización. Todos los datos de los ejercicios son sintéticos.

## Cómo está organizada cada sesión

| Carpeta | Para qué |
|---|---|
| `demo/` | Lo que la docente muestra en vivo |
| `laboratorio/` | El ejercicio parecido que cada participante resuelve en clase; tiene pruebas o una plantilla de entrega |
| `autonomo/` | Trabajo para antes de la siguiente sesión |
| `reto-del-curso/` | El reto en equipos que avanza de la sesión 2 a la 10 |

Las presentaciones se publican en `slides/` después de cada sesión.

## Preparación del entorno (una sola vez)

Requisitos: Python 3.10 o superior, VS Code, extensiones **Python** y **GitHub Copilot / Copilot Chat**.

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
```

Comprobación rápida:

```bash
python sesion-01/demo/01_tokens.py
pytest sesion-01/laboratorio/tests -q      # al inicio las pruebas fallan: es lo esperado
```

> **Red corporativa:** `tiktoken` descarga su vocabulario la primera vez desde Internet.
> Si la red lo bloquea, los ejercicios siguen funcionando con un conteo aproximado y lo indican en pantalla.

## Cronograma

| Semana | Sesión | Módulo | Tema | Hito del reto | Carpeta |
|---|---|---|---|---|---|
| 1 | S1 | M1 Entender | Cómo "lee" un LLM tu código: tokens, atención, embeddings y uso seguro | — | `sesion-01/` |
| 1 | S2 | M2 Explorar | Modelos, asistentes y APIs; Copilot frente a Claude; criterios de selección | **Hito 1:** reto definido | `sesion-02/` |
| 2 | S3 | M3 Hacer | Prompt engineering y context engineering | — | próximamente |
| 2 | S4 | M3 Hacer | Generar, documentar y refactorizar; salidas estructuradas | **Hito 2:** primer componente | próximamente |
| 3 | S5 | M4 Transformar | Flujos con asistentes en el IDE; depuración y revisión | — | próximamente |
| 3 | S6 | M4 Transformar | Refactorización y pruebas automatizadas | **Hito 3:** suite de pruebas | próximamente |
| 4 | S7 | M4 Transformar | Vulnerabilidades y revisión de seguridad con IA | — | próximamente |
| 4 | S8 | M4 Transformar | Optimización de prompts y buenas prácticas | **Hito 4:** refactorizado y asegurado | próximamente |
| 5 | S9 | M5 Apropiar | Consolidación y revisión cruzada | — | próximamente |
| 5 | S10 | M5 Apropiar | Demos de los equipos y cierre | **Entregable final** | próximamente |

Certificación: asistencia mínima del 80 % (máximo 2 inasistencias de 10 sesiones).
