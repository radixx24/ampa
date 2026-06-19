# ADR-0007: Portabilidad del núcleo (stdlib, pathlib, pyproject, CMake)

> Formato según Concepto Maestro §13.

## Estado

Aceptada

## Contexto

AMPA debe correr igual en Windows, Linux y macOS, en CPU modesta y sin fricción de
instalación. La portabilidad es una prioridad explícita del proyecto. La primera
línea de código ya debe respetarla.

## Opciones consideradas

- **A. Núcleo con dependencias** (p. ej. `platformdirs`, `click`): cómodo, pero
  añade instalación y posibles puntos de fallo en cada máquina.
- **B. Núcleo solo con biblioteca estándar**: cero dependencias, máxima
  portabilidad, algo más de código propio.
- **C. Rutas con cadenas y `os.path`**: frágil entre sistemas (separadores,
  mayúsculas, expansión de `~`).

## Decisión

**Opción B.** El núcleo (`ampa.core`) usa solo biblioteca estándar:

- Rutas con `pathlib.Path`; ubicación base por convención de SO + override
  `AMPA_HOME`.
- CLI con `argparse`.
- Pruebas con `unittest` (sin instalar nada).
- Empaquetado con `pyproject.toml` (setuptools).
- C++ con **CMake** y C++17 estándar puro; aleatoriedad reproducible con
  `std::mt19937_64`.

## Justificación

Cero dependencias significa que corre en cualquier máquina con Python 3.9+ y, en
C++, con g++, clang o MSVC. La **inyección** de `system` y `env` permite probar los
tres sistemas operativos desde uno solo. `pathlib` elimina los errores clásicos de
separadores de ruta. CMake es el estándar portable para C++.

## Consecuencias

- 👍 Instalación trivial; pruebas sin red; comportamiento idéntico entre SO.
- 👍 Verificado: 18 pruebas pasan; la sonda C++ compila y es reproducible.
- 👎 Algunas comodidades (p. ej. directorios estándar) hay que implementarlas a
  mano en lugar de usar una librería.
- ➡️ Deuda: revisar rutas largas en Windows y permisos por SO cuando crezca el
  módulo `scribe`.
