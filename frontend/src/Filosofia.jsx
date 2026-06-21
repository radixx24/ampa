import { useEffect, useState } from "react";
import { api } from "./api.js";

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
        {titulo}:{" "}
        {items.map((x, i) => (
          <span key={i} className="chip">{render(x)}</span>
        ))}
      </p>
    );

  return (
    <section className="card">
      <h3>Identificar filosofía</h3>
      <textarea rows={3} value={texto} onChange={(e) => setTexto(e.target.value)} />
      <button onClick={run}>Identificar</button>
      {error && <p className="err">{error}</p>}
      {res && (
        <div className="result">
          <Grupo titulo="Filósofos" items={res.filosofos} render={(x) => `${x.nombre} (${x.epoca})`} />
          <Grupo titulo="Corrientes" items={res.corrientes} render={(x) => x.nombre} />
          <Grupo titulo="Conceptos" items={res.conceptos} render={(x) => x.nombre} />
          {!res.filosofos.length && !res.corrientes.length && !res.conceptos.length && (
            <p className="vacio">Sin filosofía detectada.</p>
          )}
        </div>
      )}
    </section>
  );
}

function Cuaderno() {
  const [texto, setTexto] = useState("");
  const [sobre, setSobre] = useState("");
  const [dicc, setDicc] = useState({});
  const [abierto, setAbierto] = useState(null);
  const [error, setError] = useState("");

  const cargar = () => api.diccionario().then(setDicc).catch(() => {});
  useEffect(() => { cargar(); }, []);

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
      <h3>Cuaderno personal</h3>
      <textarea
        rows={3}
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        placeholder="Escribe tu pensamiento…"
      />
      <input
        value={sobre}
        onChange={(e) => setSobre(e.target.value)}
        placeholder="términos (separados por comas) — opcional"
      />
      <button onClick={pensar} disabled={!texto.trim()}>
        Guardar pensamiento
      </button>
      {error && <p className="err">{error}</p>}
      <h4>Diccionario ({terminos.length})</h4>
      {terminos.length === 0 && <p className="vacio">Aún no hay términos. Escribe algo arriba.</p>}
      <ul className="dicc">
        {terminos.map((t) => (
          <li key={t}>
            <button className="link" onClick={() => setAbierto(abierto === t ? null : t)}>
              {t} <span className="cuenta">{dicc[t].length}</span>
            </button>
            {abierto === t && (
              <ul className="entradas">
                {dicc[t].map((p, i) => (
                  <li key={i}>{p.texto}</li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}

export default function Filosofia() {
  return (
    <div className="apartado">
      <div className="columnas">
        <Identificar />
        <Cuaderno />
      </div>
    </div>
  );
}
