"""Análisis de fórmulas químicas: parseo y validación (sin dependencias).

Convierte una fórmula (``H2O``, ``CO2``, ``Ca(OH)2``) en su composición
(elemento → número de átomos), soportando paréntesis y multiplicadores.
"""
from __future__ import annotations

import re
from collections import defaultdict
from typing import Dict, Optional

from .elements import ELEMENTOS

_TOKEN = re.compile(r"[A-Z][a-z]?|\d+|\(|\)")


def parsear_formula(formula: str) -> Dict[str, int]:
    """Devuelve la composición de ``formula`` (elemento → átomos).

    Lanza ``ValueError`` si la cadena no es una fórmula bien formada (no valida
    que los símbolos sean elementos reales: para eso, :func:`composicion_valida`).
    """
    tokens = _TOKEN.findall(formula)
    if "".join(tokens) != formula:
        raise ValueError(f"Fórmula no reconocible: {formula!r}")
    pila = [defaultdict(int)]
    i, n = 0, len(tokens)
    while i < n:
        token = tokens[i]
        if token == "(":
            pila.append(defaultdict(int))
            i += 1
        elif token == ")":
            i += 1
            mult = 1
            if i < n and tokens[i].isdigit():
                mult = int(tokens[i])
                i += 1
            if len(pila) < 2:
                raise ValueError("paréntesis desbalanceados")
            grupo = pila.pop()
            for elemento, cuenta in grupo.items():
                pila[-1][elemento] += cuenta * mult
        elif token[0].isalpha():
            elemento = token
            i += 1
            cuenta = 1
            if i < n and tokens[i].isdigit():
                cuenta = int(tokens[i])
                i += 1
            pila[-1][elemento] += cuenta
        else:  # un dígito suelto al inicio de un grupo no es válido
            raise ValueError(f"token inesperado: {token!r}")
    if len(pila) != 1:
        raise ValueError("paréntesis desbalanceados")
    return dict(pila[0])


def composicion_valida(formula: str) -> Optional[Dict[str, int]]:
    """Composición si ``formula`` es válida y todos sus símbolos son elementos
    reales; ``None`` en caso contrario."""
    try:
        composicion = parsear_formula(formula)
    except ValueError:
        return None
    if not composicion or any(sim not in ELEMENTOS for sim in composicion):
        return None
    return composicion
