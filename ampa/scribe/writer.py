"""Escritura segura y portable de archivos (Escriba, Fase 5).

Principios de diseño:

- **Respaldo previo**: antes de sobrescribir un archivo existente, se copia a la
  carpeta de respaldos portable (``Paths.backups``) con marca de tiempo.
- **Modo simulación**: ``simular=True`` describe lo que haría sin tocar el disco.
- **Bloqueo por riesgo**: si el ``riesgo_operativo`` es ``alto`` (la señal que
  emite la percepción), se rechaza la escritura salvo ``forzar=True``
  (autorización explícita).
- **Escritura atómica**: se escribe en un archivo temporal de la misma carpeta y
  se reemplaza con ``os.replace``, evitando archivos a medias ante fallos.

Solo biblioteca estándar: corre igual en Windows, Linux y macOS.
"""
from __future__ import annotations

import os
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union

from ..core.paths import Paths, get_paths
from ..perception.events import ALTO

SUFIJO_RESPALDO = ".bak"

RutaLike = Union[str, "os.PathLike[str]"]


@dataclass
class ResultadoEscritura:
    """Resultado de una operación de escritura segura (auditable)."""

    ruta: Path
    escrito: bool = False
    simulado: bool = False
    bloqueado: bool = False
    respaldo: Optional[Path] = None
    bytes_escritos: int = 0
    motivo: str = ""

    def resumen(self) -> str:
        """Línea legible para la CLI y los logs."""
        if self.bloqueado:
            return f"BLOQUEADO {self.ruta}: {self.motivo}"
        if self.simulado:
            extra = f" (respaldaría → {self.respaldo.name})" if self.respaldo else ""
            return f"SIMULADO {self.ruta}: {self.motivo}{extra}"
        if self.escrito:
            extra = f"; respaldo → {self.respaldo}" if self.respaldo else ""
            return f"ESCRITO {self.ruta} ({self.bytes_escritos} bytes){extra}"
        return f"SIN CAMBIOS {self.ruta}: {self.motivo}"


def _marca_tiempo() -> str:
    return datetime.now().strftime("%Y%m%dT%H%M%S_%f")


def _nombre_respaldo(ruta: Path, marca: Optional[str] = None) -> str:
    return f"{ruta.name}.{marca or _marca_tiempo()}{SUFIJO_RESPALDO}"


def _carpeta_respaldos(paths: Optional[Paths]) -> Path:
    return (paths or get_paths()).backups


def _ruta_respaldo_unica(carpeta: Path, ruta: Path) -> Path:
    """Ruta de respaldo garantizada única (evita colisiones de marca de tiempo)."""
    marca = _marca_tiempo()
    candidato = carpeta / _nombre_respaldo(ruta, marca)
    contador = 1
    while candidato.exists():
        candidato = carpeta / f"{ruta.name}.{marca}_{contador}{SUFIJO_RESPALDO}"
        contador += 1
    return candidato


def escribir(
    ruta: RutaLike,
    contenido: str,
    *,
    riesgo: str = "bajo",
    simular: bool = False,
    forzar: bool = False,
    respaldar: bool = True,
    codificacion: str = "utf-8",
    paths: Optional[Paths] = None,
) -> ResultadoEscritura:
    """Escribe ``contenido`` en ``ruta`` de forma segura, atómica y portable.

    Devuelve un :class:`ResultadoEscritura` que describe lo ocurrido (escrito,
    simulado o bloqueado), apto para auditoría.
    """
    ruta = Path(ruta)
    datos = contenido.encode(codificacion)
    existe = ruta.exists()

    # 1. Bloqueo por riesgo alto (señal emitida por la percepción).
    if riesgo == ALTO and not forzar:
        return ResultadoEscritura(
            ruta=ruta,
            bloqueado=True,
            motivo="riesgo_operativo alto; usa --forzar para autorizar.",
        )

    carpeta_resp = _carpeta_respaldos(paths)

    # 2. Simulación: no toca el disco, solo describe.
    if simular:
        respaldo_previsto = (
            carpeta_resp / _nombre_respaldo(ruta) if (existe and respaldar) else None
        )
        accion = "sobrescribiría" if existe else "crearía"
        return ResultadoEscritura(
            ruta=ruta,
            simulado=True,
            respaldo=respaldo_previsto,
            bytes_escritos=len(datos),
            motivo=f"{accion} {len(datos)} bytes.",
        )

    # 3. Respaldo previo (solo si el archivo ya existe).
    respaldo_real: Optional[Path] = None
    if existe and respaldar:
        carpeta_resp.mkdir(parents=True, exist_ok=True)
        respaldo_real = _ruta_respaldo_unica(carpeta_resp, ruta)
        shutil.copy2(ruta, respaldo_real)

    # 4. Escritura atómica: temporal en la misma carpeta + os.replace.
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(ruta.parent), prefix=".ampa-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(datos)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, ruta)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise

    accion = "sobrescrito" if existe else "creado"
    return ResultadoEscritura(
        ruta=ruta,
        escrito=True,
        respaldo=respaldo_real,
        bytes_escritos=len(datos),
        motivo=f"{accion}.",
    )


def respaldos_de(nombre: RutaLike, paths: Optional[Paths] = None) -> List[Path]:
    """Respaldos de un archivo (por nombre), del más reciente al más antiguo."""
    nombre = Path(nombre).name
    carpeta = _carpeta_respaldos(paths)
    if not carpeta.exists():
        return []
    return sorted(carpeta.glob(f"{nombre}.*{SUFIJO_RESPALDO}"), reverse=True)


def restaurar(
    ruta: RutaLike,
    respaldo: Optional[RutaLike] = None,
    *,
    paths: Optional[Paths] = None,
) -> ResultadoEscritura:
    """Restaura ``ruta`` desde un respaldo (el más reciente si no se indica)."""
    ruta = Path(ruta)
    if respaldo is None:
        candidatos = respaldos_de(ruta.name, paths)
        if not candidatos:
            return ResultadoEscritura(ruta=ruta, motivo="no hay respaldos disponibles.")
        respaldo = candidatos[0]
    respaldo = Path(respaldo)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(respaldo, ruta)
    return ResultadoEscritura(
        ruta=ruta,
        escrito=True,
        respaldo=respaldo,
        bytes_escritos=respaldo.stat().st_size,
        motivo=f"restaurado desde {respaldo.name}.",
    )
