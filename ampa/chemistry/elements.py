"""Tabla periódica y utilidades de elementos (datos estáticos, sin dependencias).

`ELEMENTOS` mapea símbolo → :class:`Elemento` (número atómico, nombre, masa,
periodo, grupo y categoría). Es la base de datos para el reconocimiento químico y
para usos **visuales** (color por categoría, posición por grupo/periodo, tamaño
por masa).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

# Tabla de transliteración para normalizar nombres (sin acentos, minúsculas).
_TABLA = str.maketrans("áéíóúüñ", "aeiouun")


def normalizar(texto: str) -> str:
    """Minúsculas y sin acentos, preservando longitud (útil para spans)."""
    return texto.lower().translate(_TABLA)


@dataclass(frozen=True)
class Elemento:
    """Un elemento químico con datos listos para visualizar."""

    z: int
    simbolo: str
    nombre: str
    masa: float
    periodo: int
    grupo: int  # 1–18; 0 para lantánidos/actínidos del bloque f
    categoria: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "simbolo": self.simbolo,
            "numero_atomico": self.z,
            "nombre": self.nombre,
            "masa": self.masa,
            "periodo": self.periodo,
            "grupo": self.grupo,
            "categoria": self.categoria,
        }


# (Z, símbolo, nombre, masa, periodo, grupo, categoría)
_DATOS = [
    (1, "H", "hidrógeno", 1.008, 1, 1, "no metal"),
    (2, "He", "helio", 4.0026, 1, 18, "gas noble"),
    (3, "Li", "litio", 6.94, 2, 1, "alcalino"),
    (4, "Be", "berilio", 9.0122, 2, 2, "alcalinotérreo"),
    (5, "B", "boro", 10.81, 2, 13, "metaloide"),
    (6, "C", "carbono", 12.011, 2, 14, "no metal"),
    (7, "N", "nitrógeno", 14.007, 2, 15, "no metal"),
    (8, "O", "oxígeno", 15.999, 2, 16, "no metal"),
    (9, "F", "flúor", 18.998, 2, 17, "halógeno"),
    (10, "Ne", "neón", 20.180, 2, 18, "gas noble"),
    (11, "Na", "sodio", 22.990, 3, 1, "alcalino"),
    (12, "Mg", "magnesio", 24.305, 3, 2, "alcalinotérreo"),
    (13, "Al", "aluminio", 26.982, 3, 13, "post-transición"),
    (14, "Si", "silicio", 28.085, 3, 14, "metaloide"),
    (15, "P", "fósforo", 30.974, 3, 15, "no metal"),
    (16, "S", "azufre", 32.06, 3, 16, "no metal"),
    (17, "Cl", "cloro", 35.45, 3, 17, "halógeno"),
    (18, "Ar", "argón", 39.948, 3, 18, "gas noble"),
    (19, "K", "potasio", 39.098, 4, 1, "alcalino"),
    (20, "Ca", "calcio", 40.078, 4, 2, "alcalinotérreo"),
    (21, "Sc", "escandio", 44.956, 4, 3, "transición"),
    (22, "Ti", "titanio", 47.867, 4, 4, "transición"),
    (23, "V", "vanadio", 50.942, 4, 5, "transición"),
    (24, "Cr", "cromo", 51.996, 4, 6, "transición"),
    (25, "Mn", "manganeso", 54.938, 4, 7, "transición"),
    (26, "Fe", "hierro", 55.845, 4, 8, "transición"),
    (27, "Co", "cobalto", 58.933, 4, 9, "transición"),
    (28, "Ni", "níquel", 58.693, 4, 10, "transición"),
    (29, "Cu", "cobre", 63.546, 4, 11, "transición"),
    (30, "Zn", "zinc", 65.38, 4, 12, "transición"),
    (31, "Ga", "galio", 69.723, 4, 13, "post-transición"),
    (32, "Ge", "germanio", 72.630, 4, 14, "metaloide"),
    (33, "As", "arsénico", 74.922, 4, 15, "metaloide"),
    (34, "Se", "selenio", 78.971, 4, 16, "no metal"),
    (35, "Br", "bromo", 79.904, 4, 17, "halógeno"),
    (36, "Kr", "criptón", 83.798, 4, 18, "gas noble"),
    (37, "Rb", "rubidio", 85.468, 5, 1, "alcalino"),
    (38, "Sr", "estroncio", 87.62, 5, 2, "alcalinotérreo"),
    (39, "Y", "itrio", 88.906, 5, 3, "transición"),
    (40, "Zr", "circonio", 91.224, 5, 4, "transición"),
    (41, "Nb", "niobio", 92.906, 5, 5, "transición"),
    (42, "Mo", "molibdeno", 95.95, 5, 6, "transición"),
    (43, "Tc", "tecnecio", 98.0, 5, 7, "transición"),
    (44, "Ru", "rutenio", 101.07, 5, 8, "transición"),
    (45, "Rh", "rodio", 102.91, 5, 9, "transición"),
    (46, "Pd", "paladio", 106.42, 5, 10, "transición"),
    (47, "Ag", "plata", 107.87, 5, 11, "transición"),
    (48, "Cd", "cadmio", 112.41, 5, 12, "transición"),
    (49, "In", "indio", 114.82, 5, 13, "post-transición"),
    (50, "Sn", "estaño", 118.71, 5, 14, "post-transición"),
    (51, "Sb", "antimonio", 121.76, 5, 15, "metaloide"),
    (52, "Te", "telurio", 127.60, 5, 16, "metaloide"),
    (53, "I", "yodo", 126.90, 5, 17, "halógeno"),
    (54, "Xe", "xenón", 131.29, 5, 18, "gas noble"),
    (55, "Cs", "cesio", 132.91, 6, 1, "alcalino"),
    (56, "Ba", "bario", 137.33, 6, 2, "alcalinotérreo"),
    (57, "La", "lantano", 138.91, 6, 3, "lantánido"),
    (58, "Ce", "cerio", 140.12, 6, 0, "lantánido"),
    (59, "Pr", "praseodimio", 140.91, 6, 0, "lantánido"),
    (60, "Nd", "neodimio", 144.24, 6, 0, "lantánido"),
    (61, "Pm", "prometio", 145.0, 6, 0, "lantánido"),
    (62, "Sm", "samario", 150.36, 6, 0, "lantánido"),
    (63, "Eu", "europio", 151.96, 6, 0, "lantánido"),
    (64, "Gd", "gadolinio", 157.25, 6, 0, "lantánido"),
    (65, "Tb", "terbio", 158.93, 6, 0, "lantánido"),
    (66, "Dy", "disprosio", 162.50, 6, 0, "lantánido"),
    (67, "Ho", "holmio", 164.93, 6, 0, "lantánido"),
    (68, "Er", "erbio", 167.26, 6, 0, "lantánido"),
    (69, "Tm", "tulio", 168.93, 6, 0, "lantánido"),
    (70, "Yb", "iterbio", 173.05, 6, 0, "lantánido"),
    (71, "Lu", "lutecio", 174.97, 6, 0, "lantánido"),
    (72, "Hf", "hafnio", 178.49, 6, 4, "transición"),
    (73, "Ta", "tantalio", 180.95, 6, 5, "transición"),
    (74, "W", "wolframio", 183.84, 6, 6, "transición"),
    (75, "Re", "renio", 186.21, 6, 7, "transición"),
    (76, "Os", "osmio", 190.23, 6, 8, "transición"),
    (77, "Ir", "iridio", 192.22, 6, 9, "transición"),
    (78, "Pt", "platino", 195.08, 6, 10, "transición"),
    (79, "Au", "oro", 196.97, 6, 11, "transición"),
    (80, "Hg", "mercurio", 200.59, 6, 12, "transición"),
    (81, "Tl", "talio", 204.38, 6, 13, "post-transición"),
    (82, "Pb", "plomo", 207.2, 6, 14, "post-transición"),
    (83, "Bi", "bismuto", 208.98, 6, 15, "post-transición"),
    (84, "Po", "polonio", 209.0, 6, 16, "post-transición"),
    (85, "At", "astato", 210.0, 6, 17, "halógeno"),
    (86, "Rn", "radón", 222.0, 6, 18, "gas noble"),
    (87, "Fr", "francio", 223.0, 7, 1, "alcalino"),
    (88, "Ra", "radio", 226.0, 7, 2, "alcalinotérreo"),
    (89, "Ac", "actinio", 227.0, 7, 3, "actínido"),
    (90, "Th", "torio", 232.04, 7, 0, "actínido"),
    (91, "Pa", "protactinio", 231.04, 7, 0, "actínido"),
    (92, "U", "uranio", 238.03, 7, 0, "actínido"),
    (93, "Np", "neptunio", 237.0, 7, 0, "actínido"),
    (94, "Pu", "plutonio", 244.0, 7, 0, "actínido"),
    (95, "Am", "americio", 243.0, 7, 0, "actínido"),
    (96, "Cm", "curio", 247.0, 7, 0, "actínido"),
    (97, "Bk", "berkelio", 247.0, 7, 0, "actínido"),
    (98, "Cf", "californio", 251.0, 7, 0, "actínido"),
    (99, "Es", "einstenio", 252.0, 7, 0, "actínido"),
    (100, "Fm", "fermio", 257.0, 7, 0, "actínido"),
    (101, "Md", "mendelevio", 258.0, 7, 0, "actínido"),
    (102, "No", "nobelio", 259.0, 7, 0, "actínido"),
    (103, "Lr", "lawrencio", 266.0, 7, 0, "actínido"),
    (104, "Rf", "rutherfordio", 267.0, 7, 4, "transición"),
    (105, "Db", "dubnio", 268.0, 7, 5, "transición"),
    (106, "Sg", "seaborgio", 269.0, 7, 6, "transición"),
    (107, "Bh", "bohrio", 270.0, 7, 7, "transición"),
    (108, "Hs", "hasio", 269.0, 7, 8, "transición"),
    (109, "Mt", "meitnerio", 278.0, 7, 9, "transición"),
    (110, "Ds", "darmstadtio", 281.0, 7, 10, "transición"),
    (111, "Rg", "roentgenio", 282.0, 7, 11, "transición"),
    (112, "Cn", "copernicio", 285.0, 7, 12, "transición"),
    (113, "Nh", "nihonio", 286.0, 7, 13, "post-transición"),
    (114, "Fl", "flerovio", 289.0, 7, 14, "post-transición"),
    (115, "Mc", "moscovio", 290.0, 7, 15, "post-transición"),
    (116, "Lv", "livermorio", 293.0, 7, 16, "post-transición"),
    (117, "Ts", "teneso", 294.0, 7, 17, "halógeno"),
    (118, "Og", "oganesón", 294.0, 7, 18, "gas noble"),
]

# símbolo → Elemento
ELEMENTOS: Dict[str, Elemento] = {
    sim: Elemento(z, sim, nombre, masa, periodo, grupo, categoria)
    for (z, sim, nombre, masa, periodo, grupo, categoria) in _DATOS
}

# Sinónimos de nombres de elemento (forma normalizada → símbolo).
_SINONIMOS = {"cinc": "Zn", "tungsteno": "W"}

# nombre normalizado → símbolo (para detección por nombre).
NOMBRE_A_SIMBOLO: Dict[str, str] = {
    normalizar(elemento.nombre): simbolo for simbolo, elemento in ELEMENTOS.items()
}
NOMBRE_A_SIMBOLO.update(_SINONIMOS)


def es_simbolo(simbolo: str) -> bool:
    return simbolo in ELEMENTOS


def tabla() -> list:
    """Todos los elementos ordenados por número atómico."""
    return sorted(ELEMENTOS.values(), key=lambda e: e.z)
