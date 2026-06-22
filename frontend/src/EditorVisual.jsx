import { useEffect, useRef, useState } from "react";
import { api } from "./api.js";
import Visor3D from "./Visor3D.jsx";
import ReaccionAnimada from "./ReaccionAnimada.jsx";

const PALETA = ["C", "H", "O", "N", "S", "Cl", "P", "F"];
const COLOR = {
  H: "#dfe3ea", C: "#3a4150", O: "#e06c75", N: "#61afef",
  S: "#e5c07b", Cl: "#98c379", P: "#d19a66", F: "#56b6c2", Br: "#c0744a",
};
const colorDe = (el) => COLOR[el] || "#7a8290";
const TEXTO_OSCURO = new Set(["H", "F", "S", "Cl"]);
const MODOS = [["construir", "✏️ Construir"], ["mover", "✋ Mover"], ["borrar", "🗑 Borrar"]];
const W = 560;
const H = 320;
const R = 16;
const POL_COLOR = {
  "covalente no polar": "#7e889a",
  "covalente polar": "#e5c07b",
  "iónico": "#e06c75",
  "n/d": "#555c66",
};
const SAT_COLOR = { saturado: "#6ee7b7", libre: "#e5c07b", sobreenlazado: "#f87171", "n/d": "#0e1116" };

function benceno() {
  const cx = 280, cy = 160, Rc = 52, Rh = 92;
  const atomos = [];
  const enlaces = [];
  for (let k = 0; k < 6; k++) {
    const a = ((-90 + k * 60) * Math.PI) / 180;
    atomos.push({ el: "C", x: cx + Rc * Math.cos(a), y: cy + Rc * Math.sin(a) });
  }
  for (let k = 0; k < 6; k++) {
    const a = ((-90 + k * 60) * Math.PI) / 180;
    atomos.push({ el: "H", x: cx + Rh * Math.cos(a), y: cy + Rh * Math.sin(a) });
  }
  for (let k = 0; k < 6; k++) enlaces.push({ a: k, b: (k + 1) % 6, orden: k % 2 === 0 ? 2 : 1 });
  for (let k = 0; k < 6; k++) enlaces.push({ a: k, b: 6 + k, orden: 1 });
  return { nombre: "benceno", atomos, enlaces };
}

const PLANTILLAS = {
  agua: {
    nombre: "agua",
    atomos: [{ el: "O", x: 280, y: 160 }, { el: "H", x: 232, y: 128 }, { el: "H", x: 328, y: 128 }],
    enlaces: [{ a: 0, b: 1, orden: 1 }, { a: 0, b: 2, orden: 1 }],
  },
  metano: {
    nombre: "metano",
    atomos: [
      { el: "C", x: 280, y: 160 }, { el: "H", x: 280, y: 96 }, { el: "H", x: 280, y: 224 },
      { el: "H", x: 216, y: 160 }, { el: "H", x: 344, y: 160 },
    ],
    enlaces: [{ a: 0, b: 1, orden: 1 }, { a: 0, b: 2, orden: 1 }, { a: 0, b: 3, orden: 1 }, { a: 0, b: 4, orden: 1 }],
  },
  "dióxido de carbono": {
    nombre: "dióxido de carbono",
    atomos: [{ el: "O", x: 190, y: 160 }, { el: "C", x: 280, y: 160 }, { el: "O", x: 370, y: 160 }],
    enlaces: [{ a: 0, b: 1, orden: 2 }, { a: 1, b: 2, orden: 2 }],
  },
  eteno: {
    nombre: "eteno",
    atomos: [
      { el: "C", x: 248, y: 160 }, { el: "C", x: 312, y: 160 }, { el: "H", x: 208, y: 126 },
      { el: "H", x: 208, y: 194 }, { el: "H", x: 352, y: 126 }, { el: "H", x: 352, y: 194 },
    ],
    enlaces: [
      { a: 0, b: 1, orden: 2 }, { a: 0, b: 2, orden: 1 }, { a: 0, b: 3, orden: 1 },
      { a: 1, b: 4, orden: 1 }, { a: 1, b: 5, orden: 1 },
    ],
  },
  etanol: {
    nombre: "etanol",
    atomos: [
      { el: "C", x: 214, y: 172 }, { el: "C", x: 274, y: 150 }, { el: "O", x: 334, y: 168 },
      { el: "H", x: 364, y: 200 }, { el: "H", x: 178, y: 142 }, { el: "H", x: 188, y: 210 },
      { el: "H", x: 214, y: 232 }, { el: "H", x: 262, y: 96 }, { el: "H", x: 304, y: 112 },
    ],
    enlaces: [
      { a: 0, b: 1, orden: 1 }, { a: 1, b: 2, orden: 1 }, { a: 2, b: 3, orden: 1 },
      { a: 0, b: 4, orden: 1 }, { a: 0, b: 5, orden: 1 }, { a: 0, b: 6, orden: 1 },
      { a: 1, b: 7, orden: 1 }, { a: 1, b: 8, orden: 1 },
    ],
  },
  benceno: benceno(),
};

export default function EditorVisual() {
  const svgRef = useRef(null);
  const [el, setEl] = useState("C");
  const [orden, setOrden] = useState(1);
  const [modo, setModo] = useState("construir");
  const [atomos, setAtomos] = useState([]);
  const [enlaces, setEnlaces] = useState([]);
  const [sel, setSel] = useState(null);
  const [arrastrando, setArrastrando] = useState(null);
  const [preview, setPreview] = useState(null);
  const cadena = useRef(null);
  const suprimir = useRef(false);
  const [nombre, setNombre] = useState("");
  const [res, setRes] = useState(null);
  const [error, setError] = useState("");
  const [guardados, setGuardados] = useState([]);
  const [mol3d, setMol3d] = useState(null);
  const [animMol, setAnimMol] = useState(null);
  const [temp, setTemp] = useState(298);

  const cargar = () => api.listarCompuestos().then(setGuardados).catch(() => {});
  useEffect(() => { cargar(); }, []);

  function coords(e) {
    const r = svgRef.current.getBoundingClientRect();
    return [((e.clientX - r.left) * W) / r.width, ((e.clientY - r.top) * H) / r.height];
  }

  function clicLienzo(e) {
    if (suprimir.current) { suprimir.current = false; return; }  // soltó un encadenado
    if (modo !== "construir") return;
    const [x, y] = coords(e);
    setAtomos([...atomos, { el, x, y }]);
    setRes(null);
  }

  function clicAtomo(e, i) {
    e.stopPropagation();
    if (suprimir.current) { suprimir.current = false; return; }
    if (modo === "borrar") { borrarAtomo(i); return; }
    if (modo !== "construir") return;
    if (sel === null) { setSel(i); return; }
    if (sel === i) { setSel(null); return; }
    const mismo = (b) => (b.a === sel && b.b === i) || (b.a === i && b.b === sel);
    if (enlaces.some(mismo)) setEnlaces(enlaces.map((b) => (mismo(b) ? { ...b, orden } : b)));
    else setEnlaces([...enlaces, { a: sel, b: i, orden }]);
    setSel(null);
    setRes(null);
  }

  function borrarAtomo(i) {
    setAtomos(atomos.filter((_, j) => j !== i));
    setEnlaces(
      enlaces.filter((b) => b.a !== i && b.b !== i)
        .map((b) => ({ a: b.a > i ? b.a - 1 : b.a, b: b.b > i ? b.b - 1 : b.b, orden: b.orden }))
    );
    setSel(null); setRes(null);
  }
  function borrarEnlace(idx) { setEnlaces(enlaces.filter((_, j) => j !== idx)); setRes(null); }

  function onPointerDownAtomo(e, i) {
    e.stopPropagation();
    if (modo === "mover") { setArrastrando(i); return; }
    if (modo === "construir") {  // inicia un posible "encadenar" (arrastre)
      const A = atomos[i];
      cadena.current = { desde: i, movido: false };
      setPreview({ x1: A.x, y1: A.y, x2: A.x, y2: A.y });
    }
  }
  function onPointerMove(e) {
    if (modo === "mover" && arrastrando !== null) {
      const [x, y] = coords(e);
      setAtomos(atomos.map((a, j) => (j === arrastrando ? { ...a, x, y } : a)));
      return;
    }
    if (modo === "construir" && cadena.current) {
      const [x, y] = coords(e);
      const A = atomos[cadena.current.desde];
      if (Math.hypot(x - A.x, y - A.y) > 8) cadena.current.movido = true;
      setPreview({ x1: A.x, y1: A.y, x2: x, y2: y });
    }
  }
  function onPointerUp(e) {
    if (modo === "mover") { setArrastrando(null); return; }
    const c = cadena.current;
    cadena.current = null;
    setPreview(null);
    if (modo === "construir" && c && c.movido) {
      const [x, y] = coords(e);
      let destino = null;  // ¿soltó sobre otro átomo? → enlaza; si no, crea uno
      atomos.forEach((a, j) => {
        if (j !== c.desde && Math.hypot(a.x - x, a.y - y) <= R) destino = j;
      });
      suprimir.current = true;  // evita que el click suelto añada otro átomo
      const mismo = (b, q) => (b.a === c.desde && b.b === q) || (b.a === q && b.b === c.desde);
      if (destino !== null) {
        if (!enlaces.some((b) => mismo(b, destino)))
          setEnlaces([...enlaces, { a: c.desde, b: destino, orden }]);
      } else {
        const nuevo = atomos.length;
        setAtomos([...atomos, { el, x, y }]);
        setEnlaces([...enlaces, { a: c.desde, b: nuevo, orden }]);
      }
      setSel(null); setRes(null);
    }
  }
  function finArrastre() { setArrastrando(null); cadena.current = null; setPreview(null); }

  function cargarPlantilla(clave) {
    const p = PLANTILLAS[clave];
    if (!p) return;
    setAtomos(p.atomos.map((a) => ({ ...a })));
    setEnlaces(p.enlaces.map((b) => ({ ...b })));
    setNombre(p.nombre);
    setSel(null); setRes(null);
  }

  const molecula = () => ({
    nombre,
    atomos: atomos.map((a) => a.el),
    enlaces: enlaces.map((b) => [b.a, b.b, b.orden]),
  });

  async function analizar() {
    try { setError(""); setRes(await api.analizar(molecula())); }
    catch (e) { setError("" + e); }
  }
  async function guardar() {
    try { setError(""); await api.guardarCompuesto(molecula()); cargar(); }
    catch (e) { setError("" + e); }
  }
  function limpiar() { setAtomos([]); setEnlaces([]); setSel(null); setRes(null); setError(""); }

  function exportarPNG() {
    const xml = new XMLSerializer().serializeToString(svgRef.current);
    const fuente = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(xml)));
    const img = new Image();
    img.onload = () => {
      const c = document.createElement("canvas");
      c.width = W * 2; c.height = H * 2;
      const ctx = c.getContext("2d");
      ctx.fillStyle = "#0e1116";
      ctx.fillRect(0, 0, c.width, c.height);
      ctx.drawImage(img, 0, 0, c.width, c.height);
      const a = document.createElement("a");
      a.download = (nombre || "molecula") + ".png";
      a.href = c.toDataURL("image/png");
      a.click();
    };
    img.src = fuente;
  }

  const combustible =
    atomos.some((a) => a.el === "C") &&
    atomos.some((a) => a.el === "H") &&
    atomos.every((a) => ["C", "H", "O"].includes(a.el));
  const analisis = res && res.enlaces_analisis;
  const tieneDobleCC = enlaces.some(
    (b) => b.orden === 2 && atomos[b.a] && atomos[b.b] && atomos[b.a].el === "C" && atomos[b.b].el === "C"
  );
  const esAcido = res && res.grupos_funcionales && res.grupos_funcionales.includes("ácido carboxílico");

  return (
    <section className="card">
      <h3>Editor de enlaces de carbono</h3>
      <div className="paleta">
        <span>Modo:</span>
        {MODOS.map(([m, etiqueta]) => (
          <button key={m} className={"pchip " + (modo === m ? "on" : "")} onClick={() => { setModo(m); setSel(null); }}>
            {etiqueta}
          </button>
        ))}
        <select className="plantillas" defaultValue="" onChange={(e) => { cargarPlantilla(e.target.value); e.target.value = ""; }}>
          <option value="" disabled>＋ Plantilla…</option>
          {Object.keys(PLANTILLAS).map((k) => <option key={k} value={k}>{k}</option>)}
        </select>
      </div>
      <div className="paleta">
        <span>Átomo:</span>
        {PALETA.map((s) => (
          <button
            key={s}
            className={"pchip " + (el === s ? "on" : "")}
            style={{ background: colorDe(s), color: TEXTO_OSCURO.has(s) ? "#1a1f27" : "#fff" }}
            onClick={() => setEl(s)}
          >
            {s}
          </button>
        ))}
        <span className="sep">Enlace:</span>
        {[1, 2, 3].map((o) => (
          <button key={o} className={"pchip " + (orden === o ? "on" : "")} onClick={() => setOrden(o)}>
            {["—", "═", "≡"][o - 1]}
          </button>
        ))}
      </div>
      <div className="paleta">
        <span>Temp (K):</span>
        <input
          type="number" className="temp" value={temp} min={0} max={6000}
          onChange={(e) => setTemp(Number(e.target.value) || 0)}
        />
        {analisis && (
          <span className="leyenda">
            <i className="lp" style={{ background: POL_COLOR["covalente no polar"] }} /> no polar
            <i className="lp" style={{ background: POL_COLOR["covalente polar"] }} /> polar
            <i className="lp" style={{ background: POL_COLOR["iónico"] }} /> iónico
            {!analisis.estable && <b className="alerta">⚠ valencias</b>}
          </span>
        )}
      </div>
      <p className="hint">
        {modo === "construir" && "Clic = átomo · clic en dos átomos = enlace · arrastra desde un átomo = encadenar"}
        {modo === "mover" && "Arrastra los átomos para reacomodarlos"}
        {modo === "borrar" && "Clic en un átomo o un enlace para eliminarlo"}
      </p>
      <svg
        ref={svgRef}
        className={"lienzo modo-" + modo}
        viewBox={`0 0 ${W} ${H}`}
        onClick={clicLienzo}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerLeave={finArrastre}
      >
        {preview && (
          <line x1={preview.x1} y1={preview.y1} x2={preview.x2} y2={preview.y2}
                stroke="#6ee7b7" strokeWidth="2" strokeDasharray="5 4" pointerEvents="none" />
        )}
        {enlaces.map((b, i) => {
          const A = atomos[b.a];
          const B = atomos[b.b];
          if (!A || !B) return null;
          const dx = B.x - A.x;
          const dy = B.y - A.y;
          const len = Math.hypot(dx, dy) || 1;
          const ox = -dy / len;
          const oy = dx / len;
          const offsets = b.orden === 1 ? [0] : b.orden === 2 ? [-3, 3] : [-5, 0, 5];
          const polColor = analisis && analisis.enlaces[i]
            ? (POL_COLOR[analisis.enlaces[i].polaridad] || "#8a93a3")
            : "#8a93a3";
          return (
            <g key={i}>
              <line
                x1={A.x} y1={A.y} x2={B.x} y2={B.y}
                stroke="transparent" strokeWidth="14"
                style={{ pointerEvents: modo === "borrar" ? "stroke" : "none", cursor: "pointer" }}
                onClick={(e) => { e.stopPropagation(); borrarEnlace(i); }}
              />
              {offsets.map((o, k) => (
                <line key={k} x1={A.x + ox * o} y1={A.y + oy * o} x2={B.x + ox * o} y2={B.y + oy * o} stroke={polColor} strokeWidth={analisis ? 2.6 : 2} />
              ))}
            </g>
          );
        })}
        {atomos.map((a, i) => (
          <g key={i} onClick={(e) => clicAtomo(e, i)} onPointerDown={(e) => onPointerDownAtomo(e, i)} style={{ cursor: modo === "mover" ? "grab" : "pointer" }}>
            <circle cx={a.x} cy={a.y} r={R} fill={colorDe(a.el)} stroke={sel === i ? "#6ee7b7" : (analisis && analisis.atomos[i] ? (SAT_COLOR[analisis.atomos[i].estado] || "#0e1116") : "#0e1116")} strokeWidth={sel === i ? 3 : (analisis ? 2.6 : 2)} />
            <text x={a.x} y={a.y + 4} textAnchor="middle" fontSize="13" fontWeight="700" fill={TEXTO_OSCURO.has(a.el) ? "#1a1f27" : "#fff"}>
              {a.el}
            </text>
          </g>
        ))}
      </svg>
      <div className="row">
        <input className="nombre" value={nombre} onChange={(e) => setNombre(e.target.value)} placeholder="nombre (opcional)" />
        <button onClick={analizar} disabled={!atomos.length}>Analizar</button>
        <button className="sec" onClick={() => setMol3d(molecula())} disabled={!atomos.length}>🧊 Ver en 3D</button>
        <button className="sec" onClick={() => setAnimMol({ mol: molecula(), tipo: "combustion" })} disabled={!combustible} title={combustible ? "" : "Necesita C y H"}>🎬 Combustión</button>
        <button className="sec" onClick={() => setAnimMol({ mol: molecula(), tipo: "hidrogenacion" })} disabled={!tieneDobleCC} title={tieneDobleCC ? "" : "Necesita un C=C"}>🎬 Hidrogenación</button>
        <button className="sec" onClick={() => setAnimMol({ mol: molecula(), tipo: "neutralizacion" })} disabled={!esAcido} title={esAcido ? "" : "Analiza un ácido carboxílico primero"}>🎬 Neutralización</button>
      </div>
      <div className="row">
        <button className="sec" onClick={guardar} disabled={!atomos.length}>Guardar</button>
        <button className="sec" onClick={exportarPNG} disabled={!atomos.length}>🖼 PNG</button>
        <button className="sec" onClick={limpiar}>Limpiar</button>
      </div>
      {error && <p className="err">{error}</p>}
      {mol3d && <Visor3D molecula={mol3d} temp={temp} onCerrar={() => setMol3d(null)} />}
      {animMol && <ReaccionAnimada molecula={animMol.mol} tipo={animMol.tipo} onCerrar={() => setAnimMol(null)} />}
      {res && (
        <div className="result">
          <p className="formula"><b>{res.formula}</b> · {res.masa_molar} g/mol</p>
          <p>
            Grupos:{" "}
            {res.grupos_funcionales.length
              ? res.grupos_funcionales.map((g, i) => <span key={i} className="chip">{g}</span>)
              : "—"}
          </p>
          {res.reacciones.length > 0 && (
            <ul className="reacciones">
              {res.reacciones.map((r, i) => (
                <li key={i}><span className="tipo">{r.tipo}</span> {r.ecuacion}</li>
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
              <li key={i}>{m.nombre || "(sin nombre)"} — <b>{m.formula}</b> · {m.masa_molar} g/mol</li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
