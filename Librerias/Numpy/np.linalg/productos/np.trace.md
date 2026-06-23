---
title: np.trace — suma de la diagonal (colapsa los dos ejes de la matriz)
aliases:
  - trace
  - np.trace
  - traza
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np
tipo: funcion
retorna: ndarray | escalar
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.trace — la traza: suma de la diagonal principal

`np.trace` calcula la **traza** de una matriz: la suma de los elementos de su diagonal principal.
Donde una reducción ordinaria colapsa **un** eje, la traza colapsa **dos a la vez** —los dos ejes
que forman la matriz— quedándose con un solo número por matriz. Es un invariante fundamental: la
traza es igual a la **suma de los autovalores** y no cambia bajo cambios de base.

## La idea en una fórmula

Para una matriz $A$ de shape $(n, n)$, la traza recorre la diagonal ($i = j$) y la suma:

$$
\operatorname{tr}(A) \;=\; \sum_{i} A_{ii} \qquad (A \in \mathbb{R}^{n \times n})
$$

Solo aparece **un** índice $i$ en el sumatorio porque se exige $i = j$: la diagonal. Los dos ejes de
la matriz **se contraen juntos** y desaparecen.

**El mapa de shapes** (la relación entrada → salida, incluido el caso por lotes N-D):

$$
(\underbrace{\dots}_{\text{lote}},\, n,\, n)\ \xrightarrow{\ \text{trace}\ }\ (\underbrace{\dots}_{\text{lote}})
$$

Los **dos últimos ejes** (por defecto) son la matriz y se **colapsan a un escalar**; los `…`
anteriores son ejes de lote que **sobreviven**. Una matriz $(n,n)$ da un escalar `()`; una pila
$(b,n,n)$ da un vector $(b,)$ —una traza por matriz del lote—. La regla extendida con `offset` suma
la diagonal desplazada $A_{i,\,i+\text{offset}}$.

Visualmente, para una matriz $4\times 4$ la traza recorre la diagonal marcada:

```text
┌ ■  ·  ·  · ┐
│ ·  ■  ·  · │   tr = A00 + A11 + A22 + A33
│ ·  ·  ■  · │   (offset=0: la diagonal principal)
└ ·  ·  ·  ■ ┘
```

## Firma

```python
np.trace(
    a,           # array_like: tensor con al menos 2 ejes
    offset=0,    # int: diagonal a sumar (0 principal, >0 arriba, <0 abajo)
    axis1=0,     # int: primer eje del par que forma la matriz
    axis2=1,     # int: segundo eje del par que forma la matriz
    dtype=None,  # dtype: tipo del acumulador y del resultado
    out=None,    # ndarray: destino preasignado
) -> ndarray | escalar
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` con `ndim >= 2`. La matriz cuyo rastro se calcula se forma con los ejes `axis1`/`axis2`;
el resto de ejes son lote. No es obligatorio que la matriz sea cuadrada: con shape $(n, m)$ se suma
la diagonal de longitud $\min(n, m)$.

### `offset` — qué diagonal se suma
`int` (defecto `0`). Selecciona la diagonal desplazada respecto a la principal: `offset > 0` sube
hacia la esquina superior derecha ($A_{i,\,i+\text{offset}}$), `offset < 0` baja a la inferior
izquierda. Misma convención que [[np.diagonal]].

```python
A = np.arange(9).reshape(3, 3)   # [[0,1,2],[3,4,5],[6,7,8]]
np.trace(A)            # 12   → 0 + 4 + 8 (principal)
np.trace(A, offset=1)  # 6    → 1 + 5 (diagonal de encima)
np.trace(A, offset=-1) # 10   → 3 + 7 (diagonal de debajo)
```

### `axis1`, `axis2` — qué par de ejes forman la matriz
`int` (defecto `0` y `1`). En un tensor N-D eligen **cuáles** de los ejes se interpretan como la
matriz a diagonalizar; los demás quedan como lote. Por defecto se toman los **dos primeros** ejes
(no los dos últimos como en `@`/`matmul`), un detalle fácil de olvidar.

```python
T = np.ones((4, 5, 6))
np.trace(T).shape                  # (6,)  → matriz sobre ejes 0,1 → sobrevive el 2
np.trace(T, axis1=1, axis2=2).shape  # (4,) → matriz sobre ejes 1,2 → sobrevive el 0
```

### `dtype` — tipo del acumulador
Fija el tipo en el que se **acumula** la suma (no solo el del resultado). Igual que en [[np.sum]],
importa con enteros de pocos bits: el acumulador hereda el `dtype` de `a` y puede **desbordar en
silencio**; fíjalo a `int64`/`float64` para una suma larga segura.

### `out` — buffer de salida
`ndarray` preasignado con el shape exacto del resultado (el del lote). Evita asignar memoria; útil al
repetir en un bucle.

## El eje y el caso N-D

La regla es mecánica: **los ejes `axis1` y `axis2` se contraen juntos y desaparecen**; los demás
sobreviven en orden. Para un lote, leerlo como "una traza por cada combinación de los ejes que
sobreviven".

| `a.shape` | parámetros | salida | lectura |
|-----------|-----------|--------|---------|
| `(n, n)` | defecto | `()` escalar | traza de la matriz |
| `(n, m)` | defecto | `()` escalar | suma de la diagonal $\min(n,m)$ |
| `(b, n, n)` | `axis1=1, axis2=2` | `(b,)` | una traza por matriz del lote |
| `(b, n, n)` | defecto (`axis1=0, axis2=1`) | `(n,)` | ¡matriz sobre ejes 0,1! rara vez es lo que quieres |
| `(b, c, n, n)` | `axis1=-2, axis2=-1` | `(b, c)` | traza de cada matriz de la rejilla |

> [!warning] Para un lote, fija `axis1`/`axis2` a los dos últimos
> Los defectos `axis1=0, axis2=1` toman los **dos primeros** ejes. Para "la traza de cada matriz de
> una pila `(b, n, n)`" debes pasar `axis1=-2, axis2=-1` (o `1, 2`); si no, NumPy diagonaliza el par
> equivocado y el shape de salida te sorprenderá.

```python
P = np.arange(2*3*3).reshape(2, 3, 3)   # lote de 2 matrices 3x3
np.trace(P, axis1=-2, axis2=-1)         # [12, 39]  → traza de cada matriz, shape (2,)
np.trace(P, axis1=-2, axis2=-1).shape   # (2,)
```

## Vectorización

La traza por lotes es [[concepto_vectorizacion]] pura: una traza por matriz **sin bucle Python**.
Las dos versiones dan lo mismo, pero la vectorizada recorre el lote en C:

```python
# Bucle Python: una traza por matriz del lote
def batch_trace(P):
    out = np.empty(P.shape[0])
    for i in range(P.shape[0]):
        out[i] = np.trace(P[i])
    return out

# Vectorizado: NumPy contrae los dos últimos ejes de golpe
np.trace(P, axis1=-2, axis2=-1)
```

Equivalente conceptual: `np.diagonal(P, axis1=-2, axis2=-1).sum(-1)` —extraer la diagonal y sumarla—.
`np.trace` lo hace en un paso sin materializar la diagonal.

## Valor de retorno

| Entrada | parámetros | salida (shape) | tipo |
|---------|-----------|----------------|------|
| `(n, n)` | defecto | `()` | **escalar de NumPy** (`np.int64`, `np.float64`...) |
| `(b, n, n)` | un par de ejes | `(b,)` | `ndarray` |
| `(b, c, n, n)` | dos ejes de matriz | `(b, c)` | `ndarray` |

Reglas de `dtype` (sin `dtype=` explícito), idénticas a [[np.sum]]:
- enteros de `< int_` se **promueven** al entero por defecto de la plataforma (`int64`) para reducir
  overflow; `bool` también se promueve a `int64`.
- floats y complejos conservan su tipo (`float32` → `float32`).

```python
np.trace(np.eye(4))            # np.float64(4.0)   escalar, no ndarray
type(np.trace(np.ones((5,3,3)), axis1=1, axis2=2))  # numpy.ndarray
```

## Casos de uso

### Invariantes de una matriz
```python
A = np.array([[2., 1.], [0., 3.]])
np.trace(A)                       # 5.0  = suma de la diagonal
np.linalg.eigvals(A).sum()        # 5.0  → traza = suma de autovalores
```
La traza coincide con la **suma de los autovalores** ([[np.linalg.eigvals]]); ambos son invariantes
bajo cambio de base.

### Suma de una diagonal desplazada
```python
M = np.arange(16).reshape(4, 4)
np.trace(M)             # 30   diagonal principal
np.trace(M, offset=2)   # 14   → 2 + 12 (dos por encima)
```

### Traza por lotes de matrices N-D
```python
batch = np.random.rand(100, 5, 5)       # 100 matrices 5x5
traces = np.trace(batch, axis1=-2, axis2=-1)
traces.shape            # (100,)  → una traza por matriz, sin bucle
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Shape de salida inesperado en un lote | los defectos `axis1=0, axis2=1` toman los dos PRIMEROS ejes | pasar `axis1=-2, axis2=-1` |
| Resultado negativo/absurdo | overflow del acumulador (`int8`/`int16`) | `dtype=np.int64` |
| `ValueError` por `ndim < 2` | la entrada es 1D | la traza exige al menos 2 ejes |
| Esperar la traza de una no cuadrada distinta | suma solo $\min(n,m)$ elementos | es el comportamiento correcto, no un error |
| Confundir con la diagonal | `trace` devuelve la **suma**, no los elementos | para los elementos usar [[np.diagonal]] |

## Notas relacionadas

- [[concepto_shape]] — la traza como contracción de los dos ejes de la matriz
- [[np.diagonal]] — extrae la diagonal (la traza es su suma)
- [[np.sum]] — la reducción de un eje; la traza colapsa dos
- [[np.linalg.eigvals]] — la traza es la suma de los autovalores
