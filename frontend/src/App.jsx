import { useEffect, useState } from "react";
import { api } from "./api.js";
import Quimica from "./Quimica.jsx";
import Filosofia from "./Filosofia.jsx";

export default function App() {
  const [tab, setTab] = useState("quimica");
  const [salud, setSalud] = useState(null);

  useEffect(() => {
    api.salud().then(setSalud).catch(() => setSalud(false));
  }, []);

  return (
    <div className="app">
      <header className="topbar">
        <h1 className="marca">AMPA</h1>
        <nav className="tabs">
          <button className={tab === "quimica" ? "activo" : ""} onClick={() => setTab("quimica")}>
            🧪 Química
          </button>
          <button className={tab === "filosofia" ? "activo" : ""} onClick={() => setTab("filosofia")}>
            📚 Filosofía
          </button>
        </nav>
        <span className={"estado " + (salud ? "ok" : salud === false ? "mal" : "")}>
          {salud ? `API v${salud.version}` : salud === false ? "API offline" : "conectando…"}
        </span>
      </header>
      <main className="contenido">{tab === "quimica" ? <Quimica /> : <Filosofia />}</main>
      <footer className="pie">AMPA · local y portable · sin dependencias en el núcleo</footer>
    </div>
  );
}
