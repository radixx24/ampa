import { useEffect, useRef, useState } from "react";
import { api } from "./api.js";
import Explorar from "./Explorar.jsx";
import GrafoFilosofia from "./GrafoFilosofia.jsx";

function Identificar() {
  const [texto, setTexto] = useState("Kant criticó el empirismo de Hume sobre el fenómeno.");
  const [res, setRes] = useState(null);
  const [error, setError] = useState("");

  async function run() {
    try {
      setError("");
      setRes(await api.identificarFilosofia(texto));
    } catch (e) {
      setError("" + e);
    }
  }

  const Grupo = ({ titulo, items, render }) =>
    items.length > 0 && (
      <p>
        <span className="g-tit">{titulo}</span>
        {items.map((x, i) => (
          <span key={i} className="chip">{render(x)}</span>
        ))}
      </p>
    );

  return (
    <section className="card">
      <h3>🔍 Identificar</h3>
      <p className="sub">Pega cualquier texto y AMPA detecta a los filósofos, corrientes y conceptos que aparecen.</p>
      <textarea rows={3} value={texto} onChange={(e) => setTexto(e.target.value)} />
      <button onClick={run}>Identificar</button>
      {error && <p className="err">{error}</p>}
      {res && (
        <div className="result">
          <Grupo titulo="Filósofos" items={res.filosofos} render={(x) => `${x.nombre} · ${x.epoca}`} />
          <Grupo titulo="Corrientes" items={res.corrientes} render={(x) => x.nombre} />
          <Grupo titulo="Conceptos" items={res.conceptos} render={(x) => x.nombre} />
          {!res.filosofos.length && !res.corrientes.length && !res.conceptos.length && (
            <p className="vacio">No reconocí ningún filósofo ni concepto en ese texto. Prueba con un nombre conocido.</p>
          )}
        </div>
      )}
    </section>
  );
}

function Cuaderno({ semilla }) {
  const [texto, setTexto] = useState("");
  const [sobre, setSobre] = useState("");
  const [dicc, setDicc] = useState({});
  const [abierto, setAbierto] = useState(null);
  const [error, setError] = useState("");
  const areaRef = useRef(null);

  const cargar = () => api.diccionario().then(setDicc).catch(() => {});
  useEffect(() => { cargar(); }, []);

  // Cuando eliges algo en "Explorar", se siembra aquí y enfoca.
  useEffect(() => {
    if (semilla && semilla.t) {
      setSobre(semilla.t);
      if (areaRef.current) areaRef.current.focus();
    }
  }, [semilla]);

  async function pensar() {
    try {
      setError("");
      const terminos = sobre.trim()
        ? sobre.split(",").map((s) => s.trim()).filter(Boolean)
        : null;
      await api.pensar(texto, terminos);
      setTexto("");
      setSobre("");
      cargar();
    } catch (e) {
      setError("" + e);
    }
  }

  const terminos = Object.keys(dicc).sort((a, b) => dicc[b].length - dicc[a].length);

  return (
    <section className="card">
      <h3>✍️ Tu cuaderno</h3>
      <p className="sub">Escribe lo que piensas. AMPA lo guarda y arma tu diccionario personal con tus términos.</p>
      <textarea
        ref={areaRef}
        rows={3}
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        placeholder={sobre ? `Tu idea sobre ${sobre}…` : "Escribe tu pensamiento…"}
      />
      <input
        value={sobre}
        onChange={(e) => setSobre(e.target.value)}
        placeholder="términos (separados por comas) — opcional"
      />
      <button onClick={pensar} disabled={!texto.trim()}>Guardar pensamiento</button>
      {error && <p className="err">{error}</p>}
      <h4>Tu diccionario · {terminos.length} {terminos.length === 1 ? "término" : "términos"}</h4>
      {terminos.length === 0 ? (
        <p className="vacio">Aún no hay nada. Escribe un pensamiento arriba (o toca algo en “Explorar”) y aparecerá aquí.</p>
      ) : (
        <ul className="dicc">
          {terminos.map((t) => (
            <li key={t}>
              <button className="link" onClick={() => setAbierto(abierto === t ? null : t)}>
                {abierto === t ? "▾ " : "▸ "}{t} <span className="cuenta">{dicc[t].length}</span>
              </button>
              {abierto === t && (
                <ul className="entradas">
                  {dicc[t].map((p, i) => <li key={i}>{p.texto}</li>)}
                </ul>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default function Filosofia() {
  const [semilla, setSemilla] = useState(null);

  return (
    <div className="apartado">
      <Explorar onEscribir={(t) => setSemilla({ t, n: Date.now() })} />
      <div className="columnas">
        <Cuaderno semilla={semilla} />
        <Identificar />
      </div>
      <GrafoFilosofia />
    </div>
  );
}
