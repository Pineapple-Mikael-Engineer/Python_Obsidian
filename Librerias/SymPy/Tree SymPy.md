---
title: Tree SymPy
draft: true
---

# 🌳 Tree SymPy

> Estructura **jerárquica** por **submódulo** (`sympy.core`, `sympy.solvers`, `sympy.calculus`…)
> cruzado con **temáticas**. SymPy es **matemática simbólica**: opera sobre `Expr` (árboles de
> expresión exactos), no sobre números de punto flotante.
> `✅` = nota creada · sin marca = roadmap pendiente.

---

## 📁 Tipos de notas

| Tipo | Ubicación | Ejemplo |
|------|-----------|---------|
| **Concepto transversal** | `conceptos_transversales/` | `concepto_expr_arbol.md` |
| **Función de submódulo** | `sympy.<sub>/<tematica>/` | `sympy.solve.md`, `sympy.diff.md` |
| **Clase / objeto** | `sympy.<sub>/` o su temática | `Symbol.md`, `Matrix.md`, `Poly.md` |
| **Método de objeto** | junto a su clase | `Matrix.det.md`, `Expr.subs.md` |
| **Índice de carpeta** | `index.md` en **cada** directorio | nota madre/hub que lista su contenido |

> Cada carpeta del árbol lleva su `index.md` (hub de navegación). No se listan en el bloque
> de abajo para no saturarlo; ver [[Reglas]] §2. `sync_tree.py` los ignora en el conteo de cobertura.

Naming API-style: funciones top-level como `sympy.<funcion>.md` (`sympy.integrate.md`); clases con
su **nombre real** (`Symbol.md`, `Matrix.md`, `Interval.md`); métodos `Objeto.metodo.md`
(`Matrix.eigenvals.md`); conceptos `concepto_<tema>.md`.

---

## 📂 Estructura completa (roadmap)

```tree
SymPy/
│
├── introduccion.md
│
├── 📁 conceptos_transversales/
│   ├── ✅ concepto_simbolico_vs_numerico.md      # por que SymPy: exacto vs flotante
│   ├── ✅ concepto_expr_arbol.md                 # Expr, .func/.args, srepr, inmutabilidad
│   ├── ✅ concepto_symbols_assumptions.md        # Symbol + supuestos (real, positive…)
│   ├── ✅ concepto_evalf_lambdify.md             # de simbolico a numerico (subs/evalf/lambdify)
│   └── ✅ concepto_simplificacion_automatica.md  # auto-simplify, Rational vs float
│
├── 📁 sympy.core/
│   ├── 📁 simbolos/
│   │   ├── ✅ sympy.symbols.md
│   │   ├── ✅ Symbol.md
│   │   └── ✅ sympy.sympify.md                   # str/num -> Expr (S())
│   ├── 📁 numeros/
│   │   ├── ✅ Rational.md
│   │   ├── ✅ Integer.md
│   │   ├── ✅ Float.md
│   │   └── ✅ sympy.constantes_simbolicas.md     # pi, E, oo, I, nan, S
│   ├── 📁 expresiones/
│   │   ├── ✅ Expr.md
│   │   ├── ✅ sympy.srepr.md
│   │   └── ✅ Expr.subs.md
│   └── 📁 evaluacion/
│       ├── ✅ Expr.evalf.md                      # evaluacion numerica de precision arbitraria
│       └── ✅ sympy.lambdify.md                  # Expr -> funcion numpy/python
│
├── 📁 sympy.simplify/
│   ├── 📁 general/
│   │   ├── ✅ sympy.simplify.md
│   │   ├── ✅ sympy.nsimplify.md
│   │   └── ✅ sympy.cancel.md
│   ├── 📁 trig_y_radicales/
│   │   ├── ✅ sympy.trigsimp.md
│   │   ├── ✅ sympy.radsimp.md
│   │   └── ✅ sympy.powsimp.md
│   └── 📁 reescritura/
│       └── ✅ Expr.rewrite.md
│
├── 📁 sympy.polys/
│   ├── ✅ Poly.md
│   ├── 📁 expandir_factorizar/
│   │   ├── ✅ sympy.expand.md
│   │   ├── ✅ sympy.factor.md
│   │   ├── ✅ sympy.collect.md
│   │   ├── ✅ sympy.apart.md
│   │   └── ✅ sympy.together.md
│   └── 📁 operaciones/
│       ├── ✅ sympy.gcd.md
│       ├── ✅ sympy.lcm.md
│       ├── ✅ sympy.div.md
│       ├── ✅ sympy.degree.md
│       └── ✅ sympy.real_roots.md
│
├── 📁 sympy.calculus/
│   ├── 📁 derivadas/
│   │   ├── ✅ sympy.diff.md
│   │   └── ✅ Derivative.md
│   ├── 📁 integrales/
│   │   ├── ✅ sympy.integrate.md
│   │   └── ✅ Integral.md
│   ├── 📁 limites/
│   │   ├── ✅ sympy.limit.md
│   │   └── ✅ Limit.md
│   ├── 📁 series/
│   │   ├── ✅ sympy.series.md
│   │   └── ✅ sympy.fourier_series.md
│   └── 📁 sumatorios/
│       ├── ✅ Sum.md
│       └── ✅ Product.md
│
├── 📁 sympy.solvers/
│   ├── 📁 algebraicas/
│   │   ├── ✅ sympy.solve.md
│   │   ├── ✅ sympy.solveset.md
│   │   ├── ✅ sympy.roots.md
│   │   └── ✅ sympy.nsolve.md
│   ├── 📁 sistemas/
│   │   ├── ✅ sympy.linsolve.md
│   │   └── ✅ sympy.nonlinsolve.md
│   ├── 📁 diferenciales/
│   │   └── ✅ sympy.dsolve.md
│   └── 📁 recurrencias/
│       └── ✅ sympy.rsolve.md
│
├── 📁 sympy.matrices/
│   ├── ✅ Matrix.md
│   ├── 📁 creacion/
│   │   ├── ✅ sympy.eye.md
│   │   ├── ✅ sympy.zeros.md
│   │   ├── ✅ sympy.ones.md
│   │   └── ✅ sympy.diag.md
│   └── 📁 operaciones/
│       ├── ✅ Matrix.det.md
│       ├── ✅ Matrix.inv.md
│       ├── ✅ Matrix.rref.md
│       ├── ✅ Matrix.eigenvals.md
│       ├── ✅ Matrix.eigenvects.md
│       └── ✅ Matrix.nullspace.md
│
├── 📁 sympy.functions/
│   ├── 📁 elementales/
│   │   ├── ✅ sympy.sqrt.md
│   │   ├── ✅ sympy.exp_log.md                   # exp, log
│   │   ├── ✅ sympy.trigonometricas.md           # sin, cos, tan, asin…
│   │   ├── ✅ sympy.hiperbolicas.md              # sinh, cosh, tanh
│   │   └── ✅ Abs.md
│   └── 📁 especiales/
│       ├── ✅ sympy.gamma.md
│       ├── ✅ sympy.factorial_binomial.md
│       ├── ✅ Piecewise.md
│       └── ✅ sympy.Heaviside_DiracDelta.md
│
├── 📁 sympy.sets/
│   ├── ✅ Interval.md
│   ├── ✅ FiniteSet.md
│   ├── ✅ sympy.conjuntos_predefinidos.md        # S.Reals, S.Naturals, S.Integers
│   └── ✅ sympy.operaciones_conjuntos.md         # Union, Intersection, Complement
│
├── 📁 sympy.logic/
│   ├── ✅ sympy.operadores_logicos.md            # And, Or, Not, Implies, Equivalent
│   ├── ✅ sympy.satisfiable.md
│   └── ✅ sympy.simplify_logic.md
│
├── 📁 sympy.assumptions/
│   ├── ✅ sympy.supuestos_simbolos.md            # Symbol(real=True, positive=True…)
│   └── ✅ sympy.ask.md                           # ask(), predicados Q
│
├── 📁 sympy.ntheory/
│   ├── ✅ sympy.isprime.md
│   ├── ✅ sympy.factorint.md
│   ├── ✅ sympy.primerange.md
│   └── ✅ sympy.gcd_entero.md                     # igcd, ilcm
│
├── 📁 sympy.geometry/
│   ├── Point.md
│   ├── Line.md
│   ├── Circle.md
│   └── Polygon.md
│
├── 📁 sympy.stats/
│   ├── sympy.distribuciones.md                # Normal, Die, Bernoulli, Exponential…
│   └── sympy.E_variance_P.md                  # E, variance, P, density
│
├── 📁 sympy.physics.units/
│   ├── sympy.unidades.md                      # Quantity, sistema de unidades
│   └── sympy.convert_to.md
│
└── 📁 sympy.printing/
    ├── ✅ sympy.pprint.md
    ├── ✅ sympy.latex.md
    ├── ✅ sympy.init_printing.md
    └── ✅ sympy.ccode_pycode.md                  # generacion de codigo C/Python
```

---

## 📊 Estado actual de implementación

> Rama **limpia** creada desde el commit de skills (`8e98b49`), sin notas de otras librerías.
> **Roadmap: 90 / ~99 notas redactadas.** Sin marca = pendiente.

| Submódulo | Plan | Estado | Prioridad |
|-----------|:----:|--------|-----------|
| `conceptos_transversales/` | 5 | ✅ **5/5 completo** | 🔴 primero (modelo mental) |
| `sympy.core/` | 12 | ✅ **12/12 completo** | 🔴 base de todo |
| `sympy.simplify/` | 7 | ✅ **7/7 completo** | 🟠 alta |
| `sympy.polys/` | 11 | ✅ **11/11 completo** | 🟠 alta |
| `sympy.calculus/` | 10 | ✅ **10/10 completo** | 🔴 núcleo de ingeniería |
| `sympy.solvers/` | 8 | ✅ **8/8 completo** | 🔴 núcleo de ingeniería |
| `sympy.matrices/` | 11 | ✅ **11/11 completo** | 🟠 alta |
| `sympy.functions/` | 9 | ✅ **9/9 completo** | 🟡 media |
| `sympy.sets/` | 4 | ✅ **4/4 completo** | 🟡 media |
| `sympy.logic/` | 3 | ✅ **3/3 completo** | 🟢 baja |
| `sympy.assumptions/` | 2 | ✅ **2/2 completo** | 🟡 media |
| `sympy.ntheory/` | 4 | ✅ **4/4 completo** | 🟢 baja |
| `sympy.geometry/` | 4 | ⬜ pendiente | 🟢 opcional |
| `sympy.stats/` | 2 | ⬜ pendiente | 🟢 opcional |
| `sympy.physics.units/` | 2 | ⬜ pendiente | 🟢 opcional |
| `sympy.printing/` | 4 | ✅ **4/4 completo** | 🟡 media |
| raíz (`introduccion.md`) | 1 | ⬜ pendiente | 🔴 entrada |
| **Total** | **~99** | **90 creadas** | |

### Orden sugerido de relleno

1. **conceptos_transversales** + `introduccion` — el modelo mental: `Expr`, símbolos, supuestos,
   simbólico vs numérico (`evalf`/`lambdify`).
2. **`sympy.core`** — símbolos, números exactos (`Rational`), sustitución (`subs`), evaluación.
3. **Núcleo de ingeniería**: `sympy.calculus` (`diff`, `integrate`, `limit`, `series`) y
   `sympy.solvers` (`solve`, `solveset`, `dsolve`).
4. **`sympy.polys` + `sympy.simplify`** — expandir/factorizar/simplificar.
5. **`sympy.matrices`** y **`sympy.functions`**.
6. Resto: `sets`, `assumptions`, `printing`, `logic`, `ntheory` y opcionales
   (`geometry`, `stats`, `physics.units`).

### Notas

- SymPy opera sobre **expresiones exactas**: `Rational(1,3)` no es `0.333…`. El puente al mundo
  numérico (NumPy/SciPy) es `lambdify`; enlazar ahí donde aplique (wikilink válido aunque viva en
  otra rama).
- Muchas operaciones son **funciones top-level** (`sympy.solve`) y a la vez **métodos**
  (`expr.subs`, `M.det()`); el árbol prioriza la forma más usada de cada una.
- `solveset` es el reemplazo moderno de `solve` para muchos casos; marcar la relación en las notas.

---

## Notas relacionadas

- [[Estandarizan Directorio Librerias]]
