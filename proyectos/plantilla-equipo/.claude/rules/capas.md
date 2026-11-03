---
description: La regla de capas del código del equipo
paths:
  - "src/**/*.py"
---

# Regla de capas

El código vive en `src/<paquete>/` con cinco capas. Cada capa solo importa las que tiene permitidas:

| Capa | Qué va aquí | Puede importar |
|---|---|---|
| `dominio` | Reglas de negocio puras: entidades, cálculos, validaciones | Nada del proyecto. Ningún framework (`convenciones.paquetes_de_framework`) |
| `puertos` | Contratos hacia afuera (`typing.Protocol`) | `dominio` |
| `casos_uso` | Lo que el usuario quiere lograr; orquesta dominio y puertos | `dominio`, `puertos` |
| `adaptadores` | Implementaciones de los puertos: en memoria o servicios reales | `dominio`, `puertos`, `casos_uso` |
| `app` | La entrada: Streamlit, FastAPI o línea de comandos | Todas |

- Los valores de negocio (tasas, límites) llegan al dominio como parámetros o desde un puerto de configuración; no se leen archivos dentro del dominio.
- Un servicio del catálogo se usa a través de un puerto, nunca directo desde un caso de uso.
- Antes de terminar, ejecute `python herramientas/verificar_capas.py`: debe decir OK.
