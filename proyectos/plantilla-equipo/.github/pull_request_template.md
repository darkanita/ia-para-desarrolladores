## Caso y etapa

- Caso: `docs/sdlc/<caso>/`
- Rama: `<tipo>/<caso>-<descripcion>` (ver `convenciones.ramas`)
- Etapa: intención · especificación · plan · construcción · corrección · revisión · entrega

## Artefactos

- [ ] `intent.md` aprobado
- [ ] `spec.md` aprobado
- [ ] `plan.md` aprobado
- [ ] `revision.md` del agente revisor, sin hallazgos bloqueantes abiertos

## Verificación

- [ ] `python -m pytest -q` en verde
- [ ] `python herramientas/verificar_capas.py` en OK
- [ ] Solo datos sintéticos; sin secretos ni datos restringidos en logs o mensajes

## Qué hizo el agente y qué revisó una persona

<!-- Una o dos frases: qué generó el asistente, qué hallazgos se atendieron y quién decidió. -->
