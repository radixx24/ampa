"""Reconocimiento de filosofía de AMPA (Concepto Maestro, Fase 6).

Identifica **filósofos**, **corrientes** y **conceptos** en texto y los entrega
estructurados (época, corriente, rama) para usos visuales/adaptativos. Reglas +
datos, como el dominio químico (ADR 0013). Sin dependencias.
"""
from .recognizer import EntidadFilosofica, ResultadoFilosofia, identificar  # noqa: F401
