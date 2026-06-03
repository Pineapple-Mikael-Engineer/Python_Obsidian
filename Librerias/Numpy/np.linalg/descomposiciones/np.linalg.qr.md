---
title: np.linalg.qr — Descomposición QR (ortogonal · triangular)
aliases:
  - qr
  - linalg.qr
  - np.linalg.qr
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: tuple (Q, R) o ndarray según mode
inplace: false
draft: false
---

# np.linalg.qr — Descomposición QR (ortogonal · triangular)

Factoriza una matriz `a` como `a = Q @ R`, donde `Q` tiene columnas **ortonormales** y `R` es **triangular superior**. Es la herramienta estándar para resolver mínimos cuadrados y para ortogonalizar bases de forma numéricamente estable (alternativa robusta a Gram-Schmidt).

## Firma de la función

```python
np.linalg.qr(
    a,
    mode='reduced'
) -> tuple[ndarray, ndarray] | ndarray
```

## Valor de retorno

Para una entrada `a` de [[concepto_shape|shape]] `(M, N)` y `K = min(M, N)`, el retorno depende de `mode`:

| `mode` | Retorno | Shapes | Descripción |
|--------|---------|--------|-------------|
| `'reduced'` (defecto) | **tupla** `(Q, R)` | `Q (M, K)`, `R (K, N)` | Forma económica; suficiente para `a = Q @ R` |
| `'complete'` | **tupla** `(Q, R)` | `Q (M, M)`, `R (M, N)` | `Q` cuadrada y ortogonal completa |
| `'r'` | **solo** `R` (ndarray) | `R (K, N)` | Únicamente la triangular superior |
| `'raw'` | **tupla** `(h, tau)` | `h (N, M)`, `tau (K,)` | Reflectores de Householder crudos (uso avanzado/LAPACK) |

En los modos `'reduced'` y `'complete'` se cumple que `Q.T @ Q = I` (columnas ortonormales) y `R` es triangular superior.

```python
import numpy as np
A = np.array([[1.0, 2.0],
              [3.0, 4.0],
              [5.0, 6.0]])          # shape (3, 2)

Q, R = np.linalg.qr(A)             # mode='reduced'
Q.shape    # (3, 2)
R.shape    # (2, 2)   → triangular superior
np.allclose(A, Q @ R)             # True
np.allclose(Q.T @ Q, np.eye(2))   # True  → columnas ortonormales
```

## Parámetros en detalle

### `a` — matriz de entrada

Array de shape `(..., M, N)`. Admite **stacks**: las dimensiones iniciales actúan como lote y la QR se calcula sobre cada matriz `(M, N)` final.

```python
lote = np.random.rand(4, 5, 3)    # 4 matrices 5×3
Q, R = np.linalg.qr(lote)
Q.shape                           # (4, 5, 3)
R.shape                           # (4, 3, 3)
```

### `mode` — variante de la descomposición

Controla qué se devuelve y los tamaños (ver tabla de retorno). Reglas prácticas:

- `'reduced'`: el habitual; barato y suficiente para reconstruir `a`.
- `'complete'`: cuando necesitas la base ortonormal completa del espacio (incluido el complemento ortogonal).
- `'r'`: cuando solo te interesa `R` (p. ej. para resolver el sistema triangular en mínimos cuadrados).

```python
R = np.linalg.qr(A, mode='r')          # devuelve solo R (un array)
Qc, Rc = np.linalg.qr(A, mode='complete')
Qc.shape                               # (3, 3)
```

## Casos de uso

### Mínimos cuadrados (sistema sobredeterminado)

```python
# Resolver A x ≈ b con A de shape (m, n), m > n
Q, R = np.linalg.qr(A)
x = np.linalg.solve(R, Q.T @ b)        # R x = Qᵀ b (triangular, barato)
```

### Ortonormalizar un conjunto de vectores

```python
V = np.random.rand(5, 3)               # 3 vectores columna en R^5
Q, _ = np.linalg.qr(V)                 # columnas de Q: base ortonormal
np.allclose(Q.T @ Q, np.eye(3))        # True
```

### Estabilidad numérica frente a Gram-Schmidt

```python
# QR de Householder es estable incluso con columnas casi colineales
Q, R = np.linalg.qr(matriz_mal_condicionada)
```

## Buenas prácticas

1. Para mínimos cuadrados, QR es más estable que las ecuaciones normales `(AᵀA)x = Aᵀb`.
2. Usa `mode='reduced'` (defecto) salvo que necesites el espacio ortogonal completo.
3. `R` es triangular superior: aprovéchalo con [[np.linalg.solve]] o una sustitución hacia atrás en vez de invertir.
4. Si solo necesitas `R`, usa `mode='r'` y evita calcular `Q`.
5. Las columnas de `Q` ya están ortonormalizadas: úsalas directamente como base.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError` al converger | entrada con `NaN`/`inf` | validar con `np.isfinite(a).all()` |
| Esperar `Q` con `mode='r'` | ese modo devuelve **solo** `R` | usar `'reduced'`/`'complete'` si quieres `Q` |
| `R` no parece triangular | confundir `R` con `Q`, o lote mal interpretado | recordar el orden `(Q, R)` y el shape `(M, N)` |
| `ValueError` al desempaquetar | `mode='r'` no devuelve tupla | asignar a una sola variable |
| `Q @ R` no reconstruye `a` | mezclar resultados de modos distintos | usar el `Q` y `R` del mismo `mode` |

## Notas relacionadas

- [[concepto_shape]]
- [[np.linalg.svd]]
- [[np.linalg.solve]]
- [[np.linalg.cholesky]]
- [[np.linalg.lstsq]]
