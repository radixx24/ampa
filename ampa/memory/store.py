"""Persistencia portable de la memoria documental (JSONL).

Guarda y carga :class:`Fragmento` bajo la carpeta de memoria portable
(``Paths.memory``). Solo biblioteca estándar.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from ..core.paths import get_paths
from .documents import Fragmento

NOMBRE_ARCHIVO = "fragmentos.jsonl"


def ruta_memoria(ruta: Optional[Path] = None) -> Path:
    if ruta is not None:
        return ruta
    return get_paths().memory / NOMBRE_ARCHIVO


def guardar_fragmentos(
    fragmentos: List[Fragmento], ruta: Optional[Path] = None
) -> Path:
    destino = ruta_memoria(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("a", encoding="utf-8") as archivo:
        for fragmento in fragmentos:
            archivo.write(json.dumps(fragmento.to_dict(), ensure_ascii=False) + "\n")
    return destino


def cargar_fragmentos(ruta: Optional[Path] = None) -> List[Fragmento]:
    destino = ruta_memoria(ruta)
    if not destino.exists():
        return []
    fragmentos: List[Fragmento] = []
    with destino.open("r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                fragmentos.append(Fragmento.from_dict(json.loads(linea)))
    return fragmentos


def reiniciar(ruta: Optional[Path] = None) -> None:
    """Vacía la memoria (elimina el archivo de fragmentos)."""
    destino = ruta_memoria(ruta)
    if destino.exists():
        destino.unlink()


def fuentes(ruta: Optional[Path] = None) -> List[str]:
    """Lista ordenada de fuentes distintas presentes en la memoria."""
    return sorted({fragmento.fuente for fragmento in cargar_fragmentos(ruta)})
