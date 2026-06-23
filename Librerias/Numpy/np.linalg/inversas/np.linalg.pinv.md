---
title: np.linalg.pinv — pseudoinversa de Moore-Penrose
aliases:
  - pinv
  - linalg.pinv
  - np.linalg.pinv
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

# np.linalg.pinv — pseudoinversa de Moore-Penrose

`np.linalg.pinv` calcula la **pseudoinversa de Moore-Penrose** $A^{+}$, la generalización de la
inversa que existe **para cualquier matriz**: rectangular, singular o cuadrada. Se construye a
partir de la [[np.linalg.svd|descomposición en valores singulares (SVD)]], invirtiendo los valores
singulares no nulos. Donde [[np.linalg.inv]] exige una matriz cuadrada e invertible, `pinv` siempre
devuelve algo: la mejor inversa "en sentido de mínimos cuadrados". Es la herramienta para sistemas
**sobredeterminados**, **mal condicionados** o **rango deficiente**.

## La idea en una fórmula

Vía SVD, si $A = U \Sigma V^{*}$, la pseudoinversa invierte $\Sigma$ (recíproco de cada valor
singular no nulo, ceros donde había ceros) y transpone:

$$
A^{+} = V\, \Sigma^{+}\, U^{*}
\qquad\text{con}\qquad
(\Sigma^{+})_{ii} = \begin{cases} 1/\sigma_i & \sigma_i > \tau \\ 0 & \sigma_i \le \tau \end{cases}
$$

donde $\tau$ es el umbral (`rcond`). Cumple las cuatro condiciones de Moore-Penrose; en particular
$A A^{+} A = A$. Si $A$ es cuadrada e invertible, $A^{+} = A^{-1}$ exactamente.

**El mapa de shapes** (entrada → salida, incluido el lote N-D) — nota que los dos últimos ejes se
**intercambian**:

$$
(\underbrace{\dots}_{\text{lote}},\, m,\, n)\ \xrightarrow{\ \text{pinv}\ }\ (\underbrace{\dots}_{\text{lote}},\, n,\, m)
$$

Una matriz $(m, n)$ produce una $(n, m)$: la pseudoinversa "transpone" la forma, igual que la
inversa de una aplicación lineal va del espacio de llegada al de salida.

## Firma

```python
np.linalg.pinv(
    a,                 # array_like (..., M, N): la matriz a pseudo-invertir
    rcond=1e-15,       # float | array_like: umbral relativo de valores singulares
    hermitian=False,   # bool: asumir a hermítica (simétrica si es real)
) -> ndarray
```

> En NumPy reciente, `rcond` se renombró a `rtol` (mismo significado, umbral relativo). `rcond`
> sigue funcionando como alias retrocompatible.

## Los parámetros en detalle

### `a` — la matriz de entrada
`array_like` de shape `(..., m, n)`. **No** necesita ser cuadrada ni invertible. El
[[concepto_shape|shape]] del resultado intercambia los dos últimos ejes a `(..., n, m)`. Se promueve
a flotante/complejo.

```python
A = np.array([[1., 0.], [0., 1.], [1., 1.]])   # (3, 2) rectangular
np.linalg.pinv(A).shape                         # (2, 3)
```

### `rcond` / `rtol` — umbral de valores singulares
`float` (o `array_like` para aplicar un umbral por matriz del lote). Los valores singulares menores
que `rcond * σ_max` (el mayor valor singular) se tratan como **cero** y no se invierten. Es el dial
de **regularización**: subirlo descarta direcciones casi degeneradas y estabiliza problemas mal
condicionados; bajarlo conserva más detalle (y más ruido).

```python
A = np.array([[1., 1.], [1., 1.0000001]])   # casi singular
np.linalg.pinv(A, rcond=1e-3)                # descarta el σ minúsculo → resultado estable
```

### `hermitian` — atajo para matrices hermíticas
`bool`. Si `True`, asume que `a` es hermítica (simétrica si es real) y usa la descomposición
espectral (eigendescomposición), **más rápida** que la SVD general. Solo pásalo si de verdad lo es;
si no, el resultado es incorrecto.

## El caso N-D

`pinv` también opera por lotes: los **dos últimos ejes** son la matriz y los anteriores el lote.

| `a.shape` | salida | caso |
|-----------|--------|------|
| `(m, n)`, `m>n` | `(n, m)` | sobredeterminado → mínimos cuadrados |
| `(m, n)`, `m<n` | `(n, m)` | infradeterminado → norma mínima |
| `(n, n)` no singular | `(n, n)` | coincide con `inv` |
| `(n, n)` singular | `(n, n)` | inversa generalizada (sin error) |
| `(k, m, n)` | `(k, n, m)` | `k` pseudoinversas en lote |

```python
pila = np.random.rand(6, 3, 2)   # 6 matrices 3×2
np.linalg.pinv(pila).shape       # (6, 2, 3)  → 6 pseudoinversas, sin bucle
```

## Vectorización

Como toda la familia `linalg`, el lote se resuelve en código compilado (LAPACK), no en un bucle
Python — el mismo principio de [[concepto_vectorizacion]]:

```python
# Bucle Python: una SVD por matriz del lote
def batch_pinv(T):
    out = np.empty((T.shape[0], T.shape[2], T.shape[1]))
    for i in range(T.shape[0]):
        out[i] = np.linalg.pinv(T[i])
    return out

# Vectorizado: NumPy recorre el lote en C / LAPACK
np.linalg.pinv(T)
```

## Valor de retorno

| Entrada (shape, dtype) | salida | tipo |
|---|---|---|
| `(m, n)` real | `(n, m)` | `ndarray` `float64` |
| `(m, n)` complejo | `(n, m)` | `ndarray` `complex128` |
| `(..., m, n)` pila | `(..., n, m)` | `ndarray` |
| `inf`/`NaN` en la entrada | — | `LinAlgError: SVD did not converge` |

Siempre flotante o complejo; el shape intercambia los dos últimos ejes. Nunca lanza por
singularidad (esa es la razón de existir frente a `inv`).

## Casos de uso

### Mínimos cuadrados explícitos (sistema sobredeterminado)
```python
A = np.array([[1., 1.], [1., 2.], [1., 3.]])   # 3 ecuaciones, 2 incógnitas
b = np.array([1., 2., 2.])
x = np.linalg.pinv(A) @ b      # solución de mínimos cuadrados
```

### Inversa de matriz singular sin error
```python
S = np.array([[1., 2.], [2., 4.]])   # singular (filas proporcionales)
np.linalg.pinv(S)                    # devuelve resultado en vez de LinAlgError
```

### Lote N-D de pseudoinversas
```python
np.random.seed(0)
T = np.random.rand(4, 3, 2)    # 4 matrices rectangulares 3×2
P = np.linalg.pinv(T)
P.shape                        # (4, 2, 3)
np.allclose(P[0] @ T[0], np.eye(2))   # True → A⁺A ≈ I (lado izquierdo, columnas indep.)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: SVD did not converge` | `inf`/`NaN` o datos patológicos | limpiar entrada; comprobar `np.isfinite` |
| Resultado dominado por ruido | `rcond` demasiado bajo | subir `rcond`/`rtol` para descartar σ pequeños |
| Lentitud frente a `solve` | usar `pinv` en sistema cuadrado bien definido | usar `solve` o `inv` |
| Resultado incorrecto con `hermitian=True` | la matriz no era hermítica | dejar `hermitian=False` |
| Esperar exactitud bit a bit con `inv` | `pinv` pasa por SVD (más caro) | si es cuadrada y no singular, usar `inv` |

## Notas relacionadas

- [[np.linalg.svd]] — la descomposición sobre la que se construye la pseudoinversa
- [[np.linalg.lstsq]] — mínimos cuadrados directo (da residuos y rango), preferible a `pinv(A) @ b`
- [[np.linalg.inv]] — la inversa ordinaria (caso cuadrado no singular)
- [[concepto_shape]] — el mapa `(...,m,n) → (...,n,m)`
