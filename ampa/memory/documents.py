"""Estructuras de la memoria documental: el fragmento citable.

Un :class:`Fragmento` es la unidad mínima de memoria: un trozo de texto con su
fuente y posición, lo que permite **citar** de dónde salió cada respuesta. Sin
dependencias externas.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class Fragmento:
    """Trozo de apunte con su procedencia (para citar)."""

    texto: str
    fuente: str
    indice: int
    dominio: str = "general"

    @property
    def id(self) -> str:
        return f"{self.fuente}#{self.indice}"

    def to_dict(self) -> Dict[str, object]:
        return {
            "texto": self.texto,
            "fuente": self.fuente,
            "indice": self.indice,
            "dominio": self.dominio,
        }

    @classmethod
    def from_dict(cls, datos: Dict[str, object]) -> "Fragmento":
        return cls(
            texto=str(datos["texto"]),
            fuente=str(datos["fuente"]),
            indice=int(datos["indice"]),  # type: ignore[arg-type]
            dominio=str(datos.get("dominio", "general")),
        )
