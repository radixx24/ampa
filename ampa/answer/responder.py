"""Respuesta con fuentes: percepción + recuperación de memoria (Fase 4).

Compone una respuesta **extractiva y citada** a partir de los apuntes: percibe la
consulta (dominio, riesgo), recupera los fragmentos más relevantes (BM25) y los
presenta con sus citas, su **confianza** y su **origen**. Además señala la
**química detectada** (elementos y compuestos). La **generación con modelo**
llegará como capa posterior sobre estos mismos fragmentos (ADR 0011). Sin
dependencias externas.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from ..chemistry import ResultadoQuimica, identificar
from ..memory import Resultado, recuperar
from ..memory.retriever import tokenizar
from ..perception import perceive
from ..perception.events import Evento


def _una_linea(texto: str, limite: int = 220) -> str:
    plano = " ".join(texto.split())
    return plano if len(plano) <= limite else plano[: limite - 1] + "…"


def _estimar_confianza(
    evento: Evento, resultados: List[Resultado], consulta: str
) -> str:
    """Confianza cualitativa, honesta y portable.

    Se basa en la **cobertura** de los términos de la consulta por la mejor
    evidencia más el **acuerdo de dominio**, no en el score BM25 absoluto (que
    depende del tamaño del corpus).
    """
    if not resultados:
        return "nula"
    terminos = set(tokenizar(consulta))
    if not terminos:
        return "baja"
    cubiertos = terminos & set(tokenizar(resultados[0].fragmento.texto))
    cobertura = len(cubiertos) / len(terminos)
    dominio_ok = resultados[0].fragmento.dominio == evento.dominio_probable
    if cobertura >= 0.6 and dominio_ok:
        return "alta"
    if cobertura >= 0.3:
        return "media"
    return "baja"


@dataclass
class Respuesta:
    """Respuesta citada a una consulta, construida por recuperación."""

    consulta: str
    evento: Evento
    resultados: List[Resultado]
    confianza: str = "nula"
    quimica: Optional[ResultadoQuimica] = None

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

    def origen(self) -> List[str]:
        """Fuentes que respaldan la respuesta (sinónimo de `fuentes`)."""
        return self.fuentes()

    def _texto_quimica(self) -> str:
        if not self.quimica or not self.quimica.hay():
            return ""
        partes = []
        elementos = ", ".join(e.simbolo for e in self.quimica.elementos)
        compuestos = ", ".join(c.formula for c in self.quimica.compuestos)
        if elementos:
            partes.append(f"elementos: {elementos}")
        if compuestos:
            partes.append(f"compuestos: {compuestos}")
        return "Química detectada — " + " · ".join(partes)

    def texto(self) -> str:
        """Respuesta legible y honesta, con citas, confianza y origen."""
        quimica = self._texto_quimica()
        if not self.resultados:
            cuerpo = (
                f"No encuentro nada en la memoria sobre «{self.consulta}» "
                f"(dominio probable: {self.dominio}).\n"
                "No invento la respuesta: por ahora solo recupero de tus apuntes, "
                "aún sin generación con modelo."
            )
            return cuerpo + (f"\n\n{quimica}" if quimica else "")
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
            f"Confianza: {self.confianza} · Origen: {', '.join(self.origen()) or '—'}",
        ]
        if quimica:
            lineas.append(quimica)
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
            f"confianza: {self.confianza}",
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
    material = " ".join([consulta] + [r.fragmento.texto for r in resultados[:2]])
    return Respuesta(
        consulta=consulta,
        evento=evento,
        resultados=resultados,
        confianza=_estimar_confianza(evento, resultados, consulta),
        quimica=identificar(material),
    )
