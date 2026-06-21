import { useEffect, useState } from "react";
import { api, slug } from "./api.js";

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

const EJEMPLO = JSON.stringify({
  nombre: "etanol",
  atomos: ["C", "C", "O", "H", "H", "H", "H", "H", "H"],
  enlaces: [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 4, 1], [0, 5, 1], [0, 6, 1], [1, 7, 1], [1, 8, 1]],
});

function Editor() {
  const [texto, setTexto] = useState(EJEMPLO);
  const [res, setRes] = useState(null);
  const [error, setError] = useState("");
  const [guardados, setGuardados] = useState([]);

  const cargar = () => api.listarCompuestos().then(setGuardados).catch(() => {});
  useEffect(() => { cargar(); }, []);

  function leer() {
    return JSON.parse(texto);
  }

  async function analizar() {
    try {
      setError("");
      setRes(await api.analizar(leer()));
    } catch (e) {
      setError("" + e);
    }
  }

  async function guardar() {
    try {
      setError("");
      await api.guardarCompuesto(leer());
      cargar();
    } catch (e) {
      setError("" + e);
    }
  }

  return (
    <section className="card">
      <h3>Editor de moléculas (enlaces de carbono)</h3>
      <p className="hint">{"JSON: { nombre, atomos:[…], enlaces:[[a,b,orden],…] }"}</p>
      <textarea rows={5} className="mono" value={texto} onChange={(e) => setTexto(e.target.value)} />
      <div className="row">
        <button onClick={analizar}>Analizar</button>
        <button className="sec" onClick={guardar}>Guardar compuesto</button>
      </div>
      {error && <p className="err">{error}</p>}
      {res && (
        <div className="result">
          <p className="formula">
            <b>{res.formula}</b> · {res.masa_molar} g/mol
          </p>
          <p>
            Grupos:{" "}
            {res.grupos_funcionales.length
              ? res.grupos_funcionales.map((g, i) => <span key={i} className="chip">{g}</span>)
              : "—"}
          </p>
          {res.reacciones.length > 0 && (
            <ul className="reacciones">
              {res.reacciones.map((r, i) => (
                <li key={i}>
                  <span className="tipo">{r.tipo}</span> {r.ecuacion}
                </li>
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
              <li key={i}>
                {m.nombre || "(sin nombre)"} — <b>{m.formula}</b> · {m.masa_molar} g/mol
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}

export default function Quimica() {
  return (
    <div className="apartado">
      <TablaPeriodica />
      <div className="columnas">
        <Identificar />
        <Editor />
      </div>
    </div>
  );
}
