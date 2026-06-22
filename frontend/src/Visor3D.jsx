import { useEffect, useRef } from "react";
import { api } from "./api.js";
import Icon from "./Icon.jsx";

const COLOR = {
  H: "#dfe3ea", C: "#3a4150", O: "#e06c75", N: "#61afef",
  S: "#e5c07b", Cl: "#98c379", P: "#d19a66", F: "#56b6c2", Br: "#c0744a",
};
const TEXTO_OSCURO = new Set(["H", "F", "S", "Cl"]);
const colorDe = (e) => COLOR[e] || "#7a8290";
const ESCALA = 64; // px por ångström de posición
const ESCALA_R = 26; // px por ångström de radio atómico

function oscurecer(hex, f = 0.42) {
  const n = parseInt(hex.slice(1), 16);
  return `rgb(${Math.round(((n >> 16) & 255) * f)},${Math.round(((n >> 8) & 255) * f)},${Math.round((n & 255) * f)})`;
}

export default function Visor3D({ molecula, temp = 298, onCerrar }) {
  const canvasRef = useRef(null);
  const geoRef = useRef(null);
  const errRef = useRef("");
  const tempRef = useRef(temp);
  tempRef.current = temp;
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
      dibujar(ctx, canvasRef.current, geoRef.current, s.rotX, s.rotY, errRef.current, tempRef.current, performance.now());
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

  function exportarPNG() {
    const a = document.createElement("a");
    a.download = (molecula.nombre || "molecula") + "-3d.png";
    a.href = canvasRef.current.toDataURL("image/png");
    a.click();
  }

  return (
    <div className="visor3d">
      <div className="visor-top">
        <b><Icon name="cube" size={15} /> Vista 3D — gira sola · arrastra para rotar</b>
        <span>
          <button className="sec" onClick={() => { estado.current.auto = !estado.current.auto; }} title="Pausar/reanudar giro"><Icon name="play" size={14} /> Auto</button>
          <button className="sec" onClick={exportarPNG}><Icon name="image" size={14} /> PNG</button>
          <button className="sec" onClick={onCerrar}><Icon name="x" size={14} /> Cerrar</button>
        </span>
      </div>
      <canvas
        ref={canvasRef} width={520} height={360} className="canvas3d"
        onPointerDown={down} onPointerMove={move} onPointerUp={up} onPointerLeave={up}
      />
    </div>
  );
}

function dibujar(ctx, canvas, geo, rotX, rotY, err, temp, now) {
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
  const amp = Math.min(8, (temp || 0) / 90); // vibración térmica ∝ temperatura
  const pts = geo.atomos.map((a, i) => {
    const x1 = a.x * cy - a.z * sy;
    const z1 = a.x * sy + a.z * cy;
    const y1 = a.y * cx - z1 * sx;
    const z2 = a.y * sx + z1 * cx;
    const persp = 5 / (5 + z2);
    const jx = Math.sin(now * 0.006 + i * 1.7) * amp;
    const jy = Math.cos(now * 0.005 + i * 2.3) * amp;
    return {
      el: a.el, radio: a.radio || 0.7, z: z2, persp,
      sx: W / 2 + x1 * ESCALA * persp + jx, sy: H / 2 + y1 * ESCALA * persp + jy,
    };
  });

  // Enlaces: dobles/triples como líneas paralelas (perpendicular en 2D proyectado).
  ctx.lineCap = "round";
  ctx.strokeStyle = "#7e889a";
  (geo.enlaces || []).forEach(([a, b, orden]) => {
    const A = pts[a], B = pts[b];
    if (!A || !B) return;
    const dx = B.sx - A.sx, dy = B.sy - A.sy;
    const len = Math.hypot(dx, dy) || 1;
    const ox = -dy / len, oy = dx / len;
    const offs = orden === 2 ? [-3.2, 3.2] : orden === 3 ? [-5.5, 0, 5.5] : [0];
    const w = (orden > 1 ? 3.4 : 4.6) * ((A.persp + B.persp) / 2);
    ctx.lineWidth = w;
    offs.forEach((o) => {
      ctx.beginPath();
      ctx.moveTo(A.sx + ox * o, A.sy + oy * o);
      ctx.lineTo(B.sx + ox * o, B.sy + oy * o);
      ctx.stroke();
    });
  });

  // Átomos: del más lejano al más cercano, tamaño por radio covalente.
  pts.map((_, i) => i).sort((i, j) => pts[i].z - pts[j].z).forEach((i) => {
    const p = pts[i];
    const r = Math.max(5, p.radio * ESCALA_R * p.persp);
    const col = colorDe(p.el);
    const grad = ctx.createRadialGradient(p.sx - r * 0.35, p.sy - r * 0.35, r * 0.1, p.sx, p.sy, r);
    grad.addColorStop(0, "#ffffff");
    grad.addColorStop(0.25, col);
    grad.addColorStop(1, oscurecer(col));
    ctx.fillStyle = grad;
    ctx.beginPath(); ctx.arc(p.sx, p.sy, r, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = TEXTO_OSCURO.has(p.el) ? "#1a1f27" : "#fff";
    ctx.font = `700 ${Math.max(8, r * 0.8)}px sans-serif`;
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(p.el, p.sx, p.sy);
  });
}
