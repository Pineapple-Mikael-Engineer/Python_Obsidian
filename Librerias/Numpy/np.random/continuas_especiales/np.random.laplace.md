---
title: np.random.laplace — Distribución de Laplace (doble exponencial)
aliases:
  - laplace
  - random.laplace
  - np.random.laplace
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

# np.random.laplace — Distribución de Laplace

Modela la distribución de **Laplace** o **doble exponencial**: simétrica respecto a su centro `loc`, con un **pico agudo** (no redondeado como la normal) y **colas más pesadas**. Equivale a pegar dos distribuciones exponenciales espalda con espalda. Es la base de la regularización L1 (LASSO) y del ruido en privacidad diferencial.

## Firma de la función

```python
np.random.laplace(
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

Valores reales centrados en `loc`, simétricos, con densidad proporcional a `exp(-|x-loc|/scale)`.

```python
import numpy as np
np.random.laplace()             # 0.207...  (loc=0, scale=1)
np.random.laplace(size=4)       # array([-0.31, 1.84, -0.05, 0.42])
```

## Parámetros en detalle

### `loc` — posición (mu)

Centro y pico de la distribución. Desplaza toda la curva sin cambiar su forma.

```python
np.random.laplace(loc=10, size=3)   # picos alrededor de 10
```

### `scale` — escala (b)

Factor de dispersión (`> 0`); controla la anchura. La varianza es `2 * scale**2`. A mayor `scale`, colas más extendidas.

```python
np.random.laplace(scale=0.5, size=3)   # concentrada
np.random.laplace(scale=5,   size=3)   # muy dispersa
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del resultado. Con `None` devuelve un escalar.

```python
np.random.laplace(0, 1, size=(2, 2))   # array 2x2
```

## Casos de uso

### Ruido de Laplace para privacidad diferencial

```python
# Añadir ruido calibrado a la sensibilidad / epsilon
sensibilidad, epsilon = 1.0, 0.5
ruido = np.random.laplace(loc=0, scale=sensibilidad/epsilon, size=100)
```

### Modelar errores con valores atípicos

```python
# Colas más pesadas que la normal → outliers más frecuentes
errores = np.random.laplace(loc=0, scale=2, size=1000)
```

## Buenas prácticas

1. Fija la semilla con [[np.random.seed]] para reproducir muestras.
2. Mantén `scale > 0`; un `scale=0` degenera en una constante igual a `loc`.
3. Recuerda que la varianza es `2*scale**2`, no `scale**2` como en la normal.
4. Si necesitas colas aún más pesadas en estimación de medias, considera [[np.random.t]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: scale < 0` | escala negativa | usar `scale > 0` |
| Dispersión menor de la esperada | confundir `scale` con desviación típica | usar `std = sqrt(2)*scale` |
| Salida constante | `scale=0` | usar un `scale` positivo |
| `TypeError` con `size` | pasar float como tamaño | usar `int` o `tuple` de enteros |

## Notas relacionadas

- [[np.random.logistic]]
- [[np.random.t]]
- [[np.random.f]]
- [[np.random.seed]]
- [[concepto_shape]]
