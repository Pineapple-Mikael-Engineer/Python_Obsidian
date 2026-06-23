---
title: np.any — ¿hay algún elemento verdadero a lo largo de un eje?
aliases:
  - any
  - np.any
  - alguno
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: bool | ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_vectorizacion
  - concepto_indexing

draft: false
---

# np.any — ¿hay algún elemento verdadero a lo largo de un eje?

`np.any` es una **reducción lógica**: recorre un eje del tensor y lo **colapsa** a un único valor
booleano que responde "¿hay **algún** elemento verdadero?". Es el **OR lógico** aplicado a lo largo
del eje: basta con que **un** elemento sea no-cero para que el resultado sea `True`. Como toda
reducción, la pregunta no es "¿alguno?" sino **"¿qué eje desaparece?"**. Se usa casi siempre sobre
una **máscara booleana** (`(arr > 0).any(...)`) para preguntar si **existe** alguna celda que cumpla
una condición.

## La idea en una fórmula

`any` reduce un eje vía **disyunción** ($\bigvee$, el OR). Para una matriz $A$ de shape $(m, n)$,
reducir el eje `0` produce un vector indexado por la columna $j$ donde cada entrada es `True` si
**existe** alguna fila con valor no-cero:

$$
\text{any}_j = \bigvee_{i=0}^{m-1} a_{ij} \qquad (\exists\, i: a_{ij}\neq 0) \qquad \text{(axis=0, desaparece el eje } i\text{)}
$$

El **mapa de shapes** es el de cualquier reducción: el eje de `axis` se elimina del shape.

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{any, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

NumPy trata **cualquier valor no-cero como `True`** (también `NaN`, que es no-cero), y solo el `0`
(o `0.0`, `False`, cadena vacía en arrays de objetos) como `False`. El eje que aparece en el
subíndice del $\bigvee$ es el que se reduce y **desaparece** (ver [[concepto_axis_parametro]]).

## Firma

```python
np.any(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int | tuple[int]: eje(s) a reducir con OR
    out=None,          # ndarray: destino preasignado (dtype bool)
    keepdims=False,    # bool: conservar los ejes reducidos con tamaño 1
    where=True,        # array_like[bool]: qué elementos entran en el OR
) -> bool | ndarray
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. No necesita ser
booleano: NumPy interpreta **no-cero como `True`**, así que `np.any([0, 0, 3])` es `True`. Lo
habitual es pasar directamente una **máscara** producto de una comparación (`arr > 5`).

### `axis` — qué eje se reduce con OR
El parámetro central. `None` (defecto) hace el OR sobre **todos** los elementos y devuelve un único
`bool`. Un `int` reduce ese eje. Una **tupla** reduce varios ejes a la vez:

```python
T = np.zeros((2, 3, 4)); T[0, 1, 2] = 1
np.any(T, axis=None)          # True  → ¿hay algún no-cero en todo el tensor?
np.any(T, axis=0).shape       # (3, 4)  → desaparece el eje 0
np.any(T, axis=(0, 2)).shape  # (3,)    → desaparecen los ejes 0 y 2
```
Acepta ejes negativos (`axis=-1` = último eje), lo idiomático para "¿alguno en la última dimensión?"
sin importar cuántas haya.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida y `dtype=bool`. Evita una asignación de memoria; útil
en bucles. Debe tener el shape exacto de salida.

### `keepdims` — conservar el eje reducido como tamaño 1
Si `True`, el eje reducido **no desaparece**: queda con tamaño 1. Sirve para que el resultado siga
siendo **broadcasteable** contra el array original (ver [[concepto_broadcasting]]).

```python
M = np.array([[0, 1], [0, 0]])
M.any(axis=1).shape              # (2,)    → no broadcastea de vuelta a (2,2)
M.any(axis=1, keepdims=True).shape  # (2, 1)  → sí broadcastea
```

### `where` — OR condicional (máscara)
`array_like` booleano broadcasteable con `a`. Solo entran en el OR los elementos donde `where` es
`True`; los demás se ignoran (como si no estuvieran). Útil para preguntar "¿hay algún verdadero
**entre los elementos seleccionados**?".

```python
arr = np.array([0, 1, 0, 1])
np.any(arr, where=np.array([True, False, True, False]))   # False → solo mira posiciones 0 y 2
```

## El eje y el caso N-D

La regla es mecánica: **el eje (o ejes) de `axis` se elimina del shape**; los demás quedan en orden.
Conviene leerlo como "para cada combinación de los ejes que **sobreviven**, ¿hay algún no-cero a lo
largo del que se reduce?".

| `a.shape` | `axis` | salida | lectura |
|-----------|--------|--------|---------|
| `(n,)` | `0` o `None` | `()` escalar `bool` | ¿hay algún no-cero? |
| `(m, n)` | `0` | `(n,)` | ¿algún no-cero por **columna**? |
| `(m, n)` | `1` | `(m,)` | ¿algún no-cero por **fila**? |
| `(m, n)` | `None` | `()` | ¿algún no-cero en toda la matriz? |
| `(d0, d1, d2)` | `0` | `(d1, d2)` | OR **a lo largo del lote** |
| `(d0, d1, d2)` | `(1, 2)` | `(d0,)` | ¿alguna celda no-cero por cada hoja del lote? |
| `(d0, d1, d2)` | `-1` | `(d0, d1)` | OR de la última dimensión |

```python
# Tensor (d0, d1, d2) = (2, 3, 4): ¿qué filas tienen algún valor negativo?
T = np.arange(-2, 22).reshape(2, 3, 4)   # valores de -2 a 21
mask = T < 0                              # máscara booleana (2, 3, 4)
mask.any(axis=2)        # ¿alguna columna negativa por fila?  shape (2, 3)
# [[ True, False, False],
#  [False, False, False]]
mask.any(axis=(1, 2))   # ¿la hoja del lote tiene algún negativo?  → [ True, False]
```
Con `keepdims=True`, cualquiera de esos resultados conserva los ejes reducidos en tamaño 1
(`(2, 3, 1)`, `(2, 1, 1)`...), listo para broadcastear contra `T`.

## Vectorización

`np.any` reemplaza un bucle Python con cortocircuito escrito a mano. Las dos versiones dan lo mismo,
pero la vectorizada corre en C sobre memoria contigua en vez de en el intérprete:

```python
# Bucle Python (lento, explícito):
def alguno_por_columna(M):
    m, n = M.shape
    out = np.zeros(n, dtype=bool)
    for j in range(n):
        for i in range(m):
            if M[i, j]:
                out[j] = True
                break
    return out

# Vectorizado (NumPy recorre el eje 0 en C):
M.any(axis=0)
```
NumPy ejecuta el OR como un recorrido optimizado del eje (con cortocircuito interno), sin crear
objetos Python por elemento. Es el mismo principio de [[concepto_vectorizacion]]: describes *qué* eje
reducir, no *cómo* iterar.

## Valor de retorno

El tipo del retorno **depende de `axis`**: escalar booleano de NumPy o `ndarray` de `bool`.

| Entrada | `axis` | `keepdims` | salida (shape) | tipo |
|---------|--------|------------|----------------|------|
| `(m, n)` | `None` | `False` | `()` | **`np.bool_`** (escalar booleano) |
| `(m, n)` | `int`/`tuple` | `False` | shape sin esos ejes | `ndarray` de `bool` |
| `(m, n)` | cualquiera | `True` | esos ejes en tamaño 1 | `ndarray` de `bool` |
| `(n,)` | `0` | `False` | `()` | `np.bool_` |

El resultado es **siempre `bool`** (o `np.bool_`), independientemente del `dtype` de entrada: `any`
sobre un array de floats o enteros sigue devolviendo booleanos.

```python
np.any([0, 0, 3])               # np.True_   → escalar booleano, no ndarray
type(np.any([[0, 1]], axis=0))  # numpy.ndarray
np.any([0.0, np.nan])           # True       → NaN es no-cero
```

> [!note] `any` de un eje vacío es `False`
> El elemento neutro del OR es `False`, así que `np.any([])` devuelve `False` (no existe ningún
> verdadero). Es el espejo de `np.all([])`, que es `True`.

## Casos de uso

### ¿Existe alguna celda que cumpla una condición?
```python
arr = np.array([3, -1, 7, 2])
(arr < 0).any()      # True   → ¿hay algún negativo?
(arr > 100).any()    # False  → ¿hay algún valor mayor que 100?
```

### Validar filas/columnas con una máscara
```python
M = np.array([[1, 0, 2],
              [0, 0, 0],
              [4, 5, 0]])
(M != 0).any(axis=1)   # [ True, False,  True]  → ¿qué filas tienen algún no-cero?
```

### Detección de `NaN` en un array
```python
datos = np.array([1.0, np.nan, 3.0])
np.isnan(datos).any()   # True  → ¿hay algún NaN antes de procesar?
```

### N-D: ¿qué muestras del lote tienen algún outlier?
```python
batch = np.random.randn(32, 10)        # 32 muestras, 10 features
(np.abs(batch) > 3).any(axis=1)        # shape (32,)  → True donde la muestra tiene un outlier
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `any()` da `True` con datos "vacíos" | hay `NaN` (es no-cero → `True`) | filtrar `NaN` o usar `np.isnan` aparte |
| Esperaba `bool` y obtuvo `ndarray` | se pasó `axis=`, no reduce a escalar | omitir `axis` o usar `.any()` sin eje |
| Sentido de `axis` invertido | confundir "filas" con "sobre el eje 0" | el eje de `axis` **desaparece**; mira el shape de salida |
| `if arr:` sobre array de varios elementos | ambigüedad de verdad de un ndarray | usar `if arr.any():` (o `.all()`) explícitamente |
| Broadcasting falla tras reducir | se perdió el eje reducido | `keepdims=True` |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[concepto_vectorizacion]] — por qué `axis` sustituye al bucle
- [[np.all]] — el complemento: ¿son **todos** verdaderos? (AND)
- [[np.count_nonzero]] — en vez de "¿alguno?", **cuántos**
- [[np.sum]] · [[np.where]] · [[concepto_broadcasting]]
