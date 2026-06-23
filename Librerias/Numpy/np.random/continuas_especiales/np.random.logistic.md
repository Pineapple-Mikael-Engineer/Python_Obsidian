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
retorna: ndarray | float
inplace: false
draft: false
---

# np.random.logistic — Distribución logística

`np.random.logistic` muestrea de la distribución **logística**: simétrica y acampanada como la normal, pero con **colas más pesadas**. Su función de distribución acumulada es la **sigmoide** (función logística), lo que la conecta con la **regresión logística** y los modelos de elección discreta. La distribución de [[np.random.laplace|Laplace]] comparte el rasgo de colas pesadas, pero con pico agudo en vez de redondeado.

> [!tip] Versión moderna
> Esta función usa el **estado global** de `np.random` (el que fija [[np.random.seed]]), hoy considerado *legacy*. La API recomendada crea un generador propio y aislado con [[np.random.default_rng]]:
> ```python
> rng = np.random.default_rng()
> rng.logistic(loc=0.0, scale=1.0, size=(3, 3))   # equivalente moderno
> ```
> El método `rng.logistic` tiene la misma firma; cambia solo de dónde sale la aleatoriedad.

## La idea

Cada muestra se extrae de una densidad simétrica en torno a `loc`, con la escala `scale` ($s > 0$) fijando la anchura. La media, mediana y moda valen `loc`; la varianza es $\pi^2 s^2 / 3$. La **acumulada es la sigmoide** $F(x)=1/(1+e^{-z})$ con $z=(x-\mu)/s$.

$$ f(x) = \frac{e^{-z}}{s\,(1 + e^{-z})^2}, \qquad z = \frac{x - \mu}{s}, \quad \mu = \texttt{loc},\ s = \texttt{scale} $$

$$ X_{i_0,\dots,i_{k-1}} \sim \mathrm{Logistic}(\mu, s) \quad \text{i.i.d., con shape } \texttt{size} $$

Frente a la normal, la logística tiene la misma silueta acampanada pero **más masa en las colas**: los eventos extremos son más frecuentes.

## Firma

```python
np.random.logistic(
    loc=0.0,     # float | array_like: centro de la distribución (μ)
    scale=1.0,   # float | array_like: escala s > 0; varianza = (s·π)²/3
    size=None,   # int | tuple[int] | None: shape de salida; None → escalar
) -> ndarray | float
```

## Los parámetros en detalle

### `loc` — posición (μ)

Centro de la distribución; coincide con la media, la mediana y la moda. Desplaza la curva sin alterar su forma. Acepta escalar o array (broadcasting con `size`).

```python
np.random.logistic(loc=5, size=3)   # centrada en 5
```

### `scale` — escala (s)

Factor de dispersión, debe ser `> 0`; controla la anchura. La **varianza es `(scale*pi)**2 / 3`**, por lo que la desviación típica es `scale*pi/sqrt(3)`. A mayor `scale`, colas más extendidas.

```python
np.random.logistic(scale=0.3, size=3)   # concentrada
np.random.logistic(scale=4,   size=3)   # muy dispersa
```

Un `scale=0` degenera en la constante `loc`.

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del resultado. Con `None` devuelve un único `float`.

```python
np.random.logistic(0, 1, size=(3, 3))   # array 3x3
```

## size y la forma de salida

La forma del array generado es exactamente `size`; cada muestra es i.i.d. Sin `size`, el retorno es un `float` escalar (no un array `0-d`).

| Llamada | `size` | retorno | shape |
|---|---|---|---|
| `np.random.logistic()` | `None` | `float` | — |
| `np.random.logistic(size=4)` | `int` | `ndarray` | `(4,)` |
| `np.random.logistic(0, 1, (3, 3))` | `tuple` | `ndarray` | `(3, 3)` |

```python
import numpy as np
np.random.seed(0)
np.random.logistic(size=4)   # array([ 0.07,  1.39, -0.05,  0.66])  centradas en loc=0
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

### Verificar la varianza teórica

```python
m = np.random.logistic(loc=0, scale=1, size=100000)
m.var()   # ≈ pi**2 / 3 ≈ 3.29
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: scale < 0` | escala negativa | usar `scale > 0` |
| Varianza mayor de la esperada | confundir `scale` con la desviación típica | la desviación es `scale*pi/sqrt(3)` |
| Salida constante | `scale=0` | usar un `scale` positivo |
| `TypeError` con `size` | pasar un float como tamaño | usar `int` o `tuple` de enteros |

## Notas relacionadas

- [[np.random.laplace]] — colas pesadas, pero con pico agudo
- [[np.random.normal]] — el contraste: misma campana, colas más ligeras
- [[np.random.t]] — colas pesadas para muestras pequeñas
- [[np.random.default_rng]] · [[np.random.seed]] · [[concepto_shape]]
