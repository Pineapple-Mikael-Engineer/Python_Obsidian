---
title: np.random.f — Distribución F de Snedecor (cociente de chi-cuadrado)
aliases:
  - f
  - random.f
  - np.random.f
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

# np.random.f — Distribución F de Snedecor

Modela la distribución **F de Snedecor**, definida como el cociente de dos variables chi-cuadrado independientes, cada una dividida por sus grados de libertad. Es la distribución de referencia en **ANOVA** y en los contrastes de **comparación de varianzas** entre dos poblaciones. Está construida a partir de la [[np.random.chisquare|distribución chi-cuadrado]].

## Firma de la función

```python
np.random.f(
    dfnum,
    dfden,
    size=None
) -> ndarray | float
```

## Valor de retorno

| Caso | `size` | Retorno | Shape |
|------|--------|---------|-------|
| Escalar | `None` | `float` | `()` |
| Vector | `int` | `ndarray` | `(size,)` |
| nD | `tuple` | `ndarray` | igual a `size` |

Los valores son siempre **no negativos** (`>= 0`), asimétricos a la derecha (cola larga superior).

```python
import numpy as np
np.random.f(5, 20)          # 0.873...  (un escalar float)
np.random.f(5, 20, size=4)  # array([1.21, 0.44, 2.07, 0.68])
```

## Parámetros en detalle

### `dfnum` — grados de libertad del numerador

Grados de libertad de la chi-cuadrado del numerador (`> 0`). En ANOVA corresponde a los grados de libertad **entre grupos**.

```python
np.random.f(1, 30)    # numerador con 1 g.l.
np.random.f(10, 30)   # numerador con 10 g.l.
```

### `dfden` — grados de libertad del denominador

Grados de libertad de la chi-cuadrado del denominador (`> 0`). En ANOVA corresponde a los grados de libertad **dentro de los grupos** (residual). A mayor `dfden`, la distribución se concentra alrededor de 1.

```python
np.random.f(5, 5)     # colas pesadas, mucha dispersión
np.random.f(5, 100)   # más concentrada cerca de 1
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del resultado. Con `None` devuelve un escalar.

```python
np.random.f(5, 20, size=(2, 3))   # array 2x3 de valores F
```

## Casos de uso

### Estadístico F simulado para ANOVA

```python
# Distribución nula de F con 3 grupos (dfnum=2) y 27 observaciones residuales
nulo = np.random.f(2, 27, size=10000)
umbral = np.percentile(nulo, 95)   # valor crítico al 5%
```

### Comparación de dos varianzas muestrales

```python
# Bajo H0 (varianzas iguales), el cociente s1^2 / s2^2 sigue una F
ratios = np.random.f(9, 9, size=5000)   # dos muestras de n=10
```

## Buenas prácticas

1. Fija la semilla con [[np.random.seed]] para reproducir las simulaciones.
2. Recuerda que ambos parámetros deben ser estrictamente positivos.
3. Si necesitas las chi-cuadrado por separado, genera dos con [[np.random.chisquare]] y divídelas manualmente.
4. Para grandes `dfden`, la F tiende a comportarse como una chi-cuadrado escalada.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: dfnum <= 0` | grados de libertad no positivos | usar `dfnum > 0` y `dfden > 0` |
| Valores enormes inesperados | `dfden` muy bajo (cola pesada) | aumentar `dfden` o revisar el modelo |
| Esperar valores negativos | la F siempre es `>= 0` | no aplicar a datos con signo |
| `TypeError` con `size` | pasar float como tamaño | usar `int` o `tuple` de enteros |

## Notas relacionadas

- [[np.random.chisquare]]
- [[np.random.t]]
- [[np.random.laplace]]
- [[np.random.logistic]]
- [[np.random.seed]]
- [[concepto_shape]]
