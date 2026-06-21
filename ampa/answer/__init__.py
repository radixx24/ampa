"""Capa de respuesta de AMPA (Concepto Maestro, Fase 4).

Responde preguntas **con fuentes**: percibe la consulta, recupera de la memoria y
compone una respuesta con citas. Recuperación **extractiva** (sin generación de
lenguaje todavía; ADR 0011). Sin dependencias externas.
"""
from .responder import Respuesta, responder  # noqa: F401
