---
title: np.ndarray — metodos de transformacion
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — metodos de transformacion

5 metodos que cambian el tipo de dato, la interpretacion de los bytes o el contenido del array. La distincion vista/copia/in-place es critica aqui: equivocarse puede causar modificaciones silenciosas en el array original o desperdiciar memoria innecesariamente.

## Tabla de metodos

| Metodo | Firma resumida | Vista / Copia / In-place | Descripcion |
|--------|---------------|--------------------------|-------------|
| [[ndarray.astype]] | `arr.astype(dtype)` | Siempre copia | Convierte los valores a otro dtype |
| [[ndarray.view]] | `arr.view(dtype)` | Siempre vista | Reinterpreta los mismos bytes como otro tipo |
| [[ndarray.copy]] | `arr.copy(order='C')` | Siempre copia | Copia profunda independiente del original |
| [[ndarray.fill]] | `arr.fill(value)` | In-place, devuelve `None` | Rellena todos los elementos con un valor fijo |
| [[ndarray.byteswap]] | `arr.byteswap(inplace=False)` | Copia o in-place segun `inplace` | Invierte el orden de bytes de cada elemento |

## `astype` vs `view` — la distincion fundamental

Ambos "cambian el tipo", pero de formas radicalmente distintas:

- `astype` **convierte** los valores: `float64(1.5)` se convierte en `int32(1)` con truncamiento. Siempre asigna un buffer nuevo; el array original no cambia.
- `view` **reinterpreta** los mismos bytes sin convertir: los datos fisicos no cambian, solo cambia como NumPy los lee. Util para manipulacion de bajo nivel (leer floats como enteros para comparar bits).

```python
arr = np.array([1.5, 2.5], dtype=np.float64)

arr.astype(np.int32)   # → [1, 2]   (conversion de valores, copia)
arr.view(np.uint8)     # → los 16 bytes crudos de arr vistos como uint8
```

`view` falla o produce resultados incorrectos si el nuevo dtype tiene un tamaño de elemento que no divide exactamente al buffer original.

## `copy` — romper la dependencia con el original

Util cuando se tiene una vista y se necesita modificarla sin afectar al array base:

```python
arr = np.arange(10)
sub = arr[::2]          # vista — modificar sub cambia arr
safe = arr[::2].copy()  # copia — independiente de arr
```

El parametro `order` controla si la copia es C-contigua (`'C'`) o F-contigua (`'F'`).

## `fill` — relleno in-place

Mas rapido que `arr[:] = value` para arrays grandes porque evita la creacion de un array temporal. No devuelve el array modificado: devuelve `None`, por lo que no se puede encadenar:

```python
arr = np.empty((1000, 1000))
arr.fill(0.0)   # correcto — in-place
arr = arr.fill(0.0)  # incorrecto — arr queda None
```

## `byteswap` — compatibilidad de endianness

Necesario cuando se leen datos binarios producidos en una arquitectura con orden de bytes distinto (little-endian vs big-endian). Con `inplace=False` (por defecto) devuelve una copia con los bytes invertidos; con `inplace=True` modifica el array en sitio:

```python
arr = np.array([256], dtype=np.int16)   # 0x0100 en memoria
arr.byteswap()           # → [1]  (0x0001) como copia
arr.byteswap(inplace=True)  # modifica arr directamente
```
