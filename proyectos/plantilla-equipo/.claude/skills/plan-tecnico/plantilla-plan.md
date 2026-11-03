# Plan: <título del caso>

| Campo | Valor |
|---|---|
| Caso | `<caso>` |
| Estado | borrador |
| Especificación | [`spec.md`](spec.md) (aprobada por <nombre>) |
| Autor | <equipo o persona> |
| Fecha | <AAAA-MM-DD> |
| Aprobado por | pendiente (líder técnico) |

## 1. Resumen técnico
<Cómo se construye, en 3 a 5 frases: paquete, capas, qué entra por puertos, cuál es el primer componente.>

## 2. Estructura
```text
src/<paquete>/
├── dominio/        <archivos>
├── puertos/        <archivos>
├── casos_uso/      <archivos>
├── adaptadores/    <archivos>
└── app/            <archivos>
tests/              <archivos>
```

## 3. Componentes
| Capa | Archivo | Responsabilidad | Cubre (RF / RN) |
|---|---|---|---|
| dominio | | | |

## 4. Puertos y adaptadores
| Puerto | Qué abstrae | Adaptador para pruebas | Adaptador real (servicio del catálogo) |
|---|---|---|---|
| | | | |

## 5. Nombres validados
| Tipo | Nombre | `validar_nombre` |
|---|---|---|
| paquete | | OK |

## 6. Pruebas
| Criterio de aceptación (spec) | Archivo | Prueba |
|---|---|---|
| RF-01 · <criterio> | `tests/test_<modulo>.py` | `test_<regla>_<caso>` |

## 7. Pasos (en orden, prueba primero)
- [ ] **Paso 1 · Estructura.** `python herramientas/crear_estructura.py <paquete>`.
- [ ] **Paso 2 · <componente>.** Prueba: <pruebas>. Implementación: <archivo>. Listo cuando: <criterio>.
- [ ] ...

**Primer componente:** pasos 1 a <n>.

## 8. Dependencias
| Paquete | Para qué | ¿Aprobada en `banco.yaml`? |
|---|---|---|
| pytest | pruebas | sí |

## 9. Decisiones técnicas y riesgos
-

## 10. Fuera de este plan
-

## 11. Preguntas abiertas
-
