import { useState } from "react";
import { api } from "./api.js";

const PARES = [
  ["Na", "Cl"], ["Al", "O"], ["Ca", "O"], ["C", "O"], ["Fe", "Cu"], ["Ne", "F"],
];

// Color por tipo de enlace.
const ENLACE_COLOR = {
  "iónico": "#fbbf24",
  "covalente polar": "#60a5fa",
  "covalente no polar": "#6ee7b7",
  "metálico": "#c084fc",
  "inerte": "#9aa7b4",
};

const REACT_COLOR = {
  "muy alta": "#f87171", "alta": "#fb923c", "media": "#fbbf24",
  "baja": "#6ee7b7", "nula": "#9aa7b4",
};

export default function Compatibilidad() {
  const [a, setA] = useState("Na");
  const [b, setB] = useState("Cl");
  const [temp, setTemp] = useState(298);
  const [res, setRes] = useState(null);
  const [error, setError] = useState("");

  async function evaluar() {
    try {
      setError("");
      setRes(await api.compatibilidad(a, b, Number(temp)));
    } catch (e) {
      setError("" + e);
      setRes(null);
    }
  }

  return (
    <section className="card">
      <h3>🧲 Compatibilidad entre elementos</h3>
      <p className="hint">
        ¿Se llevan? Tipo de enlace (por ΔEN), fórmula probable (aspa de cargas) y
        si su unión es favorable a esta temperatura (ΔG).
      </p>

      <div className="pares">
        {PARES.map(([x, y]) => (
          <button key={x + y} className="ej" onClick={() => { setA(x); setB(y); setRes(null); }}>
            {x}+{y}
          </button>
        ))}
      </div>

      <div className="row compat-in">
        <input className="elin" value={a} onChange={(e) => setA(e.target.value)} placeholder="Na" />
        <span className="mas">+</span>
        <input className="elin" value={b} onChange={(e) => setB(e.target.value)} placeholder="Cl" />
        <button onClick={evaluar}>Evaluar</button>
      </div>

      <div className="row tctrl">
        <span className="tlbl">T: <b>{temp} K</b></span>
        <input type="range" min="100" max="2000" step="10" value={temp}
               onChange={(e) => setTemp(e.target.value)} className="slider" />
      </div>

      {error && <p className="err">{error}</p>}
      {res && !res.ok && <p className="alerta">⚠️ {res.razon}</p>}

      {res && res.ok && (
        <div className="result">
          <div className="compat-cabeza">
            <span className="bola">{res.a}</span>
            <span className="mas">+</span>
            <span className="bola">{res.b}</span>
            {res.producto && <><span className="mas">→</span><span className="prod">{res.producto}</span></>}
          </div>
          <div className="badges">
            <span className="badge" style={{ borderColor: ENLACE_COLOR[res.tipo_enlace] }}>
              enlace {res.tipo_enlace}
            </span>
            {res.delta_en != null && <span className="badge">ΔEN {res.delta_en}</span>}
            <span className="badge" style={{ borderColor: REACT_COLOR[res.reactividad] }}>
              reactividad {res.reactividad}
            </span>
          </div>
          <p className="veredicto-txt">{res.veredicto}</p>
          {res.termo && res.termo.ok && (
            <p className="hint">
              Formación: ΔG = <b>{res.termo.dG} kJ/mol</b> a {res.termo.T} K · {res.termo.motor}.
            </p>
          )}
        </div>
      )}
    </section>
  );
}
