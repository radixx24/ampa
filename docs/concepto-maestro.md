# Concepto Maestro de AMPA

> Documento rector del proyecto AMPA. Su función es reunir en una sola visión qué es el sistema, qué problema intenta resolver, cómo se organiza técnicamente y cómo debe documentarse cada parte para evitar ambigüedad, crecimiento desordenado o decisiones sin justificación.
>
> Estado: **vigente**  
> Fecha: **2026-06-19**  
> Versión: **0.2 — énfasis en percepción, memoria y documentación controlada**

---

## 0. Cómo usar este documento

Este documento no es una lista de ideas sueltas. Debe usarse como **documento maestro** para decidir qué pertenece a AMPA y qué debe quedar fuera por ahora.

Uso correcto:

1. Consultarlo antes de crear módulos nuevos.
2. Usarlo para validar que cada función fortalece lenguaje, percepción, memoria, documentación u operación segura.
3. Actualizarlo solo cuando cambie la visión general del proyecto.
4. Crear un ADR cuando una decisión técnica importante cambie la arquitectura.
5. Mantener los documentos derivados alineados con esta fuente.

### Por qué iniciar con una regla de uso

Un documento maestro pierde valor si nadie sabe cuándo aplicarlo. Esta regla evita que AMPA se fragmente en documentos contradictorios. También define jerarquía: si un documento de módulo contradice este concepto maestro, se corrige el documento de módulo o se actualiza este documento mediante una decisión explícita.

---

## 1. Definición central

**AMPA** es un sistema local de **lenguaje, percepción y memoria** diseñado para acompañar procesos de investigación, escritura, estudio y razonamiento. No se plantea como un LLM entrenado desde cero ni como una simulación de conciencia. Se plantea como una arquitectura práctica: un modelo base pequeño, ejecutado localmente, rodeado por memoria dinámica, recuperación documental, clasificación de dominio, escritura controlada de archivos y documentación estricta del sistema.

AMPA debe correr en una computadora personal con CPU y aproximadamente 16 GB de RAM. Por eso su valor no está en competir con modelos gigantes, sino en construir una estructura local, incremental y verificable que pueda trabajar con los apuntes, documentos y decisiones del usuario.

### 1.1. Qué significa que AMPA sea lenguaje, percepción y memoria

| Eje | Significado dentro de AMPA | Por qué existe |
|---|---|---|
| **Lenguaje** | Capacidad de interpretar preguntas, explicar conceptos, redactar, corregir y razonar con texto. | Es la interfaz natural del sistema. Permite que el usuario piense, pregunte y construya conocimiento sin depender de comandos rígidos. |
| **Percepción** | Capacidad de observar entradas autorizadas: preguntas, apuntes, documentos, cambios en archivos, errores, correcciones, patrones de uso y comandos explícitos. | Sin percepción, AMPA solo responde a una pregunta aislada. Con percepción, puede convertir el entorno autorizado en señales útiles para razonar. |
| **Memoria** | Capacidad de conservar, organizar y reutilizar conocimiento entre sesiones mediante notas, embeddings, índice vectorial, hechos relevantes y estado del proyecto. | Sin memoria, cada interacción empieza desde cero. Con memoria, AMPA puede acompañar una línea de investigación acumulativa. |

**Idea clave:** sin percepción, AMPA solo contesta; con percepción y memoria, AMPA empieza a acompañar un proceso de pensamiento.

---

## 2. Problema que AMPA intenta resolver

El problema no es únicamente “tener un chatbot local”. El problema real es construir un sistema que pueda trabajar con conocimiento personal de forma acumulativa, ordenada y verificable.

Un asistente común puede responder preguntas sueltas, pero suele fallar en cuatro puntos:

1. No recuerda de forma controlada lo que el usuario construye con el tiempo.
2. No distingue claramente entre conocimiento externo, apuntes del usuario y suposiciones.
3. No documenta por qué se tomó una decisión técnica o conceptual.
4. No tiene una arquitectura local que pueda inspeccionarse, respaldarse y modificarse.

AMPA responde a ese problema mediante una arquitectura donde cada módulo tiene una responsabilidad clara, cada fuente de conocimiento tiene trazabilidad y cada decisión importante debe quedar documentada.

### Por qué esta definición importa

Esta definición evita que AMPA se vuelva un proyecto demasiado amplio. El objetivo no es hacer “una IA general”, sino un sistema local de conocimiento con memoria, percepción autorizada y documentación controlada.

---

## 3. Dominios principales: química y filosofía

AMPA se orienta principalmente a dos dominios:

1. **Química**, como eje científico.
2. **Filosofía**, como lente epistemológica.

La química funciona como dominio material: estructura de la materia, reacciones, nomenclatura, termodinámica, materiales, análisis y procesos. La filosofía funciona como dominio crítico: lógica, teoría del conocimiento, ética, filosofía de la ciencia y análisis de supuestos.

### Por qué química y filosofía

La química aporta el estudio del mundo material. La filosofía aporta el análisis de cómo se justifica lo que se afirma. Juntas permiten que AMPA no solo responda “qué ocurre”, sino también “por qué creemos que ocurre” y “qué límites tiene esa explicación”.

### Clasificación de dominio

AMPA debe incluir un clasificador de dominio que enrute cada consulta hacia una de estas categorías:

- química;
- filosofía;
- general;
- documentación del sistema;
- operación técnica.

### Por qué clasificar el dominio

Clasificar evita que todas las preguntas pasen por el mismo tratamiento. Una pregunta de química necesita fuentes, precisión conceptual y quizá fórmulas. Una pregunta filosófica necesita distinciones, argumentos y supuestos. Una pregunta operativa necesita pasos reproducibles. La clasificación permite aplicar reglas distintas según el tipo de problema.

---

## 4. Regla de conocimiento: 90% apuntes, 10% base curada

El conocimiento de AMPA debe organizarse bajo una regla práctica:

| Fuente | Peso aproximado | Función |
|---|---:|---|
| **Apuntes del usuario** | 90% | Núcleo vivo del sistema. Incluye `.md`, `.txt`, `.pdf`, notas de investigación, correcciones, decisiones y documentos propios. |
| **Base curada abierta** | 10% | Cimiento externo mínimo para química, filosofía y operación técnica. Debe ser confiable, documentado y reemplazable. |

AMPA no aprende reentrenando el modelo en cada cambio. El flujo normal debe ser:

```text
ingesta documental → chunking → embeddings → índice vectorial → recuperación contextual → respuesta citada
```

### Por qué no reentrenar en cada cambio

Reentrenar constantemente sería costoso, inestable y arriesgado. Puede producir olvido catastrófico, contaminación del modelo o resultados difíciles de reproducir. Por eso el aprendizaje cotidiano de AMPA debe ocurrir mediante recuperación aumentada por documentos, memoria persistente y actualización controlada de índices.

El ajuste de pesos mediante LoRA o QLoRA queda como una fase futura y controlada, no como mecanismo diario de aprendizaje.

---

## 5. Percepción operativa

La percepción es la capa que permite que AMPA no dependa únicamente de una pregunta aislada. Su función es observar entradas dentro de un entorno autorizado y convertirlas en eventos estructurados.

AMPA puede percibir:

- preguntas y comandos del usuario;
- apuntes nuevos o modificados;
- documentos incorporados a la base de conocimiento;
- errores reportados por el usuario;
- correcciones hechas durante una sesión;
- decisiones técnicas o conceptuales;
- patrones de uso, como temas frecuentes o dudas repetidas;
- relaciones entre documentos, conceptos y proyectos;
- solicitudes dirigidas al módulo de escritura de archivos.

### 5.1. Qué no es percepción

La percepción de AMPA no significa vigilancia general del sistema operativo, monitoreo oculto, acceso irrestricto a carpetas ni interpretación emocional del usuario.

AMPA solo debe percibir lo que el usuario autorice explícitamente:

- carpetas de trabajo definidas;
- archivos permitidos;
- sesiones activas;
- comandos directos;
- eventos técnicos que el propio sistema genere.

### 5.2. Salida de la capa de percepción

Cada evento percibido debe convertirse en una estructura mínima:

```yaml
evento:
  tipo: pregunta | archivo_modificado | correccion | error | decision | comando
  dominio_probable: quimica | filosofia | general | documentacion | operacion
  entidades_relevantes: []
  archivos_relacionados: []
  intencion_detectada: ""
  riesgo_operativo: bajo | medio | alto
  guardar_en_memoria: true | false
  justificacion: ""
```

### Por qué estructurar la percepción

Si AMPA solo “ve” texto sin estructura, no puede decidir qué guardar, qué ignorar, qué citar o qué ejecutar. La estructura convierte una entrada ambigua en un dato operativo. También permite auditar el sistema: se puede saber qué percibió, cómo lo interpretó y por qué actuó.

---

## 6. Memoria dinámica persistente

La memoria es el mecanismo que da continuidad a AMPA. Sin memoria, cada conversación sería un episodio aislado. Con memoria, el sistema puede construir una línea de investigación acumulativa.

AMPA debe manejar tres niveles de memoria:

| Nivel | Descripción | Uso |
|---|---|---|
| **Memoria paramétrica** | Conocimiento ya contenido en el modelo base. | Sirve como capacidad lingüística y conocimiento general inicial. |
| **Memoria no paramétrica** | Documentos recuperables mediante RAG: apuntes, PDFs, notas, fuentes y decisiones. | Es la memoria principal del usuario. Se puede actualizar sin reentrenar. |
| **Memoria de adaptación** | Ajustes futuros mediante LoRA/QLoRA en ciclos controlados. | Solo se usa cuando haya datos suficientes, evaluación y necesidad real. |

### 6.1. Qué debe recordar AMPA

AMPA debe priorizar memoria sobre:

- conceptos recurrentes;
- definiciones propias del proyecto;
- decisiones técnicas tomadas;
- relaciones entre documentos;
- correcciones del usuario;
- preferencias de documentación;
- errores ya diagnosticados;
- rutas de trabajo autorizadas;
- estado de módulos en desarrollo.

### 6.2. Qué no debe recordar automáticamente

AMPA no debe guardar todo. Debe evitar acumular ruido.

No debe guardar automáticamente:

- frases accidentales;
- datos sensibles no necesarios;
- información sin relevancia futura;
- suposiciones no confirmadas;
- contenido contradictorio sin marcarlo como conflicto;
- eventos técnicos temporales que no aporten aprendizaje.

### 6.3. Relevancia, recencia y recurrencia

La memoria debe ponderar tres criterios:

| Criterio | Pregunta que responde | Por qué importa |
|---|---|---|
| **Relevancia** | ¿Esto ayuda a resolver problemas futuros? | Evita guardar ruido. |
| **Recencia** | ¿Esto acaba de cambiar o fue decidido recientemente? | Evita usar información obsoleta. |
| **Recurrencia** | ¿Esto aparece repetidamente en el trabajo del usuario? | Refuerza temas centrales del proyecto. |

### Por qué la memoria debe ser dinámica

Una memoria estática se vuelve archivo muerto. Una memoria dinámica permite que AMPA ajuste la prioridad del conocimiento según el uso real. Esto no significa que invente, sino que reorganiza y recupera mejor aquello que el usuario demuestra necesitar.

---

## 7. Ciclo percepción-memoria-acción

AMPA debe operar bajo este ciclo:

```text
percibir → interpretar → recuperar memoria → razonar → responder o actuar → registrar aprendizaje
```

### 7.1. Desglose del ciclo

| Etapa | Qué ocurre | Por qué es necesaria |
|---|---|---|
| **Percibir** | AMPA recibe una pregunta, archivo, corrección, error o comando. | Sin entrada registrada no hay contexto verificable. |
| **Interpretar** | Clasifica dominio, intención, riesgo y entidades relevantes. | Evita tratar todos los eventos como si fueran iguales. |
| **Recuperar memoria** | Busca documentos, notas y hechos relacionados. | Conecta la respuesta actual con el trabajo previo. |
| **Razonar** | Construye una respuesta, diagnóstico o acción posible. | Convierte memoria y contexto en salida útil. |
| **Responder o actuar** | Responde al usuario o modifica archivos mediante el módulo escriba. | Cierra el ciclo operativo. |
| **Registrar aprendizaje** | Guarda decisiones, correcciones o cambios relevantes. | Permite continuidad entre sesiones. |

### Por qué este ciclo es el centro de AMPA

Este ciclo diferencia a AMPA de un chatbot local simple. El sistema no solo produce texto; también convierte interacciones en eventos, decide qué memoria usar y registra aprendizaje útil. Esa continuidad es el núcleo del proyecto.

---

## 8. Arquitectura integrada

```text
Preguntas / apuntes / archivos / errores / correcciones / comandos
                              │
                              ▼
                    ┌──────────────────────┐
                    │  Capa de percepción  │
                    │  eventos estructurados│
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Orquestador Python   │
                    │ clasificación        │
                    │ políticas            │
                    │ recuperación         │
                    └──────┬───────┬───────┘
                           │       │
             ┌─────────────┘       └─────────────┐
             ▼                                   ▼
┌─────────────────────────┐         ┌─────────────────────────┐
│ Memoria dinámica         │         │ Motor de inferencia      │
│ RAG + estado + hechos    │         │ llama.cpp + modelo base  │
└─────────────┬───────────┘         └─────────────┬───────────┘
              │                                   │
              └──────────────┬────────────────────┘
                             ▼
                  ┌──────────────────────┐
                  │ Respuesta citada     │
                  │ confianza            │
                  │ límites              │
                  └──────────┬───────────┘
                             ▼
                  ┌──────────────────────┐
                  │ Escriba + backups    │
                  │ solo si se autoriza   │
                  └──────────────────────┘
```

### 8.1. Responsabilidades por capa

| Capa | Responsabilidad | Por qué se separa |
|---|---|---|
| **Interfaz** | Recibir instrucciones del usuario. | Mantiene simple la entrada y permite cambiar CLI por GUI en el futuro. |
| **Percepción** | Convertir entradas en eventos estructurados. | Evita que el sistema actúe sobre texto ambiguo. |
| **Orquestador** | Coordinar clasificación, memoria, modelo, políticas y escritura. | Centraliza reglas y evita lógica dispersa. |
| **Memoria** | Recuperar conocimiento relevante y conservar continuidad. | Separa conocimiento actualizado del modelo base. |
| **Modelo** | Generar lenguaje y razonamiento asistido. | Permite cambiar de modelo sin rediseñar todo el sistema. |
| **Escriba** | Crear, modificar o corregir archivos autorizados. | Aísla acciones riesgosas y obliga a respaldos. |
| **Documentación** | Explicar qué existe, por qué existe y cómo se mantiene. | Evita pérdida de control conforme el sistema crece. |

---

## 9. Módulo escriba y escritura segura

El módulo **escriba** permite que AMPA cree, corrija o reorganice archivos dentro de un espacio autorizado. Su uso principal es mantener documentación, apuntes y archivos de conocimiento.

### 9.1. Reglas obligatorias

1. Solo puede operar dentro de carpetas autorizadas.
2. Debe usar rutas multiplataforma mediante `pathlib`.
3. Debe crear backup antes de modificar un archivo existente.
4. Debe registrar qué cambió, cuándo cambió y por qué cambió.
5. Debe poder operar en modo simulación antes de escribir.
6. Debe bloquear cambios si el riesgo operativo es alto y no hay confirmación explícita.

### Por qué el módulo escriba debe estar aislado

Modificar archivos es una acción de mayor riesgo que responder texto. Separar el módulo escriba evita que una respuesta normal termine alterando documentos por accidente. También facilita pruebas, auditoría y reversión.

---

## 10. Sistema de documentación controlada

La documentación no debe ser un agregado posterior. En AMPA, la documentación es parte de la arquitectura. Cada módulo debe existir acompañado de una explicación clara de qué hace, por qué existe, cómo se usa, cómo se prueba y qué límites tiene.

### 10.1. Principio rector

Cada pieza del sistema debe responder cinco preguntas:

1. **Qué es.** Define el componente sin adornos.
2. **Para qué existe.** Explica el problema que resuelve.
3. **Por qué se diseñó así.** Justifica la decisión técnica o conceptual.
4. **Cómo se usa.** Describe entradas, salidas y flujo operativo.
5. **Cómo se verifica.** Define pruebas, criterios de aceptación o señales de error.

### Por qué documentar así

Este formato obliga a separar descripción, intención, justificación, operación y validación. Eso evita documentación decorativa. Cada documento debe servir para tomar decisiones, mantener el sistema o recuperar contexto en el futuro.

---

## 11. Niveles documentales obligatorios

La documentación de AMPA debe dividirse en niveles. Cada nivel tiene una función distinta y no debe mezclarse con los demás.

| Nivel | Documento | Qué contiene | Por qué existe |
|---|---|---|---|
| **Rector** | `conceptomaestro.md` | Visión general, límites, arquitectura y principios. | Evita que el proyecto pierda dirección. |
| **Arquitectura** | `arquitectura.md` | Capa por capa, flujo de datos, responsabilidades y dependencias. | Permite entender cómo se conecta el sistema completo. |
| **Decisiones** | `adr/ADR-000x.md` | Decisiones técnicas importantes, alternativas y consecuencia. | Evita olvidar por qué se eligió una solución. |
| **Módulos** | `modulos/<modulo>.md` | Responsabilidad, entradas, salidas, errores y pruebas de cada módulo. | Permite mantener cada componente sin depender de memoria informal. |
| **Contratos** | `contratos/<nombre>.md` | Esquemas de datos, formatos de eventos, rutas y estructuras. | Evita ambigüedad entre módulos. |
| **Operación** | `operacion/<tarea>.md` | Pasos reproducibles para ejecutar, respaldar, restaurar o diagnosticar. | Convierte tareas técnicas en procedimientos repetibles. |
| **Pruebas** | `pruebas/<caso>.md` | Casos, entradas esperadas, salidas esperadas y criterios de aceptación. | Permite saber si el sistema funciona o solo parece funcionar. |
| **Bitácora** | `CHANGELOG.md` | Cambios por versión, fecha y efecto. | Mantiene trazabilidad histórica. |

### Por qué separar niveles

Si todo se escribe en un solo archivo, el documento se vuelve grande, confuso y difícil de mantener. Separar niveles permite que cada documento tenga una responsabilidad precisa. El documento maestro decide dirección; los documentos de módulos explican implementación; los ADR explican decisiones; los contratos evitan malentendidos técnicos.

---

## 12. Formato obligatorio para documentar módulos

Cada módulo nuevo de AMPA debe documentarse con esta plantilla mínima:

```md
# Módulo: <nombre>

## 1. Propósito
Qué problema resuelve el módulo.

## 2. Responsabilidad exacta
Qué hace y qué no hace.

## 3. Entradas
Datos, archivos, comandos o eventos que recibe.

## 4. Salidas
Datos, archivos, respuestas o eventos que produce.

## 5. Flujo interno
Pasos principales del procesamiento.

## 6. Decisiones de diseño
Por qué se construyó de esta manera y no de otra.

## 7. Errores esperados
Fallos posibles, causa probable y respuesta del sistema.

## 8. Seguridad y límites
Qué operaciones están prohibidas o requieren confirmación.

## 9. Pruebas mínimas
Casos necesarios para validar que funciona.

## 10. Cambios pendientes
Deuda técnica, mejoras y restricciones conocidas.
```

### Por qué esta plantilla es obligatoria

La plantilla obliga a documentar antes de crecer. Si un módulo no puede explicar sus entradas, salidas y límites, todavía no está listo para implementarse. Esto reduce crecimiento horizontal desordenado y evita que AMPA se convierta en un conjunto de scripts difíciles de mantener.

---

## 13. Documentación de decisiones: ADR

Toda decisión importante debe tener un ADR (*Architecture Decision Record*).

Ejemplos de decisiones que requieren ADR:

- elegir FAISS o `sqlite-vec`;
- elegir un modelo base;
- decidir si se usa LoRA;
- definir el formato de eventos de percepción;
- permitir o bloquear escritura automática de archivos;
- cambiar la estructura de carpetas;
- modificar la política de memoria.

### Formato ADR

```md
# ADR-000X: <decisión>

## Estado
Propuesta | Aceptada | Rechazada | Sustituida

## Contexto
Qué problema obligó a tomar esta decisión.

## Opciones consideradas
- Opción A
- Opción B
- Opción C

## Decisión
Qué se eligió.

## Justificación
Por qué se eligió.

## Consecuencias
Qué mejora, qué limita y qué deuda genera.
```

### Por qué usar ADR

Los ADR impiden que las decisiones dependan de memoria informal. Cuando el proyecto crece, no basta con saber “qué se hizo”; se necesita saber “por qué se hizo”. Esa diferencia es crítica para mantener un sistema técnico serio.

---

## 14. Documentación de contratos internos

Los contratos definen cómo se comunican los módulos. Deben ser explícitos.

Ejemplos de contratos:

- formato de evento de percepción;
- estructura de un chunk documental;
- metadatos de memoria;
- formato de respuesta citada;
- formato de backup;
- esquema de registro de cambios;
- interfaz del módulo escriba.

### Ejemplo: contrato de memoria documental

```yaml
chunk:
  id: ""
  documento_origen: ""
  ruta: ""
  titulo: ""
  texto: ""
  embedding_model: "multilingual-e5-small"
  fecha_ingesta: "YYYY-MM-DD"
  dominio: quimica | filosofia | general | documentacion | operacion
  tags: []
  confianza_fuente: alta | media | baja
```

### Por qué documentar contratos

Sin contratos, cada módulo interpreta los datos a su manera. Eso produce errores silenciosos. Un contrato permite que memoria, percepción, orquestador y modelo trabajen bajo el mismo formato.

---

## 15. Documentación de pruebas

AMPA debe probarse con casos pequeños, repetibles y escritos.

Cada prueba debe incluir:

- nombre del caso;
- objetivo;
- entrada exacta;
- memoria o documentos disponibles;
- salida esperada;
- criterio de aceptación;
- errores aceptables;
- fecha de ejecución;
- resultado.

### Ejemplo

```md
# Prueba: recuperación de apunte químico

## Objetivo
Verificar que AMPA recupera un apunte propio antes de responder con conocimiento general.

## Entrada
"Explícame la diferencia entre enlace iónico y covalente según mis apuntes."

## Documentos disponibles
- apuntes/quimica/enlaces.md

## Salida esperada
Respuesta basada en el apunte, con cita del documento.

## Criterio de aceptación
La respuesta debe citar el archivo y no debe inventar una fuente externa.
```

### Por qué documentar pruebas

Sin pruebas escritas, el sistema puede parecer correcto por casualidad. Las pruebas convierten el comportamiento esperado en una referencia estable. También permiten detectar regresiones cuando se cambia el modelo, el índice vectorial o el orquestador.

---

## 16. Stack técnico propuesto

| Capa | Elección | Motivo |
|---|---|---|
| **Inferencia** | `llama.cpp` | Permite ejecutar modelos cuantizados localmente en CPU. |
| **Modelo base** | 1.7B–3B | Balance razonable entre capacidad y límite de RAM. |
| **Embeddings** | `multilingual-e5-small` | Útil para español e inglés, tamaño manejable. |
| **Vector DB** | FAISS o `sqlite-vec` | FAISS para rendimiento; `sqlite-vec` para portabilidad simple. |
| **Orquestación** | Python | Facilita integración entre documentos, embeddings, memoria y CLI. |
| **Componentes críticos** | C++ | Útil para comprender y optimizar partes de bajo nivel. |
| **Adaptación futura** | LoRA/QLoRA | Solo para ciclos controlados de ajuste, no para memoria diaria. |
| **Documentación** | Markdown + ADR + CHANGELOG | Portable, versionable y compatible con docs-as-code. |

### Por qué este stack es coherente

El stack se elige por restricciones reales: hardware local, bajo consumo, trazabilidad, portabilidad y aprendizaje progresivo. Python permite avanzar rápido; C++ permite entender y optimizar; Markdown permite documentar sin depender de plataformas externas; RAG permite actualizar conocimiento sin reentrenar.

---

## 17. Pistas de desarrollo

AMPA debe avanzar en dos pistas paralelas, pero controladas.

### 17.1. Pista A: sistema funcional

Objetivo: construir el asistente local usable.

Incluye:

- CLI inicial;
- ingesta de documentos;
- embeddings;
- índice vectorial;
- recuperación RAG;
- memoria persistente;
- respuestas citadas;
- módulo escriba;
- backups;
- documentación operativa.

### 17.2. Pista B: aprendizaje desde cero

Objetivo: entender los fundamentos técnicos.

Incluye:

- tokenizer didáctico;
- MLP en NumPy;
- versión C++ del MLP;
- clasificador de dominio;
- mini-transformer didáctico;
- pruebas pequeñas y explicadas.

### Por qué separar las pistas

La pista funcional produce utilidad real. La pista didáctica produce comprensión profunda. Si se mezclan sin control, el proyecto se vuelve confuso: ni asistente usable ni laboratorio educativo. Separarlas permite avanzar sin perder claridad.

---

## 18. Principios del proyecto

1. **Local primero.** La memoria y los apuntes deben permanecer en la máquina del usuario salvo autorización explícita.
2. **Percepción autorizada.** AMPA solo observa carpetas, sesiones y archivos permitidos.
3. **Memoria con criterio.** No todo se guarda; se prioriza relevancia, recencia y recurrencia.
4. **Honestidad epistémica.** AMPA debe distinguir entre fuente propia, base externa, inferencia y desconocimiento.
5. **Documentación obligatoria.** Todo módulo debe explicar qué hace, por qué existe y cómo se verifica.
6. **Escritura segura.** Ningún archivo se modifica sin backup, registro y control de riesgo.
7. **Reproducibilidad.** Los procesos aleatorios deben permitir semilla cuando sea necesario.
8. **Sin coautoría artificial.** El proyecto pertenece al usuario. La documentación no debe presentar al asistente como autor.
9. **Crecimiento vertical antes que horizontal.** Primero se profundizan módulos esenciales; después se agregan nuevas capacidades.

---

## 19. Roadmap resumido

| Fase | Objetivo | Entregables |
|---|---|---|
| **0 — Concepto rector** | Cerrar definición, límites y arquitectura. | `conceptomaestro.md`, mapa de módulos, reglas documentales. |
| **1 — Documentación base** | Crear estructura documental controlada. | `arquitectura.md`, carpeta `adr/`, plantillas, `CHANGELOG.md`. |
| **2 — Percepción mínima** | Convertir entradas en eventos estructurados. | contrato de evento, clasificador inicial, logs. |
| **3 — Memoria documental** | Ingerir apuntes y recuperar contexto. | chunking, embeddings, índice vectorial, citas. |
| **4 — CLI funcional** | Permitir preguntas y respuestas con fuentes. | interfaz local, comandos, modo diagnóstico. |
| **5 — Escriba seguro** | Crear/corregir documentos autorizados. | backups, modo simulación, bitácora. |
| **6 — Dominio químico-filosófico** | Consolidar base curada y clasificación. | corpus mínimo, pruebas por dominio. |
| **7 — Evaluación** | Verificar calidad y seguridad. | banco de pruebas, métricas, regresiones. |
| **8 — Adaptación futura** | Evaluar LoRA/QLoRA si hay necesidad real. | ADR, dataset, pruebas antes/después. |

---

## 20. Criterios para considerar que AMPA avanza correctamente

AMPA avanza correctamente si cumple estas condiciones:

1. Puede explicar qué sabe y de dónde lo sabe.
2. Puede recuperar apuntes propios con citas.
3. Puede recordar decisiones relevantes entre sesiones.
4. Puede distinguir entre química, filosofía, documentación y operación técnica.
5. Puede modificar archivos solo bajo reglas seguras.
6. Puede respaldar lo que modifica.
7. Puede documentar cada módulo antes de expandirlo.
8. Puede reconocer incertidumbre en lugar de inventar.

### Por qué estos criterios son necesarios

Estos criterios impiden confundir avance real con apariencia de avance. Un sistema que responde bonito pero no cita, no recuerda, no documenta y no puede verificarse no cumple la visión de AMPA.

---

## 21. Regla final de control

Antes de agregar cualquier función nueva a AMPA, debe responderse este filtro:

```text
1. ¿Esta función fortalece lenguaje, percepción, memoria, documentación u operación segura?
2. ¿Existe un documento que explique por qué debe existir?
3. ¿Tiene entradas y salidas claras?
4. ¿Tiene riesgos identificados?
5. ¿Tiene una prueba mínima?
6. ¿Tiene lugar dentro de la arquitectura actual sin romperla?
```

Si la respuesta a cualquiera de estas preguntas es negativa, la función no debe implementarse todavía.

### Por qué cerrar con esta regla

AMPA debe crecer con control. La regla final protege el proyecto contra la expansión impulsiva. Cada nueva capacidad debe reforzar el núcleo: percepción, memoria, lenguaje, trazabilidad y documentación.

---

## 22. Síntesis

AMPA no busca ser una inteligencia artificial general ni un modelo gigante entrenado desde cero. Busca ser un sistema local, documentado y acumulativo que pueda percibir su entorno autorizado, recordar lo importante, razonar con los apuntes del usuario y actuar de forma segura sobre archivos.

Su valor está en la continuidad: percibir, recordar, razonar, documentar y mejorar sin perder trazabilidad.

La documentación no es decoración. Es el mecanismo que mantiene al proyecto comprensible, auditable y desarrollable.

---

## Anexo A. Correcciones aplicadas en esta versión

| Corrección | Aplicación | Motivo |
|---|---|---|
| Énfasis en percepción | Se añadió una capa completa de percepción operativa, eventos estructurados y límites de autorización. | Convertir AMPA en un sistema que interpreta contexto autorizado, no solo preguntas aisladas. |
| Énfasis en memoria | Se amplió la memoria dinámica persistente con niveles, criterios y límites. | Dar continuidad real entre sesiones sin guardar ruido ni depender de reentrenamiento constante. |
| Ciclo percepción-memoria-acción | Se agregó un ciclo central con etapas y justificación. | Explicar cómo AMPA transforma entrada, contexto y memoria en respuesta o acción. |
| Documentación controlada | Se incorporaron niveles documentales, plantillas de módulos, ADR, contratos y pruebas. | Evitar crecimiento desordenado y obligar a explicar el porqué de cada componente. |
| Seguridad operativa | Se reforzó la separación del módulo escriba, backups, modo simulación y autorización. | Reducir riesgo al permitir que AMPA modifique archivos. |
| Criterio de crecimiento | Se añadió una regla final para filtrar nuevas funciones. | Mantener el proyecto concentrado en su núcleo y evitar expansión horizontal prematura. |
