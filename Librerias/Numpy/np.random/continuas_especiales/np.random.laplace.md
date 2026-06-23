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
retorna: ndarray | float
inplace: false
draft: false
---

# np.random.laplace — Distribución de Laplace

`np.random.laplace` muestrea de la distribución de **Laplace** (o **doble exponencial**): simétrica respecto a su centro `loc`, con un **pico agudo** —no redondeado como la normal— y **colas más pesadas**. Equivale a pegar dos exponenciales espalda con espalda. Es la base de la **regularización L1** (LASSO, prior de Laplace) y del ruido en **privacidad diferencial**.

> [!tip] Versión moderna
> Esta función usa el **estado global** de `np.random` (el que fija [[np.random.seed]]), hoy considerado *legacy*. La API recomendada crea un generador propio y aislado con [[np.random.default_rng]]:
> ```python
> rng = np.random.default_rng()
> rng.laplace(loc=0.0, scale=1.0, size=(2, 3))   # equivalente moderno
> ```
> El método `rng.laplace` tiene la misma firma; cambia solo de dónde sale la aleatoriedad.

## La idea

Cada muestra se extrae de una densidad que decae **exponencialmente a ambos lados** del centro `loc`, con la escala `scale` ($b > 0$) controlando la anchura. La media y la mediana valen `loc`; la varianza es $2b^2$ (el doble que una normal de la misma escala).

$$ f(x) = \frac{1}{2b}\,\exp\!\left(-\frac{\lvert x - \mu\rvert}{b}\right), \qquad \mu = \texttt{loc},\ b = \texttt{scale} $$

$$ X_{i_0,\dots,i_{k-1}} \sim \mathrm{Laplace}(\mu, b) \quad \text{i.i.d., con shape } \texttt{size} $$

El valor absoluto $\lvert x-\mu\rvert$ es lo que produce el **pico** en el centro: la densidad no se aplana en torno a `loc` como en la normal, sino que forma una punta.

## Firma

```python
np.random.laplace(
    loc=0.0,     # float | array_like: centro y pico de la distribución (μ)
    scale=1.0,   # float | array_like: escala b > 0; varianza = 2·scale²
    size=None,   # int | tuple[int] | None: shape de salida; None → escalar
) -> ndarray | float
```

## Los parámetros en detalle

### `loc` — posición (μ)

Centro y pico de la distribución; coincide con la media y la mediana. Desplaza toda la curva sin cambiar su forma. Acepta escalar o array (se aplica broadcasting con `size`).

```python
np.random.laplace(loc=10, size=3)   # picos alrededor de 10
```

### `scale` — escala (b)

Factor de dispersión, debe ser `> 0`; controla la anchura. La **varianza es `2*scale**2`**, no `scale**2` como en la normal: a igual `scale`, la Laplace dispersa más. A mayor `scale`, colas más extendidas.

```python
np.random.laplace(scale=0.5, size=3)   # concentrada
np.random.laplace(scale=5,   size=3)   # muy dispersa
```

Un `scale=0` degenera en la constante `loc`.

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del resultado. Con `None` devuelve un único `float`.

```python
np.random.laplace(0, 1, size=(2, 2))   # array 2x2
```

## size y la forma de salida

La forma del array generado es exactamente `size`; cada muestra es i.i.d. Sin `size`, el retorno es un `float` escalar (no un array `0-d`).

| Llamada | `size` | retorno | shape |
|---|---|---|---|
| `np.random.laplace()` | `None` | `float` | — |
| `np.random.laplace(size=4)` | `int` | `ndarray` | `(4,)` |
| `np.random.laplace(0, 1, (2, 3))` | `tuple` | `ndarray` | `(2, 3)` |

```python
import numpy as np
np.random.seed(0)
np.random.laplace(size=4)   # array([ 0.04,  0.13, -0.31,  1.84])  centradas en loc=0
```

## Casos de uso

### Ruido de Laplace para privacidad diferencial

```python
# Ruido calibrado a la sensibilidad y al presupuesto de privacidad epsilon
sensibilidad, epsilon = 1.0, 0.5
ruido = np.random.laplace(loc=0, scale=sensibilidad / epsilon, size=100)
```

### Modelar errores con valores atípicos

```python
# Colas más pesadas que la normal → outliers más frecuentes
errores = np.random.laplace(loc=0, scale=2, size=1000)
errores.var()   # ≈ 2 * 2**2 = 8
```

### Verificar la varianza teórica

```python
m = np.random.laplace(loc=0, scale=3, size=100000)
m.var()   # ≈ 2 * 3**2 = 18
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: scale < 0` | escala negativa | usar `scale > 0` |
| Dispersión mayor de la esperada | confundir `scale` con la desviación típica | la desviación es `sqrt(2)*scale` |
| Salida constante | `scale=0` | usar un `scale` positivo |
| `TypeError` con `size` | pasar un float como tamaño | usar `int` o `tuple` de enteros |

## Notas relacionadas

- [[np.random.logistic]] — también colas pesadas, pero con pico redondeado
- [[np.random.t]] — colas pesadas para estimación de medias
- [[np.random.normal]] — el contraste: pico redondeado, colas ligeras
- [[np.random.default_rng]] · [[np.random.seed]] · [[concepto_shape]]
