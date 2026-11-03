---
description: "Reglas para las APIs del equipo (FastAPI)"
applyTo: "**/api/**/*.py,**/adaptadores/api*.py"
---
<!-- Generado desde .claude/rules/api.md con herramientas/sincronizar_skills.py: edite el original. -->

# Reglas para las APIs

- Rutas en plural, en español y con versión: `/v1/clientes/{id_cliente}`. Consulte `politicas.apis` y `politicas.nombres`.
- Los modelos de entrada y salida son de Pydantic y viven en el adaptador, no en el dominio.
- Montos como texto decimal en el contrato (`"1500000.00"`), convertidos a `Decimal` al entrar.
- Errores con el formato `{codigo, mensaje, id_correlacion}`; el mensaje es apto para el usuario y no muestra detalles internos.
- Antes de crear un servicio nuevo, busque en el catálogo (`catalogo_servicios`) si ya existe uno que sirva.
- Ningún dato restringido en la respuesta si el caso no lo necesita; cuentas enmascaradas.
