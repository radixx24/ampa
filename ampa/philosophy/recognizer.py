"""Reconocedor de entidades filosóficas en texto libre (sin dependencias).

Identifica **filósofos**, **corrientes** y **conceptos** por nombre (coincidencia
de palabra completa, sin acentos) y los devuelve **estructurados** (con época,
corriente o rama). Misma estrategia de reglas + datos que el dominio químico.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List

from .data import CONCEPTOS, CORRIENTES, FILOSOFOS, normalizar


def _regex(claves) -> "re.Pattern[str]":
    ordenadas = sorted(claves, key=len, reverse=True)
    return re.compile(r"\b(?:" + "|".join(re.escape(c) for c in ordenadas) + r")\b")


_RE_FILOSOFOS = _regex(FILOSOFOS)
_RE_CONCEPTOS = _regex(CONCEPTOS)
_RE_CORRIENTES = _regex(CORRIENTES)


@dataclass
class EntidadFilosofica:
    """Una entidad filosófica detectada, estructurada para consumo programático."""

    tipo: str  # "filósofo" | "corriente" | "concepto"
    nombre: str
    categoria: str = ""  # filósofo→corriente; concepto→rama
    epoca: str = ""
    texto: str = ""

    def to_dict(self) -> Dict[str, object]:
        return {
            "tipo": self.tipo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "epoca": self.epoca,
            "texto": self.texto,
        }


@dataclass
class ResultadoFilosofia:
    entidades: List[EntidadFilosofica] = field(default_factory=list)

    @property
    def filosofos(self) -> List[EntidadFilosofica]:
        return [e for e in self.entidades if e.tipo == "filósofo"]

    @property
    def corrientes(self) -> List[EntidadFilosofica]:
        return [e for e in self.entidades if e.tipo == "corriente"]

    @property
    def conceptos(self) -> List[EntidadFilosofica]:
        return [e for e in self.entidades if e.tipo == "concepto"]

    def hay(self) -> bool:
        return bool(self.entidades)

    def to_dict(self) -> Dict[str, object]:
        return {
            "filosofos": [e.to_dict() for e in self.filosofos],
            "corrientes": [e.to_dict() for e in self.corrientes],
            "conceptos": [e.to_dict() for e in self.conceptos],
        }


def identificar(texto: str) -> ResultadoFilosofia:
    """Identifica filósofos, corrientes y conceptos en ``texto``."""
    norm = normalizar(texto)
    entidades: Dict[tuple, EntidadFilosofica] = {}

    for match in _RE_FILOSOFOS.finditer(norm):
        nombre, epoca, corriente = FILOSOFOS[match.group(0)]
        entidades.setdefault(
            ("filósofo", nombre),
            EntidadFilosofica(
                "filósofo", nombre, corriente, epoca, texto[match.start():match.end()]
            ),
        )

    for match in _RE_CORRIENTES.finditer(norm):
        nombre = CORRIENTES[match.group(0)]
        entidades.setdefault(
            ("corriente", nombre),
            EntidadFilosofica("corriente", nombre, texto=texto[match.start():match.end()]),
        )

    for match in _RE_CONCEPTOS.finditer(norm):
        nombre, rama = CONCEPTOS[match.group(0)]
        entidades.setdefault(
            ("concepto", nombre),
            EntidadFilosofica("concepto", nombre, rama, texto=texto[match.start():match.end()]),
        )

    orden = {"filósofo": 0, "corriente": 1, "concepto": 2}
    ordenadas = sorted(entidades.values(), key=lambda e: (orden[e.tipo], e.nombre))
    return ResultadoFilosofia(entidades=ordenadas)
