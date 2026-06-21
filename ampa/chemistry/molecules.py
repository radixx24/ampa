"""Modelo de moléculas (átomos + enlaces) y persistencia de compuestos.

Una :class:`Molecula` es un grafo: **átomos** (símbolos) y **enlaces** con orden
(1 simple, 2 doble, 3 triple). Deriva su **fórmula** (notación de Hill),
composición y **masa molar**, y se guarda/lee en JSONL portable. Es la base del
**editor de enlaces de carbono** (los grupos funcionales y las reacciones se
construyen sobre este modelo). Sin dependencias externas.
"""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ..core.paths import get_paths
from .elements import ELEMENTOS
from .formulas import masa_molar

NOMBRE_ARCHIVO = "compuestos.jsonl"

Enlace = Tuple[int, int, int]  # (átomo a, átomo b, orden)


@dataclass
class Molecula:
    """Molécula como grafo de átomos y enlaces, con datos derivados."""

    nombre: str = ""
    atomos: List[str] = field(default_factory=list)
    enlaces: List[Enlace] = field(default_factory=list)

    def composicion(self) -> Dict[str, int]:
        return dict(Counter(self.atomos))

    def formula(self) -> str:
        """Fórmula en notación de Hill (C, luego H, luego el resto alfabético)."""
        comp = Counter(self.atomos)
        partes: List[str] = []

        def agregar(simbolo: str) -> None:
            cuenta = comp.pop(simbolo)
            partes.append(f"{simbolo}{cuenta if cuenta > 1 else ''}")

        if "C" in comp:
            agregar("C")
            if "H" in comp:
                agregar("H")
        for simbolo in sorted(comp):
            partes.append(f"{simbolo}{comp[simbolo] if comp[simbolo] > 1 else ''}")
        return "".join(partes)

    def masa_molar(self) -> float:
        return masa_molar(self.composicion())

    def validar(self) -> "Molecula":
        """Verifica símbolos reales e índices/órdenes de enlace válidos."""
        n = len(self.atomos)
        for simbolo in self.atomos:
            if simbolo not in ELEMENTOS:
                raise ValueError(f"Elemento desconocido: {simbolo!r}")
        for a, b, orden in self.enlaces:
            if not (0 <= a < n and 0 <= b < n):
                raise ValueError(f"Enlace fuera de rango: {(a, b, orden)}")
            if a == b:
                raise ValueError("Un enlace no puede unir un átomo consigo mismo")
            if orden not in (1, 2, 3):
                raise ValueError(f"Orden de enlace inválido: {orden}")
        return self

    def to_dict(self) -> Dict[str, object]:
        return {
            "nombre": self.nombre,
            "atomos": list(self.atomos),
            "enlaces": [list(e) for e in self.enlaces],
            "formula": self.formula(),
            "composicion": self.composicion(),
            "masa_molar": round(self.masa_molar(), 3),
        }

    @classmethod
    def from_dict(cls, datos: Dict[str, object]) -> "Molecula":
        try:
            atomos = [str(a) for a in datos.get("atomos", [])]
            enlaces = [
                (int(e[0]), int(e[1]), int(e[2])) for e in datos.get("enlaces", [])
            ]
        except (TypeError, ValueError, IndexError) as exc:
            raise ValueError(f"Molécula mal formada: {exc}") from exc
        return cls(nombre=str(datos.get("nombre", "")), atomos=atomos, enlaces=enlaces)


def ruta_compuestos(ruta: Optional[Path] = None) -> Path:
    if ruta is not None:
        return ruta
    return get_paths().data / NOMBRE_ARCHIVO


def guardar_compuesto(mol: Molecula, ruta: Optional[Path] = None) -> Path:
    """Valida y guarda un compuesto (alimentado por el usuario) en JSONL portable."""
    mol.validar()
    destino = ruta_compuestos(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(mol.to_dict(), ensure_ascii=False) + "\n")
    return destino


def cargar_compuestos(ruta: Optional[Path] = None) -> List[Molecula]:
    destino = ruta_compuestos(ruta)
    if not destino.exists():
        return []
    compuestos: List[Molecula] = []
    with destino.open("r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                compuestos.append(Molecula.from_dict(json.loads(linea)))
    return compuestos
