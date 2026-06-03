---
title: np.polyval — Evaluar un polinomio en puntos
aliases:
  - polyval
  - np.polyval
tags:
  - numpy
  - api/funcion
  - polinomios

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_broadcasting

draft: false
---

# np.polyval — Evaluar un polinomio en puntos

## Firma de la función

```python
np.polyval(p, x) -> ndarray | escalar
```

## Valor de retorno

Evalúa el polinomio de coeficientes `p` (de mayor a menor potencia) en `x`. Pareja natural de [[np.polyfit]].

```python
import numpy as np
p = [1, 0, -1]                 # x² - 1
np.polyval(p, 2)               # 3   → 2² - 1
np.polyval(p, [0, 1, 2])       # [-1, 0, 3]
```

## Parámetros en detalle

### `p` — coeficientes

Array (o [[np.poly1d]]) de mayor a menor grado: `[a, b, c]` representa `a·x² + b·x + c`.

### `x` — punto(s) de evaluación

Escalar o array (se evalúa elemento a elemento por [[concepto_broadcasting|broadcasting]]).

## Casos de uso

### Predecir con un ajuste

```python
coef = np.polyfit(x, y, 3)
curva = np.polyval(coef, x_fino)
```

### Curva suave para graficar

```python
x_fino = np.linspace(x.min(), x.max(), 500)
y_fino = np.polyval(coef, x_fino)
```

## Buenas prácticas

1. Usa los mismos coeficientes que devuelve [[np.polyfit]] (mismo orden).
2. Un objeto [[np.poly1d]] es **callable**: `p(x)` equivale a `polyval(p, x)`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado invertido | orden de `p` al revés | recordar: mayor → menor grado |

## Limitaciones

- Asume el orden de coeficientes de mayor a menor.

## Notas relacionadas

- [[concepto_broadcasting]]
- [[np.polyfit]]
- [[np.poly1d]]
