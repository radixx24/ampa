// Cliente de la API de AMPA. La URL base se puede sobreescribir con VITE_AMPA_API.
const BASE = import.meta.env.VITE_AMPA_API || "http://127.0.0.1:8000";

async function get(path) {
  const r = await fetch(BASE + path);
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

async function post(path, body) {
  const r = await fetch(BASE + path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) {
    let msg = `HTTP ${r.status}`;
    try {
      msg = (await r.json()).error || msg;
    } catch (_) {}
    throw new Error(msg);
  }
  return r.json();
}

export const api = {
  salud: () => get("/api/salud"),
  tabla: () => get("/api/quimica/tabla"),
  identificarQuimica: (texto) => post("/api/quimica/identificar", { texto }),
  analizar: (molecula) => post("/api/quimica/analizar", molecula),
  geometria: (molecula) => post("/api/quimica/geometria", molecula),
  balancear: (reactivos, productos) =>
    post("/api/quimica/balancear", { reactivos, productos }),
  proyectar: (reactivos, productos, temperatura) =>
    post("/api/quimica/proyectar", { reactivos, productos, temperatura }),
  compatibilidad: (a, b, temperatura) =>
    post("/api/quimica/compatibilidad", { a, b, temperatura }),
  listarCompuestos: () => get("/api/quimica/compuestos"),
  guardarCompuesto: (molecula) => post("/api/quimica/compuestos", molecula),
  identificarFilosofia: (texto) => post("/api/filosofia/identificar", { texto }),
  pensar: (texto, terminos) => post("/api/filosofia/pensar", { texto, terminos }),
  diccionario: () => get("/api/filosofia/diccionario"),
  clasificar: (terminos) => post("/api/filosofia/clasificar", { terminos }),
};

// Normaliza una categoría a una clase CSS (sin acentos ni espacios).
export const slug = (s) =>
  (s || "")
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/\s+/g, "-");
