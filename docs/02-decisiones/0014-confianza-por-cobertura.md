# ADR-0014: Confianza por cobertura léxica y dominio (no por score absoluto)

> Formato según Concepto Maestro §13.

## Estado

Aceptada

## Contexto

La capa de respuesta debe expresar **cuánta confianza** tiene en lo que devuelve
(honestidad epistémica). El score BM25 es relativo al corpus: su magnitud cambia
con el número de documentos (el *idf* colapsa con memorias pequeñas), así que un
umbral absoluto sobre el score daría una confianza engañosa.

## Opciones consideradas

- **A. Cobertura de términos + acuerdo de dominio**: qué fracción de los términos
  (con contenido) de la consulta cubre la mejor evidencia, y si su dominio coincide.
- **B. Umbral sobre el score BM25**: simple, pero depende del tamaño del corpus.
- **C. Probabilidad calibrada (ML)**: requeriría datos y dependencias.

## Decisión

**Opción A.** Confianza ∈ {nula, baja, media, alta}: `nula` sin evidencia; `alta`
si la cobertura ≥ 0.6 y el dominio coincide; `media` si la cobertura ≥ 0.3; `baja`
en otro caso. Explicable, portable e independiente del tamaño del corpus.

## Alternativas

**B** se descartó por engañoso con corpus pequeños; **C** por sus dependencias y
necesidad de datos etiquetados.

## Consecuencias

- 👍 Señal honesta y estable; no promete una certeza que no tiene.
- 👎 Heurística (léxica): no capta sinónimos ni cobertura semántica.
- ➡️ Con embeddings/LLM podrá medirse cobertura semántica manteniendo la escala.
