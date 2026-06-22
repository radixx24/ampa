# Módulo: termodinámica (el umbral de existencia)

> Documentado según la plantilla del Concepto Maestro §12.
> Código: `ampa/chemistry/{balance,thermo,compatibility}.py` · Decisión: ADR 0016
> Pruebas: `tests/test_balance.py`, `tests/test_thermo.py`, `tests/test_compatibility.py`

## 1. Propósito

Decidir, **antes de experimentar**, si una reacción o un compuesto que proyectas
puede existir / ser espontáneo. El criterio es la **Energía Libre de Gibbs**:

    ΔG = ΔH − T·ΔS      (si ΔG < 0 → espontánea)

Es el mismo umbral que usan los químicos para saber, sin tocar un tubo de ensayo,
que «el sodio destruirá el agua» o que un «óxido de sodio hidratado» colapsará a
hidróxido (la forma más estable). Aquí se hace con **datos curados + álgebra**,
sin DFT ni dependencias (ADR 0016).

## 2. Responsabilidad exacta

**Hace:**
- **Balancea** cualquier ecuación (`balance.py`) por conservación de la materia,
  con aritmética **exacta** (`fractions.Fraction`).
- Calcula **ΔH, ΔS y ΔG** de una reacción balanceada a una temperatura `T`
  (`thermo.py`), con la **temperatura de cruce** (T donde ΔG cambia de signo) y
  una explicación del **motor** (entálpico vs entrópico).
- Evalúa la **compatibilidad** de dos elementos (`compatibility.py`): tipo de
  enlace (ΔEN), **fórmula probable** por aspa de cargas, reactividad y el ΔG de
  formación cuando hay datos.

**No hace:**
- No simula orbitales (no es DFT/química cuántica). No predice cinética (qué tan
  *rápido* ocurre), solo si es **termodinámicamente** favorable.
- No inventa datos: si falta ΔHf°/S° de una especie, lo **reporta** (`faltan`).

## 3. Entradas

- `balancear(reactivos, productos)`: listas de fórmulas (`["CH4","O2"]`).
- `proyectar(reactivos, productos, T)`: lo mismo + temperatura en K (def. 298.15).
- `compatibilidad(a, b, T)`: dos elementos (símbolo o nombre) + temperatura.

## 4. Salidas

- `balancear` → `([coef_react…], [coef_prod…])` (enteros mínimos) o `None`.
- `proyectar` → `{ok, ecuacion, dH, dS, dG, espontanea, veredicto, motor,
  t_cruce, T, coeficientes}` o `{ok:false, razon|faltan}`.
- `compatibilidad` → `{ok, a, b, tipo_enlace, delta_en, producto, reactividad,
  veredicto, termo?}`.

## 5. Flujo interno (cómo actúa)

### Balanceo general (`balance.py`)
1. Cada especie se parsea a su composición (`formulas.parsear_formula`).
2. Se arma la matriz **elemento × especie**: reactivos en **positivo**, productos
   en **negativo**. Conservar la materia es `M · x = 0`.
3. Se reduce la matriz a RREF y se busca el **espacio nulo**. Si su dimensión es 1
   (rango = nº especies − 1), hay solución única salvo factor.
4. El vector se escala a **enteros mínimos** (mínimo común múltiplo de los
   denominadores ÷ máximo común divisor). Si quedan signos mezclados o ceros, el
   reparto reactivos/productos no balancea → `None`.

### Gibbs (`thermo.py`)
1. De la tabla `_TERMO` (ΔHf° en kJ/mol, S° en J/mol·K a 298 K, 1 bar) se obtiene
   cada especie. Por elemento en estado estándar, ΔHf° = 0 (su S° no).
2. `ΔH = Σ coef·ΔHf°(prod) − Σ coef·ΔHf°(react)`; igual para `ΔS` con S°.
3. `ΔG = ΔH − T·ΔS/1000` (cuida las unidades: S° viene en J, ΔH en kJ).
4. **Temperatura de cruce** `T* = ΔH·1000 / ΔS`: si ΔH y ΔS tienen el mismo signo,
   ahí ΔG = 0 y el veredicto cambia (Ellingham).

### Compatibilidad (`compatibility.py`)
1. **Tipo de enlace**: gas noble → inerte; dos metales → metálico (aleación);
   metal + no metal con ΔEN ≥ 1.7 → iónico; resto → covalente (polar/no polar).
2. **Fórmula** (solo iónicos): aspa de cargas — el subíndice de cada ion es la
   carga del otro, reducido por su MCD (Na⁺ + Cl⁻ → NaCl; Al³⁺ + O²⁻ → Al₂O₃).
3. **Termo**: arma la formación `elementos → compuesto` (con los diatómicos en su
   forma estándar: O→O₂, Cl→Cl₂…), la balancea y la pasa por `proyectar`.

## 6. Decisiones de diseño

- **Datos + álgebra antes que DFT** (ADR 0016): explicable y portable.
- **Aritmética exacta** en el balanceo (`Fraction`): sin errores de redondeo.
- **Honestidad**: si faltan datos, se dice; no se rellena con suposiciones.

## 7. Errores esperados

- Fórmula inválida o reacción no balanceable → `None` / `{ok:false}`.
- Especie sin datos termodinámicos → `{ok:false, faltan:[…]}`.
- Elemento desconocido en compatibilidad → `{ok:false, razon}`.

## 8. Seguridad y límites (NETA)

- **Aproximación de Ellingham**: ΔH y S° se toman **independientes de T**. Lejos de
  298 K el número pierde exactitud; el **signo** y la **temperatura de cruce**
  siguen siendo orientativos y útiles.
- Es **termodinámica**, no **cinética**: dice si una reacción *puede* ocurrir, no
  si es rápida (el diamante «debería» ser grafito y no lo ves convertirse).
- La tabla cubre especies **comunes**; ampliarla es añadir filas a `_TERMO`.
- Las cargas iónicas son las **típicas** (los metales de transición tienen varias).

## 9. Pruebas / verificación

- `test_balance.py` (9): combustión, formación de agua, Na+agua, óxido hidratado,
  redox del hierro, amoniaco, casos imposibles e inválidos, formato de ecuación.
- `test_thermo.py` (7): fórmula y signo de Gibbs, Na+agua ≪ 0, el óxido hidratado
  que colapsa a NaOH, combustión exotérmica, temperatura de cruce de la caliza,
  y el manejo honesto de datos faltantes.
- `test_compatibility.py` (7): NaCl iónico, Al₂O₃ por aspa, CaO reducido, C+O
  covalente, gas noble inerte, dos metales (aleación) y elemento desconocido.
- Ejecutar: `python -m unittest discover -s tests -t .`

## 10. Cambios pendientes

- Ampliar `_TERMO` (más especies; estados aq para disoluciones).
- Capacidades caloríficas (Cp) para corregir ΔH/ΔS con la temperatura.
- Predicción de varios productos plausibles y elección del más estable.
