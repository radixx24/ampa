"""Cuaderno y diccionario personal de filosofía (persistente y portable).

El usuario va escribiendo sus **pensamientos**; AMPA los **conserva** y construye
un **diccionario** que agrupa esos pensamientos por los términos a los que aluden
(detectados automáticamente o indicados a mano). Es la parte **adaptativa**: el
diccionario crece con lo que tú pones. Solo biblioteca estándar.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ..core.paths import get_paths
from .data import normalizar
from .recognizer import identificar

NOMBRE_ARCHIVO = "pensamientos.jsonl"


@dataclass
class Pensamiento:
    """Una entrada del cuaderno: el texto del usuario y sus términos."""

    texto: str
    terminos: List[str] = field(default_factory=list)
    timestamp: str = ""

    def to_dict(self) -> Dict[str, object]:
        return {
            "texto": self.texto,
            "terminos": list(self.terminos),
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, datos: Dict[str, object]) -> "Pensamiento":
        return cls(
            texto=str(datos["texto"]),
            terminos=[str(t) for t in datos.get("terminos", [])],
            timestamp=str(datos.get("timestamp", "")),
        )


def ruta_cuaderno(ruta: Optional[Path] = None) -> Path:
    if ruta is not None:
        return ruta
    return get_paths().data / NOMBRE_ARCHIVO


def _terminos_auto(texto: str) -> List[str]:
    """Términos detectados automáticamente (conceptos, filósofos, corrientes)."""
    resultado = identificar(texto)
    return [e.nombre for e in resultado.entidades]


def _limpiar(terminos: List[str]) -> List[str]:
    limpios: List[str] = []
    for termino in terminos:
        termino = termino.strip()
        if termino and termino not in limpios:
            limpios.append(termino)
    return limpios


def agregar(
    texto: str,
    terminos: Optional[List[str]] = None,
    ruta: Optional[Path] = None,
) -> Pensamiento:
    """Añade un pensamiento al cuaderno y lo devuelve.

    Si no se indican ``terminos``, se detectan automáticamente con el reconocedor
    de filosofía.
    """
    texto = texto.strip()
    if terminos is None:
        terminos = _terminos_auto(texto)
    pensamiento = Pensamiento(
        texto=texto,
        terminos=_limpiar(terminos),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    destino = ruta_cuaderno(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(pensamiento.to_dict(), ensure_ascii=False) + "\n")
    return pensamiento


def leer(ruta: Optional[Path] = None) -> List[Pensamiento]:
    destino = ruta_cuaderno(ruta)
    if not destino.exists():
        return []
    pensamientos: List[Pensamiento] = []
    with destino.open("r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                pensamientos.append(Pensamiento.from_dict(json.loads(linea)))
    return pensamientos


def diccionario(ruta: Optional[Path] = None) -> Dict[str, List[Pensamiento]]:
    """Diccionario término → pensamientos. Agrupa sin distinguir mayúsculas/acentos."""
    grupos: Dict[str, List[Pensamiento]] = {}
    display: Dict[str, str] = {}
    for pensamiento in leer(ruta):
        for termino in pensamiento.terminos:
            clave = normalizar(termino)
            display.setdefault(clave, termino)
            grupos.setdefault(clave, []).append(pensamiento)
    return {display[clave]: lista for clave, lista in grupos.items()}


def terminos(ruta: Optional[Path] = None) -> List[Tuple[str, int]]:
    """Términos del diccionario con su número de entradas (más frecuentes primero)."""
    return sorted(
        ((termino, len(lista)) for termino, lista in diccionario(ruta).items()),
        key=lambda par: (-par[1], par[0]),
    )
