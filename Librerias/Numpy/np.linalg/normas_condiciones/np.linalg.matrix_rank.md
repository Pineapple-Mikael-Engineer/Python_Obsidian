---
title: np.linalg.matrix_rank — Rango de una matriz vía SVD
aliases:
  - matrix_rank
  - linalg.matrix_rank
  - np.linalg.matrix_rank
tags:
  - numpy
  - api/funcion
  - algebra/matricial

# --- Clasificación ---
lib: numpy
mod: np.linalg
tipo: funcion

# --- Comportamiento ---
retorna: int
inplace: false

draft: false
---

# np.linalg.matrix_rank — Rango de una matriz vía SVD

## Firma de la función

```python
np.linalg.matrix_rank(
    A,
    tol=None,
    hermitian=False
) -> int
```

## Valor de retorno

Devuelve el **rango** de `A`: el número de filas/columnas **linealmente independientes**, equivalente al número de valores singulares mayores que una tolerancia. Se calcula contando valores singulares significativos de la SVD.

| Caso | Rango | Significado |
|------|-------|-------------|
| `(m, n)` rango completo | `min(m, n)` | sin dependencias lineales |
| rango deficiente | `< min(m, n)` | hay filas/columnas redundantes |
| matriz nula | `0` | todos los elementos cero |

```python
import numpy as np
A = np.array([[1, 2],
              [2, 4]])      # fila 2 = 2 × fila 1
np.linalg.matrix_rank(A)    # 1  → rango deficiente
np.linalg.matrix_rank(np.eye(3))   # 3  → rango completo
```

Para `A` con más de 2 dimensiones, opera sobre las pilas de matrices `(..., M, N)` y devuelve un `ndarray` de enteros.

## Parámetros en detalle

### `A` — array de entrada

Matriz `(M, N)` o pila de matrices `(..., M, N)`. No necesita ser cuadrada.

### `tol` — umbral de valor singular

Valores singulares por debajo de `tol` se consideran cero. Si es `None`, NumPy usa una tolerancia por defecto basada en el mayor valor singular y la precisión de máquina (`S.max() * max(M, N) * eps`). Súbelo si los datos tienen ruido.

```python
A = np.array([[1.0, 2.0],
              [2.0, 4.000001]])   # casi dependiente
np.linalg.matrix_rank(A)          # 2  → el ruido cuenta como independiente
np.linalg.matrix_rank(A, tol=1e-3)# 1  → tolerancia agresiva lo colapsa
```

### `hermitian` — matriz hermítica/simétrica

Si `True`, asume que `A` es hermítica (simétrica real) y usa una descomposición de autovalores más eficiente en lugar de la SVD general.

```python
S = np.array([[2.0, 1.0], [1.0, 2.0]])
np.linalg.matrix_rank(S, hermitian=True)   # 2
```

## Casos de uso

### Detectar columnas redundantes en datos

```python
X = np.array([[1, 2, 3],
              [2, 4, 6],
              [1, 0, 1]], dtype=float)
np.linalg.matrix_rank(X)   # 2  → una columna/fila es combinación de otras
```

### Comprobar si un sistema tiene solución única

```python
A = np.array([[1.0, 1.0], [1.0, 1.0]])
np.linalg.matrix_rank(A)   # 1 < 2  → sistema sin solución única
```

## Buenas prácticas

1. Con datos reales (ruidosos), ajusta `tol` en vez de fiarte del rango "exacto".
2. Para matrices simétricas/hermíticas, activa `hermitian=True` por rendimiento.
3. Rango `< min(M, N)` implica que la matriz es singular o el sistema es deficiente: revisa antes de invertir.
4. Combínalo con [[np.linalg.cond]] para distinguir "singular exacta" de "casi singular".

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Rango mayor del esperado | ruido numérico cuenta como independiente | subir `tol` |
| Rango menor del esperado | `tol` demasiado alto | bajar/quitar `tol` |
| Resultado inesperado en simétrica | no se usó la ruta eficiente | `hermitian=True` (solo si lo es de verdad) |
| `LinAlgError` durante la SVD | matriz con `NaN`/`inf` | limpiar valores no finitos antes |

## Notas relacionadas

- [[concepto_shape]]
- [[np.linalg.svd]]
- [[np.linalg.cond]]
- [[np.linalg.det]]
- [[np.linalg.matrix_rank|rango]]
