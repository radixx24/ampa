"""Ciclo percepción → memoria → acción (Concepto Maestro §6).

Orquesta las tres capas en un solo flujo: **percibe** una entrada, **recupera**
contexto de la memoria y **propone** (o ejecuta) una escritura segura, gobernada
por la puerta de riesgo del escriba.

Por defecto solo **propone** (simulación, sin persistir nada). Con
``ejecutar=True`` **recuerda** la observación (diario y, según la política de
memoria, la memoria documental) y **escribe** la nota con respaldo previo,
respetando la puerta de riesgo. Sin dependencias externas.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from ..core.paths import Paths, get_paths
from ..memory import Resultado, ingerir, recuperar
from ..memory import store as memory_store
from ..perception import journal, perceive
from ..perception.events import Evento
from ..scribe import writer as scribe
from ..scribe.writer import ResultadoEscritura


def _extracto(texto: str, limite: int = 100) -> str:
    plano = " ".join(texto.split())
    return plano if len(plano) <= limite else plano[: limite - 1] + "…"


def _componer_nota(entrada: str, evento: Evento, contexto: List[Resultado]) -> str:
    """Compone la nota a registrar: observación + metadatos + contexto citado."""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    lineas = [
        f"## {fecha} — {evento.dominio_probable} "
        f"({evento.tipo}, riesgo {evento.riesgo_operativo})",
        "",
        entrada.strip(),
    ]
    if contexto:
        lineas += ["", "Contexto relacionado en memoria:"]
        for resultado in contexto:
            lineas.append(
                f"- {resultado.cita()} «{_extracto(resultado.fragmento.texto)}»"
            )
    else:
        lineas += ["", "Contexto relacionado en memoria: (ninguno)."]
    return "\n".join(lineas) + "\n"


@dataclass
class ResultadoCiclo:
    """Traza auditable de un ciclo: las tres etapas y su resultado."""

    entrada: str
    evento: Evento
    contexto: List[Resultado]
    nota: str
    destino: Path
    escritura: ResultadoEscritura
    registrado: bool = False
    ingeridos: int = 0

    def resumen(self) -> str:
        lineas = [
            "● Percepción:",
            f"    dominio={self.evento.dominio_probable}"
            f" · tipo={self.evento.tipo}"
            f" · riesgo={self.evento.riesgo_operativo}",
            "● Memoria:",
        ]
        if self.contexto:
            for resultado in self.contexto:
                lineas.append(f"    - {resultado.cita()} (score {resultado.score})")
        else:
            lineas.append("    (sin contexto relacionado)")
        if self.registrado or self.ingeridos:
            lineas.append(
                f"    recordado: diario={'sí' if self.registrado else 'no'}"
                f" · +{self.ingeridos} a memoria"
            )
        lineas += ["● Acción:", f"    {self.escritura.resumen()}"]
        return "\n".join(lineas)


def ciclo(
    entrada: str,
    *,
    destino: Optional[Path] = None,
    k: int = 3,
    ejecutar: bool = False,
    forzar: bool = False,
    registrar: bool = True,
    ruta_memoria: Optional[Path] = None,
    paths: Optional[Paths] = None,
) -> ResultadoCiclo:
    """Ejecuta el ciclo percepción → memoria → acción sobre ``entrada``."""
    paths = paths or get_paths()
    destino = Path(destino) if destino is not None else (paths.data / "bitacora.md")
    ruta_mem = (
        ruta_memoria
        if ruta_memoria is not None
        else (paths.memory / memory_store.NOMBRE_ARCHIVO)
    )

    # 1. Percepción.
    evento = perceive(entrada)
    # 2. Memoria: contexto previo (antes de recordar la entrada actual).
    contexto = recuperar(entrada, k, ruta=ruta_mem)

    registrado = False
    ingeridos = 0
    if ejecutar and registrar:
        registrado = journal.registrar(evento, paths.logs / journal.NOMBRE_ARCHIVO)
        if evento.guardar_en_memoria:
            ingeridos = len(ingerir(texto=entrada, fuente="ciclo", ruta=ruta_mem))

    # 3. Acción: componer la nota y escribir (o simular) con la puerta de riesgo.
    nota = _componer_nota(entrada, evento, contexto)
    existente = destino.read_text(encoding="utf-8") if destino.exists() else ""
    contenido = f"{existente}\n{nota}" if existente else nota
    escritura = scribe.escribir(
        destino,
        contenido,
        riesgo=evento.riesgo_operativo,
        simular=not ejecutar,
        forzar=forzar,
        paths=paths,
    )

    return ResultadoCiclo(
        entrada=entrada,
        evento=evento,
        contexto=contexto,
        nota=nota,
        destino=destino,
        escritura=escritura,
        registrado=registrado,
        ingeridos=ingeridos,
    )
