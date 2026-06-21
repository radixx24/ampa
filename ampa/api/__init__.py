"""Capa API de AMPA: HTTP/JSON portable (stdlib) para el frontend.

Cero dependencias. Mantiene el núcleo intacto: la API es una capa fina sobre los
dominios (ADR 0015).
"""
from .server import manejar, servir  # noqa: F401
