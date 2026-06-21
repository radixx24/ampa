"""Diccionario curado de compuestos comunes (nombre en español → fórmula).

Pequeña base de compuestos frecuentes en química general para reconocerlos por
**nombre** además de por fórmula. Sin dependencias.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from .elements import normalizar

# (nombre con acentos para mostrar, fórmula)
_COMPUESTOS: List[Tuple[str, str]] = [
    ("agua", "H2O"),
    ("peróxido de hidrógeno", "H2O2"),
    ("agua oxigenada", "H2O2"),
    ("cloruro de sodio", "NaCl"),
    ("sal común", "NaCl"),
    ("dióxido de carbono", "CO2"),
    ("monóxido de carbono", "CO"),
    ("ozono", "O3"),
    ("amoníaco", "NH3"),
    ("amoniaco", "NH3"),
    ("metano", "CH4"),
    ("etano", "C2H6"),
    ("propano", "C3H8"),
    ("butano", "C4H10"),
    ("etanol", "C2H6O"),
    ("alcohol etílico", "C2H6O"),
    ("metanol", "CH4O"),
    ("glucosa", "C6H12O6"),
    ("sacarosa", "C12H22O11"),
    ("ácido sulfúrico", "H2SO4"),
    ("ácido clorhídrico", "HCl"),
    ("ácido nítrico", "HNO3"),
    ("ácido fosfórico", "H3PO4"),
    ("ácido acético", "C2H4O2"),
    ("ácido carbónico", "H2CO3"),
    ("hidróxido de sodio", "NaOH"),
    ("sosa cáustica", "NaOH"),
    ("hidróxido de potasio", "KOH"),
    ("hidróxido de calcio", "Ca(OH)2"),
    ("bicarbonato de sodio", "NaHCO3"),
    ("carbonato de calcio", "CaCO3"),
    ("cloruro de potasio", "KCl"),
    ("óxido de calcio", "CaO"),
    ("dióxido de azufre", "SO2"),
    ("trióxido de azufre", "SO3"),
    ("benceno", "C6H6"),
    ("acetona", "C3H6O"),
    ("urea", "CH4N2O"),
    ("sulfato de cobre", "CuSO4"),
]

# nombre normalizado → fórmula
NOMBRE_A_FORMULA: Dict[str, str] = {
    normalizar(nombre): formula for nombre, formula in _COMPUESTOS
}

# fórmula → primer nombre (con acentos) para mostrar
FORMULA_A_NOMBRE: Dict[str, str] = {}
for _nombre, _formula in _COMPUESTOS:
    FORMULA_A_NOMBRE.setdefault(_formula, _nombre)
