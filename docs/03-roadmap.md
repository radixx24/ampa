# 03 — Roadmap

> Plan por fases. Las dos pistas (sistema y red neuronal) avanzan en paralelo.
> Marcamos cada hito al completarlo. Resumen de capas en
> [`concepto-maestro.md`](concepto-maestro.md).

## Fase 0 — Fundación 🚧 (actual)

- [x] Definir visión y principios (`00-vision.md`)
- [x] Diseñar la arquitectura (`01-arquitectura.md`)
- [x] Documento maestro que conjunta todas las ideas (`concepto-maestro.md`)
- [x] Registrar decisiones (ADR 0001–0006)
- [x] Glosario y fuentes de conocimiento (química + filosofía)
- [x] `CHANGELOG.md` y `CITATION.cff` (solo autores humanos)
- [ ] Recoger el contexto del autor (nivel en C++/Python, primeros apuntes)
- [ ] Definir dependencias y entorno (`requirements`, toolchain C++)

## Fase 1 — Didáctica: red neuronal desde cero (Pista 2)

- [ ] MLP en Python (NumPy): forward, backprop, entrenamiento
- [ ] Dataset de patrones simple para validar el aprendizaje
- [ ] Espejo del MLP en C++
- [ ] Mini-tokenizer con SentencePiece
- [ ] Documento educativo paso a paso

## Fase 2 — El modelo respira + RAG de tus apuntes (Pista 1)

- [ ] Integrar `llama.cpp` y cargar un modelo 1.7B–3B Q4
- [ ] CLI mínima: pregunta → respuesta
- [ ] Benchmark de velocidad real en CPU
- [ ] Pipeline de ingesta de apuntes → embeddings → vector DB
- [ ] Recuperación (RAG) conectada al prompt, con **citas**

## Fase 3 — Memoria dinámica + escriba con backups

- [ ] Persistencia de la memoria entre sesiones
- [ ] Priorización dinámica (relevancia + recencia)
- [ ] Módulo "escriba" multiplataforma (Windows/Linux)
- [ ] **Backups** automáticos antes de cada escritura
- [ ] "Enséñale" algo y que lo recuerde en la siguiente sesión

## Fase 4 — Motor de dinamismo (simulaciones aleatorias)

- [ ] Decodificación estocástica controlada (temperatura, top-p)
- [ ] Muestreo tipo Monte Carlo + auto-consistencia
- [ ] Escenarios/ejemplos aleatorios para química
- [ ] **Semilla reproducible** en todo el sistema

## Fase 5 — Dominios y clasificador

- [ ] Curar e ingerir base de **química** y **filosofía**
- [ ] Entrenar el MLP como **clasificador de dominio** (química/filosofía/general)
- [ ] Conectarlo al orquestador para enrutar la recuperación
- [ ] Capa epistémica: marcar origen y confianza de cada respuesta

## Fase 6 — Aprendizaje paramétrico (opcional, avanzado)

- [ ] Consolidador: destilar memoria en adaptadores **LoRA/QLoRA**
- [ ] Entrenamiento por lotes (modelos pequeños)
- [ ] Evaluar si mejora frente a solo-RAG, sin degradar capacidades

## Fase 7 — Evaluación y pulido

- [ ] Banco propio de casos (química y filosofía) con respuestas de referencia
- [ ] Tests y reproducibilidad
- [ ] Empaquetado e instrucciones de instalación
- [ ] ¿Interfaz API + web mínima?

> El orden no es rígido: las fases 1 y 2 pueden ir a la par por ser de pistas
> distintas.
