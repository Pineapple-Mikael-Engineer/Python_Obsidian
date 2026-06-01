---
title: ndarray.round — Redondear los valores del array a n decimales
aliases:
  - round
  - ndarray.round
tags:
  - numpy
  - api/metodo
  - reducciones
lib: numpy
obj: ndarray
tipo: metodo
retorna: ndarray
inplace: false
draft: false
---

# ndarray.round — Redondear los valores del array a n decimales

## Firma del método

```python
ndarray.round(
    decimals=0,
    out=None
) -> ndarray
```

## Valor de retorno

| Entrada (`self`) | `decimals` | Retorno |
|------------------|------------|---------|
| `[1.234, 5.678]` | `0` | `array([1., 6.])` |
| `[1.234, 5.678]` | `2` | `array([1.23, 5.68])` |
| `[15, 25, 35]` | `-1` | `array([20, 20, 40])` (a la decena) |

No reduce: devuelve un ndarray del **mismo shape** que `self`, con cada valor redondeado. Por defecto retorna una **copia**; nunca modifica `self` salvo que se pase `out=self`.

```python
import numpy as np
a = np.array([1.234, 5.678])
a.round(2)   # array([1.23, 5.68])
```

## Equivalencia con np.round

`a.round(decimals, ...)` es la forma "bound" de [[np.round]]: `np.round(a, decimals, ...)`. Idéntico resultado y misma política de redondeo. La forma de método encadena de forma fluida; la funcional acepta como primer argumento cualquier `array_like` (listas), no solo un `ndarray` ya construido. (`ndarray.round` es además el alias de `ndarray.around`.)

## Parámetros en detalle

### `decimals` — número de decimales

Entero. Positivo redondea a esa cantidad de decimales; `0` al entero más cercano; **negativo** redondea a la izquierda del punto (decenas, centenas...).

### `out` — destino (round in-place)

Pasando `out=self` el redondeo se escribe sobre el propio array, evitando la copia. Aun así, `inplace` se documenta como `false` por el comportamiento por defecto.

### Redondeo al par (banker's rounding)

NumPy usa **redondeo al par más cercano**: los `.5` van al entero par, no siempre hacia arriba. Esto reduce el sesgo acumulado, pero sorprende si se espera "round half up".

```python
np.array([0.5, 1.5, 2.5, 3.5]).round()   # [0., 2., 2., 4.]  → al par
```

## Casos de uso

### Formatear resultados para mostrar

```python
precios = np.array([19.999, 4.501, 0.125])
precios.round(2)   # array([20.  ,  4.5 ,  0.12])
```

### Agrupar a la decena/centena

```python
np.array([123, 156, 188]).round(-1)   # array([120, 160, 190])
```

## Buenas prácticas

1. No uses `round` para "limpiar" errores de coma flotante en comparaciones; usa `np.isclose`.
2. Recuerda el redondeo al par: si necesitas "half up" estricto, impleméntalo aparte.
3. `round` no cambia el dtype: redondear un float sigue siendo float (`.0`), no int; castea con `.astype(int)` si lo necesitas.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `2.5` redondea a `2`, no a `3` | redondeo al par (bankers rounding) | esperado; implementar half-up si hace falta |
| Sigue siendo float tras `decimals=0` | `round` no cambia dtype | `.astype(int)` |
| Comparación de igualdad falla | residuos de coma flotante | `np.isclose` en vez de redondear |

## Notas relacionadas

- [[np.round]]
- [[concepto_dtype]]
- [[ndarray.clip]]
- [[ndarray.astype]]
