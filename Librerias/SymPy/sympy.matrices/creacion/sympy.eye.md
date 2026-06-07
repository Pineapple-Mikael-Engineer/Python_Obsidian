---
title: sympy.eye — identidad n x n (o n x m)
aliases:
  - eye
  - identidad
tags:
  - sympy
  - api/funcion
  - matrices/creacion
lib: sympy
mod: sympy.matrices
tipo: funcion
retorna: Matrix
requiere:
  - Matrix
draft: false
---

# sympy.eye — identidad n x n (o n x m)

`eye(n)` devuelve la **matriz identidad** n×n: unos en la diagonal principal y ceros en el resto. Con `eye(n, m)` genera una version rectangular n×m donde los 1s siguen la diagonal (posicion `(i, i)`) hasta agotarse. Es el equivalente simbolico de `numpy.eye` pero devuelve una [[Matrix]] exacta de SymPy, util para construir sistemas lineales, transformaciones y matrices de bloques. Se usa en ingenieria cuando se necesita una base identidad o un punto de partida para modificaciones elemento a elemento.

## Firma

```python
sympy.eye(
    n,        # int: numero de filas
    m=None,   # int opcional: numero de columnas; si None -> cuadrada n x n
) -> Matrix
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Matrix` | n x n (o n x m) | Matriz con 1 en la diagonal y 0 en el resto |

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Identidad cuadrada n x n | `eye(n)` |
| Rectangular n x m con diagonal 1 | `eye(n, m)` |

```python
from sympy import eye
eye(3)      # Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
eye(2, 3)   # Matrix([[1, 0, 0], [0, 1, 0]])
eye(3, 2)   # Matrix([[1, 0], [0, 1], [0, 0]])
```

## Parametros en detalle

### `n` (obligatorio)

Numero de **filas** de la matriz. Debe ser un entero no negativo.

```python
from sympy import eye
eye(1)   # Matrix([[1]])
eye(4)   # Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
```

### `m` (opcional, defecto `None`)

Numero de **columnas**. Si se omite o es `None`, la matriz es cuadrada (`m = n`). Cuando `m != n` la diagonal se extiende hasta `min(n, m)` posiciones.

```python
from sympy import eye
eye(2, 3)   # Matrix([[1, 0, 0], [0, 1, 0]])
eye(3, 2)   # Matrix([[1, 0], [0, 1], [0, 0]])
```

## Casos de uso

### Identidad como termino neutro en algebra matricial

```python
from sympy import eye, symbols
x = symbols("x")
A = eye(3)
A[0, 0] = x          # modificar un elemento sin perder el resto
A                    # Matrix([[x, 0, 0], [0, 1, 0], [0, 0, 1]])
```

### Construir A - lambda*I para autovalores

```python
from sympy import eye, Matrix, symbols
lam = symbols("lambda")
A = Matrix([[3, 1], [0, 2]])
char = A - lam * eye(2)   # Matrix([[3 - lambda, 1], [0, 2 - lambda]])
char.det()                # (3 - lambda)*(2 - lambda)
```

### Bloque identidad dentro de una matriz de bloques

```python
from sympy import eye, diag
M = diag(eye(2), 5)   # Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 5]])
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `eye(2.0)` falla | `n` debe ser entero, no flotante | Usar `eye(int(n))` |
| Confundir `eye(n, m)` con la forma NumPy | El orden es siempre `(filas, columnas)` al igual que NumPy | Correcto: `eye(2, 3)` → 2 filas, 3 columnas |
| Modificar la matriz original sin copiar | `Matrix` es mutable en SymPy | Si se quiere preservar: `B = A.copy()` antes de modificar |

## Notas relacionadas

- [[sympy.zeros]]
- [[sympy.ones]]
- [[sympy.diag]]
- [[sympy.matrices/creacion/index | creacion]]
- [[sympy.matrices/index | sympy.matrices]]
