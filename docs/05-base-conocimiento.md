# 05 — Base de conocimiento, fuentes y ética

> Cómo se forma el conocimiento de AMPA: **~90% tus apuntes** + **~10% una base
> curada** de **química** y **filosofía**. Con qué fuentes, bajo qué licencias y con
> qué responsabilidad.

## La regla 90/10

- **~90% — tus apuntes.** Tu investigación es la fuente principal. Se ingiere por
  RAG y es lo que AMPA prioriza al responder.
- **~10% — base curada.** Un cimiento de fuentes abiertas para que no parta de cero.

## Principios

1. **Solo fuentes abiertas y legales.** Nada con derechos restrictivos.
2. **Trazabilidad.** Cada fragmento conserva su fuente para poder **citarla**.
3. **Calidad sobre cantidad.** Mejor poco y confiable que mucho y dudoso.
4. **Reproducibilidad.** Las fuentes y versiones quedan registradas.

## Fuentes candidatas por dominio

> Antes de ingerir cualquier fuente se verifica su licencia y se registra abajo.

### Química / Ciencia
- **PubChem** (NIH) — datos de compuestos químicos, de uso abierto.
- **OpenStax — Chemistry** (libro universitario, CC BY).
- **ChEBI** — entidades químicas de interés biológico, abierto.
- **Wikipedia / Wikibooks de química** (CC BY-SA).
- **IUPAC** — nomenclatura y recomendaciones (según licencia de cada documento).
- **Project Gutenberg** — clásicos de ciencia en dominio público.

### Filosofía
- **Project Gutenberg** — clásicos en dominio público (Platón, Aristóteles, Kant…).
- **PhilArchive** — gran archivo de acceso abierto en filosofía.
- **PhilPapers** — índice con API; útil para **citación y navegación**, con
  restricciones de redistribución (no para corpus masivo).
- **Wikipedia de filosofía** (CC BY-SA).

> ⚠️ **SEP** e **IEP** tienen contenido con copyright: se usan como referencia, **no**
> como corpus de entrenamiento masivo. Cualquier material con todos los derechos
> reservados **no** se ingiere.

## Pipeline de ingesta (resumen)

```
fuente/apunte  →  limpieza  →  troceado  →  embeddings  →  memoria (vector DB)
(.pdf,.txt,.md)   (normalizar)  (con solape)  (multiling.)   (con su fuente y fecha)
```

Cada fragmento guarda metadatos: **fuente**, **licencia**, **dominio**, **fecha** y
si es **apunte propio** o **base curada**.

## Ética y límites

- **AMPA puede equivocarse.** Es apoyo de estudio e investigación, no una autoridad.
  Verifica lo importante con fuentes primarias.
- **Citar siempre que se pueda.** Si una afirmación viene de un apunte o fuente, se
  indica de dónde.
- **Decir "no lo sé".** Preferible a inventar (alucinar). Es parte de la capa
  epistémica.
- **Filosofía ≠ verdad absoluta.** Se presentan corrientes y argumentos como posturas
  en debate, no como dogma.
- **Respeto a las licencias.** No se redistribuye material protegido.

## Sobre tus datos y backups

- Tus apuntes y la memoria se guardan **localmente**. No salen de tu máquina.
- Antes de que el **escriba** corrija cualquier archivo, se crea un **backup** con
  marca de tiempo. La memoria también se respalda.
- Habrá forma de **revisar y borrar** lo aprendido.

## Registro de fuentes ingeridas

> Tabla viva: se llena a medida que se incorpora cada fuente.

| Fuente | Dominio | Licencia | Fecha | Estado |
|---|---|---|---|---|
| _(ninguna aún)_ | — | — | — | — |
