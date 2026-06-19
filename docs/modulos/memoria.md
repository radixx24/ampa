# Módulo: memory (memoria documental)

> Documentado según la plantilla del Concepto Maestro §12.
> Código: `ampa/memory/` · Pruebas: `tests/test_memory.py` · Decisiones: ADR 0002 y 0010

## 1. Propósito

Convertir los apuntes del usuario en **memoria consultable con citas**: ingerir,
trocear en fragmentos y recuperar los más relevantes para una consulta (estrategia
RAG, ADR 0002).

## 2. Responsabilidad exacta

**Hace:**
- Trocea apuntes en **fragmentos citables** (`chunker`), respetando los párrafos.
- Etiqueta cada fragmento con su **dominio** (reutiliza la percepción).
- Persiste los fragmentos en JSONL portable (`store`, bajo `Paths.memory`).
- Recupera por relevancia léxica **BM25** y devuelve **citas** (`retriever`).

**No hace:**
- No genera lenguaje ni redacta la respuesta (eso será la orquestación/LLM).
- No usa embeddings todavía (ADR 0010) ni dependencias externas.
- No decide acciones ni escribe archivos (eso es `scribe`).

## 3. Entradas

- Ingesta: `texto` o `ruta_fuente`, `fuente`, `max_palabras`, `solapamiento`,
  `clasificar`.
- Consulta: `consulta` (str), `k` (número de resultados).

## 4. Salidas

- `Fragmento` (texto, fuente, índice, dominio); `id` = `fuente#indice`.
- `Resultado` (fragmento + `score`) con `cita()` → `[fuente#indice]`.

## 5. Flujo interno

1. **Ingesta**: trocear → clasificar dominio → persistir (append JSONL).
2. **Consulta**: cargar fragmentos → indexar BM25 → puntuar → top-k con citas.

## 6. Decisiones de diseño

- **BM25 léxico antes que embeddings** (ADR 0010): portable y explicable.
- **Citas siempre** (fuente + índice): honestidad epistémica y trazabilidad.
- **Troceo por párrafos** con solapamiento: fragmentos legibles y citables.
- **Reutiliza la percepción** para el dominio (cohesión entre módulos).
- **Solo biblioteca estándar** (ADR 0007).

## 7. Errores esperados

- Memoria vacía o sin coincidencias → lista vacía (no falla).
- `max_palabras <= 0` → `ValueError` explícito.

## 8. Seguridad y límites

- Solo recuerda lo que se ingiere explícitamente; nada externo.
- La recuperación es local y determinista; **no inventa fuentes**.

## 9. Pruebas mínimas

- `tests/test_memory.py` (6 casos): troceo, persistencia + etiquetado, recuperación
  con cita, sin coincidencias y límite `k`.
- Ejecutar: `python -m unittest discover -s tests -t .`

## 10. Cambios pendientes

- **Embeddings + índice vectorial** (recuperador semántico/híbrido, misma API).
- Deduplicación/actualización por fuente al reingerir.
- Filtrado de la recuperación por dominio.
