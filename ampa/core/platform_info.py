"""Detección de plataforma de forma portable (Windows, Linux, macOS).

Centralizar aquí la detección del sistema operativo evita esparcir condicionales
de SO por todo el código y facilita la portabilidad. Sin dependencias externas.
"""
from __future__ import annotations

import platform as _platform
import sys
from typing import Dict, Optional

# Nombres normalizados de sistema operativo que usa AMPA en todo el código.
WINDOWS = "windows"
LINUX = "linux"
MACOS = "macos"
UNKNOWN = "unknown"


def normalize_system(system: Optional[str] = None) -> str:
    """Normaliza el nombre del SO a uno de: ``windows``, ``linux``, ``macos``,
    ``unknown``.

    ``system`` permite **inyectar** el valor (útil en pruebas para simular otro
    SO sin estar en él). Si es ``None`` se detecta con ``platform.system()``.
    """
    raw = (system if system is not None else _platform.system()).strip().lower()
    if raw.startswith("win"):
        return WINDOWS
    if raw == "linux":
        return LINUX
    if raw in ("darwin", "macos"):
        return MACOS
    return UNKNOWN


def current_system() -> str:
    """Sistema operativo normalizado de la máquina actual."""
    return normalize_system()


def is_windows() -> bool:
    return current_system() == WINDOWS


def is_linux() -> bool:
    return current_system() == LINUX


def is_macos() -> bool:
    return current_system() == MACOS


def summary() -> Dict[str, str]:
    """Resumen portable del entorno de ejecución (para diagnóstico)."""
    return {
        "sistema": current_system(),
        "sistema_raw": _platform.system(),
        "version_so": _platform.version(),
        "arquitectura": _platform.machine(),
        "python": _platform.python_version(),
        "implementacion": _platform.python_implementation(),
        "ejecutable": sys.executable,
    }
