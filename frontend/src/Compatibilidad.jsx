import { useState } from "react";
import { api } from "./api.js";
import Icon from "./Icon.jsx";

const PARES = [
  ["Na", "Cl"], ["Al", "O"], ["Ca", "O"], ["C", "O"], ["Fe", "Cu"], ["Ne", "F"],
];

// Color por tipo de enlace.
const ENLACE_COLOR = {
  "iónico": "#f5a623",
  "covalente polar": "#3291ff",
  "covalente no polar": "#0cce6b",
  "metálico": "#c084fc",
  "inerte": "#a1a1a1",
};

const REACT_COLOR = {
  "muy alta": "#ff5c5c", "alta": "#fb923c", "media": "#f5a623",
  "baja": "#0cce6b", "nula": "#a1a1a1",
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
      <h3><Icon name="link" /> Compatibilidad entre elementos</h3>
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
      {res && !res.ok && <p className="alerta"><Icon name="info" size={14} /> {res.razon}</p>}

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
