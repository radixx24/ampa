"""Escriba seguro de AMPA (Concepto Maestro, Fase 5).

Escritura de archivos multiplataforma con **respaldo previo**, **modo
simulación** y **bloqueo por riesgo operativo alto**. Sin dependencias externas.
"""
from .writer import (  # noqa: F401
    ResultadoEscritura,
    escribir,
    respaldos_de,
    restaurar,
)
