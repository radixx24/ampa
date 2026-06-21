# ADR-0011: Respuesta por recuperación (extractiva y citada) antes que generación

> Formato según Concepto Maestro §13.

## Estado

Aceptada

## Contexto

La Fase 4 introduce «preguntas y respuestas con fuentes». La generación con un
modelo (`llama.cpp`) aún no está integrada y, además, generar texto libre sin
control puede **inventar** (alucinar), en tensión con la honestidad epistémica del
proyecto y con la portabilidad (ADR 0007).

## Opciones consideradas

- **A. Respuesta extractiva citada**: devolver los fragmentos más relevantes de la
  memoria, literales y con cita, liderando con el mejor.
- **B. Generación con LLM** desde ya: redacta una respuesta, pero requiere el motor
  y el modelo, y arriesga alucinaciones sin anclaje.
- **C. No responder hasta tener el LLM**: bloquea el valor de la Fase 4.

## Decisión

**Opción A** como primera capa funcional: `responder` percibe la consulta, recupera
de la memoria (BM25) y compone una respuesta **extractiva y citada**; si no hay
evidencia, lo declara y **no inventa**. La generación (**B**) se añadirá después
**sobre estos mismos fragmentos citados**, como capa opcional.

## Alternativas

**C** se descartó por no entregar valor; **B** se pospone hasta integrar el motor,
para no romper la portabilidad ni la honestidad.

## Consecuencias

- 👍 Respuestas trazables y portables desde el primer día; cero alucinación.
- 👎 No redacta ni parafrasea: entrega citas literales, no prosa sintetizada.
- ➡️ El LLM generará prosa anclada a las mismas citas (RAG completo) más adelante.
