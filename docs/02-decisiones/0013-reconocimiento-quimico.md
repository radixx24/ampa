# ADR-0013: Reconocimiento químico por reglas y datos antes que ML/NER

> Formato según Concepto Maestro §13.

## Estado

Aceptada

## Contexto

AMPA necesita identificar **elementos y compuestos** en texto para el dominio
químico (Fase 6) y para una futura capa visual/adaptativa. Un NER entrenado
requiere datos etiquetados y dependencias; el núcleo es portable y sin
dependencias (ADR 0007), y el proyecto favorece lo explicable (ADR 0008).

## Opciones consideradas

- **A. Reglas + datos**: tabla periódica, parser de fórmulas y diccionario curado
  de compuestos.
- **B. NER/ML entrenado**: más flexible, pero con datos, dependencias y opacidad.
- **C. Llamar al LLM** para extraer química: no determinista y con coste.

## Decisión

**Opción A.** Tabla de 118 elementos, parser de fórmulas (con paréntesis) que
valida símbolos reales, y diccionario de compuestos comunes. Las fórmulas se
reconocen de forma exacta; los nombres, de forma heurística (los muy ambiguos,
solo por fórmula). Salida estructurada (símbolo, Z, composición) y JSON.

## Alternativas

**B** y **C** se posponen: aportarían cobertura, pero rompen portabilidad y
determinismo. El reconocedor por reglas es la línea base y la interfaz estable.

## Consecuencias

- 👍 Portable, explicable, testeable y con datos listos para visualizar.
- 👎 Cobertura limitada al diccionario y al léxico; sin semántica profunda.
- ➡️ Podrá complementarse con ML o con el LLM manteniendo la misma salida.
