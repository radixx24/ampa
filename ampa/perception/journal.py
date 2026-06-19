"""Diario de eventos percibidos (journal): persistencia ligera y portable.

Registra en un archivo JSONL los eventos marcados para guardar
(`guardar_en_memoria`), completando el pendiente de «logs» de la Fase 2 y
formando el puente hacia la memoria documental (Fase 3). Solo biblioteca estándar.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from ..core.paths import get_paths
from .events import Evento

NOMBRE_ARCHIVO = "eventos.jsonl"


def ruta_diario(ruta: Optional[Path] = None) -> Path:
    """Ruta del diario. Por defecto, bajo la carpeta de logs portable."""
    if ruta is not None:
        return ruta
    return get_paths().logs / NOMBRE_ARCHIVO


def registrar(
    evento: Evento,
    ruta: Optional[Path] = None,
    *,
    forzar: bool = False,
) -> bool:
    """Anexa el evento al diario si debe guardarse.

    Respeta ``evento.guardar_en_memoria`` salvo que ``forzar=True``. Devuelve
    ``True`` si se registró, ``False`` si se omitió por política de memoria.
    """
    if not (evento.guardar_en_memoria or forzar):
        return False
    destino = ruta_diario(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    registro = evento.to_dict()
    registro["timestamp"] = datetime.now(timezone.utc).isoformat()
    with destino.open("a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
    return True


def leer(ruta: Optional[Path] = None) -> List[dict]:
    """Lee todos los registros del diario. Lista vacía si aún no existe."""
    destino = ruta_diario(ruta)
    if not destino.exists():
        return []
    registros: List[dict] = []
    with destino.open("r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                registros.append(json.loads(linea))
    return registros
