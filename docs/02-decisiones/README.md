# Decisiones de arquitectura (ADR)

Un **ADR** (*Architecture Decision Record*) es una nota corta que registra una
decisión técnica importante: **qué** decidimos, **por qué**, qué **alternativas**
descartamos y qué **consecuencias** tiene.

Sirven para que, dentro de seis meses, recordemos por qué algo es como es —y para
documentar el proyecto mientras se construye, que es uno de sus objetivos.

## Formato

Cada ADR sigue esta plantilla:

- **Estado**: propuesto / aceptado / reemplazado.
- **Contexto**: la situación y las fuerzas en juego.
- **Decisión**: lo que decidimos hacer.
- **Alternativas**: lo que consideramos y por qué no.
- **Consecuencias**: lo bueno y lo malo que trae.

## Índice

| ADR | Título | Estado |
|---|---|---|
| [0001](0001-modelo-base-3b.md) | Modelo base pequeño (1.7B–3B) cuantizado | Aceptado |
| [0002](0002-aprendizaje-rag-primero.md) | Aprendizaje vía RAG primero, ganchos para LoRA | Aceptado |
| [0003](0003-dos-pistas-paralelo.md) | Dos pistas de desarrollo en paralelo | Aceptado |
| [0004](0004-cambio-dominios.md) | Cambio de dominios: química y filosofía | Aceptado |
| [0005](0005-apuntes-propios-escritura-backups.md) | Apuntes propios como fuente; escritura con backups | Aceptado |
| [0006](0006-memoria-dinamica-simulaciones.md) | Memoria dinámica y simulaciones aleatorias | Aceptado |
| [0007](0007-portabilidad.md) | Portabilidad del núcleo (stdlib, pathlib, CMake) | Aceptado |
| [0008](0008-clasificador-reglas.md) | Clasificador de dominio por reglas antes que ML | Aceptado |
| [0009](0009-escritura-segura.md) | Escritura segura: atómica, con respaldo y bloqueo por riesgo | Aceptado |
| [0010](0010-recuperacion-lexica.md) | Recuperación léxica (BM25) portable antes que embeddings | Aceptado |
| [0010](0010-recuperacion-lexica.md) | Recuperación léxica (BM25) portable antes que embeddings | Aceptado |
