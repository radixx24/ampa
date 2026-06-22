import { useEffect, useState } from "react";
import { api } from "./api.js";
import Icon from "./Icon.jsx";

// Panel de compuestos guardados: funcionan como plantillas. Cada uno se puede
// cargar al editor, analizar en sitio o mandar a la proyección termodinámica.
export default function Compuestos({ recargar, onCargar, onProyectar }) {
  const [lista, setLista] = useState([]);
  const [analisis, setAnalisis] = useState({});
  const [error, setError] = useState("");

  useEffect(() => {
    api.listarCompuestos().then(setLista).catch(() => {});
  }, [recargar]);

  async function analizar(m, i) {
    if (analisis[i]) { setAnalisis((a) => ({ ...a, [i]: null })); return; }
    try {
      setError("");
      const r = await api.analizar({ nombre: m.nombre, atomos: m.atomos, enlaces: m.enlaces });
      setAnalisis((a) => ({ ...a, [i]: r }));
    } catch (e) {
      setError("" + e);
    }
  }

  return (
    <section className="card" id="mis-compuestos">
      <h3>
        <Icon name="layers" /> Mis compuestos
        {lista.length > 0 && <span className="cuenta">{lista.length}</span>}
      </h3>
      <p className="sub">
        Tus moléculas guardadas funcionan como <b>plantillas</b>: cárgalas al editor,
        analízalas o proyéctalas (ΔG) sin volver a dibujarlas.
      </p>
      {error && <p className="err">{error}</p>}
      {lista.length === 0 ? (
        <p className="vacio">Aún no guardas ninguna. Dibuja algo en el editor y dale <Icon name="save" size={13} /> Guardar.</p>
      ) : (
        <ul className="comp-lista">
          {lista.map((m, i) => (
            <li key={i} className="comp">
              <div className="comp-top">
                <div className="comp-id">
                  <b>{m.formula}</b>
                  <span>{m.nombre || "sin nombre"} · {m.masa_molar} g/mol</span>
                </div>
                <div className="comp-acc">
                  <button className="sec mini" onClick={() => onCargar(m)} title="Cargar en el editor">
                    <Icon name="pen" size={14} /> Cargar
                  </button>
                  <button className="sec mini" onClick={() => analizar(m, i)} title="Analizar grupos y reacciones">
                    <Icon name="search" size={14} /> Analizar
                  </button>
                  <button className="sec mini" onClick={() => onProyectar(m.formula)} title="Mandar a la proyección termodinámica">
                    <Icon name="sparkles" size={14} /> Proyectar
                  </button>
                </div>
              </div>
              {analisis[i] && (
                <div className="comp-det">
                  <p>
                    Grupos:{" "}
                    {analisis[i].grupos_funcionales.length
                      ? analisis[i].grupos_funcionales.map((g, k) => <span key={k} className="chip">{g}</span>)
                      : "—"}
                  </p>
                  {analisis[i].reacciones.length > 0 && (
                    <ul className="reacciones">
                      {analisis[i].reacciones.slice(0, 5).map((r, k) => (
                        <li key={k}><span className="tipo">{r.tipo}</span> {r.ecuacion}</li>
                      ))}
                    </ul>
                  )}
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
