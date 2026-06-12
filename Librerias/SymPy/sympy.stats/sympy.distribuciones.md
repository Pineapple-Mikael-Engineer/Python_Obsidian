---
title: sympy.distribuciones — variables aleatorias simbolicas
aliases:
  - Normal
  - Die
  - Bernoulli
  - distribuciones
tags:
  - sympy
  - api/concepto
  - stats
lib: sympy
mod: sympy.stats
tipo: concepto
draft: false
---

# sympy.distribuciones — variables aleatorias simbolicas

En `sympy.stats` una distribucion de probabilidad **no es un numero ni un array**: es un objeto simbolico que representa una variable aleatoria. `X = Normal("X", mu, sigma)` crea una v.a. normal cuyo nombre interno es `"X"` y cuyos parametros son simbolos SymPy, no flotantes. A partir de ese objeto se obtienen esperanzas, varianzas y probabilidades exactas con [[sympy.E_variance_P]]. El resultado es una `Expr` SymPy que se puede simplificar, derivar o integrar como cualquier otra expresion.

## Como funciona

Cada constructora recibe un **nombre de cadena** (identifica la v.a. en expresiones impresas) y los **parametros de la distribucion** (pueden ser simbolos o numeros). El objeto resultante es una variable aleatoria simbolica que conoce su distribucion; no "sortea" valores hasta que se le pide una muestra con `sample`.

```python
from sympy.stats import Normal, Die, Bernoulli, Exponential, Uniform, E, P, variance, density
from sympy import symbols, oo

mu, sigma = symbols("mu sigma", positive=True)

# v.a. continua con parametros simbolicos
X = Normal("X", mu, sigma)

# v.a. continua con parametros concretos
X0 = Normal("X", 0, 1)

# v.a. discreta
D = Die("D", 6)        # dado de 6 caras
B = Bernoulli("B", 0.3)  # exito con probabilidad 0.3
```

## Distribuciones disponibles

| Constructora | Parametros | Tipo | Soporte |
|---|---|---|---|
| `Normal(name, mu, sigma)` | media, desv. estandar (`sigma > 0`) | continua | `(-oo, oo)` |
| `Exponential(name, rate)` | tasa (`rate > 0`) | continua | `[0, oo)` |
| `Uniform(name, a, b)` | extremos (`a < b`) | continua | `[a, b]` |
| `Die(name, sides)` | numero de caras (entero) | discreta | `{1, ..., sides}` |
| `Bernoulli(name, p)` | probabilidad de exito (`0 <= p <= 1`) | discreta | `{0, 1}` |

## Casos de uso

### Parametros simbolicos — resultado exacto en funcion de ellos

```python
from sympy.stats import Normal, E, variance
from sympy import symbols

mu, sigma = symbols("mu sigma", positive=True)
X = Normal("X", mu, sigma)

E(X)          # mu
variance(X)   # sigma**2
```

### Parametros concretos — resultado exacto (fracciones, erf…)

```python
from sympy.stats import Normal, Die, P, E

X0 = Normal("X", 0, 1)
P(X0 > 0)     # 1/2

D = Die("D", 6)
E(D)          # 7/2
P(D > 4)      # 1/3
```

### Densidad de probabilidad como funcion simbolica

```python
from sympy.stats import Normal, density
from sympy import symbols

t = symbols("t")
X0 = Normal("X", 0, 1)
density(X0)(t)    # sqrt(2)*exp(-t**2/2)/(2*sqrt(pi))
```

## Limitaciones

- Los parametros deben satisfacer las **restricciones de la distribucion** (`sigma > 0`, `rate > 0`, `0 <= p <= 1`); si no, SymPy puede lanzar un error o devolver resultados inesperados. Declarar los simbolos con supuestos (`positive=True`) evita ambiguedad.
- Las distribuciones **continuas** con integrales complejas pueden hacer que `P` o `E` devuelvan expresiones con `Integral` sin evaluar. Encadenar con `.doit()` o `simplify` ayuda.
- `sample` genera un valor numerico aleatorio (no simbolico); no es el flujo principal de `sympy.stats`.
- No cubre todas las distribuciones estadisticas; para las que falten, usar SciPy (`scipy.stats`).

## Notas relacionadas

- [[sympy.E_variance_P]]
- [[sympy.stats/index | sympy.stats]]
