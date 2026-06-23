---
title: np.random.binomial — Nº de éxitos en n ensayos Bernoulli
aliases:
  - binomial
  - random.binomial
  - np.random.binomial
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray | int
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.random.binomial — Nº de éxitos en n ensayos Bernoulli

Muestrea de una **distribución binomial**: el número de éxitos en `n` ensayos independientes, cada uno con probabilidad de éxito `p`. Cada muestra es un entero en `[0, n]`. Equivale a contar cuántas caras salen al lanzar `n` monedas sesgadas, o cuántos clientes compran en `n` visitas.

## La idea

Si $X$ cuenta los éxitos de `n` ensayos Bernoulli independientes con probabilidad `p`, su función de masa de probabilidad (PMF) es:

$$ P(X = k) = \binom{n}{k}\, p^{k}\, (1-p)^{\,n-k}, \qquad k \in \{0, 1, \dots, n\} $$

La distribución tiene **media $np$** y **varianza $np(1-p)$**. Casos límite útiles: con `n=1` se reduce a un ensayo **Bernoulli** (0/1); cuando `n` es grande y `p` pequeño, se aproxima a una [[np.random.poisson]] con `lam = n*p`.

## Firma

```python
np.random.binomial(
    n,              # int | array_like[int]: número de ensayos (≥ 0)
    p,              # float | array_like[float]: probabilidad de éxito por ensayo, [0, 1]
    size=None,      # int | tuple[int] | None: forma de la salida
) -> ndarray | int
```

## Los parámetros en detalle

### `n` — número de ensayos

Entero ≥ 0. Define el **máximo** posible de cada muestra (el soporte es `0..n`). Puede ser un array para vectorizar (broadcasting con `p` y `size`).

```python
np.random.binomial(20, 0.5)   # éxitos en 20 ensayos → 0..20
```

### `p` — probabilidad de éxito por ensayo

Float en `[0, 1]`. Controla el sesgo: `p=0.5` da una distribución simétrica; un `p` alto desplaza la media hacia `n`, uno bajo hacia 0.

```python
np.random.binomial(10, 0.1)   # media ≈ 1 (pocos éxitos)
np.random.binomial(10, 0.9)   # media ≈ 9 (casi todos)
```

### `size` — forma de la salida

Entero o tupla que fija el [[concepto_shape|shape]]. `None` devuelve un escalar.

```python
np.random.binomial(5, 0.5, size=(2, 3))  # shape (2, 3)
```

## size y la forma de salida

`size` se traslada literalmente al shape de salida; cada celda es un conteo independiente en `0..n`:

$$ \texttt{size}=(n_0, \dots, n_{k-1}) \;\longrightarrow\; \texttt{shape} = (n_0, \dots, n_{k-1}), \quad \text{valores en } \{0,\dots,n\} $$

```python
np.random.binomial(10, 0.5, size=(2, 3, 4, 5)).shape     # (2, 3, 4, 5)    → 4D
np.random.binomial(10, 0.5, size=(2, 3, 4, 5, 6)).shape  # (2, 3, 4, 5, 6) → 5D
```

Si `n` o `p` son arrays, su shape debe ser **broadcasteable** con `size`.

## Casos de uso

### Simular tasa de conversión

```python
# 1000 visitas, 4% de conversión, repetido 30 días
conversiones = np.random.binomial(1000, 0.04, size=30)
conversiones.mean()   # ≈ 40
```

### Caso Bernoulli (n=1) como moneda

```python
lanzamientos = np.random.binomial(1, 0.5, size=10)  # 0/1
```

### Aproximar la distribución empírica

```python
muestras = np.random.binomial(10, 0.3, size=100_000)
np.bincount(muestras) / muestras.size   # frecuencia por nº de éxitos
```

> [!tip] Versión moderna: `rng.binomial`
> La API recomendada desde NumPy 1.17 usa un `Generator` de [[np.random.default_rng]] con el método **`rng.binomial`**, de firma idéntica (`n, p, size`). Crea generadores independientes y reproducibles sin tocar el estado global.
> ```python
> rng = np.random.default_rng(0)
> rng.binomial(10, 0.5, size=8)   # conteos de éxitos, n=10, p=0.5
> ```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: p < 0, p > 1` | probabilidad fuera de rango | usar `p` en `[0, 1]` |
| `ValueError: n < 0` | ensayos negativos | `n` entero ≥ 0 |
| Confundir el resultado con `p` | devuelve un **conteo**, no una proporción | dividir por `n` para la tasa |
| Esperar floats | la salida es entera | normalizar manualmente si hace falta |

## Notas relacionadas

- [[concepto_shape]] — `size` define la forma de salida
- [[np.random.default_rng]] — `rng.binomial`, el reemplazo moderno
- [[np.random.poisson]] — aproximación con `n` grande y `p` pequeño (`lam = n*p`)
- [[np.random.randint]] · [[np.random.choice]]
