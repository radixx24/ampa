"""Tabla periódica y utilidades de elementos (datos estáticos, sin dependencias).

`ELEMENTOS` mapea símbolo → (número atómico, nombre en español). Es la base de
datos para el reconocimiento químico y para usos **visuales** (color, posición,
masa) en capas superiores.
"""
from __future__ import annotations

from typing import Dict, Tuple

# Tabla de transliteración para normalizar nombres (sin acentos, minúsculas).
_TABLA = str.maketrans("áéíóúüñ", "aeiouun")


def normalizar(texto: str) -> str:
    """Minúsculas y sin acentos, preservando longitud (útil para spans)."""
    return texto.lower().translate(_TABLA)


# símbolo → (Z, nombre en español). Ordenado por número atómico.
ELEMENTOS: Dict[str, Tuple[int, str]] = {
    "H": (1, "hidrógeno"), "He": (2, "helio"), "Li": (3, "litio"),
    "Be": (4, "berilio"), "B": (5, "boro"), "C": (6, "carbono"),
    "N": (7, "nitrógeno"), "O": (8, "oxígeno"), "F": (9, "flúor"),
    "Ne": (10, "neón"), "Na": (11, "sodio"), "Mg": (12, "magnesio"),
    "Al": (13, "aluminio"), "Si": (14, "silicio"), "P": (15, "fósforo"),
    "S": (16, "azufre"), "Cl": (17, "cloro"), "Ar": (18, "argón"),
    "K": (19, "potasio"), "Ca": (20, "calcio"), "Sc": (21, "escandio"),
    "Ti": (22, "titanio"), "V": (23, "vanadio"), "Cr": (24, "cromo"),
    "Mn": (25, "manganeso"), "Fe": (26, "hierro"), "Co": (27, "cobalto"),
    "Ni": (28, "níquel"), "Cu": (29, "cobre"), "Zn": (30, "zinc"),
    "Ga": (31, "galio"), "Ge": (32, "germanio"), "As": (33, "arsénico"),
    "Se": (34, "selenio"), "Br": (35, "bromo"), "Kr": (36, "criptón"),
    "Rb": (37, "rubidio"), "Sr": (38, "estroncio"), "Y": (39, "itrio"),
    "Zr": (40, "circonio"), "Nb": (41, "niobio"), "Mo": (42, "molibdeno"),
    "Tc": (43, "tecnecio"), "Ru": (44, "rutenio"), "Rh": (45, "rodio"),
    "Pd": (46, "paladio"), "Ag": (47, "plata"), "Cd": (48, "cadmio"),
    "In": (49, "indio"), "Sn": (50, "estaño"), "Sb": (51, "antimonio"),
    "Te": (52, "telurio"), "I": (53, "yodo"), "Xe": (54, "xenón"),
    "Cs": (55, "cesio"), "Ba": (56, "bario"), "La": (57, "lantano"),
    "Ce": (58, "cerio"), "Pr": (59, "praseodimio"), "Nd": (60, "neodimio"),
    "Pm": (61, "prometio"), "Sm": (62, "samario"), "Eu": (63, "europio"),
    "Gd": (64, "gadolinio"), "Tb": (65, "terbio"), "Dy": (66, "disprosio"),
    "Ho": (67, "holmio"), "Er": (68, "erbio"), "Tm": (69, "tulio"),
    "Yb": (70, "iterbio"), "Lu": (71, "lutecio"), "Hf": (72, "hafnio"),
    "Ta": (73, "tantalio"), "W": (74, "wolframio"), "Re": (75, "renio"),
    "Os": (76, "osmio"), "Ir": (77, "iridio"), "Pt": (78, "platino"),
    "Au": (79, "oro"), "Hg": (80, "mercurio"), "Tl": (81, "talio"),
    "Pb": (82, "plomo"), "Bi": (83, "bismuto"), "Po": (84, "polonio"),
    "At": (85, "astato"), "Rn": (86, "radón"), "Fr": (87, "francio"),
    "Ra": (88, "radio"), "Ac": (89, "actinio"), "Th": (90, "torio"),
    "Pa": (91, "protactinio"), "U": (92, "uranio"), "Np": (93, "neptunio"),
    "Pu": (94, "plutonio"), "Am": (95, "americio"), "Cm": (96, "curio"),
    "Bk": (97, "berkelio"), "Cf": (98, "californio"), "Es": (99, "einstenio"),
    "Fm": (100, "fermio"), "Md": (101, "mendelevio"), "No": (102, "nobelio"),
    "Lr": (103, "lawrencio"), "Rf": (104, "rutherfordio"), "Db": (105, "dubnio"),
    "Sg": (106, "seaborgio"), "Bh": (107, "bohrio"), "Hs": (108, "hasio"),
    "Mt": (109, "meitnerio"), "Ds": (110, "darmstadtio"), "Rg": (111, "roentgenio"),
    "Cn": (112, "copernicio"), "Nh": (113, "nihonio"), "Fl": (114, "flerovio"),
    "Mc": (115, "moscovio"), "Lv": (116, "livermorio"), "Ts": (117, "teneso"),
    "Og": (118, "oganesón"),
}

# Sinónimos de nombres de elemento (forma normalizada → símbolo).
_SINONIMOS = {"cinc": "Zn", "tungsteno": "W"}

# nombre normalizado → símbolo (para detección por nombre).
NOMBRE_A_SIMBOLO: Dict[str, str] = {
    normalizar(nombre): simbolo for simbolo, (_z, nombre) in ELEMENTOS.items()
}
NOMBRE_A_SIMBOLO.update(_SINONIMOS)


def es_simbolo(simbolo: str) -> bool:
    return simbolo in ELEMENTOS
