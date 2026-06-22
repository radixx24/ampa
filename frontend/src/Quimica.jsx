import { useEffect, useState } from "react";
import { api, slug } from "./api.js";
import Icon from "./Icon.jsx";
import EditorVisual from "./EditorVisual.jsx";
import Compuestos from "./Compuestos.jsx";
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
      <p className="sub">Los 118 elementos. El color es su familia química. Toca uno para ver sus datos.</p>
      {error && <p className="err">{error}</p>}
      <div className="tabla">{principales.map(Tile)}</div>
      <div className="fbloque">{fblock.map(Tile)}</div>
      {sel ? (
        <div className="detalle">
          <span className="detalle-sim">{sel.simbolo}</span>
          <div>
            <b>{sel.nombre}</b> · Z={sel.numero_atomico} · {sel.masa} u
            <div className="detalle-meta">
              {sel.categoria} · periodo {sel.periodo} · grupo {sel.grupo || "—"}
              {sel.electronegatividad ? ` · EN ${sel.electronegatividad}` : ""}
            </div>
          </div>
        </div>
      ) : (
        <div className="leyenda-cat">
          {[["no-metal", "no metal"], ["gas-noble", "gas noble"], ["alcalino", "alcalino"],
            ["alcalinoterreo", "alcalinotérreo"], ["transicion", "transición"], ["metaloide", "metaloide"],
            ["halogeno", "halógeno"], ["post-transicion", "post-transición"], ["lantanido", "lantánido"],
            ["actinido", "actínido"]].map(([c, l]) => (
            <span key={c}><i className={"cat-" + c} />{l}</span>
          ))}
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
      <h3><Icon name="search" /> Identificar química</h3>
      <p className="sub">Escribe cualquier texto y AMPA detecta los elementos y compuestos (por nombre o fórmula).</p>
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
  const [editorSeed, setEditorSeed] = useState(null);
  const [proyeccionSeed, setProyeccionSeed] = useState(null);
  const [recargar, setRecargar] = useState(0);

  function irA(id) {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  return (
    <div className="apartado">
      <TablaPeriodica />
      <Identificar />
      <div id="editor">
        <EditorVisual seed={editorSeed} onGuardado={() => setRecargar((x) => x + 1)} />
      </div>
      <Compuestos
        recargar={recargar}
        onCargar={(m) => { setEditorSeed({ ...m, n: Date.now() }); irA("editor"); }}
        onProyectar={(f) => { setProyeccionSeed({ f, n: Date.now() }); irA("proyeccion"); }}
      />
      <div className="columnas">
        <div id="proyeccion"><Proyeccion semilla={proyeccionSeed} /></div>
        <Compatibilidad />
      </div>
    </div>
  );
}
