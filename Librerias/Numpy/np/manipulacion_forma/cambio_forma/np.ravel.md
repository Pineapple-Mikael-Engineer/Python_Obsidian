---
title: np.ravel — aplana el array a una sola dimensión
aliases:
  - ravel
  - np.ravel
  - aplanar
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

# np.ravel — aplana el array a una sola dimensión

`np.ravel` es el caso particular de [[np.reshape|reshape]] que colapsa **todos** los ejes en uno: deja el array como un vector 1D con sus elementos en secuencia. Es el aplanado canónico, y su gracia frente a `flatten` es que devuelve una [[concepto_views_vs_copias|vista]] siempre que puede (sin copiar). La intuición: tomar el buffer multidimensional y leerlo como una fila larga, en el orden que diga `order`.

## La idea en una fórmula

Aplanar es reducir cualquier [[concepto_shape|shape]] a un único eje cuyo tamaño es el `size` total:

$$ (n_0, n_1, \dots, n_{k-1}) \;\xrightarrow{\ \text{ravel}\ }\; \Big(\textstyle\prod_{i=0}^{k-1} n_i\Big) $$

El producto de los ejes pasa a ser el único eje. Visto sobre una matriz concreta, con `order='C'` se recorre fila a fila:

$$ \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \;\xrightarrow{\ \text{ravel, C}\ }\; [\,1,2,3,4,5,6\,] $$

Es exactamente `reshape(-1)`: el `size` se conserva, solo que el destino tiene un único eje.

## Firma

```python
np.ravel(
    a,                 # array_like: el array a aplanar
    order='C',         # {'C', 'F', 'A', 'K'}: orden de recorrido de los elementos
) -> ndarray
```

## Los parámetros en detalle

### `a` — el array de entrada
`array_like` de cualquier dimensión. Se convierte a `ndarray` si no lo es. No se modifica; el resultado suele compartir su buffer.

### `order` — orden de recorrido
Decide en qué secuencia se leen los elementos para formar el vector 1D:

| Valor | Recorre | `[[1,2],[3,4]]` da |
|-------|---------|--------------------|
| `'C'` (defecto) | por filas (última dim primero) | `[1, 2, 3, 4]` |
| `'F'` | por columnas (primera dim primero) | `[1, 3, 2, 4]` |
| `'A'` | `'F'` si `a` es Fortran-contiguo, si no `'C'` | depende del layout |
| `'K'` | según el orden físico en memoria | el más eficiente |

```python
M = np.array([[1, 2], [3, 4]])
M.ravel(order='C')   # [1, 2, 3, 4]
M.ravel(order='F')   # [1, 3, 2, 4]
```

`'K'` es la opción cuando el orden lógico no importa y solo quieres recorrer rápido (sigue el layout real, así que nunca copia por reordenar).

## El caso N-D

Ravel **siempre** colapsa hasta 1D, sin importar cuántos ejes tenga `a`: el shape de salida es siempre `(size,)`. No existe aplanado parcial (para eso, `reshape`).

| `a.shape` | salida | lectura |
|-----------|--------|---------|
| `(2, 3)` | `(6,)` | matriz → vector |
| `(2, 3, 4)` | `(24,)` | tensor → vector |
| `(5, 2, 2, 3)` | `(60,)` | lote completo en serie |

```python
# Lote de 5 imágenes RGB 2×2:  (5, 2, 2, 3)
imgs = np.arange(5*2*2*3).reshape(5, 2, 2, 3)
imgs.ravel().shape          # (60,)  → todos los valores en serie
imgs[0].ravel().shape       # (12,)  → solo la primera imagen, aplanada
```
Para aplanar manteniendo algún eje (p. ej. el lote), no es `ravel` sino `reshape(n, -1)`.

## Vista vs copia

`ravel` devuelve una **vista** cuando puede recorrer el buffer en el `order` pedido sin moverlo (array contiguo en ese orden); si no, **copia**. Contrasta con `ndarray.flatten`, que **siempre copia**:

| Operación | Devuelve | ¿copia? | Nota |
|-----------|----------|---------|------|
| `np.ravel(a)` / `a.ravel()` | 1D | solo si hace falta | **vista** preferente |
| `a.flatten()` | 1D | **siempre** | copia independiente garantizada |
| `a.reshape(-1)` | 1D | solo si hace falta | equivalente a `ravel` |

```python
A = np.arange(12).reshape(3, 4)
plano = A.ravel()                # vista (A es contiguo)
np.shares_memory(A, plano)       # True
plano[0] = 99                    # ¡también modifica A[0, 0]!

copia = A.T.ravel()              # A.T no es contiguo en 'C'
np.shares_memory(A, copia)       # False → tuvo que copiar
```

Usa `ravel` si te vale una vista (más rápido); usa `flatten` (o `ravel().copy()`) si necesitas independencia garantizada.

## Valor de retorno

`ndarray` **1D** de shape `(a.size,)`, mismo `dtype` que `a`. Vista si el recorrido es posible sin mover datos, copia en caso contrario:

| Entrada | `order` | salida | ¿vista? |
|---------|---------|--------|---------|
| `(3, 4)` contiguo | `'C'` | `(12,)` | sí |
| `(3, 4)` transpuesto | `'C'` | `(12,)` | no (copia) |
| cualquiera | `'K'` | `(size,)` | sí (sigue el layout) |

## Casos de uso

### Recorrer todos los elementos en serie
```python
img = np.random.rand(100, 100)
for pixel in img.ravel():        # acceso lineal a los 10 000 valores
    ...
```

### Aplanar, operar y volver a la forma
```python
A = np.arange(12).reshape(3, 4)
plano = A.ravel()                # vista 1D
plano[0] = 99                    # modifica también A[0, 0] (es vista)
```

### Concatenar contenidos de varias matrices (caso N-D)
```python
a = np.arange(6).reshape(2, 3)
b = np.arange(6, 12).reshape(2, 3)
todo = np.concatenate([a.ravel(), b.ravel()])
todo   # array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11])
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El original se modificó al editar el resultado | `ravel` devolvió vista | usar `a.flatten()` o `a.ravel().copy()` |
| Orden inesperado tras venir de Fortran/MATLAB | `order='C'` por defecto | usar `order='F'` |
| Esperar 2D y recibir 1D | `ravel` aplana **del todo** | usar `reshape(n, -1)` para forma intermedia |
| `ravel` no fue gratis | array no contiguo en ese orden → copió | usar `order='K'` o asumir copia tras `.T` |

## Notas relacionadas

- [[concepto_shape]] — el `size` que se vuelve el único eje
- [[concepto_views_vs_copias]] — vista (ravel) frente a copia siempre (`flatten`)
- [[np.reshape]] — `ravel` es `reshape(-1)` con nombre propio
- [[Librerias/Numpy/np.ndarray/metodos/forma/index|ndarray.flatten]] · [[np.expand_dims]] · [[np.squeeze]]
