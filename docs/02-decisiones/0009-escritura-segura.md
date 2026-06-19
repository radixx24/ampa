# ADR-0009: Escritura segura — atómica, con respaldo y bloqueo por riesgo

> Formato según Concepto Maestro §13.

## Estado

Aceptada

## Contexto

El Escriba (Fase 5) debe aplicar cambios en archivos del usuario (apuntes,
documentación) de forma fiable y multiplataforma. ADR 0005 ya fijó que la
escritura va **con respaldos**; falta decidir *cómo* escribir para no corromper
datos y *cómo* gobernar el riesgo que emite la percepción (§6.2).

## Opciones consideradas

- **A. Escritura directa** (`open(...).write`): simple, pero puede dejar el
  archivo a medias si el proceso falla a mitad.
- **B. Escritura atómica**: escribir en un temporal de la misma carpeta y
  reemplazar con `os.replace`; respaldo previo en `Paths.backups`.
- **C. Control de versiones externo** (p. ej. git por cada cambio): potente pero
  pesado, con dependencias y fuera del alcance portable.

## Decisión

**Opción B.** Escritura atómica (`tempfile` + `os.fsync` + `os.replace`) con
**respaldo con marca de tiempo** antes de sobrescribir y opción de **restaurar**.
La escritura se **bloquea** si `riesgo_operativo == alto`, salvo autorización
explícita (`forzar` / `--forzar`). Un **modo simulación** describe la acción sin
tocar disco. Solo biblioteca estándar (ADR 0007).

## Alternativas

Se descartó **A** por el riesgo de dejar archivos corruptos, y **C** por su peso
y dependencias, incompatibles con el núcleo portable.

## Consecuencias

- 👍 Cambios fiables, reversibles y auditables (`ResultadoEscritura`); sin dependencias.
- 👎 Los respaldos crecen con el tiempo (pendiente: política de retención/poda).
- ➡️ La futura **bitácora de cambios** consolidará los resultados de escritura.
