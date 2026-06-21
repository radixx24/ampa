"""Detección de grupos funcionales sobre el grafo de enlaces de una molécula.

Recorre los enlaces (con su orden) para identificar grupos orgánicos comunes:
alcohol, éter, aldehído, cetona, ácido carboxílico, éster, amida, amina, nitrilo,
alqueno, alquino y halogenuro. Sin dependencias externas.
"""
from __future__ import annotations

from typing import List, Tuple

from .molecules import Molecula

_HALOGENOS = {"F", "Cl", "Br", "I"}


def _adyacencia(mol: Molecula) -> List[List[Tuple[int, int]]]:
    ady: List[List[Tuple[int, int]]] = [[] for _ in mol.atomos]
    for a, b, orden in mol.enlaces:
        ady[a].append((b, orden))
        ady[b].append((a, orden))
    return ady


def _agregar(grupos: List[str], nombre: str) -> None:
    if nombre not in grupos:
        grupos.append(nombre)


def grupos_funcionales(mol: Molecula) -> List[str]:
    """Lista de grupos funcionales presentes en ``mol`` (sin repetir)."""
    sym = mol.atomos
    ady = _adyacencia(mol)
    grupos: List[str] = []
    consumidos: set = set()

    # Carbonilo y derivados (prioridad: ácido, éster, amida, aldehído, cetona).
    for c in range(len(sym)):
        if sym[c] != "C":
            continue
        dobles_o = [j for j, o in ady[c] if sym[j] == "O" and o == 2]
        if not dobles_o:
            continue
        odob = dobles_o[0]
        simples_o = [j for j, o in ady[c] if sym[j] == "O" and o == 1]
        n_vec = [j for j, o in ady[c] if sym[j] == "N"]
        h_vec = [j for j, o in ady[c] if sym[j] == "H"]
        c_vec = [j for j, o in ady[c] if sym[j] == "C"]
        oh = next((j for j in simples_o if any(sym[k] == "H" for k, _ in ady[j])), None)
        if oh is not None:
            _agregar(grupos, "ácido carboxílico")
            consumidos.update({c, odob, oh})
            continue
        oc = next(
            (j for j in simples_o if any(sym[k] == "C" and k != c for k, _ in ady[j])),
            None,
        )
        if oc is not None:
            _agregar(grupos, "éster")
            consumidos.update({c, odob, oc})
            continue
        if n_vec:
            _agregar(grupos, "amida")
            consumidos.update({c, odob, n_vec[0]})
            continue
        if h_vec:
            _agregar(grupos, "aldehído")
            consumidos.update({c, odob})
            continue
        if len(c_vec) >= 2:
            _agregar(grupos, "cetona")
            consumidos.update({c, odob})
            continue
        _agregar(grupos, "carbonilo")
        consumidos.update({c, odob})

    # Alcohol / éter (oxígenos con enlaces simples, no consumidos).
    for o in range(len(sym)):
        if sym[o] != "O" or o in consumidos:
            continue
        if any(orden != 1 for _, orden in ady[o]):
            continue
        h_n = [j for j, _ in ady[o] if sym[j] == "H"]
        c_n = [j for j, _ in ady[o] if sym[j] == "C"]
        if h_n and c_n:
            _agregar(grupos, "alcohol")
        elif len(c_n) >= 2:
            _agregar(grupos, "éter")

    # Amina (N con enlaces simples, H y C, no consumida en una amida).
    for n in range(len(sym)):
        if sym[n] != "N" or n in consumidos:
            continue
        if all(orden == 1 for _, orden in ady[n]):
            h_n = [j for j, _ in ady[n] if sym[j] == "H"]
            c_n = [j for j, _ in ady[n] if sym[j] == "C"]
            if h_n and c_n:
                _agregar(grupos, "amina")

    # Enlaces múltiples y halogenuros.
    for a, b, orden in mol.enlaces:
        par = {sym[a], sym[b]}
        if orden == 3 and par == {"C", "N"}:
            _agregar(grupos, "nitrilo")
        elif orden == 2 and par == {"C"}:
            _agregar(grupos, "alqueno")
        elif orden == 3 and par == {"C"}:
            _agregar(grupos, "alquino")
        if "C" in par and (par & _HALOGENOS):
            _agregar(grupos, "halogenuro")

    return grupos
