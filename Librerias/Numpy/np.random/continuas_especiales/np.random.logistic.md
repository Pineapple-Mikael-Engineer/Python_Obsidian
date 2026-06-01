---
title: np.random.logistic — Distribución logística
aliases:
  - logistic
  - random.logistic
  - np.random.logistic
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

# np.random.logistic — Distribución logística

Modela la distribución **logística**: simétrica y acampanada como la normal, pero con **colas más pesadas**. Su función de distribución acumulada es la **sigmoide** (función logística), lo que la conecta directamente con la **regresión logística** y los modelos de elección discreta. La distribución de [[np.random.laplace|Laplace]] comparte el rasgo de colas pesadas pero con pico agudo, no redondeado.

## Firma de la función

```python
np.random.logistic(
    loc=0.0,
    scale=1.0,
    size=None
) -> ndarray | float
```

## Valor de retorno

| Caso | `size` | Retorno | Shape |
|------|--------|---------|-------|
| Escalar | `None` | `float` | `()` |
| Vector | `int` | `ndarray` | `(size,)` |
| nD | `tuple` | `ndarray` | igual a `size` |

Valores reales centrados en `loc`, simétricos, con densidad `exp(-z) / (scale*(1+exp(-z)))**2` donde `z=(x-loc)/scale`.

```python
import numpy as np
np.random.logistic()           # 0.418...  (loc=0, scale=1)
np.random.logistic(size=4)     # array([-1.07, 0.55, 2.91, -0.33])
```

## Parámetros en detalle

### `loc` — posición (mu)

Centro de la distribución (también su media y mediana). Desplaza la curva sin alterar su forma.

```python
np.random.logistic(loc=5, size=3)   # centrada en 5
```

### `scale` — escala (s)

Factor de dispersión (`> 0`); controla la anchura. La varianza es `(scale*pi)**2 / 3`. A mayor `scale`, colas más extendidas.

```python
np.random.logistic(scale=0.3, size=3)   # concentrada
np.random.logistic(scale=4,   size=3)   # muy dispersa
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del resultado. Con `None` devuelve un escalar.

```python
np.random.logistic(0, 1, size=(3, 3))   # array 3x3
```

## Casos de uso

### Término de error en un modelo logit

```python
# La logística es la base del error en modelos de elección discreta
utilidad = 0.5 + np.random.logistic(loc=0, scale=1, size=1000)
eleccion = (utilidad > 0).astype(int)
```

### Simular datos con colas pesadas pero centrados

```python
muestras = np.random.logistic(loc=0, scale=2, size=10000)
muestras.mean()   # ≈ 0  (la media coincide con loc)
```

## Buenas prácticas

1. Fija la semilla con [[np.random.seed]] para reproducir resultados.
2. Mantén `scale > 0`; controla la dispersión real con `std = scale*pi/sqrt(3)`.
3. Úsala cuando quieras un perfil casi normal pero con más eventos extremos.
4. Para colas pesadas con pico agudo, prefiere [[np.random.laplace]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: scale < 0` | escala negativa | usar `scale > 0` |
| Varianza menor de la esperada | confundir `scale` con desviación típica | usar `std = scale*pi/sqrt(3)` |
| Salida constante | `scale=0` | usar un `scale` positivo |
| `TypeError` con `size` | pasar float como tamaño | usar `int` o `tuple` de enteros |

## Notas relacionadas

- [[np.random.laplace]]
- [[np.random.t]]
- [[np.random.f]]
- [[np.random.seed]]
- [[concepto_shape]]
