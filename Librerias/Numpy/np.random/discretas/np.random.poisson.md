---
title: np.random.poisson — Eventos por intervalo (media lam)
aliases:
  - poisson
  - random.poisson
  - np.random.poisson
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

# np.random.poisson — Eventos por intervalo (media lam)

Muestrea de una **distribución de Poisson**: el número de eventos que ocurren en un intervalo fijo de tiempo o espacio, cuando suceden con una tasa media `lam` ($\lambda$) y de forma independiente. Cada muestra es un entero ≥ 0 **sin tope superior** teórico. Modela llegadas a una cola, llamadas por hora, fotones detectados o fallos por día.

## La idea

Si $X$ cuenta los eventos en un intervalo con tasa media $\lambda$ = `lam`, su función de masa de probabilidad (PMF) es:

$$ P(X = k) = \frac{\lambda^{k}\, e^{-\lambda}}{k!}, \qquad k \in \{0, 1, 2, \dots\} $$

La propiedad característica de Poisson es que **media = varianza = $\lambda$**. Por eso solo necesita un parámetro. Surge como límite de una [[np.random.binomial]] con `n` grande y `p` pequeño manteniendo `lam = n*p`; para `lam` grande se aproxima a una normal.

## Firma

```python
np.random.poisson(
    lam=1.0,        # float | array_like[float]: tasa media de eventos (≥ 0)
    size=None,      # int | tuple[int] | None: forma de la salida
) -> ndarray | int
```

## Los parámetros en detalle

### `lam` — tasa media de eventos (λ)

Float ≥ 0. Es **a la vez la media y la varianza**. Puede ser un array para generar muestras con distintas tasas (broadcasting con `size`).

```python
np.random.poisson(0.5)   # eventos raros, casi siempre 0 o 1
np.random.poisson(20)    # media alta, distribución casi simétrica
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]]. `None` devuelve un escalar.

```python
np.random.poisson(2.0, size=(3, 3))  # shape (3, 3)
```

## size y la forma de salida

`size` se traslada literalmente al shape de salida; cada celda es un conteo de eventos independiente:

$$ \texttt{size}=(n_0, \dots, n_{k-1}) \;\longrightarrow\; \texttt{shape} = (n_0, \dots, n_{k-1}), \quad \text{valores en } \{0, 1, 2, \dots\} $$

```python
np.random.poisson(5, size=(2, 3, 4, 5)).shape     # (2, 3, 4, 5)    → 4D
np.random.poisson(5, size=(2, 3, 4, 5, 6)).shape  # (2, 3, 4, 5, 6) → 5D
```

Si `lam` es un array, su shape debe ser **broadcasteable** con `size`.

## Casos de uso

### Modelar llegadas (colas, llamadas, peticiones)

```python
# Peticiones por segundo durante un minuto, tasa media 8/s
peticiones = np.random.poisson(8, size=60)
peticiones.sum()   # carga total aproximada
```

### Conteos de eventos raros

```python
# Defectos por lote, media 0.7
defectos = np.random.poisson(0.7, size=1000)
(defectos == 0).mean()   # proporción de lotes sin defectos
```

### Aproximación de binomial con n grande y p pequeño

```python
# binomial(n=10000, p=0.0005) ≈ poisson(lam=5)
np.random.poisson(10000 * 0.0005, size=5)
```

> [!tip] Versión moderna: `rng.poisson`
> La API recomendada desde NumPy 1.17 usa un `Generator` de [[np.random.default_rng]] con el método **`rng.poisson`**, de firma idéntica (`lam, size`). Reproducible y aislado del estado global.
> ```python
> rng = np.random.default_rng(0)
> rng.poisson(5, size=8)   # conteos de eventos, lam=5
> ```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: lam < 0` | tasa negativa | usar `lam >= 0` |
| Esperar un máximo fijo | Poisson no tiene tope | usar [[np.random.binomial]] si hay límite |
| Varianza inesperada | en Poisson var = media = `lam` | revisar la idoneidad del modelo |
| Esperar floats | la salida es entera | la cuenta de eventos siempre es entera |

## Notas relacionadas

- [[concepto_shape]] — `size` define la forma de salida
- [[np.random.default_rng]] — `rng.poisson`, el reemplazo moderno
- [[np.random.binomial]] — conteo acotado; Poisson es su límite con `n→∞`, `p→0`
- [[np.random.randint]] · [[np.random.choice]]
