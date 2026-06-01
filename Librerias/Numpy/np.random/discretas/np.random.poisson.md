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
retorna: ndarray o int
inplace: false
draft: false
---

# np.random.poisson — Eventos por intervalo (media lam)

Muestrea de una **distribución de Poisson**: el número de eventos que ocurren en un intervalo fijo de tiempo o espacio, cuando ocurren con una tasa media `lam` y de forma independiente. Cada muestra es un entero ≥ 0 sin tope superior teórico.

## Firma de la función

```python
np.random.poisson(
    lam=1.0,
    size=None
) -> ndarray | int
```

## Valor de retorno

Devuelve un entero o un [[concepto_ndarray|ndarray]] con el [[concepto_shape|shape]] de `size`. La distribución tiene **media = varianza = `lam`**, propiedad característica de Poisson.

| Llamada | Significado | Retorno |
|---------|-------------|---------|
| `np.random.poisson()` | eventos con `lam=1` | `int` ≥ 0 |
| `np.random.poisson(5)` | media 5 eventos/intervalo | `int` ≥ 0 |
| `np.random.poisson(3.0, size=4)` | 4 intervalos | `ndarray` shape `(4,)` |

```python
import numpy as np
np.random.poisson(5, size=8)
# array([4, 7, 3, 5, 6, 2, 5, 8])  # en torno a lam = 5
```

## Parámetros en detalle

### `lam` — tasa media de eventos (λ)

Float ≥ 0. Es a la vez la media y la varianza. Puede ser un array para generar muestras con distintas tasas (broadcasting con `size`).

```python
np.random.poisson(0.5)   # eventos raros, casi siempre 0 o 1
np.random.poisson(20)    # media alta, distribución casi simétrica
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]]. `None` devuelve un escalar.

```python
np.random.poisson(2.0, size=(3, 3))  # shape (3, 3)
```

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

## Buenas prácticas

1. `lam` es media **y** varianza; si tus datos tienen varianza ≠ media, Poisson no es el modelo adecuado.
2. La salida no tiene tope: dimensiona buffers pensando en la cola.
3. Para conteos acotados con un máximo claro usa [[np.random.binomial]].
4. Fija la semilla con `np.random.seed(...)` para reproducir simulaciones.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: lam < 0` | tasa negativa | usar `lam >= 0` |
| Esperar un máximo fijo | Poisson no tiene tope | usar [[np.random.binomial]] si hay límite |
| Varianza inesperada | en Poisson var = media = `lam` | revisar idoneidad del modelo |
| Esperar floats | la salida es entera | la cuenta de eventos siempre es entera |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.binomial]]
- [[np.random.randint]]
- [[np.random.choice]]
