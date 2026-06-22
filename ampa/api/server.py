"""API JSON portable de AMPA (solo biblioteca estándar).

Expone los dominios (química, filosofía) por HTTP/JSON para un frontend (p. ej.
React). **Cero dependencias**: usa ``http.server``. Incluye cabeceras CORS para
poder llamarla desde el servidor de desarrollo del frontend.
"""
from __future__ import annotations

import json
import mimetypes
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

from .. import __version__
from ..chemistry import (
    analizar_enlaces,
    balancear,
    cargar_compuestos,
    compatibilidad,
    ecuacion,
    geometria_3d,
    grupos_funcionales,
    guardar_compuesto,
    proyectar,
    reacciones,
    tabla,
)
from ..chemistry import identificar as identificar_quimica
from ..chemistry.molecules import Molecula
from ..philosophy import identificar as identificar_filosofia
from ..philosophy import notebook


def _analizar_molecula(datos: dict) -> dict:
    mol = Molecula.from_dict(datos)
    mol.validar()
    salida = mol.to_dict()
    salida["grupos_funcionales"] = grupos_funcionales(mol)
    salida["reacciones"] = [r.to_dict() for r in reacciones(mol)]
    salida["enlaces_analisis"] = analizar_enlaces(mol)
    return salida


def _reacciones(datos: dict) -> list:
    mol = Molecula.from_dict(datos)
    mol.validar()
    return [r.to_dict() for r in reacciones(mol)]


def _geometria(datos: dict) -> dict:
    mol = Molecula.from_dict(datos)
    mol.validar()
    return {
        "atomos": geometria_3d(mol),
        "enlaces": [list(e) for e in mol.enlaces],
        "formula": mol.formula(),
    }


def _guardar_compuesto(datos: dict) -> dict:
    mol = Molecula.from_dict(datos)
    guardar_compuesto(mol)
    return {"guardado": True, "nombre": mol.nombre, "formula": mol.formula()}


def _especies(valor: object) -> list:
    """Normaliza reactivos/productos a una lista de fórmulas (acepta lista o texto)."""
    if isinstance(valor, str):
        partes = valor.replace("+", ",").split(",")
    elif isinstance(valor, (list, tuple)):
        partes = [str(v) for v in valor]
    else:
        partes = []
    return [p.strip() for p in partes if p and p.strip()]


def _temperatura(datos: dict) -> float:
    try:
        return float(datos.get("temperatura", 298.15))
    except (TypeError, ValueError):
        return 298.15


def _balancear(datos: dict) -> dict:
    reactivos = _especies(datos.get("reactivos"))
    productos = _especies(datos.get("productos"))
    coefs = balancear(reactivos, productos)
    if coefs is None:
        return {"ok": False, "razon": "no se pudo balancear (¿faltan o sobran especies?)"}
    cr, cp = coefs
    return {
        "ok": True,
        "ecuacion": ecuacion(reactivos, productos, coefs),
        "coeficientes": {"reactivos": cr, "productos": cp},
    }


def _proyectar(datos: dict) -> dict:
    return proyectar(
        _especies(datos.get("reactivos")),
        _especies(datos.get("productos")),
        _temperatura(datos),
    )


def _compatibilidad(datos: dict) -> dict:
    return compatibilidad(
        str(datos.get("a", "")), str(datos.get("b", "")), _temperatura(datos)
    )


def _pensar(datos: dict) -> dict:
    pensamiento = notebook.agregar(datos.get("texto", ""), datos.get("terminos"))
    return pensamiento.to_dict()


def _diccionario(_: dict) -> dict:
    return {t: [p.to_dict() for p in ps] for t, ps in notebook.diccionario().items()}


# (método, ruta) → función(datos) → cuerpo serializable
_RUTAS: Dict[Tuple[str, str], Callable[[dict], object]] = {
    ("GET", "/api/salud"): lambda d: {"estado": "ok", "version": __version__},
    ("GET", "/api/quimica/tabla"): lambda d: [e.to_dict() for e in tabla()],
    ("POST", "/api/quimica/identificar"): lambda d: identificar_quimica(
        d.get("texto", "")
    ).to_dict(),
    ("POST", "/api/quimica/analizar"): _analizar_molecula,
    ("POST", "/api/quimica/reacciones"): _reacciones,
    ("POST", "/api/quimica/geometria"): _geometria,
    ("POST", "/api/quimica/balancear"): _balancear,
    ("POST", "/api/quimica/proyectar"): _proyectar,
    ("POST", "/api/quimica/compatibilidad"): _compatibilidad,
    ("GET", "/api/quimica/compuestos"): lambda d: [
        m.to_dict() for m in cargar_compuestos()
    ],
    ("POST", "/api/quimica/compuestos"): _guardar_compuesto,
    ("POST", "/api/filosofia/identificar"): lambda d: identificar_filosofia(
        d.get("texto", "")
    ).to_dict(),
    ("POST", "/api/filosofia/pensar"): _pensar,
    ("GET", "/api/filosofia/diccionario"): _diccionario,
}


def manejar(metodo: str, ruta: str, datos: Optional[dict] = None) -> Tuple[int, object]:
    """Despacha una petición (puro, sin sockets): devuelve (status, cuerpo)."""
    ruta = ruta.split("?", 1)[0].rstrip("/") or "/"
    funcion = _RUTAS.get((metodo, ruta))
    if funcion is None:
        return 404, {"error": "ruta no encontrada", "ruta": ruta}
    try:
        return 200, funcion(datos or {})
    except ValueError as exc:
        return 400, {"error": str(exc)}


def resolver_estatico(estaticos: Optional[Path], ruta: str) -> Tuple[int, bytes, str]:
    """Resuelve un archivo del frontend compilado, con fallback SPA a index.html."""
    if not estaticos or not estaticos.exists():
        return 404, b"frontend sin compilar (npm run build en frontend/)", "text/plain; charset=utf-8"
    rel = ruta.split("?", 1)[0].lstrip("/") or "index.html"
    archivo = estaticos / rel
    try:
        archivo = archivo.resolve()
        archivo.relative_to(estaticos.resolve())
    except (ValueError, OSError):
        archivo = estaticos / "index.html"
    if not archivo.is_file():
        archivo = estaticos / "index.html"  # fallback SPA
    if not archivo.is_file():
        return 404, b"no encontrado", "text/plain; charset=utf-8"
    tipo = mimetypes.guess_type(str(archivo))[0] or "application/octet-stream"
    return 200, archivo.read_bytes(), tipo


class _Handler(BaseHTTPRequestHandler):
    estaticos: Optional[Path] = None

    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _responder(self, status: int, cuerpo: object) -> None:
        datos = json.dumps(cuerpo, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_OPTIONS(self) -> None:  # noqa: N802 (firma de http.server)
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        if self.path.startswith("/api/"):
            self._responder(*manejar("GET", self.path))
            return
        status, datos, tipo = resolver_estatico(self.estaticos, self.path)
        self.send_response(status)
        self.send_header("Content-Type", tipo)
        self._cors()
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_POST(self) -> None:  # noqa: N802
        longitud = int(self.headers.get("Content-Length", 0) or 0)
        crudo = self.rfile.read(longitud) if longitud else b""
        try:
            datos = json.loads(crudo) if crudo else {}
        except json.JSONDecodeError:
            self._responder(400, {"error": "JSON inválido"})
            return
        self._responder(*manejar("POST", self.path, datos))

    def log_message(self, *args) -> None:  # silencioso
        pass


def servir(
    puerto: int = 8000, host: str = "127.0.0.1", estaticos: Optional[Path] = None
) -> None:
    """Arranca la API (y, si existe, el frontend compilado) hasta Ctrl+C."""
    if estaticos is None:
        if getattr(sys, "frozen", False):  # ejecutable empaquetado (PyInstaller)
            estaticos = Path(getattr(sys, "_MEIPASS", ".")) / "frontend" / "dist"
        else:
            estaticos = Path(__file__).resolve().parents[2] / "frontend" / "dist"
    estaticos = Path(estaticos)
    _Handler.estaticos = estaticos if estaticos.exists() else None
    servidor = ThreadingHTTPServer((host, puerto), _Handler)
    que = "web + API" if _Handler.estaticos else "API"
    print(f"AMPA ({que}) en http://{host}:{puerto}  (Ctrl+C para parar)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nDetenido.")
    finally:
        servidor.server_close()
