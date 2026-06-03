---
title: np.random.normal — Normal general con media y desviación
aliases: [normal, random.normal, np.random.normal]
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

# np.random.normal — Normal general con media y desviación

## Firma de la función

```python
np.random.normal(loc=0.0, scale=1.0, size=None) -> ndarray | float
```

Es la versión **parametrizable** de la normal: media (`loc`) y desviación (`scale`) arbitrarias. Es la más general de la familia.

## Valor de retorno

Devuelve muestras de una distribución normal `N(loc, scale²)`. Con `size` devuelve un [[concepto_ndarray|ndarray]] `float64` de ese [[concepto_shape|shape]]; con `size=None` devuelve un escalar `float`.

| Llamada | Distribución | Shape | dtype |
|---------|--------------|-------|-------|
| `np.random.normal()` | N(0, 1) | `()` escalar | `float` |
| `np.random.normal(5, 2)` | N(5, 4) | `()` escalar | `float` |
| `np.random.normal(0, 1, 3)` | N(0, 1) | `(3,)` | `float64` |
| `np.random.normal(5, 2, (2, 3))` | N(5, 4) | `(2, 3)` | `float64` |

```python
import numpy as np
np.random.seed(0)
np.random.normal(loc=5, scale=2, size=(2, 3))
# array([[8.52810469, 5.80031442, 6.95747597],
#        [9.4817864 , 8.73511598, 3.04544424]])
```

## Parámetros en detalle

### `loc` — media de la distribución

Centro de la campana. Por defecto `0.0`. Puede ser escalar o un array (se aplica por [[concepto_broadcasting|broadcasting]] junto a `scale`).

```python
np.random.normal(loc=100, size=5)   # centradas en 100
```

### `scale` — desviación estándar

Anchura de la campana; debe ser **≥ 0**. Por defecto `1.0`. No es la varianza: la varianza es `scale²`.

```python
np.random.normal(scale=10, size=5)  # más dispersas
```

### `size` — shape como entero o tupla

Igual que en [[np.random.standard_normal]]: entero o tupla. Con `None` devuelve un escalar.

```python
np.random.normal(0, 1, (4, 4))   # matriz 4×4 ~ N(0,1)
```

## Casos de uso

### Equivalencia con la normal estándar escalada

```python
# Estas dos líneas producen la misma distribución:
np.random.normal(loc=50, scale=5, size=1000)
50 + 5 * np.random.randn(1000)        # ver np.random.randn
```

### Datos sintéticos con media física conocida

```python
temperaturas = np.random.normal(loc=22.5, scale=1.8, size=24)  # °C por hora
```

### Parámetros vectorizados (broadcasting)

```python
medias = np.array([0, 10, 100])
np.random.normal(loc=medias, scale=1)   # una muestra por cada media
```

## Buenas prácticas

1. Úsala siempre que necesites media o desviación distintas de 0/1: evita escalar a mano.
2. Recuerda que `scale` es la **desviación**, no la varianza (`var = scale²`).
3. Para la estándar pura, [[np.random.standard_normal]] o [[np.random.randn]] son más directas.
4. Fija `np.random.seed(...)` para reproducibilidad.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: scale < 0` | desviación negativa | usar `scale >= 0` |
| Dispersión inesperada | confundir `scale` con la varianza | pasar `scale = sqrt(varianza)` |
| `loc`/`scale` no alinean | shapes incompatibles vía broadcasting | ajustar shapes de `loc`/`scale` |
| Resultados no reproducibles | falta semilla | `np.random.seed(0)` antes |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.randn]]
- [[np.random.standard_normal]]
- [[np.random.seed]]
