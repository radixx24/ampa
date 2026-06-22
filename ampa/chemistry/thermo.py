"""Termodinámica: Energía Libre de Gibbs como **umbral de espontaneidad**.

La pregunta «¿estos elementos/compuestos pueden coexistir o van a reaccionar?» se
responde, antes de tocar un tubo de ensayo, con la **Energía Libre de Gibbs**:

    ΔG = ΔH − T·ΔS

- **ΔH** (entalpía): si el sistema libera (−) o absorbe (+) calor.
- **ΔS** (entropía): si el desorden molecular aumenta (+) o disminuye (−).
- **Regla de oro**: si **ΔG < 0**, la reacción es **espontánea** (favorable). Si
  ΔG > 0 lo es la reacción inversa; si ΔG ≈ 0, hay equilibrio.

Para una reacción balanceada, ΔH y ΔS se obtienen de datos estándar de formación:

    ΔH° = Σ ΔHf°(productos) − Σ ΔHf°(reactivos)
    ΔS° = Σ S°(productos)   − Σ S°(reactivos)

Los datos (`_TERMO`) son valores **estándar a 298.15 K y 1 bar** (ΔHf° en kJ/mol,
S° en J/mol·K), tomados de tablas termodinámicas de referencia (CRC/NIST). Por
elemento en su **estado estándar**, ΔHf° = 0 por definición (su S° no es cero).

CONSIDERACIÓN HONESTA: usar estos valores a otra temperatura supone que ΔH y ΔS
**no dependen de T** (aproximación de Ellingham). Es una guía cualitativa muy útil
—predice bien el signo y el orden de magnitud— pero **no** sustituye a la química
cuántica / DFT, que simula los orbitales para decidir si una estructura colapsa.
Sin dependencias externas.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

from .balance import balancear, ecuacion

TEMP_ESTANDAR = 298.15  # K (25 °C)

# fórmula (en su estado estándar) → (ΔHf° kJ/mol, S° J/mol·K) a 298.15 K, 1 bar.
# Los elementos en estado estándar tienen ΔHf° = 0; el estado se indica al lado.
_TERMO: Dict[str, Tuple[float, float]] = {
    # --- Elementos en estado estándar (ΔHf° = 0) ---
    "H2": (0.0, 130.7),    # g
    "O2": (0.0, 205.2),    # g
    "N2": (0.0, 191.6),    # g
    "F2": (0.0, 202.8),    # g
    "Cl2": (0.0, 223.1),   # g
    "Br2": (0.0, 152.2),   # l
    "I2": (0.0, 116.1),    # s
    "C": (0.0, 5.7),       # s (grafito)
    "S": (0.0, 32.1),      # s (rómbico)
    "P": (0.0, 41.1),      # s (blanco)
    "Na": (0.0, 51.3),     # s
    "K": (0.0, 64.7),      # s
    "Li": (0.0, 29.1),     # s
    "Rb": (0.0, 76.8),     # s
    "Cs": (0.0, 85.2),     # s
    "Mg": (0.0, 32.7),     # s
    "Ca": (0.0, 41.6),     # s
    "Ba": (0.0, 62.5),     # s
    "Al": (0.0, 28.3),     # s
    "Fe": (0.0, 27.3),     # s
    "Cu": (0.0, 33.2),     # s
    "Zn": (0.0, 41.6),     # s
    "Ag": (0.0, 42.6),     # s
    "He": (0.0, 126.2), "Ne": (0.0, 146.3), "Ar": (0.0, 154.8),
    # --- Óxidos e hidróxidos ---
    "H2O": (-285.8, 69.9),     # l
    "H2O2": (-187.8, 109.6),   # l
    "CO2": (-393.5, 213.8),    # g
    "CO": (-110.5, 197.7),     # g
    "Na2O": (-414.2, 75.1),    # s
    "Na2O2": (-510.9, 95.0),   # s
    "NaOH": (-425.6, 64.5),    # s
    "KOH": (-424.6, 81.2),     # s
    "CaO": (-634.9, 38.1),     # s
    "Ca(OH)2": (-985.2, 83.4), # s
    "MgO": (-601.6, 27.0),     # s
    "Al2O3": (-1675.7, 50.9),  # s
    "Fe2O3": (-824.2, 87.4),   # s
    "CuO": (-157.3, 42.6),     # s
    "ZnO": (-350.5, 43.7),     # s
    "SO2": (-296.8, 248.2),    # g
    "SO3": (-395.7, 256.8),    # g
    "NO": (91.3, 210.8),       # g
    "NO2": (33.2, 240.1),      # g
    "N2O4": (9.2, 304.4),      # g
    # --- Sales y ácidos ---
    "NaCl": (-411.2, 72.1),    # s
    "KCl": (-436.5, 82.6),     # s
    "CaCl2": (-795.4, 108.4),  # s
    "CaCO3": (-1207.6, 91.7),  # s (calcita)
    "NH4Cl": (-314.4, 94.6),   # s
    "HCl": (-92.3, 186.9),     # g
    "HF": (-273.3, 173.8),     # g
    "HBr": (-36.3, 198.7),     # g
    "H2S": (-20.6, 205.8),     # g
    "HNO3": (-174.1, 155.6),   # l
    "H2SO4": (-814.0, 156.9),  # l
    "NH3": (-45.9, 192.8),     # g
    # --- Orgánicos comunes ---
    "CH4": (-74.6, 186.3),     # g
    "C2H6": (-84.0, 229.2),    # g
    "C2H4": (52.4, 219.3),     # g
    "C2H2": (227.4, 200.9),    # g
    "C3H8": (-103.8, 270.3),   # g
    "CH3OH": (-239.2, 126.8),  # l
    "C2H5OH": (-277.6, 160.7), # l
    "C6H6": (49.1, 173.4),     # l
    "C6H12O6": (-1273.3, 212.1),  # s (glucosa)
}


def datos_especie(formula: str) -> Optional[Dict[str, float]]:
    """``{formula, dHf (kJ/mol), S (J/mol·K)}`` si hay datos termo; si no, ``None``."""
    if formula in _TERMO:
        dhf, s = _TERMO[formula]
        return {"formula": formula, "dHf": dhf, "S": s}
    return None


def gibbs(dH: float, dS: float, T: float = TEMP_ESTANDAR) -> float:
    """ΔG = ΔH − T·ΔS, con ΔH en kJ y ΔS en J/K (devuelve kJ)."""
    return dH - T * dS / 1000.0


def _veredicto(dG: float) -> str:
    if dG < -0.5:
        return "espontánea"
    if dG > 0.5:
        return "no espontánea"
    return "en equilibrio"


def _motor(dH: float, dS: float) -> str:
    """Describe qué empuja la reacción (entalpía/entropía) y a qué temperatura."""
    calor = "exotérmica (libera calor)" if dH < 0 else "endotérmica (absorbe calor)"
    orden = "aumenta el desorden" if dS > 0 else "disminuye el desorden"
    if dH < 0 and dS > 0:
        cuando = "espontánea a cualquier temperatura"
    elif dH > 0 and dS < 0:
        cuando = "nunca espontánea (la inversa sí)"
    elif dH < 0 and dS < 0:
        cuando = "espontánea por debajo de la temperatura de cruce"
    else:
        cuando = "espontánea por encima de la temperatura de cruce"
    return f"{calor}; {orden}; {cuando}"


def evaluar(
    reactivos: Sequence[Tuple[int, str]],
    productos: Sequence[Tuple[int, str]],
    T: float = TEMP_ESTANDAR,
) -> Dict[str, object]:
    """Calcula ΔH, ΔS y ΔG de una reacción ya balanceada (coef, fórmula).

    Si falta algún dato termodinámico, lo reporta en ``faltan`` y no inventa.
    """
    faltan: List[str] = []
    dH = dS = 0.0
    for signo, lado in ((-1, reactivos), (1, productos)):
        for coef, formula in lado:
            d = datos_especie(formula)
            if d is None:
                faltan.append(formula)
                continue
            dH += signo * coef * d["dHf"]
            dS += signo * coef * d["S"]
    if faltan:
        return {"ok": False, "faltan": sorted(set(faltan)),
                "razon": "sin datos termodinámicos para algunas especies"}
    dG = gibbs(dH, dS, T)
    t_cruce = (dH * 1000.0 / dS) if abs(dS) > 1e-9 else None
    return {
        "ok": True,
        "T": round(T, 2),
        "dH": round(dH, 2),
        "dS": round(dS, 2),
        "dG": round(dG, 2),
        "espontanea": dG < 0,
        "veredicto": _veredicto(dG),
        "motor": _motor(dH, dS),
        "t_cruce": round(t_cruce, 1) if t_cruce is not None else None,
    }


def proyectar(
    reactivos: Sequence[str],
    productos: Sequence[str],
    T: float = TEMP_ESTANDAR,
) -> Dict[str, object]:
    """Balancea ``reactivos → productos`` y evalúa su Gibbs (el **umbral**).

    Es el pipeline completo de una *proyección*: balancea por conservación,
    calcula ΔG a la temperatura dada y emite un veredicto de espontaneidad.
    """
    coefs = balancear(reactivos, productos)
    if coefs is None:
        return {"ok": False, "razon": "no se pudo balancear (¿faltan o sobran especies?)"}
    cr, cp = coefs
    ev = evaluar(list(zip(cr, reactivos)), list(zip(cp, productos)), T)
    ev["ecuacion"] = ecuacion(reactivos, productos, coefs)
    ev["coeficientes"] = {"reactivos": cr, "productos": cp}
    return ev
