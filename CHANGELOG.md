# Changelog

Todos los cambios notables del proyecto se documentan aquí.
Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
versionado según [SemVer](https://semver.org/lang/es/).

## [No publicado]

### Añadido
- **Capa de percepción** (`ampa/perception/`): contrato de evento (§5.2),
  clasificador de dominio por reglas, evaluación de riesgo y política de memoria.
- **Comando `ampa percibir`** y 13 pruebas; contrato `docs/contratos/evento.md`,
  módulo `docs/modulos/percepcion.md` y **ADR 0008**.
- **Diario de eventos** (`ampa/perception/journal.py`, JSONL) y comando
  `ampa diario`: persiste los eventos marcados para guardar (cubre el pendiente
  «logs» de la Fase 2). +5 pruebas.
- **Escriba seguro** (`ampa/scribe/`) y comandos `ampa escribir` / `ampa restaurar`:
  escritura atómica y portable con respaldo previo, *rollback*, modo simulación
  (`--simular`) y bloqueo por riesgo alto (`--forzar`). Módulo
  `docs/modulos/escriba.md` y **ADR 0009**. +8 pruebas (**44** en total).
- **Memoria documental** (`ampa/memory/`): ingesta de apuntes con troceo
  (chunking) y etiquetado de dominio, y **recuperación con citas** mediante
  ranking léxico **BM25** (sin dependencias). Comandos `ampa recordar`,
  `ampa consultar` y `ampa memoria`. Módulo `docs/modulos/memoria.md` y
  **ADR 0010**. +6 pruebas (**50** en total).
- **Respuesta con fuentes** (`ampa/answer/`) y comando `ampa responder`
  (`--detalle`): une percepción y memoria para devolver una respuesta
  **extractiva y citada**, honesta cuando no hay evidencia (no inventa). Incluye
  filtrado de palabras vacías en la recuperación. Módulo
  `docs/modulos/respuesta.md` y **ADR 0011**. +5 pruebas (**55** en total).
- **Ciclo percepción → memoria → acción** (`ampa/cycle/`) y comando `ampa ciclo`:
  percibe, recupera contexto citado y **propone** una escritura segura; con
  `--ejecutar` recuerda (diario + memoria) y escribe con respaldo bajo la puerta
  de riesgo (`--forzar`). Módulo `docs/modulos/ciclo.md` y **ADR 0012**.
  +4 pruebas (**59** en total).
- **Ingesta de carpeta**: `ampa recordar --carpeta apuntes/` ingiere
  recursivamente los `.md`/`.txt` (omite ilegibles), con citas por ruta relativa
  (POSIX). +2 pruebas (**61** en total).
- **Reconocimiento químico** (`ampa/chemistry/`) y comando `ampa quimica`
  (`--json`): identifica **elementos** y **compuestos** (por nombre o fórmula) y
  los entrega estructurados (símbolo, Z, composición) para usos visuales. Incluye
  tabla periódica (118) y parser de fórmulas. Módulo `docs/modulos/quimica.md` y
  **ADR 0013**. +7 pruebas (**68** en total).
- **Capa epistémica** en `ampa responder`: cada respuesta indica su **confianza**
  (cobertura de términos + dominio, **ADR 0014**) y su **origen**, y señala la
  **química detectada** (integra `chemistry`). +1 prueba (**69** en total).
- **Química visual-ready**: cada elemento incluye **masa, grupo, periodo y
  categoría**; se calcula la **masa molar** de los compuestos; `ampa quimica
  --tabla` vuelca la tabla periódica (con `--json`). Diccionario de compuestos
  ampliado. +3 pruebas (**72** en total).
- **Reconocimiento de filosofía** (`ampa/philosophy/`) y comando `ampa filosofia`
  (`--json`): identifica **filósofos** (época y corriente), **corrientes** y
  **conceptos** (rama). Módulo `docs/modulos/filosofia.md`. Cierra «base de
  filosofía» y «pruebas por dominio» de la Fase 6. +5 pruebas (**77** en total).
- **Cuaderno y diccionario personal de filosofía** (`ampa/philosophy/notebook.py`):
  `ampa pensar "..."` guarda tus pensamientos (términos `--sobre` o autodetectados)
  y `ampa diccionario [término] [--json]` los conserva y agrupa. Capa **adaptativa**:
  el diccionario crece con lo que pones. +3 pruebas (**80** en total).
- **Modelo de moléculas y compuestos** (`ampa/chemistry/molecules.py`): `Molecula`
  (átomos + enlaces) deriva fórmula (Hill), composición y masa molar; `ampa
  compuesto guardar|listar|analizar` **guarda tus compuestos** (JSON portable).
  Base del editor de enlaces de carbono. +4 pruebas (**84** en total).
- **Editor de carbono — grupos funcionales y reacciones** (`ampa/chemistry/groups.py`
  y `reactions.py`): detecta grupos (alcohol, ácido, alqueno, cetona, amina…) sobre
  el grafo de enlaces e infiere reacciones (**combustión balanceada**, hidrogenación,
  neutralización…); `ampa compuesto analizar` las muestra (con `--json`). Completa
  «los tres» del editor. +8 pruebas (**92** en total).
- **API JSON portable** (`ampa/api/`, comando `ampa servir`): expone química y
  filosofía por HTTP/JSON con **cero dependencias** (`http.server`) y CORS, lista
  para un frontend React. Despacho puro y testeable (`manejar`). **ADR 0015** y
  módulo `docs/modulos/api.md`. +7 pruebas (**99** en total).
- **Frontend React (Vite)** en `frontend/`: interfaz fresca con **dos apartados**
  (Química / Filosofía) que consume la API. Incluye **tabla periódica interactiva**
  (coloreada por categoría), identificación, **editor visual de enlaces** (dibujas
  la molécula con clics en un lienzo SVG → fórmula, masa, grupos y reacciones, y
  guardas el compuesto) y el **cuaderno/diccionario** personal. `npm run build`
  verificado.
- **Editor visual con modos**: construir / **mover** (arrastrar átomos) / **borrar**
  (eliminar átomos y enlaces) en el lienzo SVG.
- **Más reacciones** (halogenación de alcanos y alquenos, hidratación, deshidratación,
  saponificación, reducción…) y **endpoint `POST /api/quimica/reacciones`**.
  +4 pruebas (**106** en total).
- **Ejecutable único** (`packaging/build_exe.py`, PyInstaller): un binario que sirve
  **web + API** sin Python ni Node; el servidor localiza el frontend incrustado vía
  `sys._MEIPASS`. Verificado de extremo a extremo.
- **🧊 Visor 3D de moléculas (desde cero, sin librerías)**: endpoint
  `POST /api/quimica/geometria` (layout 3D por fuerzas, stdlib) + visor en `canvas`
  con proyección y rotación **a mano** (gira solo; arrastras para rotar). Dibujas la
  molécula en 2D y la ves girar en 3D. +5 pruebas (**111** en total).
- **Editor**: **plantillas** (agua, metano, CO₂, eteno, etanol, benceno) y
  **exportar PNG** de la molécula.
- **CI** (`.github/workflows/build.yml`): compila el frontend, corre las pruebas y
  genera el **ejecutable para Windows, macOS y Linux** en cada tag `v*`.
- **Visor 3D mejorado**: enlaces **dobles/triples** (líneas paralelas) y tamaño de
  átomo por **radio covalente real** (118 elementos, Cordero et al.); la geometría
  usa longitudes de enlace ≈ suma de radios.
- **🎬 Animación de combustión**: los átomos se **reorganizan** de reactivos a
  productos (conservación de la materia) con la ecuación balanceada en vivo.
- **Documentación a fondo**: `README.md` maestro (qué hace cada cosa, para qué,
  cómo actúa y las consideraciones) y módulo `docs/modulos/frontend.md`.
- **Química viva en el editor**: **electronegatividad** y **valencia** en los 118
  elementos; `analizar_enlaces` (saturación de valencia + **polaridad** por Δ
  electronegatividad) en `POST /api/quimica/analizar`. El editor colorea enlaces por
  polaridad y átomos por saturación; input de **temperatura** que hace **vibrar** el
  visor 3D. +4 pruebas (**115** en total).
- **Animación de reacciones**: además de combustión, **hidrogenación** y
  **neutralización**.
- **🕸️ Grafo de conocimiento (estilo Obsidian)** en Filosofía: términos como nodos,
  co-ocurrencia como aristas, con layout de fuerzas en vivo e interacción.
- **🔮 Termodinámica — la Energía Libre de Gibbs como umbral de existencia**
  (`ampa/chemistry/{balance,thermo,compatibility}.py`, **ADR 0016** y módulo
  `docs/modulos/termodinamica.md`): **balanceo general** de ecuaciones por espacio
  nulo (`Fraction`, exacto); **ΔG = ΔH − T·ΔS** con datos estándar curados (ΔHf°,
  S°), **temperatura de cruce** y motor entálpico/entrópico; **compatibilidad** entre
  elementos (tipo de enlace por ΔEN, fórmula por aspa de cargas y ΔG de formación).
  Endpoints `POST /api/quimica/{balancear,proyectar,compatibilidad}`. Reproduce los
  casos clásicos (Na+agua, el óxido hidratado que colapsa a NaOH, la caliza a ~1120 K).
  +27 pruebas (**142** en total).
- **Frontend de proyección**: `Proyeccion.jsx` (reactivos→productos + slider de
  temperatura → ecuación, ΔH/ΔS/ΔG y veredicto con color) y `Compatibilidad.jsx`
  (dos elementos → enlace, fórmula y ΔG). Estilos nuevos.
- **Editor — encadenar átomos**: arrastrar desde un átomo crea átomo + enlace en un
  gesto (o enlaza si sueltas sobre otro), con línea guía. **Visor 3D**: exportar PNG.
- **Grafo enriquecido**: **buscador** (resalta/atenúa) y **agrupar por
  época/corriente** con leyenda de colores (`POST /api/filosofia/clasificar`).
  +1 prueba (**143** en total).
- **🎨 Rediseño con estética Vercel**: paleta monocroma (negro/grises + acento azul),
  bordes finos, tipografía apretada y mucho aire; sistema de diseño con tokens en
  `styles.css`. **Responsivo** (móvil y escritorio) y **guía rápida** de onboarding
  (3 pasos por apartado) con subtítulos que explican cada tarjeta.
- **🧭 Filosofía concluida**: nuevo `Explorar` (catálogo navegable de filósofos por
  época, corrientes y conceptos por rama) que **siembra el cuaderno** al tocarlo
  (flujo explorar → escribir → grafo). Endpoint `GET /api/filosofia/catalogo`.
  +1 prueba (**144** en total).
- **Cliente al mismo origen**: en producción la web llama a la API en su **propio
  origen** (cualquier puerto), no a un `127.0.0.1:8000` fijo.
- **Arreglo**: el grafo ya no rompía la pestaña de Filosofía cuando el diccionario
  estaba vacío (se protege el `canvas` antes de dibujar).
- **Compuestos como plantillas** (`Compuestos.jsx`): lo que guardas se puede
  **cargar** al editor (con *layout* 2D reconstruido), **analizar** en sitio o
  **proyectar** (ΔG) con un clic. Estado elevado en `Quimica.jsx`.
- **Notificaciones** (`Toast.jsx`, contexto `useToast`): aviso al guardar (y al
  fallar), abajo y autodescartable, sin librerías.
- **Iconos minimalistas** (`Icon.jsx`): set de SVG de línea (`currentColor`) con
  *hovers* suaves que **reemplazan todos los emojis** de la interfaz.
- **Atajos de teclado** en el editor (`C`/`M`/`B`/`1`·`2`·`3`/`Esc`) **auto-explicados**
  (teclas en `<kbd>` y línea de atajos) + **barra desplegable** «Más» para las
  herramientas secundarias.
- **Barra de navegación inferior** en móvil (las pestañas se mueven abajo).
- **`ampa ampakadabra`** ✨: un solo comando que **conjura web + API** — compila el
  frontend si hace falta, lo sirve junto a la API desde el **mismo servidor** (un
  artefacto portable) y abre el navegador. La API sirve el build de React con
  fallback SPA. +2 pruebas (**101** en total).
- **Filosofía en `responder`**: la respuesta señala también los **filósofos,
  corrientes y conceptos** detectados, simétrico a la química. +1 prueba
  (**102** en total).
- **Núcleo portable** (`ampa/core/`): detección de plataforma (`platform_info.py`)
  y rutas multiplataforma (`paths.py`), solo con biblioteca estándar.
- **CLI portable** (`ampa/cli/`): comandos `info`, `version` y `paths`.
- **Pruebas** con `unittest` (18 casos): plataforma, rutas (Windows/macOS/Linux
  simulados) y CLI.
- **Base C++ portable** (`cpp/`): proyecto CMake y sonda `ampa-probe` con
  aleatoriedad reproducible (`std::mt19937_64`).
- `pyproject.toml`: empaquetado, *entry point* `ampa`, núcleo sin dependencias.
- Documento de módulo `docs/modulos/core.md` y **ADR 0007** (portabilidad).
- ADR 0004–0006 (dominios, apuntes/escriba, memoria/simulaciones), `CITATION.cff`.

### Cambiado
- **Concepto Maestro actualizado a v0.2**: ejes lenguaje/percepción/memoria, capa de
  percepción, ciclo percepción‑memoria‑acción, sistema de documentación controlada
  y regla final de control.
- Dominios del proyecto: a **química** (eje científico) y **filosofía** (lente).
- Visión, arquitectura, roadmap, glosario y base de conocimiento alineados.

## [0.0.1] - 2026-06-18

### Añadido
- Fundación de documentación: visión, arquitectura, ADRs 0001–0003, roadmap,
  glosario y base de conocimiento.
- `.gitignore` para modelos, datos y artefactos de compilación.
