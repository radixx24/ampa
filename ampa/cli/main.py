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
from ..answer import responder
from ..core import paths as paths_mod
from ..core import platform_info
from ..memory import (
    cargar_fragmentos,
    fuentes,
    ingerir,
    recuperar,
    reiniciar,
    ruta_memoria,
)
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


def _cmd_recordar(
    texto, desde, fuente, max_palabras, solapamiento, reiniciar_, sin_clasificar
) -> int:
    if texto is None and desde is None:
        print("error: indica --texto o --desde.", file=sys.stderr)
        return 2
    if reiniciar_:
        reiniciar()
    frags = ingerir(
        texto=texto,
        ruta_fuente=Path(desde) if desde else None,
        fuente=fuente,
        clasificar=not sin_clasificar,
        max_palabras=max_palabras,
        solapamiento=solapamiento,
    )
    print(f"Ingeridos {len(frags)} fragmentos en {ruta_memoria()}")
    return 0


def _cmd_consultar(consulta, k) -> int:
    resultados = recuperar(consulta, k)
    if not resultados:
        print("Sin coincidencias en la memoria.")
        return 0
    for n, resultado in enumerate(resultados, 1):
        fragmento = resultado.fragmento
        extracto = " ".join(fragmento.texto.split())
        if len(extracto) > 160:
            extracto = extracto[:157] + "..."
        print(f"{n}. {resultado.cita()} ({fragmento.dominio}, score {resultado.score})")
        print(f"   {extracto}")
    return 0


def _cmd_memoria() -> int:
    frags = cargar_fragmentos()
    lista_fuentes = fuentes()
    print(f"Memoria: {ruta_memoria()}")
    print(f"Fragmentos: {len(frags)} · Fuentes: {len(lista_fuentes)}")
    for nombre in lista_fuentes:
        print(f"  - {nombre}")
    return 0


def _cmd_responder(consulta, k, detalle) -> int:
    resp = responder(consulta, k)
    print(resp.texto())
    if detalle:
        print("\n[diagnóstico]")
        print(resp.diagnostico())
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

    p_rec = sub.add_parser("recordar", help="Ingiere apuntes en la memoria documental.")
    grupo_rec = p_rec.add_mutually_exclusive_group()
    grupo_rec.add_argument("--texto", default=None, help="Texto a recordar.")
    grupo_rec.add_argument("--desde", default=None, help="Archivo de apuntes a ingerir.")
    p_rec.add_argument(
        "--fuente", default=None, help="Nombre de la fuente (aparece en las citas)."
    )
    p_rec.add_argument(
        "--max-palabras",
        type=int,
        default=120,
        dest="max_palabras",
        help="Tamaño máximo de cada fragmento, en palabras.",
    )
    p_rec.add_argument(
        "--solapamiento",
        type=int,
        default=20,
        help="Solapamiento entre fragmentos largos, en palabras.",
    )
    p_rec.add_argument(
        "--reiniciar", action="store_true", help="Vacía la memoria antes de ingerir."
    )
    p_rec.add_argument(
        "--sin-clasificar",
        action="store_true",
        dest="sin_clasificar",
        help="No etiqueta el dominio de cada fragmento.",
    )

    p_con = sub.add_parser(
        "consultar", help="Recupera fragmentos relevantes de la memoria, con citas."
    )
    p_con.add_argument("consulta", help="La consulta o pregunta.")
    p_con.add_argument(
        "-k", type=int, default=5, help="Número de fragmentos a devolver."
    )

    sub.add_parser("memoria", help="Muestra el estado de la memoria documental.")

    p_resp = sub.add_parser(
        "responder", help="Responde una pregunta con fuentes de la memoria."
    )
    p_resp.add_argument("consulta", help="La pregunta.")
    p_resp.add_argument(
        "-k", type=int, default=3, help="Fragmentos a considerar como evidencia."
    )
    p_resp.add_argument(
        "--detalle",
        action="store_true",
        help="Muestra el diagnóstico (percepción de la consulta + scores).",
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
    if args.comando == "recordar":
        return _cmd_recordar(
            args.texto,
            args.desde,
            args.fuente,
            args.max_palabras,
            args.solapamiento,
            args.reiniciar,
            args.sin_clasificar,
        )
    if args.comando == "consultar":
        return _cmd_consultar(args.consulta, args.k)
    if args.comando == "memoria":
        return _cmd_memoria()
    if args.comando == "responder":
        return _cmd_responder(args.consulta, args.k, args.detalle)

    # Sin subcomando: mostrar la ayuda.
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
