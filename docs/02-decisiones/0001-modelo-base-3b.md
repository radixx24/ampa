# ADR 0001 — Modelo base de ~3B parámetros, cuantizado

- **Estado:** Aceptado
- **Fecha:** 2026-06-18

## Contexto

AMPA debe correr en **CPU con 16 GB de RAM**, sin GPU. El modelo base es la pieza
que más recursos consume. Hay que elegir un tamaño que equilibre **capacidad** y
**velocidad** en hardware modesto.

Referencias de consumo y velocidad (CPU de 4 núcleos, cuantización Q4_K_M):

| Tamaño | RAM en runtime | Velocidad aprox. | Calidad |
|---|---|---|---|
| 3B | ~3–4 GB | ~8–15 tokens/s | Buena para su tamaño |
| 7–8B | ~6–7 GB | ~3–6 tokens/s | Mejor razonamiento |

## Decisión

Usar un **modelo base pequeño de 1.7B–3B parámetros cuantizado a Q4**, ejecutado con
`llama.cpp`. Candidatos: SmolLM2-1.7B, Granite-3.3-2B, Qwen2.5-3B, Phi-3-mini
(todos con licencias permisivas y verificados en el informe de investigación).

El sistema se diseñará para que **cambiar de modelo sea trivial** (la ruta del GGUF
es configuración, no código), de modo que migrar a 7–8B más adelante sea solo
descargar otro archivo.

## Alternativas

- **Modelo 7–8B:** más capaz, pero ~2–3× más lento en CPU. Lo dejamos como opción de
  configuración, no como base.
- **Modelo <2B (1B, etc.):** muy rápido, pero la calidad cae demasiado para
  razonamiento multidominio.
- **Entrenar desde cero:** inviable con este hardware.

## Consecuencias

- 👍 Respuestas fluidas en CPU, experiencia interactiva.
- 👍 Margen de RAM amplio para RAG, embeddings y memoria.
- 👍 Posibilidad de subir a 7–8B sin reescribir nada.
- 👎 Menos capacidad de razonamiento que un modelo grande; se compensa con RAG y
  buen diseño de prompts.
