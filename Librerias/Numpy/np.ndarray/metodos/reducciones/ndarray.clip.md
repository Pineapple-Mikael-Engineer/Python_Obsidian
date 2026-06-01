---
title: ndarray.clip — Acotar los valores del array a un intervalo [min, max]
aliases:
  - clip
  - ndarray.clip
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

# ndarray.clip — Acotar los valores del array a un intervalo [min, max]

## Firma del método

```python
ndarray.clip(
    min=None,
    max=None,
    out=None,
    **kwargs
) -> ndarray
```

## Valor de retorno

| Entrada (`self`) | `min` | `max` | Retorno |
|------------------|-------|-------|---------|
| `[-2, 0, 5, 9]` | `0` | `5` | `array([0, 0, 5, 5])` |
| `[-2, 0, 5, 9]` | `0` | `None` | `array([0, 0, 5, 9])` (solo límite inferior) |
| `[-2, 0, 5, 9]` | `None` | `5` | `array([-2, 0, 5, 5])` (solo límite superior) |

No reduce: devuelve un ndarray del **mismo shape** que `self`, con cada valor recortado al intervalo. Por defecto retorna una **copia**; nunca modifica `self` salvo que se pase `out=self`.

```python
import numpy as np
a = np.array([-2, 0, 5, 9])
a.clip(0, 5)   # array([0, 0, 5, 5])
```

## Equivalencia con np.clip

`a.clip(min, max, ...)` es la forma "bound" de [[np.clip]]: `np.clip(a, min, max, ...)`. Mismo resultado y soporte de broadcasting en los límites. La forma de método encadena de forma fluida; la funcional acepta como primer argumento cualquier `array_like` (listas), no solo un `ndarray` ya construido.

## Parámetros en detalle

### `min` / `max` — límites del intervalo

Escalares o arrays compatibles por broadcasting. Al menos uno debe indicarse. `None` deja ese lado sin acotar.

```python
v = np.array([1, 5, 10, 20])
lo = np.array([0, 0, 12, 12])
v.clip(min=lo, max=15)   # límites por elemento → array([1, 5, 12, 15])
```

### `out` — destino (clip in-place)

Pasando `out=self` el recorte se escribe sobre el propio array, evitando la copia:

```python
a = np.array([-2, 0, 5, 9])
a.clip(0, 5, out=a)   # a queda [0, 0, 5, 5]  (in-place)
```

A pesar de ello, `inplace` se documenta como `false` porque el comportamiento por defecto del método es devolver una copia.

## Casos de uso

### Saturar valores fuera de rango físico

```python
medidas = np.array([-0.3, 0.5, 1.4])
medidas.clip(0.0, 1.0)   # array([0. , 0.5, 1. ])
```

### Evitar desbordes numéricos antes de un log/exp

```python
x.clip(1e-9, None)   # evita log(0)
```

## Buenas prácticas

1. Usa `out=self` solo si realmente quieres mutar el array y ahorrar memoria; si no, deja la copia por defecto.
2. Si solo necesitas un límite, pasa `None` al otro lado en vez de un valor "neutro" arbitrario.
3. Para condiciones más complejas que un intervalo, usa `np.where`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: One of max or min must be given` | ambos `None` | indicar al menos un límite |
| `min` mayor que `max` | intervalo invertido | NumPy fuerza todo a `max`; revisar el orden |
| Esperar mutación de `self` | retorna copia por defecto | pasar `out=self` |

## Notas relacionadas

- [[np.clip]]
- [[concepto_broadcasting]]
- [[ndarray.round]]
- [[ndarray.max]]
