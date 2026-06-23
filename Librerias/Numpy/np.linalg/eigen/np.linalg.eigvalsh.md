---
title: np.linalg.eigvalsh — solo los autovalores de una matriz simétrica/Hermítica
aliases:
  - eigvalsh
  - linalg.eigvalsh
  - np.linalg.eigvalsh
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

# np.linalg.eigvalsh — solo los autovalores de una matriz simétrica/Hermítica

`np.linalg.eigvalsh` calcula **solo los autovalores** de una matriz **simétrica** (real) o
**Hermítica** (compleja), sin los autovectores. Es la versión **barata** de [[np.linalg.eigh]] y la
opción correcta cuando la matriz es simétrica y solo necesitas el espectro: test de definida
positiva, número de condición, inercia o niveles de energía. Por la simetría, los autovalores son
**reales** y vienen en **orden ascendente** —algo que [[np.linalg.eigvals]] no garantiza—.

## La idea en una fórmula

Los autovalores son los $\lambda$ de la ecuación central; por la simetría de $A$ son **reales**:

$$
A\,\mathbf{v} = \lambda\,\mathbf{v}, \qquad \lambda\in\mathbb{R}, \qquad \det(A-\lambda I)=0
$$

Se relacionan directamente con dos invariantes de la matriz, útiles como chequeo: la **traza** es la
suma y el **determinante** el producto de los autovalores.

$$
\sum_i \lambda_i = \operatorname{tr}(A) \qquad\qquad \prod_i \lambda_i = \det(A)
$$

Ver [[np.trace]] (la traza) y [[np.linalg.det]] (el determinante).

**El mapa de shapes** — entrada `(...,n,n)` → **una sola** salida `(...,n)`:

$$
\underbrace{(n_0,\dots,n_{k-1},\,n,\,n)}_{A}\ \xrightarrow{\ \text{eigvalsh}\ }\ \underbrace{(n_0,\dots,n_{k-1},\,n)}_{w\ \text{reales, ascendentes}}
$$

## Firma

```python
np.linalg.eigvalsh(a, UPLO='L') -> ndarray
# a    : array_like, shape (..., n, n) — simétrica (real) o Hermítica (compleja)
# UPLO : {'L', 'U'} — qué triángulo de a se lee (defecto 'L', inferior)
```

## Los parámetros en detalle

### `a` — la(s) matriz(ces) simétrica(s)/Hermítica(s)
`array_like` de shape `(..., n, n)`, opcionalmente apilada. Solo se lee el **triángulo** indicado por
`UPLO`; el otro **se ignora** (se asume simetría). Si pasas una matriz no simétrica, `eigvalsh`
**no falla**: opera sobre la simetrización del triángulo leído, lo que puede dar un resultado
silenciosamente distinto.

### `UPLO` — qué triángulo se usa (`'L'` o `'U'`)
`'L'` (defecto) lee el triángulo **inferior**; `'U'` el **superior**. La otra mitad se reconstruye por
simetría/conjugación, no se mira.

```python
lote = np.random.rand(4, 3, 3)
sim  = lote + lote.transpose(0, 2, 1)   # forzar simetría por matriz
np.linalg.eigvalsh(sim).shape           # (4, 3)
```

## El caso N-D

Los **dos últimos ejes** son la matriz; los anteriores son **lote**. No hay `axis`.

| `a.shape` | `w.shape` | qué pasa |
|-----------|-----------|----------|
| `(n, n)` | `(n,)` | espectro de una matriz |
| `(b, n, n)` | `(b, n)` | espectro de cada una de las `b` matrices |
| `(b, c, n, n)` | `(b, c, n)` | lote 2D |

```python
lote = np.random.rand(100, 5, 5)
sim  = lote + lote.transpose(0, 2, 1)
w = np.linalg.eigvalsh(sim)             # (100, 5) reales y ascendentes por matriz
condicion = w[:, -1] / w[:, 0]          # número de condición por matriz (si w[:,0] > 0)
```

## Vectorización

El lote calcula el espectro de muchas matrices sin bucle Python, delegando en **LAPACK** (rutina
`syevd`/`heevd` para matrices simétricas):

```python
# Bucle Python: un eigvalsh por matriz
def batch_eigvalsh(A):
    return np.array([np.linalg.eigvalsh(A[k]) for k in range(A.shape[0])])

# Vectorizado: NumPy recorre el lote en C / LAPACK
w = np.linalg.eigvalsh(A)
```

Ver [[concepto_vectorizacion]].

## Valor de retorno

Devuelve **un solo `ndarray`** (no una tupla): los autovalores.

| Salida | Shape | Contenido |
|--------|-------|-----------|
| `w` | `(..., n)` | los $n$ autovalores por matriz, **reales** y en **orden ascendente** (`w[..., 0]` el menor, `w[..., -1]` el mayor) |

- A diferencia de `eigvals`, aquí el **orden está garantizado** (ascendente) y el resultado **siempre
  es real** (nunca complejo espurio).

```python
a = np.array([[2.0, 1.0],
              [1.0, 2.0]])              # simétrica
np.linalg.eigvalsh(a)                   # array([1., 3.])  → reales y ascendentes
```

## Casos de uso

### Ejemplo trabajado con números: espectro de una matriz simétrica

Para la matriz **simétrica** 2×2:

$$
A=\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}
\ \xrightarrow{\ \text{eigvalsh}\ }\
w=\begin{bmatrix} 1 & 3 \end{bmatrix}
$$

$\det(A-\lambda I)=(2-\lambda)^2-1=0$ da $\lambda=1,3$, y `eigvalsh` los devuelve **reales** y en
**orden ascendente**. Una matriz simétrica 3×3 tridiagonal muestra lo mismo en dimensión mayor:

$$
B=\begin{bmatrix} 2 & 1 & 0 \\ 1 & 2 & 1 \\ 0 & 1 & 2 \end{bmatrix}
\ \xrightarrow{\ \text{eigvalsh}\ }\
w=\begin{bmatrix} 2-\sqrt2 & 2 & 2+\sqrt2 \end{bmatrix}
\approx
\begin{bmatrix} 0.586 & 2 & 3.414 \end{bmatrix}
$$

```python
a = np.array([[2.0, 1.0],
              [1.0, 2.0]])
np.linalg.eigvalsh(a)                   # array([1., 3.])  → reales y ascendentes

b = np.array([[2.0, 1.0, 0.0],
              [1.0, 2.0, 1.0],
              [0.0, 1.0, 2.0]])
np.linalg.eigvalsh(b)                   # array([0.586, 2., 3.414])  → ascendentes
```

### Test de definida positiva (sin autovectores)
```python
C = np.cov(np.random.rand(50, 4), rowvar=False)   # covarianza 4×4 (simétrica)
np.all(np.linalg.eigvalsh(C) > 0)                  # True → definida positiva
```

### Número de condición de una matriz SPD
```python
w = np.linalg.eigvalsh(C)
cond = w[-1] / w[0]      # mayor / menor (ambos > 0 en SPD)
```

### Lote (N-D): inercia / chequeo con la traza

Para un lote `(b, n, n)` simétrico la salida es `(b, n)`: `n` autovalores reales ascendentes por
matriz, sin autovectores.

```python
H = np.random.rand(20, 6, 6)           # b=20 matrices 6×6  → shape (20, 6, 6)
H = H + H.transpose(0, 2, 1)           # simetrizar cada matriz del lote
w = np.linalg.eigvalsh(H)              # w: (20, 6)
w.shape                                # (20, 6)
np.allclose(w.sum(axis=1), np.trace(H, axis1=1, axis2=2))   # True (suma = traza)

# lote 2D (4D): (b, c, n, n) → (b, c, n)
B = np.random.rand(9, 4, 5, 5)
B = B + B.transpose(0, 1, 3, 2)               # simetrizar el bloque (5,5) final
np.linalg.eigvalsh(B).shape                   # (9, 4, 5)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Last 2 dimensions must be square` | matriz no cuadrada | verificar shape `(..., n, n)` |
| Esperar una tupla `(w, v)` | `eigvalsh` devuelve **solo** `w` | usar [[np.linalg.eigh]] para los autovectores |
| Resultado distinto al esperado | matriz no simétrica; medio triángulo ignorado | asegurar simetría o usar `eigvals` |
| Buscar el máximo en `w[0]` | el orden es **ascendente** | el máximo está en `w[-1]` |

## Notas relacionadas

- [[concepto_shape]] — el lote `(..., n, n)` y la contracción a `(..., n)`
- [[np.linalg.eigh]] — autovalores **y** autovectores de una matriz simétrica/Hermítica
- [[np.linalg.eigvals]] — solo autovalores de una matriz general
- [[np.trace]] — la suma de autovalores · [[np.linalg.det]] — el producto · [[np.linalg.eig]]
