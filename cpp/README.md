# Componente C++ de AMPA

Esta carpeta alberga la **pista de C++** del proyecto: a futuro, el envoltorio del
motor de inferencia (`llama.cpp`) y la red neuronal desde cero. Por ahora contiene
la **base portable**: una sonda que valida que el entorno C++ compila y corre en
cualquier sistema.

## Por qué CMake

CMake es el estándar para construir C++ de forma **portable** (Windows, Linux,
macOS) con distintos compiladores (g++, clang, MSVC). El mismo `CMakeLists.txt`
funciona en todas partes.

## Compilar y ejecutar (portable)

```sh
cmake -S . -B build
cmake --build build
./build/ampa-probe          # en Windows: build\Debug\ampa-probe.exe
```

La sonda imprime el sistema operativo detectado y un número aleatorio **reproducible**
a partir de una semilla. Con la misma semilla, el valor es idéntico en cualquier SO:

```sh
./build/ampa-probe 123      # pasa una semilla concreta
```
