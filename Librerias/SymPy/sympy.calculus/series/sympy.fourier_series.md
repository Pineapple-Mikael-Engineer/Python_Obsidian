---
title: sympy.fourier_series — desarrollo en serie de Fourier de una funcion periodica
aliases:
  - fourier_series
  - sympy.fourier_series
  - serie de Fourier
tags:
  - sympy
  - api/funcion
  - calculus/series
lib: sympy
mod: sympy.series
tipo: funcion
retorna: FourierSeries
draft: false
---

# sympy.fourier_series — desarrollo en serie de Fourier de una funcion periodica

Calcula la **serie de Fourier** de una expresion sobre un intervalo `(x, a, b)`, que se interpreta como un periodo. Devuelve un objeto `FourierSeries` que representa la suma **infinita** de senos y cosenos de forma perezosa: no se evalua entera, sino que se accede a sus terminos o se trunca con `.truncate(n)`. A diferencia de [[sympy.series]] (Taylor local, potencias de `x`), aqui la base son armonicos `sin(n*x)`, `cos(n*x)` y la aproximacion es **global** sobre todo el periodo. Es la herramienta para descomponer señales periodicas: ondas cuadradas, dientes de sierra, rectificaciones.

> [!info] Exactitud simbolica
> Los coeficientes son **exactos** (`4/pi`, `2/3`, ...), no flotantes. El objeto guarda las formulas de los coeficientes `an`/`bn` como sucesiones simbolicas y solo materializa terminos cuando se truncan o se indexan.

## Firma

```python
sympy.fourier_series(
    f,            # Expr: funcion a desarrollar (el periodo es el intervalo dado)
    limits=None,  # (x, a, b): variable y extremos del periodo (por defecto (x, -pi, pi))
) -> FourierSeries
```

## Valor de retorno

| Aspecto | Detalle |
|---------|---------|
| Tipo | `FourierSeries` (suma simbolica perezosa) |
| `.a0` | termino constante (media sobre el periodo) |
| `.an` / `.bn` | `SeqFormula`: formulas de los coeficientes de coseno/seno |
| Indexacion `s[k]` | k-esimo termino ya materializado (`s[0]` es el termino constante) |
| `.truncate(n)` | suma de los primeros `n` terminos no nulos, como `Expr` |

```python
from sympy import symbols, fourier_series, pi
x = symbols("x")
s = fourier_series(x, (x, -pi, pi))
s.truncate(3)    # 2*sin(x) - sin(2*x) + 2*sin(3*x)/3
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Sobre `[-pi, pi]` (por defecto) | `fourier_series(f, (x, -pi, pi))` |
| Sobre otro periodo | `fourier_series(f, (x, a, b))` |
| Truncar a `n` terminos | `fourier_series(f, (x, -pi, pi)).truncate(n)` |
| Termino constante (media) | `s.a0` |
| k-esimo termino | `s[k]` |
| Coeficientes simbolicos | `s.an`, `s.bn` |

## Parametros en detalle

### `f`

Expresion periodica a desarrollar. Puede ser una expresion suave (`x`, `x**2`) o definida a trozos con `Piecewise` (tipico para onda cuadrada o rectificacion). La simetria de `f` determina que coeficientes se anulan: funcion **impar** → solo senos (`an = 0`); funcion **par** → solo cosenos (`bn = 0`).

```python
from sympy import symbols, fourier_series, pi, Piecewise
x = symbols("x")

# Diente de sierra f(x) = x (impar): solo senos
fourier_series(x, (x, -pi, pi)).truncate(4)
# 2*sin(x) - sin(2*x) + 2*sin(3*x)/3 - sin(4*x)/2

# Onda cuadrada (impar): solo armonicos impares de seno
onda = Piecewise((-1, x < 0), (1, x >= 0))
fourier_series(onda, (x, -pi, pi)).truncate(3)
# 4*sin(x)/pi + 4*sin(3*x)/(3*pi) + 4*sin(5*x)/(5*pi)
```

### `limits`

Tupla `(x, a, b)` con la variable y los extremos del **periodo**. Por defecto `(x, -pi, pi)`. Cambiar `(a, b)` cambia la frecuencia base de los armonicos. Para una funcion **par** aparecen cosenos y el termino constante:

```python
from sympy import symbols, fourier_series, pi
x = symbols("x")
fourier_series(x**2, (x, -pi, pi)).truncate(3)
# -4*cos(x) + cos(2*x) + pi**2/3   -> par: cosenos + termino constante pi**2/3
```

## Acceder a terminos y truncar

El objeto es infinito; se materializa de dos maneras. **`.truncate(n)`** suma los primeros `n` terminos **no nulos** y devuelve una `Expr` lista para graficar o evaluar. **Indexar** `s[k]` devuelve un termino concreto (`s[0]` es el termino constante `a0`).

```python
from sympy import symbols, fourier_series, pi
x = symbols("x")
s = fourier_series(x, (x, -pi, pi))

s.truncate(2)    # 2*sin(x) - sin(2*x)
s.a0             # 0          -> media nula (funcion impar)
s[0]             # 0          -> termino constante
s[1]             # 2*sin(x)   -> primer armonico no nulo
```

## Casos de uso

### Aproximar una onda cuadrada y graficarla

```python
import numpy as np
from sympy import symbols, fourier_series, pi, Piecewise, lambdify
x = symbols("x")

onda = Piecewise((-1, x < 0), (1, x >= 0))
aprox = fourier_series(onda, (x, -pi, pi)).truncate(5)   # suma de 5 armonicos
f = lambdify(x, aprox, "numpy")
xs = np.linspace(-pi, pi, 400)
ys = f(xs)                                                # listo para plt.plot(xs, ys)
```

### Inspeccionar la energia por armonico

```python
from sympy import symbols, fourier_series, pi
x = symbols("x")
s = fourier_series(x, (x, -pi, pi))
[s[k] for k in range(1, 4)]    # [2*sin(x), -sin(2*x), 2*sin(3*x)/3]
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Intentar evaluar el objeto entero | `FourierSeries` es una suma infinita perezosa | usar `.truncate(n)` para obtener una `Expr` |
| `truncate(n)` da menos terminos de lo esperado | cuenta terminos **no nulos**, no indices | subir `n`; los nulos no consumen cupo |
| Esperar cosenos en funcion impar | una funcion impar tiene `an = 0` | es correcto: solo apareceran senos |
| Periodo equivocado en la grafica | `limits` define el periodo | hacer coincidir `(a, b)` con el dominio fisico |
| Indexar esperando el armonico n en `s[n]` | `s[0]` es el termino constante | el k-esimo armonico no nulo se obtiene recorriendo `s[k]` |

## Limitaciones

- Devuelve una representacion **simbolica perezosa**; para numeros hay que truncar y compilar con [[sympy.lambdify]].
- En discontinuidades la serie exhibe el **fenomeno de Gibbs** (sobreoscilacion) por mas terminos que se sumen.
- El intervalo `(a, b)` debe ser un periodo completo; fuera de el la serie repite periodicamente, no extrapola la formula original.

## Notas relacionadas

- [[sympy.series]]
- [[sympy.lambdify]]
- [[sympy.calculus/series/index | series]]
