# Módulo: core (núcleo portable)

> Documentado según la plantilla del Concepto Maestro §12.
> Código: `ampa/core/` · Pruebas: `tests/test_platform_info.py`, `tests/test_paths.py`

## 1. Propósito

Proveer la base **portable** sobre la que se apoya todo AMPA: detección de sistema
operativo y resolución de las rutas estándar del proyecto, comportándose igual en
Windows, Linux y macOS.

## 2. Responsabilidad exacta

**Hace:**
- Normaliza el SO a `windows` / `linux` / `macos` / `unknown`.
- Resuelve la carpeta base de AMPA y sus subcarpetas (`data`, `models`, `config`,
  `cache`, `backups`, `logs`, `memory`) usando `pathlib`.
- Crea esas carpetas de forma idempotente.

**No hace:**
- No lee ni escribe configuración del usuario (será otro módulo).
- No accede a la red.
- No depende de bibliotecas externas.

## 3. Entradas

- `system` (opcional): nombre del SO, inyectable para pruebas.
- `env` (opcional): mapa de variables de entorno, inyectable para pruebas.
- Variable de entorno `AMPA_HOME`: si existe, fuerza la ubicación base.

## 4. Salidas

- Cadena normalizada de SO (`platform_info.normalize_system`).
- Objeto `Paths` con rutas `pathlib.Path` (`paths.get_paths`).
- Carpetas creadas en disco al invocar `Paths.create()`.

## 5. Flujo interno

1. `normalize_system()` interpreta el SO (real o inyectado).
2. `resolve_home()` aplica prioridad: `AMPA_HOME` > convención por SO.
3. `Paths` deriva las subcarpetas a partir de `home`.
4. `Paths.create()` crea las carpetas (`mkdir(parents=True, exist_ok=True)`).

## 6. Decisiones de diseño

- **Solo biblioteca estándar** para garantizar portabilidad (ver ADR 0007).
- `system` y `env` **inyectables**: permiten probar Windows y macOS desde Linux.
- `pathlib` en todas partes; nunca cadenas con separadores `/` o `\`.
- `Paths` inmutable (`dataclass(frozen=True)`): las subrutas derivan de `home`.

## 7. Errores esperados

- `AMPA_HOME` con ruta inválida → `create()` lanzará `OSError` (se propaga a la
  capa superior, que decidirá cómo informarlo).
- SO no reconocido → `unknown`; se aplica la convención tipo Linux/XDG.

## 8. Seguridad y límites

- No escribe fuera de las carpetas resueltas.
- `create()` es idempotente y **no borra** nada.

## 9. Pruebas mínimas

- 18 casos en `tests/`: los cuatro SO, el override `AMPA_HOME`, las subcarpetas y la
  creación idempotente.
- Ejecutar: `python -m unittest discover -s tests -t .`

## 10. Cambios pendientes

- Módulo de configuración (`config`) apoyado en estas rutas.
- Registro (`logging`) portable.
- Integración con el módulo `scribe` (escritura segura + backups).
