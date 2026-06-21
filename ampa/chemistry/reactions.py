"""Inferencia de reacciones posibles según la composición y los grupos.

Devuelve reacciones plausibles para una molécula: la **combustión** se balancea
de verdad (coeficientes enteros); las demás se proponen de forma cualitativa a
partir de los grupos funcionales. Sin dependencias externas.
"""
from __future__ import annotations

import functools
from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Dict, List, Optional

from .groups import grupos_funcionales
from .molecules import Molecula


@dataclass
class Reaccion:
    tipo: str
    ecuacion: str
    descripcion: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {"tipo": self.tipo, "ecuacion": self.ecuacion, "descripcion": self.descripcion}


def _coef(n: int, formula: str) -> str:
    return (f"{n} " if n != 1 else "") + formula


def _combustion(mol: Molecula) -> Optional[Reaccion]:
    comp = mol.composicion()
    if set(comp) - {"C", "H", "O"}:
        return None  # solo hidrocarburos / compuestos C-H-O
    c, h, o = comp.get("C", 0), comp.get("H", 0), comp.get("O", 0)
    if c == 0 or h == 0:
        return None
    o2 = Fraction(c) + Fraction(h, 4) - Fraction(o, 2)
    if o2 <= 0:
        return None
    coeffs = [Fraction(1), o2, Fraction(c), Fraction(h, 2)]
    lcm = functools.reduce(
        lambda x, y: x * y // gcd(x, y), [f.denominator for f in coeffs]
    )
    enteros = [int(f * lcm) for f in coeffs]
    divisor = functools.reduce(gcd, enteros)
    fuel, o2i, co2i, h2oi = [n // divisor for n in enteros]
    ecuacion = (
        f"{_coef(fuel, mol.formula())} + {_coef(o2i, 'O2')} → "
        f"{_coef(co2i, 'CO2')} + {_coef(h2oi, 'H2O')}"
    )
    return Reaccion("combustión", ecuacion, "Combustión completa con oxígeno.")


def reacciones(mol: Molecula) -> List[Reaccion]:
    """Reacciones plausibles para ``mol`` según su composición y grupos."""
    resultado: List[Reaccion] = []
    combustion = _combustion(mol)
    if combustion:
        resultado.append(combustion)

    grupos = grupos_funcionales(mol)
    formula = mol.formula()
    if "alqueno" in grupos or "alquino" in grupos:
        resultado.append(
            Reaccion(
                "hidrogenación",
                f"{formula} + H2 → alcano",
                "Adición de H2 al enlace múltiple (catalizada).",
            )
        )
    if "ácido carboxílico" in grupos:
        resultado.append(
            Reaccion(
                "neutralización",
                f"{formula} + NaOH → sal + H2O",
                "Reacción ácido–base con una base.",
            )
        )
        if "alcohol" in grupos:
            resultado.append(
                Reaccion(
                    "esterificación",
                    "ácido + alcohol → éster + H2O",
                    "Esterificación de Fischer.",
                )
            )
    if "alcohol" in grupos:
        resultado.append(
            Reaccion(
                "oxidación",
                f"{formula} → aldehído/cetona → ácido",
                "Oxidación del grupo alcohol.",
            )
        )
    return resultado
