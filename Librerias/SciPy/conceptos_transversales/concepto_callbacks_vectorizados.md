---
title: callbacks y funciones vectorizadas — la funcion que le pasas a SciPy
aliases:
  - callbacks scipy
  - funciones vectorizadas
  - callable scipy
  - args parametro
tags:
  - scipy
  - concepto
  - rendimiento
lib: scipy
tipo: concepto
requiere:
  - concepto_relacion_numpy
  - concepto_objetos_resultado
draft: false
---

# callbacks y funciones vectorizadas — la funcion que le pasas a SciPy

## Definicion fundamental

Las rutinas de SciPy son **funciones de orden superior**: les pasas **otra funcion** de Python (el objetivo a minimizar, el integrando, el lado derecho de una EDO) y SciPy la **llama muchas veces** por dentro. Como esa funcion se evalua en bucle, su firma y su rendimiento determinan que tan rapido y robusto es todo el calculo.

```python
from scipy.optimize import minimize

def objetivo(v):          # SciPy la llamara decenas o cientos de veces
    x, y = v
    return (x - 1)**2 + (y - 2.5)**2

res = minimize(objetivo, x0=[0.0, 0.0])
```

## La firma importa: que espera recibir tu funcion

Cada rutina fija el **contrato** de la funcion que le pasas. Equivocar el orden de los argumentos es un fallo silencioso clasico.

| Rutina | Firma esperada | Devuelve |
|--------|----------------|----------|
| `optimize.minimize` | `f(x)` con `x` vector | escalar |
| `optimize.curve_fit` | `f(x, *params)` | array (modelo) |
| `integrate.quad` | `f(x)` con `x` escalar | escalar |
| `integrate.solve_ivp` | `f(t, y)` — **tiempo primero** | `dy/dt` (array) |
| `integrate.odeint` | `f(y, t)` — **estado primero** | `dy/dt` (array) |

> `solve_ivp` usa `f(t, y)` y `odeint` usa `f(y, t)`: el orden **esta invertido** entre ambas. Es la confusion mas comun al migrar de una a otra.

## Pasar parametros extra: `args` antes que closures

Casi todas estas rutinas aceptan un parametro `args` para inyectar constantes sin ensuciar la firma ni crear closures:

```python
from scipy.integrate import quad

def integrando(x, a, b):
    return a * x + b

# args inyecta (a, b); quad solo varia x
valor, err = quad(integrando, 0, 1, args=(2.0, 5.0))   # ∫ (2x+5) dx en [0,1] = 6.0
```

## La regla central: vectoriza la funcion, no la llames en bucle

La funcion que pasas debe estar escrita con **operaciones de NumPy**, no con bucles Python, porque se evalua una y otra vez. Apoyate en las [[concepto_relacion_numpy|ufuncs de NumPy]] para que cada llamada sea codigo C.

```python
# ❌ lento: bucle Python dentro del integrando/objetivo
def f(v):
    total = 0.0
    for vi in v:
        total += vi**2
    return total

# ✅ rapido: vectorizado con NumPy
def f(v):
    return np.sum(v**2)
```

### Modo vectorizado explicito

Algunas rutinas permiten evaluar **muchos puntos de golpe** pasando un flag, lo que reduce drasticamente el numero de llamadas Python:

| Rutina | Activacion | Efecto |
|--------|-----------|--------|
| `integrate.solve_ivp` | `vectorized=True` | la funcion recibe varias columnas de estado a la vez |
| `integrate.quad_vec` | *(por diseño)* | integra funciones que devuelven arrays |
| `optimize.differential_evolution` | `vectorized=True` | evalua toda la poblacion en una llamada |

## Callbacks de monitoreo

Aparte de la funcion principal, varias rutinas aceptan un `callback` que se ejecuta **en cada iteracion** para inspeccionar o detener el proceso:

```python
def traza(xk):
    print("iterado actual:", xk)

minimize(objetivo, x0=[0, 0], callback=traza)
```

En SciPy reciente, `minimize` invoca el callback con un objeto-resultado intermedio (ver [[concepto_objetos_resultado|objetos resultado]]); lanzar `StopIteration` desde el callback detiene la optimizacion limpiamente.

## Casos que fallan

| Sintoma | Causa | Solucion |
|---------|-------|----------|
| EDO da resultados sin sentido | Firma invertida (`f(y, t)` vs `f(t, y)`) | Ajusta al contrato de `solve_ivp`/`odeint` |
| `curve_fit` no ajusta | El modelo no esta vectorizado en `x` | Devuelve un array con ops de NumPy |
| Todo va muy lento | Bucle Python dentro de la funcion | Vectoriza; considera `vectorized=True` |
| `args` da `TypeError` | Pasaste un escalar, no una tupla | `args=(a,)` para un solo extra |

## Notas relacionadas

- [[concepto_relacion_numpy]]
- [[concepto_objetos_resultado]]
