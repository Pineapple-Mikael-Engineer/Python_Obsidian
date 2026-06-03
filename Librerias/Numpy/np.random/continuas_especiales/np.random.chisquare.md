---
title: np.random.chisquare — Muestras de la distribución chi-cuadrado
aliases: [chisquare, random.chisquare, np.random.chisquare]
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

# np.random.chisquare — Muestras de la distribución chi-cuadrado

Modela la **suma de cuadrados de `df` normales estándar** independientes. Es la distribución de referencia en **tests de hipótesis** (bondad de ajuste, independencia en tablas de contingencia) y en la estimación de varianzas. Su único parámetro es `df`, los grados de libertad.

## Firma de la función

```python
np.random.chisquare(
    df,
    size=None
) -> ndarray | float
```

## Valor de retorno

Devuelve reales no negativos cuya media tiende a `df` y cuya varianza tiende a `2·df`. Es un caso particular de la gamma (`shape=df/2`, `scale=2`); por eso siempre es positiva y asimétrica, acercándose a una normal cuando `df` crece.

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `chisquare(2)` con `size=None` | `float` | `1.37` |
| `chisquare(2, size=4)` | `ndarray (4,)` | `[0.9, 3.1, 1.2, 0.4]` |
| `chisquare(10)` | media ≈ 10 | menos asimétrica |
| `chisquare(5, size=(2,3))` | `ndarray (2,3)` | matriz positiva |

```python
import numpy as np
np.random.seed(0)
np.random.chisquare(df=4, size=3)
# array([3.21, 5.84, 2.10])  → media tiende a df = 4
```

## Parámetros en detalle

### `df` — grados de libertad

Número de normales estándar al cuadrado que se suman. Fija tanto la media (`df`) como la asimetría: con pocos `df` la distribución es muy sesgada a la derecha; con muchos se vuelve casi simétrica. Debe ser `> 0` (admite valores no enteros).

```python
np.random.chisquare(1)    # muy asimétrica, masa cerca de 0
np.random.chisquare(30)   # casi acampanada
np.random.chisquare(2.5)  # df no entero es válido
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del array; `None` devuelve un escalar.

```python
np.random.chisquare(4, size=1000)    # vector (1000,)
np.random.chisquare(4, size=(5, 5))  # matriz (5, 5)
```

## Casos de uso

### Distribución nula de un estadístico chi-cuadrado por simulación

```python
# Test con 6 categorías → df = 6-1 = 5; aproximar la nula y un valor crítico
nula = np.random.chisquare(df=5, size=100000)
critico_95 = np.percentile(nula, 95)   # umbral de rechazo al 5%
```

### Verificar empíricamente media y varianza

```python
m = np.random.chisquare(df=8, size=100000)
m.mean()   # ≈ 8     (df)
m.var()    # ≈ 16    (2*df)
```

## Buenas prácticas

1. Asocia siempre `df` con los grados de libertad del test (categorías − 1, o filas-1 × columnas-1).
2. Recuerda media = `df` y varianza = `2·df` para validar tus simulaciones.
3. Es equivalente a `gamma(shape=df/2, scale=2)`: usa [[np.random.gamma]] si necesitas más flexibilidad.
4. Fija la semilla con [[np.random.seed]] para reproducir la distribución nula.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: df <= 0` | Grados de libertad no positivos | Garantizar `df > 0` |
| Media inesperada | Olvidar que la media es `df` | Ajustar `df` al estadístico real |
| Esperar simetría con `df` bajo | Con pocos `df` es muy asimétrica | Subir `df` o aceptar el sesgo |
| Valores negativos esperados | La chi-cuadrado es siempre ≥ 0 | Usar la t o la normal si necesitas negativos |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.gamma]]
- [[np.random.randn]]
- [[np.random.seed]]
