# ADR 0004 — Cambio de dominios: química y filosofía

- **Estado:** Aceptado
- **Fecha:** 2026-06-18
- **Reemplaza parcialmente a:** el alcance de dominios previo (medicina, psicología,
  filosofía)

## Contexto

El proyecto nació apuntando a tres dominios: medicina, psicología y filosofía. El
autor decide reorientar el foco hacia su pasión por la ciencia, en concreto la
**química**, manteniendo la **filosofía** como lente de razonamiento.

## Decisión

Los dominios de AMPA pasan a ser:

1. **Ciencia con eje en la química** (sustituye a medicina y psicología).
2. **Filosofía** (se mantiene), con énfasis en **filosofía de la ciencia**,
   epistemología, lógica y ética.

El clasificador de dominio se reentrena para enrutar a **química / filosofía /
general**.

## Alternativas

- **Mantener medicina y psicología:** implican gobernanza de datos sensible (datos
  clínicos, salud mental, riesgo en crisis) y disclaimers fuertes. Química y
  filosofía son más afines al autor y de menor riesgo.
- **Abarcar todas las ciencias por igual:** demasiado amplio para empezar; la química
  como "ciencia central" da un eje concreto y conectado.

## Consecuencias

- 👍 Menor carga ética/regulatoria que el ámbito clínico.
- 👍 Combinación distintiva: **filosofía de la ciencia aplicada**.
- 👍 Alineado con la motivación real del autor ("amo la ciencia").
- 👎 Hay que rehacer la curación de corpus y el conjunto de prueba del clasificador.
- ➡️ Se actualizan `00-vision.md`, `01-arquitectura.md` y `05-base-conocimiento.md`.
