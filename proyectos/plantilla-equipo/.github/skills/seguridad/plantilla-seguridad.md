# Revisión de seguridad · <caso>

| Campo | Valor |
|---|---|
| Caso | `docs/sdlc/<caso>/` |
| Alcance | <rama `<nombre>` frente a `main` · o · el caso completo> |
| Estado | borrador |
| Aprobado por | pendiente (dueño del código) |
| Revisó | <agente y asistente, por ejemplo: agente seguridad en Copilot, modelo X> |

## 1. Resumen
<Dos o tres frases: qué se revisó y la conclusión. ¿Puede entrar a main?>

| Bloqueantes | Importantes | Sugerencias | ¿Rotar secretos? |
|---|---|---|---|
| <n> | <n> | <n> | <sí: cuáles (sin el valor) · no> |

## 2. Verificación automática
| Verificación | Resultado |
|---|---|
| `python herramientas/buscar_secretos.py --historia` | <OK · n hallazgos> |
| `python -m pytest -q` | <n passed> |
| `python herramientas/verificar_capas.py` | <OK · violaciones> |
| Hook `proteger.py` en `.claude/settings.json` y `.github/hooks/` | <sí · no> |

## 3. Hallazgos
| ID | Severidad | OWASP | Archivo:línea | Qué pasa (sin secretos ni datos completos) | Política | Recomendación |
|---|---|---|---|---|---|---|
| S-01 | bloqueante | A04 | `<archivo>:<línea>` | <...> | `politicas.seguridad` | <...> |

## 4. Lista OWASP Top 10 (2025)
| Categoría | ¿Aplica? | Resultado |
|---|---|---|
| A01 Control de acceso roto (incluye SSRF) | <sí · no> | <hallazgos o "sin hallazgos"> |
| A02 Configuración insegura | | |
| A03 Cadena de suministro | | |
| A04 Fallas criptográficas | | |
| A05 Inyección | | |
| A06 Diseño inseguro | | |
| A07 Fallas de autenticación | | |
| A08 Integridad de software o datos | | |
| A09 Registro y alertas | | |
| A10 Condiciones excepcionales | | |

## 5. Lo que no se revisó
<Lo que quedó fuera del alcance y por qué (por ejemplo: dependencias transitivas, infraestructura).>

## 6. Revisión cruzada
| Escribió el código | Revisó la seguridad |
|---|---|
| <persona · asistente y modelo, según los commits o lo que diga la persona> | <agente, asistente y modelo de esta revisión> |

## 7. Para el pull request
<Un párrafo para pegar como comentario: hallazgos bloqueantes, secretos a rotar y qué decide el dueño del código.>
