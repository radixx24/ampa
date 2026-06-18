# AMPA

**AMPA — Aprendizaje Multidominio con Patrones Adaptativos**

> Un sistema de lenguaje **local, incremental y documentado** que corre en **CPU con
> 16 GB de RAM**. Aprende —sobre todo— de **tus propios apuntes de investigación**,
> con eje temático en **química** y **filosofía**. Sin GPU, sin nube.

> ℹ️ *El nombre "AMPA" es una propuesta de significado. Si para ti significa otra
> cosa, lo ajustamos.*

---

## Estado del proyecto

🚧 **Fase 0 — Fundación.** Definiendo visión, arquitectura y documentación.
Todavía no hay código ejecutable; estamos construyendo la idea sobre bases sólidas.

📄 **Punto de partida:** lee el [**Concepto Maestro**](docs/concepto-maestro.md), que
conjunta toda la visión del proyecto.

## La idea en una frase

No entrenamos un LLM desde cero (eso requiere GPUs y datos masivos). Construimos una
**arquitectura de conocimiento actualizable**: un modelo base pequeño rodeado de una
**memoria dinámica** que aprende de lo que tú investigas y escribes.

## Los dos dominios

- **Ciencia, con eje en la química** — la "ciencia central" de la materia.
- **Filosofía** — como lente epistemológica: *filosofía de la ciencia*, lógica, ética.

## Qué hace, en breve

- **Aprende de tus apuntes (90/10):** ~90% tu investigación, ~10% una base curada.
- **Memoria dinámica persistente:** recuerda entre sesiones; prioriza por relevancia
  y recencia.
- **Escriba multiplataforma + backups:** puede corregir documentación en Windows o
  Linux, siempre con copia de seguridad previa.
- **Simulaciones aleatorias reproducibles:** respuestas más dinámicas, con semilla
  fija para no perder rigor científico.
- **Citas y honestidad:** responde con fuentes y sabe decir *"no lo sé"*.

## Requisitos objetivo

- **CPU** x86-64 con AVX2 (la mayoría de procesadores desde ~2015)
- **16 GB de RAM** · **Sin GPU obligatoria**
- Linux / Windows / macOS

## Dos pistas de desarrollo (en paralelo)

1. **El sistema AMPA** — motor de inferencia en **C++** (`llama.cpp`) + orquestación
   **RAG** en **Python**, con memoria, escriba y motor de dinamismo.
2. **Red neuronal desde cero** — un MLP en **Python (NumPy)** y su espejo en **C++**,
   más un mini-tokenizer/transformer didáctico. Educa y sirve como **clasificador de
   dominio** del sistema.

## Documentación

| Documento | Contenido |
|---|---|
| [`docs/concepto-maestro.md`](docs/concepto-maestro.md) | **Visión unificada (empieza aquí)** |
| [`docs/00-vision.md`](docs/00-vision.md) | El porqué, principios y diferenciadores |
| [`docs/01-arquitectura.md`](docs/01-arquitectura.md) | Componentes, flujo y estructura |
| [`docs/02-decisiones/`](docs/02-decisiones/) | Registros de decisión (ADR) |
| [`docs/03-roadmap.md`](docs/03-roadmap.md) | Fases e hitos |
| [`docs/04-glosario.md`](docs/04-glosario.md) | Términos en lenguaje claro |
| [`docs/05-base-conocimiento.md`](docs/05-base-conocimiento.md) | Fuentes, licencias y ética |
| [`CHANGELOG.md`](CHANGELOG.md) | Historial de cambios |
| [`CITATION.cff`](CITATION.cff) | Cómo citar (solo autores humanos) |

## Aviso

AMPA es una herramienta **educativa y de investigación**. Sus respuestas pueden
contener errores; verifica siempre la información importante con fuentes primarias.
