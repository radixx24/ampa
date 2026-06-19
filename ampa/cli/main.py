"""CLI portable de AMPA.

Usa solo ``argparse`` de la biblioteca estándar para máxima portabilidad.
Puntos de entrada: el comando ``ampa`` (ver ``pyproject.toml``) o
``python -m ampa``.
"""
from __future__ import annotations

import argparse
from typing import Optional, Sequence

from .. import __version__
from ..core import paths as paths_mod
from ..core import platform_info
from ..perception import journal, perceive


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

    # Sin subcomando: mostrar la ayuda.
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
