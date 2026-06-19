# 01 — Arquitectura

> Visión técnica de los componentes de AMPA y cómo encajan. Pensada para CPU + 16 GB
> RAM. Para el panorama unificado, ver [`concepto-maestro.md`](concepto-maestro.md).

## Componentes

| # | Componente | Tecnología | Rol |
|---|---|---|---|
| 1 | **Motor de inferencia** | `llama.cpp` (**C++**) | Ejecuta el modelo en CPU (GGUF, AVX2) |
| 2 | **Modelo base** | LLM 1.7B–3B cuantizado Q4 | El "cerebro" pre-entrenado |
| 3 | **Memoria dinámica** | Vector DB + embeddings | Aprende de tus apuntes (RAG); persiste y prioriza |
| 4 | **Escriba + backups** | Python (`pathlib`) | Corrige documentación en Win/Linux con respaldo |
| 5 | **Motor de dinamismo** | Python | Simulaciones aleatorias reproducibles |
| 6 | **Orquestación** | **Python** | El pegamento: ingesta, recuperación, prompts |
| 7 | **Red neuronal propia** | NumPy + **C++** | Clasificador de dominio + módulo educativo |

Con un modelo de 1.7B–3B en Q4 (~1–4 GB) más embeddings y vector DB, el consumo
total queda holgado por debajo de los 16 GB.

> **Nota de alineación.** El detalle conceptual de la **capa de percepción**, el
> **ciclo percepción‑memoria‑acción** y el **sistema de documentación controlada**
> vive en el documento rector [`concepto-maestro.md`](concepto-maestro.md) (§5–§15).
> Esta arquitectura se irá alineando módulo a módulo. El **núcleo portable**
> (`ampa/core/`) ya está implementado y probado.

## Diagrama de alto nivel

```
                         ┌───────────────────────────────┐
     Tú ───pregunta────► │          Interfaz (CLI)        │
     Tú ───apuntes─────► │                                │
                         └───────────────┬───────────────┘
                                         ▼
                         ┌───────────────────────────────┐
                         │      Orquestador (Python)      │
                         │  ┌──────────────┐  ┌─────────┐ │
                         │  │ Clasificador │  │ Motor de│ │
                         │  │ de dominio   │  │dinamismo│ │
                         │  │ (NN propia)  │  │ (azar)  │ │
                         │  └──────────────┘  └─────────┘ │
                         └───┬─────────┬─────────┬────────┘
                  ┌──────────┘         │         └──────────┐
                  ▼                    ▼                    ▼
        ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
        │ Memoria dinámica │ │  Escriba +       │ │ Motor + modelo   │
        │ persistente      │ │  Backups         │ │ base (llama.cpp, │
        │ (RAG: 90% tus    │ │ (corrige docs    │ │ C++)             │
        │ apuntes)         │ │  en Win/Linux)   │ │                  │
        └────────┬─────────┘ └──────────────────┘ └────────▲─────────┘
                 │  fragmentos citados + contexto           │
                 └──────────────────────┬───────────────────┘
                                        ▼
                       respuesta + fuentes + nivel de confianza
```

## Flujo de una consulta (paso a paso)

1. Escribes una pregunta (o ingieres apuntes nuevos) en la CLI.
2. La **capa de percepción** estructura la entrada (ver Concepto Maestro §5) y el
   **clasificador de dominio** la enruta: química, filosofía, general,
   documentación u operación técnica.
3. Se generan **embeddings** de la pregunta y se recuperan los fragmentos más
   relevantes de la **memoria dinámica** (tus apuntes + la base curada).
4. El **motor de dinamismo** decide cuánta variación aplicar (y con qué semilla).
5. El orquestador arma el **prompt**: pregunta + fragmentos + instrucciones.
6. El **motor (llama.cpp)** ejecuta el modelo y genera la respuesta.
7. Se devuelve la respuesta **con fuentes** y una **marca de confianza**.

## Las dos pistas de desarrollo

### Pista 1 — El sistema AMPA (asistente usable)
Componentes 1–6: motor + modelo + memoria + escriba + dinamismo + orquestación.

### Pista 2 — Red neuronal desde cero (educativa + práctica)
Componente 7: un MLP en NumPy y en C++, más un mini-tokenizer (SentencePiece) y un
mini-transformer didáctico. **Entiende** los fundamentos y **sirve** como clasificador
de dominio real del sistema.

## Stack tecnológico (alineado con la investigación)

| Capa | Elección | Alternativas / notas |
|---|---|---|
| Inferencia | `llama.cpp` + `llama-cpp-python` | ONNX Runtime GenAI |
| Modelo base | SmolLM2-1.7B · Granite-3.3-2B · Qwen2.5-3B · Phi-3-mini (Q4) | Licencias permisivas |
| Embeddings | `multilingual-e5-small` (384 dim) | `bge-small-en` si fuese solo inglés |
| Vector DB | FAISS (escritorio) | `sqlite-vec` (ultraligero) |
| Tokenizer (pista 2) | SentencePiece | BPE / unigram |
| Pesos | `safetensors` (entrenar) → GGUF (inferir) | — |
| Adaptación (futuro) | PyTorch + Transformers + PEFT + TRL (QLoRA) | Solo ciclos controlados |
| Orquestación | Python estándar | LangChain / LlamaIndex (opcional) |
| NN desde cero | NumPy + C++ (sin libs externas) | LibTorch como referencia |

> Las elecciones definitivas se registran como ADR en `02-decisiones/`.

## Estructura del repositorio (propuesta)

```
ampa/
├── README.md · CHANGELOG.md · CITATION.cff · pyproject.toml
├── docs/                          ← documentación (docs-as-code)
│   ├── concepto-maestro.md        ← documento rector (v0.2)
│   ├── 00-vision.md · 01-arquitectura.md · ...
│   ├── 02-decisiones/             ← ADRs
│   └── modulos/                   ← documentación por módulo
├── ampa/                          ← PISTA A: el sistema (paquete Python)
│   ├── core/        ✅            ← portabilidad: plataforma + rutas
│   ├── cli/         ✅            ← interfaz de línea de comandos
│   ├── perception/  ✅            ← capa de percepción (eventos + clasificador)
│   ├── knowledge/   ⏳            ← ingesta de apuntes (RAG)
│   ├── memory/      ⏳            ← memoria dinámica persistente
│   ├── scribe/      ⏳            ← escritura multiplataforma + backups
│   ├── dynamism/    ⏳            ← simulaciones aleatorias
│   ├── domains/     ⏳            ← clasificador de dominio
│   └── engine/      ⏳            ← wrapper sobre llama.cpp
├── cpp/             ✅            ← C++ portable (CMake): sonda; futuro runtime/NN
├── nn/              ⏳            ← PISTA B: red neuronal desde cero (Python)
├── tests/           ✅            ← pruebas (unittest, sin dependencias)
├── models/                        ← modelos GGUF (no se versionan)
└── data/                          ← apuntes, memoria y backups (no se versionan)
```

> Las carpetas de código se crearán al iniciar cada módulo, documentando el porqué.
