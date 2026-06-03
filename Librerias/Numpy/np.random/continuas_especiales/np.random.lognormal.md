---
title: np.random.lognormal — Muestras de la distribución log-normal
aliases: [lognormal, random.lognormal, np.random.lognormal]
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

# np.random.lognormal — Muestras de la distribución log-normal

Modela **magnitudes positivas que surgen de efectos multiplicativos**: una variable es log-normal cuando su logaritmo es normal. Aparece donde el crecimiento es proporcional (precios, ingresos, tamaños de archivo, concentraciones, tiempos de respuesta). Sus parámetros `mean` y `sigma` describen la normal subyacente del logaritmo, **no** la media y desviación de los valores finales.

## Firma de la función

```python
np.random.lognormal(
    mean=0.0,
    sigma=1.0,
    size=None
) -> ndarray | float
```

## Valor de retorno

Devuelve reales estrictamente positivos. Si `Y ~ Normal(mean, sigma²)`, entonces `X = exp(Y)` es lo que se muestrea. La media de `X` es `exp(mean + sigma²/2)`, mayor que `exp(mean)` por la asimetría; la distribución tiene cola larga a la derecha.

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `size=None` | `float` positivo | `2.31` |
| `lognormal(0, 1, size=4)` | `ndarray (4,)` | `[0.7, 2.4, 1.1, 5.9]` |
| `sigma` grande | cola más larga | valores muy dispersos |
| `lognormal(0, 1, (2,3))` | `ndarray (2,3)` | matriz positiva |

```python
import numpy as np
np.random.seed(0)
np.random.lognormal(mean=0.0, sigma=1.0, size=3)
# array([5.73, 1.49, 2.65])  → mediana ≈ exp(0) = 1, media ≈ exp(0.5)
```

## Parámetros en detalle

### `mean` — media del logaritmo (escala / mediana)

Media de la normal subyacente. Como `exp(mean)` es la **mediana** de la log-normal, este parámetro fija el orden de magnitud central. Puede ser cualquier real (positivo o negativo).

```python
np.random.lognormal(mean=0.0)   # mediana ≈ 1
np.random.lognormal(mean=3.0)   # mediana ≈ exp(3) ≈ 20
```

### `sigma` — desviación del logaritmo (forma / dispersión)

Desviación estándar de la normal subyacente. Controla la asimetría y el ancho: con `sigma` pequeño es casi simétrica; con `sigma` grande la cola derecha se dispara. Debe ser `> 0`.

```python
np.random.lognormal(0, 0.25)   # estrecha, casi simétrica
np.random.lognormal(0, 1.5)    # muy asimétrica, cola larga
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del array; `None` devuelve un escalar.

```python
np.random.lognormal(0, 1, size=1000)    # vector (1000,)
np.random.lognormal(0, 1, size=(4, 4))  # matriz (4, 4)
```

## Casos de uso

### Simular precios o ingresos con sesgo positivo

```python
# Ingresos con mediana ≈ exp(10) ≈ 22026 y dispersión moderada
ingresos = np.random.lognormal(mean=10, sigma=0.5, size=10000)
np.median(ingresos)   # ≈ 22026
ingresos.mean()       # mayor que la mediana por la cola derecha
```

### Calibrar a partir de datos reales

```python
datos = np.array([12.0, 18.0, 9.0, 30.0, 22.0])
log = np.log(datos)
sim = np.random.lognormal(mean=log.mean(), sigma=log.std(), size=1000)
```

## Buenas prácticas

1. `mean` y `sigma` describen el **logaritmo**, no los valores finales: calíbralos sobre `np.log(datos)`.
2. Usa `exp(mean)` como mediana de referencia y recuerda que la media siempre la supera.
3. Si tu fenómeno es aditivo (no multiplicativo) usa la normal [[np.random.randn]] en su lugar.
4. Fija la semilla con [[np.random.seed]] para reproducir las muestras.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Pasar la media de los valores como `mean` | `mean` es la media del log | Usar `np.log(datos).mean()` |
| `ValueError: sigma < 0` | Desviación negativa | Garantizar `sigma > 0` |
| Media muestral mayor que la esperada | Media = `exp(mean+sigma²/2)`, no `exp(mean)` | Comparar con la fórmula correcta |
| Valores negativos esperados | La log-normal es siempre positiva | Usar la normal si necesitas negativos |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.randn]]
- [[np.random.gamma]]
- [[np.random.seed]]
