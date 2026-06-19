# ADR-0010: Recuperación léxica (BM25) portable antes que embeddings

> Formato según Concepto Maestro §13.

## Estado

Aceptada

## Contexto

La memoria documental (Fase 3) debe recuperar fragmentos relevantes de los apuntes
para responder **con citas** (ADR 0002, «RAG primero»). Los embeddings semánticos
requieren un modelo y dependencias, mientras que el núcleo es portable y sin
dependencias (ADR 0007).

## Opciones consideradas

- **A. Recuperación léxica (BM25/TF-IDF)**: solo texto, sin dependencias.
- **B. Embeddings + índice vectorial** (p. ej. FAISS): mejor semántica, pero
  pesado, con dependencias y un modelo que cargar.
- **C. Búsqueda por subcadena**: trivial, pero sin ranking ni relevancia.

## Decisión

**Opción A** para la primera iteración: índice **BM25** en memoria sobre los
fragmentos almacenados, con tokenización normalizada (minúsculas, sin acentos).
Cada resultado conserva **fuente e índice** para citar. Los embeddings (**B**)
llegan en una segunda iteración **sin romper** la interfaz `recuperar(...)`.

## Alternativas

**C** se descartó por calidad (sin relevancia); **B** se pospone por su peso y
dependencias, no por su valor: será un recuperador alternativo o híbrido.

## Consecuencias

- 👍 Funciona desde el primer día: portable, explicable, testeable y con citas exactas.
- 👎 No captura sinónimos ni paráfrasis (limitación inherente a lo léxico).
- ➡️ Se añadirán embeddings manteniendo la misma API de recuperación.
