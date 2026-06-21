import { useEffect, useState } from "react";
import { api } from "./api.js";

const PALETA = ["C", "H", "O", "N", "S", "Cl", "P", "F"];
const COLOR = {
  H: "#dfe3ea", C: "#3a4150", O: "#e06c75", N: "#61afef",
  S: "#e5c07b", Cl: "#98c379", P: "#d19a66", F: "#56b6c2", Br: "#c0744a",
};
const colorDe = (el) => COLOR[el] || "#7a8290";
const TEXTO_OSCURO = new Set(["H", "F", "S", "Cl"]);
const W = 560;
const H = 320;
const R = 16;

export default function EditorVisual() {
  const [el, setEl] = useState("C");
  const [orden, setOrden] = useState(1);
  const [atomos, setAtomos] = useState([]); // { el, x, y }
  const [enlaces, setEnlaces] = useState([]); // { a, b, orden }
  const [sel, setSel] = useState(null);
  const [nombre, setNombre] = useState("");
  const [res, setRes] = useState(null);
  const [error, setError] = useState("");
  const [guardados, setGuardados] = useState([]);

  const cargar = () => api.listarCompuestos().then(setGuardados).catch(() => {});
  useEffect(() => { cargar(); }, []);

  function clicLienzo(e) {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = ((e.clientX - rect.left) * W) / rect.width;
    const y = ((e.clientY - rect.top) * H) / rect.height;
    setAtomos([...atomos, { el, x, y }]);
    setRes(null);
  }

  function clicAtomo(e, i) {
    e.stopPropagation();
    if (sel === null) { setSel(i); return; }
    if (sel === i) { setSel(null); return; }
    const mismo = (b) => (b.a === sel && b.b === i) || (b.a === i && b.b === sel);
    if (enlaces.some(mismo)) {
      setEnlaces(enlaces.map((b) => (mismo(b) ? { ...b, orden } : b)));
    } else {
      setEnlaces([...enlaces, { a: sel, b: i, orden }]);
    }
    setSel(null);
    setRes(null);
  }

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

  function Enlace(b, i) {
    const A = atomos[b.a];
    const B = atomos[b.b];
    if (!A || !B) return null;
    const dx = B.x - A.x;
    const dy = B.y - A.y;
    const len = Math.hypot(dx, dy) || 1;
    const ox = -dy / len;
    const oy = dx / len;
    const offsets = b.orden === 1 ? [0] : b.orden === 2 ? [-3, 3] : [-5, 0, 5];
    return offsets.map((o, k) => (
      <line
        key={`${i}-${k}`}
        x1={A.x + ox * o} y1={A.y + oy * o}
        x2={B.x + ox * o} y2={B.y + oy * o}
        stroke="#8a93a3" strokeWidth="2"
      />
    ));
  }

  return (
    <section className="card">
      <h3>Editor de enlaces de carbono</h3>
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
        Clic en el lienzo = añadir átomo · clic en dos átomos = enlazar · clic en uno (otra vez) = cancelar
      </p>
      <svg className="lienzo" viewBox={`0 0 ${W} ${H}`} onClick={clicLienzo}>
        {enlaces.map(Enlace)}
        {atomos.map((a, i) => (
          <g key={i} onClick={(e) => clicAtomo(e, i)} style={{ cursor: "pointer" }}>
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
