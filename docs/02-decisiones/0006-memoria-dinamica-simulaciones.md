# ADR 0006 — Memoria dinámica persistente y motor de simulaciones aleatorias

- **Estado:** Aceptado
- **Fecha:** 2026-06-18

## Contexto

El autor quiere que AMPA (1) **persista** lo aprendido entre prompts y sesiones con
una **memoria dinámica**, y (2) genere respuestas **más dinámicas** mediante
**simulaciones aleatorias**.

## Decisión

### Memoria dinámica persistente
- La memoria (índice vectorial + estado + hechos) se **guarda en disco** y se recarga
  en cada arranque.
- Es **dinámica**: pondera por **relevancia** y **recencia**, puede archivar lo poco
  usado y reforzar lo recurrente.
- Se respalda junto con los backups del sistema.

### Motor de dinamismo (simulaciones aleatorias)
- **Decodificación estocástica controlada** (temperatura, top-p).
- **Muestreo tipo Monte Carlo:** varias respuestas candidatas + auto-consistencia.
- **Escenarios/ejemplos aleatorios** para ciencia (moléculas, reacciones, problemas).
- **Semilla reproducible:** todo el azar es re-ejecutable de forma idéntica.

## Alternativas

- **Memoria estática (solo lectura):** simple, pero no "vive" ni prioriza; no cumple
  el requisito de dinamismo.
- **Aleatoriedad sin semilla:** rompe la reproducibilidad, inaceptable para un
  proyecto con vocación científica.
- **Temperatura fija alta:** da variedad pero también incoherencia; mejor un motor
  que **module** la aleatoriedad según el caso.

## Consecuencias

- 👍 Lo aprendido perdura y se prioriza con criterio.
- 👍 Respuestas variadas y exploratorias, sin perder rigor.
- 👍 Reproducibilidad científica garantizada por semilla.
- 👎 Mayor complejidad en la capa de generación y de memoria.
- ➡️ Introduce los módulos `memory/` (persistencia dinámica) y `dynamism/` (motor
  estocástico).
