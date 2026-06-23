---
title: np.linalg.eigh — autovalores y autovectores de una matriz simétrica/Hermítica
aliases:
  - eigh
  - linalg.eigh
  - np.linalg.eigh
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: tuple (eigenvalues, eigenvectors)
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.linalg.eigh — autovalores y autovectores de una matriz simétrica/Hermítica

`np.linalg.eigh` resuelve el problema de autovalores cuando la matriz es **simétrica** (real) o
**Hermítica** (compleja). Es la versión especializada y **preferida** frente a [[np.linalg.eig]]
siempre que la matriz lo sea: explota la simetría para ser **más rápida y numéricamente más estable**,
y garantiza dos propiedades que `eig` no da: los autovalores son **reales** y vienen en **orden
ascendente**, y los autovectores son **ortonormales**. Es el caballo de batalla del PCA, los
Hamiltonianos cuánticos y cualquier matriz de covarianza, Gram o $A^{\mathsf{T}}A$.

## La idea en una fórmula

El par autovalor–autovector cumple la ecuación central; la diferencia es que aquí, por la simetría
de $A$, todo sale "bonito":

$$
A\,\mathbf{v} = \lambda\,\mathbf{v}, \qquad \lambda\in\mathbb{R}, \qquad \mathbf{v}_i^{\mathsf{T}}\mathbf{v}_j=\delta_{ij}
$$

Como los autovectores son **ortonormales**, $V$ es una matriz ortogonal/unitaria ($V^{-1}=V^{\mathsf{T}}$),
y la diagonalización se vuelve una **descomposición espectral**:

$$
A = V\,\Lambda\,V^{\mathsf{T}} \qquad \Lambda=\operatorname{diag}(\lambda_0\le\lambda_1\le\dots\le\lambda_{n-1})
$$

**El mapa de shapes** — entrada `(...,n,n)` → dos salidas:

$$
\underbrace{(\dots,\,n,\,n)}_{A}\ \xrightarrow{\ \text{eigh}\ }\ \big(\ \underbrace{(\dots,\,n)}_{w\ \text{reales, ascendentes}}\ ,\ \underbrace{(\dots,\,n,\,n)}_{v\ \text{ortonormales en columnas}}\ \big)
$$

```text
   w =  [ λ0 ≤ λ1 ≤ λ2 ]      orden ASCENDENTE garantizado
   v =  columnas ortonormales:  v[:, i] = autovector de w[i],  v.T @ v == I
   relación:  A @ v[:, i] == w[i] * v[:, i]
```

## Firma

```python
np.linalg.eigh(a, UPLO='L') -> EighResult(eigenvalues, eigenvectors)
# a    : array_like, shape (..., n, n) — simétrica (real) o Hermítica (compleja)
# UPLO : {'L', 'U'} — qué triángulo de a se lee (defecto 'L', inferior)
```

## Los parámetros en detalle

### `a` — la(s) matriz(ces) simétrica(s)/Hermítica(s)
`array_like` de shape `(..., n, n)`, opcionalmente apilada en un lote. Solo se lee el **triángulo**
indicado por `UPLO`; el otro **se ignora** (se asume simetría). Por eso, si pasas una matriz no
simétrica, `eigh` **no falla**: opera como si la matriz fuera la simetrización del triángulo leído,
lo que puede dar un resultado silenciosamente distinto al esperado.

### `UPLO` — qué triángulo se usa (`'L'` o `'U'`)
Selecciona la mitad de `a` que se lee: `'L'` (defecto) el triángulo **inferior**, `'U'` el
**superior**. La otra mitad se reconstruye por simetría/conjugación, no se mira.

```python
a = np.array([[2.0, 1.0],
              [9.9, 2.0]])   # triángulo superior "sucio" (9.9 no es 1.0)
np.linalg.eigh(a, UPLO='L').eigenvalues   # usa el 1.0 inferior → array([1., 3.])
np.linalg.eigh(a, UPLO='U').eigenvalues   # usaría el 9.9 superior → otro resultado
```

## El caso N-D

Como [[np.matmul]] y `eig`, los **dos últimos ejes** son la matriz y los anteriores son **lote**.
No hay `axis`; la descomposición es siempre sobre el bloque `(n, n)` final.

| `a.shape` | `w.shape` | `v.shape` | qué pasa |
|-----------|-----------|-----------|----------|
| `(n, n)` | `(n,)` | `(n, n)` | una descomposición |
| `(b, n, n)` | `(b, n)` | `(b, n, n)` | `b` descomposiciones independientes |
| `(b, c, n, n)` | `(b, c, n)` | `(b, c, n, n)` | lote 2D |

```python
lote = np.random.rand(8, 4, 4)
sim  = lote + lote.transpose(0, 2, 1)        # simetrizar cada matriz
w, v = np.linalg.eigh(sim)                   # w:(8,4) ascendente  v:(8,4,4)
np.allclose(sim @ v, v @ (w[..., None, :] * np.eye(4)))   # True
```

## Vectorización

El lote evita el bucle Python y delega en **LAPACK** (rutina `syevd`/`heevd`, optimizada para
matrices simétricas):

```python
# Bucle Python: una eigh por matriz
def batch_eigh(A):
    ws, vs = [], []
    for k in range(A.shape[0]):
        w, v = np.linalg.eigh(A[k])
        ws.append(w); vs.append(v)
    return np.array(ws), np.array(vs)

# Vectorizado: NumPy recorre el lote en C / LAPACK
w, v = np.linalg.eigh(A)
```

Ver [[concepto_vectorizacion]]: describes *qué* descomponer, no *cómo* iterar el lote.

## Valor de retorno

Devuelve un **namedtuple** `EighResult(eigenvalues, eigenvectors)` —la tupla
`(autovalores, autovectores)`, desempaquetable como `w, v = np.linalg.eigh(a)`.

| Posición | Nombre | Shape | Contenido |
|----------|--------|-------|-----------|
| 0 | `eigenvalues` (`w`) | `(..., n)` | los $n$ autovalores **reales**, en **orden ascendente** (`w[..., 0]` el menor, `w[..., -1]` el mayor) |
| 1 | `eigenvectors` (`v`) | `(..., n, n)` | matriz cuyas **columnas** son los autovectores **ortonormales**: `v[..., :, i]` ↔ `w[..., i]` |

> [!tip] Los autovectores son las COLUMNAS de `v`, y `v` es ortogonal
> El autovector de `w[i]` es `v[:, i]` (columna), nunca `v[i]`. Como las columnas son ortonormales,
> `v.T @ v == I`. Y como `w` está **ordenado ascendente**, la **componente principal** (mayor
> autovalor) es `v[:, -1]`.

```python
a = np.array([[2.0, 1.0],
              [1.0, 2.0]])              # simétrica
w, v = np.linalg.eigh(a)
w                                       # array([1., 3.])  → reales y ascendentes
np.allclose(v.T @ v, np.eye(2))         # True → columnas ortonormales
np.allclose(a @ v, v @ np.diag(w))      # True → A V = V Λ
```

## Casos de uso

### PCA: direcciones de máxima varianza
```python
X = np.random.rand(100, 3)
C = np.cov(X, rowvar=False)             # covarianza 3×3 (simétrica)
w, v = np.linalg.eigh(C)
componente_principal = v[:, -1]         # mayor autovalor → al FINAL (orden ascendente)
```

### Test de definida positiva
```python
G = X @ X.T                             # matriz de Gram (simétrica, ≥0)
es_pos_def = np.all(np.linalg.eigh(G).eigenvalues > 0)
```

### Lote de Hamiltonianos (N-D): niveles de energía
```python
H = np.random.rand(50, 6, 6)
H = H + H.transpose(0, 2, 1)            # 50 matrices simétricas 6×6
energias = np.linalg.eigh(H).eigenvalues   # (50, 6) reales y ordenadas por matriz
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Last 2 dimensions must be square` | matriz no cuadrada | verificar shape `(..., n, n)` |
| Resultado inesperado con matriz no simétrica | `eigh` ignora medio triángulo | asegurar simetría o usar [[np.linalg.eig]] |
| Tomar `v[i]` como autovector | son **columnas**, no filas | usar `v[:, i]` |
| Buscar el mayor autovalor en `w[0]` | el orden es **ascendente** | el máximo está en `w[-1]` |
| Resultado distinto al cambiar `UPLO` | la matriz no era simétrica | simetrizar antes, o usar `eig` |

## Notas relacionadas

- [[concepto_shape]] — el lote `(..., n, n)` y el mapa a las dos salidas
- [[np.linalg.eig]] — la versión general (matrices no simétricas)
- [[np.linalg.eigvalsh]] — solo los autovalores de una matriz Hermítica
- [[np.linalg.eigvals]] · [[np.trace]] · [[np.linalg.det]]
