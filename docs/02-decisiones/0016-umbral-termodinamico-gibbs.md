# ADR-0016: Umbral de existencia por termodinámica (Gibbs) con datos curados

> Formato según Concepto Maestro §13.

## Estado

Aceptada

## Contexto

El usuario quiere *proyectar* compuestos y reacciones y decidir, **antes de
experimentar**, si pueden existir o si reaccionarían de forma destructiva. En
química, ese umbral lo da la **Energía Libre de Gibbs**:

    ΔG = ΔH − T·ΔS   →   si ΔG < 0, la reacción es espontánea.

La industria lo modela hoy con **química cuántica / DFT** (simula orbitales para
decidir si una estructura colapsa). DFT es inviable aquí: requiere librerías
pesadas, datos masivos y cómputo — choca de frente con la portabilidad (ADR 0007)
y con «reglas + datos antes que ML» (ADR 0008/0013).

## Opciones consideradas

- **A. Datos termodinámicos estándar curados + ΔG = ΔH − T·ΔS.** Tabla de ΔHf° y
  S° (298 K, 1 bar) de especies comunes; ΔH/ΔS de la reacción por diferencia
  productos − reactivos; veredicto por el signo de ΔG. Cero dependencias.
- **B. DFT / química cuántica real** (PySCF, psi4…): exacto en principio, pero
  pesado, lento y no portable.
- **C. Solo heurística cualitativa** (metal + no metal → reactivo): simple pero
  sin número, sin temperatura y sin honestidad cuantitativa.

## Decisión

**Opción A.** `ampa/chemistry/thermo.py` calcula ΔG a partir de una tabla curada
de ΔHf° y S°, sobre una ecuación **balanceada de forma general** (`balance.py`,
espacio nulo con `fractions.Fraction`). `proyectar(reactivos, productos, T)` es el
pipeline del umbral: balancea → calcula ΔH, ΔS, ΔG → emite veredicto y
**temperatura de cruce** (T donde ΔG = 0). La compatibilidad entre elementos
(`compatibility.py`) reúsa este motor para la **formación** del compuesto iónico
que predice por cargas.

## Alternativas

**B** se descartó por incompatible con la portabilidad (es el mismo motivo por el
que no usamos modelos pesados en el resto del sistema). **C** se incorpora como
*complemento* (tipo de enlace por ΔEN, fórmula por aspa de cargas), pero no como
el criterio principal: el número manda cuando hay datos.

## Consecuencias

- 👍 Reproduce los casos clásicos con el signo y el orden de magnitud correctos:
  Na + agua (ΔG ≪ 0), el «óxido de sodio hidratado» que colapsa a 2 NaOH (más
  estable), la caliza CaCO₃ que se descompone por encima de ~1120 K.
- 👍 Explicable y portable: se ve **por qué** (entalpía vs entropía, temperatura).
- 👎 Aproximación de Ellingham: usa ΔH y S° **independientes de T**; lejos de
  298 K el número pierde precisión (el **signo** y el cruce siguen siendo útiles).
- 👎 Cobertura limitada a las especies con datos en la tabla; si falta una, se
  **reporta** («faltan») en lugar de inventar (honestidad epistémica).
- ➡️ Si algún día se quiere precisión real, se puede enchufar DFT detrás de la
  misma interfaz `proyectar()` sin tocar el resto.
