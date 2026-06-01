---
title: np.polyfit — Ajustar un polinomio por mínimos cuadrados
aliases:
  - polyfit
  - np.polyfit
  - ajuste polinomial
tags:
  - numpy
  - api/funcion
  - polinomios

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape

draft: false
---

# np.polyfit — Ajustar un polinomio por mínimos cuadrados

## Firma de la función

```python
np.polyfit(
    x,
    y,
    deg,
    rcond=None,
    full=False,
    w=None,
    cov=False
) -> ndarray
```

## Valor de retorno

Devuelve los **coeficientes** del polinomio de grado `deg` que mejor ajusta los puntos `(x, y)` por mínimos cuadrados. Los coeficientes van de **mayor a menor** potencia.

| `deg` | Retorno | Modelo |
|-------|---------|--------|
| `1` | `[m, b]` | recta `m·x + b` |
| `2` | `[a, b, c]` | parábola `a·x² + b·x + c` |

```python
import numpy as np
x = np.array([0, 1, 2, 3])
y = np.array([1, 3, 7, 13])
coef = np.polyfit(x, y, 2)        # [1., 1., 1.] → x² + x + 1
```

## Evaluar el ajuste

Combina con [[np.polyval]] para predecir:

```python
coef = np.polyfit(x, y, 2)
y_pred = np.polyval(coef, x_nuevo)
```

## Parámetros en detalle

### `x`, `y` — datos

Arrays 1D de la misma longitud.

### `deg` — grado del polinomio

Entero. Cuidado: grados altos **sobreajustan** (oscilan entre puntos).

### `w` — pesos

Da más importancia a ciertos puntos en el ajuste.

### `cov` / `full` — diagnósticos

Devuelven la matriz de covarianza o información del residuo.

## Casos de uso

### Regresión lineal simple

```python
m, b = np.polyfit(x, y, 1)
```

### Tendencia de una serie

```python
coef = np.polyfit(np.arange(len(serie)), serie, 1)
pendiente = coef[0]
```

## Buenas prácticas

1. Empareja siempre con [[np.polyval]] (o [[np.poly1d]]) para evaluar.
2. Evita grados altos: sobreajustan (oscilaciones de Runge).
3. La API moderna recomendada es `np.polynomial.Polynomial.fit` (más estable numéricamente).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RankWarning: poly badly conditioned` | grado alto / x sin escalar | bajar grado o normalizar `x` |
| Predicciones absurdas fuera del rango | extrapolación | no extrapolar lejos de los datos |

## Limitaciones

- Numéricamente inestable con grados altos; preferir la API `polynomial`.

## Notas relacionadas

- [[concepto_shape]]
- [[np.polyval]]
- [[np.poly1d]]
- [[np.roots]]
