# ADR 0003 — Dos pistas de desarrollo en paralelo

- **Estado:** Aceptado
- **Fecha:** 2026-06-18

## Contexto

El proyecto tiene dos objetivos que podrían parecer separados:

1. Construir un **asistente usable** (LLM + RAG).
2. Construir una **red neuronal simplificada desde cero** en Python y C++, para
   aprender patrones y entender los fundamentos.

Hay que decidir si hacerlos en serie (uno y luego el otro) o en paralelo.

## Decisión

Desarrollar **ambas pistas en paralelo**, y hacer que **se encuentren** en un punto
útil: la red neuronal desde cero será el **clasificador de dominio** del sistema
(¿la pregunta es de medicina, psicología o filosofía?).

- **Pista 1 — El sistema AMPA:** motor `llama.cpp` + modelo + RAG + CLI (`ampa/`).
- **Pista 2 — Red neuronal desde cero:** MLP en NumPy y en C++ (`nn/`).

## Alternativas

- **Solo el sistema RAG:** llegaríamos antes a algo usable, pero perderíamos el
  objetivo de aprendizaje profundo y el clasificador propio.
- **Solo la red desde cero:** muy educativo, pero sin un asistente que mostrar.
- **En serie:** retrasa uno de los dos objetivos innecesariamente.

## Consecuencias

- 👍 La red neuronal no es un juguete aislado: **cumple una función real**.
- 👍 Avanzamos en el objetivo práctico y en el educativo a la vez.
- 👍 Entender la NN desde cero hace menos "mágico" al LLM grande.
- 👎 Más frentes abiertos; exige disciplina en la documentación y el roadmap para no
  dispersarse.
