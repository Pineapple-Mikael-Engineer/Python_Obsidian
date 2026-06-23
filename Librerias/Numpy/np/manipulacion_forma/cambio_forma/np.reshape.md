---
title: np.reshape — reorganiza los elementos en otra forma con el mismo total
aliases:
  - reshape
  - np.reshape
tags:
  - numpy
  - api/funcion
  - shape

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
  - concepto_views_vs_copias

draft: false
---

# np.reshape — reorganiza los elementos en otra forma con el mismo total

`np.reshape` es la operación de cambio de forma por excelencia: toma el buffer plano de un array y lo **reinterpreta** bajo otra tupla de ejes, sin tocar ni un solo elemento ni su orden lineal en memoria. No mueve datos, solo reescribe el [[concepto_shape|shape]] y los `strides`. La única condición es que el número total de elementos se conserve. La pregunta al usarla no es "¿qué valores cambian?" (ninguno) sino **"¿cómo se reparte el mismo `size` entre los ejes nuevos?"**.

## La idea en una fórmula

Reshape redistribuye el `size` entre los ejes nuevos, manteniendo el producto constante:

$$ (n_0, n_1, \dots, n_{k-1}) \;\xrightarrow{\ \text{reshape}\ }\; (m_0, m_1, \dots, m_{j-1}) \qquad\text{sujeto a}\qquad \prod_{i=0}^{k-1} n_i \;=\; \prod_{l=0}^{j-1} m_l $$

El `size` (el producto de los ejes) es el **invariante**: cualquier tupla destino cuyo producto coincida es válida; cualquier otra falla. Los datos se leen en el orden lineal de `a` y se vuelven a empaquetar bajo la forma nueva:

$$ \underbrace{[\,0,1,2,3,4,5\,]}_{(6,)} \;\xrightarrow{\ (2,3)\ }\; \begin{bmatrix} 0 & 1 & 2 \\ 3 & 4 & 5 \end{bmatrix} $$

Con `order='C'` (defecto) la última dimensión es la que varía más rápido, así que el buffer `[0,1,2,3,4,5]` se rellena fila a fila.

## Firma

```python
np.reshape(
    a,                 # array_like: el array a reinterpretar
    newshape,          # int | tuple[int]: la forma destino (un eje puede ser -1)
    order='C',         # {'C', 'F', 'A'}: orden de lectura/escritura de los elementos
) -> ndarray
```

## Los parámetros en detalle

### `a` — el array de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. No se modifica; el resultado suele compartir su buffer (ver [[concepto_views_vs_copias|vista vs copia]]).

### `newshape` — la forma destino
`int` o tupla de `int`. Su producto debe ser igual a `a.size`. Una de las dimensiones puede ser `-1` y NumPy la **infiere** dividiendo `size` entre el producto de las demás:

```python
arr = np.arange(12)
arr.reshape(3, -1)    # NumPy deduce 4 → (3, 4)
arr.reshape(-1, 6)    # NumPy deduce 2 → (2, 6)
arr.reshape(-1)       # aplana a (12,)  → equivale a ravel
```

Solo se permite **un** `-1` por llamada (dos dimensiones desconocidas no son resolubles). El método `arr.reshape(3, 4)` admite los enteros sueltos; la función exige la tupla `np.reshape(arr, (3, 4))`.

### `order` — orden de lectura/escritura de los elementos
Controla en qué orden se recorren los elementos al aplanar y al rellenar la forma nueva:

| Valor | Significado |
|-------|-------------|
| `'C'` (defecto) | por filas: la **última** dimensión varía más rápido (estilo C) |
| `'F'` | por columnas: la **primera** dimensión varía más rápido (estilo Fortran) |
| `'A'` | `'F'` si `a` es Fortran-contiguo, si no `'C'` |

```python
a = np.arange(6)
a.reshape(2, 3, order='C')   # [[0, 1, 2], [3, 4, 5]]
a.reshape(2, 3, order='F')   # [[0, 2, 4], [1, 3, 5]]
```

`order` cambia **qué valor cae en cada celda**, no solo el rendimiento. Es la trampa al venir de Fortran/MATLAB, donde el default es columna.

## El caso N-D

La regla es puramente aritmética: cualquier tupla cuyo producto sea `size` es válida, independientemente del número de ejes. Conviene leer el reshape como "agrupar/desagrupar" ejes del orden lineal:

| `a.shape` | `newshape` | salida | lectura |
|-----------|-----------|--------|---------|
| `(12,)` | `(3, 4)` | `(3, 4)` | 12 elementos en 3 filas de 4 |
| `(12,)` | `(2, 2, 3)` | `(2, 2, 3)` | tensor 2×2×3 |
| `(3, 4)` | `(-1,)` | `(12,)` | aplanar |
| `(2, 3, 4)` | `(6, 4)` | `(6, 4)` | fusiona los ejes 0 y 1 |
| `(2, 3, 4)` | `(2, -1)` | `(2, 12)` | aplana todo menos el lote |

```python
# Lote de 5 imágenes RGB 2×2:  (5, 2, 2, 3)
imgs = np.arange(5*2*2*3).reshape(5, 2, 2, 3)
imgs.reshape(5, -1).shape      # (5, 12)  → vectorizar cada imagen (aplanar todo menos el lote)
imgs.reshape(5, 4, 3).shape    # (5, 4, 3) → fusiona alto×ancho en un eje espacial
imgs.reshape(-1, 3).shape      # (20, 3)  → lista plana de todos los píxeles RGB
```
Fusionar ejes adyacentes (`alto, ancho → alto*ancho`) o separar uno en dos es el uso típico en N-D; el orden lineal manda y por eso `order` importa cuando los ejes no son contiguos.

## Vista vs copia

`reshape` devuelve una **vista** siempre que el buffer pueda reinterpretarse sin moverlo, lo que exige que `a` sea contiguo en el `order` pedido (ver [[concepto_views_vs_copias]]). Si no lo es —típicamente tras una transpuesta o un slice con paso—, NumPy se ve forzado a **copiar**:

```python
arr = np.arange(12).reshape(3, 4)

vista = arr.reshape(12)
np.shares_memory(arr, vista)     # True   → contiguo, vista barata

copia = arr.T.reshape(12)        # arr.T NO es contiguo
np.shares_memory(arr, copia)     # False  → tuvo que copiar
```

No hay forma de forzar "siempre vista": si la forma pedida no es representable con strides sobre el buffer actual, la copia es inevitable. Por eso no conviene asumir que `reshape` es gratis en arrays no contiguos.

## Valor de retorno

`ndarray` con el `newshape` y el **mismo `dtype`** y los **mismos datos** que `a`. Vista si es posible, copia si la contigüidad lo impide:

| Entrada | `newshape` | salida | ¿vista? |
|---------|-----------|--------|---------|
| `(12,)` contiguo | `(3, 4)` | `(3, 4)` | sí |
| `(3, 4)` contiguo | `(-1,)` | `(12,)` | sí |
| `(3, 4)` transpuesto | `(12,)` | `(12,)` | no (copia) |

Como suele ser vista, **escribir en el resultado puede alterar `a`**; añade `.copy()` si necesitas independencia.

## Casos de uso

### Vector ↔ matriz
```python
datos = np.arange(1, 13)        # (12,)
tabla = datos.reshape(3, 4)     # 3 filas, 4 columnas
tabla.reshape(-1)               # de vuelta a (12,)
```

### Insertar un eje de tamaño 1
```python
v = np.arange(3)
v.reshape(1, -1)    # (1, 3) fila    (más expresivo: np.expand_dims o np.newaxis)
v.reshape(-1, 1)    # (3, 1) columna
```

### Aplanar todo menos el lote (caso N-D)
```python
batch = np.arange(2*3*4).reshape(2, 3, 4)
plano = batch.reshape(batch.shape[0], -1)   # (2, 12)
plano
# array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11],
#        [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]])
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `cannot reshape array of size N into shape (...)` | `prod(newshape) != size` | ajustar dimensiones o usar `-1` |
| `can only specify one unknown dimension` | dos `-1` en `newshape` | dejar solo uno |
| El original cambió inesperadamente | el resultado era una vista | usar `.copy()` |
| Valores en celdas inesperadas | `order` distinto al asumido | revisar `order='F'` si vienes de Fortran/MATLAB |
| `reshape` no fue gratis | array no contiguo → copió | esperar copia tras `.T` o slices con paso |

## Notas relacionadas

- [[concepto_shape]] — el `size` invariante que reshape conserva
- [[concepto_views_vs_copias]] — cuándo devuelve vista y cuándo copia
- [[np.ravel]] — el caso particular de aplanar a 1D
- [[np.expand_dims]] · [[np.squeeze]] · [[np.transpose]]
