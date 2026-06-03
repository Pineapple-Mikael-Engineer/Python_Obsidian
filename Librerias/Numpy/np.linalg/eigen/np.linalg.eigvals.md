---
title: np.linalg.eigvals — Solo autovalores de matriz general
aliases:
  - eigvals
  - linalg.eigvals
  - np.linalg.eigvals
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

# np.linalg.eigvals — Solo autovalores de matriz general

## Firma de la función

```python
np.linalg.eigvals(a) -> ndarray
```

Donde `a` es una matriz **cuadrada general** de [[concepto_shape|shape]] `(..., M, M)`.

## Valor de retorno

Devuelve **un solo `ndarray`** (no una tupla): los autovalores de `a`, sin los autovectores. Es la versión barata de [[np.linalg.eig]] cuando no necesitas la matriz `v`.

| Salida | Shape | Contenido |
|--------|-------|-----------|
| `w` | `(..., M)` | Autovalores, **1D**, sin ordenar. Pueden ser **complejos** aunque `a` sea real |

```python
import numpy as np
a = np.array([[2.0, 0.0],
              [0.0, 3.0]])
np.linalg.eigvals(a)   # array([2., 3.])

# Real pero con autovalores complejos (rotación):
r = np.array([[0.0, -1.0],
              [1.0,  0.0]])
np.linalg.eigvals(r)   # array([0.+1.j, 0.-1.j])
```

## Parámetros en detalle

### `a` — matriz de entrada

Array de shape `(..., M, M)`: una o varias matrices cuadradas apiladas. No requiere simetría.

```python
lote = np.random.rand(4, 3, 3)
np.linalg.eigvals(lote).shape   # (4, 3)  → autovalores por matriz
```

## Casos de uso

| Caso | Idea |
|------|------|
| Estabilidad | Mirar el signo de `Re(w)` sin calcular autovectores |
| Radio espectral | `max(abs(w))` → convergencia de métodos iterativos |
| Condicionamiento | Relación entre el mayor y menor autovalor en módulo |
| Determinante / traza | `det = prod(w)`, `traza = sum(w)` (chequeo de consistencia) |

```python
# Radio espectral: ¿converge x_{k+1} = a·x_k?
a = np.array([[0.5, 0.1], [0.2, 0.4]])
radio = np.max(np.abs(np.linalg.eigvals(a)))
radio < 1   # True → converge
```

## Buenas prácticas

1. Usa `eigvals` (no `eig`) cuando **solo** te interesen los autovalores: ahorra el cálculo de los autovectores.
2. Si la matriz es **simétrica/Hermitiana**, prefiere [[np.linalg.eigvalsh]]: autovalores reales y en orden ascendente.
3. Para obtener también los autovectores, cambia a [[np.linalg.eig]].
4. No asumas orden: `eigvals` no ordena el resultado.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Last 2 dimensions must be square` | matriz no cuadrada | verificar `a.shape[-1] == a.shape[-2]` |
| Esperar una tupla `(w, v)` | `eigvals` devuelve solo `w` | usar `eig` si quieres autovectores |
| Resultado complejo inesperado | matriz real no simétrica | correcto; usar `eigvalsh` si es simétrica |
| Orden inesperado de autovalores | `eigvals` no ordena | `np.sort(w)` o usar `eigvalsh` |

## Notas relacionadas

- [[np.linalg.eig]]
- [[np.linalg.eigvalsh]]
- [[np.linalg.eigh]]
- [[concepto_shape]]
