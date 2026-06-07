---
title: np.ndarray — metodos de transformacion
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — metodos de transformacion

Los 5 metodos de transformacion cambian el tipo, la interpretacion de bytes o el contenido del array. La distincion clave entre ellos es si producen una **copia**, una **vista** o modifican **in-place**.

## Tabla de metodos

| Metodo | Firma resumida | Copia / Vista / In-place | Descripcion |
|--------|---------------|--------------------------|-------------|
| [[ndarray.astype]] | `arr.astype(dtype)` | Siempre copia | Convierte a otro dtype |
| [[ndarray.view]] | `arr.view(dtype)` | Vista (mismos bytes) | Reinterpreta los bytes como otro tipo |
| [[ndarray.copy]] | `arr.copy(order='C')` | Siempre copia | Copia profunda garantizada |
| [[ndarray.fill]] | `arr.fill(value)` | In-place (`None`) | Rellena todos los elementos con un valor |
| [[ndarray.byteswap]] | `arr.byteswap(inplace=False)` | Copia o in-place | Invierte el orden de bytes (endianness) |

## Notas de uso

### `astype` vs `view`

Ambos "cambian el tipo", pero de formas radicalmente distintas:

- `astype` **convierte** los valores: `float64(1.5)` se convierte en `int32(1)` con truncamiento. Siempre asigna un buffer nuevo.
- `view` **reinterpreta** los mismos bytes: los datos no cambian, solo cambia como NumPy los lee. Util para manipulacion de bajo nivel (ej. leer floats como enteros para comparar bits).

```python
arr = np.array([1.5, 2.5], dtype=np.float64)
arr.astype(np.int32)   # → [1, 2]  (conversion de valores)
arr.view(np.uint8)     # → los 16 bytes crudo de arr como enteros sin signo
```

### `copy` — cuando usarla

Util para romper la dependencia entre una vista y su base:

```python
sub = arr[::2]         # vista — modifica arr si se modifica sub
safe = arr[::2].copy() # copia — independiente de arr
```

### `byteswap` — endianness

Operacion necesaria al leer datos binarios producidos en una arquitectura con orden de bytes distinto:

```python
arr = np.array([1], dtype=np.int16)
arr.byteswap(inplace=True)  # modifica arr directamente
```
