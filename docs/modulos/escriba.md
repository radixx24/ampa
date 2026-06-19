# Módulo: scribe (Escriba seguro)

> Documentado según la plantilla del Concepto Maestro §12.
> Código: `ampa/scribe/` · Pruebas: `tests/test_scribe.py` · Decisiones: ADR 0005 y 0009

## 1. Propósito

Aplicar en disco, de forma **segura y reversible**, los cambios que AMPA decide
hacer sobre archivos (corregir apuntes, escribir documentación), respetando la
señal de **riesgo operativo** que emite la percepción (Concepto Maestro §6 y §7).

## 2. Responsabilidad exacta

**Hace:**
- Escribe archivos de forma **multiplataforma** (`pathlib`) y **atómica**
  (temporal + `os.replace`): nunca deja un archivo a medias.
- Crea un **respaldo con marca de tiempo** antes de sobrescribir (`Paths.backups`).
- Permite **restaurar** un archivo desde su respaldo (rollback).
- **Bloquea** la escritura cuando el `riesgo_operativo` es `alto`, salvo
  autorización explícita (`forzar=True`).
- Ofrece **modo simulación** (`simular=True`): describe la acción sin tocar disco.

**No hace:**
- No decide *qué* escribir ni *por qué* (viene de la memoria/orquestación).
- No evalúa el riesgo: lo **recibe** de la percepción (§6.2).
- No usa dependencias externas (portabilidad, ADR 0007).

## 3. Entradas

- `ruta` (str | Path): archivo destino.
- `contenido` (str): texto a escribir.
- `riesgo` (str): `bajo` | `medio` | `alto`; `alto` bloquea salvo `forzar`.
- Banderas: `simular`, `forzar`, `respaldar`, `codificacion`, `paths`.

## 4. Salidas

- `ResultadoEscritura` (dataclass, **auditable**): `escrito` / `simulado` /
  `bloqueado`, `respaldo`, `bytes_escritos` y `motivo`; con `resumen()` legible.

## 5. Flujo interno

1. Si `riesgo == alto` y no hay `forzar` → **bloqueado** (no toca nada).
2. Si `simular` → describe la acción (incl. respaldo previsto) y termina.
3. Si el archivo existe y `respaldar` → copia a `backups/` con marca de tiempo única.
4. Crea las carpetas necesarias y escribe en un archivo **temporal**.
5. `os.fsync` + `os.replace`: reemplazo **atómico** del destino.

## 6. Decisiones de diseño

- **Escritura atómica** (`os.replace`) para no corromper archivos ante fallos
  (ADR 0009).
- **Respaldo antes de sobrescribir** y rollback (ADR 0005).
- **El riesgo manda**: `alto` exige autorización explícita; percepción y escriba
  quedan desacoplados pero coordinados por esa señal.
- **Solo biblioteca estándar** (ADR 0007).

## 7. Errores esperados

- Carpeta destino inexistente → se crea (`mkdir parents`).
- Fallo durante la escritura → se elimina el temporal; el destino queda intacto.
- `restaurar` sin respaldos → `ResultadoEscritura` sin cambios, con motivo claro.

## 8. Seguridad y límites

- **Reversible por diseño**: sobrescribir siempre deja respaldo (salvo `--sin-respaldo`).
- **Puerta de riesgo**: el `alto` no se escribe «por accidente»; requiere `--forzar`.
- El escriba solo toca las rutas que se le indican explícitamente.

## 9. Pruebas mínimas

- `tests/test_scribe.py` (8 casos): creación, respaldo y rollback, simulación,
  bloqueo por riesgo, `forzar`, `sin-respaldo` y orden de respaldos.
- Ejecutar: `python -m unittest discover -s tests -t .`

## 10. Cambios pendientes

- **Bitácora de cambios** consolidada (los `ResultadoEscritura` ya son auditables).
- Política de retención/poda de respaldos antiguos.
- Escritura guiada directamente por un `Evento` (tomar el `riesgo` del evento).
