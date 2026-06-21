"""Ingesta de apuntes a la memoria documental.

Trocea el texto, etiqueta cada fragmento con su **dominio probable** (reutilizando
la capa de percepción) y lo persiste. Sin dependencias externas.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

from ..perception import perceive
from .chunker import trocear
from .documents import Fragmento
from .store import guardar_fragmentos


def ingerir(
    *,
    texto: Optional[str] = None,
    ruta_fuente: Optional[Path] = None,
    fuente: Optional[str] = None,
    clasificar: bool = True,
    max_palabras: int = 120,
    solapamiento: int = 20,
    ruta: Optional[Path] = None,
) -> List[Fragmento]:
    """Ingiere texto (o un archivo) en la memoria y devuelve los fragmentos.

    El dominio de cada fragmento se infiere con la percepción salvo que
    ``clasificar=False``.
    """
    if texto is None and ruta_fuente is None:
        raise ValueError("Indica 'texto' o 'ruta_fuente'.")
    if texto is None:
        ruta_fuente = Path(ruta_fuente)  # type: ignore[arg-type]
        texto = ruta_fuente.read_text(encoding="utf-8")
        fuente = fuente or ruta_fuente.name
    fuente = fuente or "texto"

    fragmentos: List[Fragmento] = []
    for indice, trozo in enumerate(trocear(texto, max_palabras, solapamiento)):
        dominio = perceive(trozo).dominio_probable if clasificar else "general"
        fragmentos.append(
            Fragmento(texto=trozo, fuente=fuente, indice=indice, dominio=dominio)
        )
    guardar_fragmentos(fragmentos, ruta)
    return fragmentos


@dataclass
class ResultadoIngesta:
    """Resumen de una ingesta de carpeta."""

    archivos: int
    fragmentos: int
    por_archivo: List[Tuple[str, int]]
    omitidos: int = 0


def ingerir_carpeta(
    carpeta: Path,
    *,
    extensiones: Sequence[str] = (".md", ".txt"),
    clasificar: bool = True,
    max_palabras: int = 120,
    solapamiento: int = 20,
    ruta: Optional[Path] = None,
) -> ResultadoIngesta:
    """Ingiere recursivamente los archivos de ``carpeta`` (por defecto .md/.txt).

    Cada fragmento se cita por su **ruta relativa** (POSIX) dentro de la carpeta,
    estable entre sistemas. Los archivos ilegibles (binarios, permisos) se omiten.
    """
    carpeta = Path(carpeta)
    if not carpeta.is_dir():
        raise ValueError(f"No es una carpeta: {carpeta}")
    exts = tuple(e.lower() for e in extensiones)

    por_archivo: List[Tuple[str, int]] = []
    fragmentos_total = 0
    omitidos = 0
    for archivo in sorted(carpeta.rglob("*")):
        if not archivo.is_file() or archivo.suffix.lower() not in exts:
            continue
        fuente = archivo.relative_to(carpeta).as_posix()
        try:
            frags = ingerir(
                ruta_fuente=archivo,
                fuente=fuente,
                clasificar=clasificar,
                max_palabras=max_palabras,
                solapamiento=solapamiento,
                ruta=ruta,
            )
        except (UnicodeDecodeError, OSError):
            omitidos += 1
            continue
        if frags:
            por_archivo.append((fuente, len(frags)))
            fragmentos_total += len(frags)
    return ResultadoIngesta(
        archivos=len(por_archivo),
        fragmentos=fragmentos_total,
        por_archivo=por_archivo,
        omitidos=omitidos,
    )
