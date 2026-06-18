# 03 — Roadmap

> Plan por fases. Las dos pistas (sistema y red neuronal) avanzan en paralelo.
> Marcamos cada hito al completarlo.

## Fase 0 — Fundación 🚧 (actual)

- [x] Definir visión y principios (`00-vision.md`)
- [x] Diseñar la arquitectura (`01-arquitectura.md`)
- [x] Registrar decisiones iniciales (ADR 0001–0003)
- [x] Glosario y fuentes de conocimiento
- [ ] Recoger el contexto del autor (conocimientos, contenido propio)
- [ ] Definir dependencias y entorno (`requirements`, toolchain C++)

## Fase 1 — El modelo respira (Pista 1)

- [ ] Integrar `llama.cpp` (compilar o vía `llama-cpp-python`)
- [ ] Descargar y cargar un modelo 3B Q4
- [ ] CLI mínima: pregunta → respuesta
- [ ] Medir velocidad real en CPU (benchmark reproducible)

## Fase 2 — Primer cerebro propio (Pista 2)

- [ ] MLP en Python (NumPy): forward, backprop, entrenamiento
- [ ] Dataset de patrones simple para validar el aprendizaje
- [ ] Espejo en C++ del mismo MLP
- [ ] Documento educativo paso a paso

## Fase 3 — Memoria y conocimiento (Pista 1)

- [ ] Pipeline de ingesta: documento → troceo → embeddings → vector DB
- [ ] Recuperación (RAG) conectada al prompt
- [ ] Respuestas **con citas** de la fuente
- [ ] Aprendizaje: "enséñale" algo y que lo recupere después

## Fase 4 — Las dos pistas se encuentran

- [ ] Entrenar el MLP como **clasificador de dominio** (medicina/psicología/filosofía)
- [ ] Conectarlo al orquestador para enrutar la recuperación
- [ ] Capa epistémica: marcar origen y confianza de cada respuesta

## Fase 5 — Base de conocimientos de los tres dominios

- [ ] Curar e ingerir corpus de medicina, psicología y filosofía
- [ ] Verificar licencias y registrar fuentes
- [ ] Disclaimers automáticos en temas sensibles (salud)

## Fase 6 — Aprendizaje paramétrico (opcional, avanzado)

- [ ] Consolidador: destilar memoria RAG en adaptadores **LoRA**
- [ ] Entrenamiento por lotes en CPU (modelos pequeños)
- [ ] Evaluar si mejora frente a solo-RAG

## Fase 7 — Pulido

- [ ] Interfaz mejorada (¿API + web mínima?)
- [ ] Tests y reproducibilidad
- [ ] Empaquetado e instrucciones de instalación

> El orden no es rígido: las fases 1 y 2 pueden ir a la par por ser de pistas
> distintas.
