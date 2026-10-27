# Sesión 1 — Entender: cómo "lee" un LLM tu código

**Módulo 1 · Fundamentos de IA · 2 horas · Semana 1**

## Objetivo

Comprender los fundamentos técnicos de la IA generativa y los LLMs aplicados al desarrollo de software, y reconocer sus capacidades, límites y riesgos en un entorno financiero.

## Agenda

| Tiempo | Bloque | Material |
|---|---|---|
| 0:00 – 0:10 | Apertura, acuerdos del curso, reto continuo y reglas de datos | Presentación |
| 0:10 – 0:30 | Qué hay dentro de un LLM: siguiente token, tokens, transformer, atención, embeddings | Presentación + `demo/01` a `03` |
| 0:30 – 1:15 | Las herramientas del curso: qué son VS Code, Git, GitHub Copilot y Claude Code; los controles de Copilot Chat; cómo trabaja un agente; Copilot y Claude Code, cada uno en VS Code y en la terminal; qué modelos hay y cuándo usar cada uno; recorrido en vivo por las cuatro formas de uso y qué modelos tiene cada una | Presentación + `proyectos/transferencias` |
| 1:15 – 1:20 | Demo: alucinación y datos sensibles, en Copilot Chat y Claude Code | Presentación |
| 1:20 – 1:45 | Manos a la obra: Copilot y Claude Code construyen un simulador de crédito a partir de un documento de requisitos | `proyectos/simulador-credito` |
| 1:45 – 1:52 | Capacidades, límites, riesgos y cinco reglas | Presentación |
| 1:52 – 2:00 | Cómo llegar listos a la sesión 2 y trabajo autónomo | `preparacion/`, `autonomo/` |

## Archivos

```
sesion-01/
├── demo/
│   ├── tokenizador.py            tiktoken con respaldo sin red
│   ├── 01_tokens.py              tokens, contexto y costo
│   ├── 02_atencion.py            self-attention causal en NumPy
│   ├── 03_busqueda_semantica.py  embeddings y similitud coseno
│   └── 04_amortizacion.py        tabla de amortización de un crédito
├── laboratorio/                 guardián de prompts: práctica opcional
│   ├── ENUNCIADO.md
│   ├── guardian_prompt.py        plantilla con TODOs
│   └── tests/                    34 pruebas automáticas
└── autonomo/
    ├── INSTRUCCIONES.md          trabajo para antes de la sesión 2
    ├── validador_transacciones.py
    └── BITACORA.md
```

## Ejecutar

```bash
python sesion-01/demo/01_tokens.py
python sesion-01/demo/02_atencion.py
python sesion-01/demo/03_busqueda_semantica.py
pytest sesion-01/laboratorio/tests -q      # al inicio fallan las 34: es lo esperado
```
