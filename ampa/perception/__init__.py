"""Capa de percepción de AMPA (Concepto Maestro §5).

Convierte entradas autorizadas en eventos estructurados que el resto del sistema
puede interpretar, recuperar y auditar. Sin dependencias externas.
"""
from .events import Evento  # noqa: F401
from .perceiver import perceive  # noqa: F401
