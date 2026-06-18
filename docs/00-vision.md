# 00 — Visión

## El problema

Los grandes modelos de lenguaje (LLM) comerciales son potentes, pero:

- Viven en la nube y **no son privados**.
- **No aprenden** de ti de forma persistente: olvidan lo que les enseñas.
- Son cajas cerradas: no sabes qué saben ni de dónde lo sacan.
- Requieren hardware caro o suscripciones.

## La idea

**AMPA** es un asistente que corre **en tu propia máquina** (CPU, 16 GB de RAM) y
que tiene dos cualidades centrales:

1. **Una base de conocimientos propia.** Desde el primer arranque sabe de
   **medicina**, **psicología** y **filosofía**, porque le cargamos corpus curados
   de fuentes abiertas.
2. **Aprende de lo que le enseñas.** Cada documento, nota o conversación que le das
   pasa a formar parte de su memoria y lo usa en respuestas futuras.

## Qué NO es (para evitar malentendidos)

- **No es un LLM entrenado desde cero.** Eso requiere miles de GPUs. AMPA usa un
  modelo base pequeño y ya entrenado, y construye *alrededor* de él.
- **No da consejo médico.** Es apoyo educativo y de razonamiento. Cualquier tema de
  salud debe validarse con un profesional. (Ver `05-base-conocimiento.md`.)
- **No es mágico.** Un modelo de 3B parámetros tiene límites; los compensamos con
  recuperación de conocimiento (RAG) y buen diseño, no fingiendo que no existen.

## Principios de diseño

1. **Local primero.** Todo corre sin nube. La privacidad es un requisito, no un extra.
2. **Hardware modesto.** Si no corre con CPU y 16 GB, no entra en el diseño base.
3. **Aprendizaje real.** "Aprender" significa que mañana responde mejor por lo que
   le enseñaste hoy.
4. **Honestidad epistémica.** El sistema distingue lo que sabe de su base, lo que
   aprendió de ti, y lo que **no** sabe.
5. **Documentar mientras se construye.** Cada decisión deja un registro (ADR).
6. **Comprender, no solo usar.** La pista de "red neuronal desde cero" existe para
   entender de verdad lo que hay debajo.

## Qué hace a AMPA distinto (dónde está "lo nuevo")

La mayoría de proyectos caseros se quedan en "un chatbot con RAG". AMPA apunta a
tres ideas poco explotadas:

1. **Ciclo de aprendizaje continuo.** Cómo conviven tres tipos de memoria:
   - de sesión (la conversación actual),
   - de largo plazo (RAG, vectorial),
   - paramétrica (LoRA, opcional y más adelante).
2. **Capa epistémica / de confianza.** Que el sistema marque el origen de cada
   afirmación: *"esto es de mi base"*, *"esto me lo enseñaste tú"*, *"esto no lo sé"*.
3. **Razonamiento multidominio.** Combinar medicina + psicología + filosofía para
   preguntas holísticas (por ejemplo, bioética o bienestar), no como tres silos
   separados.

## Para quién

- Para ti, como autor, que quieres entender y construir algo propio.
- Para usuarios que quieran un asistente privado de estudio y consulta en estos
  tres dominios, con la conciencia clara de sus límites.

## Cómo medimos el éxito (primeras señales)

- ✅ El modelo base responde por CPU a una velocidad usable (varios tokens/segundo).
- ✅ El sistema recupera de su base de conocimientos y cita la fuente.
- ✅ Le enseñas algo nuevo y en la siguiente sesión lo usa.
- ✅ Sabe decir "no lo sé" en lugar de inventar.
