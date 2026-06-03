---
title: scipy.optimize.minimize — minimizacion multivariable con y sin restricciones
aliases:
  - minimize
  - scipy.optimize.minimize
  - optimizacion multivariable
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

# scipy.optimize.minimize — minimizacion multivariable con y sin restricciones

Minimiza una funcion escalar de **una o mas variables**. Es el punto de entrada general de SciPy para optimizacion local: parte de un punto inicial `x0` y desciende hacia un minimo. Soporta varios algoritmos (con/sin gradiente), cotas por variable (`bounds`) y restricciones de igualdad/desigualdad (`constraints`). Devuelve un objeto-resultado cuyo campo `.x` es el vector solucion.

## Firma

```python
scipy.optimize.minimize(
    fun,                 # callable: f(x, *args) -> float
    x0,                  # array_like, shape (n,): punto inicial (OBLIGATORIO)
    args=(),             # tuple: argumentos extra fijos para fun/jac/hess
    method=None,         # str | None: algoritmo (autoselecciona segun bounds/constraints)
    jac=None,            # callable | bool | str | None: gradiente
    hess=None,           # callable | str | None: hessiano
    bounds=None,         # secuencia de (min, max) por variable, o Bounds
    constraints=(),      # dict | LinearConstraint | NonlinearConstraint | lista de ellos
    tol=None,            # float: tolerancia de terminacion
    callback=None,       # callable: invocada por iteracion
    options=None,        # dict: opciones especificas del metodo (maxiter, disp, ...)
) -> OptimizeResult
```

## Valor de retorno

Devuelve un `OptimizeResult` (Bunch). Campos mas usados:

| Campo | Tipo | Significado |
|-------|------|-------------|
| `x` | `ndarray (n,)` | Vector solucion (el minimo encontrado) |
| `fun` | `float` | Valor de la funcion objetivo en `x` |
| `success` | `bool` | True si el optimizador termino correctamente |
| `status` | `int` | Codigo de terminacion (0 suele ser exito) |
| `message` | `str` | Descripcion legible del motivo de parada |
| `jac` | `ndarray` | Gradiente en `x` (si el metodo lo expone) |
| `nit` | `int` | Numero de iteraciones |
| `nfev` | `int` | Evaluaciones de `fun` |
| `njev` / `nhev` | `int` | Evaluaciones de gradiente / hessiano |

## Formas basicas de llamada

| Objetivo | Llamada | Metodo efectivo |
|----------|---------|-----------------|
| Sin restricciones, sin gradiente | `minimize(f, x0)` | BFGS (autoselecciona) |
| Sin gradiente, robusto | `minimize(f, x0, method='Nelder-Mead')` | simplex Nelder-Mead |
| Con gradiente analitico | `minimize(f, x0, jac=grad)` | BFGS / L-BFGS-B |
| Solo cotas por variable | `minimize(f, x0, bounds=bnds)` | L-BFGS-B (autoselecciona) |
| Con restricciones | `minimize(f, x0, constraints=cons)` | SLSQP (autoselecciona) |
| Restricciones + cotas, gran escala | `minimize(f, x0, bounds=bnds, constraints=cons, method='trust-constr')` | trust-constr |

> Si no se pasa `method`, SciPy elige: BFGS sin restricciones, L-BFGS-B si solo hay `bounds`, SLSQP si hay `constraints`.

## Parametros en detalle

### `x0` (obligatorio)

Punto inicial. Su **longitud define el numero de variables** `n`; `fun` siempre recibe un vector de esa forma.

```python
import numpy as np
from scipy.optimize import minimize

f = lambda x: (x[0] - 1)**2 + (x[1] + 2)**2     # minimo en (1, -2)
res = minimize(f, x0=np.array([0.0, 0.0]))
res.x        # → array([ 1., -2.])
res.fun      # → ~0.0
```

La calidad del minimo local depende de `x0`: `minimize` es **local**, no global. Para optimos globales usar `differential_evolution`, `dual_annealing` o `basinhopping`.

### `method` (algoritmos clave)

| Metodo | Usa gradiente | bounds | constraints | Cuando usarlo |
|--------|---------------|--------|-------------|---------------|
| `Nelder-Mead` | No | si (>=1.7) | no | Funciones ruidosas/no diferenciables, pocas variables |
| `Powell` | No | si | no | Sin gradiente, mas eficiente que Nelder-Mead en algunos casos |
| `CG` | Si | no | no | Gradiente conjugado, problemas medianos |
| `BFGS` | Si | no | no | Default sin restricciones; cuasi-Newton denso |
| `L-BFGS-B` | Si | si | no | Muchas variables + cotas; bajo consumo de memoria |
| `TNC` | Si | si | no | Newton truncado con cotas |
| `SLSQP` | Si | si | igualdad y desigualdad | Restricciones generales, pocas-medianas variables |
| `trust-constr` | Si | si | igualdad y desigualdad | Restricciones a gran escala; admite hessiano |

### `jac` (gradiente)

Acelera y estabiliza los metodos basados en gradiente. Sin `jac`, SciPy aproxima el gradiente por **diferencias finitas** (mas lento, menos preciso).

```python
f    = lambda x: (x[0]-1)**2 + (x[1]+2)**2
grad = lambda x: np.array([2*(x[0]-1), 2*(x[1]+2)])

res = minimize(f, [0, 0], jac=grad, method='BFGS')   # gradiente analitico
res.x        # → array([ 1., -2.])

# jac=True: fun devuelve (valor, gradiente) en una sola llamada
def fg(x):
    return (x[0]-1)**2 + (x[1]+2)**2, np.array([2*(x[0]-1), 2*(x[1]+2)])
res = minimize(fg, [0, 0], jac=True)
```

### `hess` (hessiano)

Solo lo usan metodos de tipo Newton (`trust-constr`, `Newton-CG`, `dogleg`, `trust-ncg`). Acepta callable que devuelve la matriz hessiana, o estrategias de cuasi-Newton (`'2-point'`, `'3-point'`, `BFGS()`, `SR1()`).

### `bounds`

Secuencia de tuplas `(min, max)` por variable; usar `None` para lado no acotado. Tambien admite un objeto `Bounds(lb, ub)`.

```python
# x0 en [0, 10], x1 en [-5, 5]
bnds = [(0, 10), (-5, 5)]
res = minimize(f, [1, 1], bounds=bnds)   # autoselecciona L-BFGS-B
```

### `constraints`

Restricciones de igualdad/desigualdad. Para `SLSQP`, formato **dict**; para `trust-constr`, objetos `LinearConstraint` / `NonlinearConstraint`.

```python
# SLSQP: dict con 'type' ('eq' | 'ineq') y 'fun' (ineq se interpreta como fun(x) >= 0)
cons = [
    {'type': 'eq',   'fun': lambda x: x[0] + x[1] - 1},   # x0 + x1 == 1
    {'type': 'ineq', 'fun': lambda x: x[0]},               # x0 >= 0
]
res = minimize(f, [0.5, 0.5], constraints=cons, method='SLSQP')
```

```python
from scipy.optimize import LinearConstraint, NonlinearConstraint
# trust-constr: lb <= A @ x <= ub
lin = LinearConstraint([[1, 1]], lb=1, ub=1)              # x0 + x1 == 1
nl  = NonlinearConstraint(lambda x: x[0]**2 + x[1]**2, 0, 4)  # dentro del circulo r=2
res = minimize(f, [0.5, 0.5], constraints=[lin, nl], method='trust-constr')
```

## Casos de uso

### Minimo cuadratico simple (sin restricciones)

```python
# Ajuste implicito: minimizar energia 1/2 x^T A x - b^T x  ->  resuelve A x = b
A = np.array([[3.0, 1.0], [1.0, 2.0]])
b = np.array([1.0, 0.0])
E    = lambda x: 0.5 * x @ A @ x - b @ x
grad = lambda x: A @ x - b
res = minimize(E, [0, 0], jac=grad, method='BFGS')
res.x        # → solucion de A x = b
```

### Minimizar con cotas (diseño fisico acotado)

```python
# Minimizar coste(d) de un tubo con diametro entre 0.05 y 0.5 m
coste = lambda d: 1000*d[0]**2 + 50/d[0]          # material + perdida de carga
res = minimize(coste, x0=[0.2], bounds=[(0.05, 0.5)])
res.x, res.fun
```

### Optimizacion con restriccion de igualdad (balance de masa)

```python
# Repartir 100 kg/h entre 2 corrientes minimizando un coste convexo, con suma fija
coste = lambda x: 0.02*x[0]**2 + 0.05*x[1]**2
cons  = [{'type': 'eq', 'fun': lambda x: x[0] + x[1] - 100}]
bnds  = [(0, 100), (0, 100)]
res = minimize(coste, [50, 50], bounds=bnds, constraints=cons, method='SLSQP')
res.x        # reparto optimo que suma 100
```

## Buenas practicas

1. **Comprueba siempre `res.success`** (y `res.message`) antes de usar `res.x`; un valor sin convergencia no es fiable.
2. Proporciona `jac` analitico cuando puedas: mas rapido y robusto que las diferencias finitas.
3. Escala las variables para que tengan magnitudes comparables; mejora drasticamente la convergencia de los metodos basados en gradiente.
4. Elige `method` segun el problema: sin restricciones BFGS, muchas variables + cotas L-BFGS-B, restricciones SLSQP o trust-constr.
5. La funcion objetivo se evalua **muchas veces**: vectorizala con NumPy y evita trabajo redundante dentro de `fun`.
6. Para optimos globales, ejecuta varios `x0` o usa `differential_evolution` / `basinhopping`; `minimize` solo encuentra minimos locales.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `res.success is False`, `x` absurdo | No convergio (mal `x0`, escala, `maxiter` bajo) | Reescalar, mejorar `x0`, subir `options={'maxiter': N}` |
| `ValueError: ... bounds` ignorados | El `method` elegido no soporta `bounds` (p.ej. BFGS) | Usar L-BFGS-B / TNC / SLSQP / trust-constr |
| Restricciones ignoradas | `method` no soporta `constraints` | Usar SLSQP o trust-constr |
| `TypeError: fun() takes 1 arg` | Argumentos extra no pasados via `args` | `minimize(fun, x0, args=(p1, p2))` |
| Convergencia lentisima | Gradiente por diferencias finitas en alta dimension | Pasar `jac` analitico o `jac='2-point'/'3-point'` |
| Desempaquetas el retorno como tupla | `minimize` devuelve un objeto, no una tupla | `res = minimize(...)`; luego `res.x` |

## Limitaciones

- Es un optimizador **local**: el resultado depende de `x0` y no garantiza el optimo global.
- No todos los metodos aceptan `bounds`/`constraints`; combinarlos mal hace que SciPy los ignore o lance error.
- El soporte de `bounds` en `Nelder-Mead` existe solo desde SciPy 1.7.
- Las restricciones tipo `dict` solo las entiende `SLSQP` (y `COBYLA` para desigualdades); `trust-constr` exige objetos `LinearConstraint`/`NonlinearConstraint`.

## Notas relacionadas

- [[concepto_objetos_resultado]]
- [[OptimizeResult]]
- [[scipy.optimize.minimize_scalar]]
- [[scipy.optimize.linprog]]
- [[concepto_callbacks_vectorizados]]
