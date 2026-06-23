---
title: np.linalg.cond — número de condición (sensibilidad numérica) de una matriz
aliases:
  - cond
  - linalg.cond
  - np.linalg.cond
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: escalar | ndarray
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.linalg.cond — número de condición (sensibilidad numérica) de una matriz

`np.linalg.cond` mide cuán **mal condicionada** está una matriz: cuánto se amplifican los errores
de los datos al resolver el sistema $Ax=b$. Un número de condición $\kappa$ grande significa que la
solución es **sensible** a perturbaciones diminutas (ruido, redondeo) y que la matriz está cerca de
ser singular. Es el diagnóstico que se hace **antes** de invertir o resolver: avisa de pérdida de
precisión. Internamente, con la norma 2 se reduce a un cociente de [[np.linalg.svd|valores
singulares]].

## La idea en una fórmula

El número de condición es el producto de la norma de $A$ por la de su inversa; con la norma
espectral (`p=2`) equivale al cociente entre el mayor y el menor valor singular:

$$
\kappa(A) = \lVert A\rVert\,\lVert A^{-1}\rVert
\qquad\Longrightarrow\qquad
\kappa_2(A) = \frac{\sigma_{\max}(A)}{\sigma_{\min}(A)} \;\ge\; 1
$$

**El mapa de shapes**: `cond` colapsa los dos últimos ejes (la matriz) a un escalar y conserva
cualquier eje de lote anterior:

$$
(\underbrace{\dots}_{\text{lote}},\, m,\, n)\ \xrightarrow{\ \text{cond}\ }\ (\underbrace{\dots}_{\text{lote}})
$$

La interpretación práctica: con $\kappa \approx 10^{k}$ esperas **perder unos $k$ dígitos** de
precisión al resolver. $\kappa = 1$ es perfecto (matrices ortogonales); $\kappa \to \infty$ cuando
$\sigma_{\min} \to 0$, es decir, cuando la matriz tiende a singular.

```text
σ_max grande, σ_min ~ 0  →  κ enorme  →  el sistema "estira" mucho una dirección
                                          y "aplasta" otra: la inversa amplifica el ruido
```

## Firma

```python
np.linalg.cond(
    x,                 # array_like (..., M, N): matriz o pila de matrices
    p=None,            # None | 1 | -1 | 2 | -2 | inf | -inf | 'fro': norma usada
) -> escalar | ndarray
```

## Los parámetros en detalle

### `x` — la matriz de entrada
`array_like` de shape `(..., M, N)`. Para `p=2`/`None`/`-2` puede **no ser cuadrada** (usa los
valores singulares de la SVD). Para el resto de normas debe ser **cuadrada e invertible**, porque
`cond` calcula explícitamente `inv(x)`. Con más de 2 ejes opera por lotes sobre los dos últimos.

### `p` — la norma con la que se mide
Selecciona la norma de la definición $\kappa = \lVert A\rVert\,\lVert A^{-1}\rVert$. Por defecto
(`None`) usa la norma 2 (cociente de valores singulares vía SVD), la interpretación estándar.

| `p` | Norma / fórmula | Requiere |
|-----|-----------------|----------|
| `None` | norma 2: $\sigma_{\max}/\sigma_{\min}$ | solo SVD (admite no cuadrada) |
| `2` | $\sigma_{\max}/\sigma_{\min}$ | solo SVD |
| `-2` | $\sigma_{\min}/\sigma_{\max}$ | solo SVD |
| `1` | norma 1 (máx. suma de columna) | cuadrada e invertible (`inv`) |
| `-1` | norma 1 de mínimo | cuadrada e invertible |
| `np.inf` | norma ∞ (máx. suma de fila) | cuadrada e invertible |
| `-np.inf` | norma ∞ de mínimo | cuadrada e invertible |
| `'fro'` | norma de Frobenius | cuadrada e invertible |

```python
A = np.array([[1.0, 2.0],
              [2.0, 4.001]])   # casi linealmente dependiente
np.linalg.cond(A)              # ~ 5e3   → mal condicionada
np.linalg.cond(A, p=1)         # otra norma, otro valor (mismo orden de magnitud)
```

## El caso N-D / axis

`cond` no tiene parámetro `axis`: trata **siempre** los dos últimos ejes como la matriz y todo lo
anterior como **lote** (igual que [[np.matmul]] o el resto de `np.linalg`). El resultado tiene el
shape del lote, con los dos ejes de la matriz colapsados a un escalar.

| `x.shape` | salida | lectura |
|-----------|--------|---------|
| `(m, n)` | `()` escalar | número de condición de la matriz |
| `(b, m, n)` | `(b,)` | un número de condición por matriz del lote |
| `(b, c, m, n)` | `(b, c)` | una rejilla de números de condición |

```python
B = np.stack([np.eye(3), np.array([[1.,1.,1.],[0.,1e-8,0.],[0.,0.,1.]])])
B.shape                 # (2, 3, 3)  → 2 matrices
np.linalg.cond(B)       # [1.0, 1e8...]  → bien y mal condicionada, en una llamada
```

## Vectorización

El caso por lotes evita un bucle Python sobre las matrices: NumPy aplica la SVD (o la inversa) a
cada una en C/LAPACK, sin saltar al intérprete por matriz. Es [[concepto_vectorizacion]] aplicada
al álgebra lineal:

```python
# Bucle Python: una SVD por matriz del lote
def conds(stack):
    out = np.empty(stack.shape[0])
    for i in range(stack.shape[0]):
        out[i] = np.linalg.cond(stack[i])
    return out

# Vectorizado: NumPy recorre el lote en LAPACK
np.linalg.cond(stack)
```

Mismo resultado; la versión vectorizada delega los `stack.shape[0]` cómputos en código numérico
optimizado en vez de en el intérprete.

## Valor de retorno

| Entrada | `p` | salida | tipo |
|---------|-----|--------|------|
| `(m, n)` | cualquiera | `()` | **escalar de NumPy** (`np.float64`) |
| `(b, m, n)` | cualquiera | `(b,)` | `ndarray` de flotantes |
| singular (algún `σ_min = 0`) | cualquiera | `inf` | `np.float64` / `ndarray` con `inf` |

- El retorno es siempre **flotante** y $\ge 1$ (por definición $\kappa \ge 1$).
- Para una matriz **singular** devuelve `inf` (con `p=2`, porque $\sigma_{\min}=0$); con otras
  normas suele lanzar `LinAlgError` al no poder invertir.

```python
I = np.eye(3)
np.linalg.cond(I)        # 1.0   → perfectamente condicionada
type(np.linalg.cond(I))  # numpy.float64
```

## Casos de uso

### Diagnosticar un sistema antes de resolverlo
```python
A = np.array([[1.0, 1.0], [1.0, 1.0001]])
b = np.array([2.0, 2.0001])
np.linalg.cond(A)        # ~ 4e4   → la solución será sensible al ruido
x = np.linalg.solve(A, b)# resuélvelo sabiendo que pierdes ~4-5 dígitos
```

### Estimar dígitos de precisión perdidos
```python
k = np.linalg.cond(A)
np.log10(k)              # ~ 4.6   → ≈ 4-5 dígitos perdidos en doble precisión
```

### Comparar estabilidad de matrices candidatas
```python
np.linalg.cond(np.eye(4))             # 1.0      → ideal
np.linalg.cond(np.vander([1,2,3,4]))  # ~ 1e3    → Vandermonde mal condicionada
```

### N-D: condición de un lote de matrices
```python
lote = np.random.rand(5, 4, 4)
np.linalg.cond(lote)     # (5,)  → un κ por matriz, para filtrar las inestables
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `cond` devuelve `inf` | matriz singular ($\sigma_{\min}=0$) | revisar dependencias lineales; no es invertible |
| `LinAlgError` | `p ≠ 2` con matriz no cuadrada o singular | usar `p=2`/`None`, que admite SVD |
| Resultados poco fiables tras resolver | `cond` alto ignorado | regularizar o reformular el problema |
| Esperar precisión total | confiar en un sistema con `cond` enorme | estimar dígitos perdidos como `log10(cond)` |
| Tratar `cond` alto como un error | es un **diagnóstico**, no un fallo | avisa de pérdida de precisión, no la causa |

## Notas relacionadas

- [[np.linalg.svd]] — los valores singulares de los que sale $\kappa_2 = \sigma_{\max}/\sigma_{\min}$
- [[np.linalg.norm]] — las normas que componen $\kappa = \lVert A\rVert\,\lVert A^{-1}\rVert$
- [[np.linalg.matrix_rank]] · [[np.linalg.solve]] · [[np.linalg.lstsq]]
- [[normas_condiciones/index|normas y condiciones]] — la nota madre del grupo
