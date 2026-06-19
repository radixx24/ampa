"""CLI portable de AMPA.

Usa solo ``argparse`` de la biblioteca estándar para máxima portabilidad.
Puntos de entrada: el comando ``ampa`` (ver ``pyproject.toml``) o
``python -m ampa``.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .. import __version__
from ..core import paths as paths_mod
from ..core import platform_info
from ..perception import journal, perceive
from ..scribe import writer as scribe


def _cmd_version() -> int:
    print(f"AMPA {__version__}")
    return 0


def _cmd_info() -> int:
    print(f"AMPA {__version__}")
    print("\n[Plataforma]")
    for clave, valor in platform_info.summary().items():
        print(f"  {clave:14}: {valor}")

    rutas = paths_mod.get_paths()
    print("\n[Rutas portables]")
    for ruta in rutas.all():
        etiqueta = "home" if ruta == rutas.home else ruta.name
        print(f"  {etiqueta:14}: {ruta}")
    return 0


def _cmd_paths(crear: bool) -> int:
    rutas = paths_mod.get_paths()
    if crear:
        rutas.create()
        print(f"Carpetas creadas bajo: {rutas.home}")
    else:
        for ruta in rutas.all():
            print(ruta)
    return 0


def _cmd_percibir(texto, tipo, archivos, registrar) -> int:
    evento = perceive(texto, tipo=tipo, archivos=archivos)
    print(evento.as_yaml(), end="")
    if registrar:
        if journal.registrar(evento):
            print(f"  → registrado en el diario: {journal.ruta_diario()}")
        else:
            print("  → no registrado (guardar_en_memoria=false)")
    return 0


def _cmd_diario() -> int:
    registros = journal.leer()
    print(f"Diario: {journal.ruta_diario()}")
    print(f"Eventos registrados: {len(registros)}")
    for registro in registros[-5:]:
        print(
            f"  - [{registro.get('timestamp', '')}] "
            f"{registro.get('tipo', '')}/{registro.get('dominio_probable', '')}"
            f" · riesgo {registro.get('riesgo_operativo', '')}"
        )
    return 0


def _cmd_escribir(ruta, contenido, desde, riesgo, simular, forzar, sin_respaldo) -> int:
    if contenido is None and desde is None:
        print("error: indica --contenido o --desde.", file=sys.stderr)
        return 2
    if contenido is None:
        contenido = (
            sys.stdin.read() if desde == "-" else Path(desde).read_text(encoding="utf-8")
        )
    res = scribe.escribir(
        ruta,
        contenido,
        riesgo=riesgo,
        simular=simular,
        forzar=forzar,
        respaldar=not sin_respaldo,
    )
    print(res.resumen())
    return 0 if (res.escrito or res.simulado) else 1


def _cmd_restaurar(ruta, respaldo) -> int:
    res = scribe.restaurar(ruta, respaldo)
    print(res.resumen())
    return 0 if res.escrito else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ampa",
        description="AMPA — sistema local de lenguaje, percepción y memoria.",
    )
    parser.add_argument(
        "--version", action="version", version=f"AMPA {__version__}"
    )
    sub = parser.add_subparsers(dest="comando")

    sub.add_parser("info", help="Muestra la plataforma y las rutas portables.")
    sub.add_parser("version", help="Muestra la versión.")
    p_paths = sub.add_parser("paths", help="Lista o crea las carpetas de AMPA.")
    p_paths.add_argument(
        "--create", action="store_true", help="Crea las carpetas en disco."
    )

    p_perc = sub.add_parser(
        "percibir", help="Estructura una entrada como evento de percepción."
    )
    p_perc.add_argument("texto", help="El texto a percibir.")
    p_perc.add_argument(
        "--tipo",
        default=None,
        help="Tipo de evento (pregunta, comando, correccion, error, decision).",
    )
    p_perc.add_argument(
        "--archivo",
        action="append",
        default=None,
        dest="archivos",
        help="Archivo relacionado (se puede repetir).",
    )
    p_perc.add_argument(
        "--registrar",
        action="store_true",
        help="Registra el evento en el diario si la política de memoria lo permite.",
    )

    sub.add_parser("diario", help="Muestra los eventos registrados en el diario.")

    p_esc = sub.add_parser(
        "escribir",
        help="Escribe un archivo de forma segura (respaldo + simulación).",
    )
    p_esc.add_argument("ruta", help="Ruta del archivo a escribir.")
    grupo = p_esc.add_mutually_exclusive_group()
    grupo.add_argument("--contenido", default=None, help="Contenido literal a escribir.")
    grupo.add_argument(
        "--desde",
        default=None,
        help="Lee el contenido de un archivo ('-' = entrada estándar).",
    )
    p_esc.add_argument(
        "--riesgo",
        choices=("bajo", "medio", "alto"),
        default="bajo",
        help="Riesgo operativo; 'alto' bloquea la escritura salvo --forzar.",
    )
    p_esc.add_argument(
        "--simular",
        action="store_true",
        help="No toca el disco; describe lo que haría.",
    )
    p_esc.add_argument(
        "--forzar",
        action="store_true",
        help="Autoriza la escritura aunque el riesgo sea alto.",
    )
    p_esc.add_argument(
        "--sin-respaldo",
        action="store_true",
        dest="sin_respaldo",
        help="No crea respaldo previo al sobrescribir.",
    )

    p_rest = sub.add_parser(
        "restaurar", help="Restaura un archivo desde su respaldo más reciente."
    )
    p_rest.add_argument("ruta", help="Ruta del archivo a restaurar.")
    p_rest.add_argument(
        "--respaldo",
        default=None,
        help="Respaldo específico (por defecto, el más reciente).",
    )

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Punto de entrada. Devuelve el código de salida del proceso."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.comando == "info":
        return _cmd_info()
    if args.comando == "version":
        return _cmd_version()
    if args.comando == "paths":
        return _cmd_paths(args.create)
    if args.comando == "percibir":
        return _cmd_percibir(args.texto, args.tipo, args.archivos, args.registrar)
    if args.comando == "diario":
        return _cmd_diario()
    if args.comando == "escribir":
        return _cmd_escribir(
            args.ruta,
            args.contenido,
            args.desde,
            args.riesgo,
            args.simular,
            args.forzar,
            args.sin_respaldo,
        )
    if args.comando == "restaurar":
        return _cmd_restaurar(args.ruta, args.respaldo)

    # Sin subcomando: mostrar la ayuda.
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
