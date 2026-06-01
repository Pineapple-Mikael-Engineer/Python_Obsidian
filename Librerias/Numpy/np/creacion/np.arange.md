---
title: np.arange — Secuencia por paso constante
aliases:
  - arange
  - np.arange
  - rango
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

# np.arange — Secuencia por paso constante

## Firma de la función

```python
np.arange(
    [start,]
    stop,
    [step,]
    dtype=None,
    *,
    like=None
) -> ndarray
```

El número de argumentos posicionales cambia su significado (estilo `range` de Python).

## Valor de retorno

Devuelve un [[concepto_ndarray|ndarray]] 1D con valores espaciados uniformemente en el intervalo **`[start, stop)`** (fin **excluido**), con paso `step`.

| Llamada | Resultado | Nota |
|---------|-----------|------|
| `np.arange(5)` | `[0, 1, 2, 3, 4]` | start=0, step=1, stop excluido |
| `np.arange(2, 7)` | `[2, 3, 4, 5, 6]` | start..stop-1 |
| `np.arange(0, 10, 2)` | `[0, 2, 4, 6, 8]` | paso 2 |
| `np.arange(0, 1, 0.25)` | `[0., 0.25, 0.5, 0.75]` | paso flotante |
| `np.arange(5, 0, -1)` | `[5, 4, 3, 2, 1]` | paso negativo |

```python
import numpy as np
np.arange(5)         # array([0, 1, 2, 3, 4])
np.arange(1, 4)      # array([1, 2, 3])
```

## Formas básicas de llamada

| Argumentos | Interpretación | Ejemplo |
|------------|----------------|---------|
| `arange(stop)` | start=0, step=1 | `np.arange(4)` → `[0,1,2,3]` |
| `arange(start, stop)` | step=1 | `np.arange(2, 5)` → `[2,3,4]` |
| `arange(start, stop, step)` | completo | `np.arange(0, 1, 0.2)` |

## Parámetros en detalle

### `start` — inicio (incluido)

Primer valor de la secuencia. Si se omite, vale `0`.

### `stop` — fin (excluido)

Límite superior **no incluido**. Es la diferencia clave frente a [[np.linspace]], que sí incluye el extremo.

```python
np.arange(0, 5)    # [0, 1, 2, 3, 4]  → 5 NO aparece
```

### `step` — paso

Distancia entre valores consecutivos. Puede ser negativo (secuencia descendente) o flotante. No puede ser `0`.

```python
np.arange(10, 0, -2)   # [10, 8, 6, 4, 2]
np.arange(0, 2, 0.5)   # [0., 0.5, 1., 1.5]
```

### `dtype` — tipo de salida

Si se omite, se infiere de los argumentos: enteros → `int64`, alguno flotante → `float64` (ver [[concepto_dtype]]).

## Casos de uso

### Índices o ejes para iterar

```python
for i in np.arange(len(datos)):
    procesar(datos[i])
```

### Eje temporal discreto

```python
muestras = np.arange(0, 100)          # 0..99
```

### Generar un grid junto a reshape

```python
grid = np.arange(12).reshape(3, 4)    # matriz 3x4 con 0..11
```

## Buenas prácticas

1. Para **número exacto de puntos** entre dos extremos, usa [[np.linspace]] (control preciso, sin error de redondeo).
2. Usa `arange` con **enteros**; con `step` flotante el conteo puede ser impredecible por redondeo.
3. Recuerda que `stop` se excluye: para incluirlo, suma el paso o usa `linspace`.
4. Para secuencias logarítmicas, usa [[np.logspace]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Falta el último valor esperado | `stop` es exclusivo | ampliar `stop` o usar [[np.linspace]] |
| Longitud inesperada con paso flotante | error de redondeo binario | preferir [[np.linspace]] con `num` |
| `ZeroDivisionError` / array vacío | `step=0` o `start==stop` | usar paso ≠ 0 |
| Secuencia vacía | dirección del paso no coincide | `arange(5, 0)` da `[]`; usar `step=-1` |

## Limitaciones

- Con pasos flotantes, el número de elementos no siempre es predecible: para eso existe [[np.linspace]].
- Solo produce progresiones aritméticas (paso constante); para escala logarítmica usa [[np.logspace]].
- Siempre es 1D; combina con `reshape` para más dimensiones.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_dtype]]
- [[np.linspace]]
- [[np.logspace]]
- [[np.reshape]]
- [[np.array]]
