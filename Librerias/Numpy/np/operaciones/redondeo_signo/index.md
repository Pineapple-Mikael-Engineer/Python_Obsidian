---
title: np/operaciones/redondeo_signo — valor absoluto, signo y redondeo (ufuncs)
tags:
  - numpy
  - indice
draft: false
---

# np/operaciones/redondeo_signo — valor absoluto, signo y redondeo (ufuncs)

Las 4 [[concepto_ufuncs|ufuncs]] de valor absoluto, signo y redondeo de NumPy. Operan **elemento a elemento** sobre arrays de cualquier shape.

## Tabla de funciones

| ufunc | Descripcion | Soporta complejos | Resultado |
|---|---|---|---|
| [[np.abs]] | valor absoluto (alias de `np.absolute`) | si | mismo [[concepto_dtype\|dtype]] o float |
| [[np.fabs]] | valor absoluto flotante | no | siempre float |
| [[np.sign]] | signo del elemento | no | -1, 0 o +1 |
| [[np.ceil]] | redondeo hacia arriba (techo) | no | float (entero matematico) |

> [!note] Funciones de redondeo no cubiertas en este grupo
> `np.floor` (hacia abajo) y `np.rint` (al entero mas cercano) pertenecen al mismo dominio conceptual pero no estan en esta subcarpeta.

## Uso basico

```python
import numpy as np

x = np.array([-3.7, -1.0, 0.0, 2.3, 5.9])

np.abs(x)    # [3.7  1.   0.   2.3  5.9]
np.fabs(x)   # [3.7  1.   0.   2.3  5.9]  — siempre float
np.sign(x)   # [-1.  -1.   0.   1.   1.]
np.ceil(x)   # [-3.  -1.   0.   3.   6.]
```

### Diferencia entre `abs` y `fabs`

```python
z = np.array([3 + 4j, -2 + 0j])

np.abs(z)    # [5.  2.]   — soporta complejos: sqrt(re^2 + im^2)
np.fabs(z)   # TypeError  — no soporta numeros complejos
```

### `sign` para clasificar elementos

```python
errores = np.array([-0.5, 0.0, 1.2, -3.1, 0.8])

signos = np.sign(errores)   # [-1.  0.  1.  -1.  1.]
positivos = errores[signos == 1]    # [1.2  0.8]
negativos = errores[signos == -1]   # [-0.5  -3.1]
```

### `ceil` para calcular tamanos de buffer

```python
n_elementos = 17
tamano_bloque = 4

n_bloques = int(np.ceil(n_elementos / tamano_bloque))   # 5 bloques
```

## Broadcasting

```python
M = np.array([[-2.1, 3.7], [0.0, -5.5]])

np.abs(M)    # [[2.1  3.7], [0.  5.5]]
np.sign(M)   # [[-1.  1.], [0.  -1.]]
np.ceil(M)   # [[-2.  4.], [0.  -5.]]
```

## Notas de este grupo

- [[np.abs]]
- [[np.fabs]]
- [[np.sign]]
- [[np.ceil]]

## Notas relacionadas

- [[concepto_ufuncs]]
- [[concepto_broadcasting]]
- [[Librerias/Numpy/np/operaciones/index|np/operaciones — ufuncs element-wise]]
