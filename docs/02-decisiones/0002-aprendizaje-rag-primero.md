# ADR 0002 — Aprendizaje vía RAG primero, con ganchos para LoRA

- **Estado:** Aceptado
- **Fecha:** 2026-06-18

## Contexto

Uno de los pilares de AMPA es que **aprenda de lo que el usuario le enseña**. Hay
tres maneras de lograrlo, con costos muy distintos en CPU:

1. **Memoria RAG (vectorial):** lo aprendido se trocea, se convierte en vectores y
   se recupera al responder. Instantáneo, sin entrenamiento, sin GPU.
2. **Memoria estructurada / grafo:** extraer hechos y relaciones. Más complejo.
3. **Fine-tuning paramétrico (LoRA):** actualizar los pesos del modelo. Cambia el
   modelo "de verdad", pero es **lento en CPU**.

## Decisión

Implementar **primero el aprendizaje vía RAG** (opción 1) y **dejar los ganchos de
diseño preparados** para añadir LoRA (opción 3) más adelante, sin rehacer la
arquitectura.

En concreto, la capa de memoria expondrá una interfaz estable
(`recordar()`, `recuperar()`) de modo que añadir un "consolidador" que destile la
memoria en adaptadores LoRA sea una extensión, no una reescritura.

## Alternativas

- **Solo RAG, sin pensar en LoRA:** más simple, pero cerraría la puerta a
  aprendizaje paramétrico real.
- **LoRA desde el inicio:** lento de entrenar en CPU y prematuro; añade complejidad
  antes de tener el sistema básico funcionando.

## Consecuencias

- 👍 AMPA aprende **desde el día uno**, sin esperar entrenamientos.
- 👍 Cero coste de GPU para el aprendizaje cotidiano.
- 👍 La puerta a LoRA queda abierta por diseño.
- 👎 El conocimiento aprendido vive "fuera" del modelo (en la base vectorial), no en
  sus pesos —hasta que se implemente el consolidador LoRA.
