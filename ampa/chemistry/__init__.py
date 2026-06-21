"""Reconocimiento químico de AMPA (componentes y compuestos).

Identifica **elementos** y **compuestos** en texto y los entrega estructurados
(símbolo, número atómico, composición) para usos visuales/adaptativos. Incluye una
tabla periódica de 118 elementos y un parser de fórmulas. Sin dependencias.
"""
from .elements import ELEMENTOS  # noqa: F401
from .formulas import composicion_valida, parsear_formula  # noqa: F401
from .recognizer import EntidadQuimica, ResultadoQuimica, identificar  # noqa: F401
