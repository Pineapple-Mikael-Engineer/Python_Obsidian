---
title: scipy.optimize.linprog — programacion lineal (minimizacion sujeta a restricciones lineales)
aliases:
  - linprog
  - scipy.optimize.linprog
  - programacion lineal
tags:
  - scipy
  - api/funcion
  - optimizacion
lib: scipy
tipo: funcion
mod: scipy.optimize
retorna: OptimizeResult
requiere:
  - numpy
  - concepto_objetos_resultado
draft: false
---

# scipy.optimize.linprog — programacion lineal (minimizacion sujeta a restricciones lineales)

Resuelve problemas de **programacion lineal**: minimiza una funcion lineal `c·x` sujeta a desigualdades lineales (`A_ub·x <= b_ub`), igualdades lineales (`A_eq·x = b_eq`) y cotas por variable (`bounds`). Todo es lineal: objetivo y restricciones. Devuelve un objeto-resultado con el vector optimo en `.x`.

Forma canonica que resuelve:

```text
min  c · x
s.a. A_ub · x <= b_ub
     A_eq · x  = b_eq
     lb <= x <= ub        (por variable, via bounds)
```

## Firma

```python
scipy.optimize.linprog(
    c,                  # array_like (n,): coeficientes del objetivo a MINIMIZAR
    A_ub=None,          # array_like (m_ub, n): matriz de desigualdades
    b_ub=None,          # array_like (m_ub,): lado derecho de A_ub @ x <= b_ub
    A_eq=None,          # array_like (m_eq, n): matriz de igualdades
    b_eq=None,          # array_like (m_eq,): lado derecho de A_eq @ x == b_eq
    bounds=None,        # (min, max) por variable; default (0, None) -> x >= 0
    method='highs',     # str: 'highs' (default moderno) | 'highs-ds' | 'highs-ipm'
    callback=None,      # callable
    options=None,       # dict: opciones del solver
    x0=None,            # array_like: punto inicial (solo algunos metodos)
    integrality=None,   # array_like: 0=continua, 1=entera (MIP con HiGHS)
) -> OptimizeResult
```

## Valor de retorno

Devuelve un `OptimizeResult` (Bunch). Campos relevantes:

| Campo | Tipo | Significado |
|-------|------|-------------|
| `x` | `ndarray (n,)` | Vector solucion optimo |
| `fun` | `float` | Valor optimo de `c · x` |
| `success` | `bool` | True si encontro solucion optima |
| `status` | `int` | 0 optimo · 1 limite iter · 2 infactible · 3 no acotado · 4 error |
| `message` | `str` | Descripcion del estado |
| `slack` | `ndarray` | Holgura de las desigualdades: `b_ub - A_ub @ x` |
| `con` | `ndarray` | Residuo de las igualdades: `b_eq - A_eq @ x` |
| `nit` | `int` | Numero de iteraciones |

## Formas basicas de llamada

| Problema | Llamada |
|----------|---------|
| Solo desigualdades | `linprog(c, A_ub=A, b_ub=b)` |
| Solo igualdades | `linprog(c, A_eq=A, b_eq=b)` |
| Cotas por variable | `linprog(c, bounds=[(0, 5), (0, None)])` |
| Completo | `linprog(c, A_ub, b_ub, A_eq, b_eq, bounds=bnds)` |
| Maximizacion | `linprog(-c, ...)` y negar `res.fun` |
| Variables enteras (MIP) | `linprog(c, ..., integrality=1)` |

## Parametros en detalle

### `c` y la convencion de minimizar

`linprog` **siempre minimiza**. Para **maximizar** `c·x`, minimiza `-c·x` y luego niega el valor optimo:

```python
import numpy as np
from scipy.optimize import linprog

# maximizar  3 x0 + 2 x1   ->   minimizar  -3 x0 - 2 x1
c = [-3, -2]
res = linprog(c, A_ub=[[1, 1]], b_ub=[4], bounds=[(0, None), (0, None)])
optimo = -res.fun        # volver al signo original del objetivo
```

### `A_ub`, `b_ub` (desigualdades)

Toda desigualdad debe escribirse como `<=`. Una `>=` se convierte multiplicando por `-1`:

```text
2 x0 + x1 >= 10   ->   -2 x0 - x1 <= -10
```

### `A_eq`, `b_eq` (igualdades)

Restricciones de igualdad exacta `A_eq @ x == b_eq`, p.ej. balances de masa o suma fija de recursos.

### `bounds`

Lista de `(min, max)` por variable; `None` = sin cota por ese lado. **Default `(0, None)`**: si no se pasa `bounds`, todas las variables son `>= 0`. Para permitir negativos hay que indicarlo explicitamente.

```python
bounds = [(0, 10), (None, None), (5, None)]   # x0 in [0,10], x1 libre, x2 >= 5
```

### `method`

| Metodo | Estado | Notas |
|--------|--------|-------|
| `highs` | **recomendado** (default desde SciPy 1.6) | Elige automaticamente entre dual simplex e interior-point (HiGHS) |
| `highs-ds` | activo | Fuerza dual simplex de HiGHS |
| `highs-ipm` | activo | Fuerza interior-point de HiGHS |
| `simplex` | **deprecado / eliminado** | Antiguo, lento; sustituido por HiGHS |
| `interior-point` | **deprecado / eliminado** | Implementacion legacy de SciPy |
| `revised simplex` | **deprecado / eliminado** | Legacy |

> Usa siempre `'highs'` (o no pases `method`): los metodos antiguos estan deprecados desde 1.9 y eliminados en versiones recientes. Solo HiGHS soporta `integrality` (MILP).

## Casos de uso

### Asignacion de recursos / mezcla (maximizar beneficio)

```python
import numpy as np
from scipy.optimize import linprog

# Una planta fabrica 2 productos. Beneficio: 40 x0 + 30 x1 (maximizar).
# Recursos limitados:
#   horas maquina:   2 x0 + 1 x1 <= 100
#   materia prima:   1 x0 + 1 x1 <=  80
#   x >= 0
c     = [-40, -30]                  # negado para maximizar
A_ub  = [[2, 1],
         [1, 1]]
b_ub  = [100, 80]
res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None), (0, None)], method='highs')

res.x            # → unidades optimas de cada producto, p.ej. array([20., 60.])
-res.fun         # → beneficio maximo
res.slack        # holgura de cada recurso (0 => recurso saturado)
res.success      # → True
```

### Problema de dieta / coste minimo con igualdad

```python
# Minimizar coste de mezclar 3 ingredientes cumpliendo:
#   masa total exacta = 100 kg            (igualdad)
#   proteina aportada >= 25 kg            (desigualdad >= -> negar)
coste  = [2.0, 3.5, 1.2]                  # $/kg de cada ingrediente
A_eq   = [[1, 1, 1]]; b_eq = [100]        # suma de masas == 100
A_ub   = [[-0.3, -0.5, -0.1]]; b_ub = [-25]  # 0.3 x0 + 0.5 x1 + 0.1 x2 >= 25
bounds = [(0, None)] * 3
res = linprog(coste, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
res.x, res.fun
```

## Buenas practicas

1. Comprueba `res.success` y `res.status` antes de usar `res.x`: `status=2` (infactible) o `3` (no acotado) significan que no hay solucion utilizable.
2. Usa `method='highs'` (o no especifiques `method`); evita los solvers legacy deprecados.
3. Para **maximizar**, niega `c` y recuerda negar tambien `res.fun` al interpretar el optimo.
4. Convierte toda `>=` en `<=` multiplicando la fila por `-1` (incluido su `b`).
5. Recuerda el default `bounds=(0, None)`: declara explicitamente las variables que puedan ser negativas o libres.
6. Inspecciona `res.slack` para ver que restricciones quedan saturadas (cuellos de botella) y `res.con` para verificar las igualdades.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `res.status == 2` (infactible) | Restricciones contradictorias | Revisar signos, `bounds` y consistencia de igualdades |
| `res.status == 3` (no acotado) | Falta acotar el objetivo en la direccion de mejora | Añadir restricciones/`bounds` que limiten `x` |
| Solucion "maximiza al reves" | `linprog` minimiza; no se nego `c` | Pasar `-c` y negar `res.fun` |
| Variables salen 0 inesperadamente | Default `bounds=(0, None)` impide negativos | Pasar `bounds=[(None, None), ...]` |
| Restriccion `>=` no se cumple | No se convirtio a `<=` | Multiplicar fila y `b` por `-1` |
| `ValueError` de dimensiones | `A_ub`/`A_eq` no encajan con longitud de `c` | Cada fila debe tener `n` columnas (= len(c)) |
| Warning de metodo deprecado | `method='simplex'`/`'interior-point'` | Cambiar a `'highs'` |

## Limitaciones

- Solo problemas **lineales**: objetivo y restricciones deben ser lineales (si no, usar `minimize` con SLSQP/trust-constr o `differential_evolution`).
- Encuentra optimos **globales** del LP (la region factible es convexa), pero no resuelve no-linealidades.
- El soporte de variables enteras (`integrality`, MILP) existe solo con `method='highs'`.
- Los metodos `simplex`, `interior-point` y `revised simplex` estan deprecados (1.9) y eliminados en versiones posteriores.

## Notas relacionadas

- [[scipy.optimize.minimize]]
- [[concepto_objetos_resultado]]
- [[OptimizeResult]]
