---
title: np.random.binomial — Nº de éxitos en n ensayos Bernoulli
aliases:
  - binomial
  - random.binomial
  - np.random.binomial
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray o int
inplace: false
draft: false
---

# np.random.binomial — Nº de éxitos en n ensayos Bernoulli

Muestrea de una **distribución binomial**: el número de éxitos en `n` ensayos independientes, cada uno con probabilidad de éxito `p`. Cada muestra es un entero en `[0, n]`. Equivale a contar cuántas caras salen al lanzar `n` monedas sesgadas.

## Firma de la función

```python
np.random.binomial(
    n,
    p,
    size=None
) -> ndarray | int
```

## Valor de retorno

Devuelve un entero o un [[concepto_ndarray|ndarray]] con el [[concepto_shape|shape]] de `size`. Cada valor está en `0..n` y tiene media `n*p` y varianza `n*p*(1-p)`.

| Llamada | Significado | Retorno |
|---------|-------------|---------|
| `np.random.binomial(10, 0.5)` | caras en 10 monedas justas | `int` en 0..10 |
| `np.random.binomial(1, 0.3)` | un ensayo Bernoulli | `0` o `1` |
| `np.random.binomial(100, 0.2, size=5)` | 5 experimentos de 100 ensayos | `ndarray` shape `(5,)` |

```python
import numpy as np
np.random.binomial(10, 0.5, size=8)
# array([5, 4, 6, 7, 3, 5, 4, 6])  # alrededor de n*p = 5
```

## Parámetros en detalle

### `n` — número de ensayos

Entero ≥ 0. Define el máximo posible de cada muestra. Puede ser un array para vectorizar (broadcasting con `p`).

```python
np.random.binomial(20, 0.5)   # éxitos en 20 ensayos → 0..20
```

### `p` — probabilidad de éxito por ensayo

Float en `[0, 1]`. Controla el sesgo: `p=0.5` simétrico, `p` alto desplaza la media hacia `n`.

```python
np.random.binomial(10, 0.1)   # media ≈ 1 (pocos éxitos)
np.random.binomial(10, 0.9)   # media ≈ 9 (casi todos)
```

### `size` — forma de la salida

Entero o tupla que fija el [[concepto_shape|shape]]. `None` devuelve un escalar.

```python
np.random.binomial(5, 0.5, size=(2, 3))  # shape (2, 3)
```

## Casos de uso

### Simular tasa de conversión

```python
# 1000 visitas, 4% de conversión, repetido 30 días
conversiones = np.random.binomial(1000, 0.04, size=30)
conversiones.mean()   # ≈ 40
```

### Caso Bernoulli (n=1) como moneda

```python
lanzamientos = np.random.binomial(1, 0.5, size=10)  # 0/1
```

### Aproximar la distribución empírica

```python
muestras = np.random.binomial(10, 0.3, size=100_000)
np.bincount(muestras) / muestras.size   # frecuencia por nº de éxitos
```

## Buenas prácticas

1. Para un único ensayo binario usa `n=1` (Bernoulli); para 0/1 sueltos también sirve [[np.random.randint]] con `[0, 2)`.
2. Verifica que `0 <= p <= 1`; valores fuera lanzan error.
3. Cuando `n` es grande y `p` pequeño, la binomial se aproxima a [[np.random.poisson]] con `lam = n*p`.
4. Fija la semilla para reproducir simulaciones.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: p < 0, p > 1` | probabilidad fuera de rango | usar `p` en `[0, 1]` |
| `ValueError: n < 0` | ensayos negativos | `n` entero ≥ 0 |
| Confundir resultado con `p` | devuelve **conteo**, no proporción | dividir por `n` si quieres tasa |
| Esperar floats | la salida es entera | normalizar manualmente si hace falta |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.poisson]]
- [[np.random.randint]]
- [[np.random.choice]]
