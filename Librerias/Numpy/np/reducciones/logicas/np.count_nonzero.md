---
title: np.count_nonzero — cuenta cuántos elementos son no-cero a lo largo de un eje
aliases:
  - count_nonzero
  - np.count_nonzero
  - contar
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: int | ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_vectorizacion
  - concepto_indexing

draft: false
---

# np.count_nonzero — cuenta cuántos elementos son no-cero a lo largo de un eje

`np.count_nonzero` es una **reducción de conteo**: recorre un eje del tensor y lo **colapsa** a un
**entero** que dice **cuántos** elementos son no-cero (o `True`). Donde [[np.any]] responde
"¿alguno?" y [[np.all]] "¿todos?", esta responde **"¿cuántos?"**. Es **el idioma** para contar
cuántas celdas cumplen una condición: `np.count_nonzero(arr > 5, axis=0)`. Como toda reducción, la
pregunta no es "¿cuántos?" sino **"¿qué eje desaparece?"**.

## La idea en una fórmula

Contar no-ceros es **sumar la indicatriz** $[a_{ij}\neq 0]$ (1 si el elemento es no-cero, 0 si es
cero) a lo largo del eje. Para una matriz $A$ de shape $(m, n)$, reducir el eje `0` produce un vector
indexado por la columna $j$:

$$
\text{cnt}_j = \sum_{i=0}^{m-1} [\,a_{ij}\neq 0\,] \qquad \text{(axis=0, desaparece el eje } i\text{)}
$$

El **mapa de shapes** es el de cualquier reducción: el eje de `axis` se elimina del shape.

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{count\_nonzero, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

`NaN` cuenta como no-cero (suma 1). El eje del subíndice del sumatorio es el que se reduce y
**desaparece** (ver [[concepto_axis_parametro]]).

## Firma

```python
np.count_nonzero(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int | tuple[int]: eje(s) a contar
    *,
    keepdims=False,    # bool: conservar los ejes reducidos con tamaño 1
) -> int | ndarray
```

> [!note] Firma más estrecha que `sum`/`any`/`all`
> `count_nonzero` **no** tiene `out`, `dtype` ni `where`. Solo `a`, `axis` y `keepdims` (este último
> es keyword-only). Si necesitas máscara condicional, aplícala antes (`count_nonzero(mask & where)`).

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. No necesita ser
booleano: cuenta cualquier valor **no-cero**, así que `np.count_nonzero([0, 3, 0, -1])` es `2`. Lo
idiomático es pasar una **máscara** producto de una comparación (`arr > 5`), donde contar no-ceros =
contar `True`.

### `axis` — qué eje se reduce (acepta int o tupla)
El parámetro central. `None` (defecto) cuenta los no-ceros de **todo** el array y devuelve un `int`.
Un `int` reduce ese eje. Una **tupla** reduce varios ejes a la vez:

```python
T = np.array([[0, 1, 2], [0, 0, 3]])
np.count_nonzero(T, axis=None)   # 3   → no-ceros en todo el array
np.count_nonzero(T, axis=0)      # [0, 1, 2]  → no-ceros por columna
np.count_nonzero(T, axis=1)      # [2, 1]     → no-ceros por fila
```
Acepta ejes negativos (`axis=-1` = último eje) y tuplas (`axis=(0, 2)`), igual que las demás
reducciones.

### `keepdims` — conservar el eje reducido como tamaño 1
Keyword-only. Si `True`, el eje reducido **no desaparece**: queda con tamaño 1. Sirve para que el
resultado siga siendo **broadcasteable** contra el array original (ver [[concepto_broadcasting]]).

```python
M = np.array([[0, 1, 2], [3, 0, 0]])
np.count_nonzero(M, axis=1).shape                 # (2,)
np.count_nonzero(M, axis=1, keepdims=True).shape  # (2, 1)  → broadcastea de vuelta
```

## El eje y el caso N-D

La regla es mecánica: **el eje (o ejes) de `axis` se elimina del shape**; los demás quedan en orden.
Conviene leerlo como "para cada combinación de los ejes que **sobreviven**, ¿cuántos no-ceros hay a
lo largo del que se reduce?".

| `a.shape` | `axis` | salida | lectura |
|-----------|--------|--------|---------|
| `(n,)` | `0` o `None` | `()` → `int` | cuántos no-ceros en total |
| `(m, n)` | `0` | `(n,)` | cuántos no-ceros por **columna** |
| `(m, n)` | `1` | `(m,)` | cuántos no-ceros por **fila** |
| `(m, n)` | `None` | `int` | cuántos no-ceros en toda la matriz |
| `(d0, d1, d2)` | `0` | `(d1, d2)` | conteo **a lo largo del lote** |
| `(d0, d1, d2)` | `(1, 2)` | `(d0,)` | cuántos no-ceros por hoja del lote |
| `(d0, d1, d2)` | `-1` | `(d0, d1)` | conteo de la última dimensión |

```python
# Tensor (d0, d1, d2) = (2, 3, 4): contar valores positivos por fila
T = np.arange(-5, 19).reshape(2, 3, 4)    # valores de -5 a 18
pos = T > 0                                # máscara booleana (2, 3, 4)
np.count_nonzero(pos, axis=2)    # cuántos positivos por fila  shape (2, 3)
# [[0, 3, 4],
#  [4, 4, 4]]
np.count_nonzero(pos, axis=(1, 2))   # cuántos positivos por hoja del lote → [7, 12]
```
Con `keepdims=True`, esos resultados conservan los ejes reducidos en tamaño 1 (`(2, 3, 1)`,
`(2, 1, 1)`...), listos para broadcastear contra `T`.

## Vectorización

`np.count_nonzero` reemplaza un bucle de conteo escrito a mano. Las dos versiones dan lo mismo, pero
la vectorizada corre en C sobre memoria contigua en vez de en el intérprete:

```python
# Bucle Python (lento, explícito):
def contar_por_columna(M):
    m, n = M.shape
    out = np.zeros(n, dtype=int)
    for j in range(n):
        for i in range(m):
            if M[i, j] != 0:
                out[j] += 1
    return out

# Vectorizado (NumPy recorre el eje 0 en C):
np.count_nonzero(M, axis=0)
```
NumPy ejecuta el conteo como un recorrido optimizado del eje, sin crear objetos Python por elemento.
Es el mismo principio de [[concepto_vectorizacion]]: describes *qué* eje reducir, no *cómo* iterar.

### `count_nonzero` frente a `sum` de la máscara

`np.count_nonzero(mask)` y `np.sum(mask)` dan **el mismo número** sobre una máscara booleana (`True`
suma 1), pero `count_nonzero` es preferible: es **más explícito** ("estoy contando") y **más rápido**
(no promueve el `dtype` ni acarrea el riesgo de overflow del acumulador de `sum`).

```python
mask = np.array([True, False, True, True])
np.count_nonzero(mask)   # 4 elementos → 3   (idioma claro)
np.sum(mask)             # 3            (equivalente, pero menos explícito)
```

## Valor de retorno

El tipo del retorno **depende de `axis`**: `int` de Python (con `axis=None`) o `ndarray` de enteros.

| Entrada | `axis` | `keepdims` | salida (shape) | tipo |
|---------|--------|------------|----------------|------|
| `(m, n)` | `None` | `False` | escalar | **`int` de Python** |
| `(m, n)` | `int`/`tuple` | `False` | shape sin esos ejes | `ndarray` de `intp` |
| `(m, n)` | cualquiera | `True` | esos ejes en tamaño 1 | `ndarray` de `intp` |
| `(n,)` | `0` | `False` | escalar | `int` de Python |

El conteo es **siempre entero** (`int`/`np.intp`), independientemente del `dtype` de entrada. A
diferencia de `sum`, no hay riesgo de overflow ni promoción de tipo configurable.

```python
np.count_nonzero([0, 1, 0, 2])               # 2   → int de Python
type(np.count_nonzero([[0, 1]], axis=0))     # numpy.ndarray
np.count_nonzero([0.0, np.nan, 0.0])         # 1   → NaN cuenta como no-cero
```

## Casos de uso

### Cuántas celdas cumplen una condición (el idioma)
```python
arr = np.array([3, -1, 7, 2, -4])
np.count_nonzero(arr > 0)     # 3   → cuántos positivos
np.count_nonzero(arr < 0)     # 2   → cuántos negativos
```

### Conteo por fila/columna con una máscara
```python
M = np.array([[1, 0, 2],
              [0, 0, 0],
              [4, 5, 0]])
np.count_nonzero(M, axis=1)   # [2, 0, 2]  → no-ceros por fila
np.count_nonzero(M, axis=0)   # [2, 1, 1]  → no-ceros por columna
```

### Proporción de verdaderos (combinado con tamaño)
```python
mask = np.array([[True, False], [True, True]])
np.count_nonzero(mask) / mask.size   # 0.75  → fracción de True
```

### N-D: cuántos outliers por muestra del lote
```python
batch = np.random.randn(32, 10)            # 32 muestras, 10 features
np.count_nonzero(np.abs(batch) > 2, axis=1)   # shape (32,)  → nº de outliers por muestra
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Conteo mayor de lo esperado | `NaN` cuenta como no-cero | filtrar `NaN` antes o restar `np.isnan(...).sum()` |
| `TypeError` por pasar `out=`/`where=`/`dtype=` | `count_nonzero` no acepta esos parámetros | aplicar la máscara antes: `count_nonzero(mask & cond)` |
| Cuenta ceros como si no estuvieran | cuenta **no-ceros**, no "elementos" | usar `a.size` o `mask` adecuada para el total |
| Sentido de `axis` invertido | confundir "filas" con "sobre el eje 0" | el eje de `axis` **desaparece**; mira el shape de salida |
| Usar `sum` de máscara de `int8` y desbordar | `sum` promueve/desborda; `count_nonzero` no | preferir `count_nonzero` para contar condiciones |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[concepto_vectorizacion]] — por qué `axis` sustituye al bucle
- [[np.sum]] — equivalente sobre una máscara, pero menos explícito y con riesgo de overflow
- [[np.any]] — "¿alguno?" en vez de "¿cuántos?" (OR)
- [[np.all]] — "¿todos?" en vez de "¿cuántos?" (AND)
- [[np.nonzero]] · [[np.where]] · [[concepto_broadcasting]]
