"""Rutas portables de AMPA (Windows, Linux, macOS).

El **corazón de la portabilidad**. Todas las rutas se construyen con
``pathlib.Path``, nunca concatenando cadenas con ``/`` o ``\\``. La ubicación
base ("AMPA home") se resuelve según la convención de cada sistema operativo, y
siempre puede forzarse con la variable de entorno ``AMPA_HOME`` (máxima
portabilidad y reproducibilidad).

Sin dependencias externas: solo biblioteca estándar.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Mapping, Optional

from .platform_info import MACOS, WINDOWS, normalize_system

# Variable de entorno que, si existe, sobreescribe la ubicación base.
ENV_HOME = "AMPA_HOME"

# Nombre de la aplicación para las carpetas estándar del SO.
APP_NAME = "AMPA"


def _user_home(env: Mapping[str, str]) -> Path:
    """Carpeta del usuario de forma portable: ``HOME`` en Unix, ``USERPROFILE``
    en Windows. Si ninguna está definida, recurre a ``Path.home()``.
    """
    raw = env.get("HOME") or env.get("USERPROFILE")
    return Path(raw).expanduser() if raw else Path.home()


def resolve_home(
    system: Optional[str] = None,
    env: Optional[Mapping[str, str]] = None,
) -> Path:
    """Resuelve la carpeta base de AMPA de forma portable.

    Prioridad:

    1. Variable de entorno ``AMPA_HOME`` (si está definida): lo más portable y
       reproducible.
    2. Convención del sistema operativo:

       - Windows: ``%LOCALAPPDATA%\\AMPA`` (o ``%APPDATA%``, o el perfil del
         usuario como último respaldo).
       - macOS: ``~/Library/Application Support/AMPA``.
       - Linux y otros: ``$XDG_DATA_HOME/ampa`` (o ``~/.local/share/ampa``).

    ``system`` y ``env`` se pueden **inyectar** para pruebas: permiten simular
    otro SO sin estar en él. Por defecto se detectan del entorno real.
    """
    env = os.environ if env is None else env
    sys_name = normalize_system(system)

    # 1. Override explícito.
    override = env.get(ENV_HOME)
    if override:
        return Path(override).expanduser()

    home = _user_home(env)

    # 2. Convención por SO.
    if sys_name == WINDOWS:
        base = env.get("LOCALAPPDATA") or env.get("APPDATA")
        return (Path(base) / APP_NAME) if base else (home / APP_NAME)
    if sys_name == MACOS:
        return home / "Library" / "Application Support" / APP_NAME
    # Linux y cualquier otro: estándar XDG.
    xdg = env.get("XDG_DATA_HOME")
    return (Path(xdg) / "ampa") if xdg else (home / ".local" / "share" / "ampa")


@dataclass(frozen=True)
class Paths:
    """Conjunto de rutas estándar de AMPA, todas bajo la carpeta base ``home``.

    Es inmutable: las subcarpetas se derivan de ``home``, garantizando coherencia.
    """

    home: Path

    @property
    def data(self) -> Path:
        return self.home / "data"

    @property
    def models(self) -> Path:
        return self.home / "models"

    @property
    def config(self) -> Path:
        return self.home / "config"

    @property
    def cache(self) -> Path:
        return self.home / "cache"

    @property
    def backups(self) -> Path:
        return self.home / "backups"

    @property
    def logs(self) -> Path:
        return self.home / "logs"

    @property
    def memory(self) -> Path:
        return self.home / "memory"

    def all(self) -> List[Path]:
        """Todas las rutas gestionadas, empezando por ``home``."""
        return [
            self.home,
            self.data,
            self.models,
            self.config,
            self.cache,
            self.backups,
            self.logs,
            self.memory,
        ]

    def create(self) -> "Paths":
        """Crea todas las carpetas si no existen. Idempotente y portable."""
        for path in self.all():
            path.mkdir(parents=True, exist_ok=True)
        return self


def get_paths(
    system: Optional[str] = None,
    env: Optional[Mapping[str, str]] = None,
) -> Paths:
    """Construye el conjunto de rutas portables para el entorno dado."""
    return Paths(home=resolve_home(system=system, env=env))
