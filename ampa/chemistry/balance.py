"""Balanceo general de ecuaciones químicas (álgebra lineal, sin dependencias).

Dada una lista de **reactivos** y **productos** (fórmulas), encuentra los
coeficientes enteros más pequeños que **conservan cada elemento**. No se limita a
la combustión: resuelve el sistema de conservación como el **espacio nulo** de la
matriz de conteos atómicos, con aritmética exacta (`fractions.Fraction`).

Conservación de la materia: para cada elemento, ``Σ coef·átomos`` en reactivos =
``Σ coef·átomos`` en productos. Con los reactivos en positivo y los productos en
negativo, eso es ``M · x = 0``; el vector ``x`` (los coeficientes) vive en el
núcleo de ``M``. Si ese núcleo tiene **dimensión 1**, la ecuación se balancea de
forma única (salvo un factor); si no, es ambigua o imposible y se reporta así.
"""
from __future__ import annotations

import functools
from fractions import Fraction
from math import gcd
from typing import List, Optional, Sequence, Tuple

from .formulas import composicion_valida

Coeficientes = Tuple[List[int], List[int]]  # (reactivos, productos)


def _nucleo(matriz: List[List[Fraction]]) -> Optional[List[Fraction]]:
    """Un vector base del espacio nulo si su dimensión es exactamente 1.

    Reduce la matriz a su forma escalonada reducida (RREF) y, si hay una sola
    variable libre, devuelve la solución no trivial; en otro caso ``None``
    (sistema sin solución útil o con más de un grado de libertad → ambiguo).
    """
    filas = [fila[:] for fila in matriz]
    n_filas = len(filas)
    n_cols = len(filas[0]) if filas else 0
    pivotes: List[int] = []
    r = 0
    for c in range(n_cols):
        piv = next((i for i in range(r, n_filas) if filas[i][c] != 0), None)
        if piv is None:
            continue
        filas[r], filas[piv] = filas[piv], filas[r]
        cabeza = filas[r][c]
        filas[r] = [x / cabeza for x in filas[r]]
        for i in range(n_filas):
            if i != r and filas[i][c] != 0:
                factor = filas[i][c]
                filas[i] = [a - factor * b for a, b in zip(filas[i], filas[r])]
        pivotes.append(c)
        r += 1
        if r == n_filas:
            break
    libres = [c for c in range(n_cols) if c not in pivotes]
    if len(libres) != 1:
        return None  # 0 → solo solución trivial; >1 → ambiguo
    libre = libres[0]
    x = [Fraction(0)] * n_cols
    x[libre] = Fraction(1)
    for fila_i, col_piv in enumerate(pivotes):
        x[col_piv] = -filas[fila_i][libre]
    return x


def _a_enteros(x: Sequence[Fraction]) -> List[int]:
    """Escala un vector racional a los enteros más pequeños (signo preservado)."""
    com = functools.reduce(lambda a, b: a * b // gcd(a, b), [v.denominator for v in x], 1)
    enteros = [int(v * com) for v in x]
    divisor = functools.reduce(gcd, [abs(e) for e in enteros], 0)
    if divisor == 0:
        return enteros
    return [e // divisor for e in enteros]


def balancear(
    reactivos: Sequence[str], productos: Sequence[str]
) -> Optional[Coeficientes]:
    """Coeficientes enteros que balancean ``reactivos → productos``.

    Devuelve ``([c_react…], [c_prod…])`` con todos los coeficientes positivos, o
    ``None`` si alguna fórmula es inválida, si no hay solución, o si el balanceo
    no es único (p. ej. faltan especies o sobran grados de libertad).
    """
    especies = list(reactivos) + list(productos)
    if len(especies) < 2:
        return None
    comps = []
    for formula in especies:
        comp = composicion_valida(formula)
        if comp is None:
            return None
        comps.append(comp)
    elementos = sorted({el for comp in comps for el in comp})

    matriz: List[List[Fraction]] = []
    for el in elementos:
        fila: List[Fraction] = []
        for j, comp in enumerate(comps):
            signo = 1 if j < len(reactivos) else -1
            fila.append(Fraction(signo * comp.get(el, 0)))
        matriz.append(fila)

    x = _nucleo(matriz)
    if x is None:
        return None
    enteros = _a_enteros(x)
    if any(e == 0 for e in enteros):
        return None
    if enteros[0] < 0:
        enteros = [-e for e in enteros]
    if any(e < 0 for e in enteros):  # signos mezclados → el reparto no balancea
        return None
    corte = len(reactivos)
    return enteros[:corte], enteros[corte:]


def _lado(coefs: Sequence[int], formulas: Sequence[str]) -> str:
    partes = [(f"{c} " if c != 1 else "") + f for c, f in zip(coefs, formulas)]
    return " + ".join(partes)


def ecuacion(
    reactivos: Sequence[str], productos: Sequence[str], coefs: Coeficientes
) -> str:
    """Arma la cadena ``a A + b B → c C + d D`` a partir de los coeficientes."""
    cr, cp = coefs
    return f"{_lado(cr, reactivos)} → {_lado(cp, productos)}"
