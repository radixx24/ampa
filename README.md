# AMPA

**AMPA — Aprendizaje Multidominio con Patrones Adaptativos**

> Un asistente local que combina una **base de conocimientos propia** (medicina,
> psicología y filosofía) con la capacidad de **aprender de lo que tú le enseñas**.
> Pensado para correr en **CPU con 16 GB de RAM**, sin GPU ni nube.

> ℹ️ *El nombre "AMPA" es una propuesta de significado. Si para ti significa otra
> cosa, lo ajustamos sin problema.*

---

## Estado del proyecto

🚧 **Fase 0 — Fundación.** Definiendo visión, arquitectura y documentación.
Todavía no hay código ejecutable; estamos construyendo la idea sobre bases sólidas.

## La idea en una frase

No entrenamos un LLM desde cero (eso requiere GPUs y mucho dinero). Construimos un
**sistema** alrededor de un modelo base pequeño que: **(1)** ya sabe de medicina,
psicología y filosofía gracias a una base de conocimientos curada, y **(2)
aprende** de cada cosa que le enseñas, desde el primer día.

## Qué es y qué no es

| AMPA **es** | AMPA **no es** |
|---|---|
| Un asistente local que aprende de ti | Un GPT entrenado desde cero |
| Apoyo educativo y de razonamiento | Consejo médico ni diagnóstico clínico |
| Privado: corre en tu máquina | Un servicio en la nube |
| Multidominio (medicina, psicología, filosofía) | Un sustituto de un profesional |

## Requisitos objetivo

- **CPU** x86-64 con AVX2 (la mayoría de procesadores desde ~2015)
- **16 GB de RAM**
- **Sin GPU obligatoria**
- Linux / Windows / macOS

## Dos pistas de desarrollo (en paralelo)

1. **El sistema AMPA** — motor de inferencia en **C++** (`llama.cpp`) + orquestación
   **RAG** en **Python**. Es el asistente usable.
2. **Red neuronal desde cero** — un MLP en **Python (NumPy)** y su espejo en **C++**,
   con fines educativos y como **clasificador de dominio** real del sistema.

## Documentación

| Documento | Contenido |
|---|---|
| [`docs/00-vision.md`](docs/00-vision.md) | El porqué, principios y qué hace nuevo a AMPA |
| [`docs/01-arquitectura.md`](docs/01-arquitectura.md) | Las piezas, el flujo y la estructura del repo |
| [`docs/02-decisiones/`](docs/02-decisiones/) | Registros de decisión (ADR) |
| [`docs/03-roadmap.md`](docs/03-roadmap.md) | Fases e hitos |
| [`docs/04-glosario.md`](docs/04-glosario.md) | Términos en lenguaje claro |
| [`docs/05-base-conocimiento.md`](docs/05-base-conocimiento.md) | Fuentes, licencias y ética |

## Aviso importante

AMPA es una herramienta **educativa y de apoyo**. **No sustituye** a un profesional
de la salud, la salud mental ni a cualquier otro especialista. Ver
[`docs/05-base-conocimiento.md`](docs/05-base-conocimiento.md) para el detalle ético.
