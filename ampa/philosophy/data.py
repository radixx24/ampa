"""Base curada de filosofía (datos estáticos, sin dependencias).

Tres datasets mínimos para reconocer **filósofos**, **corrientes** y **conceptos**
en texto, con metadatos (época, corriente, rama) para usos visuales/adaptativos.
Ampliable.
"""
from __future__ import annotations

from typing import Dict, Tuple

_TABLA = str.maketrans("áéíóúüñ", "aeiouun")


def normalizar(texto: str) -> str:
    """Minúsculas y sin acentos, preservando longitud (útil para spans)."""
    return texto.lower().translate(_TABLA)


# clave normalizada (lo que aparece en el texto) → (nombre, época, corriente)
_FILOSOFOS = [
    ("socrates", "Sócrates", "Antigua", "mayéutica"),
    ("platon", "Platón", "Antigua", "idealismo"),
    ("aristoteles", "Aristóteles", "Antigua", "realismo"),
    ("epicuro", "Epicuro", "Antigua", "epicureísmo"),
    ("seneca", "Séneca", "Antigua", "estoicismo"),
    ("agustin", "San Agustín", "Medieval", "patrística"),
    ("aquino", "Tomás de Aquino", "Medieval", "escolástica"),
    ("descartes", "Descartes", "Moderna", "racionalismo"),
    ("spinoza", "Spinoza", "Moderna", "racionalismo"),
    ("leibniz", "Leibniz", "Moderna", "racionalismo"),
    ("locke", "Locke", "Moderna", "empirismo"),
    ("hume", "Hume", "Moderna", "empirismo"),
    ("berkeley", "Berkeley", "Moderna", "idealismo"),
    ("hobbes", "Hobbes", "Moderna", "contractualismo"),
    ("rousseau", "Rousseau", "Moderna", "contractualismo"),
    ("kant", "Kant", "Moderna", "idealismo trascendental"),
    ("hegel", "Hegel", "Moderna", "idealismo"),
    ("schopenhauer", "Schopenhauer", "Moderna", "idealismo"),
    ("kierkegaard", "Kierkegaard", "Contemporánea", "existencialismo"),
    ("marx", "Marx", "Contemporánea", "materialismo"),
    ("nietzsche", "Nietzsche", "Contemporánea", "vitalismo"),
    ("husserl", "Husserl", "Contemporánea", "fenomenología"),
    ("heidegger", "Heidegger", "Contemporánea", "fenomenología"),
    ("sartre", "Sartre", "Contemporánea", "existencialismo"),
    ("camus", "Camus", "Contemporánea", "existencialismo"),
    ("wittgenstein", "Wittgenstein", "Contemporánea", "filosofía analítica"),
    ("russell", "Russell", "Contemporánea", "filosofía analítica"),
    ("popper", "Popper", "Contemporánea", "racionalismo crítico"),
    ("comte", "Comte", "Contemporánea", "positivismo"),
    ("foucault", "Foucault", "Contemporánea", "postestructuralismo"),
]

# clave normalizada → (nombre con acentos, rama)
_CONCEPTOS = [
    ("epistemologia", "epistemología", "teoría del conocimiento"),
    ("gnoseologia", "gnoseología", "teoría del conocimiento"),
    ("metafisica", "metafísica", "metafísica"),
    ("ontologia", "ontología", "ser / metafísica"),
    ("etica", "ética", "ética"),
    ("estetica", "estética", "estética"),
    ("logica", "lógica", "lógica"),
    ("dialectica", "dialéctica", "método / lógica"),
    ("fenomeno", "fenómeno", "epistemología"),
    ("noumeno", "noúmeno", "metafísica"),
    ("sustancia", "sustancia", "metafísica"),
    ("esencia", "esencia", "metafísica"),
    ("existencia", "existencia", "metafísica"),
    ("trascendental", "trascendental", "epistemología"),
    ("virtud", "virtud", "ética"),
    ("silogismo", "silogismo", "lógica"),
    ("mayeutica", "mayéutica", "método"),
    ("imperativo categorico", "imperativo categórico", "ética"),
]

# clave normalizada → nombre con acentos
_CORRIENTES = [
    ("racionalismo", "racionalismo"),
    ("empirismo", "empirismo"),
    ("idealismo", "idealismo"),
    ("materialismo", "materialismo"),
    ("realismo", "realismo"),
    ("existencialismo", "existencialismo"),
    ("estoicismo", "estoicismo"),
    ("epicureismo", "epicureísmo"),
    ("escepticismo", "escepticismo"),
    ("escolastica", "escolástica"),
    ("patristica", "patrística"),
    ("fenomenologia", "fenomenología"),
    ("positivismo", "positivismo"),
    ("nihilismo", "nihilismo"),
    ("utilitarismo", "utilitarismo"),
    ("pragmatismo", "pragmatismo"),
    ("marxismo", "marxismo"),
    ("dualismo", "dualismo"),
    ("monismo", "monismo"),
    ("determinismo", "determinismo"),
    ("relativismo", "relativismo"),
    ("humanismo", "humanismo"),
    ("estructuralismo", "estructuralismo"),
    ("hedonismo", "hedonismo"),
]

FILOSOFOS: Dict[str, Tuple[str, str, str]] = {
    clave: (nombre, epoca, corriente) for clave, nombre, epoca, corriente in _FILOSOFOS
}
CONCEPTOS: Dict[str, Tuple[str, str]] = {
    clave: (nombre, rama) for clave, nombre, rama in _CONCEPTOS
}
CORRIENTES: Dict[str, str] = {clave: nombre for clave, nombre in _CORRIENTES}
