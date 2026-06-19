"""Recuperación léxica portable (BM25) con citas.

Primera iteración **sin embeddings** (ADR 0010): ranking BM25 sobre los
fragmentos almacenados. Cada resultado conserva su fuente e índice para **citar**
el origen. Solo biblioteca estándar.
"""
from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from .documents import Fragmento
from .store import cargar_fragmentos

_TOKEN = re.compile(r"[a-z0-9]+")


def _sin_acentos(texto: str) -> str:
    descompuesto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in descompuesto if not unicodedata.combining(c))


def tokenizar(texto: str) -> List[str]:
    """Normaliza (minúsculas, sin acentos) y extrae los tokens alfanuméricos."""
    return _TOKEN.findall(_sin_acentos(texto.lower()))


@dataclass
class Resultado:
    """Fragmento recuperado con su puntuación de relevancia."""

    fragmento: Fragmento
    score: float

    def cita(self) -> str:
        return f"[{self.fragmento.fuente}#{self.fragmento.indice}]"


class Indice:
    """Índice BM25 en memoria sobre una lista de fragmentos."""

    def __init__(
        self, fragmentos: List[Fragmento], k1: float = 1.5, b: float = 0.75
    ) -> None:
        self.fragmentos = fragmentos
        self.k1 = k1
        self.b = b
        self._tokens = [tokenizar(f.texto) for f in fragmentos]
        self._tf = [Counter(t) for t in self._tokens]
        self.N = len(fragmentos)
        self.avgdl = (sum(len(t) for t in self._tokens) / self.N) if self.N else 0.0
        df: Counter = Counter()
        for tokens in self._tokens:
            df.update(set(tokens))
        self.idf = {
            termino: math.log(1 + (self.N - n + 0.5) / (n + 0.5))
            for termino, n in df.items()
        }

    def buscar(self, consulta: str, k: int = 5) -> List[Resultado]:
        terminos = tokenizar(consulta)
        resultados: List[Resultado] = []
        for i, fragmento in enumerate(self.fragmentos):
            dl = len(self._tokens[i])
            score = 0.0
            for termino in terminos:
                frecuencia = self._tf[i].get(termino, 0)
                if not frecuencia:
                    continue
                idf = self.idf.get(termino, 0.0)
                denom = (
                    frecuencia + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
                    if self.avgdl
                    else 1.0
                )
                score += idf * (frecuencia * (self.k1 + 1)) / denom
            if score > 0:
                resultados.append(Resultado(fragmento=fragmento, score=round(score, 4)))
        resultados.sort(key=lambda r: r.score, reverse=True)
        return resultados[:k]


def recuperar(
    consulta: str,
    k: int = 5,
    *,
    ruta: Optional[Path] = None,
    fragmentos: Optional[List[Fragmento]] = None,
) -> List[Resultado]:
    """Recupera los ``k`` fragmentos más relevantes para ``consulta``, con citas."""
    frags = fragmentos if fragmentos is not None else cargar_fragmentos(ruta)
    return Indice(frags).buscar(consulta, k)
