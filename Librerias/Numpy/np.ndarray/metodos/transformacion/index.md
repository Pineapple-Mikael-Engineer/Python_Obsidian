---
title: np.ndarray — métodos de transformación
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — métodos de transformación

Métodos que **transforman el array a otra representación**: a otro tipo de dato, a otra interpretación de sus bytes, a otra disposición en memoria, o a otro contenido. Cubren las cuatro palancas:

- **el tipo** → [[ndarray.astype]] convierte el [[concepto_dtype|dtype]] (con copia).
- **la memoria** → [[ndarray.copy]] duplica el buffer; [[ndarray.view]] lo comparte reinterpretándolo.
- **el contenido** → [[ndarray.fill]] machaca todos los elementos con un escalar, in-place.
- **los bytes** → [[ndarray.byteswap]] invierte el endianness de cada elemento.

La distinción **vista / copia / in-place** es la clave de todo este grupo (ver [[concepto_views_vs_copias]]): equivocarse puede modificar el array original en silencio o desperdiciar memoria.

## Tabla de métodos

| Método | Firma resumida | Vista / Copia / In-place | Qué transforma |
|--------|----------------|--------------------------|----------------|
| [[ndarray.astype]] | `arr.astype(dtype)` | Siempre copia | el **dtype**: convierte los valores |
| [[ndarray.view]] | `arr.view(dtype)` | Siempre vista | la **interpretación**: reinterpreta los bytes |
| [[ndarray.copy]] | `arr.copy(order='C')` | Siempre copia | la **memoria**: buffer propio e independiente |
| [[ndarray.fill]] | `arr.fill(value)` | In-place, devuelve `None` | el **contenido**: todos los elementos a un escalar |
| [[ndarray.byteswap]] | `arr.byteswap(inplace=False)` | Copia o in-place según `inplace` | los **bytes**: invierte el endianness |

## La clave: vista vs copia

El error más caro de este grupo es tratar una vista como si fuera independiente. La regla mínima:

| Método | ¿Comparte buffer con el original? | ¿Modificar el resultado toca el original? |
|--------|-----------------------------------|-------------------------------------------|
| `view` | Sí (vista) | Sí |
| `copy` | No (buffer propio) | No |
| `astype` | No (copia con otro dtype) | No |
| `fill` | — (muta el propio array) | es el propio array |
| `byteswap` | según `inplace` | con `inplace=True`, sí |

## `astype` vs `view` — convertir vs reinterpretar

Ambos "cambian el tipo", pero de formas radicalmente distintas:

- `astype` **convierte** los valores: `float64(1.5)` se vuelve `int32(1)` (trunca). Siempre asigna un buffer nuevo; el original no cambia.
- `view` **reinterpreta** los mismos bytes sin convertir: los datos físicos no se mueven, solo cambia cómo NumPy los lee (p. ej. ver un `float64` como dos `int32` para inspeccionar bits).

```python
arr = np.array([1.5, 2.5], dtype=np.float64)
arr.astype(np.int32)   # → [1, 2]   conversión de valores (copia)
arr.view(np.uint8)     # → los 16 bytes crudos de arr vistos como 16 uint8
```

`view` falla si el nuevo `itemsize` no divide exactamente el tamaño en bytes del último eje.

## `copy` — romper la dependencia con el original

Materializa los datos en un buffer propio. Necesario cuando se tiene una vista y se quiere mutar sin afectar al array base:

```python
arr = np.arange(10)
sub = arr[::2]          # vista — modificar sub cambia arr
safe = arr[::2].copy()  # copia — independiente de arr
```

El parámetro `order` decide si la copia queda C-contigua (`'C'`) o F-contigua (`'F'`), ver [[concepto_contiguidad_memoria|contigüidad]].

## `fill` — relleno in-place

Pone todos los elementos a un escalar **sin crear un array temporal**, más rápido que `arr[:] = value`. Devuelve `None`, así que no se encadena:

```python
arr = np.empty((1000, 1000))
arr.fill(0.0)         # correcto — in-place
arr = arr.fill(0.0)   # incorrecto — arr queda None
```

## `byteswap` — compatibilidad de endianness

Invierte el orden de bytes de cada elemento. Necesario al leer datos binarios producidos en otra arquitectura (little-endian vs big-endian). Con `inplace=False` (defecto) devuelve una copia; con `inplace=True` muta el array:

```python
arr = np.array([256], dtype=np.int16)   # 0x0100 en memoria
arr.byteswap()              # → [1]  (0x0001) como copia
arr.byteswap(inplace=True)  # modifica arr en sitio
```
