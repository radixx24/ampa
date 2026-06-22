"""Compatibilidad entre elementos: ¿se llevan?, ¿qué forman y a qué T?

Cruza tres señales para decidir cómo interactúan dos elementos —y no solo de forma
orientativa, sino con química detrás:

1. **Tipo de enlace** por la diferencia de **electronegatividad** (ΔEN) y la
   naturaleza metálica/no metálica: iónico, covalente (polar/no polar), metálico
   (aleación) o inerte (gas noble).
2. **Fórmula probable** del compuesto iónico por balance de **cargas** (método del
   aspa / criss-cross): el subíndice de cada ion es la carga del otro, reducido.
3. **Veredicto termodinámico** (si hay datos): construye la reacción de formación
   ``elementos → compuesto``, la balancea y calcula su **ΔG** a la temperatura
   pedida (umbral de espontaneidad, ver `thermo`). Así la «compatibilidad» deja de
   ser cualitativa y se vuelve cuantitativa cuando hay datos.

Sin dependencias externas. Las cargas típicas son las usuales (orientativas para
metales de transición, que tienen varias).
"""
from __future__ import annotations

from math import gcd
from typing import Dict, Optional

from .elements import ELEMENTOS, NOMBRE_A_SIMBOLO, normalizar
from .thermo import proyectar

# Carga iónica típica (la más común) por símbolo. Positiva = catión (metal),
# negativa = anión (no metal). El carbono/silicio se tratan como covalentes (±4).
_CARGA: Dict[str, int] = {
    "H": 1, "Li": 1, "Na": 1, "K": 1, "Rb": 1, "Cs": 1,
    "Be": 2, "Mg": 2, "Ca": 2, "Sr": 2, "Ba": 2,
    "B": 3, "Al": 3, "Ga": 3,
    "N": -3, "P": -3,
    "O": -2, "S": -2, "Se": -2,
    "F": -1, "Cl": -1, "Br": -1, "I": -1,
    "Zn": 2, "Ag": 1, "Cu": 2, "Fe": 3, "Ni": 2, "Sn": 2, "Pb": 2,
}

# Forma estándar del elemento como reactivo (diatómicos) para la reacción termo.
_FORMA_ESTANDAR: Dict[str, str] = {
    "H": "H2", "O": "O2", "N": "N2", "F": "F2", "Cl": "Cl2",
}

_METALES = {
    "alcalino", "alcalinotérreo", "transición", "post-transición",
    "lantánido", "actínido",
}


def _resolver(sim_o_nombre: str) -> Optional[str]:
    """Acepta símbolo (``Na``) o nombre (``sodio``) y devuelve el símbolo."""
    s = sim_o_nombre.strip()
    if s in ELEMENTOS:
        return s
    return NOMBRE_A_SIMBOLO.get(normalizar(s))


def _formula_ionica(cat: str, q_cat: int, an: str, q_an: int) -> str:
    """Fórmula por balance de cargas (aspa), con subíndices reducidos."""
    sub_cat, sub_an = abs(q_an), abs(q_cat)
    g = gcd(sub_cat, sub_an)
    sub_cat, sub_an = sub_cat // g, sub_an // g

    def parte(sim: str, n: int) -> str:
        return sim + (str(n) if n > 1 else "")

    return parte(cat, sub_cat) + parte(an, sub_an)


def _reactividad(ea, eb, delta: float) -> str:
    cats = {ea.categoria, eb.categoria}
    if "gas noble" in cats:
        return "nula"
    muy = {"alcalino", "alcalinotérreo"}
    reactivo_no_metal = {"halógeno"} | ({"no metal"} if "O" in (ea.simbolo, eb.simbolo) else set())
    if (ea.categoria in muy and eb.categoria in reactivo_no_metal) or (
        eb.categoria in muy and ea.categoria in reactivo_no_metal
    ):
        return "muy alta"
    if delta > 2.0:
        return "alta"
    if delta >= 1.0:
        return "media"
    return "baja"


def compatibilidad(a: str, b: str, T: float = 298.15) -> Dict[str, object]:
    """Evalúa cómo se comportan los elementos ``a`` y ``b`` a la temperatura ``T``."""
    sa, sb = _resolver(a), _resolver(b)
    if sa is None or sb is None:
        falla = a if sa is None else b
        return {"ok": False, "razon": f"elemento desconocido: {falla!r}"}
    ea, eb = ELEMENTOS[sa], ELEMENTOS[sb]

    salida: Dict[str, object] = {"ok": True, "a": sa, "b": sb, "T": round(T, 2)}

    # Gas noble → inerte.
    if "gas noble" in (ea.categoria, eb.categoria):
        salida.update(tipo_enlace="inerte", producto=None, reactividad="nula",
                      veredicto="Un gas noble es prácticamente inerte: no forma "
                                "compuestos en condiciones normales.")
        return salida

    delta = round(abs(ea.electronegatividad - eb.electronegatividad), 2) \
        if ea.electronegatividad and eb.electronegatividad else None
    salida["delta_en"] = delta

    amb_metal = ea.categoria in _METALES and eb.categoria in _METALES
    qa, qb = _CARGA.get(sa), _CARGA.get(sb)
    cation = anion = None
    if qa is not None and qb is not None and (qa > 0) != (qb > 0):
        (cation, q_cat), (anion, q_an) = (
            ((sa, qa), (sb, qb)) if qa > 0 else ((sb, qb), (sa, qa))
        )

    if amb_metal:
        salida.update(tipo_enlace="metálico", producto=None,
                      reactividad="baja",
                      veredicto="Dos metales forman una aleación (enlace metálico), "
                                "no un compuesto iónico definido.")
        return salida

    # Tipo de enlace por ΔEN (umbral clásico 1.7 para iónico).
    if delta is not None and delta >= 1.7 and cation is not None:
        tipo = "iónico"
    elif delta is not None and delta >= 0.5:
        tipo = "covalente polar"
    else:
        tipo = "covalente no polar"
    salida["tipo_enlace"] = tipo
    salida["reactividad"] = _reactividad(ea, eb, delta or 0.0)

    producto = None
    if cation is not None:
        producto = _formula_ionica(cation, _CARGA[cation], anion, _CARGA[anion])
    salida["producto"] = producto

    # Veredicto termodinámico de la formación, si hay producto y datos.
    if producto is not None:
        ra = _FORMA_ESTANDAR.get(sa, sa)
        rb = _FORMA_ESTANDAR.get(sb, sb)
        termo = proyectar([ra, rb], [producto], T)
        if termo.get("ok"):
            salida["termo"] = termo
            esp = "favorable (ΔG < 0)" if termo["espontanea"] else "desfavorable (ΔG > 0)"
            salida["veredicto"] = (
                f"Formarían {producto} con enlace {tipo}. Su formación es {esp} a "
                f"{round(T)} K (ΔG = {termo['dG']} kJ/mol)."
            )
        else:
            salida["veredicto"] = (
                f"Tenderían a formar {producto} con enlace {tipo} "
                f"(reactividad {salida['reactividad']})."
            )
    else:
        salida["veredicto"] = (
            f"Interacción {tipo} (ΔEN = {delta}); no es un par iónico simple."
        )
    return salida
