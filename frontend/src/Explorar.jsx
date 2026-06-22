import { useEffect, useState } from "react";
import { api } from "./api.js";

const TABS = [
  ["filosofos", "Filósofos"],
  ["corrientes", "Corrientes"],
  ["conceptos", "Conceptos"],
];
const EPOCAS = ["Antigua", "Medieval", "Moderna", "Contemporánea"];

function agrupar(lista, clave) {
  const g = {};
  lista.forEach((x) => {
    const k = x[clave];
    if (!g[k]) g[k] = [];
    g[k].push(x);
  });
  return g;
}

export default function Explorar({ onEscribir }) {
  const [cat, setCat] = useState(null);
  const [tab, setTab] = useState("filosofos");
  const [error, setError] = useState("");

  useEffect(() => {
    api.catalogoFilosofia().then(setCat).catch((e) => setError("" + e));
  }, []);

  return (
    <section className="card">
      <h3>🧭 Explorar la filosofía</h3>
      <p className="sub">
        Navega la base de conocimiento sin escribir nada. Toca a cualquiera para
        escribir tu propia idea sobre él en el cuaderno de abajo.
      </p>
      {error && <p className="err">{error}</p>}
      {!cat && !error && <p className="vacio">Cargando catálogo…</p>}

      {cat && (
        <>
          <div className="exp-tabs">
            {TABS.map(([k, l]) => (
              <button key={k} className={tab === k ? "on" : ""} onClick={() => setTab(k)}>
                {l} <span className="cuenta">{cat[k].length}</span>
              </button>
            ))}
          </div>

          {tab === "filosofos" &&
            EPOCAS.filter((ep) => agrupar(cat.filosofos, "epoca")[ep]).map((ep) => {
              const grupo = agrupar(cat.filosofos, "epoca")[ep];
              return (
                <div key={ep}>
                  <div className="exp-epoca">{ep}</div>
                  <div className="exp-grid">
                    {grupo.map((f) => (
                      <button key={f.nombre} className="fil-card" onClick={() => onEscribir(f.nombre)}
                              title={`Escribir sobre ${f.nombre}`}>
                        <b>{f.nombre}</b>
                        <span>{f.corriente}</span>
                      </button>
                    ))}
                  </div>
                </div>
              );
            })}

          {tab === "corrientes" && (
            <div className="exp-tags">
              {cat.corrientes.map((c) => (
                <button key={c} className="exp-tag" onClick={() => onEscribir(c)}>{c}</button>
              ))}
            </div>
          )}

          {tab === "conceptos" &&
            Object.entries(agrupar(cat.conceptos, "rama"))
              .sort((a, b) => a[0].localeCompare(b[0]))
              .map(([rama, items]) => (
                <div key={rama}>
                  <div className="exp-epoca">{rama}</div>
                  <div className="exp-tags">
                    {items.map((c) => (
                      <button key={c.nombre} className="exp-tag" onClick={() => onEscribir(c.nombre)}>
                        {c.nombre}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
        </>
      )}
    </section>
  );
}
