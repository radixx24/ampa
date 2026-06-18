# 04 — Glosario

> Términos del proyecto explicados en lenguaje claro. Si algo en el código no se
> entiende, debería estar aquí.

### LLM (Large Language Model / Modelo de Lenguaje Grande)
Una red neuronal entrenada con enormes cantidades de texto para predecir la
siguiente palabra. De esa simple tarea emerge la capacidad de conversar, resumir y
razonar.

### Token
La unidad mínima que procesa el modelo. No es exactamente una palabra: puede ser una
palabra, parte de ella o un signo. "Velocidad de X tokens/segundo" mide qué tan
rápido genera texto.

### Parámetros (3B, 7B…)
Los "pesos" ajustables del modelo. "3B" = 3 mil millones de parámetros. Más
parámetros suelen dar más capacidad, pero también más consumo de RAM y menos
velocidad.

### Cuantización (Q4, Q8…)
Técnica para **comprimir** el modelo guardando sus parámetros con menos precisión
(p. ej. 4 bits en vez de 16). Reduce mucho la RAM y acelera en CPU, con una pérdida
de calidad pequeña. "Q4_K_M" es un esquema concreto, buen equilibrio.

### GGUF
El formato de archivo de modelo que usa `llama.cpp`. Un único archivo que contiene
el modelo ya cuantizado, listo para cargar.

### llama.cpp
Motor de inferencia escrito en **C++**, optimizado para correr LLMs en **CPU**
(aunque también soporta GPU). Es la pieza que ejecuta el modelo en AMPA.

### Inferencia
El acto de **usar** un modelo ya entrenado para generar una respuesta (distinto de
*entrenar*, que es ajustar sus pesos).

### Embedding
Una lista de números (vector) que representa el **significado** de un texto. Textos
con significado parecido tienen vectores cercanos. Es la base de la búsqueda
semántica.

### Vector DB (base de datos vectorial)
Almacén especializado en guardar embeddings y encontrar rápidamente los más
**parecidos** a una consulta. El corazón de la memoria de AMPA.

### RAG (Retrieval-Augmented Generation)
"Generación aumentada por recuperación". En vez de confiar solo en lo que el modelo
memorizó, **buscamos** fragmentos relevantes en una base de conocimientos y se los
**damos** al modelo junto con la pregunta. Así responde con información actualizada y
**citable**.

### Troceado (chunking)
Partir documentos largos en fragmentos manejables antes de convertirlos en
embeddings. El tamaño del trozo afecta la calidad de la recuperación.

### Fine-tuning
**Reentrenar** parcialmente un modelo ya existente para especializarlo. Cambia sus
pesos. Más costoso que RAG.

### LoRA (Low-Rank Adaptation)
Una forma **eficiente** de fine-tuning: en vez de tocar todos los pesos, se entrenan
unos pocos "adaptadores" pequeños. Hace viable (aunque lento en CPU) el aprendizaje
paramétrico con poco hardware.

### MLP (Perceptrón multicapa)
La red neuronal "clásica": capas de neuronas conectadas. Es la que implementaremos
**desde cero** en la Pista 2.

### Forward pass (paso hacia adelante)
Calcular la salida de la red a partir de una entrada, capa por capa.

### Backpropagation (retropropagación)
El algoritmo que calcula **cómo ajustar** cada peso para reducir el error,
propagando el error desde la salida hacia atrás. El motor del aprendizaje de una NN.

### Descenso de gradiente
El método que usa la backpropagation para mejorar: dar pequeños pasos en la
dirección que **reduce el error**.

### Capa epistémica
Término propio de AMPA: la parte del sistema que distingue **el origen** de una
afirmación —de la base, aprendida del usuario, o desconocida— y su nivel de
confianza.

### Memoria dinámica
La memoria de AMPA que **persiste** entre sesiones y **evoluciona**: pondera por
relevancia y recencia, refuerza lo recurrente y archiva lo poco usado. No es un
cajón estático.

### Semilla (seed)
Un número que inicializa el generador de aleatoriedad. Con la **misma semilla** se
obtiene **el mismo resultado**: así una respuesta "aleatoria" se vuelve
**reproducible**. Clave para el rigor científico de AMPA.

### Monte Carlo
Familia de métodos que usan **muestreo aleatorio** para explorar resultados
posibles. En AMPA: generar varias respuestas candidatas y contrastarlas
(auto-consistencia) para elegir o combinar la mejor.

### Temperatura y top-p
Dos perillas que controlan cuán "creativa" o "conservadora" es la generación.
**Temperatura** alta = más variedad; **top-p** limita la elección a las opciones más
probables. Juntas modulan el dinamismo de las respuestas.

### SentencePiece
Herramienta para crear un **tokenizer** propio de forma agnóstica al idioma (BPE o
unigram), con soporte en C++ y Python. La usaremos en la pista educativa.

### FAISS
Biblioteca en C++ (con bindings de Python) para **búsqueda por similitud** entre
vectores a gran velocidad. Candidata para la memoria de AMPA en escritorio.

### sqlite-vec
Extensión de SQLite para búsqueda vectorial **embebida y ultraligera**: corre "casi
en cualquier parte". Alternativa portable a FAISS.

### safetensors
Formato **seguro y rápido** para guardar los pesos de un modelo, sin los riesgos del
`pickle` de Python. Se usa al entrenar; para inferir se convierte a GGUF.

### PEFT (Parameter-Efficient Fine-Tuning)
Conjunto de técnicas para **adaptar** un modelo grande entrenando solo una pequeña
parte de sus parámetros. LoRA y QLoRA son ejemplos.

### QLoRA
Variante de LoRA que carga el modelo base **cuantizado a 4 bits** y entrena solo los
adaptadores. Hace viable la adaptación con poco hardware.

### Escriba
Módulo de AMPA que puede **escribir y corregir archivos** en Windows o Linux (rutas
con `pathlib`), siempre creando un **backup** previo y dentro de un espacio acotado.

### Diátaxis
Marco para organizar documentación en cuatro tipos: **tutoriales**, **guías
how-to**, **referencia** y **explicación**. Evita mezclar "cómo se usa" con "por qué
existe".
