"""Clasificador de dominio inicial, por reglas (Concepto Maestro §3).

Heurístico, sin ML ni dependencias externas: cuenta términos distintivos por
dominio sobre el texto normalizado (minúsculas, sin acentos). Se complementará
con la red neuronal (Pista B) más adelante; ver ADR 0008.
"""
from __future__ import annotations

import unicodedata
from typing import Dict, List, Tuple

from .events import DOCUMENTACION, FILOSOFIA, GENERAL, OPERACION, QUIMICA

# Términos distintivos por dominio (ya normalizados: minúsculas, sin acentos).
_KEYWORDS: Dict[str, Tuple[str, ...]] = {
    QUIMICA: (
        "atomo", "molecul", "enlace", "reaccion", "acido", "oxidacion",
        "reduccion", "elemento", "compuesto", "orbital", "electron", "valencia",
        "termodinamic", "entalpia", "catalizador", "disolucion", "solucion",
        "ionico", "covalent", "quimic", "estequiometr", "isotopo", "reactivo",
        "tabla periodica",
    ),
    FILOSOFIA: (
        "epistemolog", "ontolog", "metafisic", "etica", "moral", "falacia",
        "argument", "silogismo", "kant", "platon", "aristotel", "nietzsche",
        "descartes", "filosof", "dialectic", "fenomenolog", "libre albedrio",
        "empiris", "racionalis", "virtud", "deontolog", "utilitaris",
        "conocimiento", "verdad", "existenc",
    ),
    DOCUMENTACION: (
        "documentacion", "documento", "readme", "changelog", "glosario",
        "roadmap", "concepto maestro", "plantilla", "contrato", "docstring",
        "markdown", "bitacora", "adr",
    ),
    OPERACION: (
        "instalar", "ejecutar", "compilar", "comando", "backup", "respaldo",
        "ruta", "carpeta", "directorio", "cmake", "configurar", "dependencia",
        "terminal", "script", "commit", "push", "portabilidad", "windows",
        "linux", "macos", "build", "prueba", "test",
    ),
}

# Orden de preferencia ante empates de puntuación.
_PRIORIDAD = (QUIMICA, FILOSOFIA, OPERACION, DOCUMENTACION)


def normalizar(texto: str) -> str:
    """Minúsculas y sin acentos, para comparar de forma robusta en español."""
    t = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def puntuar(texto: str) -> Dict[str, List[str]]:
    """Devuelve, por dominio con coincidencias, la lista de términos hallados."""
    norm = normalizar(texto)
    hits: Dict[str, List[str]] = {}
    for dominio, claves in _KEYWORDS.items():
        encontrados = [k for k in claves if k in norm]
        if encontrados:
            hits[dominio] = encontrados
    return hits


def clasificar(texto: str) -> Tuple[str, List[str]]:
    """Clasifica el dominio. Devuelve ``(dominio, términos_encontrados)``.

    Si no hay coincidencias, el dominio es ``general``. En empate de número de
    coincidencias, gana el de mayor prioridad (``_PRIORIDAD``).
    """
    hits = puntuar(texto)
    if not hits:
        return GENERAL, []
    mejor = max(hits, key=lambda d: (len(hits[d]), -_PRIORIDAD.index(d)))
    return mejor, sorted(set(hits[mejor]))
