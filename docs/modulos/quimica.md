# Módulo: chemistry (reconocimiento químico)

> Documentado según la plantilla del Concepto Maestro §12.
> Código: `ampa/chemistry/` · Pruebas: `tests/test_chemistry.py` · Decisión: ADR 0013

## 1. Propósito

Identificar **componentes (elementos)** y **compuestos** químicos en texto y
entregarlos **estructurados** (símbolo, número atómico, composición), como base
para el dominio químico (Fase 6) y para capas **visuales/adaptativas**.

## 2. Responsabilidad exacta

**Hace:**
- Reconoce **elementos** por nombre (es) o por fórmula de un solo elemento (`O2`).
- Reconoce **compuestos** por nombre curado o por **fórmula** (`H2O`, `Ca(OH)2`).
- **Parsea** fórmulas a su composición (elemento → átomos), con paréntesis.
- Devuelve entidades estructuradas y serializables (`to_dict`, JSON).

**No hace:**
- No balancea reacciones ni calcula masas (aún): solo identifica y compone.
- No usa ML/NER ni dependencias externas (reglas + datos, como ADR 0008/0007).

## 3. Entradas

- `texto` (str): texto libre a analizar.

## 4. Salidas

- `ResultadoQuimica`: `elementos` y `compuestos` (`EntidadQuimica`), con `to_dict()`.
- `EntidadQuimica`: `tipo`, `nombre`, `formula`, `simbolo`, `numero_atomico`,
  `composicion`, `texto`.

## 5. Flujo interno

1. Compuestos por **nombre** (diccionario curado), registrando sus posiciones.
2. **Fórmulas** sobre el texto original (sensibles a mayúsculas), validando que
   los símbolos sean elementos reales.
3. Elementos por **nombre**, omitiendo los que caen dentro de un compuesto ya visto.

## 6. Decisiones de diseño

- **Reglas + datos antes que ML** (ADR 0013): explicable, portable y sin descargas.
- **Validación estricta de fórmulas**: evita falsos positivos con palabras normales.
- **Nombres muy ambiguos** (p. ej. «radio») se reconocen solo por fórmula.
- **Estructura lista para visualizar**: composición y número atómico por entidad.

## 7. Errores esperados

- Texto sin química → resultado vacío (`hay()` es `False`).
- Fórmula mal formada o con símbolos inexistentes → se ignora.

## 8. Seguridad y límites

- Determinista y local; el diccionario de compuestos es **mínimo** (ampliable).
- La detección por nombre es heurística (español); las fórmulas son exactas.

## 9. Pruebas mínimas

- `tests/test_chemistry.py` (7 casos): parseo con paréntesis, validación de
  símbolos, compuestos por fórmula y por nombre, elementos por nombre, no
  duplicar el elemento dentro de un compuesto y ausencia de falsos positivos.
- Ejecutar: `python -m unittest discover -s tests -t .`

## 10. Cambios pendientes

- Ampliar el diccionario de compuestos y los sinónimos.
- Masas atómicas y propiedades (para cálculos y visualización).
- Usar la química detectada para enriquecer las respuestas (capa epistémica).
