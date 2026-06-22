# AMPA

**AMPA — Aprendizaje Multidominio con Patrones Adaptativos**

Un sistema **local, portable y explicable** de lenguaje, percepción y memoria, con
dos dominios de conocimiento (**química** y **filosofía**) y una interfaz **visual**.

> Tesis del proyecto: **percibir → recordar → actuar**, sin inventar, citando
> siempre, y corriendo **donde sea** (idealmente sin instalar nada).

> 📄 Visión completa y a largo plazo (LLM local vía RAG, memoria dinámica, red
> neuronal desde cero): [**Concepto Maestro**](docs/concepto-maestro.md). Este
> README documenta lo que **ya está construido y corriendo**.

---

## Tabla de contenido

1. [Qué es y para qué sirve](#1-qué-es-y-para-qué-sirve)
2. [Filosofía de diseño](#2-filosofía-de-diseño-las-reglas-del-juego)
3. [Cómo correrlo (3 formas)](#3-cómo-correrlo-3-formas)
4. [Arquitectura](#4-arquitectura)
5. [Mapa de módulos](#5-mapa-de-módulos-qué-hace-cada-cosa)
6. [Comandos de la CLI](#6-comandos-de-la-cli)
7. [La API](#7-la-api-httpjson)
8. [El frontend (web)](#8-el-frontend-web)
9. [Cómo funciona por dentro](#9-cómo-funciona-por-dentro-neta)
10. [Consideraciones y límites (NETA)](#10-consideraciones-y-límites-neta)
11. [Pruebas](#11-pruebas)
12. [Estructura de carpetas](#12-estructura-de-carpetas)

---

## 1. Qué es y para qué sirve

AMPA convierte entradas autorizadas en **eventos estructurados** (percepción), los
**recuerda con citas** (memoria), y **actúa con seguridad** sobre archivos
(escriba). Encima de ese núcleo viven dos **dominios de conocimiento**:

- **Química** 🧪 — reconoce elementos y compuestos, modela moléculas (átomos +
  enlaces), detecta grupos funcionales, infiere reacciones (con combustión
  **balanceada**) y genera **geometría 3D** para verlas.
- **Filosofía** 📚 — reconoce filósofos, corrientes y conceptos, y mantiene un
  **cuaderno/diccionario personal** que crece con lo que tú escribes.

Y una **interfaz visual** (React) con tabla periódica interactiva, **editor visual
de enlaces**, **visor 3D** y **animación de reacciones**.

**¿Para qué?** Para estudiar, anotar y *ver* lo que proyectas, con un asistente que
**no alucina**: si no tiene evidencia, lo dice.

> La generación de lenguaje con un LLM local (`llama.cpp` vía RAG) y la **red
> neuronal desde cero** (Pista B) son parte de la visión y están en el
> [roadmap](docs/03-roadmap.md); hoy `responder` es **extractivo** (cita, no inventa).

---

## 2. Filosofía de diseño (las reglas del juego)

| Principio | Qué significa | Por qué |
|---|---|---|
| **Portabilidad extrema** | El núcleo usa **solo la biblioteca estándar** de Python. Cero `pip install`. | Corre en Windows, macOS y Linux igual; hasta como **ejecutable único**. |
| **Honestidad epistémica** | Recupera y **cita**; no inventa. Declara su **confianza**. | Un asistente de estudio que miente no sirve. |
| **Explicable antes que mágico** | Clasificadores por reglas, fórmulas validadas, heurísticas claras. | Se puede auditar, testear y entender. |
| **Reversible y seguro** | La escritura va con **respaldo** y **puerta de riesgo**. | Nunca pierdes datos por accidente. |
| **Documentado mientras se construye** | Cada módulo tiene su doc; cada decisión, su **ADR**. | El "por qué" no se olvida. |

Objetivo de hardware: **CPU x86-64**, ~**16 GB de RAM**, **sin GPU**. Linux/Windows/macOS.

---

## 3. Cómo correrlo (3 formas)

**A) El conjuro (recomendado):**
```bash
python -m ampa ampakadabra
#  compila el frontend la 1ª vez (si hay Node), sirve web + API en
#  http://127.0.0.1:8000 y te abre el navegador.
```

**B) Desarrollo (front con recarga en vivo):**
```bash
python -m ampa servir                          # API en :8000
cd frontend && npm install && npm run dev      # web en :5173
```

**C) Ejecutable único (para repartir):**
```bash
cd frontend && npm install && npm run build && cd ..
pip install pyinstaller
python packaging/build_exe.py    # → dist_exe/ampakadabra (no necesita Python ni Node)
```

> El núcleo + la CLI corren **sin instalar nada**: `python -m ampa <comando>`.

---

## 4. Arquitectura

```
            ┌──────────────────────── el ciclo (§6) ────────────────────────┐
            │                                                                │
   entrada →│  PERCIBIR ──► RECORDAR (memoria + citas) ──► ACTUAR (escriba)  │→ bitácora
            │  perception        memory                     scribe           │
            └────────────────────────────────────────────────────────────────┘

   Dominios:   chemistry (química)        philosophy (filosofía)
   Respuesta:  answer  (une percepción + memoria + química + filosofía, con confianza)

   ┌─ React (2 apartados) ─┐  HTTP/JSON   ┌─ API (stdlib, 0 deps) ─┐   ┌─ Núcleo (stdlib) ─┐
   │ tabla · editor · 3D   │ ───────────► │  ampa/api  (manejar)   │──►│ chemistry/philo…  │
   └───────────────────────┘              └────────────────────────┘   └───────────────────┘
```

El **núcleo** (`ampa/`) no sabe que existe la web: la **API** es una capa fina, y
el **frontend** consume la API. Por eso todo se puede empaquetar en **un binario**.

---

## 5. Mapa de módulos (qué hace cada cosa)

| Módulo | Qué hace | Para qué | Doc |
|---|---|---|---|
| `core` | Detección de plataforma y **rutas portables** (Windows/macOS/Linux). | Guardar y leer en el sitio correcto en cualquier SO. | [core.md](docs/modulos/core.md) |
| `perception` | Convierte una entrada en un **Evento** (dominio, tipo, **riesgo**, política de memoria) + un **diario**. | Entender y clasificar lo que entra, sin actuar. | [percepcion.md](docs/modulos/percepcion.md) |
| `memory` | **Ingesta** (troceo) de apuntes y **recuperación con citas** (BM25). | Una memoria consultable y trazable. | [memoria.md](docs/modulos/memoria.md) |
| `scribe` | **Escritura segura**: respaldo previo, atómica, simulación y **bloqueo por riesgo**. | Corregir archivos sin romperlos; reversible. | [escriba.md](docs/modulos/escriba.md) |
| `answer` | **Responde con fuentes**: percibe + recupera + **confianza/origen** + química/filosofía. | Q&A honesto sobre tus apuntes. | [respuesta.md](docs/modulos/respuesta.md) |
| `cycle` | Orquesta **percibir → recordar → actuar** en un comando. | La tesis del proyecto, hecha demo. | [ciclo.md](docs/modulos/ciclo.md) |
| `chemistry` | Tabla (118), fórmulas, reconocedor, **moléculas**, **grupos**, **reacciones**, **geometría 3D**. | El editor de enlaces de carbono. | [quimica.md](docs/modulos/quimica.md) |
| `chemistry` (termo) | **Balanceo general**, **Gibbs (ΔG)** como umbral y **compatibilidad** entre elementos. | Proyectar si algo puede existir/reaccionar. | [termodinamica.md](docs/modulos/termodinamica.md) |
| `philosophy` | Reconocedor (filósofos/corrientes/conceptos) y **cuaderno/diccionario personal**. | Pensar y construir tu propio glosario. | [filosofia.md](docs/modulos/filosofia.md) |
| `api` | **API JSON** portable (stdlib) + sirve el frontend compilado. | Que la web (u otra cosa) hable con AMPA. | [api.md](docs/modulos/api.md) |
| `cli` | Interfaz de línea de comandos (`argparse`). | Manejar todo desde la terminal. | — |
| *frontend* | App React: apartados, editor visual, **visor 3D**, **animación**, **proyección termodinámica**, **grafo**. | *Ver* las sustancias que proyectas. | [frontend.md](docs/modulos/frontend.md) |

---

## 6. Comandos de la CLI

`python -m ampa <comando>` (o `ampa <comando>` si lo instalas).

| Comando | Qué hace |
|---|---|
| `info` / `version` / `paths` | Plataforma y rutas portables. |
| `percibir "..."` `[--registrar]` | Estructura una entrada como **Evento**. |
| `diario` | Eventos percibidos y guardados. |
| `recordar` `--texto/--desde/--carpeta` | **Ingiere** apuntes a la memoria. |
| `consultar "..."` `[-k N]` | Recupera fragmentos con **citas**. |
| `responder "..."` `[--detalle]` | Respuesta con fuentes, **confianza** y química/filosofía. |
| `memoria` | Estado de la memoria documental. |
| `ciclo "..."` `[--ejecutar] [--forzar]` | Percibir → recordar → **proponer/ejecutar** escritura. |
| `escribir RUTA` `--contenido/--desde` | Escritura segura (respaldo, `--simular`, `--forzar`). |
| `restaurar RUTA` | Restaura desde el respaldo más reciente. |
| `quimica "..."` `[--json] [--tabla]` | Identifica elementos/compuestos; vuelca la tabla. |
| `compuesto guardar/listar/analizar` | **Moléculas**: fórmula, masa, grupos, reacciones. |
| `filosofia "..."` `[--json]` | Identifica filósofos/corrientes/conceptos. |
| `pensar "..."` `[--sobre t1,t2]` | Añade un **pensamiento** al cuaderno. |
| `diccionario [término]` `[--json]` | Tu **diccionario personal**. |
| `servir` `[--puerto]` | Arranca la API (+ frontend si está compilado). |
| `ampakadabra` ✨ | Conjura **web + API** en un comando y abre el navegador. |

---

## 7. La API (HTTP/JSON)

Stdlib pura, con CORS. Despacho probado sin sockets (`manejar`).

| Método y ruta | Devuelve |
|---|---|
| `GET  /api/salud` | Estado y versión. |
| `GET  /api/quimica/tabla` | Los 118 elementos (símbolo, Z, masa, grupo, periodo, categoría, radio). |
| `POST /api/quimica/identificar` `{texto}` | Elementos y compuestos detectados. |
| `POST /api/quimica/analizar` `{molécula}` | Fórmula, masa, **grupos**, **reacciones**, **valencia/polaridad**. |
| `POST /api/quimica/reacciones` `{molécula}` | Reacciones plausibles. |
| `POST /api/quimica/geometria` `{molécula}` | Coordenadas **3D** por átomo (con radio). |
| `POST /api/quimica/balancear` `{reactivos, productos}` | **Balancea** la ecuación → coeficientes. |
| `POST /api/quimica/proyectar` `{reactivos, productos, temperatura}` | **ΔH/ΔS/ΔG** + veredicto de espontaneidad. |
| `POST /api/quimica/compatibilidad` `{a, b, temperatura}` | Enlace, **fórmula** y **ΔG** de formación. |
| `GET/POST /api/quimica/compuestos` | Listar / **guardar** compuestos. |
| `POST /api/filosofia/identificar` `{texto}` | Filósofos, corrientes, conceptos. |
| `POST /api/filosofia/pensar` `{texto, terminos}` | Guarda un pensamiento. |
| `GET  /api/filosofia/diccionario` | Diccionario personal. |
| `POST /api/filosofia/clasificar` `{terminos}` | Clasifica términos (época/corriente) para el grafo. |
| `GET  /api/filosofia/catalogo` | Filósofos, corrientes y conceptos para **explorar**. |
| `GET  /*` | El frontend compilado (SPA). |

Molécula = `{ "nombre", "atomos": ["C","H",…], "enlaces": [[a,b,orden],…] }`.

---

## 8. El frontend (web)

Dos **apartados**:

- **Química**: tabla periódica interactiva (color por categoría, posición por
  grupo/periodo), **identificar** texto, y el **editor de enlaces de carbono**:
  - Modos **construir / mover / borrar**, plantillas, **exportar PNG**, y
    **encadenar** (arrastrar desde un átomo crea átomo + enlace de un gesto).
  - **Química viva**: enlaces coloreados por **polaridad**, átomos por **saturación
    de valencia**, e input de **temperatura**.
  - **Ver en 3D** — visor **hecho desde cero** (sin librerías 3D); enlaces
    dobles/triples, tamaño por **radio**, **vibración térmica** y exportar PNG.
  - **Reacciones** — combustión (átomo a átomo), hidrogenación y neutralización.
  - **Proyección termodinámica** — reactivos→productos + temperatura → **ΔG** y
    veredicto de si **puede existir**; y **compatibilidad** entre dos elementos.
  - **Mis compuestos** — lo que guardas queda como **plantilla**: lo **cargas**,
    **analizas** o **proyectas** (ΔG) con un clic; al guardar sale una **notificación**.
  - **Atajos de teclado** (`C` crear · `M` mover · `B` borrar · `1/2/3` enlace · `Esc`)
    que el propio editor muestra, y una **barra desplegable** con las herramientas extra.
- **Filosofía**: **explorar** la base (filósofos por época, corrientes, conceptos) →
  **escribir** en tu cuaderno/diccionario → **ver** tus ideas conectadas en un
  **grafo** (estilo Obsidian) con buscador y agrupado por época/corriente.

Diseño con **estética Vercel** (monocromo, bordes finos), **iconos minimalistas**
(sin emojis) con *hovers* suaves, **responsivo** (con **barra inferior** en móvil) y
una **guía rápida** para empezar sin saber nada. El cliente usa el **mismo origen**
que sirve la web, así que funciona en cualquier puerto.

Detalle técnico en [docs/modulos/frontend.md](docs/modulos/frontend.md).

---

## 9. Cómo funciona por dentro (NETA)

- **Percepción** — clasifica el dominio por **reglas léxicas** (sin ML), infiere el
  tipo, evalúa el **riesgo** (verbo de comando + modificación de archivo = alto) y
  decide si vale la pena guardarlo (evita ruido). *No actúa; solo describe.*
- **Memoria** — trocea por párrafos (con solapamiento), indexa con **BM25**
  (filtrando palabras vacías) y devuelve los mejores fragmentos **con cita**
  (`fuente#índice`). La **confianza** se mide por **cobertura de términos +
  dominio**, no por el score (que engaña con corpus chicos).
- **Escriba** — escribe en un temporal y hace `os.replace` (**atómico**); antes de
  sobrescribir, **respalda**; si el riesgo es alto, **bloquea** salvo `--forzar`.
- **Química** — fórmulas validadas contra los 118 símbolos; **grupos funcionales**
  por patrones sobre el grafo de enlaces; **combustión balanceada** con fracciones
  exactas; **geometría 3D** por un layout de fuerzas (repulsión + resortes con
  longitud ≈ suma de **radios covalentes**).
- **Termodinámica (el umbral)** — **balancea cualquier ecuación** resolviendo el
  **espacio nulo** de la matriz de conteos atómicos (con `Fraction`, exacto), y
  calcula la **Energía Libre de Gibbs** `ΔG = ΔH − T·ΔS` a partir de datos estándar
  de formación (ΔHf°, S°). Si **ΔG < 0**, es espontánea. Da la **temperatura de
  cruce** (donde cambia el signo) y, para dos elementos, predice el enlace (ΔEN), la
  **fórmula por aspa de cargas** y el ΔG de su formación. *El número manda; si falta
  un dato, lo dice (no inventa).*
- **Filosofía** — reconocimiento por **palabra completa** (sin acentos); el cuaderno
  agrupa pensamientos por término (los pones tú o los detecta).
- **Visor 3D** — rota los puntos con matrices a mano, proyecta con perspectiva,
  ordena por profundidad (*painter's algorithm*) y dibuja esferas con degradado.
- **Animación de combustión** — balancea, coloca reactivos y productos, **empareja
  los átomos por elemento** (porque se conservan) e interpola sus posiciones.

---

## 10. Consideraciones y límites (NETA)

Para que no te agarren en curva, esto es lo que AMPA **no** hace o hace con matices:

- **No genera lenguaje** (todavía no hay LLM): `responder` es **extractivo** (citas
  literales). La generación llegará como capa sobre las mismas citas (ADR 0011).
- **La clasificación de dominio es léxica**: si un texto no tiene términos
  distintivos, cae en `general`. Es explicable, no semántica.
- **La confianza es una heurística** (cobertura de términos): no entiende sinónimos.
- **La química es educativa, no un motor de simulación**:
  - El reconocedor por nombre evita términos muy ambiguos (p. ej. «radio»).
  - Las **reacciones** son plausibles/cualitativas (salvo la **combustión**, que sí
    se balancea); no es química cuántica.
  - La **geometría 3D** es un *layout* para visualizar: respeta longitudes ≈ radios
    covalentes y la conectividad, pero **no** modela ángulos ni estereoquímica.
  - Los **radios covalentes** son los de Cordero et al. (aproximados en superpesados).
  - La **termodinámica (ΔG)** usa datos estándar (298 K) **independientes de T**
    (aproximación de Ellingham): el **signo** y la **temperatura de cruce** orientan
    bien, pero no es DFT. Es **termodinámica, no cinética** (dice si *puede*, no si es
    *rápida*) y solo cubre las especies con datos en la tabla (ampliable).
- **Los datasets de filosofía son mínimos** (ampliables): cubren lo común.
- **La API y el CORS están pensados para uso local** (127.0.0.1); endurécelos antes
  de exponerlos en red.
- **El frontend necesita Node** para compilar; el **núcleo y la API, no**.

> ⚠️ AMPA es una herramienta **educativa y de investigación**. Sus salidas pueden
> contener errores; verifica lo importante con fuentes primarias.

---

## 11. Pruebas

```bash
python -m unittest discover -s tests -t .     # 143 pruebas, sin dependencias
```

Cada módulo tiene su archivo (`tests/test_*.py`). El frontend se valida con
`npm run build`. La CI (`.github/workflows/build.yml`) corre las pruebas y genera
los **ejecutables** para Windows/macOS/Linux en cada tag `v*`.

---

## 12. Estructura de carpetas

```
ampa/            núcleo (stdlib): core, perception, memory, scribe, answer, cycle,
                 chemistry, philosophy, api, cli
frontend/        app React (Vite): apartados, editor, visor 3D, animación
packaging/       empaquetado en ejecutable (PyInstaller)
cpp/             base C++ portable (CMake)
tests/           pruebas (unittest)
docs/            concepto-maestro, visión, arquitectura, roadmap, glosario,
                 módulos/, contratos/, 02-decisiones/ (ADRs)
.github/         CI
```

📚 Más: [Concepto Maestro](docs/concepto-maestro.md) ·
[Arquitectura](docs/01-arquitectura.md) ·
[Decisiones (ADR 0001–0016)](docs/02-decisiones/README.md) ·
[Roadmap](docs/03-roadmap.md) · [Glosario](docs/04-glosario.md) ·
[CHANGELOG](CHANGELOG.md)
