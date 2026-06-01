---
title: np.random.gamma — Muestras de la distribución gamma
aliases: [gamma, random.gamma, np.random.gamma]
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

# np.random.gamma — Muestras de la distribución gamma

Modela el **tiempo de espera hasta que ocurren `k` eventos** de un proceso de Poisson, es decir la suma de `k` exponenciales independientes. Generaliza a la exponencial mediante dos parámetros: la **forma** (`shape`, número de eventos / curvatura) y la **escala** (`scale = 1/λ`). Aparece en fiabilidad, tiempos agregados, lluvias y como prior bayesiano de tasas.

## Firma de la función

```python
np.random.gamma(
    shape,
    scale=1.0,
    size=None
) -> ndarray | float
```

## Valor de retorno

Devuelve reales no negativos de densidad `f(x) ∝ x^(shape−1)·exp(−x/scale)`. La media tiende a `shape·scale` y la varianza a `shape·scale²`. Con `shape=1` recupera la exponencial.

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `gamma(2.0)` con `size=None` | `float` | `1.85` |
| `gamma(2.0, size=4)` | `ndarray (4,)` | `[1.2, 3.4, 0.9, 2.1]` |
| `gamma(2.0, scale=3.0)` | media ≈ 6.0 | valores escalados ×3 |
| `gamma(9.0, size=(2,2))` | `ndarray (2,2)` | casi simétrica (forma alta) |

```python
import numpy as np
np.random.seed(0)
np.random.gamma(shape=2.0, scale=2.0, size=3)
# array([4.12, 6.78, 1.43])  → media tiende a 2*2 = 4
```

## Parámetros en detalle

### `shape` — parámetro de forma (k)

Controla la curvatura. Valores bajos (`<1`) concentran masa cerca de 0 con cola larga; `shape=1` es exponencial; valores altos hacen la distribución cada vez más simétrica (tiende a normal). Debe ser `> 0`.

```python
np.random.gamma(0.5)   # muy asimétrica, masa cerca de 0
np.random.gamma(1.0)   # equivale a exponencial(scale)
np.random.gamma(10.0)  # casi acampanada
```

### `scale` — escala (1/λ)

Estira el eje horizontal: misma forma, valores más grandes. Es `1/λ`, igual que en la exponencial. Debe ser `> 0`.

```python
np.random.gamma(2.0, scale=1.0)   # media ≈ 2
np.random.gamma(2.0, scale=5.0)   # media ≈ 10
```

### `size` — forma de la salida

Entero o tupla que fija el [[concepto_shape|shape]] del array; `None` devuelve un escalar.

```python
np.random.gamma(3.0, size=1000)     # vector (1000,)
np.random.gamma(3.0, size=(4, 5))   # matriz (4, 5)
```

## Casos de uso

### Tiempo total hasta el k-ésimo fallo

```python
# Espera hasta el 3er fallo, tasa media 1 fallo cada 100 h (scale=100)
espera_3_fallos = np.random.gamma(shape=3, scale=100, size=1000)
espera_3_fallos.mean()   # ≈ 300
```

### Modelar montos agregados (totales de lluvia, importes de seguros)

```python
# Distribución sesgada y positiva, calibrada por momentos
montos = np.random.gamma(shape=2.5, scale=40, size=5000)
```

## Buenas prácticas

1. Piensa en `shape` como "número de exponenciales sumadas" y en `scale` como `1/λ`.
2. Para una sola espera (`shape=1`) usa directamente [[np.random.exponential]], es más claro.
3. La suma de gammas con igual `scale` es otra gamma: útil para componer modelos.
4. Fija la semilla con [[np.random.seed]] para reproducibilidad.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Confundir `shape` (forma) con `size` (dimensiones) | Ambos se llaman parecido | `shape`=parámetro k, `size`=forma del array |
| `ValueError: shape < 0` | Forma o escala no positivas | Garantizar `shape > 0` y `scale > 0` |
| Media inesperada | Olvidar que media = `shape*scale` | Calibrar ambos parámetros juntos |
| Esperar valores negativos | La gamma es estrictamente positiva | Usar otra distribución si necesitas negativos |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.exponential]]
- [[np.random.chisquare]]
- [[np.random.seed]]
