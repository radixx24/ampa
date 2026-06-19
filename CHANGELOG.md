# Changelog

Todos los cambios notables del proyecto se documentan aquí.
Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
versionado según [SemVer](https://semver.org/lang/es/).

## [No publicado]

### Añadido
- **Capa de percepción** (`ampa/perception/`): contrato de evento (§5.2),
  clasificador de dominio por reglas, evaluación de riesgo y política de memoria.
- **Comando `ampa percibir`** y 13 pruebas; contrato `docs/contratos/evento.md`,
  módulo `docs/modulos/percepcion.md` y **ADR 0008**.
- **Núcleo portable** (`ampa/core/`): detección de plataforma (`platform_info.py`)
  y rutas multiplataforma (`paths.py`), solo con biblioteca estándar.
- **CLI portable** (`ampa/cli/`): comandos `info`, `version` y `paths`.
- **Pruebas** con `unittest` (18 casos): plataforma, rutas (Windows/macOS/Linux
  simulados) y CLI.
- **Base C++ portable** (`cpp/`): proyecto CMake y sonda `ampa-probe` con
  aleatoriedad reproducible (`std::mt19937_64`).
- `pyproject.toml`: empaquetado, *entry point* `ampa`, núcleo sin dependencias.
- Documento de módulo `docs/modulos/core.md` y **ADR 0007** (portabilidad).
- ADR 0004–0006 (dominios, apuntes/escriba, memoria/simulaciones), `CITATION.cff`.

### Cambiado
- **Concepto Maestro actualizado a v0.2**: ejes lenguaje/percepción/memoria, capa de
  percepción, ciclo percepción‑memoria‑acción, sistema de documentación controlada
  y regla final de control.
- Dominios del proyecto: a **química** (eje científico) y **filosofía** (lente).
- Visión, arquitectura, roadmap, glosario y base de conocimiento alineados.

## [0.0.1] - 2026-06-18

### Añadido
- Fundación de documentación: visión, arquitectura, ADRs 0001–0003, roadmap,
  glosario y base de conocimiento.
- `.gitignore` para modelos, datos y artefactos de compilación.
