---
title: np.roll — Desplazar elementos circularmente
aliases:
  - roll
  - np.roll
  - desplazamiento circular
tags:
  - numpy
  - api/funcion
  - manipulacion

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
  - concepto_axis_parametro

draft: false
---

# np.roll — Desplazar elementos circularmente

## Firma de la función

```python
np.roll(
    a,
    shift,
    axis=None
) -> ndarray
```

## Valor de retorno

Devuelve un array con los elementos **desplazados** `shift` posiciones; los que salen por un extremo **reaparecen por el otro** (desplazamiento circular). No se pierde ningún valor.

| Entrada | `shift` | `axis` | Salida |
|---------|---------|--------|--------|
| `[0,1,2,3,4]` | `2` | `None` | `[3,4,0,1,2]` |
| `[0,1,2,3,4]` | `-1` | `None` | `[1,2,3,4,0]` |

```python
import numpy as np
np.roll(np.arange(5), 2)    # array([3, 4, 0, 1, 2])
np.roll(np.arange(5), -1)   # array([1, 2, 3, 4, 0])
```

## Parámetros en detalle

### `a` — array de entrada

Array de cualquier dimensión.

### `shift` — cuántas posiciones

Entero (positivo = hacia la derecha/abajo, negativo = izquierda/arriba). Puede ser tupla para desplazar varios ejes a la vez.

### `axis` — eje del desplazamiento

`None` aplana, desplaza y restaura el shape. Un entero desplaza solo ese [[concepto_axis_parametro|eje]].

```python
M = np.arange(6).reshape(2, 3)
np.roll(M, 1, axis=0)   # desplaza filas
np.roll(M, 1, axis=1)   # desplaza columnas
```

## Casos de uso

### Calcular diferencias circulares (vecino siguiente)

```python
x = np.array([10, 20, 30, 40])
siguiente = np.roll(x, -1)         # [20, 30, 40, 10]
delta = siguiente - x             # diferencia con el vecino
```

### Rotar una señal periódica

```python
señal = np.sin(np.linspace(0, 2*np.pi, 100))
desfasada = np.roll(señal, 25)     # desfase de cuarto de ciclo
```

## Buenas prácticas

1. Es **circular**: ningún dato se pierde, a diferencia de un shift con relleno.
2. Si necesitas desplazar y rellenar con ceros (no circular), usa slicing o `np.pad`.
3. `shift` y `axis` como tuplas permiten desplazar varios ejes en una llamada.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar relleno con ceros | `roll` es circular | usar slicing/`np.pad` para shift con relleno |
| Matriz aplanada inesperadamente | `axis=None` por defecto | pasar `axis` |
| Sentido del desplazamiento contrario | signo de `shift` | positivo = derecha/abajo |

## Limitaciones

- No rellena: siempre reintroduce los elementos por el extremo opuesto.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_axis_parametro]]
- [[np.repeat]]
- [[np.tile]]
