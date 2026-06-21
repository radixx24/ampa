"""Análisis de enlaces de una molécula: valencia y polaridad.

Para cada átomo calcula cuántos enlaces usa frente a su **valencia típica**
(saturación: libre / saturado / sobreenlazado). Para cada enlace estima su
**polaridad** por la diferencia de **electronegatividad** (covalente no polar /
covalente polar / iónico). Es orientativo y educativo, no un motor químico. Sin
dependencias externas.
"""
from __future__ import annotations

from typing import Dict, List

from .elements import ELEMENTOS
from .molecules import Molecula


def polaridad(delta: float) -> str:
    """Clasifica un enlace por la diferencia de electronegatividad (Pauling)."""
    if delta < 0.5:
        return "covalente no polar"
    if delta < 1.7:
        return "covalente polar"
    return "iónico"


def analizar_enlaces(mol: Molecula) -> Dict[str, object]:
    """Devuelve el análisis de valencia (por átomo) y polaridad (por enlace)."""
    usada = [0] * len(mol.atomos)
    for a, b, orden in mol.enlaces:
        usada[a] += orden
        usada[b] += orden

    atomos: List[Dict[str, object]] = []
    for i, simbolo in enumerate(mol.atomos):
        elem = ELEMENTOS.get(simbolo)
        tipica = elem.valencia if elem else 0
        if not tipica:
            estado = "n/d"
        elif usada[i] == tipica:
            estado = "saturado"
        elif usada[i] > tipica:
            estado = "sobreenlazado"
        else:
            estado = "libre"
        atomos.append({
            "i": i,
            "el": simbolo,
            "valencia_usada": usada[i],
            "valencia_tipica": tipica,
            "libres": max(0, tipica - usada[i]) if tipica else 0,
            "estado": estado,
        })

    enlaces: List[Dict[str, object]] = []
    for a, b, orden in mol.enlaces:
        ea = ELEMENTOS.get(mol.atomos[a])
        eb = ELEMENTOS.get(mol.atomos[b])
        if ea and eb and ea.electronegatividad and eb.electronegatividad:
            delta = round(abs(ea.electronegatividad - eb.electronegatividad), 2)
            pol = polaridad(delta)
        else:
            delta, pol = None, "n/d"
        enlaces.append({"a": a, "b": b, "orden": orden, "delta_en": delta, "polaridad": pol})

    estable = all(x["estado"] in ("saturado", "n/d") for x in atomos)
    return {"atomos": atomos, "enlaces": enlaces, "estable": estable}
