# Concepto Maestro de AMPA

> Documento que **conjunta y hace congruentes** todas las ideas del proyecto en una
> sola visión. Es la fuente de verdad de "qué es AMPA y por qué". Si otro documento
> contradice a este, este manda (y se corrige el otro).
>
> Estado: **vigente** · Fecha: 2026-06-18

---

## 1. La idea, en un párrafo

**AMPA** es un sistema de lenguaje **local, incremental y documentado** que corre en
CPU con 16 GB de RAM. No es un LLM entrenado desde cero (eso exige GPUs y datos
masivos), sino una **arquitectura de conocimiento actualizable**: un modelo base
pequeño y ya entrenado, rodeado de una **memoria dinámica** que aprende —sobre
todo— de **tus propios apuntes de investigación**. Su carácter es el de un
**compañero de ciencia**: piensa con eje en la **química** y razona con la lente de
la **filosofía**.

> Esta definición es congruente con tu informe de investigación: el valor nuevo no
> está en replicar un *frontier model*, sino en diseñar un **motor de conocimiento
> incremental** bien documentado.

## 2. Los dos dominios: química y filosofía

Cambiamos el rumbo anterior (medicina y psicología) por una dupla más afín a tu
pasión por la ciencia:

- **Ciencia, con eje en la química.** La química como "ciencia central": conecta la
  física con la biología y los materiales. Conceptos, nomenclatura, reacciones,
  termodinámica, estructura de la materia.
- **Filosofía.** No como adorno, sino como **lente epistemológica**: filosofía de la
  ciencia, lógica, ética, teoría del conocimiento. La pregunta *"¿cómo sabemos
  esto?"* acompaña a cada respuesta científica.

**Por qué esta combinación es potente:** la química aporta el *qué* y el *cómo* del
mundo material; la filosofía aporta el *por qué lo creemos* y el *qué significa*.
Juntas habilitan un razonamiento que pocos asistentes caseros intentan: **filosofía
de la ciencia aplicada**. Ese es un nicho genuinamente tuyo.

> El clasificador de dominio (nuestra red neuronal desde cero) enruta cada pregunta a
> **química**, **filosofía** o **general**.

## 3. Cómo aprende: el 90% son tus apuntes

El corazón de AMPA es tu investigación. La regla de diseño es **90/10**:

- **~90% — tus apuntes.** Todo lo que investigas y escribes (`.md`, `.txt`, `.pdf`)
  se ingiere, se trocea, se convierte en *embeddings* y se guarda en la memoria. A
  partir de ahí, AMPA aprende y responde con **tu** material, citándolo.
- **~10% — base curada.** Un cimiento de fuentes abiertas y confiables (química y
  filosofía) para que no parta de cero. Ver `05-base-conocimiento.md`.

Esto sigue el principio del informe: el material nuevo entra por **ingestión +
recuperación (RAG)**, no reentrenando el modelo cada vez (lo que causaría *olvido
catastrófico* e inestabilidad). El ajuste de pesos (LoRA) queda para ciclos
controlados y futuros, no para el día a día.

## 4. Las capacidades nuevas (y cómo encajan)

### 4.1. Memoria dinámica persistente

AMPA **recuerda entre sesiones**. La memoria vive en disco y evoluciona:

- **Persistencia:** el índice vectorial, el estado y los hechos aprendidos se guardan
  y se recargan en el siguiente arranque. Lo que le enseñas hoy, lo usa mañana.
- **Dinámica:** pondera por **relevancia** y **recencia**; puede archivar lo que casi
  no se usa y reforzar lo recurrente. No es un cajón estático, es una memoria viva.
- **Tres niveles** (según tu informe): paramétrica (el modelo base), **no paramétrica
  (RAG: tus apuntes)** y de adaptación (LoRA, futuro).

### 4.2. Escritura de archivos multiplataforma (módulo "escriba")

AMPA podrá **escribir y corregir archivos** en **Windows o Linux**, pensado sobre
todo para **mantener al día la documentación** y pulir tus apuntes. Con
salvaguardas estrictas:

- **Rutas multiplataforma** (vía `pathlib`): el mismo código funciona en Windows y
  Linux.
- **Espacio acotado:** solo escribe dentro de un directorio de trabajo autorizado.
- **Nunca sin respaldo:** antes de modificar algo, crea un **backup** (ver 4.3).
- **Trazabilidad:** cada cambio queda registrado (qué, cuándo, por qué).

### 4.3. Backups

Antes de tocar cualquier archivo, AMPA guarda una **copia de seguridad con
marca de tiempo**. Se respaldan:

- Tus apuntes y la documentación que corrija.
- La **memoria** misma (índice vectorial + estado), para no perder lo aprendido.

Así, "corregir" nunca significa "arriesgar". Siempre se puede volver atrás.

### 4.4. Motor de dinamismo: simulaciones aleatorias

Para que las respuestas no sean repetitivas ni planas, AMPA incorpora un **motor
estocástico** —y, fiel a la ciencia, **reproducible**:

- **Decodificación controlada:** temperatura y *top-p* ajustables para variar el tono
  y la creatividad.
- **Muestreo tipo Monte Carlo:** genera varias respuestas candidatas y las contrasta
  (auto-consistencia), eligiendo o combinando la mejor.
- **Escenarios y ejemplos aleatorios para ciencia:** moléculas, reacciones o
  problemas de química generados al azar para ilustrar, practicar y explorar.
- **Semilla reproducible:** fijas la semilla y obtienes exactamente el mismo
  resultado. Dinamismo **sin** sacrificar el rigor científico.

## 5. Arquitectura integrada

```
                         ┌───────────────────────────────┐
     Tú ───pregunta────► │          Interfaz (CLI)        │
     Tú ───apuntes─────► │                                │
                         └───────────────┬───────────────┘
                                         ▼
                         ┌───────────────────────────────┐
                         │      Orquestador (Python)      │
                         │  ┌──────────────┐  ┌────────┐  │
                         │  │ Clasificador │  │ Motor  │  │
                         │  │ de dominio   │  │ de     │  │
                         │  │ (NN propia)  │  │dinamismo│ │
                         │  └──────────────┘  └────────┘  │
                         └───┬─────────┬─────────┬────────┘
                  ┌──────────┘         │         └──────────┐
                  ▼                    ▼                    ▼
        ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
        │  Memoria dinámica│ │   Escriba +      │ │  Motor + modelo  │
        │  persistente     │ │   Backups        │ │  base (llama.cpp,│
        │  (RAG: 90% tus   │ │  (corrige docs   │ │  C++)            │
        │  apuntes)        │ │   en Win/Linux)  │ │                  │
        └──────────────────┘ └──────────────────┘ └──────────────────┘
                  │                                         │
                  └─────────► contexto citado ◄─────────────┘
                                     │
                                     ▼
                    respuesta + fuentes + nivel de confianza
```

**Flujo de una consulta:** clasificas dominio → recuperas de la memoria (tus apuntes
+ base) → el motor de dinamismo decide cuánta variación aplicar → el modelo genera →
se responde con **citas** y una **marca de confianza**. Si no hay evidencia, AMPA
dice *"no lo sé"* en lugar de inventar.

## 6. Stack técnico (según tu investigación)

| Capa | Elección | Notas |
|---|---|---|
| **Inferencia (C++)** | `llama.cpp` | CPU x86 AVX2, cuantización 1.5–8 bits |
| **Modelo base** | 1.7B–3B (SmolLM2-1.7B, Granite-3.3-2B, Qwen2.5-3B, Phi-3-mini) | Licencias permisivas, cabe en RAM |
| **Embeddings** | `multilingual-e5-small` | Multilingüe (español + inglés), 384 dim |
| **Vector DB** | FAISS (escritorio) · `sqlite-vec` (ultraligero) | Búsqueda por similitud |
| **Tokenizer (pista educativa)** | SentencePiece | BPE/unigram, C++ y Python |
| **Pesos** | `safetensors` (entrenar) → **GGUF** (inferir) | Seguro y portable |
| **Adaptación (futuro)** | PyTorch + Transformers + PEFT + TRL (QLoRA) | Solo en ciclos controlados |
| **Orquestación** | Python | El pegamento del sistema |

## 7. Las dos pistas de desarrollo (en paralelo)

1. **El sistema AMPA** — motor `llama.cpp` (C++) + RAG + memoria + escriba + motor de
   dinamismo, orquestado en Python. El asistente usable.
2. **Red neuronal desde cero** — un MLP en Python (NumPy) y su espejo en C++; además,
   un mini-tokenizer con SentencePiece y un mini-transformer didáctico. Sirve para
   **entender** el fondo y como **clasificador de dominio** real del sistema.

## 8. Principios y ética

1. **Local primero.** Tus apuntes y tu memoria no salen de tu máquina.
2. **Honestidad epistémica.** Marca el origen: *de mi base / me lo enseñaste tú / no
   lo sé*. Filosofía de la ciencia en acción.
3. **Reproducibilidad.** Todo lo aleatorio es **semillable**. Ciencia, no azar ciego.
4. **Seguridad al escribir.** Nada se modifica sin backup y registro.
5. **Citas siempre que se pueda.** Si una afirmación viene de un apunte o fuente, se
   dice de dónde.
6. **Sin coautoría de IA.** El proyecto es **tuyo**. Ningún asistente figura como
   autor (ni en commits ni en `CITATION.cff`).
7. **Documentar mientras se construye.** Cada módulo nace con su documento gemelo
   (enfoque *docs-as-code* / Diátaxis) y se registra en el `CHANGELOG`.

## 9. Roadmap resumido

| Capa | Entregable |
|---|---|
| **0 — Fundación** | Visión, arquitectura, decisiones, documentación *(en curso)* |
| **1 — Didáctica** | Tokenizer propio + MLP/mini-transformer en Python y C++ |
| **2 — Primer sistema útil** | Modelo pequeño + RAG de tus apuntes + citas (CLI) |
| **3 — Memoria + escriba** | Memoria dinámica persistente, backups, corrección de docs |
| **4 — Dinamismo** | Motor de simulaciones aleatorias reproducibles |
| **5 — Dominios** | Base curada de química y filosofía + clasificador de dominio |
| **6 — Adaptación** | LoRA/QLoRA en ciclos controlados (opcional, avanzado) |
| **7 — Evaluación y seguridad** | Banco de casos propio, confianza por respuesta |

Detalle en [`03-roadmap.md`](03-roadmap.md).

## 10. Qué sigue

- Confirmar este documento maestro (¿algo que ajustar?).
- Empezar a construir: propuesta de arrancar por la **Pista 2** (red neuronal y
  tokenizer desde cero), porque es autocontenida y la puedo construir y probar aquí
  mismo, sin descargar modelos de varios GB.
- Cuando quieras, me cuentas tu nivel en C++/Python para ajustar las explicaciones.
