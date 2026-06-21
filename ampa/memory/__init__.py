"""Memoria documental de AMPA (Concepto Maestro, Fase 3).

Ingiere apuntes, los trocea en **fragmentos citables** y los recupera por
relevancia léxica (**BM25**) con **citas**. Primera iteración sin embeddings
(ADR 0010). Sin dependencias externas.
"""
from .chunker import trocear  # noqa: F401
from .documents import Fragmento  # noqa: F401
from .ingest import ResultadoIngesta, ingerir, ingerir_carpeta  # noqa: F401
from .retriever import Resultado, recuperar  # noqa: F401
from .store import (  # noqa: F401
    cargar_fragmentos,
    fuentes,
    reiniciar,
    ruta_memoria,
)
