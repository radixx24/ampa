"""API JSON portable de AMPA (solo biblioteca estándar).

Expone los dominios (química, filosofía) por HTTP/JSON para un frontend (p. ej.
React). **Cero dependencias**: usa ``http.server``. Incluye cabeceras CORS para
poder llamarla desde el servidor de desarrollo del frontend.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable, Dict, Optional, Tuple

from .. import __version__
from ..chemistry import (
    cargar_compuestos,
    grupos_funcionales,
    guardar_compuesto,
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
    return salida


def _guardar_compuesto(datos: dict) -> dict:
    mol = Molecula.from_dict(datos)
    guardar_compuesto(mol)
    return {"guardado": True, "nombre": mol.nombre, "formula": mol.formula()}


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


class _Handler(BaseHTTPRequestHandler):
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
        self._responder(*manejar("GET", self.path))

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


def servir(puerto: int = 8000, host: str = "127.0.0.1") -> None:
    """Arranca la API en ``host:puerto`` hasta Ctrl+C."""
    servidor = ThreadingHTTPServer((host, puerto), _Handler)
    print(f"AMPA API en http://{host}:{puerto}  (Ctrl+C para parar)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nDetenido.")
    finally:
        servidor.server_close()
