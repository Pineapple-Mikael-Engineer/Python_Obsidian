---
title: objetos resultado — los Bunch que devuelve SciPy (OptimizeResult, etc.)
aliases:
  - objetos resultado
  - OptimizeResult
  - Bunch scipy
  - result object
tags:
  - scipy
  - concepto
  - fundamentos
lib: scipy
tipo: concepto
requiere:
  - concepto_relacion_numpy
draft: false
---

# objetos resultado — los Bunch que devuelve SciPy (OptimizeResult, etc.)

## Definicion fundamental

Muchas rutinas de SciPy **no devuelven el resultado pelado**, sino un **objeto-resultado** tipo *Bunch*: un contenedor que se comporta a la vez como diccionario y como objeto, donde cada dato se accede como **atributo** (`res.x`, `res.success`). Agrupan el resultado principal junto con metadatos del algoritmo (convergencia, iteraciones, mensaje).

```python
from scipy.optimize import minimize

res = minimize(lambda v: (v[0]-3)**2, x0=[0.0])
res.x          # array([3.]) — la solucion
res.success    # True       — ¿convergio?
res.fun        # ~0.0       — valor de la funcion en el optimo
res.nit        # numero de iteraciones
```

## Por que existe

Un algoritmo numerico **puede fallar o converger a medias**. Devolver solo `res.x` ocultaria si ese valor es de fiar. El objeto-resultado obliga a tener a mano la solucion **y** su diagnostico en un unico retorno, sin tuplas largas e ilegibles del tipo `x, success, msg, nit, ... = f()`.

## La regla central: revisa `success` antes de usar `x`

> El campo principal (`x`, `root`, `y`…) **solo es valido si el flag de exito lo es**. Leer la solucion sin mirar la convergencia es el error numero uno.

```python
res = minimize(objetivo, x0)
if not res.success:
    raise RuntimeError(f"No convergio: {res.message}")
usar(res.x)
```

## Doble cara: atributo y diccionario

Un Bunch responde a las dos sintaxis; son el mismo dato:

```python
res.x          # acceso por atributo (preferido, legible)
res["x"]       # acceso por clave (util si la clave es dinamica)
res.keys()     # campos disponibles
print(res)     # repr legible con todos los campos y sus valores
```

## Mapa de los objetos-resultado mas comunes

| Rutina | Objeto | Campo principal | Flag de exito |
|--------|--------|-----------------|---------------|
| `optimize.minimize` | `OptimizeResult` | `x` | `success` |
| `optimize.root` / `fsolve` | `OptimizeResult` | `x` | `success` |
| `optimize.curve_fit` | *(tupla `popt, pcov`)* | `popt` | inspeccionar `pcov` |
| `integrate.solve_ivp` | `OdeResult` | `y`, `t` | `success` |
| `integrate.quad` | *(tupla `valor, error`)* | `valor` | `error` pequeño |
| `stats.ttest_ind` | `TtestResult` | `statistic`, `pvalue` | — |
| `stats.linregress` | `LinregressResult` | `slope`, `intercept`, `rvalue` | — |

> No todo en SciPy es un Bunch: `curve_fit` y `quad` devuelven **tuplas**. La regla "revisa el diagnostico" sigue aplicando (ahi es `pcov` o el error estimado).

## Casos que fallan

| Sintoma | Causa | Solucion |
|---------|-------|----------|
| Usas `res.x` y los numeros son absurdos | No convergio; `res.success is False` | Comprueba `success`/`message`, ajusta `x0`/`method` |
| `res[0]` falla en un OptimizeResult | No es una tupla, es un Bunch | Accede por nombre: `res.x` |
| Desempaquetas `x, ok = minimize(...)` | `minimize` devuelve **un** objeto, no una tupla | `res = minimize(...)`, luego `res.x` |
| No sabes que campos hay | Cada rutina expone campos distintos | `print(res)` o `res.keys()` |

## Notas relacionadas

- [[concepto_relacion_numpy]]
- [[OptimizeResult]]
- [[concepto_callbacks_vectorizados]]
