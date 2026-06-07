---
title: sympy.lambdify — compilar una expresion a funcion numerica rapida
aliases:
  - lambdify
  - sympy.lambdify
tags:
  - sympy
  - api/funcion
  - core/evaluacion
lib: sympy
mod: sympy.utilities
tipo: funcion
retorna: callable
requiere:
  - numpy
  - concepto_evalf_lambdify
draft: false
---

# sympy.lambdify — compilar una expresion a funcion numerica rapida

Convierte una expresion simbolica en una **funcion Python ejecutable** que evalua numeros, no simbolos. Es el **puente a NumPy/SciPy**: traduce `sin`, `exp`, `Matrix`, etc. a las funciones del backend elegido (`"numpy"`, `"math"`, `"mpmath"`) y devuelve un `callable` rapido. A diferencia de [[Expr.evalf]] (un valor por llamada, lento en bucle), una funcion `lambdify` con backend `"numpy"` se **vectoriza** sobre arrays enteros, por lo que es la forma correcta de graficar o simular una expresion sobre miles de puntos. El flujo simbolico → numerico completo esta en [[concepto_evalf_lambdify]].

> [!warning] Seguridad
> `lambdify` genera codigo y lo compila con `eval` interno. **No** pases expresiones provenientes de entrada no confiable: equivale a ejecutar codigo arbitrario.

## Firma

```python
sympy.lambdify(
    args,            # Symbol | secuencia de Symbol: variables de entrada (orden = orden de llamada)
    expr,            # Expr: expresion (o lista/Matrix de Expr) a compilar
    modules=None,    # str | list | dict: backend numerico ("numpy", "math", "mpmath", "sympy")
    dummify=False,   # bool: renombra args no validos como nombres Python
    cse=False,       # bool: factoriza subexpresiones comunes antes de compilar
) -> callable
```

## Valor de retorno

| Aspecto | Detalle |
|---------|---------|
| Tipo | Funcion Python (`callable`) |
| Entrada | Tantos argumentos como simbolos en `args`, en ese orden |
| Salida | `float`/`complex`, o `ndarray` si la entrada es array (backend `"numpy"`) |
| Estado | Sin estado simbolico: ya no entiende `Symbol`, solo numeros |

```python
from sympy import symbols, lambdify
x = symbols("x")
f = lambdify(x, x**2 + 1)
f(3)        # 10        -> ya es un numero, no simbolico
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Una variable, backend NumPy | `lambdify(x, expr, "numpy")` |
| Varias variables (orden fijo) | `lambdify((x, y), expr)` |
| Backend escalar puro | `lambdify(x, expr, "math")` |
| Backend de precision arbitraria | `lambdify(x, expr, "mpmath")` |
| Compilar una lista/Matrix | `lambdify(x, [f1, f2])` |

## Parametros en detalle

### `args`

Simbolo o secuencia de simbolos que seran los **argumentos** de la funcion generada. El **orden importa**: define el orden posicional de llamada.

```python
from sympy import symbols, lambdify
x, y = symbols("x y")
g = lambdify((x, y), x*y + 1)
g(2, 3)     # 7    -> g(x_val, y_val) en ese orden
```

### `expr`

Expresion a compilar. Puede ser una sola `Expr`, o una **lista**/`Matrix` de expresiones; en ese caso la funcion devuelve una lista/array de resultados.

```python
from sympy import symbols, sin, cos, lambdify
t = symbols("t")
traj = lambdify(t, [cos(t), sin(t)])   # devuelve [x(t), y(t)]
traj(0)     # [1.0, 0.0]
```

### `modules` (backend)

Define a que **biblioteca numerica** se traducen las funciones. El mas usado es `"numpy"` por su vectorizacion.

| Backend | Cuando usarlo | Vectoriza arrays |
|---------|---------------|------------------|
| `"numpy"` | graficar/simular sobre arrays (lo habitual) | si |
| `"math"` | un escalar puro, sin dependencia de NumPy | no |
| `"mpmath"` | precision arbitraria controlada | no |
| `"sympy"` | mantener resultado simbolico (raro) | no |

```python
import numpy as np
from sympy import symbols, sin, lambdify
x = symbols("x")

f = lambdify(x, sin(x)/x, "numpy")
xs = np.linspace(0.1, 10, 1000)
f(xs)       # ndarray de 1000 valores en una sola llamada (vectorizado)

g = lambdify(x, sin(x)/x, "math")
g(0.5)      # 0.958851077208406   -> escalar, no acepta arrays
```

## Casos de uso

### Graficar una expresion simbolica

```python
import numpy as np
from sympy import symbols, exp, sin, lambdify
x = symbols("x")
expr = exp(-x/5) * sin(x)

f = lambdify(x, expr, "numpy")
xs = np.linspace(0, 20, 500)
ys = f(xs)                       # listo para plt.plot(xs, ys)
```

### Derivar simbolico y evaluar numerico

El patron tipico: hacer el calculo **exacto** en SymPy y compilar solo al final.

```python
import numpy as np
from sympy import symbols, diff, sin, lambdify
x = symbols("x")
expr = sin(x)**2
d = diff(expr, x)                # 2*sin(x)*cos(x)  -> derivada exacta
df = lambdify(x, d, "numpy")
df(np.array([0.0, np.pi/2]))     # array([0., 0.])  -> evaluada rapido
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `NameError` / funcion sin equivalente | la expresion usa algo que el backend `"numpy"` no tiene | usar `"mpmath"`/`"sympy"` o pasar `modules={"nombre": impl}` |
| `TypeError` al pasar un array | backend `"math"` no vectoriza | usar `modules="numpy"` |
| Resultados en orden equivocado | `args` no coincide con el orden de llamada | fijar y respetar el orden de `args` |
| Pasar simbolos sobrantes o de menos | numero de `args` ≠ argumentos pasados | la firma es exactamente `args` |
| Ejecutar codigo no confiable | `lambdify` usa `eval` interno | nunca compilar expresiones de entrada externa |
| `lambdify` no "ve" un simbolo nuevo | la funcion se compilo antes de cambiar la expresion | recompilar tras modificar la expresion |

## Limitaciones

- La funcion resultante es **puramente numerica**: no acepta `Symbol`, no simplifica ni deriva.
- Algunas funciones especiales no tienen equivalente directo en `"numpy"`; ahi conviene `"mpmath"` o un `modules` personalizado.
- Para **un solo** valor de alta precision basta [[Expr.evalf]]; `lambdify` rinde cuando hay muchas evaluaciones.

## Notas relacionadas

- [[Expr.evalf]]
- [[concepto_evalf_lambdify]]
- [[sympy.core/evaluacion/index | evaluacion]]
