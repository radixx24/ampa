# 01 — Arquitectura

> Visión técnica de las piezas de AMPA y cómo encajan. Pensada para CPU + 16 GB RAM.

## Las cinco piezas

| # | Pieza | Tecnología | Rol | RAM aprox. |
|---|---|---|---|---|
| 1 | **Motor de inferencia** | `llama.cpp` (**C++**) | Ejecuta el modelo en CPU (GGUF, AVX2) | — |
| 2 | **Modelo base** | LLM 3B cuantizado Q4 | El "cerebro" pre-entrenado | 3–4 GB |
| 3 | **Base de conocimientos** | Vector DB + embeddings | Memoria de largo plazo (RAG) | <1 GB |
| 4 | **Orquestación** | **Python** | El pegamento: ingesta, recuperación, prompts | — |
| 5 | **Red neuronal propia** | NumPy + **C++** | Clasificador de dominio / re-ranker + módulo educativo | mínima |

Con un modelo 3B en Q4 (~3–4 GB) más embeddings y vector DB, el consumo total queda
holgado por debajo de los 16 GB.

## Diagrama de alto nivel

```
                            ┌──────────────────────────┐
        Tú  ───pregunta───► │      Interfaz (CLI)       │
                            └────────────┬─────────────┘
                                         │
                                         ▼
                            ┌──────────────────────────┐
                            │   Orquestador (Python)    │
                            │  ┌────────────────────┐   │
                            │  │ 5. Clasificador de │   │  ¿medicina? ¿psicología?
                            │  │  dominio (NN)      │   │  ¿filosofía?
                            │  └─────────┬──────────┘   │
                            └────────────┼─────────────┘
                                         │
                  ┌──────────────────────┼──────────────────────┐
                  ▼                       ▼                       ▼
        ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
        │ 3. Base de       │   │  Memoria de       │   │ 1+2. Motor +     │
        │  conocimientos   │   │  sesión / largo   │   │  modelo base     │
        │  (RAG vectorial) │   │  plazo            │   │  (llama.cpp, C++)│
        └────────┬─────────┘   └────────┬──────────┘   └────────▲─────────┘
                 │  fragmentos relevantes │                      │
                 └───────────┬────────────┘                      │
                             ▼                                   │
                   ┌──────────────────┐    prompt + contexto     │
                   │  Constructor de  │ ─────────────────────────┘
                   │  prompt + fuentes│
                   └──────────────────┘
                             │
                             ▼
                      respuesta + citas
```

## Flujo de una consulta (paso a paso)

1. Escribes una pregunta en la CLI.
2. El **clasificador de dominio** (nuestra red neuronal) decide si es de medicina,
   psicología, filosofía o general.
3. Se generan **embeddings** de la pregunta y se buscan los fragmentos más
   relevantes en la **base de conocimientos** y en la **memoria** de lo que le
   enseñaste.
4. El orquestador arma un **prompt** que incluye la pregunta + esos fragmentos +
   las instrucciones del sistema.
5. El **motor (llama.cpp)** ejecuta el modelo y genera la respuesta.
6. Se devuelve la respuesta **con sus fuentes** y una marca de confianza.

## Las dos pistas de desarrollo

### Pista 1 — El sistema AMPA (asistente usable)
Piezas 1–4. Es lo que conviertes en algo que se usa: motor + modelo + RAG + CLI.

### Pista 2 — Red neuronal desde cero (educativa + práctica)
Pieza 5. Un MLP implementado **dos veces** —en Python (NumPy) y en C++— para:
- **Entender** de verdad forward pass, backpropagation y descenso de gradiente.
- **Servir** como clasificador de dominio real del sistema (no es un juguete aparte).

Las dos pistas avanzan en paralelo y se encuentran en el clasificador de dominio.

## Stack tecnológico (propuesto)

| Capa | Opción elegida | Alternativas consideradas |
|---|---|---|
| Inferencia | `llama.cpp` + `llama-cpp-python` | `ctransformers`, `ollama` |
| Modelo base | Qwen2.5-3B / Llama-3.2-3B (Q4_K_M) | Phi-3.5-mini, Gemma-2-2B |
| Embeddings | multilingüe (e5 / bge-m3) | MiniLM (solo si va en inglés) |
| Vector DB | `sqlite-vec` o ChromaDB | FAISS, Qdrant embebido |
| Orquestación | Python estándar | LangChain, LlamaIndex |
| NN desde cero | NumPy + C++ (sin libs externas) | PyTorch (solo de referencia) |

> Las elecciones definitivas se registran como ADR en `02-decisiones/`.

## Estructura del repositorio (propuesta)

```
ampa/
├── README.md
├── docs/                       ← toda la documentación
│   ├── 00-vision.md
│   ├── 01-arquitectura.md
│   ├── 02-decisiones/          ← ADRs
│   ├── 03-roadmap.md
│   ├── 04-glosario.md
│   └── 05-base-conocimiento.md
├── ampa/                       ← PISTA 1: el sistema (paquete Python)
│   ├── engine/                 ← wrapper sobre llama.cpp
│   ├── knowledge/              ← ingesta, troceado, embeddings, vector store
│   ├── memory/                 ← memoria de sesión + largo plazo (+ ganchos LoRA)
│   ├── domains/                ← uso del clasificador de dominio
│   └── cli/                    ← interfaz de línea de comandos
├── nn/                         ← PISTA 2: red neuronal desde cero
│   ├── python/                 ← MLP en NumPy (forward/backprop)
│   └── cpp/                    ← el mismo MLP en C++
├── models/                     ← modelos GGUF descargados (no se versionan)
└── data/                       ← corpus y base vectorial (no se versionan)
```

> Las carpetas de código se crearán al iniciar cada módulo, documentando el porqué.
