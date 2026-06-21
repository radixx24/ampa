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
- Calcula la **masa molar** y expone datos por elemento (masa, grupo, periodo,
  categoría) para visualización.
- Modela **moléculas** (átomos + enlaces), deriva su fórmula/masa y **guarda
  compuestos** que tú alimentes (`ampa compuesto`).
- Detecta **grupos funcionales** e infiere **reacciones** posibles (combustión
  balanceada, hidrogenación, neutralización…): el **editor de carbono**.
- Genera **geometría 3D** (layout por fuerzas) para visualizar la molécula.
- Devuelve entidades estructuradas y serializables (`to_dict`, JSON).

**No hace:**
- No balancea reacciones ni calcula masas (aún): solo identifica y compone.
- No usa ML/NER ni dependencias externas (reglas + datos, como ADR 0008/0007).

## 3. Entradas

- `texto` (str): texto libre a analizar.

## 4. Salidas

- `ResultadoQuimica`: `elementos` y `compuestos` (`EntidadQuimica`), con `to_dict()`.
- `EntidadQuimica`: `tipo`, `nombre`, `formula`, `simbolo`, `numero_atomico`,
  `composicion`, `masa_molar`, `texto`.
- `Elemento` (tabla periódica): `simbolo`, `z`, `nombre`, `masa`, `periodo`,
  `grupo`, `categoria`; `tabla()` los devuelve todos y `ampa quimica --tabla` los vuelca.
- `Molecula` (átomos + enlaces): `formula()`, `composicion()`, `masa_molar()`,
  `to_dict()`; se persiste con `guardar_compuesto` / `cargar_compuestos`.
- `grupos_funcionales(mol)` → lista de grupos; `reacciones(mol)` → lista de
  `Reaccion` (`tipo`, `ecuacion`, `descripcion`).
- `geometria_3d(mol)` → coordenadas 3D por átomo (para el visor 3D).

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

- `tests/test_chemistry.py` (10 casos): parseo con paréntesis, validación de
  símbolos, compuestos por fórmula/nombre, elementos por nombre, no duplicar el
  elemento dentro de un compuesto, ausencia de falsos positivos, y datos de la
  tabla (118 elementos, masa molar, datos por elemento).
- `tests/test_molecules.py` (4 casos): fórmula de Hill, masa, validación y
  persistencia de compuestos.
- `tests/test_carbon.py` (11 casos): grupos funcionales y reacciones (combustión
  balanceada, halogenación, hidratación, deshidratación, neutralización…).
- `tests/test_geometry.py` (4 casos): coordenadas por átomo, determinismo, molécula
  vacía y distancia de enlace razonable.
- Ejecutar: `python -m unittest discover -s tests -t .`

## 10. Cambios pendientes

- Ampliar aún más el diccionario de compuestos y los sinónimos.
- Más tipos de reacción y balanceo general (no solo combustión).
- Más propiedades por elemento (electronegatividad, estados).
