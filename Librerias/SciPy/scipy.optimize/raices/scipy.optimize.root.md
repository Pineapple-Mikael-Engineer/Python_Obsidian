---
title: root — raices de sistemas no lineales (interfaz moderna)
aliases:
  - root
  - scipy root
  - raices sistema
tags:
  - scipy
  - api/funcion
  - optimize/raices
lib: scipy
tipo: funcion
mod: scipy.optimize
retorna: OptimizeResult
requiere:
  - concepto_objetos_resultado
  - concepto_callbacks_vectorizados
draft: false
---

# root — raices de sistemas no lineales

Interfaz **moderna y unificada** para encontrar raices de **sistemas** de ecuaciones no lineales: resuelve `fun(x) = 0` donde `x` es un vector. Reemplaza a la interfaz antigua `fsolve` exponiendo varios metodos bajo una sola firma y devolviendo siempre un objeto-resultado.

## Firma

```python
scipy.optimize.root(fun, x0, args=(), method='hybr', jac=None,
                    tol=None, callback=None, options=None)
```

## Valor de retorno

Devuelve un objeto tipo [[OptimizeResult]] con los atributos clave:

| Atributo | Tipo | Significado |
|----------|------|-------------|
| `.x` | `ndarray` | Vector solucion (la raiz hallada) |
| `.success` | `bool` | `True` si convergio |
| `.fun` | `ndarray` | Valor de `fun(x)` en la solucion (~0) |
| `.message` | `str` | Descripcion del estado de salida |
| `.nfev` | `int` | Numero de evaluaciones de `fun` |
| `.status` | `int` | Codigo de salida del solver |

## Formas basicas de llamada

```python
import numpy as np
from scipy.optimize import root

# Sistema 2x2: x0*cos(x1)=4 ; x0*x1 - x1 = 5
def sistema(v):
    x0, x1 = v
    return [x0 * np.cos(x1) - 4,
            x0 * x1 - x1 - 5]

sol = root(sistema, x0=[1.0, 1.0])
sol.x        # → array([6.50409711, 0.90841421])
sol.success  # → True
```

## Parametros en detalle

### fun

`callable` que recibe el vector `x` y devuelve un array de **residuos** del mismo tamaño que `x`. Se evalua **muchas veces**, por lo que conviene escribirla con operaciones de NumPy (ver [[concepto_callbacks_vectorizados]]). El sistema esta resuelto cuando todos los residuos son ~0.

### x0

`ndarray` con la **semilla inicial**. Su longitud fija la dimension del sistema. Una mala semilla puede llevar a no convergencia o a una raiz distinta de la deseada.

### method

Selecciona el algoritmo. Cada metodo tiene compromisos distintos:

| method | Algoritmo | Cuando usarlo |
|--------|-----------|---------------|
| `'hybr'` | Powell hibrido (MINPACK) | **Default**; sistemas pequeños-medianos, robusto |
| `'lm'` | Levenberg-Marquardt | Sistemas sobre/sub-determinados, minimos cuadrados |
| `'broyden1'` | Cuasi-Newton (buena Jacobiana inversa) | Jacobiana cara de calcular |
| `'broyden2'` | Cuasi-Newton (formula de Sherman-Morrison) | Variante de broyden1 |
| `'krylov'` | Newton-Krylov (sin Jacobiana densa) | **Sistemas grandes** y dispersos |
| `'anderson'` | Mezcla de Anderson | Iteraciones de punto fijo |
| `'df-sane'` | Spectral residual sin Jacobiana | Grande, libre de derivadas |

### jac

Jacobiana de `fun`. Puede ser `callable` que devuelve la matriz, o `True` (entonces `fun` debe devolver `(residuos, jacobiana)`). Si es `None`, se estima por diferencias finitas. Aportar la Jacobiana acelera y estabiliza la convergencia.

### tol

Tolerancia de terminacion. Para control fino se prefiere pasar tolerancias especificas dentro de `options` (cada metodo expone las suyas, p. ej. `xtol`, `ftol`, `maxiter`).

### callback

`callable(x, f)` (la firma depende del metodo) invocado en cada iteracion para monitorear el progreso.

### options

`dict` con opciones especificas del metodo elegido (`maxiter`, `xtol`, `fatol`, etc.).

## Casos de uso

### Con Jacobiana analitica

```python
def f(v):
    x, y = v
    return [x + 0.5 * (x - y)**3 - 1.0,
            0.5 * (y - x)**3 + y]

def jac(v):
    x, y = v
    return np.array([[1 + 1.5*(x-y)**2, -1.5*(x-y)**2],
                     [-1.5*(y-x)**2,    1 + 1.5*(y-x)**2]])

sol = root(f, [0, 0], jac=jac, method='hybr')
sol.x   # → array([0.8411639, 0.1588361])
```

### Sistema grande con Krylov

```python
# Para N grande, 'krylov' evita formar la Jacobiana densa NxN
sol = root(f_grande, x0=np.zeros(10000), method='krylov')
```

### Inyectar parametros con args

```python
def f(v, a):
    return [v[0]**2 - a, v[1] - v[0]]

root(f, [1.0, 1.0], args=(2.0,)).x   # → array([1.41421356, 1.41421356])
```

## Buenas practicas

- Verifica **siempre** `sol.success` antes de usar `sol.x`; un resultado no convergido es basura.
- Proporciona `jac` cuando sea factible: menos evaluaciones y mejor estabilidad.
- Para sistemas grandes/dispersos usa `'krylov'` o `'df-sane'` en lugar de `'hybr'`.
- Escala las variables a magnitudes comparables para que la Jacobiana este bien condicionada.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `sol.success == False` | Mala semilla o sistema mal escalado | Cambia `x0`, escala variables, prueba otro `method` |
| `TypeError: ... arguments` | `fun` no acepta el numero de args | Usa `args=(...)` para parametros extra |
| Residuos no llegan a 0 | `fun` devuelve tamaño distinto de `x` | Asegura `len(fun(x)) == len(x)` |
| Convergencia lentisima | Jacobiana por diferencias finitas cara | Aporta `jac` analitica |

## Limitaciones

- Encuentra **una** raiz cercana a `x0`; no es un solver global ni enumera todas las raices.
- `'hybr'` y `'lm'` no escalan bien a dimension muy alta (Jacobiana densa).
- No garantiza convergencia desde cualquier semilla.

## Notas relacionadas

- [[OptimizeResult]]
- [[scipy.optimize.fsolve]]
- [[concepto_callbacks_vectorizados]]
