# Base portable del componente C++ de AMPA.
# CMake es la herramienta estándar para construir C++ de forma portable
# (Windows, Linux, macOS) con distintos compiladores (g++, clang, MSVC).
cmake_minimum_required(VERSION 3.16)
project(ampa_cpp LANGUAGES CXX)

# C++17 estándar puro (sin extensiones del compilador) = más portable.
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Sonda de portabilidad: detecta el SO y demuestra aleatoriedad reproducible.
add_executable(ampa-probe src/platform_probe.cpp)
