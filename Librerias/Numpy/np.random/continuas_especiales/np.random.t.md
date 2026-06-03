---
title: np.random.t — Distribución t de Student
aliases:
  - t
  - random.t
  - np.random.t
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

# np.random.t — Distribución t de Student

Modela la distribución **t de Student** con `df` grados de libertad. Es simétrica y con forma de campana como la normal, pero con **colas más pesadas**: aparece al estimar medias con **muestras pequeñas** y varianza poblacional desconocida. Cuando `df` crece, converge a la normal estándar (ver [[np.random.standard_normal]]).

## Firma de la función

```python
np.random.t(
    df,
    size=None
) -> ndarray | float
```

## Valor de retorno

| Caso | `size` | Retorno | Shape |
|------|--------|---------|-------|
| Escalar | `None` | `float` | `()` |
| Vector | `int` | `ndarray` | `(size,)` |
| nD | `tuple` | `ndarray` | igual a `size` |

Valores reales centrados en `0`, simétricos, con cola más gruesa cuanto menor es `df`.

```python
import numpy as np
np.random.t(10)          # -0.534...  (un escalar float)
np.random.t(10, size=4)  # array([ 1.12, -0.07, -2.34, 0.61])
```

## Parámetros en detalle

### `df` — grados de libertad

Número de grados de libertad (`> 0`). Controla el grosor de las colas:

| `df` | Comportamiento |
|------|----------------|
| `1` | Distribución de Cauchy (colas muy pesadas, sin media definida) |
| `5`–`30` | Colas notablemente más pesadas que la normal |
| `> 100` | Prácticamente indistinguible de la normal estándar |

```python
np.random.t(1, size=3)    # colas extremas (Cauchy)
np.random.t(30, size=3)   # casi normal
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del resultado. Con `None` devuelve un escalar.

```python
np.random.t(8, size=(3, 2))   # array 3x2 de valores t
```

## Casos de uso

### Distribución nula de un estadístico t

```python
# Contraste de una media con n=10 → df = n-1 = 9
nulo = np.random.t(9, size=10000)
critico = np.percentile(nulo, [2.5, 97.5])   # límites bilaterales al 5%
```

### Simular datos con valores atípicos (colas pesadas)

```python
# Ruido más realista que la normal para outliers ocasionales
ruido = np.random.t(3, size=1000)
```

## Buenas prácticas

1. Fija la semilla con [[np.random.seed]] para reproducir resultados.
2. Usa `df` pequeño para modelar colas pesadas; grande para aproximar la normal.
3. Para `df=1` recuerda que la media y la varianza no existen: evita promediar.
4. Si solo necesitas normalidad, usa directamente [[np.random.standard_normal]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: df <= 0` | grados de libertad no positivos | usar `df > 0` |
| Media muestral inestable | `df` muy bajo (colas pesadas) | aumentar `df` o usar la mediana |
| Esperar valores acotados | la t no tiene cota; produce extremos | no asumir rango fijo |
| `TypeError` con `size` | pasar float como tamaño | usar `int` o `tuple` de enteros |

## Notas relacionadas

- [[np.random.standard_normal]]
- [[np.random.f]]
- [[np.random.chisquare]]
- [[np.random.laplace]]
- [[np.random.seed]]
- [[concepto_shape]]
