---
title: np.linalg — determinantes
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — determinantes

El **determinante** es un único escalar que se extrae de una matriz cuadrada y que resume dos cosas:
**si la matriz es invertible** ($\det \neq 0$) y **cómo escala el volumen** la transformación lineal
que representa (en valor absoluto). Esta carpeta cubre las dos formas de obtenerlo en NumPy —
[[np.linalg.det]] (el valor directo) y [[np.linalg.slogdet]] (signo y logaritmo, estable) — y cuándo
elegir cada una.

## Qué mide el determinante

- **Factor de escala de volumen.** $|\det A|$ es el factor por el que la transformación $x \mapsto Ax$
  multiplica volúmenes. Un cubo unidad pasa a tener volumen $|\det A|$. Si $\det A < 0$, además
  **invierte la orientación** (reflexión).
- **Singularidad / invertibilidad.** $\det A = 0$ ⟺ la matriz es **singular** (no invertible): colapsa
  el espacio a una dimensión menor (volumen 0). Es la lectura más usada en la práctica.
- **Producto de autovalores.** $\det A = \prod_i \lambda_i$. Por eso un autovalor nulo implica
  $\det = 0$, y un determinante negativo significa un número impar de autovalores negativos.

$$
\det A = 0 \;\Longleftrightarrow\; A \text{ singular}
\qquad\qquad
|\det A| = \text{factor de volumen}
\qquad\qquad
\det A = \prod_i \lambda_i
$$

Ambas funciones aceptan **pilas** de matrices `(..., n, n)` y colapsan los dos últimos ejes a un
escalar por matriz, dejando intacto el lote (ver [[concepto_shape]]).

## `det` vs `slogdet`: el problema del overflow

El determinante es un **producto de $n$ pivotes**, así que crece o decae **exponencialmente** con el
tamaño. Para matrices grandes [[np.linalg.det]] **desborda a `inf`** o **subdesborda a `0`** con
facilidad, perdiendo toda la información. [[np.linalg.slogdet]] resuelve esto trabajando en escala
logarítmica: devuelve `(sign, logabsdet)` con $\det = \text{sign}\cdot e^{\text{logabsdet}}$, donde
`logabsdet` se mantiene en un rango manejable aunque el determinante real sea astronómico.

| Función | Qué devuelve | Estabilidad | Cuándo |
|---|---|---|---|
| [[np.linalg.det]] | el determinante directo (escalar/ndarray) | overflow/underflow en matrices grandes | matrices pequeñas, valor exacto necesario |
| [[np.linalg.slogdet]] | `(sign, logabsdet)`, namedtuple | estable a cualquier tamaño | matrices grandes, valores dispares, $\log\det$ |

| Situación | Función recomendada |
|---|---|
| Matriz pequeña (< ~10×10), se quiere el valor concreto | [[np.linalg.det]] |
| Matriz grande o con valores muy pequeños/grandes | [[np.linalg.slogdet]] |
| Estadística / ML (log-verosimilitud, $\log\det\Sigma$) | [[np.linalg.slogdet]] |
| Solo importa si $\det \neq 0$ (invertibilidad) | [[np.linalg.det]] o `np.linalg.matrix_rank` |

## Relación con `inv`, `eigvals` y `matrix_rank`

El determinante es un punto de unión de toda el álgebra lineal de `np.linalg`:

- **`inv`** — $A^{-1}$ existe ⟺ $\det A \neq 0$. Comprobar el determinante (con `np.isclose`, no `== 0`)
  antes de invertir evita un `LinAlgError`. Pero **no** uses la regla de Cramer (`det`) para resolver
  sistemas: para eso está `np.linalg.solve`, más rápido y estable.
- **`eigvals`** — $\det A = \prod_i \lambda_i$. El determinante y los autovalores cuentan la misma
  historia sobre singularidad desde dos ángulos.
- **`matrix_rank`** — para decidir invertibilidad de forma **robusta**, el rango (vía SVD) suele ser
  mejor termómetro que el determinante: dice cuántas dimensiones "sobreviven", sin sufrir el
  overflow del producto de pivotes.

## Relación entre `det` y `slogdet`

`slogdet` devuelve `(sign, logabsdet)` tal que `det = sign * exp(logabsdet)`. Reconstruir el
determinante es exacto, pero **anula la ventaja** si el objetivo era evitar el overflow (exponenciar
vuelve a desbordar): cuando puedas, trabaja con `logabsdet` directamente.

```python
import numpy as np
A = np.array([[1., 2.], [3., 4.]])

np.linalg.det(A)               # -2.0
sign, logabsdet = np.linalg.slogdet(A)
sign * np.exp(logabsdet)       # -2.0  → mismo resultado, ruta estable
```
