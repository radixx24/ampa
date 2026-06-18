# 05 — Base de conocimiento, fuentes y ética

> Cómo construimos la base de conocimientos de AMPA en **medicina**, **psicología** y
> **filosofía**, con qué fuentes, bajo qué licencias y con qué responsabilidad.

## Principios

1. **Solo fuentes abiertas y legales.** Nada con derechos de autor restrictivos.
2. **Trazabilidad.** Cada fragmento conserva su fuente para poder **citarla**.
3. **Calidad sobre cantidad.** Mejor poco y confiable que mucho y dudoso.
4. **Responsabilidad en temas sensibles**, en especial salud.

## Fuentes candidatas por dominio

> Antes de ingerir cualquier fuente se verifica su licencia y se registra aquí.

### Medicina
- **MedlinePlus** (información de salud al público, dominio público en EE. UU.).
- **Artículos médicos de Wikipedia** (CC BY-SA).
- **PubMed Central — subconjunto Open Access** (abstracts y artículos con licencia
  abierta).
- **Guías y hojas informativas de la OMS** (según licencia de cada documento).

### Psicología
- **OpenStax — Psychology** (libro de texto universitario, CC BY).
- **Obras de dominio público** (p. ej. textos clásicos ya liberados).
- **Artículos de psicología de Wikipedia** (CC BY-SA).

### Filosofía
- **Project Gutenberg** (dominio público: Platón, Aristóteles, Kant, Nietzsche…).
- **Stanford Encyclopedia of Philosophy** (verificar términos de uso por entrada).
- **Artículos de filosofía de Wikipedia** (CC BY-SA).

> ⚠️ Documentos con copyright (p. ej. el **DSM**, manuales comerciales, libros de
> texto con todos los derechos reservados) **no** se ingieren.

## Pipeline de ingesta (resumen)

```
documento  →  limpieza  →  troceado  →  embeddings  →  vector DB
   (.pdf,        (quitar     (fragmentos    (vectores)    (con su
   .txt,         ruido)      con solape)                  fuente)
   .md, web)
```

Cada fragmento guarda metadatos: **fuente**, **licencia**, **dominio** y **fecha**.

## Ética y límites (importante)

- **AMPA no da consejo médico.** Puede explicar conceptos, pero toda decisión de
  salud debe consultarse con un profesional. En temas clínicos, el sistema mostrará
  un **aviso automático**.
- **No es un terapeuta.** En temas de salud mental sensibles (crisis, autolesión),
  la respuesta correcta es derivar a ayuda profesional y líneas de apoyo, no
  improvisar.
- **Filosofía ≠ verdad absoluta.** Se presentan corrientes y argumentos, señalando
  que son posturas en debate.
- **Citar siempre que se pueda.** Si una afirmación viene de la base, se indica de
  dónde.
- **Decir "no lo sé".** Preferible a inventar (alucinar). Es parte de la capa
  epistémica.

## Sobre datos del usuario

- Lo que le enseñes a AMPA se guarda **localmente**. No sale de tu máquina.
- Habrá forma de **revisar y borrar** lo aprendido (pendiente de diseño).

## Registro de fuentes ingeridas

> Tabla viva: se llena a medida que se incorpora cada fuente.

| Fuente | Dominio | Licencia | Fecha | Estado |
|---|---|---|---|---|
| _(ninguna aún)_ | — | — | — | — |
