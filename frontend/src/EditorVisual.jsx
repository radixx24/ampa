import { useEffect, useRef, useState } from "react";
import { api } from "./api.js";

const PALETA = ["C", "H", "O", "N", "S", "Cl", "P", "F"];
const COLOR = {
  H: "#dfe3ea", C: "#3a4150", O: "#e06c75", N: "#61afef",
  S: "#e5c07b", Cl: "#98c379", P: "#d19a66", F: "#56b6c2", Br: "#c0744a",
};
const colorDe = (el) => COLOR[el] || "#7a8290";
const TEXTO_OSCURO = new Set(["H", "F", "S", "Cl"]);
const MODOS = [
  ["construir", "✏️ Construir"],
  ["mover", "✋ Mover"],
  ["borrar", "🗑 Borrar"],
];
const W = 560;
const H = 320;
const R = 16;

export default function EditorVisual() {
  const svgRef = useRef(null);
  const [el, setEl] = useState("C");
  const [orden, setOrden] = useState(1);
  const [modo, setModo] = useState("construir");
  const [atomos, setAtomos] = useState([]); // { el, x, y }
  const [enlaces, setEnlaces] = useState([]); // { a, b, orden }
  const [sel, setSel] = useState(null);
  const [arrastrando, setArrastrando] = useState(null);
  const [nombre, setNombre] = useState("");
  const [res, setRes] = useState(null);
  const [error, setError] = useState("");
  const [guardados, setGuardados] = useState([]);

  const cargar = () => api.listarCompuestos().then(setGuardados).catch(() => {});
  useEffect(() => { cargar(); }, []);

  function coords(e) {
    const r = svgRef.current.getBoundingClientRect();
    return [((e.clientX - r.left) * W) / r.width, ((e.clientY - r.top) * H) / r.height];
  }

  function clicLienzo(e) {
    if (modo !== "construir") return;
    const [x, y] = coords(e);
    setAtomos([...atomos, { el, x, y }]);
    setRes(null);
  }

  function clicAtomo(e, i) {
    e.stopPropagation();
    if (modo === "borrar") { borrarAtomo(i); return; }
    if (modo !== "construir") return;
    if (sel === null) { setSel(i); return; }
    if (sel === i) { setSel(null); return; }
    const mismo = (b) => (b.a === sel && b.b === i) || (b.a === i && b.b === sel);
    if (enlaces.some(mismo)) setEnlaces(enlaces.map((b) => (mismo(b) ? { ...b, orden } : b)));
    else setEnlaces([...enlaces, { a: sel, b: i, orden }]);
    setSel(null);
    setRes(null);
  }

  function borrarAtomo(i) {
    setAtomos(atomos.filter((_, j) => j !== i));
    setEnlaces(
      enlaces
        .filter((b) => b.a !== i && b.b !== i)
        .map((b) => ({ a: b.a > i ? b.a - 1 : b.a, b: b.b > i ? b.b - 1 : b.b, orden: b.orden }))
    );
    setSel(null);
    setRes(null);
  }
  function borrarEnlace(idx) {
    setEnlaces(enlaces.filter((_, j) => j !== idx));
    setRes(null);
  }

  function onPointerDownAtomo(e, i) {
    if (modo !== "mover") return;
    e.stopPropagation();
    setArrastrando(i);
  }
  function onPointerMove(e) {
    if (arrastrando === null || modo !== "mover") return;
    const [x, y] = coords(e);
    setAtomos(atomos.map((a, j) => (j === arrastrando ? { ...a, x, y } : a)));
  }
  const finArrastre = () => setArrastrando(null);

  const molecula = () => ({
    nombre,
    atomos: atomos.map((a) => a.el),
    enlaces: enlaces.map((b) => [b.a, b.b, b.orden]),
  });

  async function analizar() {
    try { setError(""); setRes(await api.analizar(molecula())); }
    catch (e) { setError("" + e); }
  }
  async function guardar() {
    try { setError(""); await api.guardarCompuesto(molecula()); cargar(); }
    catch (e) { setError("" + e); }
  }
  function limpiar() {
    setAtomos([]); setEnlaces([]); setSel(null); setRes(null); setError("");
  }

  return (
    <section className="card">
      <h3>Editor de enlaces de carbono</h3>
      <div className="paleta">
        <span>Modo:</span>
        {MODOS.map(([m, etiqueta]) => (
          <button key={m} className={"pchip " + (modo === m ? "on" : "")} onClick={() => { setModo(m); setSel(null); }}>
            {etiqueta}
          </button>
        ))}
      </div>
      <div className="paleta">
        <span>Átomo:</span>
        {PALETA.map((s) => (
          <button
            key={s}
            className={"pchip " + (el === s ? "on" : "")}
            style={{ background: colorDe(s), color: TEXTO_OSCURO.has(s) ? "#1a1f27" : "#fff" }}
            onClick={() => setEl(s)}
          >
            {s}
          </button>
        ))}
        <span className="sep">Enlace:</span>
        {[1, 2, 3].map((o) => (
          <button key={o} className={"pchip " + (orden === o ? "on" : "")} onClick={() => setOrden(o)}>
            {["—", "═", "≡"][o - 1]}
          </button>
        ))}
      </div>
      <p className="hint">
        {modo === "construir" && "Clic en el lienzo = átomo · clic en dos átomos = enlace"}
        {modo === "mover" && "Arrastra los átomos para reacomodarlos"}
        {modo === "borrar" && "Clic en un átomo o un enlace para eliminarlo"}
      </p>
      <svg
        ref={svgRef}
        className={"lienzo modo-" + modo}
        viewBox={`0 0 ${W} ${H}`}
        onClick={clicLienzo}
        onPointerMove={onPointerMove}
        onPointerUp={finArrastre}
        onPointerLeave={finArrastre}
      >
        {enlaces.map((b, i) => {
          const A = atomos[b.a];
          const B = atomos[b.b];
          if (!A || !B) return null;
          const dx = B.x - A.x;
          const dy = B.y - A.y;
          const len = Math.hypot(dx, dy) || 1;
          const ox = -dy / len;
          const oy = dx / len;
          const offsets = b.orden === 1 ? [0] : b.orden === 2 ? [-3, 3] : [-5, 0, 5];
          return (
            <g key={i}>
              <line
                x1={A.x} y1={A.y} x2={B.x} y2={B.y}
                stroke="transparent" strokeWidth="14"
                style={{ pointerEvents: modo === "borrar" ? "stroke" : "none", cursor: "pointer" }}
                onClick={(e) => { e.stopPropagation(); borrarEnlace(i); }}
              />
              {offsets.map((o, k) => (
                <line
                  key={k}
                  x1={A.x + ox * o} y1={A.y + oy * o}
                  x2={B.x + ox * o} y2={B.y + oy * o}
                  stroke="#8a93a3" strokeWidth="2"
                />
              ))}
            </g>
          );
        })}
        {atomos.map((a, i) => (
          <g
            key={i}
            onClick={(e) => clicAtomo(e, i)}
            onPointerDown={(e) => onPointerDownAtomo(e, i)}
            style={{ cursor: modo === "mover" ? "grab" : "pointer" }}
          >
            <circle
              cx={a.x} cy={a.y} r={R} fill={colorDe(a.el)}
              stroke={sel === i ? "#6ee7b7" : "#0e1116"} strokeWidth={sel === i ? 3 : 2}
            />
            <text
              x={a.x} y={a.y + 4} textAnchor="middle" fontSize="13" fontWeight="700"
              fill={TEXTO_OSCURO.has(a.el) ? "#1a1f27" : "#fff"}
            >
              {a.el}
            </text>
          </g>
        ))}
      </svg>
      <div className="row">
        <input
          className="nombre" value={nombre}
          onChange={(e) => setNombre(e.target.value)} placeholder="nombre (opcional)"
        />
        <button onClick={analizar} disabled={!atomos.length}>Analizar</button>
        <button className="sec" onClick={guardar} disabled={!atomos.length}>Guardar</button>
        <button className="sec" onClick={limpiar}>Limpiar</button>
      </div>
      {error && <p className="err">{error}</p>}
      {res && (
        <div className="result">
          <p className="formula"><b>{res.formula}</b> · {res.masa_molar} g/mol</p>
          <p>
            Grupos:{" "}
            {res.grupos_funcionales.length
              ? res.grupos_funcionales.map((g, i) => <span key={i} className="chip">{g}</span>)
              : "—"}
          </p>
          {res.reacciones.length > 0 && (
            <ul className="reacciones">
              {res.reacciones.map((r, i) => (
                <li key={i}><span className="tipo">{r.tipo}</span> {r.ecuacion}</li>
              ))}
            </ul>
          )}
        </div>
      )}
      {guardados.length > 0 && (
        <div className="guardados">
          <h4>Tus compuestos ({guardados.length})</h4>
          <ul>
            {guardados.map((m, i) => (
              <li key={i}>{m.nombre || "(sin nombre)"} — <b>{m.formula}</b> · {m.masa_molar} g/mol</li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
