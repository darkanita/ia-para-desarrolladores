# Pruebas · <nombre del caso>

| Campo | Valor |
|---|---|
| Caso | `<caso>` |
| Especificación | `spec.md` (aprobada) |
| Autor | Agente verificador |
| Fecha | AAAA-MM-DD |

Este archivo es evidencia: no se aprueba, se actualiza cada vez que se corre `/pruebas`.

## 1. Resumen
| Medida | Valor |
|---|---|
| Criterios y reglas de la especificación | N |
| Cubiertos por al menos una prueba | N (NN %) |
| Pruebas nuevas en esta ronda | N |
| Posibles defectos (pruebas nuevas que fallan) | N |
| Cobertura del dominio | NN % (mínimo `convenciones.pruebas.cobertura_minima_dominio`) |

## 2. Matriz criterio → prueba
| Criterio o regla | Prueba | Estado |
|---|---|---|
| RF-01 · … | `tests/test_...::test_...` | cubierto / parcial / sin prueba / **falla** |

## 3. Posibles defectos
| Prueba | Criterio | Esperado (spec) | Obtenido |
|---|---|---|---|
| `tests/...` | RF-.. | … | … |

Cada una está marcada con `@pytest.mark.xfail(strict=True, ...)`. Siguiente paso: el agente **depurador**, uno por uno; al corregir, quita la marca.

## 4. Datos de prueba
De dónde salieron (por ejemplo `datos_sinteticos("credito_consumo", 10, semilla=1, incluir_bordes=true)`) y por qué son sintéticos.

## 5. Lo que no se probó
Criterios que no se pueden probar automáticamente (por ejemplo, la interfaz) y cómo se verifican.
