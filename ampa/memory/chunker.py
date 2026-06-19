"""Troceo (chunking) de apuntes en fragmentos citables.

Estrategia portable y predecible: respeta los párrafos (separados por líneas en
blanco) y parte los más largos en ventanas de palabras con solapamiento, para no
cortar ideas a la mitad. Sin dependencias externas.
"""
from __future__ import annotations

import re
from typing import List

_PARRAFOS = re.compile(r"\n\s*\n")


def trocear(texto: str, max_palabras: int = 120, solapamiento: int = 20) -> List[str]:
    """Divide ``texto`` en fragmentos de hasta ``max_palabras`` palabras.

    Los párrafos cortos se conservan enteros; los largos se parten en ventanas
    solapadas (``solapamiento`` palabras) para preservar el contexto entre cortes.
    """
    if max_palabras <= 0:
        raise ValueError("max_palabras debe ser positivo")
    solapamiento = max(0, min(solapamiento, max_palabras - 1))
    paso = max_palabras - solapamiento

    fragmentos: List[str] = []
    for parrafo in _PARRAFOS.split(texto):
        palabras = parrafo.split()
        if not palabras:
            continue
        if len(palabras) <= max_palabras:
            fragmentos.append(" ".join(palabras))
            continue
        for inicio in range(0, len(palabras), paso):
            fragmentos.append(" ".join(palabras[inicio : inicio + max_palabras]))
            if inicio + max_palabras >= len(palabras):
                break
    return fragmentos
