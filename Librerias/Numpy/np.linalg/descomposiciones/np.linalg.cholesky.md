---
title: np.linalg.cholesky — Descomposición de Cholesky (matriz definida positiva)
aliases:
  - cholesky
  - linalg.cholesky
  - np.linalg.cholesky
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: ndarray (L triangular inferior)
inplace: false
draft: false
---

# np.linalg.cholesky — Descomposición de Cholesky (matriz definida positiva)

Factoriza una matriz **hermítica definida positiva** `a` como `a = L @ L.conj().T`, donde `L` es **triangular inferior**. Es el doble de eficiente que una descomposición LU (aprovecha la simetría) y es el método preferido para resolver sistemas con matrices de covarianza, simular gaussianas multivariantes y comprobar la definición positiva.

## Firma de la función

```python
np.linalg.cholesky(
    a
) -> ndarray
```

## Valor de retorno

Devuelve un **único ndarray** `L` (no una tupla), triangular inferior, tal que `a = L @ L.conj().T`. Para una entrada de [[concepto_shape|shape]] `(N, N)`:

| Salida | Shape | Propiedad |
|--------|-------|-----------|
| `L` | `(N, N)` | Triangular **inferior**: ceros por encima de la diagonal |

Relación de reconstrucción: `a == L @ L.conj().T` (con datos reales, `a == L @ L.T`).

```python
import numpy as np
A = np.array([[4.0, 2.0],
              [2.0, 3.0]])          # simétrica definida positiva

L = np.linalg.cholesky(A)          # shape (2, 2)
L
# [[2.        , 0.        ],
#  [1.        , 1.41421356]]        → triangular inferior

np.allclose(A, L @ L.T)            # True
```

**Importante:** NumPy devuelve la factor **inferior** `L` (convención `a = L Lᴴ`). Si necesitas la superior, usa `L.conj().T`.

## Parámetros en detalle

### `a` — matriz de entrada

Array de shape `(..., N, N)` que debe ser **hermítico definido positivo** (simétrico definido positivo en el caso real). Admite **stacks**: las dimensiones iniciales son lote y la factorización se aplica a cada matriz `(N, N)`.

```python
lote = np.array([[[2.0, 0.0], [0.0, 2.0]],
                 [[4.0, 1.0], [1.0, 3.0]]])   # 2 matrices 2×2 SPD
L = np.linalg.cholesky(lote)
L.shape                                       # (2, 2, 2)
```

NumPy **solo lee el triángulo inferior** de `a`; aun así, la matriz debe ser realmente definida positiva o lanzará `LinAlgError`.

## Casos de uso

### Resolver un sistema SPD de forma eficiente

```python
# A x = b con A definida positiva
L = np.linalg.cholesky(A)
y = np.linalg.solve(L, b)             # L y = b   (triangular)
x = np.linalg.solve(L.conj().T, y)    # Lᴴ x = y  (triangular)
```

### Muestrear de una gaussiana multivariante

```python
# x ~ N(mu, Sigma)
L = np.linalg.cholesky(Sigma)
z = np.random.standard_normal(mu.shape)
x = mu + L @ z                        # tiene covarianza Sigma
```

### Comprobar si una matriz es definida positiva

```python
def es_definida_positiva(M):
    try:
        np.linalg.cholesky(M)
        return True
    except np.linalg.LinAlgError:
        return False
```

## Buenas prácticas

1. Úsala siempre que sepas que la matriz es **simétrica definida positiva** (covarianzas, Gram, Hessianas regulares): cuesta la mitad que LU.
2. Para resolver sistemas, encadena dos `solve` triangulares con `L` y `L.conj().T` en vez de invertir.
3. El fallo con `LinAlgError` es en sí mismo una prueba de que la matriz **no** es definida positiva.
4. Asegura simetría exacta antes de llamar (p. ej. `A = (A + A.T) / 2`) para evitar fallos por errores de redondeo.
5. NumPy devuelve `L` inferior; recuerda transponer/conjugar si tu fórmula espera la superior.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Matrix is not positive definite` | la matriz no es SPD (autovalor ≤ 0) | verificar con [[np.linalg.eigvalsh]]; regularizar sumando `εI` |
| Resultado inesperado | matriz no simétrica (NumPy solo lee el triángulo inferior) | simetrizar: `A = (A + A.T) / 2` |
| Esperar la triangular superior | NumPy devuelve `L` **inferior** | usar `L.conj().T` para la superior |
| `LinAlgError` por redondeo | SPD teórica pero numéricamente indefinida | añadir pequeño jitter en la diagonal |
| `LinAlgError: Last 2 dimensions...` | entrada no cuadrada o < 2D | pasar matriz cuadrada `(N, N)` |

## Notas relacionadas

- [[concepto_shape]]
- [[np.linalg.svd]]
- [[np.linalg.qr]]
- [[np.linalg.solve]]
- [[np.linalg.eigvalsh]]
