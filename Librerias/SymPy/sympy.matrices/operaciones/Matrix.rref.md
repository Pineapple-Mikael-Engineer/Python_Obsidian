---
title: Matrix.rref — forma escalonada reducida por filas
aliases:
  - rref
  - forma escalonada reducida
  - RREF
tags:
  - sympy
  - api/metodo
  - matrices/operaciones
lib: sympy
mod: sympy.matrices
tipo: metodo
obj: Matrix
retorna: tuple
requiere:
  - Matrix
draft: false
---

# Matrix.rref — forma escalonada reducida por filas

Transforma una [[Matrix]] (no necesariamente cuadrada) a su **forma escalonada reducida por filas** (Reduced Row Echelon Form, RREF) mediante operaciones elementales de fila exactas. Devuelve una tupla con la matriz reducida y la posicion de los **pivotes** (columnas pivote), que indica el rango de la matriz y que variables son libres en un sistema asociado. Es la herramienta central para resolver sistemas lineales, hallar el rango, y construir bases del espacio nulo.

## Firma

```python
M.rref(iszerofunc=<lambda>, simplify=False, pivots=True, normalize_last=True)
```

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `iszerofunc` | `callable` | Funcion para decidir si una expresion es cero; por defecto `_iszero` simbolico |
| `simplify` | `bool \| callable` | Si simplificar durante la eliminacion; util con simbolos complejos |
| `pivots` | `bool` | Si devolver la tupla `(matriz, pivotes)` o solo la matriz |
| `normalize_last` | `bool` | Si normalizar las columnas pivote al final (default `True`) |

## Valor de retorno

Cuando `pivots=True` (default):

| Componente | Tipo | Descripcion |
|-----------|------|-------------|
| `[0]` | `Matrix` | La matriz en forma RREF |
| `[1]` | `tuple[int]` | Indices de las columnas pivote (base del espacio columna) |

El **rango** de la matriz es `len(pivotes)`.

## Casos de uso

```python
from sympy import Matrix

# --- matriz 3x3 singular (rango 2) ---
B = Matrix([[1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]])
R, pivs = B.rref()
# R    -> Matrix([[1, 0, -1], [0, 1, 2], [0, 0, 0]])
# pivs -> (0, 1)   -> columnas 0 y 1 son pivote; rango = 2

# --- extraer solo la matriz reducida ---
B.rref(pivots=False)
# Matrix([[1, 0, -1], [0, 1, 2], [0, 0, 0]])

# --- rango de la matriz ---
rango = len(B.rref()[1])   # 2

# --- sistema Ax = b: verificar consistencia ---
# Aumentada [A | b] -> aplicar rref y ver si aparece [0...0 | c] con c != 0
A = Matrix([[1, 2, 1],
            [2, 4, 3]])
# rref revela columnas pivote y variables libres
A.rref()
# (Matrix([[1, 2, 0], [0, 0, 1]]), (0, 2))
# -> columna 1 es libre; columnas 0 y 2 son pivote
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `pivots` devuelve menos columnas de lo esperado | Expresiones simbolicas que no se simplifican a cero | Usa `simplify=True` o añade supuestos a los simbolos |
| Resultado diferente segun el orden de filas | RREF es unica pero el pivoteo puede variar con ceros simbolicos | Pasa `iszerofunc=simplify` para mayor robustez |
| Error de desempaquetado | Olvidar que devuelve una tupla | Usa `R, pivs = M.rref()` o indexa con `[0]` y `[1]` |

## Notas relacionadas

- [[Matrix.nullspace]]
- [[Matrix.det]]
- [[Matrix.inv]]
- [[Matrix]]
- [[sympy.matrices/operaciones/index | operaciones]]
