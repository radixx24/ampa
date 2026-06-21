"""Reconocimiento químico de AMPA (componentes y compuestos).

Identifica **elementos** y **compuestos** en texto y los entrega estructurados
(símbolo, número atómico, composición) para usos visuales/adaptativos. Incluye una
tabla periódica de 118 elementos y un parser de fórmulas. Sin dependencias.
"""
from .elements import ELEMENTOS, Elemento, tabla  # noqa: F401
from .formulas import composicion_valida, masa_molar, parsear_formula  # noqa: F401
from .groups import grupos_funcionales  # noqa: F401
from .reactions import Reaccion, reacciones  # noqa: F401
from .molecules import (  # noqa: F401
    Molecula,
    cargar_compuestos,
    guardar_compuesto,
    ruta_compuestos,
)
from .recognizer import EntidadQuimica, ResultadoQuimica, identificar  # noqa: F401
