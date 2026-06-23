---
title: np.random.chisquare — Muestras de la distribución chi-cuadrado
aliases: [chisquare, random.chisquare, np.random.chisquare]
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray o float
inplace: false
draft: false
---

# np.random.chisquare — Muestras de la distribución chi-cuadrado

Genera muestras de una distribución **chi-cuadrado** con `df` grados de libertad. Surge como la **suma de cuadrados de `df` normales estándar** independientes, por lo que es siempre no negativa y asimétrica a la derecha. Es la distribución de referencia en **tests de hipótesis** (bondad de ajuste, independencia en tablas de contingencia) y en la inferencia sobre varianzas.

## La idea

Si $Z_1,\dots,Z_k$ son normales estándar independientes, entonces $\sum_{i=1}^{k} Z_i^2$ sigue una chi-cuadrado con $k = $ `df` grados de libertad. Su densidad sobre `x ≥ 0` es:

$$ f(x;k) \;=\; \frac{x^{\,k/2-1}\,e^{-x/2}}{2^{\,k/2}\,\Gamma(k/2)}, \qquad x \ge 0 $$

Aquí el único **parámetro de forma** es `df` (los grados de libertad $k$). Propiedades clave:

- Media $\mathbb{E}[X] = k$ y varianza $\operatorname{Var}[X] = 2k$.
- Con `df` pequeño es muy **sesgada a la derecha**; al crecer `df` se aproxima a una normal.
- Es un **caso particular de la gamma**: `chisquare(df)` ≡ `gamma(shape=df/2, scale=2)`.

> [!tip] Versión moderna
> La API recomendada desde NumPy 1.17 usa un generador explícito en vez del estado global. Ver [[np.random.default_rng]].
> ```python
> rng = np.random.default_rng()
> rng.chisquare(df=4, size=1000)
> ```

## Firma

```python
np.random.chisquare(df, size=None) -> ndarray | float
```

## Los parámetros en detalle

### `df` — grados de libertad

Número de normales estándar al cuadrado que se suman. Fija tanto la media (`df`) como la asimetría: con pocos `df` la distribución está muy sesgada a la derecha; con muchos se vuelve casi simétrica. Debe ser `> 0` y admite valores **no enteros**. Acepta escalar o array (broadcasting con `size`).

```python
np.random.chisquare(1)    # muy asimétrica, masa cerca de 0
np.random.chisquare(30)   # casi acampanada
np.random.chisquare(2.5)  # df no entero es válido
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del array; `None` devuelve un escalar.

```python
np.random.chisquare(4, size=1000)    # vector (1000,)
np.random.chisquare(4, size=(5, 5))  # matriz (5, 5)
```

## size y la forma de salida

Devuelve reales no negativos con media tendente a `df` y varianza a `2·df`.

| Llamada | Distribución | Shape | dtype |
|---------|--------------|-------|-------|
| `np.random.chisquare(2)` | χ²(2) | `()` escalar | `float` |
| `np.random.chisquare(2, 4)` | χ²(2) | `(4,)` | `float64` |
| `np.random.chisquare(10)` | χ²(10), media ≈ 10 | `()` escalar | `float` |
| `np.random.chisquare(5, (2, 3))` | χ²(5) | `(2, 3)` | `float64` |

```python
import numpy as np
np.random.seed(0)
np.random.chisquare(df=4, size=3)
# array([3.21, 5.84, 2.10])  → media tiende a df = 4
```

## Casos de uso

### Distribución nula de un estadístico chi-cuadrado por simulación

```python
# Test con 6 categorías → df = 6-1 = 5; aproximar la nula y un valor crítico
nula = np.random.chisquare(df=5, size=100000)
critico_95 = np.percentile(nula, 95)   # umbral de rechazo al 5%
```

### Verificar empíricamente media y varianza

```python
m = np.random.chisquare(df=8, size=100000)
m.mean()   # ≈ 8     (df)
m.var()    # ≈ 16    (2*df)
```

### Equivalencia con la gamma

```python
# chisquare(df) ≡ gamma(shape=df/2, scale=2)
np.random.gamma(shape=5/2, scale=2, size=1000)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: df <= 0` | Grados de libertad no positivos | Garantizar `df > 0` |
| Media inesperada | Olvidar que la media es `df` | Ajustar `df` al estadístico real |
| Esperar simetría con `df` bajo | Con pocos `df` es muy asimétrica | Subir `df` o aceptar el sesgo |
| Esperar valores negativos | La chi-cuadrado es siempre ≥ 0 | Usar la t o la normal si necesitas negativos |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.default_rng]]
- [[np.random.gamma]]
- [[np.random.randn]]
- [[np.random.seed]]
