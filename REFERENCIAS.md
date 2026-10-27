# Material de referencia por sesión

El curso usa como referencia dos rutas oficiales:

- **Microsoft Learn**, curso [GH-600T00: Developing in Agentic AI Systems](https://learn.microsoft.com/es-es/training/courses/gh-600t00) (disponible en español). Trata a GitHub Copilot como agente dentro del ciclo de desarrollo: arquitectura del agente, herramientas y MCP, multiagente, evaluación y gobierno. Conduce a la certificación [GitHub Certified: Agentic AI Developer](https://learn.microsoft.com/en-us/credentials/certifications/agentic-ai-developer/).
- **Anthropic Academy**, en especial [Claude Code 101](https://anthropic.skilljar.com/claude-code-101), que va de la instalación a la personalización avanzada (CLAUDE.md, subagentes, skills, MCP y hooks).

Se recomiendan como lectura de apoyo antes o después de cada sesión. No reemplazan los laboratorios del curso, que usan casos del sector financiero.

GH-600 es de nivel intermedio y usa GitHub como plano de control (agente en la nube, Actions, revisiones). Si su organización no les da acceso a GitHub, lean esas partes como concepto: lo mismo se practica en el curso con Copilot en VS Code y en la CLI.

| Sesión | Tema del curso | Microsoft Learn · GH-600 | Anthropic Academy · Claude Code 101 |
|---|---|---|---|
| S1 | Cómo funciona un LLM; cómo trabaja un agente; qué modelo usar | *Foundations of Agentic AI in GitHub* | *What is Claude Code?*, *How Claude Code works* · *AI Capabilities and Limitations* |
| S2 | Copilot Chat, Copilot CLI y Claude Code | *Foundations of Agentic AI in GitHub* (cierre) | *Installing Claude Code*, *Your first prompt*, *Daily workflows*, *Explore → plan → code → commit* |
| S3 | Prompt y context engineering; instrucciones del equipo | *Designing Agent Architecture and SDLC Integration* | *Context management*, *Customizing Claude Code*, *The CLAUDE.md file* |
| S4 | De historia de usuario a caso de uso con la plantilla | *Designing Agent Architecture and SDLC Integration* | *Skills* · *Introduction to Agent Skills* |
| S5 | Depuración y code review con agentes | *Multi-Agent Systems and Orchestration* | *Code review*, *Subagents* · *Introduction to Subagents* |
| S6 | Pruebas y refactorización | *Memory, State, and Evaluation* | *Hooks* |
| S7 | Seguridad | *Governance, guardrails, and operations* | *AI Capabilities and Limitations* · *Claude Code in Action* (buenas prácticas) |
| S8 | Gobierno y empaquetado del cerebro del equipo | *Tooling, MCP, and Agent Execution Environments* · *Governance, guardrails, and operations* | *MCP* · *Introduction to Model Context Protocol* |
| S9–S10 | Reto aplicado | Repaso para la certificación **GitHub Certified: Agentic AI Developer** | *Claude Code in Action* |

Los títulos en cursiva son módulos de cada curso; búsquelos por título dentro del curso en [Microsoft Learn](https://learn.microsoft.com/es-es/training/courses/gh-600t00) o en [Anthropic Academy](https://anthropic.skilljar.com/).

Para elegir modelo (S1), consulte las páginas oficiales, que cambian cada pocos meses:

- [Modelos disponibles en GitHub Copilot](https://docs.github.com/en/copilot/reference/ai-models/supported-models)
- [Configuración de modelos en Claude Code](https://code.claude.com/docs/en/model-config) (`/model`, `/effort`, alias como `opusplan`)
- [Cómo elegir un modelo Claude](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)

Las dos plataformas ofrecen insignias o certificados al completar los cursos. No son requisito del curso.
