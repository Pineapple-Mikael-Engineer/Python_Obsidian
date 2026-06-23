---
title: ndarray.view — nuevo array sobre el mismo buffer (reinterpreta dtype)
aliases:
  - view
  - ndarray.view
tags:
  - numpy
  - api/metodo
  - memoria
lib: numpy
mod: np.ndarray
obj: ndarray
tipo: metodo
retorna: ndarray
inplace: false
requiere:
  - concepto_views_vs_copias
  - concepto_dtype
draft: false
---

# ndarray.view — nuevo array sobre el mismo buffer (reinterpreta dtype)

`view` crea un **objeto `ndarray` nuevo que comparte el buffer de bytes** de `self`, sin copiar datos. Opcionalmente **reinterpreta** ese buffer con otro [[concepto_dtype|dtype]] (leer un `float64` como dos `int32`, o como ocho `uint8`) o como otra subclase de array. Es la herramienta de más bajo nivel del grupo: potente porque no cuesta memoria, y **peligrosa** porque reinterpreta los bytes crudos — no convierte valores como [[ndarray.astype]]. Escribir en la vista modifica el original.

## La idea

`view` no toca los datos: produce una **nueva cabecera** (shape, strides, dtype, tipo) sobre el **mismo buffer**. Si se pasa un `dtype` con distinto `itemsize`, los **mismos bytes** se reagrupan y el número de elementos cambia.

$$ \texttt{ndarray}\big[\text{buffer}=B,\ \text{dtype}=\tau_0\big] \ \xrightarrow{\ \texttt{view}(\tau_1)\ }\ \texttt{ndarray}\big[\text{buffer}=B\ \text{(el mismo)},\ \text{dtype}=\tau_1\big] $$

Si `itemsize(τ₁) ≠ itemsize(τ₀)`, el tamaño del último eje se reescala: un `float64` (8 bytes) visto como `int32` (4 bytes) produce **2** elementos por cada original. Los bytes no se mueven; solo cambia cómo NumPy los agrupa e interpreta.

## Firma

```python
ndarray.view(dtype=None, type=None) -> ndarray
```

## Los parámetros en detalle

### `dtype` — reinterpretación del tipo

Si se omite, la vista mantiene el dtype del original (solo cambia la cabecera). Si se da, los **mismos bytes** se leen con el nuevo [[concepto_dtype|dtype]]. El tamaño total en bytes del **último eje** debe ser divisible por el `itemsize` destino, o falla.

```python
a = np.array([1.0], dtype=np.float64)   # 8 bytes
a.view(np.int64)        # array([4607182418800017408])  → bits IEEE-754 del 1.0
a.view(np.int32)        # array([0, 1072693248])  → 8 bytes = 2 × int32
a.view(np.uint8)        # 8 elementos uint8 → un byte cada uno

b = np.arange(3, dtype=np.int16)   # 6 bytes en el último eje
b.view(np.int32)        # ValueError → 6 no es múltiplo de 4
```

> [!warning] `dtype` y `type` son cosas distintas
> `view(dtype)` cambia **cómo se interpretan los bytes**; `view(type)` cambia **la clase Python** del objeto array. Se pueden combinar.

### `type` — subclase de array

Reinterpreta el buffer como otra **subclase** de `ndarray` (p. ej. `np.recarray`, `np.matrix`) sin copiar. Útil para acceder a la interfaz de esa subclase sobre los mismos datos.

```python
r = a.view(type=np.recarray)   # misma data, interfaz de recarray
type(r)                        # numpy.recarray
```

## ¿Vista o copia?

**Siempre vista.** El array devuelto comparte el buffer de `self`: `np.shares_memory(self, v)` es `True`, `v.base` apunta al original (o a su dueño) y `v.flags.owndata` es `False`. Escribir en la vista **modifica el original** — el riesgo central de este método.

```python
import numpy as np
a = np.array([1, 2, 3], dtype=np.int32)
v = a.view()
v.base is a                 # True  → comparte buffer
np.shares_memory(a, v)      # True
v[0] = 99
a[0]                        # 99    → modificar la vista modifica el original
```

> [!danger] `view` reinterpreta, no convierte
> `a.view(np.int64)` lee los bytes del `float64` como un entero gigante; `a.astype(np.int64)` calcula el entero **equivalente** (1.0 → 1). Confundirlos da valores absurdos. Si quieres convertir valores, usa [[ndarray.astype]]. Si necesitas independencia, usa [[ndarray.copy]].

## Valor de retorno

Un `ndarray` nuevo sobre el **mismo buffer**. Mismo número de elementos si no cambia el `itemsize`; reescalado si cambia. El shape puede cambiar en el último eje; el dtype y/o la subclase, según los parámetros.

| Entrada | Llamada | Salida |
|---------|---------|--------|
| `[1, 2, 3]` int32 | `arr.view()` | misma data, otra cabecera, `base is arr` |
| `[1.0]` float64 | `arr.view(np.int64)` | bits del float como un int (`4607182418800017408`) |
| `[1.0]` float64 | `arr.view(np.int32)` | 2 elementos int32 (8 bytes → 2 × 4) |
| `[256]` int16 | `arr.view(np.uint8)` | `[0, 1]` → 2 bytes vistos como 2 uint8 |

## Casos de uso

### Inspeccionar la representación binaria de un flotante

```python
f = np.array([1.5], dtype=np.float32)
bits = f.view(np.uint32)        # patrón de bits IEEE-754 del 1.5
f'{bits[0]:032b}'               # '00111111110000000000000000000000'
```

### Ver un float64 como dos int32 (manipulación de bajo nivel)

```python
x = np.array([3.14159], dtype=np.float64)   # 8 bytes
lo, hi = x.view(np.int32)                    # los dos medios words
```

### Etiquetar/subclasificar sin copiar datos

```python
big = np.arange(1_000_000)
rec = big.view(type=np.recarray)   # otra interfaz, 0 datos copiados
```

### Ejemplo realista: comparar floats por su patrón de bits

Para detectar `-0.0` o NaN concretos hay que mirar los bits, no el valor:

```python
vals = np.array([0.0, -0.0, np.nan], dtype=np.float64)
bits = vals.view(np.uint64)
bits[0] == bits[1]   # False → +0.0 y -0.0 tienen bits distintos
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valores "raros" tras `view(int)` | reinterpreta bytes, no convierte | usar [[ndarray.astype]] para conversión real |
| `ValueError` por itemsize | el último eje no es múltiplo del nuevo `itemsize` | ajustar shape/dtype o copiar antes |
| Modificar el original sin querer | la vista comparte buffer | trabajar sobre `.copy()` si se necesita independencia |
| `view(dtype)` falla en array no contiguo | reinterpretar exige bytes contiguos | `np.ascontiguousarray(arr).view(...)` |

## Notas relacionadas

- [[concepto_views_vs_copias]] — el modelo vista/copia y cómo comprobarlo
- [[concepto_dtype]] — qué significa reinterpretar los bytes con otro tipo
- [[ndarray.astype]] — convertir valores (con copia) en vez de reinterpretar bytes
- [[ndarray.copy]] — el opuesto: buffer propio e independiente
- [[ndarray.base]] — el array dueño del buffer compartido
