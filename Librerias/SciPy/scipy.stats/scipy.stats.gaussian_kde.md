---
title: gaussian_kde — estimacion de densidad por nucleos (callable)
aliases:
  - gaussian_kde
  - scipy.stats.gaussian_kde
  - KDE gaussiano
tags:
  - scipy
  - api/clase
  - estadistica
lib: scipy
tipo: clase
mod: scipy.stats
requiere:
  - numpy
draft: false
---

# gaussian_kde — estimacion de densidad por nucleos (callable)

Clase que estima la **funcion de densidad de probabilidad (pdf)** de una variable a partir de una muestra, **sin asumir** una distribucion parametrica (no supone normal, exponencial, etc.). Es la version continua y suave de un histograma: coloca un **nucleo gaussiano** centrado en cada dato y los suma. Se **construye** con los datos y luego se **EVALUA como callable**: `kde(puntos)` devuelve la densidad estimada en esos puntos. El parametro critico es `bw_method`, el ancho de banda que controla el suavizado.

## Constructor

```python
scipy.stats.gaussian_kde(
    dataset,            # array_like: muestra. 1D (n,) o multivariado (d, n): filas = dimensiones
    bw_method=None,     # 'scott' | 'silverman' | escalar | callable: ancho de banda (suavizado)
    weights=None,       # array_like (n,) | None: pesos por dato (None = uniforme)
)                       # -> callable kde(points) -> ndarray de densidades
```

## Metodos principales

| Miembro | Tipo | Significado |
|---------|------|-------------|
| `kde(points)` / `kde.evaluate(points)` | call | Densidad estimada en `points` (callable principal) |
| `kde.pdf(x)` | metodo | Alias de `evaluate`; pdf en `x` |
| `kde.logpdf(x)` | metodo | Log de la densidad (estable para colas) |
| `kde.resample(size=None)` | metodo | Muestrea `size` datos nuevos generados por el kde |
| `kde.integrate_box_1d(low, high)` | metodo | Probabilidad acumulada en `[low, high]` (solo 1D) |
| `kde.integrate_box(low, high)` | metodo | Integral sobre una caja N-D |
| `kde.factor` | atributo | Factor de ancho de banda efectivo |
| `kde.covariance` | atributo | Matriz de covarianza del nucleo (datos * factor**2) |
| `kde.n` / `kde.d` | atributo | Numero de datos / dimensiones |

## Parametros en detalle

### `bw_method` (ancho de banda, parametro CRITICO)

Controla cuanto se **suaviza** la densidad. Es el unico parametro que cambia de forma visible el resultado:

| Valor | Significado | Efecto |
|-------|-------------|--------|
| `'scott'` (default) | Regla de Scott: `n**(-1/(d+4))` | Buen punto de partida general |
| `'silverman'` | Regla de Silverman | Algo mas suave; clasico para datos casi normales |
| escalar (float) | Multiplica la covarianza por `factor**2` | Control manual directo |
| callable | Funcion `f(kde) -> factor` | Reglas personalizadas |

Intuicion: **poco** ancho de banda = densidad **ruidosa** con muchos picos (sobreajuste, se ve el ruido muestral); **mucho** ancho = densidad **excesivamente suave** que borra estructura real (bimodalidad, asimetria). Conviene probar varios valores y comparar contra el histograma.

### `dataset` (forma de los datos)

- **1D**: pasa un array `(n,)`.
- **Multivariado**: pasa `(d, n)` donde **cada fila es una dimension** y cada columna una observacion (ojo: es la traspuesta de la convencion habitual filas=muestras).

### `weights`

Pondera cada observacion. Util cuando la muestra proviene de un muestreo no uniforme o lleva pesos de importancia. Por defecto todos los datos pesan igual.

## Casos de uso

### Construir el kde y evaluarlo

```python
import numpy as np
from scipy.stats import gaussian_kde

datos = np.concatenate([np.random.normal(0, 1, 300),
                        np.random.normal(4, 0.5, 200)])  # muestra bimodal
kde = gaussian_kde(datos)               # se construye con los datos

x = np.linspace(-4, 7, 200)
dens = kde(x)                            # se EVALUA: densidad estimada en x
kde.integrate_box_1d(-np.inf, 0)         # → P(X < 0) aprox segun el kde
```

### Densidad estimada vs histograma (uso tipico)

```python
import matplotlib.pyplot as plt

plt.hist(datos, bins=30, density=True, alpha=0.4)  # density=True para que escale igual
plt.plot(x, kde(x), lw=2)                            # KDE superpuesto al histograma
```

El `density=True` del histograma es clave: hace que el area sea 1, comparable con la pdf del kde.

### Comparar anchos de banda

```python
kde_fino  = gaussian_kde(datos, bw_method=0.1)   # ruidoso, muchos picos
kde_ancho = gaussian_kde(datos, bw_method=0.8)   # demasiado suave, pierde la bimodalidad
```

### Muestrear nuevos datos del kde

```python
nuevos = kde.resample(size=1000)         # genera datos sinteticos con la misma forma
```

## Buenas practicas

1. Compara siempre la curva KDE **contra el histograma** (`density=True`) para validar el ancho de banda.
2. Empieza con `'scott'` o `'silverman'`; ajusta a mano solo si el resultado se ve sobre o infra suavizado.
3. Para datos **acotados** (positivos, proporciones), recuerda que el KDE gaussiano **filtra masa fuera del soporte**; transforma (p.ej. log) antes de estimar si el borde importa.
4. En multivariado, ordena el dataset como `(d, n)` para evitar resultados sin sentido.
5. Usa `logpdf` en lugar de `log(pdf)` cuando trabajes con verosimilitudes en las colas.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `LinAlgError: singular matrix` | Datos colineales o sin varianza (todos iguales) | Comprobar que la muestra tiene dispersion real |
| Densidad plana o con un solo pico | `dataset` con forma `(n, d)` en multivariado | Trasponer a `(d, n)`: filas = dimensiones |
| KDE no encaja con el histograma | Histograma sin `density=True` | Usar `density=True` para que ambos tengan area 1 |
| Curva ruidosa / sobreajustada | `bw_method` demasiado pequeno | Aumentar el ancho de banda |
| Estructura borrada (bimodalidad perdida) | `bw_method` demasiado grande | Reducir el ancho de banda |
| Masa de probabilidad fuera del rango fisico | Soporte acotado con nucleo gaussiano | Transformar los datos antes del KDE |

## Limitaciones

- Asume **nucleo gaussiano** y un **unico ancho de banda** global: no se adapta a regiones de densidad muy distinta.
- Mala estimacion cerca de **bordes** del soporte (sangra densidad fuera del rango).
- Sensible al ancho de banda: el resultado puede variar mucho con `bw_method`.
- Coste y fiabilidad **empeoran en alta dimension** (maldicion de la dimensionalidad); util sobre todo en 1D-2D.
- Suaviza, pero **no es robusto** a outliers extremos: pueden generar colas artificiales.

## Notas relacionadas

- [[scipy.stats.norm]]
- [[scipy.stats.rv_histogram]]
- [[numpy.histogram]]
