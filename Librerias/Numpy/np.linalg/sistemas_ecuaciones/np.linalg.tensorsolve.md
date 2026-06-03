---
title: np.linalg.tensorsolve — Resolver la ecuación tensorial ax = b
aliases:
  - tensorsolve
  - linalg.tensorsolve
  - np.linalg.tensorsolve
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: ndarray
inplace: false
draft: false
---

# np.linalg.tensorsolve — Resolver la ecuación tensorial ax = b

## Firma de la función

```python
np.linalg.tensorsolve(a, b, axes=None) -> ndarray
```

## Valor de retorno

Resuelve la ecuación tensorial `a x = b` para `x`, donde el producto se entiende como `np.tensordot(a, x, axes)`. Es la **generalización N-dimensional** de [[np.linalg.solve]]: internamente reordena y aplana `a` a una matriz cuadrada, resuelve y reconstruye `x` con la forma adecuada.

| Entrada `a` | Entrada `b` | Retorno `x` |
|-------------|-------------|-------------|
| `(2, 3, 4)` con `prod(b.shape)=2*3` | `(2, 3)` | `(4,)` |
| `(2, 3, 6, 4)` | `(2, 3)` | `(6, 4)` |
| `(M, M)` (caso 2D) | `(M,)` | `(M,)` equivale a `solve` |

La regla clave: las dimensiones de `a` que **no** corresponden a `b` forman el [[concepto_shape|shape]] de `x`, y el total de elementos de esas dimensiones debe igualar al de `b` para que el sistema aplanado sea cuadrado.

```python
import numpy as np
a = np.eye(2*3).reshape(2, 3, 2, 3)
b = np.arange(6).reshape(2, 3).astype(float)
x = np.linalg.tensorsolve(a, b)
x.shape                          # (2, 3)
np.allclose(np.tensordot(a, x, axes=2), b)   # True
```

## Parámetros en detalle

### `a` — tensor de coeficientes

Array cuyo producto de dimensiones "de salida" (las que se aparean con `x`) debe igualar el producto de las dimensiones "de entrada" (las que se aparean con `b`), de modo que la matriz aplanada sea cuadrada.

### `b` — tensor del lado derecho

Su shape define qué ejes de `a` se contraen; el resto de ejes de `a` quedan para `x`.

### `axes` — ejes de `a` reordenados al final

Lista de ejes de `a` que se mueven al final antes de invertir. Por defecto (`None`) usa el orden natural. Útil cuando los ejes que forman `x` no son los últimos.

```python
a = np.random.randn(3, 4, 6, 2)   # 6*2 = 3*4 = 12 → cuadrado al aplanar
b = np.random.randn(3, 4)
x = np.linalg.tensorsolve(a, b)
x.shape                            # (6, 2)
```

## Casos de uso

### Sistema tensorial de transformaciones multieje

```python
a = np.eye(24).reshape(2, 3, 4, 4, 3, 2)   # aplana a (24, 24)
b = np.random.randn(2, 3, 4)
x = np.linalg.tensorsolve(a, b)
x.shape                                     # (4, 3, 2)
```

### Equivalencia con solve en 2D

```python
A = np.array([[3., 1.], [1., 2.]])
b = np.array([9., 8.])
np.linalg.tensorsolve(A, b)   # [2., 3.]  → igual que solve(A, b)
```

## Buenas prácticas

1. Para sistemas matriciales corrientes `Ax = b`, usa directamente [[np.linalg.solve]]: más claro y sin necesidad de razonar sobre ejes.
2. Verifica que el tensor aplanado sea cuadrado: `prod(dims_x) == prod(b.shape)`.
3. Usa `axes` para colocar explícitamente los ejes de `x` cuando no son los últimos de `a`.
4. Comprueba la solución con `np.tensordot(a, x, axes=b.ndim)`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Singular matrix` | el tensor aplanado es singular | revisar `a`; usar mínimos cuadrados manual |
| `ValueError` al aplanar | dimensiones no forman matriz cuadrada | ajustar shapes o `axes` para igualar productos |
| `x` con shape inesperado | ejes mal asignados | especificar `axes` explícitamente |

## Limitaciones

- Requiere que el problema sea cuadrado al aplanar; no resuelve casos sobre/infradeterminados.
- Menos intuitiva que `solve`; reservarla para problemas genuinamente N-dimensionales.

## Notas relacionadas

- [[np.linalg.solve]]
- [[np.linalg.lstsq]]
- [[concepto_shape]]
