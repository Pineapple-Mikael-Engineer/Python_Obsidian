---
title: np.linalg.tensorsolve — resuelve la ecuación tensorial Ax = b
aliases:
  - tensorsolve
  - linalg.tensorsolve
  - np.linalg.tensorsolve
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: ndarray
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.linalg.tensorsolve — resuelve la ecuación tensorial $A\mathbf{x}=\mathbf{b}$

`np.linalg.tensorsolve` resuelve $A\mathbf{x}=\mathbf{b}$ cuando $A$ es un **tensor N-D** y el producto
se entiende como una **contracción tensorial** (`np.tensordot`), no como un producto matriz·vector. Es la
**generalización N-dimensional** de [[np.linalg.solve]]: internamente **reordena y aplana** $A$ a una
matriz cuadrada, resuelve el sistema 2D equivalente y **reconstruye** $\mathbf{x}$ con la forma adecuada.
La incógnita $\mathbf{x}$ y el lado $\mathbf{b}$ pueden ser tensores de varios ejes.

## La idea en una fórmula

El sistema tensorial contrae los **últimos ejes** de $A$ contra los ejes de $\mathbf{x}$, dejando los
ejes de $\mathbf{b}$:

$$
\sum_{k_0,\dots,k_{r-1}} A_{\,i_0\dots i_{p-1},\ k_0\dots k_{r-1}}\; x_{\,k_0\dots k_{r-1}}
\;=\; b_{\,i_0\dots i_{p-1}}
\qquad\Longleftrightarrow\qquad \text{tensordot}(A,\mathbf{x}) = \mathbf{b}
$$

La estrategia de NumPy es **reducirlo a un sistema 2D**: aplana los ejes de $\mathbf{b}$ en una dimensión
$P=\prod b.\text{shape}$ y los ejes de $\mathbf{x}$ en $Q=\prod x.\text{shape}$, obteniendo una matriz
$\tilde A$ de shape $(P, Q)$. Para que sea **cuadrada e invertible** se exige $P = Q$, y entonces
resuelve $\tilde A\,\tilde{\mathbf{x}} = \tilde{\mathbf{b}}$ como un `solve` ordinario.

**El mapa de shapes** — los ejes de $A$ se parten en los que aparean con $\mathbf{b}$ (primeros) y los
que forman $\mathbf{x}$ (últimos):

$$
A:\ (\underbrace{b_0,\dots,b_{p-1}}_{\text{ejes de }b},\ \underbrace{x_0,\dots,x_{r-1}}_{\text{ejes de }x})
\ ,\quad b:\ (b_0,\dots,b_{p-1})\ \xrightarrow{\ \text{tensorsolve}\ }\ x:\ (x_0,\dots,x_{r-1})
$$
$$
\text{condición de cuadratura:}\qquad \prod_i b_i \;=\; \prod_j x_j
$$

```text
A.shape = (2, 3, 2, 3)   →  aplana a  Ã (6, 6)   (P = 2·3 = 6,  Q = 2·3 = 6)
b.shape = (2, 3)         →  aplana a  b̃ (6,)
x.shape = (2, 3)         ←  resuelve Ã x̃ = b̃  y reconstruye
```

## Firma

```python
np.linalg.tensorsolve(a, b, axes=None) -> ndarray
```

## Los parámetros en detalle

### `a` — tensor de coeficientes
`array_like` N-D. Sus ejes se dividen en dos grupos: los que **aparean con `b`** (los que se contraen) y
los que **forman `x`**. El producto de las dimensiones de cada grupo debe coincidir para que la matriz
aplanada $\tilde A$ sea cuadrada (ver [[concepto_shape]]). Si no, lanza `LinAlgError` al intentar invertir.

### `b` — tensor del lado derecho
`array_like` N-D. Su shape **determina qué ejes de `a` se contraen**: NumPy busca el grupo de ejes
iniciales de `a` que reproduce `b.shape`; el resto de ejes de `a` quedan para `x`.

### `axes` — ejes de `a` movidos al final antes de resolver
`None` (defecto) o lista de ejes. Indica qué ejes de `a` se **reordenan al final** (los que forman `x`)
antes de aplanar. Sirve cuando los ejes de la incógnita **no son los últimos** de `a`. Con `None`, NumPy
asume que los ejes de `x` ya están al final.

```python
a = np.random.randn(3, 4, 6, 2)   # 6·2 = 3·4 = 12 → cuadrado al aplanar
b = np.random.randn(3, 4)
x = np.linalg.tensorsolve(a, b)
x.shape                            # (6, 2)  → los dos últimos ejes de a forman x
```

## El caso N-D

Aquí lo N-D **es** la función: `a` siempre es un tensor de orden $\geq 2$ y la clave es leer qué ejes van
a `x` y cuáles a `b`. Algunos patrones:

| `a.shape` | `b.shape` | `x.shape` | lectura |
|-----------|-----------|-----------|---------|
| `(M, M)` | `(M,)` | `(M,)` | caso 2D → equivale a [[np.linalg.solve]] |
| `(2, 3, 2, 3)` | `(2, 3)` | `(2, 3)` | $\tilde A$ es `(6, 6)` |
| `(2, 3, 6, 4)` | `(2, 3)` | `(6, 4)` | ejes `b`= primeros 2, ejes `x`= últimos 2 |
| `(2, 3, 4, 4, 3, 2)` | `(2, 3, 4)` | `(4, 3, 2)` | $\tilde A$ es `(24, 24)` |

```python
a = np.eye(24).reshape(2, 3, 4, 4, 3, 2)   # aplana a (24, 24)
b = np.random.randn(2, 3, 4)
x = np.linalg.tensorsolve(a, b)
x.shape                                     # (4, 3, 2)
np.allclose(np.tensordot(a, x, axes=b.ndim), b)   # True
```

La regla mecánica: los **primeros** ejes de `a` deben reproducir `b.shape`; los **restantes** forman `x`,
y su producto debe igualar `prod(b.shape)`.

## Vectorización

`tensorsolve` no expone un eje de lote; su "vectorización" es **conceptual**: empaqueta un sistema de
ecuaciones expresado sobre múltiples índices tensoriales en un único `solve` 2D, evitando que tengas que
aplanar, resolver y reconstruir a mano. Equivale a:

```python
# A mano: aplanar, resolver con solve, reconstruir
def tensorsolve_manual(a, b):
    P = b.size
    A2 = a.reshape(P, -1)          # (P, Q)
    x2 = np.linalg.solve(A2, b.ravel())
    return x2.reshape(a.shape[b.ndim:])

# Equivalente directo (NumPy gestiona reorden y reshape):
np.linalg.tensorsolve(a, b)
```

El valor está en la [[concepto_vectorizacion|abstracción]]: razonas en términos de ejes del tensor, no de
una matriz aplanada que tú mismo tendrías que armar.

## Valor de retorno

Devuelve un único `ndarray` `x` (nunca tupla):

| `a` | `b` | `x` (shape) | tipo |
|-----|-----|-------------|------|
| `(2, 3, 2, 3)` | `(2, 3)` | `(2, 3)` | `ndarray` |
| `(3, 4, 6, 2)` | `(3, 4)` | `(6, 2)` | `ndarray` |
| `(M, M)` | `(M,)` | `(M,)` | `ndarray` (igual que `solve`) |
| no cuadrado al aplanar | — | — | lanza `LinAlgError` |

- El shape de `x` son exactamente los **ejes de `a` que no aparean con `b`** (reordenados según `axes`).
- El `dtype` se promueve a punto flotante, como en [[np.linalg.solve]].

## Casos de uso

### Ecuación tensorial de transformaciones multieje
```python
a = np.eye(24).reshape(2, 3, 4, 4, 3, 2)   # operador lineal sobre tensores (2,3,4)
b = np.random.randn(2, 3, 4)
x = np.linalg.tensorsolve(a, b)
x.shape                                     # (4, 3, 2)  → tensor incógnita
```

### Verificar la solución con `tensordot`
```python
a = np.random.randn(3, 4, 6, 2)
b = np.random.randn(3, 4)
x = np.linalg.tensorsolve(a, b)
np.allclose(np.tensordot(a, x, axes=x.ndim), b)   # True
```

### Equivalencia con `solve` en 2D
En el caso plano, `tensorsolve` **es** un `solve`: el tensor $A$ ya es una matriz cuadrada y $\mathbf{b}$
un vector. El sistema concreto y su solución:

$$
\begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix}
\begin{bmatrix} x_0 \\ x_1 \end{bmatrix}
=
\begin{bmatrix} 9 \\ 8 \end{bmatrix}
\quad\Longrightarrow\quad
\begin{bmatrix} x_0 \\ x_1 \end{bmatrix}
=
\begin{bmatrix} 2 \\ 3 \end{bmatrix}
$$

```python
A = np.array([[3., 1.], [1., 2.]])
b = np.array([9., 8.])
np.linalg.tensorsolve(A, b)   # [2., 3.]  → idéntico a np.linalg.solve(A, b)
```

### Operador tensorial $(2,3,2,3)$ que aplana a $\tilde A\,(6\times 6)$
El operador $A$ de shape `(2,3,2,3)` contrae sus **dos últimos ejes** contra una incógnita $\mathbf{x}$
de shape `(2,3)`, igualando un lado $\mathbf{b}$ de shape `(2,3)`. Al aplanar, el sistema es una matriz
$\tilde A$ de $6\times 6$ resuelta con `solve`:

$$
\underbrace{(2,\,3,\,2,\,3)}_{A}\ ,\ \underbrace{(2,\,3)}_{b}\ \xrightarrow{\ \text{tensorsolve}\ }\ \underbrace{(2,\,3)}_{x}
\qquad\text{con}\qquad P=2\cdot 3=6=2\cdot 3=Q
$$

```python
A = np.eye(6).reshape(2, 3, 2, 3)   # operador identidad → aplana a Ã (6, 6)
b = np.arange(6.).reshape(2, 3)     # lado (2, 3)
x = np.linalg.tensorsolve(A, b)
x.shape                              # (2, 3)  → incógnita tensorial
np.allclose(np.tensordot(A, x, axes=x.ndim), b)   # True
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Singular matrix` | el tensor aplanado $\tilde A$ es singular | revisar `a`; el sistema no tiene solución única |
| `LinAlgError` / `ValueError` al aplanar | los productos de ejes no forman matriz cuadrada | ajustar shapes o usar `axes` para igualar $\prod x_j = \prod b_i$ |
| `x` con shape inesperado | los ejes de `x` no eran los últimos de `a` | especificar `axes` explícitamente |
| Usarla para un `Ax=b` normal | sobrecomplica un sistema matricial | usar [[np.linalg.solve]]: más claro |

## Notas relacionadas

- [[concepto_shape]] — partir los ejes de `a` en grupo-`b` y grupo-`x`
- [[concepto_vectorizacion]] — empaquetar el sistema tensorial en un `solve`
- [[np.linalg.solve]] — el caso 2D; úsalo salvo que el problema sea genuinamente tensorial
- [[np.linalg.lstsq]] — cuando el sistema no es cuadrado (mínimos cuadrados)
- [[np.linalg.tensorinv]] — la inversa tensorial análoga
- [[index]] — sistemas de ecuaciones
