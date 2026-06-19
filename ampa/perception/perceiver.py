"""Perceiver: convierte una entrada autorizada en un Evento estructurado.

Implementa las etapas «percibir» e «interpretar» del ciclo del Concepto Maestro
(§5 y §7). Sin dependencias externas.
"""
from __future__ import annotations

import re
from typing import List, Optional

from . import events as E
from .classifier import clasificar, normalizar

# Verbos que indican una operación/acción (no una pregunta).
_VERBOS_COMANDO = (
    "instala", "ejecuta", "compila", "configura", "respalda", "corrige",
    "borra", "elimina", "sobrescribe", "modifica", "actualiza", "crea",
    "genera", "guarda", "reemplaza", "haz", "construye",
)

# Términos que implican modificación de archivos (riesgo de escritura).
_MOD_ARCHIVO = (
    "corrige", "corregir", "borra", "borrar", "elimina", "eliminar",
    "sobrescrib", "modifica", "modificar", "actualiza", "escribe", "escribir",
    "reemplaza", "reemplazar", "guarda",
)

# Palabras típicas de inicio de pregunta.
_INTERROGATIVAS = (
    "que", "como", "por que", "porque", "cuando", "donde", "cual", "quien",
    "cuanto", "explica", "explicame", "define", "compara",
)

# Detección sencilla de nombres de archivo (algo.ext, ruta/algo.ext).
_RE_ARCHIVO = re.compile(r"[\w./\\-]+\.[A-Za-z]{1,6}")

_INTENCION_TIPO = {
    E.PREGUNTA: "consulta",
    E.COMANDO: "solicitud de operación",
    E.CORRECCION: "corrección",
    E.ERROR: "reporte de error",
    E.DECISION: "registro de decisión",
    E.ARCHIVO_MODIFICADO: "cambio en archivo",
}
_INTENCION_DOMINIO = {
    E.QUIMICA: "de química",
    E.FILOSOFIA: "de filosofía",
    E.DOCUMENTACION: "de documentación",
    E.OPERACION: "técnica",
    E.GENERAL: "general",
}


def _inferir_tipo(texto: str, norm: str) -> str:
    palabras = norm.split()
    primera = palabras[0] if palabras else ""
    if primera in _VERBOS_COMANDO:
        return E.COMANDO
    if texto.strip().endswith("?") or any(norm.startswith(p) for p in _INTERROGATIVAS):
        return E.PREGUNTA
    return E.PREGUNTA


def _detectar_archivos(texto: str, archivos: Optional[List[str]]) -> List[str]:
    encontrados: List[str] = list(archivos) if archivos else []
    for match in _RE_ARCHIVO.findall(texto):
        if match not in encontrados:
            encontrados.append(match)
    return encontrados


def _evaluar_riesgo(tipo: str, norm: str, archivos: List[str]) -> str:
    modifica = any(k in norm for k in _MOD_ARCHIVO)
    if (tipo == E.COMANDO and modifica) or (modifica and archivos):
        return E.ALTO
    if tipo == E.COMANDO or archivos or tipo in (E.CORRECCION, E.ARCHIVO_MODIFICADO):
        return E.MEDIO
    return E.BAJO


def perceive(
    texto: str,
    tipo: Optional[str] = None,
    archivos: Optional[List[str]] = None,
) -> E.Evento:
    """Convierte ``texto`` (más metadatos opcionales) en un :class:`Evento`.

    ``tipo`` se infiere si no se indica. ``archivos`` añade rutas relacionadas a
    las que se detecten en el propio texto.
    """
    norm = normalizar(texto)
    dominio, terminos = clasificar(texto)

    if tipo is None or tipo not in E.TIPOS:
        tipo = _inferir_tipo(texto, norm)

    archivos_rel = _detectar_archivos(texto, archivos)
    riesgo = _evaluar_riesgo(tipo, norm, archivos_rel)

    # Política de memoria (§6.2): no guardar ruido general trivial.
    guardar = (dominio != E.GENERAL) or (
        tipo in (E.DECISION, E.CORRECCION, E.ARCHIVO_MODIFICADO)
    )
    if dominio == E.GENERAL and tipo == E.PREGUNTA and len(norm.split()) < 4:
        guardar = False

    intencion = (
        f"{_INTENCION_TIPO.get(tipo, 'evento')} "
        f"{_INTENCION_DOMINIO.get(dominio, '')}"
    ).strip()
    justificacion = (
        f"Clasificado como {dominio} "
        f"(términos: {', '.join(terminos) if terminos else 'ninguno'}); "
        f"tipo {tipo}; riesgo {riesgo}."
    )

    return E.Evento(
        tipo=tipo,
        dominio_probable=dominio,
        entidades_relevantes=terminos,
        archivos_relacionados=archivos_rel,
        intencion_detectada=intencion,
        riesgo_operativo=riesgo,
        guardar_en_memoria=guardar,
        justificacion=justificacion,
    )
