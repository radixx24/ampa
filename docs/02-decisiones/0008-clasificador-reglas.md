# ADR-0008: Clasificador de dominio inicial por reglas (heurístico) antes que ML

> Formato según Concepto Maestro §13.

## Estado

Aceptada

## Contexto

La capa de percepción necesita asignar un dominio a cada entrada (química /
filosofía / general / documentación / operación). Todavía no existe la red neuronal
(Pista B) ni un conjunto de datos etiquetados para entrenarla.

## Opciones consideradas

- **A. Reglas / heurística** por palabras clave distintivas.
- **B. Modelo de ML entrenado** (requiere datos etiquetados y dependencias).
- **C. Usar el propio LLM** para clasificar (coste por token, no determinista).

## Decisión

**Opción A.** Un clasificador por reglas: términos distintivos normalizados
(minúsculas, sin acentos) por dominio. Devuelve el dominio y los términos
encontrados; sin dependencias externas.

## Justificación

- **Explicable y determinista**, lo que encaja con la honestidad epistémica y la
  reproducibilidad del proyecto.
- **Sin dependencias** (portabilidad, ADR 0007); funciona desde el primer día.
- Sirve como **línea base** y como generador de casos para entrenar más adelante la
  red neuronal de la Pista B.

## Consecuencias

- 👍 Inmediato, transparente, testeable y portable.
- 👎 Cobertura limitada al léxico; puede fallar en textos ambiguos o sin términos
  distintivos (caen en `general`).
- ➡️ Se sustituirá o complementará con la red neuronal (Pista B); este clasificador
  quedará como referencia y respaldo.
