---
title: scipy.optimize.minimize_scalar — minimizacion de una variable escalar
aliases:
  - minimize_scalar
  - scipy.optimize.minimize_scalar
  - optimizacion escalar
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

# scipy.optimize.minimize_scalar — minimizacion de una variable escalar

Minimiza una funcion de **una sola variable** `f(x) -> float` con `x` escalar. Es la contraparte univariable de `minimize`: aqui no hay vector `x0`, sino un intervalo de busqueda (`bracket`) o cotas (`bounds`). Devuelve un objeto-resultado cuyo `.x` es un **escalar**, no un array.

## Firma

```python
scipy.optimize.minimize_scalar(
    fun,             # callable: f(x, *args) -> float, con x escalar
    bracket=None,    # tuple: (a, b) o (a, b, c) que encierra el minimo (brent/golden)
    bounds=None,     # tuple (a, b): intervalo cerrado (OBLIGATORIO para method='bounded')
    args=(),         # tuple: argumentos extra fijos
    method=None,     # str: 'brent' (default) | 'golden' | 'bounded'
    tol=None,        # float: tolerancia de terminacion
    options=None,    # dict: opciones del metodo (maxiter, xatol, ...)
) -> OptimizeResult
```

## Valor de retorno

Devuelve un `OptimizeResult` (Bunch). Campos relevantes:

| Campo | Tipo | Significado |
|-------|------|-------------|
| `x` | `float` | Punto que minimiza (escalar, no array) |
| `fun` | `float` | Valor minimo de la funcion |
| `success` | `bool` | True si convergio |
| `status` | `int` | Codigo de terminacion |
| `message` | `str` | Motivo de la parada |
| `nit` | `int` | Numero de iteraciones |
| `nfev` | `int` | Evaluaciones de `fun` |

## Formas basicas de llamada

| Situacion | Llamada | Metodo |
|-----------|---------|--------|
| Funcion unimodal, sin acotar | `minimize_scalar(f)` | brent (default) |
| Con bracket conocido | `minimize_scalar(f, bracket=(a, b))` | brent |
| Variante de seccion aurea | `minimize_scalar(f, method='golden')` | golden |
| Minimo dentro de [a, b] estricto | `minimize_scalar(f, bounds=(a, b), method='bounded')` | bounded |

## Parametros en detalle

### `method`

| Metodo | Requiere | Garantia | Uso tipico |
|--------|----------|----------|------------|
| `brent` | nada / `bracket` | rapido, parabolic + golden | Default; funcion unimodal sin cota dura |
| `golden` | nada / `bracket` | seccion aurea, robusto y lento | Funciones poco suaves |
| `bounded` | `bounds=(a, b)` | minimo **restringido** a `[a, b]` | Hay limites fisicos en la variable |

> `'bounded'` es el unico que respeta un intervalo cerrado: si el minimo real cae fuera de `[a, b]`, devuelve el extremo. `'brent'`/`'golden'` pueden salirse del `bracket` inicial.

### `bracket`

Para `brent`/`golden`. Dos formas:
- `(a, b)`: par inicial; SciPy busca un bracket valido a partir de el.
- `(a, b, c)`: triplete con `f(b) < f(a)` y `f(b) < f(c)` (encierra un minimo).

### `bounds`

Obligatorio con `method='bounded'`. Tupla `(a, b)` con `a < b`. La busqueda nunca sale de ese intervalo.

## Casos de uso

### Minimo simple sin cotas

```python
from scipy.optimize import minimize_scalar

f = lambda x: (x - 3)**2 + 1
res = minimize_scalar(f)
res.x        # → ~3.0
res.fun      # → ~1.0
```

### Minimo acotado (variable con limite fisico)

```python
import numpy as np
# Minimizar coste(v) de operacion en velocidad fisica v in [1, 10] m/s
coste = lambda v: 2*v**2 + 80/v
res = minimize_scalar(coste, bounds=(1, 10), method='bounded')
res.x        # velocidad optima dentro de [1, 10]
res.fun      # coste minimo
```

### Con argumentos extra fijos

```python
# f(x; a) = (x - a)**2 ; el parametro a entra por args
f = lambda x, a: (x - a)**2
res = minimize_scalar(f, args=(5.0,), bounds=(0, 10), method='bounded')
res.x        # → ~5.0
```

## Contraste con minimize

| Aspecto | `minimize_scalar` | `minimize` |
|---------|-------------------|------------|
| Variables | **una** (escalar) | una o **varias** (vector) |
| Punto inicial | no usa `x0` | `x0` obligatorio |
| Region de busqueda | `bracket` o `bounds=(a,b)` | `bounds` por variable + `constraints` |
| `res.x` | `float` | `ndarray (n,)` |
| Gradiente | no aplica | `jac` opcional |
| Restricciones generales | no | si (SLSQP, trust-constr) |

> Regla practica: si la incognita es **un solo numero**, usa `minimize_scalar`; en cuanto haya dos o mas variables, o restricciones, usa `minimize`.

## Buenas practicas

1. Revisa `res.success` antes de leer `res.x`, igual que en cualquier rutina de optimizacion.
2. Si la variable tiene limites fisicos reales, usa `method='bounded'` con `bounds`: es el unico que los respeta.
3. Asegurate de que la funcion sea aproximadamente **unimodal** en la region; `brent`/`golden` asumen un solo minimo.
4. Para funciones ruidosas o con kinks, prefiere `'golden'` (mas robusto, aunque mas lento).
5. Pasa parametros fijos por `args`, no por closures globales, para mantener la funcion pura.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ValueError: bounds required` | `method='bounded'` sin `bounds` | Pasar `bounds=(a, b)` con `a < b` |
| `res.x` no es el minimo global | Funcion multimodal; cayo en otro valle | Acotar con `bounds`+`bounded` o probar varios `bracket` |
| `res.x` es un array | Se uso `minimize` por error | Usar `minimize_scalar` para una variable |
| Resultado en el borde de `[a,b]` | El minimo real esta fuera del intervalo | Ampliar `bounds` si fisicamente es valido |
| `TypeError` por argumento faltante | Parametros extra no pasados | Usar `args=(...)` |

## Limitaciones

- Solo **una variable**: para problemas multivariable hay que usar `minimize`.
- Asume unimodalidad en la region; no garantiza minimo global si hay varios valles.
- No acepta restricciones generales ni gradientes; el control es solo `bracket`/`bounds`.
- Solo `'bounded'` respeta un intervalo cerrado; los otros dos pueden evaluar fuera del `bracket`.

## Notas relacionadas

- [[scipy.optimize.minimize]]
- [[concepto_objetos_resultado]]
- [[OptimizeResult]]
