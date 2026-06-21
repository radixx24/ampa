"""Respuesta con fuentes: percepción + recuperación de memoria (Fase 4).

Compone una respuesta **extractiva y citada** a partir de los apuntes: percibe la
consulta (dominio, riesgo), recupera los fragmentos más relevantes (BM25) y los
presenta con sus citas. La **generación con modelo** llegará como capa posterior
sobre estos mismos fragmentos (ADR 0011). Sin dependencias externas.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from ..memory import Resultado, recuperar
from ..perception import perceive
from ..perception.events import Evento


def _una_linea(texto: str, limite: int = 220) -> str:
    plano = " ".join(texto.split())
    return plano if len(plano) <= limite else plano[: limite - 1] + "…"


@dataclass
class Respuesta:
    """Respuesta citada a una consulta, construida por recuperación."""

    consulta: str
    evento: Evento
    resultados: List[Resultado]

    @property
    def dominio(self) -> str:
        return self.evento.dominio_probable

    @property
    def riesgo(self) -> str:
        return self.evento.riesgo_operativo

    def hay_evidencia(self) -> bool:
        return bool(self.resultados)

    def fuentes(self) -> List[str]:
        """Citas distintas que respaldan la respuesta, en orden de relevancia."""
        vistas: List[str] = []
        for resultado in self.resultados:
            cita = resultado.cita()
            if cita not in vistas:
                vistas.append(cita)
        return vistas

    def texto(self) -> str:
        """Respuesta legible y honesta, con citas literales."""
        if not self.resultados:
            return (
                f"No encuentro nada en la memoria sobre «{self.consulta}» "
                f"(dominio probable: {self.dominio}).\n"
                "No invento la respuesta: por ahora solo recupero de tus apuntes, "
                "aún sin generación con modelo."
            )
        principal = self.resultados[0]
        lineas = [
            f"Según tu memoria (dominio: {self.dominio}):",
            "",
            f"  «{_una_linea(principal.fragmento.texto)}» {principal.cita()}",
        ]
        if len(self.resultados) > 1:
            lineas += ["", "Otras fuentes relacionadas:"]
            for resultado in self.resultados[1:]:
                lineas.append(
                    f"  - {resultado.cita()} ({resultado.fragmento.dominio})"
                    f" · score {resultado.score}"
                )
        lineas += [
            "",
            "— Respuesta por recuperación: citas literales de tus apuntes, sin "
            "generación de lenguaje todavía.",
        ]
        return "\n".join(lineas)

    def diagnostico(self) -> str:
        """Detalle para depurar: el evento percibido y los scores recuperados."""
        lineas = [
            self.evento.as_yaml().rstrip("\n"),
            f"fragmentos recuperados: {len(self.resultados)}",
        ]
        for n, resultado in enumerate(self.resultados, 1):
            lineas.append(
                f"  {n}. {resultado.cita()} · score {resultado.score}"
                f" ({resultado.fragmento.dominio})"
            )
        return "\n".join(lineas)


def responder(
    consulta: str,
    k: int = 3,
    *,
    ruta: Optional[Path] = None,
) -> Respuesta:
    """Percibe la consulta, recupera de la memoria y devuelve una `Respuesta` citada."""
    evento = perceive(consulta)
    resultados = recuperar(consulta, k, ruta=ruta)
    return Respuesta(consulta=consulta, evento=evento, resultados=resultados)
