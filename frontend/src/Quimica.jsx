import { useEffect, useState } from "react";
import { api, slug } from "./api.js";
import EditorVisual from "./EditorVisual.jsx";
import Proyeccion from "./Proyeccion.jsx";
import Compatibilidad from "./Compatibilidad.jsx";

function TablaPeriodica() {
  const [els, setEls] = useState([]);
  const [sel, setSel] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.tabla().then(setEls).catch((e) => setError("" + e));
  }, []);

  const principales = els.filter((e) => e.grupo > 0);
  const fblock = els.filter((e) => e.grupo === 0);

  const Tile = (e) => (
    <button
      key={e.simbolo}
      className={"elem cat-" + slug(e.categoria)}
      style={e.grupo > 0 ? { gridColumn: e.grupo, gridRow: e.periodo } : undefined}
      onClick={() => setSel(e)}
      title={`${e.nombre} · ${e.categoria}`}
    >
      <span className="z">{e.numero_atomico}</span>
      <span className="sim">{e.simbolo}</span>
      <span className="masa">{Math.round(e.masa)}</span>
    </button>
  );

  return (
    <section className="card tabla-card">
      <h3>Tabla periódica</h3>
      {error && <p className="err">{error}</p>}
      <div className="tabla">{principales.map(Tile)}</div>
      <div className="fbloque">{fblock.map(Tile)}</div>
      {sel && (
        <div className="detalle">
          <span className="detalle-sim">{sel.simbolo}</span>
          <div>
            <b>{sel.nombre}</b> · Z={sel.numero_atomico} · {sel.masa} u
            <div className="detalle-meta">
              {sel.categoria} · periodo {sel.periodo} · grupo {sel.grupo || "—"}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

function Identificar() {
  const [texto, setTexto] = useState("La glucosa C6H12O6 contiene oxígeno y agua.");
  const [res, setRes] = useState(null);
  const [error, setError] = useState("");

  async function run() {
    try {
      setError("");
      setRes(await api.identificarQuimica(texto));
    } catch (e) {
      setError("" + e);
    }
  }

  return (
    <section className="card">
      <h3>Identificar química</h3>
      <textarea rows={3} value={texto} onChange={(e) => setTexto(e.target.value)} />
      <button onClick={run}>Identificar</button>
      {error && <p className="err">{error}</p>}
      {res && (
        <div className="result">
          {res.elementos.length > 0 && (
            <p>
              Elementos:{" "}
              {res.elementos.map((x) => (
                <span key={x.simbolo} className="chip">{x.simbolo}</span>
              ))}
            </p>
          )}
          {res.compuestos.length > 0 && (
            <ul>
              {res.compuestos.map((c, i) => (
                <li key={i}>
                  <b>{c.formula}</b> {c.nombre && `(${c.nombre})`} · {c.masa_molar} g/mol
                </li>
              ))}
            </ul>
          )}
          {res.elementos.length === 0 && res.compuestos.length === 0 && (
            <p className="vacio">Sin química detectada.</p>
          )}
        </div>
      )}
    </section>
  );
}

export default function Quimica() {
  return (
    <div className="apartado">
      <TablaPeriodica />
      <Identificar />
      <EditorVisual />
      <div className="columnas">
        <Proyeccion />
        <Compatibilidad />
      </div>
    </div>
  );
}
