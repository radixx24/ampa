"""Contrato del evento de percepción (Concepto Maestro §5.2 y §14).

Define la estructura mínima en la que AMPA convierte cualquier entrada autorizada.
Sin dependencias externas.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

# --- Tipos de evento (§5.2) ---
PREGUNTA = "pregunta"
ARCHIVO_MODIFICADO = "archivo_modificado"
CORRECCION = "correccion"
ERROR = "error"
DECISION = "decision"
COMANDO = "comando"
TIPOS = (PREGUNTA, ARCHIVO_MODIFICADO, CORRECCION, ERROR, DECISION, COMANDO)

# --- Dominios (§3) ---
QUIMICA = "quimica"
FILOSOFIA = "filosofia"
GENERAL = "general"
DOCUMENTACION = "documentacion"
OPERACION = "operacion"
DOMINIOS = (QUIMICA, FILOSOFIA, GENERAL, DOCUMENTACION, OPERACION)

# --- Riesgo operativo ---
BAJO = "bajo"
MEDIO = "medio"
ALTO = "alto"
RIESGOS = (BAJO, MEDIO, ALTO)


@dataclass
class Evento:
    """Evento de percepción estructurado, conforme al contrato §5.2."""

    tipo: str
    dominio_probable: str
    entidades_relevantes: List[str] = field(default_factory=list)
    archivos_relacionados: List[str] = field(default_factory=list)
    intencion_detectada: str = ""
    riesgo_operativo: str = BAJO
    guardar_en_memoria: bool = False
    justificacion: str = ""

    def to_dict(self) -> Dict[str, object]:
        return {
            "tipo": self.tipo,
            "dominio_probable": self.dominio_probable,
            "entidades_relevantes": list(self.entidades_relevantes),
            "archivos_relacionados": list(self.archivos_relacionados),
            "intencion_detectada": self.intencion_detectada,
            "riesgo_operativo": self.riesgo_operativo,
            "guardar_en_memoria": self.guardar_en_memoria,
            "justificacion": self.justificacion,
        }

    def as_yaml(self) -> str:
        """Renderiza el evento como YAML simple (sin dependencias), igual al
        formato del contrato del Concepto Maestro §5.2."""

        def lista(xs: List[str]) -> str:
            return "[" + ", ".join(xs) + "]" if xs else "[]"

        return (
            "evento:\n"
            f"  tipo: {self.tipo}\n"
            f"  dominio_probable: {self.dominio_probable}\n"
            f"  entidades_relevantes: {lista(self.entidades_relevantes)}\n"
            f"  archivos_relacionados: {lista(self.archivos_relacionados)}\n"
            f'  intencion_detectada: "{self.intencion_detectada}"\n'
            f"  riesgo_operativo: {self.riesgo_operativo}\n"
            f"  guardar_en_memoria: {'true' if self.guardar_en_memoria else 'false'}\n"
            f'  justificacion: "{self.justificacion}"\n'
        )
