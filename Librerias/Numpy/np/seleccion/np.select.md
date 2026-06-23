---
title: np.select — elige por la primera de varias condiciones (where múltiple)
aliases:
  - select
  - np.select
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
  - concepto_broadcasting

draft: false
---

# np.select — elige por la primera de varias condiciones (where múltiple)

`np.select` construye un array eligiendo, para cada posición, el valor del **primer** choice cuya condición es `True`. Es el [[np.where]] generalizado de 2 a $N$ ramas: en vez de una condición y dos salidas, recibe una lista de condiciones evaluadas **en orden de prioridad** y la lista paralela de valores. Donde ninguna condición se cumple, pone `default`. La idea en una frase: **gana la primera condición True, leída de izquierda a derecha**.

## La idea en una fórmula

Con condiciones $C_0,\dots,C_{L-1}$ (arrays booleanos broadcasteables a $(n_0,\dots,n_{k-1})$) y valores $v_0,\dots,v_{L-1}$, cada elemento de la salida es:

$$
\text{out}[\mathbf{i}] \;=\;
\begin{cases}
v_{\,p}[\mathbf{i}] & p=\min\{\,j : C_j[\mathbf{i}]=\text{True}\,\}\\[4pt]
\text{default} & \text{si ningún } C_j[\mathbf{i}] \text{ es True}
\end{cases}
$$

es decir, se toma el valor del **menor índice** $j$ cuya condición se cumple en esa posición. El mapa de shapes es el broadcasting conjunto de todas las condiciones y todos los valores:

$$
C_0.\text{shape},\dots,\ v_0.\text{shape},\dots\ \xrightarrow{\ \text{broadcast}\ }\ (n_0,\dots,n_{k-1})\ =\ \text{out.shape}
$$

Generaliza [[np.where]]: `np.where(C, x, y)` es exactamente `np.select([C], [x], default=y)`.

## Firma

```python
np.select(
    condlist,          # lista de array_like[bool]: condiciones, en orden de prioridad
    choicelist,        # lista de array_like: valores, paralela a condlist
    default=0,         # escalar: valor donde ninguna condición se cumple
) -> ndarray
```

## Los parámetros en detalle

### `condlist` — las condiciones en orden de prioridad
Lista de arrays booleanos broadcasteables a una forma común. Se evalúan **en orden**: en cada posición gana la **primera** `True`. El orden importa cuando varias condiciones se solapan.

```python
a = np.array([-5, 3, 50, 200])
condlist = [a < 0, a < 100, a >= 100]   # la 2ª y 3ª se solapan con casos
```

### `choicelist` — los valores paralelos
Lista de la **misma longitud** que `condlist`. `choicelist[j]` (escalar o array broadcasteable) es el valor tomado donde `condlist[j]` es la primera condición cierta:

```python
choicelist = ['negativo', 'normal', 'alto']
np.select(condlist, choicelist, default='?')
# array(['negativo', 'normal', 'normal', 'alto'], dtype='<U8')
```

### `default` — el caso "ninguna se cumple"
Escalar usado donde **toda** condición es `False` (por defecto `0`). Si trabajas con texto u otro dtype, fíjalo explícito: `default=0` puede chocar con un `choicelist` de strings.

## El caso N-D

Todas las condiciones y todos los valores se broadcastean a una forma común, que es la de la salida. La regla de prioridad opera **independientemente en cada posición**:

| `condlist[j].shape` | `choicelist[j].shape` | salida |
|---------------------|-----------------------|--------|
| `(n,)` | `(n,)` o escalar | `(n,)` |
| `(r, c)` | `(r, c)` o escalar | `(r, c)` |
| `(r, 1)` | `(1, c)` | `(r, c)` por broadcast |

```python
M = np.array([[-2,  4],
              [ 9, -1]])
cond = [M < 0, M < 5]            # negativos primero, luego "pequeños"
val  = [0, M]                    # negativos → 0, pequeños → ellos mismos
np.select(cond, val, default=99)
# array([[ 0,  4],
#        [99,  0]])  → 9 no cumple ninguna → default 99
```

## Vectorización

`np.select` reemplaza una cadena de `if/elif/else` por celda. El equivalente con bucle:

```python
# Bucle Python (lento, explícito):
def selecciona(condlist, choicelist, default):
    out = np.full(condlist[0].shape, default)
    for i in np.ndindex(out.shape):
        for cond, val in zip(condlist, choicelist):
            if cond[i]:
                out[i] = val[i] if np.ndim(val) else val
                break
    return out

# Vectorizado (NumPy aplica las máscaras en orden, en C):
np.select(condlist, choicelist, default)
```

Por debajo equivale a `where` anidados aplicados de la **última** condición a la primera, pero leído en orden de prioridad. Importante: **todas** las condiciones y valores se evalúan (no hay cortocircuito). Mismo principio de [[concepto_vectorizacion]]: describes las ramas, no el bucle.

## Valor de retorno

Siempre un `ndarray` con la forma del broadcasting conjunto. El `dtype` es la **promoción** de todos los `choicelist` y de `default`.

| `condlist`/`choicelist` | `default` | salida (shape) | dtype |
|-------------------------|-----------|----------------|-------|
| arrays `(r, c)` numéricos | `0` | `(r, c)` | promovido (p. ej. `float`) |
| valores string | `'?'` | broadcast | `<U…` (texto) |
| escalares + arrays | escalar | broadcast común | promovido |

## Casos de uso

### Categorizar en rangos (binning)
```python
notas = np.array([45, 70, 85, 95])
cond = [notas < 60, notas < 80, notas < 90, notas >= 90]
cat  = ['F', 'C', 'B', 'A']
np.select(cond, cat)   # array(['F', 'C', 'B', 'A'], dtype='<U1')
```

### Función definida a trozos
```python
x = np.linspace(-1, 2, 7)
# f(x) = 0 si x<0 ;  x si 0<=x<1 ;  1 si x>=1   (rampa saturada)
y = np.select([x < 0, x < 1], [0.0, x], default=1.0)
# array([0.  , 0.  , 0.  , 0.5 , 1.  , 1.  , 1.  ])
```

### N-D: clasificar una rejilla por umbrales
```python
g = np.array([[10, 55],
              [80, 95]])
cond = [g < 50, g < 90]
val  = ['bajo', 'medio']
np.select(cond, val, default='alto')
# array([['bajo', 'medio'],
#        ['medio', 'alto']], dtype='<U5')
```

`np.select` sustituye con ventaja a [[np.where]] anidados cuando hay ≥3 ramas.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `list of cases must be same length as list of conditions` | `condlist` y `choicelist` de distinta longitud | igualar longitudes |
| Resultado inesperado por solapamiento | varias condiciones True | recordar que gana la **primera**; reordenar |
| `default=0` aparece como `'0'` o rompe el dtype | default numérico con choices de texto | pasar `default` del tipo correcto |
| Esperaba cortocircuito | todas las condiciones se evalúan siempre | no usar condiciones con efectos secundarios |

## Notas relacionadas

- [[np.where]] — el caso de 2 ramas que `select` generaliza
- [[concepto_broadcasting]] — condiciones y valores se alinean por broadcasting
- [[np.choose]] — selección por índice entero en vez de condiciones
- [[concepto_indexing]] · [[np.clip]]
