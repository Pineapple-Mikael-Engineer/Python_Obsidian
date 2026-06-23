---
title: np.diff — diferencia discreta a lo largo de un eje (acorta el eje)
aliases:
  - diff
  - np.diff
  - diferencias
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_vectorizacion

draft: false
---

# np.diff — diferencia discreta a lo largo de un eje (acorta el eje)

`np.diff` calcula la **diferencia entre elementos consecutivos** a lo largo de un eje: la versión
discreta de la derivada. Es la operación que convierte una serie de **posiciones** en una de
**desplazamientos**, o una señal en sus **saltos**. A diferencia de las reducciones que colapsan el
eje a un punto (ver [[np.sum]]), `diff` no lo elimina: lo **acorta** en `n`, porque calcular las
diferencias de `m` puntos produce `m-n` diferencias.

## La idea en una fórmula

La diferencia de primer orden a lo largo de un eje es, elemento a elemento:

$$ (\Delta a)_i = a_{i+1}-a_i $$

Aplicarla de orden `n` es componerla `n` veces ($\Delta^2 a_i = a_{i+2}-2a_{i+1}+a_i$, etc.).

**El mapa de shapes.** El eje `axis=p` **no desaparece**: se **acorta** en `n` (un elemento menos
por cada orden), mientras los demás ejes quedan intactos:

$$ (n_0,\dots,n_p,\dots,n_k)\ \xrightarrow{\ \text{diff orden } n,\ \text{axis}=p\ }\ (n_0,\dots,n_p-n,\dots,n_k) $$

Visual sobre un vector de 4 elementos, primer orden:

```
a   = [ a0   a1   a2   a3 ]      shape (4,)
Δa  =    [a1-a0  a2-a1  a3-a2]   shape (3,)   ← un elemento menos
```

Con `prepend`/`append` se inserta un valor extra **antes** de diferenciar, lo que compensa el
acortamiento y devuelve la longitud original (ver más abajo).

## Firma

```python
np.diff(
    a,                 # array_like: el tensor de entrada
    n=1,               # int: nº de veces que se aplica diff (orden de la diferencia)
    axis=-1,           # int: eje a lo largo del que se diferencia
    prepend=<sin valor>,  # array_like: valores a anteponer en el eje antes de diferenciar
    append=<sin valor>,   # array_like: valores a posponer en el eje antes de diferenciar
) -> ndarray
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. Sobre él se calculan
las diferencias a lo largo de `axis`. Su `dtype` se conserva en la salida, lo que importa con
enteros: una diferencia de `uint8` puede **desbordar** (`np.diff(np.array([0, 5], dtype=np.uint8))`
da `5`, pero `[5, 0]` da `251`, no `-5`). Pasa a `float` si esperas negativos.

### `n` — orden de la diferencia
`int ≥ 0`. Cuántas veces se aplica `diff` recursivamente. `n=1` (defecto) es la primera diferencia;
`n=2` la diferencia de la diferencia (segunda derivada discreta), y así. Cada orden **acorta el eje
en 1 más**, así que un eje de tamaño `m` con orden `n` queda en `m-n` (y en `0` si `n ≥ m`).

```python
np.diff([1, 2, 4, 7])       # [1, 2, 3]   primer orden
np.diff([1, 2, 4, 7], n=2)  # [1, 1]      segunda diferencia: diff de [1,2,3]
```

### `axis` — eje a lo largo del que se diferencia
Por defecto `-1` (el **último** eje), no `0`. Es el eje cuyos vecinos se restan; los demás quedan
intactos. Ver [[concepto_axis_parametro]]. Acepta ejes negativos.

```python
M = np.array([[1, 3, 6],
              [2, 5, 9]])
np.diff(M, axis=1)   # [[2, 3], [3, 4]]  → diferencia por fila; eje 1: 3 → 2
np.diff(M, axis=0)   # [[1, 2, 3]]       → fila[1]-fila[0]; eje 0: 2 → 1
```

### `prepend` / `append` — conservar la longitud
`array_like` que se **inserta en el eje antes** de diferenciar (al principio con `prepend`, al final
con `append`). Como añaden un punto y `diff` quita uno, el resultado recupera la longitud original.
El truco clásico: anteponer `0` (o `a[0]`) para que la salida tenga el mismo shape que la entrada y
se alinee con ella.

```python
x = np.array([1, 2, 4, 7])
np.diff(x, prepend=0)      # [1, 1, 2, 3]  → misma longitud, alineable con x
np.diff(x, append=x[-1])   # [1, 2, 3, 0]
```
Deben ser broadcasteables con `a` salvo en el eje diferenciado. Sin ellos, el eje se acorta.

## El eje y el caso N-D

La regla es mecánica: **el eje de `axis` se acorta en `n`; los demás quedan en orden**. En N-D
conviene leerlo como "para cada combinación de los ejes que sobreviven, diferencio a lo largo del
eje elegido".

| `a.shape` | `axis` | `n` | salida | lectura |
|-----------|--------|-----|--------|---------|
| `(m,)` | `0`/`-1` | `1` | `(m-1,)` | diferencias consecutivas |
| `(m,)` | `0` | `2` | `(m-2,)` | segunda diferencia |
| `(r, c)` | `1` | `1` | `(r, c-1)` | una diferencia por **fila** |
| `(r, c)` | `0` | `1` | `(r-1, c)` | resta filas vecinas (por columna) |
| `(b, t, k)` | `1` | `1` | `(b, t-1, k)` | diferencia a lo largo del eje temporal |

```python
# Lote de 4 series temporales de 5 pasos, 3 canales:  (4, 5, 3)
T = np.arange(4*5*3).reshape(4, 5, 3)
np.diff(T, axis=1).shape   # (4, 4, 3)  → el eje temporal (5) se acorta a 4
np.diff(T, axis=1, n=2).shape  # (4, 3, 3)  → segunda diferencia: 5 → 3
```
Nótese que, al contrario que en una reducción, **el eje sigue presente** en la salida; solo es más
corto.

## Vectorización

`np.diff` reemplaza el bucle de restar cada par de vecinos. Internamente es una resta de dos
**rebanadas** desplazadas del array (`a[1:] - a[:-1]`), que NumPy ejecuta en C sobre memoria
contigua sin objetos Python por elemento:

```python
# Bucle Python (lento, explícito):
def diferencias(v):
    out = np.empty(len(v) - 1, dtype=v.dtype)
    for i in range(len(v) - 1):
        out[i] = v[i+1] - v[i]
    return out

# Vectorizado (NumPy resta dos vistas desplazadas):
v[1:] - v[:-1]      # exactamente lo que hace np.diff sobre el último eje
```
`np.diff` generaliza ese `a[1:] - a[:-1]` a cualquier eje y orden. Es el principio de
[[concepto_vectorizacion]]: describes *qué* eje diferenciar, no *cómo* iterar.

## Valor de retorno

Siempre un `ndarray` (nunca un escalar suelto, salvo que el resultado quede de tamaño 0/1). El shape
es el de la entrada con el eje `axis` reducido en `n`; el `dtype` se **conserva** (cuidado con
enteros sin signo, ver `a`).

| Entrada (shape) | `axis` | `n` | salida (shape) | dtype |
|-----------------|--------|-----|----------------|-------|
| `(m,)` | `-1` | `1` | `(m-1,)` | igual que `a` |
| `(m,)` | `-1` | `k` | `(m-k,)` | igual que `a` |
| `(r, c)` | `1` | `1` | `(r, c-1)` | igual que `a` |
| `(r, c)` | `0` | `1` | `(r-1, c)` | igual que `a` |
| con `prepend`/`append` | — | `1` | eje **sin acortar** | igual que `a` |

```python
np.diff(np.array([1, 2, 4, 7])).dtype     # int64 (conserva el de la entrada)
np.diff(np.array([1, 2], dtype=np.uint8), append=np.uint8(0))  # [1, 254]  ← overflow
```

## Casos de uso

### Velocidad a partir de posiciones
```python
posicion = np.array([0, 5, 12, 20])
velocidad = np.diff(posicion)      # [5, 7, 8]  → desplazamiento por paso
```

### Detectar cambios o saltos en una serie
```python
serie = np.array([3, 3, 3, 5, 5, 2])
cambios = np.where(np.diff(serie) != 0)[0]   # [2, 4]  posiciones donde salta
```

### Segunda diferencia (curvatura / aceleración discreta)
```python
x = np.array([0, 1, 4, 9, 16])      # cuadrática
np.diff(x, n=2)                     # [2, 2, 2]  → segunda diferencia constante
```

### Conservar la longitud para alinear con el original
```python
precio = np.array([100, 102, 101, 105])
retorno = np.diff(precio, prepend=precio[0])   # [0, 2, -1, 4]  → mismo tamaño que precio
```

### N-D: diferencia a lo largo del eje temporal de un lote
```python
# (2 series, 4 instantes):
S = np.array([[1, 2, 4, 7],
              [0, 0, 3, 3]])
np.diff(S, axis=1)
# [[1, 2, 3],
#  [0, 3, 0]]   → el eje 1 pasa de 4 a 3; cada fila se diferencia por separado
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Desalineación de longitudes | `diff` acorta el eje en `n` | usar `prepend`/`append` |
| Eje equivocado | por defecto `axis=-1`, no `0` | pasar `axis` explícito |
| Diferencia entera incorrecta (gigante) | overflow de `uint`/`int` pequeño | convertir `a` a `float` |
| Se esperaba derivada con escala física | `diff` ignora el espaciado (paso 1) | usar [[np.gradient]] |
| Resultado vacío | `n ≥ tamaño del eje` | reducir `n` o revisar el eje |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué eje se acorta
- [[concepto_vectorizacion]] — por qué sustituye al bucle de vecinos
- [[np.gradient]] — derivada que **conserva** la longitud y usa diferencias centradas
- [[np.trapz]] · [[np.cumsum]] (operación inversa aproximada)
