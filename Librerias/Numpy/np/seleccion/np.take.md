---
title: np.take — toma elementos por índice a lo largo de un eje
aliases:
  - take
  - np.take
tags:
  - numpy
  - api/funcion
  - indexado

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing
  - concepto_axis_parametro

draft: false
---

# np.take — toma elementos por índice a lo largo de un eje

`np.take` recoge elementos de `a` por **índice entero** a lo largo de un eje. Es el [[concepto_indexing|fancy indexing]] expuesto como función: `np.take(a, idx, axis=p)` equivale a `a[..., idx, ...]` indexando el eje `p`, pero con control explícito de `axis` y de qué hacer con índices fuera de rango (`mode`). La idea clave en una frase: **el eje indexado se reemplaza por la forma de `indices`**.

## La idea en una fórmula

Tomar a lo largo del eje `p` **sustituye** ese eje por la forma completa de `indices`. Si `a` tiene shape $(n_0,\dots,n_{k-1})$ e `indices` tiene shape arbitrario `indices.shape`, el mapa de shapes es:

$$
(\dots,\,n_p,\,\dots)\ \xrightarrow{\ \text{take, axis}=p\ }\ (\dots,\,\underbrace{\text{indices.shape}}_{\text{reemplaza }n_p},\,\dots)
$$

La fórmula por índices: cada elemento de la salida copia el de `a` cuyo índice en el eje `p` lo dicta `indices`. Para `axis=p` e `indices` 1-D de longitud $m$:

$$
\text{out}[\dots,\,u,\,\dots] \;=\; a[\dots,\,\text{indices}[u],\,\dots] \qquad u=0,\dots,m-1
$$

Con `axis=None`, `a` se **aplana** primero y se indexa el array 1-D resultante: la salida toma la forma de `indices`.

## Firma

```python
np.take(
    a,                 # array_like: el tensor fuente
    indices,           # int | array_like[int]: posiciones a tomar
    axis=None,         # None | int: eje a indexar (None = a aplanado)
    out=None,          # ndarray: destino preasignado
    mode='raise',      # 'raise' | 'wrap' | 'clip': qué hacer con índices fuera de rango
) -> ndarray
```

## Los parámetros en detalle

### `a` — el tensor fuente
`array_like`. Se convierte a `ndarray` si no lo es. Solo aporta los **valores**; la forma de la salida la dictan `indices` y `axis`.

### `indices` — qué posiciones tomar
`int` o `array_like` de enteros (admite negativos: `-1` = último). Su **shape determina** la porción de la forma de salida que reemplaza al eje indexado. Puede repetir y reordenar índices libremente:

```python
a = np.array([10, 20, 30, 40])
np.take(a, [3, 0, 0, 2])   # array([40, 10, 10, 30])  → repite y reordena
```

### `axis` — qué eje se indexa
`None` (defecto) opera sobre `a` **aplanado**. Un `int` selecciona a lo largo de ese eje (admite negativos); los demás ejes quedan intactos:

```python
M = np.arange(12).reshape(3, 4)
np.take(M, [0, 2], axis=1).shape   # (3, 2)  → columnas 0 y 2
np.take(M, [0, 2], axis=0).shape   # (2, 4)  → filas 0 y 2
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape/dtype exactos de la salida. Evita una asignación de memoria; útil en bucles.

### `mode` — índices fuera de rango
Controla qué pasa cuando un índice excede el tamaño del eje:

| `mode` | Comportamiento | Ejemplo (eje de tamaño 4, índice 5) |
|--------|----------------|--------------------------------------|
| `'raise'` (defecto) | lanza `IndexError` | error |
| `'wrap'` | da la vuelta (módulo) | `5 % 4 = 1` |
| `'clip'` | recorta al borde válido | `→ 3` (último) |

```python
a = np.array([10, 20, 30, 40])
np.take(a, [5], mode='wrap')   # array([20])  → 5 % 4 = 1
np.take(a, [5], mode='clip')   # array([40])  → recorta al último
```

`'clip'` nunca lanza, pero **sesga** hacia los bordes; úsalo a sabiendas.

## El caso N-D

La regla es mecánica: el eje de `axis` **desaparece** y en su lugar se inserta la forma completa de `indices`; los demás ejes quedan en orden. Esto permite que `indices` sea N-D y "esculpa" nuevas dimensiones:

| `a.shape` | `indices.shape` | `axis` | salida |
|-----------|-----------------|--------|--------|
| `(n,)` | `(m,)` | `0` o `None` | `(m,)` |
| `(r, c)` | `(m,)` | `1` | `(r, m)` |
| `(r, c)` | `(p, q)` | `1` | `(r, p, q)` |
| `(b, n, m)` | `(k,)` | `0` | `(k, n, m)` |

```python
# Tensor (lote, alto, ancho)
a = np.arange(2*3*4).reshape(2, 3, 4)

# indices 1-D sobre el último eje: reemplaza el eje 2 (tamaño 4) por (2,)
np.take(a, [0, 3], axis=2).shape       # (2, 3, 2)

# indices 2-D: el eje indexado se reemplaza por TODA la forma de indices
idx = np.array([[0, 2], [3, 1]])       # shape (2, 2)
np.take(a, idx, axis=2).shape          # (2, 3, 2, 2)  ← (b, n, indices.shape)
```

## Vectorización

`np.take` reemplaza un bucle de recolección por índice. Las dos versiones dan lo mismo, pero la vectorizada recorre los índices en C:

```python
# Bucle Python (lento, explícito):
def toma(a, idx):
    return np.array([a[i] for i in idx])

# Vectorizado (NumPy recoge en C, además controla axis/mode):
np.take(a, idx)
```

Frente a `a[idx]` (fancy indexing puro), `np.take` añade `axis` explícito —útil cuando el eje se decide en tiempo de ejecución— y `mode`, que el `[]` no ofrece. Comparte el modelo de [[concepto_vectorizacion]]: describes *qué* recoger, no *cómo* iterar.

## Valor de retorno

Siempre devuelve un `ndarray` (nunca escalar, ni siquiera con un solo índice: `np.take(a, [2])` da shape `(1,)`). Devuelve una **copia**, como todo fancy indexing.

| Entrada | `indices` | `axis` | salida (shape) | dtype |
|---------|-----------|--------|----------------|-------|
| `(n,)` | `(m,)` | `None`/`0` | `(m,)` | el de `a` |
| `(r, c)` | `(m,)` | `1` | `(r, m)` | el de `a` |
| `(r, c)` | `(p, q)` | `0` | `(p, q, c)` | el de `a` |
| cualquiera | escalar `int` | `p` | shape de `a` sin el eje `p` | el de `a` |

El `dtype` se **conserva** (solo se copian valores, no se opera sobre ellos).

## Casos de uso

### Muestrear / reordenar filas
```python
datos = np.arange(20).reshape(5, 4)
np.take(datos, [3, 0, 0], axis=0)   # 3 filas (con repetición), shape (3, 4)
```

### Lookup table (tabla de búsqueda)
```python
tabla = np.array([0.0, 0.5, 1.0])
np.take(tabla, [2, 0, 1, 2])   # array([1. , 0. , 0.5, 1. ])
```

### N-D: seleccionar canales de un lote de imágenes
```python
# (lote, alto, ancho, canal) en orden RGBA
imgs = np.arange(2*2*2*4).reshape(2, 2, 2, 4)
rgb = np.take(imgs, [0, 1, 2], axis=-1)   # descarta alfa
rgb.shape                                  # (2, 2, 2, 3)
```

`np.take` es el **inverso** de [[np.put]]: `take` lee por índice, `put` escribe por índice.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `IndexError: index out of bounds` | índice fuera de rango con `mode='raise'` | validar, o `mode='clip'`/`'wrap'` a sabiendas |
| Resultado aplanado inesperado | `axis=None` por defecto | pasar `axis` explícito |
| Sentido del eje invertido | confundir qué eje se reemplaza | el eje de `axis` **desaparece**; mira el shape de salida |
| Se esperaba modificar `a` | `take` devuelve copia | para escribir usa [[np.put]] |

## Notas relacionadas

- [[concepto_indexing]] — el fancy indexing del que `take` es la versión funcional
- [[concepto_axis_parametro]] — qué eje se indexa y se reemplaza
- [[np.put]] — la operación inversa (escribir por índice)
- [[np.take_along_axis]] · [[np.choose]] · [[np.where]]
