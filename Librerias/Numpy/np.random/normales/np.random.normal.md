---
title: np.random.normal — muestrea la normal general N(loc, scale²) con media y desviación arbitrarias
aliases:
  - normal
  - np.random.normal
  - random.normal
  - distribucion normal
tags:
  - numpy
  - api/funcion
  - aleatorio

# --- Clasificación ---
lib: numpy
mod: np.random
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
draft: false
---

# np.random.normal — muestrea la normal general N(loc, scale²) con media y desviación arbitrarias

`np.random.normal` extrae muestras de una distribución **normal (gaussiana)** con media `loc` ($\mu$) y desviación típica `scale` ($\sigma$) arbitrarias. Es la **más general** de la familia normal: `standard_normal` y `randn` son el caso particular $\mu=0,\ \sigma=1$. Su salida es un [[concepto_shape|shape]] gobernado por `size`, que decide cuántas muestras y con qué forma se devuelven. La pregunta al usarla no es "¿normal?" sino **"¿qué media, qué desviación y qué `size`?"**.

## La idea

La distribución normal $N(\mu, \sigma^2)$ es la campana de Gauss: simétrica alrededor de la media $\mu$, con anchura controlada por la desviación $\sigma$. Aparece en errores de medida, ruido y como límite del **teorema central del límite** (la suma de muchas variables independientes tiende a una normal). Su densidad de probabilidad (PDF) es:

$$ f(x) = \frac{1}{\sigma\sqrt{2\pi}}\, e^{-\frac{(x-\mu)^2}{2\sigma^2}} $$

El factor $\frac{1}{\sigma\sqrt{2\pi}}$ normaliza el área a 1; el exponente $-(x-\mu)^2/2\sigma^2$ es la campana centrada en $\mu$. La relación clave: una muestra de $N(\mu,\sigma^2)$ es una muestra estándar $z\sim N(0,1)$ desplazada y escalada,

$$ x = \mu + \sigma\, z \qquad\Longleftrightarrow\qquad \texttt{normal(loc, scale, size)} \equiv \texttt{loc + scale * standard\_normal(size)} $$

Eso es exactamente lo que `loc` y `scale` hacen: mover el centro y estirar la anchura. La media estimada de las muestras se calcula con [[np.mean]] y su desviación con [[np.std]] (debe rondar `scale`).

> [!tip] Versión moderna
> La API legacy (`np.random.normal`) usa el **estado global** del generador, que `np.random.seed` modifica de forma compartida y poco segura en código concurrente. La forma recomendada hoy es crear un generador propio con [[np.random.default_rng]] y llamar a su método `normal`:
> ```python
> rng = np.random.default_rng()        # o default_rng(seed) para reproducir
> rng.normal(loc=5, scale=2, size=(2, 3))
> ```
> Mismo muestreo, sin estado global. La nota documenta la legacy por ubicuidad, pero en código nuevo usa `rng.normal(...)`.

## Firma

```python
np.random.normal(
    loc=0.0,      # float | array_like: media μ de la distribución
    scale=1.0,    # float | array_like: desviación típica σ (debe ser ≥ 0)
    size=None,    # None | int | tuple[int]: forma de la salida
) -> ndarray | float
```

## Los parámetros en detalle

### `loc` — la media $\mu$
Centro de la campana. Por defecto `0.0`. Puede ser un escalar o un `array_like`; en ese caso se combina con `scale` por [[concepto_broadcasting|broadcasting]], generando una muestra por cada par `(loc, scale)`.

```python
np.random.normal(loc=100, size=5)        # 5 muestras centradas en 100
np.random.normal(loc=[0, 10, 100])       # una muestra por cada media → shape (3,)
```

### `scale` — la desviación típica $\sigma$
Anchura de la campana; debe ser **≥ 0** (un `scale < 0` lanza `ValueError`). Por defecto `1.0`. **No es la varianza**: la varianza es `scale²`. Para fijar una varianza $v$, pasa `scale = sqrt(v)`.

```python
np.random.normal(scale=10, size=5)       # muestras muy dispersas (σ=10)
np.random.normal(scale=0, size=3)        # σ=0 → todas valen exactamente loc
```

### `size` — la forma de la salida
Entero (vector) o tupla (tensor). Con `None` (defecto) devuelve **un escalar** `float` (salvo que `loc`/`scale` sean arrays, en cuyo caso el shape sale del broadcasting). Es el parámetro que decide cuántas muestras y con qué forma; se detalla en la sección siguiente.

```python
np.random.normal(0, 1, 5)        # (5,)    vector
np.random.normal(0, 1, (2, 3))   # (2, 3)  matriz
np.random.normal(0, 1)           # escalar float
```

## size y la forma de salida

`size` se traslada **literalmente** al shape de la salida: no hay reducción ni contracción, cada posición del tensor recibe una muestra independiente de $N(\mu,\sigma^2)$. El mapa es la identidad sobre la forma:

$$ \texttt{size}=(n_0,\dots,n_{k-1}) \ \xrightarrow{\ \text{normal}\ }\ \texttt{salida.shape}=(n_0,\dots,n_{k-1}) $$

| Llamada | Distribución | Shape de salida | dtype |
|---------|--------------|-----------------|-------|
| `np.random.normal()` | N(0, 1) | `()` escalar | `float` |
| `np.random.normal(5, 2)` | N(5, 4) | `()` escalar | `float` |
| `np.random.normal(0, 1, 3)` | N(0, 1) | `(3,)` | `float64` |
| `np.random.normal(5, 2, (2, 3))` | N(5, 4) | `(2, 3)` | `float64` |

En aprendizaje automático y visión por computador los lotes de datos viven en 4D o 5D, y `size` produce ese tensor de golpe. Un lote de 2 imágenes RGB-como-canales de 64×64 (formato `(lote, canales, alto, ancho)`):

```python
import numpy as np
ruido = np.random.normal(0, 1, size=(2, 3, 64, 64))
ruido.shape      # (2, 3, 64, 64)  → 4D: lote=2, canales=3, alto=64, ancho=64
ruido.size       # 2*3*64*64 = 24_576 muestras independientes ~ N(0,1)

# 5D: un lote de clips de vídeo (lote, tiempo, canales, alto, ancho)
vol = np.random.normal(loc=0, scale=1, size=(4, 8, 3, 32, 32))
vol.shape        # (4, 8, 3, 32, 32)
```

Cada uno de esos cientos de miles de valores es una muestra gaussiana independiente; `size` solo decide cómo se empaquetan en la malla del tensor.

## Casos de uso

### Datos sintéticos con media física conocida
```python
temperaturas = np.random.normal(loc=22.5, scale=1.8, size=24)   # °C por hora
temperaturas.mean()   # ≈ 22.5
```

### Ruido gaussiano sobre una señal
```python
señal = np.linspace(0, 1, 100)
observado = señal + np.random.normal(0, 0.05, size=señal.shape)
```

### Equivalencia con la estándar escalada
```python
# Las dos líneas muestrean la misma distribución N(50, 25):
np.random.normal(loc=50, scale=5, size=1000)
50 + 5 * np.random.standard_normal(1000)     # μ + σ·z
```

### Parámetros vectorizados (broadcasting)
```python
medias = np.array([0., 10., 100.])
np.random.normal(loc=medias, scale=[1, 2, 3])   # shape (3,): una muestra por par (μ,σ)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: scale < 0` | desviación negativa | usar `scale >= 0` |
| Dispersión inesperada | confundir `scale` (σ) con la varianza (σ²) | pasar `scale = sqrt(varianza)` |
| Shape de salida inesperado | `loc`/`scale` son arrays y dominan el broadcasting | fijar `size` explícito o alinear shapes |
| `TypeError`/shape raro al pasar dimensiones sueltas | `normal(0, 1, 2, 3)` no es válido | usar `size=(2, 3)` |
| Resultados no reproducibles | falta semilla (estado global) | usar `rng = np.random.default_rng(seed)` |

## Notas relacionadas

- [[concepto_shape]] — cómo `size` define la forma de salida
- [[np.random.default_rng]] — el generador moderno sin estado global
- [[np.random.standard_normal]] · [[np.random.randn]] — el caso N(0,1)
- [[np.mean]] · [[np.std]] — recuperar μ y σ de las muestras
- [[np.random.seed]] — reproducibilidad en la API legacy
