import { useEffect, useRef, useState } from "react";
import { api } from "./api.js";

const W = 560;
const H = 380;
const norm = (s) => (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");

function construir(dicc) {
  const terms = Object.keys(dicc);
  const idx = {};
  terms.forEach((t, i) => (idx[t] = i));
  const aDisplay = {};
  terms.forEach((t) => (aDisplay[norm(t)] = t));

  const nodos = terms.map((t, i) => ({
    t, n: dicc[t].length,
    x: W / 2 + Math.cos(i) * 90 + (Math.random() - 0.5) * 60,
    y: H / 2 + Math.sin(i) * 90 + (Math.random() - 0.5) * 60,
    vx: 0, vy: 0,
  }));

  // Pensamientos únicos → aristas por co-ocurrencia de términos.
  const vistos = new Set();
  const peso = {};
  Object.values(dicc).forEach((lista) =>
    lista.forEach((p) => {
      const clave = (p.timestamp || "") + "|" + p.texto;
      if (vistos.has(clave)) return;
      vistos.add(clave);
      const ts = [...new Set((p.terminos || []).map((x) => aDisplay[norm(x)]).filter(Boolean))];
      for (let i = 0; i < ts.length; i++)
        for (let j = i + 1; j < ts.length; j++) {
          const a = idx[ts[i]], b = idx[ts[j]];
          const k = a < b ? `${a}-${b}` : `${b}-${a}`;
          peso[k] = (peso[k] || 0) + 1;
        }
    })
  );
  const aristas = Object.entries(peso).map(([k, w]) => {
    const [a, b] = k.split("-").map(Number);
    return { a, b, w };
  });
  return { nodos, aristas };
}

function paso(g) {
  const { nodos, aristas } = g;
  const n = nodos.length;
  for (let i = 0; i < n; i++) { nodos[i].vx *= 0.84; nodos[i].vy *= 0.84; }
  for (let i = 0; i < n; i++)
    for (let j = i + 1; j < n; j++) {
      const dx = nodos[i].x - nodos[j].x, dy = nodos[i].y - nodos[j].y;
      const d2 = dx * dx + dy * dy + 0.01, d = Math.sqrt(d2);
      const f = 1400 / d2, ux = dx / d, uy = dy / d;
      nodos[i].vx += f * ux; nodos[i].vy += f * uy;
      nodos[j].vx -= f * ux; nodos[j].vy -= f * uy;
    }
  aristas.forEach(({ a, b, w }) => {
    const dx = nodos[b].x - nodos[a].x, dy = nodos[b].y - nodos[a].y;
    const d = Math.hypot(dx, dy) + 0.01;
    const f = (d - 74) * 0.02 * Math.min(3, w), ux = dx / d, uy = dy / d;
    nodos[a].vx += f * ux; nodos[a].vy += f * uy;
    nodos[b].vx -= f * ux; nodos[b].vy -= f * uy;
  });
  for (let i = 0; i < n; i++) {
    nodos[i].vx += (W / 2 - nodos[i].x) * 0.0025;
    nodos[i].vy += (H / 2 - nodos[i].y) * 0.0025;
    nodos[i].x += Math.max(-6, Math.min(6, nodos[i].vx));
    nodos[i].y += Math.max(-6, Math.min(6, nodos[i].vy));
    nodos[i].x = Math.max(24, Math.min(W - 24, nodos[i].x));
    nodos[i].y = Math.max(24, Math.min(H - 24, nodos[i].y));
  }
}

function dibujar(ctx, g, sel) {
  ctx.fillStyle = "#0c1220";
  ctx.fillRect(0, 0, W, H);
  const { nodos, aristas } = g;
  aristas.forEach(({ a, b }) => {
    const activo = sel && (nodos[a].t === sel || nodos[b].t === sel);
    ctx.strokeStyle = activo ? "rgba(110,231,183,0.65)" : "rgba(122,130,154,0.22)";
    ctx.lineWidth = activo ? 2 : 1;
    ctx.beginPath();
    ctx.moveTo(nodos[a].x, nodos[a].y);
    ctx.lineTo(nodos[b].x, nodos[b].y);
    ctx.stroke();
  });
  nodos.forEach((nd) => {
    const r = 6 + Math.min(16, nd.n * 3);
    const activo = nd.t === sel;
    ctx.fillStyle = activo ? "#6ee7b7" : "#60a5fa";
    ctx.globalAlpha = activo ? 1 : 0.85;
    ctx.beginPath();
    ctx.arc(nd.x, nd.y, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = 1;
    ctx.fillStyle = "#e6edf3";
    ctx.font = `${activo ? "700 " : ""}12px sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    ctx.fillText(nd.t, nd.x, nd.y + r + 2);
  });
}

export default function GrafoFilosofia() {
  const canvasRef = useRef(null);
  const grafoRef = useRef({ nodos: [], aristas: [] });
  const selRef = useRef(null);
  const [dicc, setDicc] = useState(null);
  const [sel, setSel] = useState(null);

  useEffect(() => { api.diccionario().then(setDicc).catch(() => {}); }, []);
  useEffect(() => { if (dicc) grafoRef.current = construir(dicc); setSel(null); }, [dicc]);
  useEffect(() => { selRef.current = sel; }, [sel]);

  useEffect(() => {
    const ctx = canvasRef.current.getContext("2d");
    let raf;
    const frame = () => {
      paso(grafoRef.current);
      dibujar(ctx, grafoRef.current, selRef.current);
      raf = requestAnimationFrame(frame);
    };
    frame();
    return () => cancelAnimationFrame(raf);
  }, []);

  function clic(e) {
    const r = canvasRef.current.getBoundingClientRect();
    const x = ((e.clientX - r.left) * W) / r.width;
    const y = ((e.clientY - r.top) * H) / r.height;
    let mejor = null, dmin = 1e9;
    grafoRef.current.nodos.forEach((nd) => {
      const d = Math.hypot(nd.x - x, nd.y - y);
      if (d < dmin) { dmin = d; mejor = nd; }
    });
    setSel(mejor && dmin < 26 ? mejor.t : null);
  }

  const terms = dicc ? Object.keys(dicc) : [];

  return (
    <section className="card">
      <h3>🕸️ Grafo de conocimiento</h3>
      {terms.length === 0 ? (
        <p className="vacio">Escribe pensamientos en el cuaderno y aquí verás cómo se conectan tus ideas.</p>
      ) : (
        <>
          <p className="hint">Nodo = término · línea = ideas que comparten términos · clic en un nodo.</p>
          <canvas ref={canvasRef} width={W} height={H} className="grafo" onClick={clic} />
          {sel && dicc[sel] && (
            <div className="result">
              <h4>{sel} ({dicc[sel].length})</h4>
              <ul className="entradas">
                {dicc[sel].map((p, i) => <li key={i}>{p.texto}</li>)}
              </ul>
            </div>
          )}
        </>
      )}
    </section>
  );
}
