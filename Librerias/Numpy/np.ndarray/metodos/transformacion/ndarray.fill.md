---
title: ndarray.fill — rellena todo el array con un escalar (in-place)
aliases:
  - fill
  - ndarray.fill
tags:
  - numpy
  - api/metodo
  - transformaciones
lib: numpy
mod: np.ndarray
obj: ndarray
tipo: metodo
retorna: None
inplace: true
requiere:
  - concepto_dtype
draft: false
---

# ndarray.fill — rellena todo el array con un escalar (in-place)

`fill` escribe un **único escalar en todos los elementos** del array, **in-place**: modifica `self` y devuelve `None`. Conserva shape y dtype; el valor se castea al [[concepto_dtype|dtype]] del array. Es la forma más directa (y la más rápida) de poner un array entero a un valor constante: más eficiente que `arr[:] = v` porque no construye ningún array temporal intermedio.

## La idea

`fill` recorre el buffer del array y **machaca cada elemento** con el mismo valor, sin crear memoria nueva. No transforma la forma ni el tipo: solo el contenido.

$$ \texttt{ndarray}\big[\text{shape}=S,\ \text{dtype}=\tau\big] \ \xrightarrow{\ \texttt{fill}(v)\ }\ \forall\, i:\ \texttt{self}[i] = \text{cast}_\tau(v)\quad(\text{in-place, retorna } \texttt{None}) $$

El valor `v` se **castea al dtype** del array: un `2.9` en un array `int` se trunca a `2`. Como modifica `self`, el efecto es visible en cualquier vista que comparta el buffer.

## Firma

```python
ndarray.fill(value) -> None
```

## Los parámetros en detalle

### `value` — el escalar a propagar

Único parámetro. Debe ser un **escalar** (no un array ni una secuencia). Se castea al [[concepto_dtype|dtype]] de `self` siguiendo las reglas habituales: float → int trunca hacia cero, un valor fuera de rango produce overflow.

```python
a = np.zeros(3, dtype=np.int32)
a.fill(2.9)    # trunca al castear → array([2, 2, 2], dtype=int32)

m = np.empty((2, 2), dtype=bool)
m.fill(True)   # array([[ True,  True], [ True,  True]])
```

> [!warning] No acepta arrays
> `arr.fill([1, 2])` lanza error: `fill` solo toma un escalar. Para un patrón por posición usa asignación con slice (`arr[:] = otro_array`).

## ¿Vista o copia?

Ninguna: `fill` es **in-place**. No crea un array nuevo; reescribe el buffer existente de `self` y devuelve `None`. Por eso **no se puede encadenar** ni asignar su resultado.

```python
arr = np.empty((1000, 1000))
arr.fill(0.0)          # correcto → arr queda en ceros
arr = arr.fill(0.0)    # ERROR conceptual → arr queda None (fill devuelve None)
```

Como muta el buffer, si existe una vista sobre `arr`, también la ve cambiada.

## Valor de retorno

Devuelve **`None`**. El efecto está en `self`, que tras la llamada tiene el mismo shape y dtype con todos sus elementos iguales a `cast_dtype(value)`.

| Entrada (`self`) | Llamada | Efecto en `self` |
|------------------|---------|------------------|
| `[0, 0, 0]` | `arr.fill(7)` | `[7, 7, 7]` |
| shape `(2, 2)` float64 | `arr.fill(1)` | `[[1., 1.], [1., 1.]]` |
| int32 | `arr.fill(2.9)` | `[2, 2, ...]` (castea, trunca) |

## fill frente a otras formas de rellenar

`fill` es **in-place**; `np.full` **crea** un array nuevo. La asignación por slice `arr[:] = v` también es in-place pero pasa por construir/broadcastear el lado derecho:

```python
arr.fill(9)            # in-place, sin temporal — la vía más rápida
arr[:] = 9             # in-place equivalente, algo menos directo
np.full(arr.shape, 9)  # crea un array nuevo lleno de 9
```

| Forma | Crea array nuevo | In-place | Retorna |
|-------|------------------|----------|---------|
| `arr.fill(v)` | no | sí | `None` |
| `arr[:] = v` | no | sí | — |
| `np.full(shape, v)` | sí | no | el array nuevo |

## Casos de uso

### Reinicializar un buffer reutilizado en un bucle

El caso fuerte: limpiar memoria ya reservada sin reasignarla.

```python
buf = np.empty(1000)
for _ in range(3):
    buf.fill(0.0)      # limpia in-place, sin reservar memoria nueva
    # ... acumular en buf
```

### Inicializar un array recién creado con `empty`

`np.empty` deja basura; `fill` lo deja en un valor conocido de forma explícita.

```python
mask = np.empty((4, 4), dtype=bool)
mask.fill(False)       # estado inicial definido
```

### Ejemplo realista: marcar una región de una imagen

```python
img = np.zeros((480, 640), dtype=np.uint8)
img[100:200, 50:150].fill(255)   # pinta el recorte de blanco, in-place
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `arr = arr.fill(v)` deja `None` | `fill` devuelve `None`, no el array | no asignar; leer `arr` tras la llamada |
| Pasar un array como `value` | `fill` solo acepta escalar | `arr[:] = otro_array` |
| Pérdida de decimales | castea float → dtype int (trunca) | usar un array float, o `np.round` antes |
| Overflow inesperado | `value` fuera del rango del dtype | elegir un dtype con rango suficiente |

## Notas relacionadas

- [[concepto_dtype]] — el casting del `value` al tipo del array
- [[np.full]] — crear un array nuevo ya relleno (no in-place)
