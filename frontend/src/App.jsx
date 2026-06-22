import { useEffect, useState } from "react";
import { api } from "./api.js";
import Icon from "./Icon.jsx";
import Quimica from "./Quimica.jsx";
import Filosofia from "./Filosofia.jsx";

const PASOS = {
  quimica: [
    ["1", "Toca la tabla", "Haz clic en cualquier elemento y mira sus datos. Los colores son su familia."],
    ["2", "Dibuja una molécula", "En el editor, clic = átomo, y une dos átomos para enlazarlos. Prueba una plantilla."],
    ["3", "Proyecta y juega", "¿Se puede crear? Mira el ΔG. ¿Dos elementos se llevan? Pruébalos. Gíralo en 3D."],
  ],
  filosofia: [
    ["1", "Explora", "Navega filósofos, corrientes y conceptos. Toca uno para saber más."],
    ["2", "Escribe lo que piensas", "En el cuaderno guarda tus ideas; AMPA arma tu diccionario personal."],
    ["3", "Mira tus conexiones", "El grafo conecta tus ideas como un mapa mental que se ordena solo."],
  ],
};

function Intro({ tab, onCerrar }) {
  return (
    <section className="intro">
      <div className="intro-top">
        <div>
          <h2>{tab === "quimica" ? "Juega con la materia" : "Piensa en voz alta"}</h2>
          <p>
            {tab === "quimica"
              ? "Construye moléculas, mira qué reacciones harían y descubre —con termodinámica de verdad— si algo puede existir. No necesitas saber química: explora y aprende sobre la marcha."
              : "Explora a los grandes pensadores, escribe tus propias ideas y velas conectarse en un grafo vivo. Aquí la filosofía se navega y se construye."}
          </p>
        </div>
        <button className="cerrar-intro" onClick={onCerrar} title="Ocultar guía" aria-label="Ocultar"><Icon name="x" size={15} /></button>
      </div>
      <div className="pasos">
        {PASOS[tab].map(([num, titulo, desc]) => (
          <div className="paso" key={num}>
            <span className="num">{num}</span>
            <b>{titulo}</b>
            <span>{desc}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

export default function App() {
  const [tab, setTab] = useState("quimica");
  const [salud, setSalud] = useState(null);
  const [verGuia, setVerGuia] = useState(
    () => localStorage.getItem("ampa_guia_off") !== "1"
  );

  useEffect(() => {
    api.salud().then(setSalud).catch(() => setSalud(false));
  }, []);

  function ocultarGuia() {
    setVerGuia(false);
    localStorage.setItem("ampa_guia_off", "1");
  }

  return (
    <div className="app">
      <header className="topbar">
        <h1 className="marca"><span className="punto" /> AMPA</h1>
        <nav className="tabs">
          <button className={tab === "quimica" ? "activo" : ""} onClick={() => setTab("quimica")}>
            <Icon name="flask" size={16} /> Química
          </button>
          <button className={tab === "filosofia" ? "activo" : ""} onClick={() => setTab("filosofia")}>
            <Icon name="book" size={16} /> Filosofía
          </button>
        </nav>
        <span className={"estado " + (salud ? "ok" : salud === false ? "mal" : "")}>
          {salud ? `conectado · v${salud.version}` : salud === false ? "API offline" : "conectando…"}
        </span>
      </header>

      {verGuia ? (
        <Intro tab={tab} onCerrar={ocultarGuia} />
      ) : (
        <button className="ghost ver-guia" onClick={() => setVerGuia(true)} style={{ marginBottom: 14 }}>
          ? Mostrar guía rápida
        </button>
      )}

      <main className="contenido">{tab === "quimica" ? <Quimica /> : <Filosofia />}</main>

      <footer className="pie">
        AMPA · local y portable · sin dependencias en el núcleo ·{" "}
        <a href="https://github.com/radixx24/ampa" target="_blank" rel="noreferrer">código</a>
      </footer>

      <nav className="bottom-nav">
        <button className={tab === "quimica" ? "activo" : ""} onClick={() => setTab("quimica")}>
          <Icon name="flask" size={20} /><span>Química</span>
        </button>
        <button className={tab === "filosofia" ? "activo" : ""} onClick={() => setTab("filosofia")}>
          <Icon name="book" size={20} /><span>Filosofía</span>
        </button>
      </nav>
    </div>
  );
}
