---
title: np.linalg.lstsq — Solución por mínimos cuadrados de Ax = b
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
draft: false
---

# np.linalg.lstsq — Solución por mínimos cuadrados de Ax = b

## Firma de la función

```python
np.linalg.lstsq(a, b, rcond=None) -> tuple  # (x, residuals, rank, s)
```

## Valor de retorno

Calcula la solución por **mínimos cuadrados** del sistema `a @ x = b`, minimizando `‖a x − b‖₂`. Es la herramienta base para **regresión lineal** y sistemas **sobredeterminados** (más ecuaciones que incógnitas). Devuelve una **tupla de cuatro elementos**.

| Posición | Nombre | Tipo / shape | Significado |
|----------|--------|--------------|-------------|
| 0 | `x` | `(N,)` o `(N, K)` | solución de mínimos cuadrados |
| 1 | `residuals` | `(K,)` o `(1,)` / vacío | suma de residuos al cuadrado `‖ax−b‖²` (vacío si `rank < N` o sistema no sobredeterminado) |
| 2 | `rank` | `int` | rango de `a` |
| 3 | `s` | `(min(M,N),)` | valores singulares de `a` |

```python
import numpy as np
# Ajuste de recta y = m*x + c por mínimos cuadrados
xd = np.array([0., 1., 2., 3.])
yd = np.array([1., 3., 4., 6.])
A = np.vstack([xd, np.ones_like(xd)]).T   # columnas: [x, 1]
m, c = np.linalg.lstsq(A, yd, rcond=None)[0]
m, c                                       # ≈ (1.6, 1.1)
```

## Valor de retorno (desempaquetado)

```python
x, residuals, rank, s = np.linalg.lstsq(A, yd, rcond=None)
x           # coeficientes [m, c]
residuals   # suma de residuos al cuadrado
rank        # 2  → A de rango completo
s           # valores singulares de A
```

## Parámetros en detalle

### `a` — matriz de diseño

Array de shape `(M, N)`. Para problemas sobredeterminados `M > N` (más filas/ecuaciones que columnas/incógnitas). El [[concepto_shape|shape]] del resultado `x` es `(N,)` o `(N, K)` según `b`.

### `b` — observaciones

Array de shape `(M,)` o `(M, K)`. Con `(M, K)` resuelve `K` problemas de mínimos cuadrados a la vez (cada columna independiente).

### `rcond` — corte de valores singulares

Valores singulares menores que `rcond * s.max()` se tratan como cero (regularización de rango). **Pásalo siempre explícito** (`rcond=None` usa el valor recomendado por la versión actual): omitirlo emite `FutureWarning` en versiones antiguas.

```python
np.linalg.lstsq(A, b, rcond=None)   # comportamiento estable recomendado
```

## Casos de uso

### Regresión lineal multivariable

```python
X = np.array([[1., 0.],
              [1., 1.],
              [1., 2.],
              [1., 3.]])     # columna de unos + variable
y = np.array([1., 2., 2.5, 4.])
coef, *_ = np.linalg.lstsq(X, y, rcond=None)
coef                          # [intercepto, pendiente]
```

### Ajuste polinómico (manual)

```python
xd = np.linspace(0, 1, 5)
yd = xd**2 + 0.1
V = np.vander(xd, 3)          # matriz de Vandermonde grado 2
coef = np.linalg.lstsq(V, yd, rcond=None)[0]
```

## Buenas prácticas

1. Desempaqueta siempre los 4 valores o indexa `[0]` para quedarte solo con `x`; no olvides que el retorno es una tupla.
2. Pasa `rcond=None` explícitamente para evitar warnings y obtener el comportamiento moderno.
3. Para sistemas cuadrados bien determinados usa [[np.linalg.solve]]; `lstsq` está pensado para sobredeterminados.
4. Si solo necesitas la matriz pseudo-inversa reutilizable, considera [[np.linalg.pinv]].
5. `residuals` viene vacío si el sistema no es sobredeterminado o si `rank < N`: calcula el error a mano en ese caso.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `FutureWarning` sobre `rcond` | no pasar `rcond` explícito | usar `rcond=None` |
| `residuals` vacío | `rank < N` o no sobredeterminado | calcular `‖A@x − b‖²` manualmente |
| `LinAlgError: SVD did not converge` | datos con `inf`/`NaN` | limpiar entrada; comprobar `np.isfinite` |
| Desempaquetado falla | tratar el retorno como un solo array | recordar que es tupla `(x, res, rank, s)` |
| `ValueError` de dimensiones | shapes de `a` y `b` incompatibles | `a` `(M, N)`, `b` `(M,)` o `(M, K)` |

## Limitaciones

- No regulariza más allá del corte por `rcond`; para regularización Tikhonov usa formulaciones explícitas.
- Para sistemas cuadrados exactos, `solve` es más directo y barato.

## Notas relacionadas

- [[np.linalg.solve]]
- [[np.linalg.pinv]]
- [[concepto_shape]]
