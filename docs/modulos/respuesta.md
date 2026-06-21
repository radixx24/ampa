# Módulo: answer (respuesta con fuentes)

> Documentado según la plantilla del Concepto Maestro §12.
> Código: `ampa/answer/` · Pruebas: `tests/test_answer.py` · Decisiones: ADR 0011 y 0014

## 1. Propósito

Responder preguntas **con fuentes**: unir percepción y memoria para devolver una
respuesta **fundamentada, citada, con su confianza y origen** a partir de los
apuntes (Concepto Maestro §5–§7; RAG, ADR 0002). Primera capa funcional de la
CLI (Fase 4).

## 2. Responsabilidad exacta

**Hace:**
- **Percibe** la consulta (dominio, riesgo) reutilizando `perception`.
- **Recupera** los fragmentos más relevantes de la memoria (BM25, con citas).
- **Compone** una respuesta extractiva: lidera con la mejor evidencia y sus citas.
- Estima la **confianza** (cobertura de términos + dominio) e indica el **origen**.
- Señala la **química detectada** en la respuesta (elementos y compuestos).
- Es **honesta**: si no hay evidencia, lo declara y **no inventa**.

**No hace:**
- No **genera** lenguaje todavía (sin LLM; ADR 0011): cita literalmente.
- No escribe ni actúa (eso es `scribe`).
- No usa dependencias externas (portabilidad, ADR 0007).

## 3. Entradas

- `consulta` (str): la pregunta.
- `k` (int): número de fragmentos a considerar como evidencia.

## 4. Salidas

- `Respuesta` (dataclass): `consulta`, `evento`, `resultados`, `confianza`,
  `quimica`; con `dominio`, `riesgo`, `hay_evidencia()`, `fuentes()`/`origen()`,
  `texto()` y `diagnostico()`.

## 5. Flujo interno

1. `perceive(consulta)` → evento (dominio, riesgo).
2. `recuperar(consulta, k)` → fragmentos citados (BM25).
3. `texto()` compone la respuesta (o el mensaje honesto si no hay evidencia).

## 6. Decisiones de diseño

- **Recuperación extractiva antes que generación** (ADR 0011): citas literales,
  trazables y portables; la generación con modelo se añadirá sobre la misma base.
- **Honestidad por defecto**: sin evidencia → se declara, no se inventa.
- **Confianza por cobertura + dominio** (ADR 0014), no por score absoluto:
  estable e independiente del tamaño del corpus.
- **Reutiliza percepción + memoria + química**: la respuesta une las tres capas.

## 7. Errores esperados

- Memoria vacía o sin coincidencias → respuesta honesta de «sin evidencia».

## 8. Seguridad y límites

- **No fabrica fuentes ni datos**: lo que afirma está citado y es literal.
- El modo `--detalle` expone la percepción y los scores para auditar la respuesta.

## 9. Pruebas mínimas

- `tests/test_answer.py` (5 casos): respuesta con cita, dominio y **confianza**,
  honestidad sin evidencia, pregunta fuera de tema, diagnóstico y **química
  detectada**.
- Ejecutar: `python -m unittest discover -s tests -t .`

## 10. Cambios pendientes

- **Generación con modelo** (`llama.cpp`) sobre los fragmentos citados.
- Síntesis de varias fuentes en una respuesta redactada (conservando las citas).
- Calibrar la confianza con más señales y permitir filtrado por dominio.
