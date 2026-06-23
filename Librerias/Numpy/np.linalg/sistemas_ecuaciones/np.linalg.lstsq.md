---
title: np.linalg.lstsq — solución por mínimos cuadrados de Ax = b
aliases:
  - lstsq
  - linalg.lstsq
  - np.linalg.lstsq
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: tuple
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.linalg.lstsq — solución por **mínimos cuadrados** de $A\mathbf{x}=\mathbf{b}$

`np.linalg.lstsq` resuelve $A\mathbf{x}=\mathbf{b}$ cuando $A$ **no es cuadrada** (más ecuaciones que
incógnitas, o al revés) o es de **rango deficiente**: en esos casos no existe una solución exacta, así
que devuelve la $\mathbf{x}$ que **minimiza el error** $\lVert A\mathbf{x}-\mathbf{b}\rVert_2$. Es el
motor de la **regresión lineal** y del **ajuste polinómico** en NumPy. A diferencia de
[[np.linalg.solve]], devuelve una **tupla de cuatro elementos**, no solo $\mathbf{x}$.

## La idea en una fórmula

No se resuelve el sistema (no tiene solución exacta), se **minimiza el residuo** en norma euclídea:

$$
\mathbf{x}^\star \;=\; \arg\min_{\mathbf{x}}\ \lVert A\mathbf{x}-\mathbf{b}\rVert_2^2
$$

Geométricamente, $A\mathbf{x}^\star$ es la **proyección** de $\mathbf{b}$ sobre el espacio columna de
$A$. NumPy lo calcula vía **SVD** (descomposición en valores singulares), lo que lo hace robusto ante
rango deficiente.

**El mapa de shapes** — $A$ es rectangular $(M,N)$ ($M$ ecuaciones, $N$ incógnitas); $\mathbf{b}$ tiene
$M$ filas; la solución $\mathbf{x}$ tiene $N$:

$$
(M,\,N)\ ,\ (M,)\ \xrightarrow{\ \text{lstsq}\ }\ \underbrace{(N,)}_{x}\,,\ \dots
$$
$$
(M,\,N)\ ,\ (M,\,K)\ \xrightarrow{\ \text{lstsq}\ }\ \underbrace{(N,\,K)}_{x}\,,\ \dots
\qquad (K\ \text{problemas a la vez})
$$

(los `…` son las otras tres salidas; ver **Valor de retorno**). Típicamente $M>N$ (**sobredeterminado**:
más datos que parámetros).

## Firma

```python
np.linalg.lstsq(a, b, rcond=None) -> tuple   # (x, residuals, rank, s)
```

## Los parámetros en detalle

### `a` — matriz de diseño
`array_like` de shape `(M, N)`. En regresión, las **filas son observaciones** y las **columnas son
features/regresores**. Para el caso sobredeterminado típico, `M > N`. El [[concepto_shape|shape]] de
`x` es `(N,)` o `(N, K)` según `b`.

### `b` — observaciones / lado derecho
`array_like` de shape `(M,)` o `(M, K)`. Con `(M, K)` resuelve **`K` problemas de mínimos cuadrados a la
vez**, cada columna independiente (misma `a`, distintos objetivos).

### `rcond` — corte de valores singulares (regularización de rango)
Los valores singulares menores que `rcond * s.max()` se tratan como **cero**. Esto descarta direcciones
casi degeneradas y estabiliza el ajuste cuando $A$ es de rango deficiente.

> [!warning] Pasa `rcond=None` explícitamente
> `rcond=None` selecciona el valor recomendado por la versión actual de NumPy (basado en la precisión de
> máquina). Omitir el argumento emitía `FutureWarning` en versiones antiguas, donde el defecto era el
> heredado `-1`. En código nuevo: siempre `rcond=None`.

```python
np.linalg.lstsq(A, b, rcond=None)   # comportamiento estable recomendado
```

## El caso N-D

`lstsq` es estrictamente **2D en `a`**: no acepta lotes de matrices (`a` debe ser `(M, N)`, no
`(..., M, N)`). El único eje "extra" admitido vive en `b`: pasar `(M, K)` resuelve `K` sistemas de
mínimos cuadrados que comparten la matriz `a`, y entonces `x` sale `(N, K)` y `residuals` sale `(K,)`.

```python
A = np.random.rand(20, 3)     # 20 ecuaciones, 3 incógnitas
B = np.random.rand(20, 4)     # 4 objetivos distintos
x, res, rank, s = np.linalg.lstsq(A, B, rcond=None)
x.shape       # (3, 4)  → una solución por columna de B
res.shape     # (4,)    → un residuo por columna
```

Para lotes genuinos de problemas con matrices distintas, hay que iterar o montarlo a mano: `lstsq` no
broadcastea los ejes previos de `a`.

## Vectorización

El caso `(M, K)` es el ejemplo de [[concepto_vectorizacion]]: una sola SVD de `a` sirve para resolver
los `K` objetivos, en vez de llamar `lstsq` `K` veces.

```python
# Bucle Python: una lstsq por columna objetivo
def multi_lstsq(A, B):
    return np.stack([np.linalg.lstsq(A, B[:, k], rcond=None)[0]
                     for k in range(B.shape[1])], axis=1)

# Vectorizado: una sola descomposición de A para todas las columnas
np.linalg.lstsq(A, B, rcond=None)[0]
```

Mismo resultado; la versión vectorizada factoriza `A` una vez y aplica la pseudo-inversa a todas las
columnas de golpe.

## Valor de retorno

Devuelve una **tupla `(x, residuals, rank, s)`** — desempaquétala siempre o indexa `[0]` para quedarte
con la solución:

| Pos | Nombre | Tipo / shape | Significado |
|-----|--------|--------------|-------------|
| 0 | `x` | `(N,)` o `(N, K)` | **solución** de mínimos cuadrados |
| 1 | `residuals` | `(K,)` o `(1,)` / **vacío** | suma de residuos al cuadrado $\lVert A\mathbf{x}-\mathbf{b}\rVert_2^2$. **Vacío** `(0,)` si `rank < N` o el sistema **no** está sobredeterminado |
| 2 | `rank` | `int` | rango efectivo de `a` (tras el corte por `rcond`) |
| 3 | `s` | `(min(M, N),)` | **valores singulares** de `a`, en orden decreciente |

- `x` se promueve a punto flotante (`float64`, o `complex` si la entrada es compleja).
- **`residuals` es la trampa más común**: viene **vacío** cuando $M \le N$ o cuando $A$ no es de rango
  completo; en ese caso hay que calcular el error a mano.

```python
x, residuals, rank, s = np.linalg.lstsq(A, yd, rcond=None)
x           # coeficientes
residuals   # suma de residuos al cuadrado (o array vacío)
rank        # rango efectivo de A
s           # valores singulares de A
```

## Casos de uso

### Ajuste de una recta $y = m x + c$ (uso estrella)
Cuatro puntos $(0,1),(1,3),(2,4),(3,6)$ generan un sistema **sobredeterminado** ($M=4$ ecuaciones,
$N=2$ incógnitas). La **matriz de diseño** $A$ (columnas $[x,\,1]$) y el lado $\mathbf{b}=\mathbf{y}$:

$$
\underbrace{\begin{bmatrix} 0 & 1 \\ 1 & 1 \\ 2 & 1 \\ 3 & 1 \end{bmatrix}}_{A\ (4\times 2)}
\begin{bmatrix} m \\ c \end{bmatrix}
\;\approx\;
\underbrace{\begin{bmatrix} 1 \\ 3 \\ 4 \\ 6 \end{bmatrix}}_{\mathbf{b}\ (4,)}
\quad\xrightarrow{\ \text{lstsq}\ }\quad
\begin{bmatrix} m \\ c \end{bmatrix}
\approx
\begin{bmatrix} 1.6 \\ 1.1 \end{bmatrix}
$$

No hay recta que pase por los cuatro puntos: `lstsq` devuelve la que **minimiza**
$\lVert A\mathbf{x}-\mathbf{b}\rVert_2$. Las **cuatro salidas** de la tupla:

```python
xd = np.array([0., 1., 2., 3.])
yd = np.array([1., 3., 4., 6.])
A = np.vstack([xd, np.ones_like(xd)]).T   # (4, 2)  columnas: [x, 1]
x, residuals, rank, s = np.linalg.lstsq(A, yd, rcond=None)
x            # [1.6, 1.1]   → (m, c), la solución (N,) = (2,)
residuals    # [0.2]        → suma de residuos al cuadrado, (1,)
rank         # 2            → rango efectivo de A (= N: rango completo)
s            # [4.10, 1.09] → valores singulares de A, (min(M,N),) = (2,)
```

### Regresión lineal multivariable
```python
X = np.array([[1., 0.],
              [1., 1.],
              [1., 2.],
              [1., 3.]])     # columna de unos (intercepto) + variable
y = np.array([1., 2., 2.5, 4.])
coef, *_ = np.linalg.lstsq(X, y, rcond=None)
coef                          # [intercepto, pendiente]
```

### Ajuste polinómico vía matriz de Vandermonde
```python
xd = np.linspace(0, 1, 5)
yd = xd**2 + 0.1
V = np.vander(xd, 3)          # Vandermonde grado 2: columnas [x², x, 1]
coef = np.linalg.lstsq(V, yd, rcond=None)[0]
coef                          # coeficientes del polinomio de grado 2
```

### Varios objetivos a la vez (N-D en `b`)
```python
A = np.random.rand(15, 2)
B = np.random.rand(15, 3)    # 3 objetivos
x, res, *_ = np.linalg.lstsq(A, B, rcond=None)
x.shape, res.shape           # (2, 3), (3,)  → una solución y un residuo por columna
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `residuals` vacío inesperado | `rank < N` o sistema no sobredeterminado | calcular `np.sum((A @ x - b)**2)` a mano |
| `FutureWarning` sobre `rcond` | no pasar `rcond` explícito | usar `rcond=None` |
| Desempaquetado falla | tratar el retorno como un solo array | recordar la tupla `(x, residuals, rank, s)`; indexar `[0]` para solo `x` |
| `LinAlgError: SVD did not converge` | datos con `inf`/`NaN` | limpiar la entrada; comprobar `np.isfinite(a)` |
| Usar `lstsq` en sistema cuadrado exacto | no es lo más directo | usar [[np.linalg.solve]] (más barato y preciso) |

## Notas relacionadas

- [[concepto_shape]] — el mapa $(M,N),(M,)\to(N,)$ del ajuste
- [[concepto_vectorizacion]] — resolver varios objetivos con una sola SVD
- [[np.linalg.solve]] — para sistemas cuadrados exactos
- [[np.linalg.pinv]] — la pseudo-inversa, reutilizable, detrás de mínimos cuadrados
- [[np.linalg.tensorsolve]] — la versión tensorial (caso cuadrado N-D)
- [[index]] — sistemas de ecuaciones
