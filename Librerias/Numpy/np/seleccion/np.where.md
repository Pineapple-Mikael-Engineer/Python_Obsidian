---
title: np.where — selección elemento a elemento (o índices de la condición)
aliases:
  - where
  - np.where
tags:
  - numpy
  - api/funcion
  - seleccion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | tuple
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing
  - concepto_broadcasting

draft: false
---

# np.where — selección elemento a elemento (o índices de la condición)

`np.where` tiene **dos personalidades** según cuántos argumentos reciba. Con tres,
`where(cond, x, y)`, es un **selector elemento a elemento**: construye un array tomando cada posición
de `x` o de `y` según diga la condición —el `if/else` vectorizado—. Con uno solo, `where(cond)`,
deja de seleccionar y **devuelve los índices** de los elementos `True`, exactamente como
[[np.nonzero]]. La pregunta al usarla es siempre "¿paso `x` e `y`, o no?": de eso depende si te
devuelve un array o una tupla.

## La idea en una fórmula

**Modo selección** (`where(cond, x, y)`). Las tres entradas se alinean por
[[concepto_broadcasting|broadcasting]] a un shape común y el resultado tiene ese shape; cada elemento
sale de `x` o de `y`:

$$ \text{cond},\,x,\,y \ \xrightarrow{\ \text{broadcast}\ }\ (n_0,\dots,n_{k-1}) \ \xrightarrow{\ \text{where}\ }\ z\ \text{de shape}\ (n_0,\dots,n_{k-1}) $$

$$ z_{\,i_0\dots i_{k-1}} \;=\; \begin{cases} x_{\,i_0\dots i_{k-1}} & \text{si } \text{cond}_{\,i_0\dots i_{k-1}} \\[2pt] y_{\,i_0\dots i_{k-1}} & \text{en otro caso} \end{cases} $$

**Modo índices** (`where(cond)`). No hay `x` ni `y`: la salida no es un array de valores sino una
tupla de $k$ arrays de índices, uno por eje, con las coordenadas de los `True` (idéntico a
[[np.nonzero]]):

$$ \text{cond de shape}\ (n_0,\dots,n_{k-1}) \ \xrightarrow{\ \text{where}\ }\ \big(\mathbf{r}_0,\dots,\mathbf{r}_{k-1}\big),\quad \mathbf{r}_j\ \text{de shape}\ (N,) $$

donde $N$ es el número de elementos `True`.

## Firma

```python
np.where(
    condition,    # array_like[bool]: la máscara (o expresión que la produzca)
    x=...,        # array_like (opcional): valores donde condition es True
    y=...,        # array_like (opcional): valores donde condition es False
    /,
) -> ndarray | tuple[ndarray, ...]
```

`x` e `y` son **posicionales**: o pasas **ambos** (modo selección) o **ninguno** (modo índices).
Pasar solo uno es un error.

## Los parámetros en detalle

### `condition` — la máscara booleana
`array_like` de booleanos, normalmente una expresión como `a > 0`. En modo selección marca qué
posiciones toman de `x` (donde es `True`) y cuáles de `y`. En modo índices es lo único que se pasa,
y sus elementos no-cero/`True` son los que se localizan. Valores no booleanos se interpretan por
truthiness (`0`/`0.0` → `False`, el resto `True`).

### `x` — valores para las posiciones `True`
`array_like`, broadcasteable con `condition` (y con `y`). Puede ser un escalar (`0`, `'alto'`), un
array del mismo shape, o algo broadcasteable. Solo existe en modo selección.

```python
a = np.array([10, 20, 30, 40])
np.where(a > 25, a, -1)        # [-1, -1, 30, 40]   x=a (array), y=-1 (escalar)
np.where(a > 25, a * 2, 0)     # [  0,   0, 60, 80]
```

### `y` — valores para las posiciones `False`
`array_like`, mismas reglas que `x`. **Trampa importante**: tanto `x` como `y` se **evalúan por
completo** antes de seleccionar; no hay cortocircuito. Si una rama contiene una operación inválida
(división por cero, log de negativos), se calcula igual y puede emitir warnings o `inf`/`nan`:

```python
a = np.array([1, 2, 0, 4]); b = np.array([2, 0, 5, 0])
np.where(b != 0, a / b, 0)     # a/b se calcula ENTERO → RuntimeWarning divide by zero
```

Para evitarlo, usa la máscara directa o el `where=` de la ufunc (`np.divide(a, b, out=..., where=b!=0)`).

## El caso N-D

**Modo selección.** La regla es pura: el resultado toma el shape del broadcasting de las tres
entradas, y la selección es elemento a elemento sin importar la dimensión.

```python
M = np.arange(6).reshape(2, 3)
#  [[0, 1, 2],
#   [3, 4, 5]]
np.where(M % 2 == 0, M, -1)
#  [[ 0, -1,  2],
#   [-1,  4, -1]]

# broadcasting: una columna decide por fila
col = np.array([[True], [False]])     # shape (2, 1)
np.where(col, M, 0)                   # fila 0 intacta, fila 1 a 0
#  [[0, 1, 2],
#   [0, 0, 0]]
```

**Modo índices.** Devuelve $k$ arrays (uno por eje); desempaquetarlos da las coordenadas:

```python
T = np.array([[[0, 5], [0, 0]],
              [[7, 0], [0, 9]]])      # shape (2, 2, 2)
z, f, c = np.where(T > 0)
z, f, c        # (array([0,1,1]), array([0,0,1]), array([1,0,1]))
T[z, f, c]     # [5, 7, 9]  → recupera los valores en esas coordenadas
```

## Vectorización

`where(cond, x, y)` reemplaza el bucle `if/else` por elemento. Las dos versiones coinciden, pero la
vectorizada recorre el array en C en vez de en el intérprete (ver [[concepto_vectorizacion]]):

```python
# Bucle Python (lento, explícito):
out = np.empty_like(a)
for i in range(a.size):
    out[i] = a[i] if a[i] > 0 else 0

# Vectorizado:
out = np.where(a > 0, a, 0)
```

NumPy evalúa la condición y ambas ramas como arrays completos y mezcla con una máscara, sin crear
objetos Python por elemento. (Ese mismo motivo es el de la "trampa" de arriba: no hay cortocircuito
porque `x` e `y` ya son arrays calculados.)

## Valor de retorno

El tipo de retorno **depende del número de argumentos**:

| Llamada | Retorno | Shape | Tipo |
|---------|---------|-------|------|
| `where(cond, x, y)` | array de valores | broadcast de `cond`, `x`, `y` | `ndarray` (dtype promovido de `x`/`y`) |
| `where(cond)` | tupla de índices | tupla de $k$ arrays `(N,)` | `tuple[ndarray, ...]`, dtype `intp` |

```python
type(np.where([True, False], 1, 0))   # numpy.ndarray
type(np.where([True, False]))         # tuple   → (array([0]),)
```

En modo selección, el `dtype` sale de la promoción de `x` e `y` (p. ej. `int` + `float` → `float64`;
con strings → `<U...`). En modo índices siempre es una tupla de arrays de enteros `intp`, aunque la
entrada sea 1D (de ahí el típico `np.where(cond)[0]`).

## Casos de uso

### `if/else` vectorizado (ReLU, recorte, etiquetado)
```python
np.where(x < 0, 0, x)                 # ReLU: negativos a 0
np.where(a > 100, 100, a)             # techo en 100 (ver np.clip)
np.where(score >= 60, 'apto', 'no')   # etiquetar por umbral
```

### Anidado para más de dos ramas
```python
np.where(a < 15, 'A',
  np.where(a < 35, 'B', 'C'))         # para muchas ramas, np.select es más legible
```

### Localizar posiciones (modo índices) e indexar con ellas
```python
idx = np.where(temperaturas > 100)[0]      # posiciones 1D
M = np.array([[0, 5], [3, 0]])
filas, cols = np.where(M > 0)              # (0,1) y (1,0)
M[filas, cols]                             # [5, 3]
```

### N-D: seleccionar entre dos tensores
```python
# Combinar dos imágenes según una máscara espacial
A = np.random.rand(3, 4, 4); B = np.zeros((3, 4, 4))
mask = np.random.rand(4, 4) > 0.5          # shape (4,4), broadcastea al canal
np.where(mask, A, B).shape                 # (3, 4, 4)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: either both or neither of x and y should be given` | se pasó solo `x` | pasar `x` e `y`, o ninguno |
| Esperar un array y recibir una tupla | se llamó en modo índices `where(cond)` | indexar `[0]` para 1D, o desempaquetar |
| Warning de división/`nan` inesperado | ambas ramas se evalúan sin cortocircuito | máscara directa o `np.divide(..., where=)` |
| Resultado con dtype raro (`<U21`, `float`) | promoción de `x` e `y` | castear `x`/`y` al tipo deseado antes |
| `where` anidado ilegible | demasiadas ramas | usar [[np.select]] |

## Notas relacionadas

- [[concepto_indexing]] — la máscara booleana y el indexado avanzado detrás del modo índices
- [[concepto_broadcasting]] — cómo se alinean `cond`, `x` e `y`
- [[np.nonzero]] — a lo que equivale `where(cond)`
- [[np.argwhere]] · [[np.select]] · [[np.clip]] · [[np.extract]] · [[np.take]]
