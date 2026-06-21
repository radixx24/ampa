"""Reconocedor de entidades químicas en texto libre (sin dependencias).

Identifica **elementos** (por nombre o fórmula de un solo elemento) y
**compuestos** (por nombre curado o por fórmula), y los devuelve **estructurados**
(símbolo, número atómico, composición) para usos visuales/adaptativos.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .compounds import FORMULA_A_NOMBRE, NOMBRE_A_FORMULA
from .elements import ELEMENTOS, NOMBRE_A_SIMBOLO, normalizar
from .formulas import composicion_valida

# Nombres de elemento demasiado comunes como palabra corriente: solo por fórmula.
_AMBIGUOS = {"radio"}

# Candidato a fórmula (se valida después con composicion_valida).
_RE_FORMULA = re.compile(r"[A-Z][A-Za-z0-9()]*")

_NOMBRES_ELEMENTO = sorted(
    (n for n in NOMBRE_A_SIMBOLO if n not in _AMBIGUOS), key=len, reverse=True
)
_RE_NOMBRE_ELEMENTO = re.compile(
    r"\b(?:" + "|".join(re.escape(n) for n in _NOMBRES_ELEMENTO) + r")\b"
)
_NOMBRES_COMPUESTO = sorted(NOMBRE_A_FORMULA, key=len, reverse=True)


@dataclass
class EntidadQuimica:
    """Una entidad química detectada, estructurada para consumo programático."""

    tipo: str  # "elemento" | "compuesto"
    nombre: str
    formula: str
    simbolo: str = ""
    numero_atomico: int = 0
    composicion: Dict[str, int] = field(default_factory=dict)
    texto: str = ""

    def to_dict(self) -> Dict[str, object]:
        return {
            "tipo": self.tipo,
            "nombre": self.nombre,
            "formula": self.formula,
            "simbolo": self.simbolo,
            "numero_atomico": self.numero_atomico,
            "composicion": self.composicion,
            "texto": self.texto,
        }


@dataclass
class ResultadoQuimica:
    entidades: List[EntidadQuimica] = field(default_factory=list)

    @property
    def elementos(self) -> List[EntidadQuimica]:
        return [e for e in self.entidades if e.tipo == "elemento"]

    @property
    def compuestos(self) -> List[EntidadQuimica]:
        return [e for e in self.entidades if e.tipo == "compuesto"]

    def hay(self) -> bool:
        return bool(self.entidades)

    def to_dict(self) -> Dict[str, object]:
        return {
            "elementos": [e.to_dict() for e in self.elementos],
            "compuestos": [e.to_dict() for e in self.compuestos],
        }


def _solapa(span: Tuple[int, int], spans: List[Tuple[int, int]]) -> bool:
    inicio, fin = span
    return any(inicio < b and a < fin for a, b in spans)


def identificar(texto: str) -> ResultadoQuimica:
    """Identifica elementos y compuestos en ``texto`` y los devuelve estructurados."""
    norm = normalizar(texto)
    entidades: Dict[Tuple[str, str], EntidadQuimica] = {}
    spans_compuesto: List[Tuple[int, int]] = []

    # 1. Compuestos por nombre (curado).
    for nombre in _NOMBRES_COMPUESTO:
        for match in re.finditer(r"\b" + re.escape(nombre) + r"\b", norm):
            spans_compuesto.append(match.span())
            formula = NOMBRE_A_FORMULA[nombre]
            clave = ("compuesto", formula)
            if clave not in entidades:
                entidades[clave] = EntidadQuimica(
                    tipo="compuesto",
                    nombre=FORMULA_A_NOMBRE.get(formula, nombre),
                    formula=formula,
                    composicion=composicion_valida(formula) or {},
                    texto=texto[match.start():match.end()],
                )

    # 2. Fórmulas (sobre el texto original, sensible a mayúsculas).
    for match in _RE_FORMULA.finditer(texto):
        candidato = match.group(0)
        composicion = composicion_valida(candidato)
        if composicion is None:
            continue
        tiene_digito = any(c.isdigit() for c in candidato)
        if not tiene_digito and len(composicion) < 2:
            continue  # símbolo suelto: se detecta por nombre, no por fórmula
        if len(composicion) == 1:
            simbolo = next(iter(composicion))
            clave = ("elemento", simbolo)
            if clave not in entidades:
                z, nombre = ELEMENTOS[simbolo]
                entidades[clave] = EntidadQuimica(
                    tipo="elemento", nombre=nombre, formula=candidato,
                    simbolo=simbolo, numero_atomico=z,
                    composicion=dict(composicion), texto=candidato,
                )
        else:
            clave = ("compuesto", candidato)
            if clave not in entidades:
                entidades[clave] = EntidadQuimica(
                    tipo="compuesto",
                    nombre=FORMULA_A_NOMBRE.get(candidato, ""),
                    formula=candidato, composicion=composicion, texto=candidato,
                )

    # 3. Elementos por nombre (omitiendo los que caen dentro de un compuesto).
    for match in _RE_NOMBRE_ELEMENTO.finditer(norm):
        if _solapa(match.span(), spans_compuesto):
            continue
        simbolo = NOMBRE_A_SIMBOLO[match.group(0)]
        clave = ("elemento", simbolo)
        if clave not in entidades:
            z, nombre = ELEMENTOS[simbolo]
            entidades[clave] = EntidadQuimica(
                tipo="elemento", nombre=nombre, formula=simbolo, simbolo=simbolo,
                numero_atomico=z, composicion={simbolo: 1},
                texto=texto[match.start():match.end()],
            )

    elementos = sorted(
        (e for e in entidades.values() if e.tipo == "elemento"),
        key=lambda e: e.numero_atomico,
    )
    compuestos = sorted(
        (e for e in entidades.values() if e.tipo == "compuesto"),
        key=lambda e: e.formula,
    )
    return ResultadoQuimica(entidades=elementos + compuestos)
