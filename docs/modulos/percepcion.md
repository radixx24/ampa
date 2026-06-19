# Módulo: perception (capa de percepción)

> Documentado según la plantilla del Concepto Maestro §12.
> Código: `ampa/perception/` · Pruebas: `tests/test_perception.py` · Contrato:
> `docs/contratos/evento.md`

## 1. Propósito

Convertir cualquier entrada autorizada (pregunta, comando, corrección, error,
decisión, cambio de archivo) en un **evento estructurado** que el resto de AMPA
pueda interpretar, recuperar y auditar (Concepto Maestro §5 y §7).

## 2. Responsabilidad exacta

**Hace:**
- Clasifica el dominio (química / filosofía / general / documentación / operación).
- Infiere el tipo de evento cuando no se indica.
- Detecta archivos relacionados mencionados en el texto.
- Evalúa el **riesgo operativo** (bajo / medio / alto).
- Decide si el evento debe **guardarse en memoria** (evita ruido, §6.2).
- Produce un `Evento` conforme al contrato §5.2.
- Persiste en un **diario** (JSONL) los eventos marcados para guardar (`journal`).

**No hace:**
- No ejecuta acciones ni escribe archivos (eso lo hace el módulo `scribe`).
- No accede a memoria ni al modelo; solo **estructura** la entrada.
- No usa ML todavía (clasificador por reglas; ver ADR 0008).

## 3. Entradas

- `texto` (str): la entrada del usuario o un evento del sistema.
- `tipo` (opcional): fuerza el tipo de evento; si no, se infiere.
- `archivos` (opcional): rutas relacionadas ya conocidas.

## 4. Salidas

- `Evento` (dataclass) con los ocho campos del contrato §5.2; serializable a
  `dict` (`to_dict`) y a YAML (`as_yaml`).

## 5. Flujo interno

1. Normaliza el texto (minúsculas, sin acentos).
2. Clasifica dominio + términos encontrados.
3. Infiere el tipo si no se indicó.
4. Detecta archivos (argumento + expresión regular).
5. Evalúa el riesgo operativo.
6. Decide `guardar_en_memoria`.
7. Construye intención y justificación.

## 6. Decisiones de diseño

- **Clasificador por reglas antes que ML** (ADR 0008): explicable, sin
  dependencias y base de comparación para la futura red neuronal.
- **Normalización sin acentos** para robustez en español.
- **Solo biblioteca estándar** (portabilidad, ADR 0007).

## 7. Errores esperados

- Texto vacío → dominio `general`, tipo `pregunta`, riesgo `bajo` (no falla).
- `tipo` desconocido recibido del usuario → se ignora y se infiere.

## 8. Seguridad y límites

- **No actúa: solo describe.** El `riesgo_operativo` es una señal para que el
  orquestador o el `scribe` pidan confirmación antes de escribir.
- No percibe nada fuera de lo que se le pasa explícitamente (§5.1).

## 9. Pruebas mínimas

- `tests/test_perception.py` (13 casos): dominios, equivalencia sin acentos, tipo,
  riesgo, detección de archivos, política de memoria y serialización YAML.
- Ejecutar: `python -m unittest discover -s tests -t .`

## 10. Cambios pendientes

- Reemplazar/complementar el clasificador por la red neuronal (Pista B).
- Ampliar los léxicos de dominio.
- La memoria documental (Fase 3) consumirá el diario de eventos como entrada.

> **Hecho:** el **diario de eventos** (`journal.py`) ya persiste en JSONL los eventos
> marcados para guardar, y `ampa diario` los lista. Cubre el pendiente de «logs» de
> la Fase 2.
