# 03 — Roadmap

> Plan por fases **alineado con el Concepto Maestro §19**. La Pista B (red neuronal
> desde cero) avanza en paralelo. Se marca cada hito al completarlo.

## Fase 0 — Concepto rector ✅

- [x] Definición, límites y arquitectura (`concepto-maestro.md` v0.2)
- [x] Decisiones registradas (ADR 0001–0008)

## Fase 1 — Documentación base ✅

- [x] Arquitectura, carpeta de decisiones, glosario, base de conocimiento
- [x] `CHANGELOG.md` y `CITATION.cff` (solo autores humanos)
- [x] Plantillas en uso: `docs/modulos/`, `docs/contratos/`
- [x] **Núcleo portable** (`ampa/core/`) + base C++ (`cpp/`) — ADR 0007

## Fase 2 — Percepción mínima ✅ (base)

- [x] Contrato de evento §5.2 → `ampa/perception/events.py` + `docs/contratos/evento.md`
- [x] Clasificador de dominio por reglas (ADR 0008)
- [x] Evaluación de riesgo operativo y política de memoria (§6.2)
- [x] Comando `ampa percibir` + 13 pruebas
- [x] Registro (logs) de eventos percibidos (`journal` JSONL + `ampa diario`)

## Fase 3 — Memoria documental ⏳

- [ ] Ingesta de apuntes: troceo (chunking) y metadatos
- [ ] Embeddings + índice vectorial
- [ ] Recuperación contextual con **citas**

## Fase 4 — CLI funcional ⏳

- [ ] Preguntas y respuestas con fuentes
- [ ] Modo diagnóstico
- [ ] Integración con el motor (`llama.cpp`)

## Fase 5 — Escriba seguro ⏳

- [ ] Escritura multiplataforma (`pathlib`)
- [ ] **Backups** automáticos antes de cada cambio
- [ ] Modo simulación y bloqueo por riesgo alto
- [ ] Bitácora de cambios

## Fase 6 — Dominio químico-filosófico ⏳

- [ ] Base curada mínima de química y filosofía
- [ ] Pruebas por dominio
- [ ] Capa epistémica: origen y confianza por respuesta

## Fase 7 — Evaluación ⏳

- [ ] Banco propio de casos (química y filosofía)
- [ ] Métricas y detección de regresiones

## Fase 8 — Adaptación futura ⏳

- [ ] LoRA/QLoRA en ciclos controlados (ADR, dataset, pruebas antes/después)

## Pista B (paralela) — Red neuronal desde cero ⏳

- [ ] Tokenizer didáctico (SentencePiece)
- [ ] MLP en NumPy (forward, backprop)
- [ ] Versión C++ del MLP
- [ ] Clasificador de dominio entrenado (reemplaza/complementa al de reglas)
- [ ] Mini-transformer didáctico
