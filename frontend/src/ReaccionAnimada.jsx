import { useEffect, useMemo, useRef } from "react";
import Icon from "./Icon.jsx";

const COLOR = {
  H: "#dfe3ea", C: "#3a4150", O: "#e06c75", N: "#61afef",
  S: "#e5c07b", Cl: "#98c379", P: "#d19a66", F: "#56b6c2",
};
const RAD = { H: 7, C: 13, O: 12, N: 12, default: 11 };
const TEXTO_OSCURO = new Set(["H", "F", "S", "Cl"]);
const W = 520;
const H = 300;

const gcd = (a, b) => (b ? gcd(b, a % b) : a);
const gcdArr = (xs) => xs.reduce(gcd);
const ease = (t) => t * t * (3 - 2 * t);
const lerp = (a, b, t) => a + (b - a) * t;

function hill(atomos) {
  const c = atomos.filter((e) => e === "C").length;
  const h = atomos.filter((e) => e === "H").length;
  const resto = {};
  atomos.forEach((e) => { if (e !== "C" && e !== "H") resto[e] = (resto[e] || 0) + 1; });
  const t = (s, n) => s + (n > 1 ? n : "");
  let f = "";
  if (c) f += t("C", c);
  if (h) f += t("H", h);
  Object.keys(resto).sort().forEach((s) => { f += t(s, resto[s]); });
  return f || "?";
}

function balance(atomos) {
  const c = atomos.filter((e) => e === "C").length;
  const h = atomos.filter((e) => e === "H").length;
  const o = atomos.filter((e) => e === "O").length;
  if (!c || !h) return null;
  let fuel = 4, o2 = 4 * c + h - 2 * o, co2 = 4 * c, h2o = 2 * h;
  if (o2 <= 0) return null;
  const g = gcdArr([fuel, o2, co2, h2o]);
  return { fuel: fuel / g, o2: o2 / g, co2: co2 / g, h2o: h2o / g };
}

function anillo(atomos, cx, cy, r) {
  if (atomos.length === 1) return [[cx, cy]];
  return atomos.map((_, i) => {
    const a = (2 * Math.PI * i) / atomos.length - Math.PI / 2;
    return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
  });
}

function emitir(species, x, r, lista, bonds) {
  const n = species.length;
  species.forEach((sp, k) => {
    const cy = 44 + (H - 88) * (n === 1 ? 0.5 : k / (n - 1));
    const base = lista.length;
    const pos = anillo(sp.atoms, x, cy, r);
    sp.atoms.forEach((el, j) => lista.push({ el, x: pos[j][0], y: pos[j][1] }));
    sp.bonds.forEach(([a, b, o]) => bonds.push([base + a, base + b, o]));
  });
}

function construirCombustion(molecula) {
  const bal = balance(molecula.atomos);
  if (!bal) return null;
  const fuelSp = Array.from({ length: bal.fuel }, () => ({ atoms: molecula.atomos, bonds: molecula.enlaces }));
  const o2Sp = Array.from({ length: bal.o2 }, () => ({ atoms: ["O", "O"], bonds: [[0, 1, 2]] }));
  const co2Sp = Array.from({ length: bal.co2 }, () => ({ atoms: ["C", "O", "O"], bonds: [[0, 1, 2], [0, 2, 2]] }));
  const h2oSp = Array.from({ length: bal.h2o }, () => ({ atoms: ["O", "H", "H"], bonds: [[0, 1, 1], [0, 2, 1]] }));
  const R = [], Rb = [], P = [], Pb = [];
  emitir(fuelSp, 150, 24, R, Rb);
  emitir(o2Sp, 58, 14, R, Rb);
  emitir(co2Sp, 372, 18, P, Pb);
  emitir(h2oSp, 466, 16, P, Pb);
  const porElR = {}, porElP = {};
  R.forEach((a, i) => (porElR[a.el] ||= []).push(i));
  P.forEach((a, i) => (porElP[a.el] ||= []).push(i));
  const pares = [];
  const rPar = new Array(R.length);
  const pPar = new Array(P.length);
  Object.keys(porElR).forEach((el) => {
    const ri = porElR[el], pi = porElP[el] || [];
    for (let k = 0; k < ri.length; k++) {
      const idx = pares.length;
      pares.push({ el, rx: R[ri[k]].x, ry: R[ri[k]].y, px: P[pi[k]].x, py: P[pi[k]].y });
      rPar[ri[k]] = idx;
      pPar[pi[k]] = idx;
    }
  });
  return {
    modo: "atomos",
    pares,
    bondsR: Rb.map(([a, b, o]) => [rPar[a], rPar[b], o]),
    bondsP: Pb.map(([a, b, o]) => [pPar[a], pPar[b], o]),
    ecuacion: `${bal.fuel > 1 ? bal.fuel + " " : ""}${hill(molecula.atomos)} + ${bal.o2 > 1 ? bal.o2 + " " : ""}O₂ → ${bal.co2 > 1 ? bal.co2 + " " : ""}CO₂ + ${bal.h2o > 1 ? bal.h2o + " " : ""}H₂O`,
  };
}

function construir(molecula, tipo) {
  if (tipo === "combustion") return construirCombustion(molecula);
  const f = hill(molecula.atomos);
  if (tipo === "hidrogenacion") {
    const f2 = hill([...molecula.atomos, "H", "H"]);
    return { modo: "tokens", reactivos: [f, "H₂"], productos: [f2], ecuacion: `${f} + H₂ → ${f2}` };
  }
  if (tipo === "neutralizacion") {
    return { modo: "tokens", reactivos: [f, "NaOH"], productos: ["sal", "H₂O"], ecuacion: `${f} + NaOH → sal + H₂O` };
  }
  return null;
}

const TITULO = {
  combustion: "Combustión — la materia se conserva",
  hidrogenacion: "Hidrogenación — adición de H₂",
  neutralizacion: "Neutralización — ácido + base",
};

export default function ReaccionAnimada({ molecula, tipo, onCerrar }) {
  const canvasRef = useRef(null);
  const datos = useMemo(() => construir(molecula, tipo), [molecula, tipo]);

  useEffect(() => {
    if (!datos) return;
    const ctx = canvasRef.current.getContext("2d");
    let raf;
    const inicio = performance.now();
    const frame = (now) => {
      const t = ((now - inicio) / 4000) % 1;
      if (datos.modo === "atomos") dibujarAtomos(ctx, datos, t);
      else dibujarTokens(ctx, datos, t);
      raf = requestAnimationFrame(frame);
    };
    raf = requestAnimationFrame(frame);
    return () => cancelAnimationFrame(raf);
  }, [datos]);

  return (
    <div className="visor3d">
      <div className="visor-top">
        <b><Icon name="film" size={15} /> {TITULO[tipo] || "Reacción"}</b>
        <button className="sec" onClick={onCerrar}><Icon name="x" size={14} /> Cerrar</button>
      </div>
      {datos ? (
        <>
          <canvas ref={canvasRef} width={W} height={H} className="canvas3d" />
          <p className="ecuacion">{datos.ecuacion}</p>
        </>
      ) : (
        <p className="err" style={{ padding: 14 }}>No se puede animar esta reacción para esta molécula.</p>
      )}
    </div>
  );
}

function fondoCanvas(ctx) {
  const g = ctx.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, "#0c1220");
  g.addColorStop(1, "#0e1116");
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, W, H);
}

function destello(ctx, t) {
  const flash = Math.max(0, 1 - Math.abs(t - 0.5) * 6);
  if (flash <= 0) return;
  const g = ctx.createRadialGradient(W / 2, H / 2, 4, W / 2, H / 2, 130);
  g.addColorStop(0, `rgba(255,170,80,${0.5 * flash})`);
  g.addColorStop(1, "rgba(255,170,80,0)");
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, W, H);
}

function dibujarAtomos(ctx, datos, t) {
  fondoCanvas(ctx);
  const e = ease(t);
  const pos = datos.pares.map((p) => ({
    el: p.el,
    x: p.rx + (p.px - p.rx) * e,
    y: p.ry + (p.py - p.ry) * e + Math.sin(t * Math.PI) * 14,
  }));
  ctx.fillStyle = "#9aa7b4";
  ctx.font = "12px sans-serif";
  ctx.textAlign = "left";
  ctx.globalAlpha = Math.max(0, 1 - t * 2);
  ctx.fillText("reactivos", 14, 18);
  ctx.globalAlpha = Math.max(0, t * 2 - 1);
  ctx.textAlign = "right";
  ctx.fillText("productos", W - 14, 18);
  ctx.globalAlpha = 1;
  const bonds = (lista, alpha) => {
    if (alpha <= 0.01) return;
    ctx.globalAlpha = alpha;
    ctx.strokeStyle = "#7e889a";
    ctx.lineWidth = 3;
    ctx.lineCap = "round";
    lista.forEach(([a, b]) => {
      ctx.beginPath();
      ctx.moveTo(pos[a].x, pos[a].y);
      ctx.lineTo(pos[b].x, pos[b].y);
      ctx.stroke();
    });
    ctx.globalAlpha = 1;
  };
  bonds(datos.bondsR, Math.max(0, 1 - t * 2.2) * 0.8);
  bonds(datos.bondsP, Math.max(0, t * 2.2 - 1.2) * 0.8);
  destello(ctx, t);
  pos.forEach((p) => {
    const r = RAD[p.el] || RAD.default;
    const col = COLOR[p.el] || "#7a8290";
    const grad = ctx.createRadialGradient(p.x - r * 0.35, p.y - r * 0.35, r * 0.1, p.x, p.y, r);
    grad.addColorStop(0, "#ffffff");
    grad.addColorStop(0.3, col);
    grad.addColorStop(1, "rgba(0,0,0,0.45)");
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = TEXTO_OSCURO.has(p.el) ? "#1a1f27" : "#fff";
    ctx.font = `700 ${Math.max(8, r * 0.85)}px sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(p.el, p.x, p.y);
  });
}

function pildora(ctx, texto, x, y, alpha) {
  ctx.globalAlpha = alpha;
  ctx.font = "700 15px ui-monospace, Menlo, monospace";
  const w = ctx.measureText(texto).width + 28;
  const h = 34;
  ctx.fillStyle = "#1c232d";
  ctx.strokeStyle = "#6ee7b7";
  ctx.lineWidth = 1.5;
  const rx = x - w / 2, ry = y - h / 2, r = 9;
  ctx.beginPath();
  ctx.moveTo(rx + r, ry);
  ctx.arcTo(rx + w, ry, rx + w, ry + h, r);
  ctx.arcTo(rx + w, ry + h, rx, ry + h, r);
  ctx.arcTo(rx, ry + h, rx, ry, r);
  ctx.arcTo(rx, ry, rx + w, ry, r);
  ctx.fill();
  ctx.stroke();
  ctx.fillStyle = "#e6edf3";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(texto, x, y);
  ctx.globalAlpha = 1;
}

function dibujarTokens(ctx, datos, t) {
  fondoCanvas(ctx);
  const fila = (n, i) => H / 2 + (i - (n - 1) / 2) * 52;
  if (t < 0.5) {
    const tt = ease(t / 0.5);
    datos.reactivos.forEach((txt, i) =>
      pildora(ctx, txt, lerp(130, W / 2, tt), fila(datos.reactivos.length, i), 1 - tt * 0.7)
    );
  } else {
    const tt = ease((t - 0.5) / 0.5);
    datos.productos.forEach((txt, i) =>
      pildora(ctx, txt, lerp(W / 2, W - 130, tt), fila(datos.productos.length, i), 0.3 + tt * 0.7)
    );
  }
  destello(ctx, t);
  ctx.fillStyle = "#6ee7b7";
  ctx.font = "26px sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.globalAlpha = Math.max(0, 1 - Math.abs(t - 0.5) * 5);
  ctx.fillText("→", W / 2, H / 2);
  ctx.globalAlpha = 1;
}
