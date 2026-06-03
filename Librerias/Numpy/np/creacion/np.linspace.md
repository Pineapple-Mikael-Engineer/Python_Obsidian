---
title: np.linspace — N puntos uniformes entre dos extremos
aliases:
  - linspace
  - np.linspace
tags:
  - numpy
  - api/funcion
  - creacion

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
  - concepto_dtype

draft: false
---

# np.linspace — N puntos uniformes entre dos extremos

## Firma de la función

```python
np.linspace(
    start,
    stop,
    num=50,
    endpoint=True,
    retstep=False,
    dtype=None,
    axis=0
) -> ndarray  |  (ndarray, float)
```

## Valor de retorno

Devuelve un [[concepto_ndarray|ndarray]] 1D con **exactamente `num` valores** equiespaciados entre `start` y `stop`. Por defecto el extremo `stop` **sí se incluye**.

| Llamada | Resultado |
|---------|-----------|
| `np.linspace(0, 1, 5)` | `[0., 0.25, 0.5, 0.75, 1.]` |
| `np.linspace(0, 10, 3)` | `[0., 5., 10.]` |
| `np.linspace(0, 1, 5, endpoint=False)` | `[0., 0.2, 0.4, 0.6, 0.8]` |

Si `retstep=True`, devuelve la tupla `(array, paso)`:

```python
import numpy as np
valores, paso = np.linspace(0, 1, 5, retstep=True)
paso   # 0.25
```

## Diferencia clave con `arange`

| Aspecto | `np.linspace` | [[np.arange]] |
|---------|---------------|---------------|
| Controlas | el **número de puntos** (`num`) | el **paso** (`step`) |
| Extremo `stop` | incluido por defecto | excluido |
| dtype por defecto | `float64` | inferido (int si son ints) |
| Riesgo de redondeo | nulo (cuenta exacta) | sí con paso flotante |

> Regla práctica: si sabes **cuántos puntos** quieres → `linspace`. Si sabes **el paso** → `arange`.

## Parámetros en detalle

### `start`, `stop` — extremos del intervalo

Primer y último valor. Con `endpoint=True` (por defecto), `stop` aparece en el resultado.

### `num` — cantidad de puntos

Entero ≥ 0. Define el [[concepto_shape|shape]] de salida: `(num,)`. Por defecto `50`.

```python
np.linspace(0, 1, 11)   # 11 puntos: 0.0, 0.1, ..., 1.0
np.linspace(0, 1, 1)    # [0.]  → un solo punto (el start)
```

### `endpoint` — incluir el extremo

| Valor | Efecto | Uso típico |
|-------|--------|------------|
| `True` (por defecto) | incluye `stop` | rangos cerrados, gráficas |
| `False` | excluye `stop` | muestreo periódico, bins |

```python
np.linspace(0, 2*np.pi, 4, endpoint=False)   # fases sin repetir el ciclo
```

### `retstep` — devolver también el paso

Si `True`, retorna `(array, step)`. Útil cuando necesitas la resolución del muestreo.

### `dtype` — tipo de salida

Por defecto `float64` aunque los extremos sean enteros (ver [[concepto_dtype]]).

### `axis` — eje del resultado (con start/stop array)

Cuando `start`/`stop` son arrays, controla en qué eje se coloca la dimensión de los `num` puntos.

## Casos de uso

### Eje X para graficar una función continua

```python
x = np.linspace(0, 2*np.pi, 200)   # suave, 200 puntos
y = np.sin(x)
```

### Interpolar entre dos valores

```python
inicio, fin = 10.0, 50.0
pasos = np.linspace(inicio, fin, 5)   # [10., 20., 30., 40., 50.]
```

### Bordes de bins sin solapamiento

```python
bins = np.linspace(0, 1, 11)          # 10 intervalos iguales en [0, 1]
```

### Rampa de color o de tiempo normalizado

```python
t = np.linspace(0, 1, num=len(frames))   # progreso 0..1 por frame
```

## Buenas prácticas

1. Para curvas suaves prefiere `linspace` sobre [[np.arange]]: garantiza el número de puntos y evita errores de redondeo.
2. Usa `endpoint=False` cuando muestrees señales periódicas (evita duplicar el extremo del ciclo).
3. Usa `retstep=True` si luego necesitas el paso (p. ej. para integración numérica).
4. Para espaciado **logarítmico** usa [[np.logspace]] en vez de aplicar `10**linspace(...)` a mano.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Un punto de más al concatenar ciclos | `endpoint=True` duplica el extremo | usar `endpoint=False` |
| `num` como si fuera el paso | confundirlo con `arange` | recordar: `num` = cantidad de puntos |
| Paso no es el esperado | `num` cuenta puntos, no intervalos | hay `num-1` intervalos; usar `retstep=True` para verlo |
| Resultado vacío | `num=0` | usar `num ≥ 1` |

## Limitaciones

- Solo produce espaciado **lineal**; para escala logarítmica usa [[np.logspace]].
- Siempre 1D respecto a `num`; combínalo con `reshape` o `meshgrid` para grids 2D.
- El dtype por defecto es flotante aunque los extremos sean enteros.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_dtype]]
- [[np.arange]]
- [[np.logspace]]
- [[np.meshgrid]]
- [[np.array]]
