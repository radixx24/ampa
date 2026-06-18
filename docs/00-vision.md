# 00 — Visión

> Para la visión unificada y completa, ver [`concepto-maestro.md`](concepto-maestro.md).
> Este documento desarrolla el "porqué" y los principios.

## El problema

Los grandes modelos de lenguaje (LLM) comerciales son potentes, pero:

- Viven en la nube y **no son privados**.
- **No aprenden** de ti de forma persistente: olvidan lo que les enseñas.
- Son cajas cerradas: no sabes qué saben ni de dónde lo sacan.
- Requieren hardware caro o suscripciones.

## La idea

**AMPA** es un asistente que corre **en tu propia máquina** (CPU, 16 GB de RAM) y
que tiene estas cualidades centrales:

1. **Aprende de tus apuntes.** ~90% de su conocimiento útil viene de **tu propia
   investigación**: notas, documentos y archivos que tú produces.
2. **Tiene un cimiento curado.** ~10% es una base de fuentes abiertas y confiables de
   **química** y **filosofía**, para no partir de cero.
3. **Recuerda y evoluciona.** Una **memoria dinámica persistente** conserva y prioriza
   lo aprendido entre sesiones.

## Los dominios

- **Ciencia con eje en la química:** estructura de la materia, reacciones,
  nomenclatura, termodinámica.
- **Filosofía:** filosofía de la ciencia, epistemología, lógica y ética — la lente
  para preguntarse *"¿cómo sabemos esto?"*.

## Qué NO es (para evitar malentendidos)

- **No es un LLM entrenado desde cero.** Usa un modelo base pequeño ya entrenado y
  construye *alrededor* de él.
- **No es una autoridad infalible.** Puede equivocarse; por eso cita fuentes y, ante
  la duda, dice *"no lo sé"*.
- **No es mágico.** Un modelo pequeño tiene límites; se compensan con recuperación
  (RAG) y buen diseño, no fingiendo que no existen.

## Principios de diseño

1. **Local primero.** Todo corre sin nube. La privacidad es un requisito.
2. **Hardware modesto.** Si no corre con CPU y 16 GB, no entra en el diseño base.
3. **Aprendizaje real.** Mañana responde mejor por lo que le enseñaste hoy.
4. **Honestidad epistémica.** Distingue lo que sabe de su base, lo aprendido de ti,
   y lo que **no** sabe.
5. **Reproducibilidad.** Todo lo aleatorio es **semillable**: ciencia, no azar ciego.
6. **Seguridad al escribir.** Nada se modifica sin backup y registro.
7. **Documentar mientras se construye.** Cada decisión deja un ADR.
8. **Comprender, no solo usar.** La pista de "red neuronal desde cero" existe para
   entender de verdad lo que hay debajo.

## Qué hace a AMPA distinto (dónde está "lo nuevo")

1. **Ciclo de aprendizaje continuo.** Conviven memoria de sesión, de largo plazo
   (RAG con tus apuntes) y paramétrica (LoRA, opcional y futura).
2. **Capa epistémica / de confianza.** Marca el origen de cada afirmación: *de mi
   base / me lo enseñaste tú / no lo sé*.
3. **Razonamiento ciencia + filosofía.** Filosofía de la ciencia aplicada a la
   química: el *qué* del mundo material y el *cómo lo sabemos*.
4. **Dinamismo reproducible.** Simulaciones aleatorias con semilla fija.

## Para quién

- Para ti, como autor y científico de corazón, que quieres entender y construir algo
  propio que crezca con tu investigación.
- Para quien quiera un asistente privado de estudio en química y filosofía, con
  conciencia clara de sus límites.

## Cómo medimos el éxito (primeras señales)

- ✅ El modelo base responde por CPU a una velocidad usable (varios tokens/segundo).
- ✅ Ingieres tus apuntes y AMPA responde con ellos, citándolos.
- ✅ Le enseñas algo hoy y en la siguiente sesión lo recuerda y lo usa.
- ✅ Con la misma semilla, una simulación aleatoria se reproduce idéntica.
- ✅ Sabe decir "no lo sé" en lugar de inventar.
