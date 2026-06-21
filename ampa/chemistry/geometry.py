"""Geometría 3D aproximada de una molécula (layout dirigido por fuerzas).

Genera coordenadas 3D para **visualizar** una molécula a partir de su grafo: los
átomos se **repelen** (tipo Coulomb) y los enlaces actúan como **resortes**. Es
determinista (semilla fija) y sin dependencias. No es geometría química exacta (no
modela ángulos de enlace), pero da una disposición 3D clara para el visor.
"""
from __future__ import annotations

import math
import random
from typing import Dict, List

from .molecules import Molecula

_LONGITUD = 1.5  # longitud de reposo de un enlace
_REPULSION = 2.0
_PASO = 0.1


def geometria_3d(
    mol: Molecula, iteraciones: int = 200, semilla: int = 7
) -> List[Dict[str, object]]:
    """Coordenadas 3D por átomo: ``[{"el", "x", "y", "z"}, ...]`` (centradas)."""
    n = len(mol.atomos)
    if n == 0:
        return []
    rnd = random.Random(semilla)
    pos = [[rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)] for _ in range(n)]

    for _ in range(iteraciones):
        fuerza = [[0.0, 0.0, 0.0] for _ in range(n)]
        # Repulsión entre todos los pares.
        for i in range(n):
            for j in range(i + 1, n):
                dx = pos[i][0] - pos[j][0]
                dy = pos[i][1] - pos[j][1]
                dz = pos[i][2] - pos[j][2]
                d2 = dx * dx + dy * dy + dz * dz + 0.01
                d = math.sqrt(d2)
                f = _REPULSION / d2
                ux, uy, uz = dx / d, dy / d, dz / d
                fuerza[i][0] += f * ux
                fuerza[i][1] += f * uy
                fuerza[i][2] += f * uz
                fuerza[j][0] -= f * ux
                fuerza[j][1] -= f * uy
                fuerza[j][2] -= f * uz
        # Resortes en los enlaces.
        for a, b, _orden in mol.enlaces:
            dx = pos[b][0] - pos[a][0]
            dy = pos[b][1] - pos[a][1]
            dz = pos[b][2] - pos[a][2]
            d = math.sqrt(dx * dx + dy * dy + dz * dz) + 1e-6
            f = (d - _LONGITUD) * 0.5
            ux, uy, uz = dx / d, dy / d, dz / d
            fuerza[a][0] += f * ux
            fuerza[a][1] += f * uy
            fuerza[a][2] += f * uz
            fuerza[b][0] -= f * ux
            fuerza[b][1] -= f * uy
            fuerza[b][2] -= f * uz
        for i in range(n):
            pos[i][0] += fuerza[i][0] * _PASO
            pos[i][1] += fuerza[i][1] * _PASO
            pos[i][2] += fuerza[i][2] * _PASO

    cx = sum(p[0] for p in pos) / n
    cy = sum(p[1] for p in pos) / n
    cz = sum(p[2] for p in pos) / n
    return [
        {
            "el": mol.atomos[i],
            "x": round(pos[i][0] - cx, 3),
            "y": round(pos[i][1] - cy, 3),
            "z": round(pos[i][2] - cz, 3),
        }
        for i in range(n)
    ]
