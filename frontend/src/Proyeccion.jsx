import { useState } from "react";
import { api } from "./api.js";

// Ejemplos clásicos (el umbral de Gibbs en acción).
const EJEMPLOS = [
  { n: "Sodio + agua", r: "Na, H2O", p: "NaOH, H2", t: 298 },
  { n: "Combustión de metano", r: "CH4, O2", p: "CO2, H2O", t: 298 },
  { n: "Óxido de sodio hidratado", r: "Na2O, H2O", p: "NaOH", t: 298 },
  { n: "Descomposición de caliza", r: "CaCO3", p: "CaO, CO2", t: 1200 },
  { n: "Síntesis de amoniaco", r: "N2, H2", p: "NH3", t: 298 },
  { n: "Oxidación del hierro", r: "Fe, O2", p: "Fe2O3", t: 298 },
];

// Color del veredicto.
const VERED = {
  "espontánea": { c: "#0cce6b", txt: "✅ ESPONTÁNEA", sub: "puede ocurrir sola (ΔG < 0)" },
  "no espontánea": { c: "#ff5c5c", txt: "❌ NO ESPONTÁNEA", sub: "la inversa es la favorable (ΔG > 0)" },
  "en equilibrio": { c: "#f5a623", txt: "⚖️ EN EQUILIBRIO", sub: "ΔG ≈ 0" },
};

export default function Proyeccion() {
  const [reactivos, setReactivos] = useState("Na, H2O");
  const [productos, setProductos] = useState("NaOH, H2");
  const [temp, setTemp] = useState(298);
  const [res, setRes] = useState(null);
  const [error, setError] = useState("");

  async function proyectar() {
    try {
      setError("");
      setRes(await api.proyectar(reactivos, productos, Number(temp)));
    } catch (e) {
      setError("" + e);
      setRes(null);
    }
  }

  function cargar(ej) {
    setReactivos(ej.r);
    setProductos(ej.p);
    setTemp(ej.t);
    setRes(null);
  }

  const v = res && res.ok ? VERED[res.veredicto] : null;

  return (
    <section className="card">
      <h3>🔮 Proyección termodinámica · ¿puede existir?</h3>
      <p className="hint">
        El <b>umbral</b> antes de tocar un tubo de ensayo: balanceo + Energía Libre
        de Gibbs (ΔG = ΔH − T·ΔS). Si ΔG &lt; 0, la reacción es espontánea.
      </p>

      <div className="ejemplos">
        {EJEMPLOS.map((ej) => (
          <button key={ej.n} className="ej" onClick={() => cargar(ej)}>
            {ej.n}
          </button>
        ))}
      </div>

      <label className="campo">
        <span>Reactivos</span>
        <input value={reactivos} onChange={(e) => setReactivos(e.target.value)}
               placeholder="Na, H2O" />
      </label>
      <div className="flecha">→</div>
      <label className="campo">
        <span>Productos</span>
        <input value={productos} onChange={(e) => setProductos(e.target.value)}
               placeholder="NaOH, H2" />
      </label>

      <div className="row tctrl">
        <span className="tlbl">Temperatura: <b>{temp} K</b> ({Math.round(temp - 273.15)} °C)</span>
        <input type="range" min="100" max="2000" step="10" value={temp}
               onChange={(e) => setTemp(e.target.value)} className="slider" />
      </div>

      <button onClick={proyectar}>Proyectar</button>
      {error && <p className="err">{error}</p>}

      {res && !res.ok && (
        <div className="result">
          <p className="alerta">⚠️ {res.razon}</p>
          {res.faltan && (
            <p className="hint">Sin datos termodinámicos para: {res.faltan.join(", ")}.</p>
          )}
        </div>
      )}

      {res && res.ok && (
        <div className="result proy">
          <p className="ecuacion">{res.ecuacion}</p>
          <div className="veredicto" style={{ borderColor: v.c, color: v.c }}>
            <b>{v.txt}</b>
            <span>{v.sub}</span>
          </div>
          <div className="termo-grid">
            <div className={"td " + (res.dH < 0 ? "neg" : "pos")}>
              <span className="tk">ΔH</span>
              <b>{res.dH}</b><span className="tu">kJ/mol</span>
              <span className="tn">{res.dH < 0 ? "exotérmica" : "endotérmica"}</span>
            </div>
            <div className={"td " + (res.dS > 0 ? "pos-s" : "neg-s")}>
              <span className="tk">ΔS</span>
              <b>{res.dS}</b><span className="tu">J/mol·K</span>
              <span className="tn">{res.dS > 0 ? "más desorden" : "menos desorden"}</span>
            </div>
            <div className={"td " + (res.dG < 0 ? "neg" : "pos")}>
              <span className="tk">ΔG</span>
              <b>{res.dG}</b><span className="tu">kJ/mol</span>
              <span className="tn">a {res.T} K</span>
            </div>
          </div>
          <p className="motor">⚙️ {res.motor}.</p>
          {res.t_cruce && (
            <p className="hint">
              🌡️ Temperatura de cruce (ΔG = 0): <b>{res.t_cruce} K</b>
              {" "}({Math.round(res.t_cruce - 273.15)} °C) — ahí cambia el veredicto.
            </p>
          )}
          <p className="nota">
            Valores estándar (298 K, 1 bar) extrapolados: guía cualitativa, no DFT.
          </p>
        </div>
      )}
    </section>
  );
}
