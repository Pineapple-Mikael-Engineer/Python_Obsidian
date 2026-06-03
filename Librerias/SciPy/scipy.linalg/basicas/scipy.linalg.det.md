---
title: scipy.linalg.det — determinante de una matriz cuadrada
aliases:
  - det
  - scipy.linalg.det
  - determinante
tags:
  - scipy
  - api/funcion
  - algebra-lineal
lib: scipy
tipo: funcion
mod: scipy.linalg
retorna: float
requiere:
  - numpy
  - concepto_relacion_numpy
draft: false
---

# scipy.linalg.det — determinante de una matriz cuadrada

Calcula el determinante de una matriz cuadrada `(n, n)` mediante factorizacion LU (LAPACK): el determinante es el producto de los pivotes de `U` por el signo de las permutaciones. Devuelve un **escalar** (`float`, o `complex` si la matriz lo es). Como toda `scipy.linalg`, usa siempre BLAS/LAPACK; ver [[concepto_relacion_numpy]].

> Nota numerica: `det(a) ≈ 0` es **mala señal** (matriz casi singular), pero un determinante pequeño no prueba singularidad y uno grande no prueba lo contrario, porque escala como `λⁿ`. Para decidir si una matriz es invertible, fiate del **numero de condicion** `np.linalg.cond(a)` o del **rango** `np.linalg.matrix_rank(a)`, no de comparar el determinante con cero.

## Firma

```python
scipy.linalg.det(
    a,                   # array (n, n): matriz cuadrada
    overwrite_a=False,   # bool: permite sobrescribir 'a' (ahorra memoria)
    check_finite=True,   # bool: valida ausencia de NaN/inf (False -> mas rapido, inseguro)
) -> float
```

## Valor de retorno

| Salida | Tipo | Significado |
|--------|------|-------------|
| `d` | `float` (o `complex`) | Determinante escalar de `a` |

```python
d = det(A)   # escalar, no array
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Determinante basico | `det(A)` |
| Sobrescribiendo la entrada | `det(A, overwrite_a=True)` |
| Sin validar finitud (bucle critico) | `det(A, check_finite=False)` |

## Parametros en detalle

### `a` (obligatorio)

Matriz cuadrada `(n, n)`. La factorizacion LU es `O(n³)`; no es una operacion barata para matrices grandes.

```python
import numpy as np
from scipy.linalg import det

A = np.array([[3.0, 2.0], [1.0, 4.0]])
d = det(A)
d    # → 10.0   (3·4 − 2·1)
```

### `overwrite_a`

Si `True`, LAPACK puede reutilizar la memoria de `a` (ahorra una copia); tras la llamada `a` queda en estado indefinido. Usalo solo si no necesitas la matriz original.

### `check_finite`

Con `True` (defecto) valida que no haya `NaN`/`inf` antes de llamar a LAPACK. `False` ahorra el chequeo en codigo de rendimiento con datos ya saneados, a riesgo de resultados sin sentido si entran no-finitos.

## Casos de uso

### Comprobar (con cautela) si un sistema tiene solucion unica

```python
import numpy as np
from scipy.linalg import det

A = np.array([[2.0, 4.0], [1.0, 2.0]])   # fila 2 = mitad de fila 1
det(A)                       # → 0.0  -> singular, sin solucion unica
np.linalg.matrix_rank(A)     # → 1    -> confirmacion mas fiable
```

### Determinante como factor de escala (jacobiano)

```python
# El |det| de la matriz jacobiana es el factor de cambio de volumen
J = np.array([[2.0, 0.0], [0.0, 3.0]])   # estira x2 en X, x3 en Y
escala = abs(det(J))
escala    # → 6.0   (el area se multiplica por 6)
```

### Riesgo de overflow/underflow en matrices grandes

```python
# Determinante de una matriz grande: el producto de n pivotes desborda
B = np.diag(np.full(500, 10.0))   # det = 10**500
det(B)                            # → inf  (overflow!)
sign, logdet = np.linalg.slogdet(B)
sign, logdet    # → (1.0, 1151.29...)  estable: trabaja en log
```

## Buenas practicas

1. No uses `det(a) == 0` como test de singularidad; usa `np.linalg.cond(a)` o `matrix_rank`.
2. Para matrices grandes o casi singulares usa `np.linalg.slogdet`, que devuelve `(signo, log|det|)` y evita overflow/underflow.
3. Recuerda que el determinante escala como `λⁿ`: su magnitud depende de la escala de los datos, no solo del condicionamiento.
4. Si solo quieres resolver un sistema, no calcules el determinante: ve directo a `solve`.
5. Deja `check_finite=True` salvo en bucles criticos con datos validados.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Usar `det≈0` como prueba de singularidad | El determinante escala con la magnitud | Usar `cond` o `matrix_rank` |
| `det` devuelve `inf` o `0.0` espurio | Overflow/underflow del producto de pivotes | Usar `np.linalg.slogdet` |
| `ValueError: ... must be square` | `a` no es `(n, n)` | El determinante solo existe para cuadradas |
| Esperar un array de salida | `det` devuelve un escalar | Tratar el resultado como `float` |
| Comparacion exacta `det(A) == 0` | Error de redondeo flotante | Comparar con tolerancia o usar el rango |

## Limitaciones

- Solo definido para matrices **cuadradas**.
- Numericamente fragil como indicador de singularidad: el numero de condicion es mas informativo.
- Propenso a overflow/underflow en dimension alta; preferir `slogdet` para trabajar en escala logaritmica.
- Coste `O(n³)`: caro para matrices grandes y rara vez necesario en algebra lineal numerica practica.

## Notas relacionadas

- [[scipy.linalg.solve]]
- [[scipy.linalg.inv]]
- [[concepto_relacion_numpy]]
