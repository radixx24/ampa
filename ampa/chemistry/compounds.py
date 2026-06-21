"""Diccionario curado de compuestos comunes (nombre en español → fórmula).

Base de compuestos frecuentes en química general para reconocerlos por **nombre**
además de por fórmula. Ampliable. Sin dependencias.
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
    ("eteno", "C2H4"),
    ("etileno", "C2H4"),
    ("etino", "C2H2"),
    ("acetileno", "C2H2"),
    ("etanol", "C2H6O"),
    ("alcohol etílico", "C2H6O"),
    ("metanol", "CH4O"),
    ("propanol", "C3H8O"),
    ("glicerina", "C3H8O3"),
    ("glicerol", "C3H8O3"),
    ("glucosa", "C6H12O6"),
    ("sacarosa", "C12H22O11"),
    ("benceno", "C6H6"),
    ("tolueno", "C7H8"),
    ("acetona", "C3H6O"),
    ("formaldehído", "CH2O"),
    ("cloroformo", "CHCl3"),
    ("urea", "CH4N2O"),
    ("cafeína", "C8H10N4O2"),
    ("aspirina", "C9H8O4"),
    ("ácido acetilsalicílico", "C9H8O4"),
    ("ácido sulfúrico", "H2SO4"),
    ("ácido clorhídrico", "HCl"),
    ("ácido nítrico", "HNO3"),
    ("ácido fosfórico", "H3PO4"),
    ("ácido acético", "C2H4O2"),
    ("vinagre", "C2H4O2"),
    ("ácido carbónico", "H2CO3"),
    ("ácido fluorhídrico", "HF"),
    ("ácido bromhídrico", "HBr"),
    ("ácido cianhídrico", "HCN"),
    ("ácido sulfhídrico", "H2S"),
    ("sulfuro de hidrógeno", "H2S"),
    ("ácido fórmico", "CH2O2"),
    ("ácido láctico", "C3H6O3"),
    ("ácido cítrico", "C6H8O7"),
    ("hidróxido de sodio", "NaOH"),
    ("sosa cáustica", "NaOH"),
    ("hidróxido de potasio", "KOH"),
    ("hidróxido de calcio", "Ca(OH)2"),
    ("hidróxido de amonio", "NH4OH"),
    ("bicarbonato de sodio", "NaHCO3"),
    ("carbonato de sodio", "Na2CO3"),
    ("carbonato de calcio", "CaCO3"),
    ("cloruro de potasio", "KCl"),
    ("cloruro de calcio", "CaCl2"),
    ("cloruro de amonio", "NH4Cl"),
    ("óxido de calcio", "CaO"),
    ("óxido de magnesio", "MgO"),
    ("óxido de aluminio", "Al2O3"),
    ("óxido de hierro", "Fe2O3"),
    ("dióxido de azufre", "SO2"),
    ("trióxido de azufre", "SO3"),
    ("dióxido de nitrógeno", "NO2"),
    ("óxido nítrico", "NO"),
    ("óxido nitroso", "N2O"),
    ("sulfato de cobre", "CuSO4"),
    ("sulfato de sodio", "Na2SO4"),
    ("sulfato de amonio", "(NH4)2SO4"),
    ("nitrato de sodio", "NaNO3"),
    ("nitrato de potasio", "KNO3"),
    ("fosfato de calcio", "Ca3(PO4)2"),
]

# nombre normalizado → fórmula
NOMBRE_A_FORMULA: Dict[str, str] = {
    normalizar(nombre): formula for nombre, formula in _COMPUESTOS
}

# fórmula → primer nombre (con acentos) para mostrar
FORMULA_A_NOMBRE: Dict[str, str] = {}
for _nombre, _formula in _COMPUESTOS:
    FORMULA_A_NOMBRE.setdefault(_formula, _nombre)
