---
title: sympy.Heaviside_DiracDelta — escalon unitario y delta de Dirac
aliases: [Heaviside, DiracDelta, funcion escalon, delta de Dirac, impulso unitario]
tags: [sympy, api/funcion, functions/especiales]
lib: sympy
mod: sympy.functions
tipo: concepto
draft: false
---

# sympy.Heaviside_DiracDelta — escalon unitario y delta de Dirac

Esta nota agrupa `Heaviside(x)` y `DiracDelta(x)`, las dos **funciones distribucionales** fundamentales de `sympy.functions`. No son funciones ordinarias en el sentido clasico: `DiracDelta` es una **distribucion**, y su sentido matematico solo aparece bajo el signo de integral. SymPy las implementa para calculos simbolicos exactos: integracion con la propiedad de muestreo, derivacion de `Heaviside` hacia `DiracDelta` y composicion con expresiones de `x`. Son indispensables en sistemas de control, procesamiento de senales y EDOs con entradas o condiciones iniciales discontinuas.

La relacion fundamental es: `Heaviside` es la **primitiva** de `DiracDelta`, y `DiracDelta` es la **derivada distribucional** de `Heaviside`.

## Firmas

```python
sympy.Heaviside(x, H0=S.Half) -> Integer | Rational | Expr
sympy.DiracDelta(x, k=0)      -> Expr
```

| Parametro | Descripcion |
|-----------|-------------|
| `x` | Argumento (simbolo o numero) |
| `H0` | Valor en `x=0`; por defecto `1/2` (convencion de Heaviside simetrico) |
| `k` | Orden de la derivada: `DiracDelta(x, 1)` = derivada de la delta |

## Valor de retorno

### Heaviside

| Condicion | Resultado |
|-----------|-----------|
| `x > 0` | `1` |
| `x = 0` | `1/2` (por defecto; configurable con `H0`) |
| `x < 0` | `0` |
| `x` simbolico | `Heaviside(x)` sin evaluar |

### DiracDelta

| Condicion | Resultado |
|-----------|-----------|
| `x != 0` (numerico) | `0` |
| `x = 0` | `DiracDelta(0)` (singularidad; no es un numero) |
| `x` simbolico | `DiracDelta(x)` sin evaluar |

## Casos de uso

### Evaluacion directa de Heaviside

```python
from sympy import Heaviside, Rational

Heaviside(1)    # 1
Heaviside(-1)   # 0
Heaviside(0)    # 1/2     (por defecto: convencion simetrica)

# Cambiar el valor en 0:
Heaviside(0, 1)   # 1     (convencion causal: H(0) = 1)
Heaviside(0, 0)   # 0
```

### Propiedad de muestreo de DiracDelta

La propiedad fundamental: `integrate(DiracDelta(x - a) * f(x), (x, -oo, oo)) == f(a)`.

```python
from sympy import symbols, DiracDelta, integrate, oo, sin, exp

x = symbols("x")

integrate(DiracDelta(x) * (x**2 + 1), (x, -oo, oo))   # 1    (f(0) = 0+1 = 1)
integrate(DiracDelta(x - 2) * x**2, (x, -oo, oo))      # 4    (f(2) = 4)
integrate(DiracDelta(x - 3) * exp(x), (x, -oo, oo))    # exp(3)
integrate(DiracDelta(x - 3) * sin(x), (x, -oo, oo))    # sin(3)
```

### Derivada de Heaviside = DiracDelta

```python
from sympy import symbols, Heaviside, diff

x = symbols("x")
diff(Heaviside(x), x)   # DiracDelta(x)
```

### Heaviside como integral de DiracDelta

```python
from sympy import symbols, Heaviside, integrate, oo

x = symbols("x")
integrate(Heaviside(x), (x, -2, 3))   # 3    (el escalon contribuye solo en [0,3])
integrate(Heaviside(x), (x, -1, 2))   # 2
```

### Modelado de senales discontinuas

```python
from sympy import symbols, Heaviside

t = symbols("t")

# Pulso rectangular: encendido en t=1, apagado en t=3
pulso = Heaviside(t - 1) - Heaviside(t - 3)

pulso.subs(t, 0)   # 0    (antes del pulso)
pulso.subs(t, 2)   # 1    (dentro del pulso)
pulso.subs(t, 4)   # 0    (despues del pulso)
```

### Derivada de orden superior de DiracDelta

`DiracDelta(x, k)` representa la derivada de orden `k` de la delta, util en respuestas impulsivas de orden superior.

```python
from sympy import symbols, DiracDelta, integrate, oo

x = symbols("x")
# DiracDelta(x, 1) = derivada primera de la delta
# Propiedad: integral DiracDelta'(x-a)*f(x) = -f'(a)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `DiracDelta(0)` da resultado numerico | `DiracDelta` en su singularidad no es un numero | Solo tiene sentido bajo una integral |
| Integral de `DiracDelta` no simplifica | Limites de integracion no contienen el punto singular | Verificar que `a` este dentro del intervalo de integracion |
| Olvidar el desplazamiento | `DiracDelta(x)` muestrea en 0; `DiracDelta(x-a)` muestrea en `a` | Usar `DiracDelta(x - a)` para muestrear en `x=a` |
| `Heaviside(0)` = 1/2 inesperado | La convencion simetrica es la predeterminada | Usar `Heaviside(0, 1)` si se quiere la convencion causal |

## Limitaciones

- `DiracDelta` fuera de una integral no tiene valor numerico definido; no usar en expresiones puramente algebraicas.
- Las integrales con `DiracDelta` y limites simbolicos (no numericos) pueden no simplificarse automaticamente.
- `Heaviside` no es diferenciable en el sentido clasico en `x=0`; la derivada distribucion se computa correctamente como `DiracDelta`, pero `lambdify` en ese punto puede producir `nan`.
- En sistemas de control, preferir la transformada de Laplace (`laplace_transform`) junto con `Heaviside` en lugar de trabajar directamente en el dominio del tiempo con `dsolve`.

## Notas relacionadas

- [[Piecewise]]
- [[sympy.functions/especiales/index | especiales]]
- [[sympy.functions/index | sympy.functions]]
