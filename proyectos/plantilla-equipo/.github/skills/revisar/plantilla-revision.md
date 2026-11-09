# Revisión · <nombre del caso>

| Campo | Valor |
|---|---|
| Caso | `<caso>` |
| Rama revisada | `<tipo>/<caso>-<descripcion>` contra `main` |
| Commits | `<primer>`..`<último>` |
| Estado | borrador |
| Autor | Agente revisor |
| Fecha | AAAA-MM-DD |
| Aprobado por | pendiente (dueño del código) |

## 1. Resumen
Qué cambia esta rama, en dos o tres frases, y el veredicto: **se puede fusionar** / **no se puede fusionar hasta atender los bloqueantes**.

## 2. Verificación automática
| Verificación | Resultado |
|---|---|
| `python -m pytest -q` | N pruebas, en verde / N fallan |
| `python herramientas/verificar_capas.py` | OK / N violaciones |

## 3. Hallazgos
| ID | Severidad | Archivo:línea | Qué pasa | Regla o política | Sugerencia |
|---|---|---|---|---|---|
| H-01 | bloqueante | `src/...:NN` | … | `politicas.logs` | … |

Severidades según `politicas.revision`: **bloqueante** (incumple una regla de negocio, una política de datos o seguridad, o rompe pruebas), **importante** (incumple una convención o deja un criterio sin prueba), **sugerencia** (mejora opcional).

## 4. Criterios de aceptación cubiertos
| Criterio (RF) | Prueba | ¿Cubierto? |
|---|---|---|
| RF-01 … | `tests/test_...::test_...` | sí / no |

## 5. Lo que no se revisó
Lo que quedó fuera de esta revisión y por qué (por ejemplo, archivos que no cambiaron).

## 6. Decisión del dueño del código
- [ ] Atender los hallazgos bloqueantes e importantes (o justificar por qué no)
- [ ] Volver a revisar después de los cambios
- [ ] Aprobar: cambiar `Estado` a `aprobado` y fusionar el pull request

## 7. Texto para el pull request
Un párrafo corto para pegar como comentario del pull request: veredicto y hallazgos bloqueantes.
