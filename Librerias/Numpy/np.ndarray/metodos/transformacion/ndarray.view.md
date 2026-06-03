---
title: ndarray.view — Nueva vista del mismo buffer (reinterpreta dtype)
aliases:
  - view
  - ndarray.view
tags:
  - numpy
  - api/metodo
  - memoria
lib: numpy
obj: ndarray
tipo: metodo
retorna: ndarray
inplace: false
draft: false
---

# ndarray.view — Nueva vista del mismo buffer (reinterpreta dtype)

## Firma del método

```python
ndarray.view(dtype=None, type=None) -> ndarray
```

## Valor de retorno

Devuelve un `ndarray` nuevo que **comparte el mismo buffer de memoria** que `self` (una vista, ver [[concepto_views_vs_copias]]). No copia datos: si se pasa `dtype`, **reinterpreta los mismos bytes** con otro tipo. Escribir en la vista modifica el original.

| Entrada | Llamada | Salida |
|---------|---------|--------|
| `[1, 2, 3]` int32 | `arr.view()` | misma data, otra cabecera, `base is arr` |
| `[1.0]` float64 | `arr.view(np.int64)` | bits del float reinterpretados como int |
| `[256]` int16 | `arr.view(np.uint8)` | `[0, 1]` → 2 bytes vistos como 2 uint8 |

```python
import numpy as np
a = np.array([1, 2, 3], dtype=np.int32)
v = a.view()
v.base is a     # True → comparte buffer
v[0] = 99
a[0]            # 99  → modificar la vista modifica el original
```

## Reinterpretación de bytes (no conversión)

Clave: `view(dtype)` **NO convierte valores** como [[ndarray.astype]]; reinterpreta los bytes crudos. El número de elementos puede cambiar si el `itemsize` difiere.

```python
a = np.array([1.0], dtype=np.float64)   # 8 bytes
a.view(np.int64)        # array([4607182418800017408])  → bits del 1.0
a.view(np.uint8)        # 8 elementos uint8 → un byte cada uno

a = np.arange(4, dtype=np.int16)        # itemsize 2
a.view(np.int32)        # 2 elementos → cada par de int16 fusionado
```

## Parámetros en detalle

### `dtype` — reinterpretación de tipo

Si se omite, la vista mantiene el dtype. Si el nuevo `itemsize` no divide el tamaño total en bytes del último eje, falla.

```python
a = np.arange(3, dtype=np.int16)   # 6 bytes
a.view(np.int32)   # ValueError → 6 no es múltiplo de 4
```

### `type` — subclase de array

Permite ver el buffer como otra subclase de `ndarray` (p. ej. `np.matrix`, `np.recarray`).

```python
a.view(type=np.recarray)   # misma data, interfaz de recarray
```

## Casos de uso

### Inspeccionar la representación binaria

```python
f = np.array([1.5], dtype=np.float32)
f.view(np.uint32)   # patrón de bits IEEE-754 del 1.5
```

### Vista barata para etiquetar sin copiar

```python
big = np.arange(1_000_000)
v = big.view()      # otra cabecera, 0 datos copiados
```

## Buenas prácticas

1. Usa `view` para **reinterpretar bytes**; usa [[ndarray.astype]] cuando quieras **convertir valores** (con copia).
2. Recuerda que escribir en la vista afecta al original: usa [[ndarray.copy]] si necesitas independencia.
3. Para arrays no contiguos, reinterpretar dtype puede fallar; aplica `.copy()` antes si hace falta.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valores "raros" tras `view(int)` | reinterpreta bytes, no convierte | usar `astype` para conversión real |
| `ValueError` por itemsize | bytes no múltiplos del nuevo dtype | ajustar shape/dtype o copiar |
| Modificar el original sin querer | la vista comparte buffer | trabajar sobre `.copy()` |

## Notas relacionadas

- [[concepto_views_vs_copias]]
- [[ndarray.copy]]
- [[ndarray.astype]]
- [[ndarray.base]]
