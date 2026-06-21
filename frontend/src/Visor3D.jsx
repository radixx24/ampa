import { useEffect, useRef } from "react";
import { api } from "./api.js";

const COLOR = {
  H: "#dfe3ea", C: "#3a4150", O: "#e06c75", N: "#61afef",
  S: "#e5c07b", Cl: "#98c379", P: "#d19a66", F: "#56b6c2", Br: "#c0744a",
};
const RADIO = { H: 11, C: 17, O: 16, N: 16, S: 19, Cl: 19, P: 19, F: 14, Br: 20 };
const TEXTO_OSCURO = new Set(["H", "F", "S", "Cl"]);
const colorDe = (e) => COLOR[e] || "#7a8290";
const radioDe = (e) => RADIO[e] || 15;

function oscurecer(hex, f = 0.42) {
  const n = parseInt(hex.slice(1), 16);
  return `rgb(${Math.round(((n >> 16) & 255) * f)},${Math.round(((n >> 8) & 255) * f)},${Math.round((n & 255) * f)})`;
}

export default function Visor3D({ molecula, onCerrar }) {
  const canvasRef = useRef(null);
  const geoRef = useRef(null);
  const errRef = useRef("");
  const estado = useRef({ rotX: 0.45, rotY: 0, auto: true, drag: false, lx: 0, ly: 0 });

  useEffect(() => {
    let vivo = true;
    geoRef.current = null;
    errRef.current = "";
    api.geometria(molecula)
      .then((g) => { if (vivo) geoRef.current = g; })
      .catch((e) => { errRef.current = "" + e; });
    return () => { vivo = false; };
  }, [molecula]);

  useEffect(() => {
    const ctx = canvasRef.current.getContext("2d");
    let raf;
    const frame = () => {
      const s = estado.current;
      if (s.auto && !s.drag) s.rotY += 0.012;
      dibujar(ctx, canvasRef.current, geoRef.current, s.rotX, s.rotY, errRef.current);
      raf = requestAnimationFrame(frame);
    };
    frame();
    return () => cancelAnimationFrame(raf);
  }, []);

  const down = (e) => { const s = estado.current; s.drag = true; s.lx = e.clientX; s.ly = e.clientY; };
  const move = (e) => {
    const s = estado.current;
    if (!s.drag) return;
    s.rotY += (e.clientX - s.lx) * 0.01;
    s.rotX += (e.clientY - s.ly) * 0.01;
    s.lx = e.clientX; s.ly = e.clientY;
  };
  const up = () => { estado.current.drag = false; };

  return (
    <div className="visor3d">
      <div className="visor-top">
        <b>🧊 Vista 3D — gira sola · arrastra para rotar</b>
        <span>
          <button className="sec" onClick={() => { estado.current.auto = !estado.current.auto; }}>⏯ Auto</button>
          <button className="sec" onClick={onCerrar}>Cerrar</button>
        </span>
      </div>
      <canvas
        ref={canvasRef} width={520} height={360} className="canvas3d"
        onPointerDown={down} onPointerMove={move} onPointerUp={up} onPointerLeave={up}
      />
    </div>
  );
}

function dibujar(ctx, canvas, geo, rotX, rotY, err) {
  const W = canvas.width;
  const H = canvas.height;
  const fondo = ctx.createLinearGradient(0, 0, 0, H);
  fondo.addColorStop(0, "#0c1220");
  fondo.addColorStop(1, "#0e1116");
  ctx.fillStyle = fondo;
  ctx.fillRect(0, 0, W, H);
  if (err) {
    ctx.fillStyle = "#f87171"; ctx.font = "13px sans-serif"; ctx.fillText(err, 14, 24);
    return;
  }
  if (!geo || !geo.atomos || !geo.atomos.length) {
    ctx.fillStyle = "#9aa7b4"; ctx.font = "13px sans-serif";
    ctx.fillText("Calculando geometría…", 14, 24);
    return;
  }
  const cx = Math.cos(rotX), sx = Math.sin(rotX), cy = Math.cos(rotY), sy = Math.sin(rotY);
  const escala = 64;
  const pts = geo.atomos.map((a) => {
    const x1 = a.x * cy - a.z * sy;
    const z1 = a.x * sy + a.z * cy;
    const y1 = a.y * cx - z1 * sx;
    const z2 = a.y * sx + z1 * cx;
    const persp = 5 / (5 + z2);
    return { el: a.el, sx: W / 2 + x1 * escala * persp, sy: H / 2 + y1 * escala * persp, z: z2, persp };
  });
  ctx.lineCap = "round";
  (geo.enlaces || []).forEach(([a, b]) => {
    const A = pts[a], B = pts[b];
    if (!A || !B) return;
    ctx.strokeStyle = "#7e889a";
    ctx.lineWidth = 5 * ((A.persp + B.persp) / 2);
    ctx.beginPath(); ctx.moveTo(A.sx, A.sy); ctx.lineTo(B.sx, B.sy); ctx.stroke();
  });
  pts.map((_, i) => i).sort((i, j) => pts[i].z - pts[j].z).forEach((i) => {
    const p = pts[i];
    const r = radioDe(p.el) * p.persp;
    const col = colorDe(p.el);
    const grad = ctx.createRadialGradient(p.sx - r * 0.35, p.sy - r * 0.35, r * 0.1, p.sx, p.sy, r);
    grad.addColorStop(0, "#ffffff");
    grad.addColorStop(0.25, col);
    grad.addColorStop(1, oscurecer(col));
    ctx.fillStyle = grad;
    ctx.beginPath(); ctx.arc(p.sx, p.sy, r, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = TEXTO_OSCURO.has(p.el) ? "#1a1f27" : "#fff";
    ctx.font = `700 ${Math.max(9, r * 0.82)}px sans-serif`;
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(p.el, p.sx, p.sy);
  });
}
