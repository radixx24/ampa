"""Ingesta de apuntes a la memoria documental.

Trocea el texto, etiqueta cada fragmento con su **dominio probable** (reutilizando
la capa de percepción) y lo persiste. Sin dependencias externas.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

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
