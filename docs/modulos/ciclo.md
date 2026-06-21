# Módulo: cycle (ciclo percepción → memoria → acción)

> Documentado según la plantilla del Concepto Maestro §12.
> Código: `ampa/cycle/` · Pruebas: `tests/test_cycle.py` · Decisión: ADR 0012

## 1. Propósito

Realizar el **ciclo rector** del Concepto Maestro (§6): unir percepción, memoria y
acción en un solo flujo auditable. Es la **tesis del proyecto** hecha comando.

## 2. Responsabilidad exacta

**Hace:**
- **Percibe** la entrada (dominio, tipo, riesgo) con `perception`.
- **Recupera** contexto citado de la memoria (`memory`, BM25).
- **Compone** una nota enriquecida (observación + metadatos + citas).
- **Propone** la escritura (simulación) por defecto; con `ejecutar` **recuerda**
  (diario + memoria según la política) y **escribe** con respaldo, bajo la puerta
  de riesgo del escriba.

**No hace:**
- No **genera** lenguaje (sin LLM): la nota es estructural y las citas, literales.
- No actúa sin autorización: por defecto solo propone; el riesgo alto exige `forzar`.
- No usa dependencias externas (portabilidad, ADR 0007).

## 3. Entradas

- `entrada` (str): la observación.
- `destino` (opcional): archivo donde anotar (por defecto `data/bitacora.md`).
- `k`, `ejecutar`, `forzar`, `registrar`.

## 4. Salidas

- `ResultadoCiclo`: `evento`, `contexto` (citas), `nota`, `destino`, `escritura`
  (`ResultadoEscritura`), `registrado`, `ingeridos`; con `resumen()` auditable.

## 5. Flujo interno

1. **Percepción**: `perceive(entrada)`.
2. **Memoria**: `recuperar(entrada, k)` (contexto previo). Si `ejecutar`: registra
   el evento (diario) e ingiere la entrada si la política lo permite.
3. **Acción**: compone la nota, la anexa al destino y la escribe **simulada** o
   **real** (con respaldo), con `riesgo = evento.riesgo_operativo`.

## 6. Decisiones de diseño

- **Proponer por defecto, ejecutar con autorización** (ADR 0012): el ciclo es
  seguro de invocar; nada se persiste sin `ejecutar`.
- **Una sola puerta de riesgo**: la señal de la percepción gobierna la escritura.
- **Anexar con respaldo**: cada ejecución es reversible (rollback vía `scribe`).
- **Reutiliza las tres capas**: el ciclo es orquestación, no lógica nueva.

## 7. Errores esperados

- Riesgo alto sin `forzar` → escritura **bloqueada** (no es un fallo: es la puerta).
- Memoria vacía → nota sin contexto («ninguno»), el ciclo continúa.

## 8. Seguridad y límites

- **Seguro por defecto**: sin `ejecutar` no toca disco ni memoria.
- **Reversible**: toda escritura real deja respaldo.
- **Trazable**: `ResultadoCiclo.resumen()` muestra las tres etapas.

## 9. Pruebas mínimas

- `tests/test_cycle.py` (4 casos): propuesta sin efectos, ejecución que escribe y
  recuerda, anexado con respaldo y `--sin-registro`.
- Ejecutar: `python -m unittest discover -s tests -t .`

## 10. Cambios pendientes

- Proponer **correcciones** concretas sobre archivos existentes (no solo bitácora).
- Generación con modelo para redactar la nota (conservando las citas).
- Consolidar la **bitácora** como log formal de cambios (Fase 5).
