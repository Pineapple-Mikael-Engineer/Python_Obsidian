---
title: np.all — ¿son todos los elementos verdaderos a lo largo de un eje?
aliases:
  - all
  - np.all
  - todos
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

# np.all — ¿son todos los elementos verdaderos a lo largo de un eje?

`np.all` es una **reducción lógica**: recorre un eje del tensor y lo **colapsa** a un único valor
booleano que responde "¿son **todos** los elementos verdaderos?". Es el **AND lógico** aplicado a lo
largo del eje: basta con que **un** elemento sea cero para que el resultado sea `False`. Como toda
reducción, la pregunta no es "¿todos?" sino **"¿qué eje desaparece?"**. Es el espejo de [[np.any]] y
se usa casi siempre sobre una **máscara booleana** (`(arr > 0).all(...)`) para verificar que **toda**
una fila/columna/lote cumple una condición.

## La idea en una fórmula

`all` reduce un eje vía **conjunción** ($\bigwedge$, el AND). Para una matriz $A$ de shape $(m, n)$,
reducir el eje `0` produce un vector indexado por la columna $j$ donde cada entrada es `True` solo si
**todas** las filas son no-cero:

$$
\text{all}_j = \bigwedge_{i=0}^{m-1} a_{ij} \qquad (\forall\, i: a_{ij}\neq 0) \qquad \text{(axis=0, desaparece el eje } i\text{)}
$$

El **mapa de shapes** es el de cualquier reducción: el eje de `axis` se elimina del shape.

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{all, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

NumPy trata **cualquier valor no-cero como `True`** (también `NaN`) y solo el `0`/`False` como
`False`. El eje que aparece en el subíndice del $\bigwedge$ es el que se reduce y **desaparece**
(ver [[concepto_axis_parametro]]).

## Firma

```python
np.all(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int | tuple[int]: eje(s) a reducir con AND
    out=None,          # ndarray: destino preasignado (dtype bool)
    keepdims=False,    # bool: conservar los ejes reducidos con tamaño 1
    where=True,        # array_like[bool]: qué elementos entran en el AND
) -> bool | ndarray
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. No necesita ser
booleano: NumPy interpreta **no-cero como `True`**, así que `np.all([1, 2, 3])` es `True` pero
`np.all([1, 0, 3])` es `False`. Lo habitual es pasar una **máscara** producto de una comparación.

### `axis` — qué eje se reduce con AND
El parámetro central. `None` (defecto) hace el AND sobre **todos** los elementos y devuelve un único
`bool`. Un `int` reduce ese eje. Una **tupla** reduce varios ejes a la vez:

```python
T = np.ones((2, 3, 4)); T[0, 1, 2] = 0
np.all(T, axis=None)          # False  → ¿son todos no-cero en todo el tensor?
np.all(T, axis=0).shape       # (3, 4)  → desaparece el eje 0
np.all(T, axis=(0, 2)).shape  # (3,)    → desaparecen los ejes 0 y 2
```
Acepta ejes negativos (`axis=-1` = último eje), lo idiomático para "¿todos en la última dimensión?"
sin importar cuántas haya.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida y `dtype=bool`. Evita una asignación de memoria; útil
en bucles. Debe tener el shape exacto de salida.

### `keepdims` — conservar el eje reducido como tamaño 1
Si `True`, el eje reducido **no desaparece**: queda con tamaño 1. Sirve para que el resultado siga
siendo **broadcasteable** contra el array original (ver [[concepto_broadcasting]]).

```python
M = np.array([[1, 1], [1, 0]])
M.all(axis=1).shape              # (2,)    → no broadcastea de vuelta a (2,2)
M.all(axis=1, keepdims=True).shape  # (2, 1)  → sí broadcastea
```

### `where` — AND condicional (máscara)
`array_like` booleano broadcasteable con `a`. Solo entran en el AND los elementos donde `where` es
`True`; los demás se ignoran. Útil para verificar "¿son todos verdaderos **entre los elementos
seleccionados**?".

```python
arr = np.array([1, 0, 1, 0])
np.all(arr, where=np.array([True, False, True, False]))   # True → solo mira posiciones 0 y 2
```

## El eje y el caso N-D

La regla es mecánica: **el eje (o ejes) de `axis` se elimina del shape**; los demás quedan en orden.
Conviene leerlo como "para cada combinación de los ejes que **sobreviven**, ¿son todos no-cero a lo
largo del que se reduce?".

| `a.shape` | `axis` | salida | lectura |
|-----------|--------|--------|---------|
| `(n,)` | `0` o `None` | `()` escalar `bool` | ¿son todos no-cero? |
| `(m, n)` | `0` | `(n,)` | ¿todos no-cero por **columna**? |
| `(m, n)` | `1` | `(m,)` | ¿todos no-cero por **fila**? |
| `(m, n)` | `None` | `()` | ¿todos no-cero en toda la matriz? |
| `(d0, d1, d2)` | `0` | `(d1, d2)` | AND **a lo largo del lote** |
| `(d0, d1, d2)` | `(1, 2)` | `(d0,)` | ¿toda la hoja del lote es no-cero? |
| `(d0, d1, d2)` | `-1` | `(d0, d1)` | AND de la última dimensión |

```python
# Tensor (d0, d1, d2) = (2, 3, 4): validar que cada fila esté completamente en rango [0, 100)
T = np.arange(0, 24).reshape(2, 3, 4)     # valores de 0 a 23
ok = (T >= 0) & (T < 100)                  # máscara booleana (2, 3, 4)
ok.all(axis=2)         # ¿toda la fila válida?  shape (2, 3)  → todo True
ok.all(axis=(1, 2))    # ¿toda la hoja del lote válida?  → [ True,  True]
```
Con `keepdims=True`, cualquiera de esos resultados conserva los ejes reducidos en tamaño 1
(`(2, 3, 1)`, `(2, 1, 1)`...), listo para broadcastear contra `T`.

## Vectorización

`np.all` reemplaza un bucle Python con cortocircuito escrito a mano. Las dos versiones dan lo mismo,
pero la vectorizada corre en C sobre memoria contigua en vez de en el intérprete:

```python
# Bucle Python (lento, explícito):
def todos_por_columna(M):
    m, n = M.shape
    out = np.ones(n, dtype=bool)
    for j in range(n):
        for i in range(m):
            if not M[i, j]:
                out[j] = False
                break
    return out

# Vectorizado (NumPy recorre el eje 0 en C):
M.all(axis=0)
```
NumPy ejecuta el AND como un recorrido optimizado del eje (con cortocircuito interno), sin crear
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

El resultado es **siempre `bool`** (o `np.bool_`), independientemente del `dtype` de entrada.

```python
np.all([1, 2, 3])               # np.True_   → escalar booleano, no ndarray
np.all([1, 0, 3])               # np.False_  → el 0 lo tumba
type(np.all([[1, 1]], axis=0))  # numpy.ndarray
```

> [!warning] `all` de un eje VACÍO es `True` (vacuamente)
> El elemento neutro del AND es `True`, así que `np.all([])` devuelve `True`: "todos los (cero)
> elementos cumplen". Es **verdad vacua** y suele sorprender. Si reduces sobre un eje que puede tener
> tamaño 0, el resultado será `True` por columnas/filas vacías, no `False`. Es el espejo exacto de
> `np.any([])`, que es `False`.

## Casos de uso

### ¿Todas las celdas cumplen una condición?
```python
arr = np.array([3, 1, 7, 2])
(arr > 0).all()      # True   → ¿son todos positivos?
(arr < 5).all()      # False  → el 7 lo tumba
```

### Validar filas completas con una máscara
```python
M = np.array([[1, 2, 3],
              [4, 0, 6],
              [7, 8, 9]])
(M != 0).all(axis=1)   # [ True, False,  True]  → ¿qué filas no tienen ningún cero?
```

### Comparar dos arrays elemento a elemento (igualdad exacta)
```python
a = np.array([1, 2, 3])
b = np.array([1, 2, 3])
(a == b).all()   # True  → ¿son idénticos? (para floats preferir np.allclose)
```

### N-D: ¿qué muestras del lote están enteramente dentro de rango?
```python
batch = np.random.rand(32, 10)         # 32 muestras, 10 features en [0,1)
((batch >= 0) & (batch <= 1)).all(axis=1)   # shape (32,)  → True si toda la muestra es válida
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `all([])` da `True` inesperado | verdad vacua del AND sobre eje vacío | validar tamaño del eje antes de reducir |
| `all()` da `True` con `NaN` presente | `NaN` es no-cero → cuenta como `True` | comprobar `NaN` con `np.isnan(...).any()` aparte |
| Igualdad de floats falla | comparar `==` exacto con redondeo | usar [[np.allclose]] en vez de `(a==b).all()` |
| Esperaba `bool` y obtuvo `ndarray` | se pasó `axis=`, no reduce a escalar | omitir `axis` o usar `.all()` sin eje |
| Sentido de `axis` invertido | confundir "filas" con "sobre el eje 0" | el eje de `axis` **desaparece**; mira el shape de salida |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[concepto_vectorizacion]] — por qué `axis` sustituye al bucle
- [[np.any]] — el complemento: ¿hay **algún** verdadero? (OR)
- [[np.count_nonzero]] — en vez de "¿todos?", **cuántos**
- [[np.allclose]] · [[np.sum]] · [[concepto_broadcasting]]
