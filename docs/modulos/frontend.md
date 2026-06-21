# Módulo: frontend (interfaz web)

> Documentado según la plantilla del Concepto Maestro §12.
> Código: `frontend/` (React + Vite) · Consume: la API (`ampa/api`, ADR 0015)

## 1. Propósito

Dar una interfaz **visual, fresca y portable** a AMPA, con **dos apartados**
(Química y Filosofía), para *ver* lo que se proyecta: tabla periódica, editor de
moléculas, **visor 3D** y **animación de reacciones**. Es la "cara"; el "cerebro"
sigue en el núcleo Python.

## 2. Responsabilidad exacta

**Hace:**
- Renderiza los dos apartados y habla con la API por **HTTP/JSON** (`src/api.js`).
- **Tabla periódica** interactiva (color por categoría, posición por grupo/periodo).
- **Editor de enlaces** con **química viva**: construir/mover/borrar, plantillas,
  PNG, **enlaces coloreados por polaridad** y **átomos por saturación de valencia**,
  e input de **temperatura**.
- **Visor 3D** (sin librerías): enlaces dobles/triples, tamaño por radio y
  **vibración térmica** según la temperatura.
- **Animación de reacciones**: combustión (átomo a átomo), hidrogenación y
  neutralización.
- **Cuaderno/diccionario** + **grafo de conocimiento** (estilo Obsidian) de filosofía.

**No hace:**
- No contiene lógica de dominio: **toda** la química/filosofía vive en el núcleo y
  se pide a la API. El front solo dibuja e interactúa.
- No persiste nada por su cuenta (la API/núcleo guardan).

## 3. Entradas

- Respuestas JSON de la API (tabla, identificación, análisis de molécula,
  geometría 3D, diccionario…).
- Interacción del usuario (clics, arrastre, texto).
- Variable `VITE_AMPA_API` para apuntar a otra URL de la API (def. `127.0.0.1:8000`).

## 4. Salidas

- Vistas renderizadas; peticiones a la API; descargas (PNG).
- Build estático en `frontend/dist/` (lo sirve la propia API / el ejecutable).

## 5. Componentes

| Archivo | Qué hace |
|---|---|
| `App.jsx` | Cabecera, pestañas (Química/Filosofía), estado de salud de la API. |
| `api.js` | Cliente HTTP (`get`/`post`) y helper `slug`. |
| `Quimica.jsx` | Tabla periódica + identificar + monta el editor. |
| `EditorVisual.jsx` | Editor SVG de moléculas (modos, plantillas, PNG, botones 3D/animación). |
| `Visor3D.jsx` | Visor 3D en `canvas` (rotación/proyección a mano + vibración térmica). |
| `ReaccionAnimada.jsx` | Animación de reacciones (combustión / hidrogenación / neutralización). |
| `GrafoFilosofia.jsx` | Grafo de conocimiento (física en vivo) del diccionario. |
| `Filosofia.jsx` | Identificar + cuaderno/diccionario + grafo. |
| `styles.css` | Tema oscuro, sin librerías de estilo. |

## 6. Flujo interno (las dos joyas, a detalle)

### Editor de moléculas (`EditorVisual`)
- Estado: `atomos` (`{el, x, y}`), `enlaces` (`{a, b, orden}`), `modo`.
- **Construir**: clic en el lienzo añade un átomo del elemento elegido; clic en dos
  átomos crea un enlace del orden elegido.
- **Mover**: `pointerdown` sobre un átomo + `pointermove` actualiza su posición.
- **Borrar**: clic en un átomo lo elimina y **reindexa** los enlaces; clic en un
  enlace (con *hitbox* ancha) lo elimina.
- Para analizar/guardar/ver en 3D, construye `{nombre, atomos:[el…],
  enlaces:[[a,b,orden]…]}` y lo manda a la API.

### Visor 3D (`Visor3D`) — sin librerías
1. Pide `POST /api/quimica/geometria` → coordenadas 3D (con `radio` por átomo).
2. En cada frame (`requestAnimationFrame`) rota los puntos con **matrices de
   rotación** en X e Y (calculadas a mano).
3. Proyecta a 2D con **perspectiva** (`persp = 5 / (5 + z)`).
4. Ordena los átomos por profundidad (*painter's algorithm*: dibuja primero los de
   atrás) y los pinta como esferas con **degradado radial** (color CPK).
5. Enlaces **dobles/triples** = líneas paralelas (desplazamiento perpendicular en el
   plano proyectado). El tamaño de cada átomo escala con su **radio covalente**.
6. Gira solo; el arrastre del puntero ajusta los ángulos de rotación.

### Animación de combustión (`ReaccionAnimada`)
1. **Balancea** la combustión en JS (multiplicando por 4 para evitar fracciones):
   `CcHhOo → CO2 y H2O`, con coeficientes enteros reducidos por su MCD.
2. Coloca los **reactivos** (la molécula + moléculas de O₂) a la izquierda y los
   **productos** (CO₂ y H₂O) a la derecha, como pequeños grupos.
3. **Empareja los átomos por elemento** entre reactivos y productos (la materia se
   conserva: hay la misma cantidad de cada elemento a ambos lados).
4. Anima `t: 0→1` interpolando cada átomo de su sitio en los reactivos a su sitio en
   los productos (con un arco y un **destello** central); los enlaces de reactivos
   se desvanecen y los de productos aparecen. Muestra la **ecuación balanceada**.

### Química viva (editor)
- Tras **Analizar**, el editor pide a la API el análisis de enlaces y **colorea**:
  cada enlace por su **polaridad** (no polar / polar / iónico) y cada átomo por su
  **saturación de valencia** (libre / saturado / sobreenlazado, con alerta global).
- La **temperatura** (K) se pasa al visor 3D, que añade una **vibración** a los
  átomos proporcional a `T` (a más calor, más agitación). Es visual y orientativo.

### Grafo de conocimiento (`GrafoFilosofia`) — estilo Obsidian
- Construye un grafo: **nodos** = términos del diccionario (tamaño por nº de
  pensamientos), **aristas** = términos que **co-ocurren** en un mismo pensamiento.
- Lo acomoda con un **layout de fuerzas en vivo** (repulsión + resortes + gravedad
  al centro); al **clic** en un nodo resalta sus conexiones y lista los pensamientos
  de ese término. Así organizas y *ves* tus ideas conectadas.

## 7. Errores esperados

- API caída → el indicador marca "API offline"; cada panel muestra el error.
- Molécula inválida (p. ej. enlace fuera de rango) → la API responde **400** y el
  editor muestra el mensaje.
- Molécula no combustible → el botón de animación se deshabilita.

## 8. Seguridad y límites

- El front **no** valida química: confía en la API (que sí valida). Es solo vista.
- Pensado para uso **local**; la URL de la API es configurable.
- Necesita **Node** para compilar; el resultado (`dist/`) es estático y portable.

## 9. Pruebas / verificación

- Se valida con **`npm run build`** (compila sin errores).
- La lógica de dominio que consume ya está cubierta por las pruebas del núcleo
  (`tests/test_*.py`).

## 10. Cambios pendientes

- Arrastrar para **encadenar** átomos (crear átomo + enlace en un gesto).
- Exportar la vista 3D como imagen y compartir moléculas por enlace.
- Enriquecer el grafo (filtros, agrupar por época/corriente).
