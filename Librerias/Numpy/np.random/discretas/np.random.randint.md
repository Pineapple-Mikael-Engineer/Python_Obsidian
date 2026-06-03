---
title: np.random.randint — Enteros uniformes en [low, high)
aliases:
  - randint
  - random.randint
  - np.random.randint
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

# np.random.randint — Enteros uniformes en [low, high)

Genera enteros aleatorios con distribución **uniforme discreta**. El intervalo es semiabierto `[low, high)`: el límite inferior se incluye y el **superior se EXCLUYE**, igual que `range()`. Es la función de referencia para muestrear enteros en NumPy.

## Firma de la función

```python
np.random.randint(
    low,
    high=None,
    size=None,
    dtype=int
) -> ndarray | int
```

## Valor de retorno

Devuelve un entero (si `size=None`) o un [[concepto_ndarray|ndarray]] de enteros con el [[concepto_shape|shape]] indicado por `size`. Todos los valores son equiprobables dentro del rango.

| Llamada | Rango efectivo | Retorno |
|---------|----------------|---------|
| `np.random.randint(10)` | `[0, 10)` | un `int` en 0..9 |
| `np.random.randint(1, 7)` | `[1, 7)` | un `int` en 1..6 (un dado) |
| `np.random.randint(0, 2, size=5)` | `[0, 2)` | `ndarray` de 5 ceros/unos |
| `np.random.randint(1, 7, size=(2, 3))` | `[1, 7)` | `ndarray` shape `(2, 3)` |

```python
import numpy as np
np.random.randint(1, 7, size=10)
# array([3, 6, 1, 5, 2, 6, 4, 1, 3, 5])  # high=7 nunca aparece
```

## Parámetros en detalle

### `low` — límite inferior (o superior si `high` es None)

Si das **un solo argumento**, este actúa como `high` y el rango pasa a ser `[0, low)`. Si das dos, `low` es el inicio inclusivo.

```python
np.random.randint(5)        # [0, 5)  → 0,1,2,3,4
np.random.randint(2, 5)     # [2, 5)  → 2,3,4
```

### `high` — límite superior EXCLUIDO

El valor `high` **nunca** se genera. Para incluir un tope `N`, usa `high = N + 1`.

```python
np.random.randint(1, 6)     # máximo posible: 5
np.random.randint(1, 6 + 1) # ahora el 6 sí es posible (1..6)
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]]. Con `None` devuelve un escalar de Python.

```python
np.random.randint(0, 100, size=4)       # (4,)
np.random.randint(0, 100, size=(3, 3))  # (3, 3)
```

### `dtype` — tipo entero de salida

Por defecto `int` (plataforma). Puede ajustarse a tipos menores para ahorrar memoria.

```python
np.random.randint(0, 256, size=5, dtype=np.uint8)
```

## Casos de uso

### Simular tiradas de dado

```python
dados = np.random.randint(1, 7, size=1000)   # 1000 tiradas de un d6
dados.mean()   # ≈ 3.5
```

### Generar máscaras o etiquetas binarias

```python
etiquetas = np.random.randint(0, 2, size=20)  # 0/1 aleatorios
```

### Índices aleatorios para muestrear filas

```python
datos = np.arange(50).reshape(10, 5)
idx = np.random.randint(0, datos.shape[0], size=3)
muestra = datos[idx]   # 3 filas al azar (con posible repetición)
```

## Buenas prácticas

1. Recuerda **siempre** que `high` está excluido: suma 1 si necesitas ese valor.
2. Fija `np.random.seed(...)` para reproducibilidad en tests.
3. Para muestrear de un array concreto o **sin reemplazo**, usa [[np.random.choice]].
4. Para probabilidades no uniformes (rango sesgado) necesitas otra distribución como [[np.random.binomial]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El tope nunca aparece | `high` es exclusivo | usar `high + 1` |
| `ValueError: low >= high` | rango invertido o vacío | asegurar `low < high` |
| Confundir con `random_integers` | aquella incluye `high` | preferir `randint` (ver [[np.random.random_integers]]) |
| Esperar floats | `randint` da enteros | usar otra función para reales |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.choice]]
- [[np.random.random_integers]]
- [[np.random.binomial]]
- [[np.random.poisson]]
