---
title: scipy.integrate.dblquad — integral doble de una funcion callable sobre region variable
aliases:
  - dblquad
  - scipy.integrate.dblquad
  - integral doble
tags:
  - scipy
  - api/funcion
  - integracion
lib: scipy
tipo: funcion
mod: scipy.integrate
retorna: tuple (float, float)
requiere:
  - numpy
  - scipy.integrate.quad
draft: false
---

# scipy.integrate.dblquad — integral doble de una funcion callable sobre region variable

Calcula la integral doble de una **funcion callable** `func(y, x)` sobre una region donde `x` varia entre constantes `a` y `b`, e `y` varia entre dos funciones `gfun(x)` y `hfun(x)` (los limites internos pueden depender de `x`). Internamente aplica `quad` anidado por cuadratura adaptativa. Devuelve una **tupla** `(valor, error_absoluto_estimado)`.

> Trampa critica del **orden de argumentos**: `func` recibe `func(y, x)` con la variable **interna `y` PRIMERO** y la externa `x` despues. Es lo contrario al orden de lectura matematico habitual y la fuente de error mas comun con esta funcion.

## Firma

```python
scipy.integrate.dblquad(
    func,             # callable: func(y, x, *args) -> float   (y interna PRIMERO)
    a,                # float: limite inferior de x (constante)
    b,                # float: limite superior de x (constante)
    gfun,             # callable(x) -> float | float: limite inferior de y
    hfun,             # callable(x) -> float | float: limite superior de y
    args=(),          # tuple: argumentos extra fijos para func
    epsabs=1.49e-8,   # float: tolerancia de error absoluto
    epsrel=1.49e-8,   # float: tolerancia de error relativo
) -> tuple
```

La integral evaluada es:

```text
∫_a^b ∫_{gfun(x)}^{hfun(x)} func(y, x) dy dx
```

## Valor de retorno

| Posicion | Tipo | Significado |
|----------|------|-------------|
| `[0]` | `float` | Valor estimado de la integral doble |
| `[1]` | `float` | Cota superior del error absoluto |

```python
valor, error = dblquad(func, a, b, gfun, hfun)
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Region rectangular | `dblquad(f, a, b, c, d)` con `c, d` constantes |
| Region con limites de y variables | `dblquad(f, a, b, lambda x: g(x), lambda x: h(x))` |
| Con parametros extra | `dblquad(f, a, b, g, h, args=(k,))` |

## Parametros en detalle

### `func` (obligatorio)

Integrando `func(y, x)`: **`y` (interna) primero, `x` (externa) despues**. Devuelve un escalar. SciPy lo evalua muchas veces; conviene escribirlo con NumPy segun [[concepto_callbacks_vectorizados]].

```python
import numpy as np
from scipy.integrate import dblquad

# OJO al orden: primero y, despues x
f = lambda y, x: x * y
```

### `a`, `b` (obligatorios)

Limites de la variable **externa `x`**. Son **constantes** (numeros, eventualmente `±np.inf`). Definen el rango exterior de integracion.

### `gfun`, `hfun` (obligatorios)

Limites de la variable **interna `y`**. Pueden ser:

- **Constantes** -> region con bordes horizontales (rectangulo en general).
- **Callables `g(x)` / `h(x)`** -> region cuyos bordes superior/inferior dependen de `x` (triangulos, sectores, areas curvas).

```python
# Region triangular: 0 <= x <= 1, 0 <= y <= x
area, err = dblquad(lambda y, x: 1.0, 0, 1, lambda x: 0, lambda x: x)
area    # → 0.5   (area del triangulo)
```

### `args`

Tupla de constantes extra inyectadas a `func` tras `(y, x)`.

```python
def integrando(y, x, k):
    return k * (x + y)

valor, err = dblquad(integrando, 0, 1, 0, 1, args=(2.0,))
valor    # → 2.0
```

## Casos de uso

### Volumen bajo una superficie sobre un rectangulo

```python
import numpy as np
from scipy.integrate import dblquad

# V = ∫∫ (x^2 + y^2) dy dx sobre [0,1] x [0,1]
f = lambda y, x: x**2 + y**2
V, err = dblquad(f, 0, 1, 0, 1)
V        # → 0.6667   (= 2/3)
```

### Integral sobre region triangular (limite interno dependiente de x)

```python
# ∫_0^1 ∫_0^x (x + y) dy dx ; el techo de y es la recta y = x
f = lambda y, x: x + y
valor, err = dblquad(f, 0, 1, lambda x: 0, lambda x: x)
valor    # → 0.5
```

### Masa de una placa con densidad variable sobre un cuarto de disco

```python
# Cuarto de disco r=1 en el primer cuadrante: y de 0 a sqrt(1 - x^2)
densidad = lambda y, x: 1 + x + y            # kg/m^2
m, err = dblquad(densidad, 0, 1,
                 lambda x: 0,
                 lambda x: np.sqrt(1 - x**2))
m        # → masa total de la placa
```

## Buenas practicas

1. **Memoriza el orden `func(y, x)`**: interna primero, externa despues. Si el resultado es absurdo, sospecha de esto antes que nada.
2. Recuerda que `gfun`/`hfun` definen los limites de **y** y son funciones de **x** (o constantes), nunca al reves.
3. Desempaqueta la tupla: `valor, error = dblquad(...)`.
4. Pasa constantes con `args` en vez de closures o globales.
5. Para integrandos con singularidades en el borde de la region, reescala o parte la integral; el adaptativo anidado puede degradarse.
6. Para integrales triples usa `tplquad` (extiende la misma logica con un nivel mas y orden `func(z, y, x)`).

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Resultado sin sentido | Orden de args invertido (`func(x, y)`) | Usar `func(y, x)`: interna primero |
| `gfun`/`hfun` como constantes erroneas | Confundir limites de x con los de y | `a, b` son de x; `gfun, hfun` son de y |
| `TypeError: gfun is not callable` | Pasar una expresion en vez de funcion | `lambda x: ...` o un escalar |
| Tratar el retorno como float | `dblquad` devuelve `(valor, error)` | Desempaquetar la tupla |
| `IntegrationWarning` | Region con singularidad o limites mal definidos | Reescalar/partir la region |

## Limitaciones

- El orden `func(y, x)` no es configurable: hay que adaptar la funcion al contrato.
- Solo integrandos escalares; no integra arrays muestreados (para eso `simpson`/`trapezoid`, y solo en 1D).
- El coste crece rapido: cada evaluacion externa dispara una integracion interna completa.
- Para mas dimensiones existe `tplquad` (triple) y `nquad` (n dimensiones generico).

## Notas relacionadas

- [[scipy.integrate.quad]]
- [[scipy.integrate.tplquad]]
- [[scipy.integrate.simpson]]
- [[concepto_callbacks_vectorizados]]
