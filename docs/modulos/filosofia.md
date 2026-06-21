# Módulo: philosophy (reconocimiento de filosofía)

> Documentado según la plantilla del Concepto Maestro §12.
> Código: `ampa/philosophy/` · Pruebas: `tests/test_philosophy.py` · Decisión: ADR 0013

## 1. Propósito

Identificar **filósofos**, **corrientes** y **conceptos** en texto y entregarlos
**estructurados** (época, corriente, rama), como base del dominio filosófico
(Fase 6) y para capas visuales/adaptativas. Además mantiene un **cuaderno
personal**: tú añades pensamientos y AMPA conserva un **diccionario** que crece
con lo que pones (término → tus reflexiones).

## 2. Responsabilidad exacta

**Hace:**
- Reconoce **filósofos** por nombre, con su **época** y **corriente**.
- Reconoce **corrientes** (`-ismo`s) y **conceptos** (con su **rama**).
- Coincidencia de palabra completa, sin acentos (evita falsos positivos).
- **Conserva pensamientos** del usuario y construye un **diccionario personal**
  (término → pensamientos), con términos detectados o indicados (`--sobre`).
- Devuelve entidades estructuradas y serializables (`to_dict`, JSON).

**No hace:**
- No interpreta ni resume doctrinas: solo identifica entidades.
- No usa ML/NER ni dependencias externas (reglas + datos; ADR 0013/0007).

## 3. Entradas

- `texto` (str): texto libre a analizar.

## 4. Salidas

- `ResultadoFilosofia`: `filosofos`, `corrientes`, `conceptos`
  (`EntidadFilosofica`), con `to_dict()`.
- `EntidadFilosofica`: `tipo`, `nombre`, `categoria` (corriente/rama), `epoca`, `texto`.
- `Pensamiento` (cuaderno): `texto`, `terminos`, `timestamp`; `diccionario()`
  agrupa por término (`ampa pensar` / `ampa diccionario [término] [--json]`).

## 5. Flujo interno

1. Normaliza el texto (minúsculas, sin acentos).
2. Busca por **palabra completa** en los tres datasets curados.
3. Deduplica y ordena (filósofos → corrientes → conceptos).

## 6. Decisiones de diseño

- **Reglas + datos** (ADR 0013), igual que química: explicable y portable.
- **Datasets mínimos y ampliables** (filósofos, corrientes, conceptos).
- **Coincidencia por palabra completa**: «marxismo» es corriente, no «Marx».

## 7. Errores esperados

- Texto sin filosofía → resultado vacío (`hay()` es `False`).

## 8. Seguridad y límites

- Determinista y local; la cobertura depende de los datasets (mínimos por ahora).

## 9. Pruebas mínimas

- `tests/test_philosophy.py` (8 casos): filósofos/corrientes/conceptos, metadatos,
  «marxismo» ≠ «Marx», ausencia de falsos positivos, estructura `to_dict`, y el
  **cuaderno** (agrupación, detección automática y vacío).
- Ejecutar: `python -m unittest discover -s tests -t .`

## 10. Cambios pendientes

- Ampliar los datasets (más filósofos, obras y conceptos).
- Relacionar filósofos ↔ corrientes ↔ conceptos (grafo para visualización).
- Integrar la filosofía detectada en las respuestas (como la química).
